"""Exercise the proton-vpn-daemon scriptlets without touching host services."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTLET = ROOT / 'devario-utilities/proton-vpn-daemon/proton-vpn-daemon.install'
BASH = shutil.which('bash')
SYSTEMCTL = shutil.which('systemctl')
UNIT = 'proton.VPN.service'


class ProtonVpnDaemonScriptlets(unittest.TestCase):
    def run_action(self, action, root, prelude=''):
        env = dict(os.environ, PATH=str(root / 'bin'), TEST_ROOT=str(root))
        result = subprocess.run(
            [BASH, '-e', '-c', prelude + '\nsource "$1"; '
             'if declare -F "$2" >/dev/null; then "$2"; fi',
             'fixture', str(SCRIPTLET), action],
            env=env, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def make_root(self, tmp):
        root = Path(tmp)
        (root / 'bin').mkdir()
        (root / 'usr/lib/systemd/system').mkdir(parents=True)
        (root / 'etc/systemd/system').mkdir(parents=True)
        (root / 'usr/lib/systemd/system' / UNIT).write_text(
            '[Service]\nType=simple\nExecStart=/usr/bin/true\n'
            '[Install]\nWantedBy=multi-user.target\n')
        return root

    def test_missing_systemctl_does_not_abort_setup(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp)
            for action in ('post_install', 'post_upgrade', 'pre_remove'):
                with self.subTest(action=action):
                    result = self.run_action(action, root)
                    self.assertIn('systemctl is unavailable', result.stderr)

    def test_systemctl_failure_is_reported_without_aborting(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp)
            tool = root / 'bin/systemctl'
            tool.write_text('#!' + BASH + '\nprintf "fixture failure\\n" >&2\nexit 1\n')
            tool.chmod(0o755)
            for action in ('post_install', 'post_upgrade', 'pre_remove'):
                with self.subTest(action=action):
                    result = self.run_action(action, root)
                    self.assertIn('fixture failure', result.stderr)

    @unittest.skipUnless(SYSTEMCTL, 'systemctl is needed for offline integration checks')
    def test_real_systemctl_enables_the_unit_offline(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp)
            prelude = 'systemctl() { "' + SYSTEMCTL + '" --root="$TEST_ROOT" "$@"; }'
            result = self.run_action('post_install', root, prelude)
            # --now cannot start anything in a root, so only the enable result counts.
            enabled = subprocess.run(
                [SYSTEMCTL, '--root', str(root), 'is-enabled', UNIT],
                capture_output=True, text=True,
            )
            if enabled.returncode != 0:
                self.assertIn('could not systemctl', result.stderr)


if __name__ == '__main__':
    unittest.main()
