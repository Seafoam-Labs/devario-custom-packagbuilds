#!/usr/bin/env python3
"""Exercise the setup helper without a GPU, network, model downloads or server."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "devario-development/strata-bin/setup-strata"


class StrataSetup(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="devario-strata-test-")
        self.addCleanup(self.temporary.cleanup)
        self.work = Path(self.temporary.name)
        self.log = self.work / "calls.jsonl"
        self.env = dict(os.environ, XDG_DATA_HOME=str(self.work / "data"),
                        STRATA_BIN=str(self.work / "strata"),
                        STRATA_TEST_LOG=str(self.log),
                        PATH=f"{self.work}:{os.environ['PATH']}")
        self.env.pop("STRATA_TEST_RESULT", None)
        self.env.pop("STRATA_TEST_EXIT", None)
        self.executable("strata", '''#!/usr/bin/env python3
import json, os, sys
with open(os.environ['STRATA_TEST_LOG'], 'a') as f:
    f.write(json.dumps({'args': sys.argv[1:], 'control': os.getenv('STRATA_CONTROL_INSTALL')}) + '\\n')
if '--output' in sys.argv:
    print(os.getenv('STRATA_TEST_RESULT', '{"ok": true, "urls": {"api": "http://127.0.0.1:8080/v1"}}'))
    sys.exit(int(os.getenv('STRATA_TEST_EXIT', '0')))
''')
        self.executable("nvidia-smi", "#!/bin/sh\nprintf 'RTX 5090, 32768, 30000, 580.1\\n'\n")
        self.executable("curl", '''#!/usr/bin/env python3
import json, os, sys
with open(os.environ['STRATA_TEST_LOG'], 'a') as f:
    f.write(json.dumps({'curl': sys.argv[1:]}) + '\\n')
print('{"status":"ok"}')
''')

    def executable(self, name, contents):
        path = self.work / name
        path.write_text(contents)
        path.chmod(0o755)

    def run_helper(self, *args, success=True):
        result = subprocess.run(["bash", str(HELPER), *args], env=self.env,
                                text=True, capture_output=True)
        if success:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout)
        return result

    def calls(self):
        return [json.loads(line) for line in self.log.read_text().splitlines()] if self.log.exists() else []

    def test_dry_run_is_inert_even_with_stop_in_either_order(self):
        for args in (("--dry-run",), ("--dry-run", "--stop"), ("--stop", "--dry-run")):
            with self.subTest(args=args):
                self.run_helper(*args)
                self.assertEqual(self.calls(), [])

    def test_defaults_and_alternative_models(self):
        plan = self.run_helper("--dry-run").stdout
        for value in ("--family nvfp4", "--model NVFP4", "--context 64k",
                      "vram-reserve-mib=2560", "--parallel 1", "--access local"):
            self.assertIn(value, plan)
        for quant, family, model in (("q5", "unsloth", "UD-Q5_K_XL"),
                                     ("q4", "unsloth", "UD-Q4_K_XL"),
                                     ("iq3", "qwen", "IQ3_S")):
            plan = self.run_helper("--dry-run", "--quant", quant).stdout
            self.assertIn(f"--family {family} --model {model}", plan)

    def test_rejects_invalid_values_and_conflicting_modes_before_execution(self):
        for args in (("--context", "999999999k"), ("--context", "0"),
                     ("--port", "65536"), ("--port", "0"), ("--gpu", "-1"),
                     ("--vram-reserve-mib", "-1"), ("--quant", "bogus"),
                     ("--vision", "bogus"), ("--context",),
                     ("--setup-only", "--tune", "quick"),
                     ("--setup-only", "--stop"), ("--status", "--stop")):
            with self.subTest(args=args):
                self.run_helper(*args, success=False)
                self.assertEqual(self.calls(), [])

    @unittest.skipIf(os.geteuid() == 0, "helper intentionally refuses root")
    def test_setup_only_prepares_without_launching_and_preserves_path_arguments(self):
        data = str(self.work / "models with spaces")
        self.run_helper("--no-start", "--vision", "off", "--context", "128K",
                        "--data-dir", data, "--vram-reserve-mib", "4096")
        calls = self.calls()
        self.assertEqual(len(calls), 3)
        self.assertEqual(calls[1]["args"], ["update", "--backend", "cuda", "--no-control"])
        install = calls[2]
        self.assertEqual(install["control"], "1")
        self.assertEqual(install["args"][:2], ["install", "--"])
        self.assertIn("--no-start", install["args"])
        for option, value in (("--vision", "no"), ("--context", "131072"),
                              ("--data-dir", data), ("--vram-reserve-mib", "4096"),
                              ("--host", "127.0.0.1")):
            self.assertEqual(install["args"][install["args"].index(option) + 1], value)

    @unittest.skipIf(os.geteuid() == 0, "helper intentionally refuses root")
    def test_status_and_stop_do_not_prepare_or_download(self):
        for action in ("status", "stop"):
            self.run_helper(f"--{action}")
        self.assertEqual([call["args"] for call in self.calls()],
                         [["launch", "--status"], ["launch", "--stop"]])

    @unittest.skipIf(os.geteuid() == 0, "helper intentionally refuses root")
    def test_launch_checks_health_before_reporting_ready(self):
        result = self.run_helper("--port", "08081")
        calls = self.calls()
        self.assertIn("--plan", calls[1]["args"])
        self.assertEqual(calls[2]["args"][-2:], ["--output", "json"])
        self.assertEqual(calls[3]["curl"][-1], "http://127.0.0.1:8081/health")
        self.assertIn("Strata is ready", result.stdout)

    @unittest.skipIf(os.geteuid() == 0, "helper intentionally refuses root")
    def test_download_only_result_is_not_reported_as_serving(self):
        self.env["STRATA_TEST_RESULT"] = '{"ok": true, "serving": false, "engine_problem": "no engine"}'
        result = self.run_helper(success=False)
        self.assertIn("Strata is not serving", result.stderr)
        self.assertFalse(any("curl" in call for call in self.calls()))

    @unittest.skipIf(os.geteuid() == 0, "helper intentionally refuses root")
    def test_launch_failure_is_not_hidden_by_tee(self):
        self.env["STRATA_TEST_EXIT"] = "5"
        self.run_helper(success=False)
        self.assertFalse(any("curl" in call for call in self.calls()))


if __name__ == "__main__":
    unittest.main()
