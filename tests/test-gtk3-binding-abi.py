#!/usr/bin/env python3
"""Exercise both binding generations' package ABI guards with real ELF fixtures."""
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CASES = (
    ("atkmm", (("libatkmm-1.6.so", 1),), "2.36.4-1"),
    ("cairomm", (("libcairomm-1.0.so", 1),), "1.19.1-1"),
    ("atkmm-2.36", (("libatkmm-2.36.so", 1),), None),
    ("cairomm-1.16", (("libcairomm-1.16.so", 1),), None),
    ("glibmm-2.68", (("libglibmm-2.68.so", 1), ("libgiomm-2.68.so", 1)), None),
    ("libsigc++-3.0", (("libsigc-3.0.so", 0),), None),
)


class Gtk3AbiTests(unittest.TestCase):
    def test_packages_accept_required_abi_and_reject_wrong_or_missing_library(self):
        for name, libraries, _ in CASES:
            variants = [("correct", None)] + [
                (variant, library) for library, _ in libraries for variant in ("wrong", "missing")
            ]
            for variant, faulty_library in variants:
                with self.subTest(package=name, variant=variant, library=faulty_library), tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    fixtures = root / "fixtures"
                    fixtures.mkdir()
                    for library, major in libraries:
                        if variant == "missing" and library == faulty_library:
                            continue
                        soname = library + (".999" if library == faulty_library else f".{major}")
                        subprocess.run(
                            ["cc", "-shared", "-fPIC", "-x", "c", "-", "-o", str(fixtures / library),
                             "-Wl,-soname," + soname],
                            input="int fixture(void) { return 0; }\n", text=True, check=True,
                        )
                    # Mock only Meson's installation. Run the real package function,
                    # including readelf verification and documentation splitting.
                    result = subprocess.run(
                        ["bash", "-c", '''
set -e
source "$1"
pkgdir="$PWD/pkg"
fixtures="$2"
meson() {
  mkdir -p "$pkgdir/usr/lib" "$pkgdir/usr/share/doc" "$pkgdir/usr/share/devhelp"
  cp -a "$fixtures/." "$pkgdir/usr/lib/"
}
"package_$3"
''', "test", str(ROOT / "devario-core" / name / "PKGBUILD"),
                         str(fixtures), name],
                        cwd=root, capture_output=True, text=True,
                    )
                    if variant == "correct":
                        self.assertEqual(result.returncode, 0, result.stderr)
                    else:
                        self.assertNotEqual(result.returncode, 0)

    def test_corrected_packages_upgrade_published_incompatible_versions(self):
        for name, _, old_version in CASES:
            if old_version is None:
                continue
            with self.subTest(package=name):
                version = subprocess.check_output(
                    ["bash", "-c", 'source "$1"; printf "%s:%s-%s" "$epoch" "$pkgver" "$pkgrel"',
                     "test", str(ROOT / "devario-core" / name / "PKGBUILD")], text=True,
                )
                comparison = subprocess.check_output(["vercmp", version, old_version], text=True)
                self.assertGreater(int(comparison), 0)

    def test_new_generations_have_distinct_package_names_and_abi_provisions(self):
        legacy = {"atkmm", "cairomm", "glibmm", "libsigc++"}
        all_names = set()
        all_libraries = set()
        for name, libraries, _ in CASES:
            with self.subTest(package=name):
                metadata = (ROOT / "devario-core" / name / ".SRCINFO").read_text()
                fields = {}
                for line in metadata.splitlines():
                    if " = " in line:
                        key, value = line.strip().split(" = ", 1)
                        fields.setdefault(key, []).append(value)
                names = set(fields["pkgname"])
                self.assertEqual(names, {name, name + "-docs"})
                self.assertFalse(names & all_names)
                all_names.update(names)
                provides = set(fields["provides"])
                expected = {item for library, major in libraries
                            for item in (library, f"{library}={major}-64")}
                self.assertEqual(provides, expected)
                self.assertFalse(provides & all_libraries)
                all_libraries.update(provides)
                for key in ("provides", "conflicts", "replaces"):
                    self.assertFalse({value.split("=")[0] for value in fields.get(key, [])} & legacy)


if __name__ == "__main__":
    unittest.main()
