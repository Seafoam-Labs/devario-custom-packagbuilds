#!/usr/bin/env python3
"""Exercise the patched binary with an isolated Shelly command and no Pacman."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

BINARY = Path(sys.argv.pop(1)).resolve()
OPTIONS = Path(sys.argv.pop(1))
MANAGERS = [name.lower() for name in re.findall(r"FF_PACKAGES_FLAG_(\w+)_BIT =", OPTIONS.read_text())]


class ShellyPackages(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.marker = self.root / "called"
        self.stub = self.root / "shelly"
        self.stub.write_text(f"#!{sys.executable}\n" + '''import os, sys
from pathlib import Path
assert sys.argv[1:] == ['list', 'standard', '--show-hidden', '--json']
Path(os.environ['SHELLY_TEST_MARKER']).write_text('called')
sys.stdout.write(os.environ['SHELLY_TEST_JSON'])
sys.exit(int(os.environ.get('SHELLY_TEST_STATUS', '0')))
''')
        self.stub.chmod(0o755)
        self.env = dict(os.environ, PATH=str(self.root), SHELLY_TEST_MARKER=str(self.marker),
                        SHELLY_TEST_JSON='[{"Name":"fish"},{"Name":"fastfetch"}]')

    def run_fetch(self, module=None, as_json=True):
        module = {"type": "packages", "disabled": [m for m in MANAGERS if m != "shelly"], **(module or {})}
        config = {"logo": {"type": "none"}, "modules": [module]}
        args = [str(BINARY), "--config", "-", "--pipe", "true"]
        if as_json:
            args += ["--format", "json"]
        result = subprocess.run(args, input=json.dumps(config), env=self.env,
                                capture_output=True, text=True, timeout=10, check=True)
        return json.loads(result.stdout)[0] if as_json else result.stdout

    def test_native_count_and_total(self):
        result = self.run_fetch()["result"]
        self.assertEqual(result["shelly"], 2)
        self.assertEqual(result["all"], 2)
        self.assertNotIn("pacman", result)
        self.assertTrue(self.marker.exists())

    def test_native_format_and_default_label(self):
        self.assertIn("2 (Shelly)", self.run_fetch(as_json=False))
        self.assertIn("2 (Shelly)", self.run_fetch({"format": "{shelly} (Shelly)"}, as_json=False))

    def test_empty_inventory(self):
        self.env["SHELLY_TEST_JSON"] = '[]'
        self.assertEqual(self.run_fetch()["result"]["all"], 0)

    def test_failed_command_even_with_valid_json(self):
        self.env["SHELLY_TEST_STATUS"] = '1'
        self.assertIn("error", self.run_fetch())

    def test_malformed_data(self):
        for payload in ['not json', '{}', '[1]', '[{}]', '[{"Name":""}]', '[{"Name":42}]']:
            with self.subTest(payload=payload):
                self.env["SHELLY_TEST_JSON"] = payload
                self.assertIn("error", self.run_fetch())

    def test_missing_shelly(self):
        self.stub.unlink()
        self.assertIn("error", self.run_fetch())

    def test_disabled_skips_command(self):
        self.assertEqual(self.run_fetch({"disabled": MANAGERS})["result"]["all"], 0)
        self.assertFalse(self.marker.exists())

    def test_pacman_is_disabled_by_build_default(self):
        # JSON disabled lists replace the compiled defaults, so inspect the
        # default configuration directly for this separate build contract.
        config = {"logo": {"type": "none"}, "modules": ["packages"]}
        result = subprocess.run([str(BINARY), "--config", "-", "--format", "json"],
                                input=json.dumps(config), env=self.env, capture_output=True,
                                text=True, timeout=10, check=True)
        self.assertNotIn("pacman", json.loads(result.stdout)[0]["result"])

    def test_inventory_changes_are_not_cached(self):
        self.assertEqual(self.run_fetch()["result"]["shelly"], 2)
        self.env["SHELLY_TEST_JSON"] = '[{"Name":"fish"}]'
        self.assertEqual(self.run_fetch()["result"]["shelly"], 1)


if __name__ == "__main__":
    unittest.main()
