"""Exercise optional WirePlumber service setup without modifying host services."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTLET = ROOT / 'devario-core/wireplumber/wireplumber.install'
BASH = shutil.which('bash')
SYSTEMCTL = shutil.which('systemctl')
UNIT = 'wireplumber.service'


class WirePlumberScriptlets(unittest.TestCase):
    def run_action(self, action, root, prelude=''):
        env = dict(os.environ, PATH=str(root / 'bin'), TEST_ROOT=str(root))
        result = subprocess.run(
            [BASH, '-e', '-c', prelude + '\nsource "$1"; '
             'if declare -F "$2" >/dev/null; then "$2" 0.5.18-2 0.5.18-1; fi',
             'fixture', str(SCRIPTLET), action],
            env=env, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def make_root(self, tmp):
        root = Path(tmp)
        (root / 'bin').mkdir()
        units = root / 'usr/lib/systemd/user'
        units.mkdir(parents=True)
        (root / 'etc/systemd/user').mkdir(parents=True)
        (units / UNIT).write_text('[Service]\nType=simple\nExecStart=/usr/bin/true\n'
                                  '[Install]\nWantedBy=pipewire.service\n'
                                  'Alias=pipewire-session-manager.service\n')
        return root

    def test_missing_systemctl_does_not_abort_install_or_removal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp)
            for action in ('post_install', 'pre_remove'):
                with self.subTest(action=action):
                    result = self.run_action(action, root)
                    self.assertIn('systemctl is unavailable', result.stderr)

    def test_systemctl_failure_is_reported_without_aborting(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp)
            tool = root / 'bin/systemctl'
            tool.write_text('#!' + BASH + '\nprintf "fixture failure\\n" >&2\nexit 1\n')
            tool.chmod(0o755)
            for action, operation in (('post_install', 'enable'), ('pre_remove', 'disable')):
                with self.subTest(action=action):
                    result = self.run_action(action, root)
                    self.assertIn('fixture failure', result.stderr)
                    self.assertIn(f'systemctl --global {operation} {UNIT}', result.stderr)

    def test_upgrade_defines_no_action_so_service_state_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp)
            result = self.run_action('post_upgrade', root,
                                     'systemctl() { echo unexpected-systemctl >&2; return 1; }')
            self.assertEqual(result.stderr, '')
            defined = subprocess.run(
                [BASH, '-c', 'source "$1"; declare -F post_upgrade', 'fixture', str(SCRIPTLET)],
                capture_output=True, text=True,
            )
            self.assertEqual(defined.stdout.strip(), '')

    @unittest.skipUnless(SYSTEMCTL, 'systemctl is needed for offline integration checks')
    def test_real_systemctl_enables_and_removes_service_offline(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp)
            prelude = 'systemctl() { "' + SYSTEMCTL + '" --root="$TEST_ROOT" "$@"; }'
            wants = root / 'etc/systemd/user/pipewire.service.wants' / UNIT
            alias = root / 'etc/systemd/user/pipewire-session-manager.service'
            self.run_action('post_install', root, prelude)
            self.assertTrue(wants.is_symlink())
            self.assertEqual(alias.readlink(), Path('/usr/lib/systemd/user') / UNIT)
            self.run_action('pre_remove', root, prelude)
            self.assertFalse(wants.is_symlink())
            self.assertFalse(alias.is_symlink())

    @unittest.skipUnless(SYSTEMCTL, 'systemctl is needed for offline integration checks')
    def test_real_systemctl_preserves_administrator_mask(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp)
            prelude = 'systemctl() { "' + SYSTEMCTL + '" --root="$TEST_ROOT" "$@"; }'
            config = root / 'etc/systemd/user'
            mask = config / UNIT
            mask.symlink_to('/dev/null')
            result = self.run_action('post_install', root, prelude)
            self.assertEqual(mask.readlink(), Path('/dev/null'))
            self.assertIn('could not enable', result.stderr)
            self.assertFalse((config / 'pipewire.service.wants' / UNIT).is_symlink())


if __name__ == '__main__':
    unittest.main()
