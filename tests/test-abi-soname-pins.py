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
    # Compiler support, numeric libraries, and language runtimes. Every value here
    # is the SONAME the published archive carries, read with `readelf -d`.
    'duktape': {'libduktape.so': 'libduktape.so=207-64',
                'libduktaped.so': 'libduktaped.so=207-64'},
    'fftw': {'libfftw3.so': 'libfftw3.so=3-64',
             'libfftw3_omp.so': 'libfftw3_omp.so=3-64',
             'libfftw3_threads.so': 'libfftw3_threads.so=3-64',
             'libfftw3f.so': 'libfftw3f.so=3-64',
             'libfftw3f_omp.so': 'libfftw3f_omp.so=3-64',
             'libfftw3f_threads.so': 'libfftw3f_threads.so=3-64',
             'libfftw3l.so': 'libfftw3l.so=3-64',
             'libfftw3l_omp.so': 'libfftw3l_omp.so=3-64',
             'libfftw3l_threads.so': 'libfftw3l_threads.so=3-64',
             'libfftw3q.so': 'libfftw3q.so=3-64',
             'libfftw3q_omp.so': 'libfftw3q_omp.so=3-64',
             'libfftw3q_threads.so': 'libfftw3q_threads.so=3-64',
             'libfftw3_mpi.so': 'libfftw3_mpi.so=3-64',
             'libfftw3f_mpi.so': 'libfftw3f_mpi.so=3-64',
             'libfftw3l_mpi.so': 'libfftw3l_mpi.so=3-64'},
    'gtest': {'libgmock.so': 'libgmock.so=1.18.0-64',
              'libgmock_main.so': 'libgmock_main.so=1.18.0-64',
              'libgtest.so': 'libgtest.so=1.18.0-64',
              'libgtest_main.so': 'libgtest_main.so=1.18.0-64'},
    'jemalloc': {'libjemalloc.so': 'libjemalloc.so=2-64'},
    'libedit': {'libedit.so': 'libedit.so=0-64'},
    'libisl': {'libisl.so': 'libisl.so=23-64'},
    'pahole': {'libdwarves.so': 'libdwarves.so=1-64',
               'libdwarves_emit.so': 'libdwarves_emit.so=1-64',
               'libdwarves_reorganize.so': 'libdwarves_reorganize.so=1-64'},
    'pcre': {'libpcre.so': 'libpcre.so=1-64',
             'libpcre16.so': 'libpcre16.so=0-64',
             'libpcre32.so': 'libpcre32.so=0-64',
             'libpcreposix.so': 'libpcreposix.so=0-64',
             'libpcrecpp.so': 'libpcrecpp.so=0-64'},
    'shaderc': {'libshaderc_shared.so': 'libshaderc_shared.so=1-64'},
    'tomlplusplus': {'libtomlplusplus.so': 'libtomlplusplus.so=3-64'},
    'yaml-cpp': {'libyaml-cpp.so': 'libyaml-cpp.so=0.9-64'},
    'yyjson': {'libyyjson.so': 'libyyjson.so=0-64'},
    'zeromq': {'libzmq.so': 'libzmq.so=5-64'},
    # Storage, boot, and installer path. libdevmapper is published under lvm2's
    # device-mapper output, libbd_* under the matching libblockdev output.
    'cryptsetup': {'libcryptsetup.so': 'libcryptsetup.so=12-64'},
    'e2fsprogs': {'libcom_err.so': 'libcom_err.so=2-64',
                  'libe2p.so': 'libe2p.so=2-64',
                  'libext2fs.so': 'libext2fs.so=2-64',
                  'libss.so': 'libss.so=2-64'},
    'efivar': {'libefiboot.so': 'libefiboot.so=1-64',
               'libefisec.so': 'libefisec.so=1-64',
               'libefivar.so': 'libefivar.so=1-64'},
    'f2fs-tools': {'libf2fs.so': 'libf2fs.so=11-64',
                   'libf2fs_format.so': 'libf2fs_format.so=10-64'},
    'libblockdev': {'libbd_utils.so': 'libbd_utils.so=3-64',
                    'libblockdev.so': 'libblockdev.so=3-64',
                    'libbd_btrfs.so': 'libbd_btrfs.so=3-64',
                    'libbd_crypto.so': 'libbd_crypto.so=3-64',
                    'libbd_dm.so': 'libbd_dm.so=3-64',
                    'libbd_fs.so': 'libbd_fs.so=3-64',
                    'libbd_loop.so': 'libbd_loop.so=3-64',
                    'libbd_lvm.so': 'libbd_lvm.so=3-64',
                    'libbd_lvm-dbus.so': 'libbd_lvm-dbus.so=3-64',
                    'libbd_mdraid.so': 'libbd_mdraid.so=3-64',
                    'libbd_mpath.so': 'libbd_mpath.so=3-64',
                    'libbd_nvdimm.so': 'libbd_nvdimm.so=3-64',
                    'libbd_nvme.so': 'libbd_nvme.so=3-64',
                    'libbd_part.so': 'libbd_part.so=3-64',
                    'libbd_smart.so': 'libbd_smart.so=3-64',
                    'libbd_smartmontools.so': 'libbd_smartmontools.so=3-64',
                    'libbd_swap.so': 'libbd_swap.so=3-64'},
    'lvm2': {'libdevmapper.so': 'libdevmapper.so=1.02-64',
             'libdevmapper-event.so': 'libdevmapper-event.so=1.02-64'},
    'udisks2': {'libudisks2.so': 'libudisks2.so=0-64'},
    # No provision of their own, but every .so they depend on is pinned above or
    # by a published provider, so their depends belong in this guard too.
    'efibootmgr': {},
    'parted': {},
    'squashfs-tools': {},
    'thin-provisioning-tools': {},
}

# Providers outside these recipes that publish only an unpinned provision, so a consumer here
# cannot name a versioned form of them without making itself uninstallable. util-linux-libs
# (libblkid, libmount, libfdisk), kmod (libkmod) and polkit (libpolkit-*) own recipe folders
# but no versioned provision, so their pins are a separate change with their own pkgrel bump.
UNPINNED_PROVIDERS = {'libkrb5.so', 'libblkid.so', 'libmount.so', 'libfdisk.so', 'libkmod.so',
                      'libpolkit-agent-1.so', 'libpolkit-gobject-1.so'}

ARRAY = re.compile(r'^(\s*)(\w+)(\+?)=\((.*?)\)', re.M | re.S)
ELEMENT = re.compile(r"'[^']*'|\"[^\"]*\"|[^\s'\"#]+")


def strip_comments(text):
    """Drop what bash would read as a comment, so an array's annotations are not elements."""
    cleaned = []
    for line in text.splitlines():
        kept, quote = [], None
        for ch in line:
            if quote:
                if ch == quote:
                    quote = None
            elif ch in '\'"':
                quote = ch
            elif ch == '#' and (not kept or kept[-1].isspace()):
                break
            kept.append(ch)
        cleaned.append(''.join(kept))
    return '\n'.join(cleaned)


def braces(word):
    """Expand the bash brace form a PKGBUILD array may hold, as bash would."""
    parts = []
    i = 0
    while i < len(word):
        if word[i] == '{' and '}' in word[i:]:
            end = word.index('}', i)
            parts.append(word[i + 1:end].split(','))
            i = end + 1
        else:
            parts.append(word[i])
            i += 1
    out = ['']
    for part in parts:
        choices = part if isinstance(part, list) else (part,)
        out = [head + choice for head in out for choice in choices]
    return out


def arrays(recipe, key):
    """Every assignment to `key` in the recipe, top level or inside a package_* function."""
    text = strip_comments((recipe / 'PKGBUILD').read_text())
    found = []
    for match in ARRAY.finditer(text):
        if match.group(2) != key:
            continue
        for element in ELEMENT.findall(match.group(4)):
            element = element.strip('\'"')
            if element:
                found.extend(braces(element))
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
