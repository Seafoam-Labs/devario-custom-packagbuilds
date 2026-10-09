"""Verify native hook paths and stage hook packaging without compiling applications."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def run_recipe(recipe, source, package, function='package', prelude=''):
    result = subprocess.run(
        ['bash', '-e', '-c',
         'source "$1"; srcdir="$2"; pkgdir="$3"; cd "$srcdir"; ' + prelude + '; ' + function,
         'fixture', str(recipe / 'PKGBUILD'), str(source), str(package)],
        capture_output=True, text=True)
    if result.returncode:
        raise AssertionError(result.stdout + result.stderr)


class HookLayout(unittest.TestCase):
    def test_all_recipe_destinations_are_native(self):
        paths = sorted(ROOT.glob('devario-*/*/PKGBUILD')) + sorted(ROOT.glob('isolation-builder/*/PKGBUILD'))
        self.assertTrue(paths)
        for path in paths:
            for number, line in enumerate(path.read_text().splitlines(), 1):
                if line.lstrip().startswith('#'):
                    continue
                # This substitution removes the upstream Makefile's default.
                if "sed -i 's|/libalpm/hooks|/rlpm/hooks|g' Makefile" in line:
                    continue
                self.assertNotRegex(line, r'(?:libalpm/(?:hooks|scripts)|pacman\.d/hooks)', f'{path}:{number}')

    def test_bundled_hooks_use_native_commands_and_targets(self):
        count = 0
        paths = list(ROOT.glob('devario-*/*/*')) + list(ROOT.glob('isolation-builder/*/*'))
        for path in paths:
            if not path.is_file() or not (path.suffix == '.hook' or path.name in ('hook.install', 'hook.remove', 'hook.upgrade')):
                continue
            text = path.read_text()
            count += 1
            self.assertIn('[Trigger]', text, str(path))
            self.assertIn('[Action]', text, str(path))
            self.assertRegex(text, r'(?m)^When\s*=\s*(PreTransaction|PostTransaction)\s*$', str(path))
            self.assertRegex(text, r'(?m)^Exec\s*=\s*/', str(path))
            self.assertNotRegex(text, r'libalpm/|pacman\.d/|var/lib/texmf/arch/', str(path))
            self.assertNotRegex(text, r'(?m)^Exec\s*=.*\b(?:pacman|pactree|pacconf|expac)\b', str(path))
        self.assertGreater(count, 50)

    def test_native_configuration_preserves_override_order(self):
        text = (ROOT / 'devario-installer/devario-base/shelly.conf').read_text()
        lines = [line.strip() for line in text.splitlines() if not line.lstrip().startswith('#')]
        self.assertIn('HookDirMode = Replace', lines)
        hooks = [line.split('=', 1)[1].strip().rstrip('/') for line in lines if re.match(r'HookDir\s*=', line)]
        self.assertEqual(hooks, ['/usr/share/rlpm/hooks', '/etc/shelly.d/hooks'])

    def test_neovim_hook_and_helper_install_together(self):
        recipe = ROOT / 'devario-development/neovim'
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'src'; package = Path(tmp) / 'pkg'; source.mkdir()
            for name in ('nvimdoc', 'nvimdoc.hook'):
                shutil.copy2(recipe / name, source / name)
            for name in ('LICENSE.txt', 'runtime/nvim.desktop', 'runtime/nvim.appdata.xml', 'runtime/nvim.png'):
                path = source / 'neovim' / name; path.parent.mkdir(parents=True, exist_ok=True); path.touch()
            run_recipe(recipe, source, package,
                       prelude='cmake() { mkdir -p "$pkgdir/usr/share/nvim/runtime"; }')
            hook = package / 'usr/share/rlpm/hooks/nvimdoc.hook'
            command = re.search(r'(?m)^Exec = (.+)$', hook.read_text()).group(1)
            self.assertTrue(os.access(package / command.lstrip('/'), os.X_OK))
            self.assertFalse((package / 'usr/share/libalpm').exists())

    def test_texinfo_hook_installation(self):
        recipe = ROOT / 'isolation-builder/texinfo'
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'src'; package = Path(tmp) / 'pkg'; source.mkdir()
            for name in ('texinfo-install.hook', 'texinfo-remove.hook'):
                shutil.copy2(recipe / name, source / name)
            run_recipe(recipe, source, package, prelude='make() { :; }')
            self.assertEqual(len(list((package / 'usr/share/rlpm/hooks').glob('*.hook'))), 2)
            self.assertFalse((package / 'usr/share/libalpm').exists())

    def test_texlive_metadata_hooks_and_helpers_agree(self):
        recipe = ROOT / 'devario-utilities/texlive-texmf'
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'src'; package = Path(tmp) / 'pkg'; source.mkdir()
            for path in recipe.iterdir():
                if path.is_file(): shutil.copy2(path, source / path.name)
            for name in ('pkgdesc-basic', 'depends-basic', 'packages-basic'):
                (source / name).write_text('')
            for suffix in ('fmts', 'maps', 'dat', 'dat.lua', 'def'):
                (source / ('basic.' + suffix)).write_text('fixture-marker\n')
            files = ('web2c/updmap.cfg', 'web2c/fmtutil.cnf', 'web2c/fmtutil-hdr.cnf',
                     'web2c/mktex.cnf', 'web2c/texmf.cnf', 'web2c/updmap-hdr.cfg',
                     'dvipdfmx/dvipdfmx.cfg', 'dvips/config/config.ps', 'xdvi/XDvi',
                     'tex/generic/tex-ini-files/pdftexconfig.tex',
                     'tex/generic/config/language.dat', 'tex/generic/config/language.dat.lua',
                     'tex/generic/config/language.def', 'tex/generic/config/language.us',
                     'tex/generic/config/language.us.lua', 'tex/generic/config/language.us.def')
            for name in files:
                path = source / 'texlive-basic/texmf-dist' / name
                path.parent.mkdir(parents=True, exist_ok=True); path.write_text('header\n')
            for name in ('TeXLive/test.pm', 'texlive.tlpdb', 'installer/config.guess'):
                path = source / 'tlpkg' / name; path.parent.mkdir(parents=True, exist_ok=True); path.touch()
            run_recipe(recipe, source, package, function='package_texlive-basic', prelude=':')
            metadata = package / 'var/lib/texmf/devario/installedpkgs'
            self.assertEqual(len(list(metadata.iterdir())), 5)
            self.assertFalse((package / 'var/lib/texmf/arch').exists())
            for path in (package / 'usr/share/rlpm/hooks').glob('*.hook'):
                command = re.search(r'(?m)^Exec = (\S+)', path.read_text()).group(1)
                if command.startswith('/usr/share/rlpm/scripts/'):
                    self.assertTrue(os.access(package / command.lstrip('/'), os.X_OK))
            # This helper uses only relative fixture files, so execute it directly.
            subprocess.run(['bash', str(package / 'usr/share/rlpm/scripts/texlive-language')], cwd=package, check=True)
            for suffix in ('dat', 'dat.lua', 'def'):
                output = package / ('etc/texmf/tex/generic/config/language.' + suffix)
                self.assertIn('fixture-marker', output.read_text())


if __name__ == '__main__':
    unittest.main()
