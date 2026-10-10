"""Exercise optional PipeWire socket setup without modifying host services."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECIPE = ROOT / 'devario-core/pipewire'
BASH = shutil.which('bash')
SYSTEMCTL = shutil.which('systemctl')


class PipeWireScriptlets(unittest.TestCase):
    def run_action(self, package, action, root, prelude=''):
        env = dict(os.environ, PATH=str(root / 'bin'), TEST_ROOT=str(root))
        result = subprocess.run(
            [BASH, '-e', '-c', prelude + '\nsource "$1"; '
             'if declare -F "$2" >/dev/null; then "$2" 1:1.6.9-3 1:1.6.9-2; fi',
             'fixture', str(RECIPE / (package + '.install')), action],
            env=env, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def test_missing_systemctl_does_not_abort_install_or_removal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'bin').mkdir()
            for package in ('pipewire', 'pipewire-pulse'):
                for action in ('post_install', 'pre_remove'):
                    with self.subTest(package=package, action=action):
                        result = self.run_action(package, action, root)
                        self.assertIn('systemctl is unavailable', result.stderr)

    def test_systemctl_failure_is_reported_without_aborting(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'bin').mkdir()
            tool = root / 'bin/systemctl'
            tool.write_text('#!' + BASH + '\nprintf "fixture failure\\n" >&2\nexit 1\n')
            tool.chmod(0o755)
            for package in ('pipewire', 'pipewire-pulse'):
                for action, operation in (('post_install', 'enable'), ('pre_remove', 'disable')):
                    with self.subTest(package=package, action=action):
                        result = self.run_action(package, action, root)
                        self.assertIn('fixture failure', result.stderr)
                        self.assertIn(f'systemctl --global {operation} {package}.socket', result.stderr)

    def test_upgrade_preserves_existing_socket_state_without_vercmp(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'bin').mkdir()
            for package in ('pipewire', 'pipewire-pulse'):
                result = self.run_action(package, 'post_upgrade', root,
                                         'systemctl() { echo unexpected-systemctl >&2; return 1; }')
                self.assertEqual(result.stderr, '')

    @unittest.skipUnless(SYSTEMCTL, 'systemctl is needed for offline integration checks')
    def test_real_systemctl_enables_and_removes_sockets_offline(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            units = root / 'usr/lib/systemd/user'
            units.mkdir(parents=True)
            (root / 'bin').mkdir()
            prelude = 'systemctl() { "' + SYSTEMCTL + '" --root="$TEST_ROOT" "$@"; }'
            for package in ('pipewire', 'pipewire-pulse'):
                (units / (package + '.socket')).write_text(
                    '[Socket]\nListenStream=%t/' + package + '\n'
                    '[Install]\nWantedBy=sockets.target\n')
                (units / (package + '.service')).write_text(
                    '[Service]\nExecStart=/usr/bin/true\n')
                link = root / 'etc/systemd/user/sockets.target.wants' / (package + '.socket')
                self.run_action(package, 'post_install', root, prelude)
                self.assertTrue(link.is_symlink())
                self.assertEqual(link.readlink(), Path('/usr/lib/systemd/user') / (package + '.socket'))
                self.run_action(package, 'pre_remove', root, prelude)
                self.assertFalse(link.is_symlink())

    @unittest.skipUnless(SYSTEMCTL, 'systemctl is needed for offline integration checks')
    def test_real_systemctl_preserves_administrator_masks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = root / 'etc/systemd/user'
            config.mkdir(parents=True)
            (root / 'bin').mkdir()
            prelude = 'systemctl() { "' + SYSTEMCTL + '" --root="$TEST_ROOT" "$@"; }'
            for package in ('pipewire', 'pipewire-pulse'):
                mask = config / (package + '.socket')
                mask.symlink_to('/dev/null')
                result = self.run_action(package, 'post_install', root, prelude)
                self.assertEqual(mask.readlink(), Path('/dev/null'))
                self.assertIn('could not enable', result.stderr)
                self.assertFalse((config / 'sockets.target.wants' / mask.name).is_symlink())


if __name__ == '__main__':
    unittest.main()
