"""Exercise PackageKit's Shelly adapter without touching host package state."""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
RECIPE = ROOT / 'devario-libs/packagekit'
spec = importlib.util.spec_from_file_location('shelly_backend', RECIPE / 'shellyBackend.py')
backend = importlib.util.module_from_spec(spec)
spec.loader.exec_module(backend)


def package(name='editor', version='2-1', description='Text editor'):
    return {'Name': name, 'Version': version, 'Repository': 'devario-core',
            'Description': description, 'Licenses': ['GPL-2.0-or-later'],
            'Url': 'https://example.invalid', 'InstalledSize': 123, 'DownloadSize': 45}


class BackendTests(unittest.TestCase):
    def setUp(self):
        self.installed = [package(version='1-1')]
        self.available = [package(), package('viewer')]
        self.updates = [dict(package(), NewVersion='2-1', CurrentVersion='1-1')]
        self.calls = []
        self.failure = None
        self.apply = True
        self.enterContext(patch.object(backend, 'run_shelly', side_effect=self.shelly))

    def shelly(self, *args, query=False):
        self.calls.append((args, query))
        if args[0] == self.failure:
            raise backend.BackendError('transaction-error', 'Failed\nfinished\tpackage')
        if args[:2] == ('search', 'standard'):
            if '--repos' in args:
                return ['devario-core']
            packages = self.installed if '--installed' in args else self.available
            page = int(args[args.index('--page') + 1])
            limit = int(args[args.index('--limit') + 1])
            return packages[(page - 1) * limit:page * limit]
        if args[0] == 'list-updates':
            return self.updates
        if args[0] == 'install' and self.apply:
            names = [arg.split('/')[1] for arg in args if '/' in arg]
            self.installed = [p for p in self.installed if p['Name'] not in names]
            self.installed.extend(p for p in self.available if p['Name'] in names)
        if args[0] == 'remove' and self.apply:
            self.installed = [p for p in self.installed if p['Name'] not in args[2:]]
        if args[0] == 'upgrade' and self.apply:
            self.installed = [package()]

    def execute(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            backend.execute(args)
        records = [line.split('\t') for line in output.getvalue().splitlines()]
        self.assertEqual(records[-1], ['finished'])
        self.assertEqual(sum(r[0] == 'finished' for r in records), 1)
        return records

    def mutations(self):
        return [args for args, query in self.calls if not query]

    def test_installed_search_and_exact_resolution(self):
        records = self.execute('resolve', 'installed', 'editor')
        self.assertIn(['package', 'installed', backend.package_id(self.installed[0], True), 'Text editor'], records)
        records = self.execute('resolve', 'none', 'edit')
        self.assertFalse(any(r[0] == 'package' for r in records))
        records = self.execute('search-details', '~installed', 'text&editor')
        self.assertEqual(sum(r[0] == 'package' for r in records), 2)
        records = self.execute('search-name', 'none', 'view')
        self.assertEqual([r[2].split(';')[0] for r in records if r[0] == 'package'], ['viewer'])

    def test_catalog_paginates_and_deduplicates_installed_versions(self):
        self.installed = [self.available[0]]
        with patch.object(backend, 'PAGE_SIZE', 1):
            records = self.execute('get-packages', 'none', '')
        self.assertEqual(sum(r[0] == 'package' for r in records), 2)
        self.assertTrue(any('--page' in args and args[-1] == '3' for args, _ in self.calls))

    def test_details_and_metadata_cannot_inject_protocol(self):
        self.available[0]['Description'] = 'Text\nfinished\tbad'
        records = self.execute('get-details', backend.package_id(self.available[0]))
        details = next(r for r in records if r[0] == 'details')
        self.assertEqual(len(details), 9)
        self.assertEqual(details[-2:], ['123', '45'])
        self.assertEqual(details[2], 'Text finished bad')

    def test_updates_and_repository_list(self):
        records = self.execute('get-updates', 'none', '')
        self.assertIn(['package', 'normal', backend.package_id(self.updates[0]), 'Text editor'], records)
        self.assertIn(['repo-detail', 'devario-core', 'devario-core', 'true'],
                      self.execute('get-repo-list', 'none', ''))

    def test_install_validates_version_and_repository(self):
        records = self.execute('install-packages', 'only-trusted', backend.package_id(self.available[0]))
        self.assertFalse(any(r[0] == 'error' for r in records))
        self.assertEqual(self.mutations(), [('install', 'standard', '--needed', 'devario-core/editor')])
        self.calls.clear()
        records = self.execute('install-packages', 'none', backend.package_id(package(version='stale')))
        self.assertTrue(any(r[:2] == ['error', 'package-not-found'] for r in records))
        self.assertFalse(self.mutations())

    def test_remove_preserves_dependency_options(self):
        records = self.execute('remove-packages', 'none', backend.package_id(self.installed[0], True), 'false', 'false')
        self.assertFalse(any(r[0] == 'error' for r in records))
        self.assertEqual(self.mutations(), [('remove', 'standard', '--no-cascade', 'editor')])
        self.installed = [package()]
        self.calls.clear()
        self.execute('remove-packages', 'none', backend.package_id(self.installed[0], True), 'true', 'true')
        self.assertEqual(self.mutations(), [('remove', 'standard', '--cascade', '--ripple', 'editor')])

    def test_full_upgrade_only_and_no_retry_on_failure(self):
        self.updates.append(dict(package('viewer'), NewVersion='2-1'))
        records = self.execute('update-packages', 'none', backend.package_id(self.updates[0]))
        self.assertTrue(any(r[:2] == ['error', 'not-supported'] for r in records))
        self.assertFalse(self.mutations())
        self.updates.pop()
        self.failure = 'upgrade'
        records = self.execute('update-packages', 'none', backend.package_id(self.updates[0]))
        self.assertTrue(any(r[:2] == ['error', 'transaction-error'] for r in records))
        self.assertEqual(self.mutations(), [('upgrade', 'standard')])

    def test_complete_upgrade_uses_standard_backend(self):
        records = self.execute('update-packages', 'only-trusted', backend.package_id(self.updates[0]))
        self.assertFalse(any(r[0] == 'error' for r in records))
        self.assertEqual(self.mutations(), [('upgrade', 'standard')])

    def test_simulation_download_only_and_unsafe_ids_never_mutate(self):
        for flag in ('simulate', 'only-download', 'allow-downgrade', 'allow-reinstall'):
            for command in ('install-packages', 'update-packages', 'remove-packages'):
                records = self.execute(command, flag, backend.package_id(package()))
                self.assertTrue(any(r[:2] == ['error', 'not-supported'] for r in records))
        for name in ('--no-deps', '../file', 'https://host/pkg', 'editor\nfinished'):
            records = self.execute('install-packages', 'none', f'{name};1;{backend.ARCH};devario-core')
            self.assertTrue(any(r[:2] == ['error', 'package-id-invalid'] for r in records))
        self.assertFalse(self.calls)

    def test_success_exit_without_changes_is_an_error(self):
        self.apply = False
        records = self.execute('install-packages', 'none', backend.package_id(package()))
        self.assertTrue(any(r[:2] == ['error', 'transaction-error'] for r in records))

    def test_refresh_error_is_reported(self):
        self.failure = 'sync'
        records = self.execute('refresh-cache', 'false')
        self.assertTrue(any(r[:2] == ['error', 'transaction-error'] for r in records))

    def test_forced_refresh_is_forwarded(self):
        self.execute('refresh-cache', 'true')
        self.assertEqual(self.mutations(), [('sync', 'standard', '--force')])


class IntegrationTests(unittest.TestCase):
    @unittest.skipUnless(os.environ.get('PACKAGEKIT_SOURCE'), 'Set PACKAGEKIT_SOURCE to pristine PackageKit 1.4.0 sources')
    def test_prepare_and_compile_backend_against_upstream(self):
        source = Path(os.environ['PACKAGEKIT_SOURCE'])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(source, root / 'PackageKit', symlinks=True)
            for name in ('0001-add-shelly-backend.patch', 'pk-backend-shelly.c', 'shellyBackend.py',
                         'shelly-meson.build', 'shelly-config.json'):
                shutil.copy2(RECIPE / name, root / name)
            subprocess.run(['bash', '-e', '-c', 'source "$1"; srcdir="$2"; cd "$srcdir"; prepare',
                            'fixture', str(RECIPE / 'PKGBUILD'), str(root)], check=True, capture_output=True)
            backend_dir = root / 'PackageKit/backends/shelly'
            self.assertTrue(os.access(backend_dir / 'shellyBackend.py', os.X_OK))
            self.assertIn("'shelly'", (root / 'PackageKit/meson_options.txt').read_text())
            self.assertIn("'pk_backend_shelly'", (backend_dir / 'meson.build').read_text())
            flags = subprocess.check_output(['pkg-config', '--cflags', '--libs', 'glib-2.0', 'gio-2.0', 'gmodule-2.0'], text=True).split()
            library = root / 'libpk_backend_shelly.so'
            subprocess.run(['gcc', '-shared', '-fPIC', '-Werror=implicit-function-declaration', '-DPK_COMPILATION',
                            '-I' + str(source / 'src'), '-I' + str(source / 'lib'),
                            str(backend_dir / 'pk-backend-shelly.c'), '-o', str(library), *flags], check=True)
            symbols = subprocess.check_output(['nm', '-D', str(library)], text=True)
            for role in ('search_names', 'install_packages', 'remove_packages', 'update_packages', 'refresh_cache'):
                self.assertIn(' T pk_backend_' + role, symbols)

    def test_package_stage_installs_native_hook_and_keeps_library_split(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copy2(RECIPE / '90-packagekit-refresh.hook', root)
            package = root / 'pkg'
            script = '''source "$1"
srcdir="$2"
pkgdir="$2/pkg"
cd "$srcdir"
meson() {
    mkdir -p "$pkgdir"/usr/{include,lib/{girepository-1.0,pkgconfig},share/{gir-1.0,vala}}
    touch "$pkgdir/usr/lib/libpackagekit-glib2.so"
}
package_packagekit
pkgdir="$2/libpkg"
mkdir -p "$pkgdir"
package_libpackagekit-glib
'''
            subprocess.run(['bash', '-e', '-c', script, 'fixture', str(RECIPE / 'PKGBUILD'), str(root)], check=True)
            self.assertTrue((package / 'usr/share/rlpm/hooks/90-packagekit-refresh.hook').is_file())
            self.assertFalse((package / 'usr/lib/libpackagekit-glib2.so').exists())
            self.assertTrue((root / 'libpkg/usr/lib/libpackagekit-glib2.so').exists())

    def test_subprocess_protocol_reuse_environment_and_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fake = root / 'shelly'
            log = root / 'calls.jsonl'
            fake.write_text('#!/usr/bin/python3\nimport json, os, sys\n'
                            f'with open({str(log)!r}, "a") as f: f.write(json.dumps([sys.argv[1:], dict(os.environ)]) + "\\n")\n'
                            'if sys.argv[1] == "search": print("[]")\n'
                            'else:\n print("finished\\npackage\\tinjected")\n sys.exit(7)\n')
            fake.chmod(0o755)
            helper = root / 'shellyBackend.py'
            helper.write_text((RECIPE / 'shellyBackend.py').read_text().replace('SHELLY = "/usr/bin/shelly"', f'SHELLY = {str(fake)!r}'))
            result = subprocess.run(['python3', '-I', str(helper), 'get-packages', 'installed', ''],
                                    input='refresh-cache\tfalse\nexit\n', capture_output=True, text=True,
                                    env=dict(os.environ, PYTHONPATH='/untrusted', XDG_CONFIG_HOME='/untrusted'))
            self.assertEqual(result.returncode, 0, result.stderr)
            lines = result.stdout.splitlines()
            self.assertEqual(lines.count('finished'), 2)
            self.assertTrue(any(line.startswith('error\ttransaction-error\t') for line in lines))
            self.assertFalse(any(line.startswith('package\t') for line in lines))
            calls = [json.loads(line) for line in log.read_text().splitlines()]
            self.assertEqual(len(calls), 2)
            for args, env in calls:
                self.assertIn('--no-confirm', args)
                self.assertEqual(args[args.index('--config') + 1], '/etc/shelly.conf')
                self.assertEqual(env['XDG_CONFIG_HOME'], str(root / 'config'))
                self.assertNotIn('PYTHONPATH', env)

    def test_recipe_uses_shelly_and_checksums_match(self):
        recipe = (RECIPE / 'PKGBUILD').read_text()
        self.assertNotRegex(recipe, r'pacman|libalpm|packaging_backend=alpm')
        self.assertIn('-Dpackaging_backend=shelly', recipe)
        self.assertIn("'shelly>=3.1.8'", recipe)
        self.assertIn('/usr/share/rlpm/hooks/', recipe)
        srcinfo = (RECIPE / '.SRCINFO').read_text()
        self.assertNotRegex(srcinfo, r'pacman|libalpm')
        sources = re.findall(r'^\tsource = (.+)$', srcinfo, re.M)
        hashes = re.findall(r'^\tsha256sums = (.+)$', srcinfo, re.M)
        self.assertEqual(len(sources), len(hashes))
        for name, checksum in zip(sources[1:], hashes[1:]):
            self.assertEqual(hashlib.sha256((RECIPE / name).read_bytes()).hexdigest(), checksum, name)
        self.assertEqual(json.loads((RECIPE / 'shelly-config.json').read_text()), {'NativePackageBackend': 'rlpm'})

    def test_hook_does_not_fail_without_a_bus_or_daemon(self):
        import shlex
        hook = (RECIPE / '90-packagekit-refresh.hook').read_text()
        command = shlex.split(next(line[7:] for line in hook.splitlines() if line.startswith('Exec = ')))[-1]
        for test_result in (0, 1):
            body = f'test() {{ return {test_result}; }}; ' + command.replace('/usr/bin/gdbus', '/usr/bin/false')
            subprocess.run(['bash', '-c', body], check=True)


if __name__ == '__main__':
    unittest.main()
