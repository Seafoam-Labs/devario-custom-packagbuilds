#!/usr/bin/env python3
"""Exercise PAM's packaged lockout default without changing host authentication."""
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECIPE = ROOT / 'devario-core/pam'


class FaillockPackageTests(unittest.TestCase):
    def stage(self, configuration):
        temporary = tempfile.TemporaryDirectory(prefix='devario-pam-test-')
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / 'faillock.conf').write_text(configuration)
        # A real ELF fixture exercises the existing ABI check. Only Meson's
        # upstream installation is mocked; the package() function runs as shipped.
        subprocess.run(['cc', '-shared', '-fPIC', '-x', 'c', '-',
                        '-Wl,-soname,libpam.so.0', '-o', str(root / 'libpam.so')],
                       input='int fixture(void) { return 0; }\n', text=True, check=True)
        result = subprocess.run(['bash', '-euc', '''
source "$1/PKGBUILD"
srcdir=$1
pkgdir=$2/package
fixtures=$2
cd "$srcdir"
meson() {
  install -Dm644 "$fixtures/faillock.conf" "$pkgdir/etc/security/faillock.conf"
  install -Dm755 "$fixtures/libpam.so" "$pkgdir/usr/lib/libpam.so"
  install -Dm755 /dev/null "$pkgdir/usr/bin/unix_chkpwd"
}
package
printf '%s\n' "${backup[@]}"
''', 'stage-pam', str(RECIPE), str(root)], capture_output=True, text=True)
        return result, root / 'package'

    def test_packaged_default_disables_lockout_and_preserves_other_settings(self):
        configuration = '# deny = 3\n# unlock_time = 600\naudit\n'
        result, payload = self.stage(configuration)
        self.assertEqual(result.returncode, 0, result.stderr)
        config = payload / 'etc/security/faillock.conf'
        active = [line.strip() for line in config.read_text().splitlines()
                  if line.strip() and not line.lstrip().startswith('#')]
        self.assertEqual(active, ['deny = 0', 'audit'])
        self.assertIn('# unlock_time = 600', config.read_text())
        self.assertEqual(config.stat().st_mode & 0o777, 0o644)
        self.assertIn('etc/security/faillock.conf', result.stdout.splitlines())
        self.assertFalse((payload / 'etc/pam.d').exists())

    def test_changed_upstream_template_cannot_silently_restore_lockout(self):
        result, _ = self.stage('# different upstream format\n# deny=3\n')
        self.assertNotEqual(result.returncode, 0)

    def test_metadata_keeps_backup_policy_and_base_requires_updated_pam(self):
        metadata = (RECIPE / '.SRCINFO').read_text()
        self.assertIn('\tpkgrel = 4\n', metadata)
        self.assertIn('\tbackup = etc/security/faillock.conf\n', metadata)
        for directory in ('devario-core', 'devario-installer'):
            with self.subTest(directory=directory):
                base = ROOT / directory / 'devario-base'
                metadata = (base / '.SRCINFO').read_text()
                self.assertIn('\tdepends = pam>=1.7.3-3\n', metadata)
                result = subprocess.check_output(['bash', '-euc',
                    'source "$1"; printf "%s\\n" "${depends[@]}"',
                    'base-dependencies', str(base / 'PKGBUILD')], text=True)
                self.assertIn('pam>=1.7.3-3', result.splitlines())


if __name__ == '__main__':
    unittest.main()
