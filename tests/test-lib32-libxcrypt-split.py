"""Verify the lib32-libxcrypt splits cannot both own a path."""
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECIPE = ROOT / 'devario-libs/lib32-libxcrypt'

# What each configure variant installs before the recipe prunes its split.
MAIN = ('libcrypt.la', 'libcrypt.so', 'libcrypt.so.2', 'libcrypt.so.2.0.0',
        'pkgconfig/libcrypt.pc', 'pkgconfig/libxcrypt.pc')
COMPAT = ('libcrypt.la', 'libcrypt.so', 'libcrypt.so.1', 'libcrypt.so.1.1.0')


class SplitOwnership(unittest.TestCase):
    def package(self, function, libraries):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        srcdir = Path(temp.name)
        build = srcdir / ('build-libxcrypt' if function.endswith('libxcrypt')
                          else 'build-libxcrypt-compat')
        (build / 'lib').mkdir(parents=True)
        pkgdir = srcdir / 'pkg'
        targets = [f'usr/lib32/{name}' for name in libraries]
        targets += ['usr/include/crypt.h', 'usr/share/man/man3/crypt.3',
                    'usr/lib32/pkgconfig/libcrypt.pc']
        (build / 'Makefile').write_text('install:\n' + ''.join(
            f'\tinstall -D -m 644 /dev/null "$(DESTDIR)/{target}"\n' for target in targets))
        result = subprocess.run(
            ['bash', '-e', '-c',
             'source "$1"; srcdir="$2"; pkgdir="$3"; cd "$srcdir"; ' + function,
             'fixture', str(RECIPE / 'PKGBUILD'), str(srcdir), str(pkgdir)],
            capture_output=True, text=True)
        if result.returncode:
            raise AssertionError(result.stdout + result.stderr)
        return {str(path.relative_to(pkgdir)) for path in pkgdir.rglob('*') if path.is_file()}

    def test_splits_share_no_path(self):
        main = self.package('package_lib32-libxcrypt', MAIN)
        compat = self.package('package_lib32-libxcrypt-compat', COMPAT)
        self.assertTrue(main and compat)
        self.assertEqual(main & compat, set())

    def test_only_the_main_split_ships_the_libtool_archive(self):
        main = self.package('package_lib32-libxcrypt', MAIN)
        compat = self.package('package_lib32-libxcrypt-compat', COMPAT)
        self.assertIn('usr/lib32/libcrypt.la', main)
        self.assertNotIn('usr/lib32/libcrypt.la', compat)
        self.assertEqual(compat, {'usr/lib32/libcrypt.so.1', 'usr/lib32/libcrypt.so.1.1.0'})


if __name__ == '__main__':
    unittest.main()
