#!/usr/bin/env python3
"""Prove the two Electron 44 providers publish the same tree.

`devario-libs/electron44` builds Electron from Chromium sources; `devario-libs/electron44-bin`
unpacks the dist.zip upstream ships. Application recipes reach the runtime through paths only —
`/usr/lib/electronNN/version`, `ELECTRON_OVERRIDE_DIST_PATH=/usr/lib/electronNN`,
`-c.electronDist=/usr/lib/electronNN`, `/usr/bin/electronNN`, and a setuid `chrome-sandbox` — so a
consumer flips `_electron` between the two providers only while both lay down the same files. This
unpacks one payload fixture through each recipe's packaging functions and diffs the results. No
Chromium build, download, or root is involved.
"""

from pathlib import Path
import filecmp
import hashlib
import os
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE_RECIPE = ROOT / "devario-libs/electron44/PKGBUILD"
BIN_RECIPE = ROOT / "devario-libs/electron44-bin/PKGBUILD"
BIN_SRCINFO = ROOT / "devario-libs/electron44-bin/.SRCINFO"
RUNTIME = "electron44"

# Payload members app recipes and Electron itself touch, plus extras that must survive the
# wholesale copy. The setuid bit is set by each recipe, not carried in the archive.
PAYLOAD = {
    "electron": "ELF\n",
    "version": "44.11.3\n",
    "chrome-sandbox": "sandbox\n",
    "chrome_crashpad_handler": "crashpad\n",
    "libffmpeg.so": "ffmpeg\n",
    "LICENSE": "MIT\n",
    "LICENSES.chromium.html": "BSD\n",
    "resources/default_app.asar": "asar\n",
    "locales/en-US.pak": "pak\n",
}
CHROMEDRIVER = {"chromedriver": "CD\n", "LICENSE": "CDLIC\n", "chromedriver.debug": "blob\n"}


def _archive(archive, files):
    with tempfile.TemporaryDirectory(prefix="devario-electron-fixture-") as staging:
        root = Path(staging)
        for name, body in files.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body)
            if name.rsplit("/", 1)[-1] in ("electron", "chrome-sandbox", "chromedriver",
                                           "chrome_crashpad_handler", "libffmpeg.so"):
                path.chmod(0o755)
        subprocess.run(["bsdtar", "-a", "-cf", str(archive), "-C", str(root), "."], check=True)


def _package(recipe, pkgname, srcdir, pkgdir, *functions):
    """Run recipe functions the way makepkg does: sourced, with pkgname and pkgdir set."""
    subprocess.run(
        [
            "bash",
            "-ec",
            'set -euo pipefail\nsource "$1"\ncd "$3"\nexport srcdir="$3" pkgdir="$4"\n'
            'pkgname="$2"\nfor fn in "${@:5}"; do "$fn"; done',
            "bash",
            str(recipe),
            pkgname,
            str(srcdir),
            str(pkgdir),
            *functions,
        ],
        check=True,
        capture_output=True,
        env={**os.environ, "CARCH": "x86_64"},
    )


def _tree(pkgdir, prefix):
    root = pkgdir / prefix
    entries = {}
    for path in sorted(root.rglob("*")):
        if path.is_dir():
            continue
        relative = path.relative_to(pkgdir).as_posix()
        if path.is_symlink():
            entries[relative] = ("link", os.readlink(path))
        else:
            mode = path.stat().st_mode & 0o7777
            entries[relative] = (oct(mode), hashlib.sha256(path.read_bytes()).hexdigest())
    return entries


def _without_licenses(paths):
    return {path: detail for path, detail in paths.items() if "licenses/" not in path}


class ElectronProviderLayout(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work = tempfile.TemporaryDirectory(prefix="devario-electron-")
        cls.srcdir = Path(cls.work.name) / "src"
        (cls.srcdir / "src/out/Release").mkdir(parents=True)
        _archive(cls.srcdir / "src/out/Release/dist.zip", PAYLOAD)
        # The icon lives in the Electron checkout the source recipe builds in $srcdir/src.
        (cls.srcdir / "src/electron/default_app").mkdir(parents=True)
        (cls.srcdir / "src/electron/default_app/icon.png").write_text("PNG\n")
        _archive(cls.srcdir / f"{RUNTIME}-44.11.3-x86_64.zip", PAYLOAD)
        _archive(cls.srcdir / f"{RUNTIME}-chromedriver-44.11.3-x86_64.zip", CHROMEDRIVER)
        shutil.copy2(BIN_RECIPE.parent / "electron-launcher.sh", cls.srcdir)
        # The source recipe rewrites @ELECTRON@ in its prepare(), which builds Chromium.
        launcher = (cls.srcdir / "electron-launcher.sh").read_text()
        (cls.srcdir / "electron-launcher.sh").write_text(
            launcher.replace("@ELECTRON@", RUNTIME)
        )

        cls.prebuilt = Path(cls.work.name) / "pkg-prebuilt"
        cls.prebuilt_driver = Path(cls.work.name) / "pkg-prebuilt-driver"
        cls.source = Path(cls.work.name) / "pkg-source"
        for directory in (cls.prebuilt, cls.prebuilt_driver, cls.source):
            directory.mkdir()
        _package(BIN_RECIPE, f"{RUNTIME}-bin", cls.srcdir, cls.prebuilt,
                 "prepare", f"package_{RUNTIME}-bin")
        _package(BIN_RECIPE, f"{RUNTIME}-bin-chromedriver", cls.srcdir, cls.prebuilt_driver,
                 f"package_{RUNTIME}-bin-chromedriver")
        _package(SOURCE_RECIPE, RUNTIME, cls.srcdir, cls.source, "package")

    @classmethod
    def tearDownClass(cls):
        cls.work.cleanup()

    def test_payload_tree_matches_the_source_recipe_byte_for_byte(self):
        prebuilt = _tree(self.prebuilt, f"usr/lib/{RUNTIME}")
        source = _tree(self.source, f"usr/lib/{RUNTIME}")
        self.assertTrue(prebuilt)
        self.assertEqual(prebuilt, source)

    def test_sandbox_helper_stays_setuid_in_both_providers(self):
        for pkgdir in (self.prebuilt, self.source):
            helper = pkgdir / f"usr/lib/{RUNTIME}/chrome-sandbox"
            self.assertTrue(helper.stat().st_mode & 0o4000, f"no setuid bit in {pkgdir.name}")

    def test_launcher_matches_the_source_recipe(self):
        prebuilt = self.prebuilt / f"usr/bin/{RUNTIME}"
        source = self.source / f"usr/bin/{RUNTIME}"
        self.assertEqual(prebuilt.read_bytes(), source.read_bytes())
        self.assertNotIn(b"@ELECTRON@", prebuilt.read_bytes())
        self.assertIn(f"name={RUNTIME}".encode(), prebuilt.read_bytes())
        self.assertIn(b"/usr/lib/${name}/electron", prebuilt.read_bytes())

    def test_license_entries_are_relative_links_into_the_payload(self):
        for pkgdir, package in ((self.prebuilt, f"{RUNTIME}-bin"), (self.source, RUNTIME)):
            licenses = pkgdir / "usr/share/licenses" / package
            names = sorted(p.name for p in licenses.iterdir())
            self.assertEqual(names, ["LICENSE", "LICENSES.chromium.html"])
            for name in names:
                link = licenses / name
                self.assertTrue(link.is_symlink(), f"{link} is not a symlink")
                self.assertTrue((link.parent / os.readlink(link)).is_file())

    def test_icon_is_the_only_file_the_prebuilt_provider_omits(self):
        prebuilt = set(_without_licenses(_tree(self.prebuilt, "usr")))
        source = set(_without_licenses(_tree(self.source, "usr")))
        self.assertEqual(source - prebuilt, {f"usr/share/pixmaps/{RUNTIME}.png"})
        self.assertEqual(prebuilt - source, set())

    def test_chromedriver_output_excludes_build_artifacts(self):
        drivers = _tree(self.prebuilt_driver, "usr")
        payload = _tree(self.prebuilt, "usr")
        self.assertIn(f"usr/lib/{RUNTIME}/chromedriver", drivers)
        self.assertIn("usr/share/licenses/electron44-bin-chromedriver/LICENSE", drivers)
        self.assertFalse(any(p.endswith(".debug") for p in drivers))
        self.assertFalse(any(p in payload for p in drivers), "split outputs share a file")

    def test_prebuilt_recipe_declares_the_electron44_provision(self):
        fields = {}
        for line in BIN_SRCINFO.read_text().splitlines():
            line = line.strip()
            if "=" in line:
                key, _, value = line.partition(" = ")
                fields.setdefault(key, []).append(value)
        self.assertIn(f"{RUNTIME}=44.11.3", fields.get("provides", []))
        self.assertIn(RUNTIME, fields.get("conflicts", []))
        self.assertIn(f"{RUNTIME}-chromedriver=44.11.3", fields.get("provides", []))
        self.assertIn(f"{RUNTIME}-chromedriver", fields.get("conflicts", []))

    def test_prebuilt_version_is_never_behind_the_source_recipe(self):
        source = _assignment(SOURCE_RECIPE, "pkgver")
        # The -bin recipe composes pkgver from _major and _subver.
        prebuilt = (int(_assignment(BIN_RECIPE, "_major")),
                    *_numbers(_assignment(BIN_RECIPE, "_subver")))
        self.assertGreaterEqual(prebuilt, _numbers(source))

    def test_both_recipes_ship_the_same_launcher_source(self):
        self.assertTrue(
            filecmp.cmp(
                BIN_RECIPE.parent / "electron-launcher.sh",
                SOURCE_RECIPE.parent / "electron-launcher.sh",
                shallow=False,
            ),
            "the two providers must ship the same launcher",
        )


def _assignment(recipe, name):
    prefix = f"{name}="
    for line in recipe.read_text().splitlines():
        if line.startswith(prefix):
            return line[len(prefix):].strip().strip("'\"")
    raise AssertionError(f"no {name} assignment in {recipe}")


def _numbers(text):
    return tuple(int(part) for part in text.split("."))


if __name__ == "__main__":
    unittest.main()
