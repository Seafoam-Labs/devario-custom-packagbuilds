#!/usr/bin/env python3
"""Exercise the legacy hook without touching host kernels or package databases."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

PACKAGE = Path(__file__).resolve().parents[1] / 'devario-core/devario-dracut'


class DracutInstall(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.modules = self.root / 'modules'
        self.boot = self.root / 'boot'
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        config = self.root / 'automation.conf'
        config.write_text('NVIDIA_EARLY_KMS=false\nAMD_EARLY_KMS=false\nINTEL_EARLY_KMS=false\n')
        script = (PACKAGE / 'dracut-install').read_text()
        script = script.replace('/etc/devario-dracut.conf', str(config))
        script = script.replace('/usr/lib/modules', str(self.modules)).replace('/boot/', str(self.boot) + '/')
        self.helper = self.root / 'dracut-install'
        self.helper.write_text(script)
        for name, body in {
            'dracut': 'printf "initramfs for %s\\n" "${*: -1}" > "${@: -2:1}"',
            'pacman': 'echo unexpected > "$TEST_ROOT/pacman-called"; exit 1',
        }.items():
            path = self.bin / name
            path.write_text('#!/bin/bash\nset -eu\n' + body + '\n')
            path.chmod(0o755)
        self.env = dict(os.environ, PATH=str(self.bin) + ':' + os.environ['PATH'], TEST_ROOT=str(self.root))

    def kernel(self, version, identifier):
        tree = self.modules / version
        tree.mkdir(parents=True)
        (tree / 'pkgbase').write_text(identifier + '\n')
        (tree / 'vmlinuz').write_text(version)
        return tree

    def run_hook(self, targets):
        return subprocess.run(['bash', '-e', str(self.helper)], input=targets,
                              env=self.env, text=True, capture_output=True)

    def test_lts_target_builds_without_pacman_even_without_final_newline(self):
        tree = self.kernel('6.18-lts', 'linux-devario-lts')
        result = self.run_hook(str(tree / 'vmlinuz').lstrip('/'))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.root / 'pacman-called').exists())
        self.assertEqual((self.boot / 'vmlinuz-linux-devario-lts').read_text(), '6.18-lts')
        self.assertIn('6.18-lts', (self.boot / 'initramfs-linux-devario-lts.img').read_text())
        self.assertTrue((self.boot / 'initramfs-linux-devario-lts-fallback.img').exists())

    def test_rebuild_copies_both_kernels_and_reports_incomplete_trees(self):
        self.kernel('6.19-regular', 'linux-devario')
        self.kernel('6.18-lts', 'linux-devario-lts')
        stale = self.modules / 'stale'
        stale.mkdir()
        result = self.run_hook('usr/lib/firmware/updated-file\n')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('missing kernel pkgbase or vmlinuz', result.stderr)
        for identifier in ('linux-devario', 'linux-devario-lts'):
            self.assertTrue((self.boot / f'vmlinuz-{identifier}').is_file())
            self.assertTrue((self.boot / f'initramfs-{identifier}.img').is_file())
        self.assertFalse((self.root / 'pacman-called').exists())

    def test_invalid_metadata_cannot_be_used_as_an_output_path(self):
        tree = self.kernel('6.18-lts', '../../escape')
        result = self.run_hook(str(tree / 'vmlinuz').lstrip('/') + '\n')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Invalid kernel metadata', result.stderr)
        self.assertFalse(self.boot.exists())

    def test_rebuild_uses_native_boot_workflow_when_available(self):
        native = self.bin / 'boot-update'
        native.write_text('#!/bin/bash\necho native-workflow\n')
        native.chmod(0o755)
        script = (PACKAGE / 'dracut-rebuild').read_text()
        script = script.replace('$EUID', '0').replace('/usr/lib/devario/boot-update', str(native))
        helper = self.root / 'dracut-rebuild'
        helper.write_text(script)
        result = subprocess.run(['bash', str(helper)], env=self.env, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), 'native-workflow')


if __name__ == '__main__':
    unittest.main()
