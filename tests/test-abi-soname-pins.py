#!/usr/bin/env python3
"""Guard the versioned SONAME provisions of the fan-in ABI libraries in devario-core.

Each recipe here publishes a shared object, so every bare `libfoo.so` provision it declares
must be paired with the `libfoo.so=N-64` form Shelly carries into `.PKGINFO`, and each pinned
form must be checked by the recipe's own ELF64/SONAME probe. The bare-only state is what let
the tree-sitter 0.27 break load an incompatible library, and a consumer that pins a provision
nothing published declares makes every isolated build root unresolvable.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

# Provisions read off the published archives with `readelf -d`, not derived from recipe text.
PINNED = {
    'acl': {'libacl.so': 'libacl.so=1-64'},
    'attr': {'libattr.so': 'libattr.so=1-64'},
    'audit': {'libaudit.so': 'libaudit.so=1-64', 'libauparse.so': 'libauparse.so=0-64'},
    'gdbm': {'libgdbm.so': 'libgdbm.so=6-64', 'libgdbm_compat.so': 'libgdbm_compat.so=4-64'},
    'libbpf': {'libbpf.so': 'libbpf.so=1-64'},
    'libcap': {'libcap.so': 'libcap.so=2-64', 'libpsx.so': 'libpsx.so=2-64'},
    'libcap-ng': {'libcap-ng.so': 'libcap-ng.so=0-64', 'libdrop_ambient.so': 'libdrop_ambient.so=0-64'},
    'libdeflate': {'libdeflate.so': 'libdeflate.so=0-64'},
    'libnsl': {'libnsl.so': 'libnsl.so=3-64'},
    'libunistring': {'libunistring.so': 'libunistring.so=5-64'},
    'libverto': {'libverto.so': 'libverto.so=1-64', 'libverto-libevent.so': 'libverto-libevent.so=1-64'},
    'oniguruma': {'libonig.so': 'libonig.so=5-64'},
    'p11-kit': {'libp11-kit.so': 'libp11-kit.so=0-64'},
}

# Providers outside these recipes that publish only an unpinned provision, so a consumer here
# cannot name a versioned form of them without making itself uninstallable.
UNPINNED_PROVIDERS = {'libkrb5.so'}

ARRAY = re.compile(r'^(\s*)(\w+)(\+?)=\((.*?)\)', re.M | re.S)
ELEMENT = re.compile(r"'[^']*'|\"[^\"]*\"|[^\s'\"#]+")


def arrays(recipe, key):
    """Every assignment to `key` in the recipe, top level or inside a package_* function."""
    text = (recipe / 'PKGBUILD').read_text()
    found = []
    for match in ARRAY.finditer(text):
        if match.group(2) != key:
            continue
        for element in ELEMENT.findall(match.group(4)):
            element = element.strip('\'"')
            if element:
                found.append(element)
    return found


class AbiSonamePins(unittest.TestCase):
    def recipes(self):
        for pkgbase in sorted(PINNED):
            recipe = ROOT / 'devario-core' / pkgbase
            self.assertTrue((recipe / 'PKGBUILD').is_file(), f'devario-core/{pkgbase}/PKGBUILD is missing')
            self.assertTrue((recipe / '.SRCINFO').is_file(), f'devario-core/{pkgbase}/.SRCINFO is missing')
            yield pkgbase, recipe

    def test_every_bare_provision_is_paired_with_its_versioned_form(self):
        for pkgbase, recipe in self.recipes():
            declared = arrays(recipe, 'provides')
            for bare, pinned in PINNED[pkgbase].items():
                self.assertIn(bare, declared, f'devario-core/{pkgbase} dropped the bare {bare} provide')
                self.assertIn(pinned, declared, f'devario-core/{pkgbase} does not declare {pinned}')
            srcinfo = (recipe / '.SRCINFO').read_text()
            for pinned in PINNED[pkgbase].values():
                self.assertIn(f'provides = {pinned}', srcinfo,
                              f'devario-core/{pkgbase}/.SRCINFO is stale: no {pinned}')

    def test_every_pinned_provision_has_a_matching_probe(self):
        for pkgbase, recipe in self.recipes():
            text = (recipe / 'PKGBUILD').read_text()
            for bare, pinned in PINNED[pkgbase].items():
                soname = f'{bare}.{pinned.split("=")[1].split("-")[0]}'
                probe = re.search(r'_verify_soname\s+"?\$\{?pkgdir\}?[^"]*?/' + re.escape(bare)
                                  + r'"+\s+' + re.escape(soname) + r'\s*\|\|\s*return 1', text)
                self.assertIsNotNone(probe,
                                     f'devario-core/{pkgbase} declares {pinned} without probing {soname}')

    def test_no_recipe_here_depends_on_an_unpinned_provision_it_can_pin(self):
        provided = {bare: pinned for pins in PINNED.values() for bare, pinned in pins.items()}
        for pkgbase, recipe in self.recipes():
            for dep in arrays(recipe, 'depends'):
                base = re.split(r'[=<>]', dep)[0]
                if not base.endswith('.so'):
                    continue
                if base in provided:
                    self.assertEqual(dep, provided[base],
                                     f'devario-core/{pkgbase} depends on bare {base}, which is '
                                     f'published as {provided[base]} in this recipe set')
                    continue
                if '=' in dep:
                    continue  # pinned against a provider that already declares the versioned form
                self.assertIn(base, UNPINNED_PROVIDERS,
                              f'devario-core/{pkgbase} depends on bare {base} with no pinned provider '
                              'recorded for it')


if __name__ == '__main__':
    unittest.main(verbosity=2)
