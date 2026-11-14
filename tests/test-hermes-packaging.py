#!/usr/bin/env python3
"""Guard the hermes-agent split-output contract without building ~37k files.

One recipe base (`pkgbase=hermes-agent`) emits the agent runtime and the Electron
desktop app, so the desktop output's `hermes-agent>=pkgver` sibling dependency can
never be published against an older runtime than itself. The pairs below are what
keeps that promise and what keeps pm's tool store satisfied: the store set in
`system-tools.py` against the runtime output's `depends`, `_electron` against the
launcher's `exec` line and against the recipe that publishes that runtime, and the
install-stamp fields that make `hermes update` refuse. The desktop packaging
function runs against a fixture tree, and the launcher's own test (shipped from
the AUR recipe) runs against the launcher exactly as packaged — no downloads, no
chroot, no Electron.
"""

from pathlib import Path
import ast
import os
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECIPE = ROOT / "devario-productivity/hermes-agent"
PKGBUILD = (RECIPE / "PKGBUILD").read_text()
LAUNCHER = (RECIPE / "hermes-desktop").read_text()
AGENT_ENV = (RECIPE / "hermes_agent_env.py").read_text()
SYSTEM_TOOLS = ast.parse((RECIPE / "system-tools.py").read_text())
ELECTRON_PROVIDER = ROOT / "devario-libs/electron44-bin/PKGBUILD"

# pm package in system-tools.py's TOOLS -> the package that provides the command.
STORE_PACKAGES = {
    "node": "nodejs",
    "npm": "npm",
    "pnpm": "pnpm",
    "ffmpeg": "ffmpeg",
    "ripgrep": "ripgrep",
    "python": "python",
    "uv": "uv",
}


def _scalar(text, name):
    """A top-level `name=value` scalar, ignoring its trailing comment."""
    match = re.search(rf"^{re.escape(name)}=(\S+)", text, re.M)
    if not match:
        raise AssertionError(f"{name} is not declared at the top level")
    return match.group(1)


def _code():
    """The recipe without its comment lines."""
    return "\n".join(l for l in PKGBUILD.splitlines() if not l.lstrip().startswith("#"))


def _function(name):
    match = re.search(rf"^{re.escape(name)}\(\) \{{\n(.*?)^\}}", PKGBUILD, re.M | re.S)
    if not match:
        raise AssertionError(f'{RECIPE / "PKGBUILD"} defines no {name}()')
    return match.group(1)


def _array(name, where=PKGBUILD):
    """Elements of the first `name=(...)` array in `where`."""
    start = where.index(f"{name}=(") + len(f"{name}=(")
    depth, end = 1, start
    while depth:
        if where[end] == "(":
            depth += 1
        elif where[end] == ")":
            depth -= 1
        end += 1
    return [token.strip("'\"") for token in where[start:end - 1].split() if not token.startswith("#")]


def _literal(tree, name):
    """A module-level literal assignment of a parsed module."""
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == name for target in node.targets
        ):
            return ast.literal_eval(node.value)
    raise AssertionError(f"system-tools.py assigns no {name}")


def _run_package(srcdir, pkgdir, function="package_hermes-agent-desktop"):
    return subprocess.run(
        [
            "bash", "-e", "-c",
            'source "$1"; srcdir="$2"; pkgdir="$3"; pkgname=hermes-agent-desktop; '
            'cd "$srcdir"; ' + function,
            "fixture", str(RECIPE / "PKGBUILD"), str(srcdir), str(pkgdir),
        ],
        capture_output=True, text=True,
    )


def _fixture(source):
    """The extract directory package_hermes-agent-desktop() expects, minus the build."""
    shutil.copy2(RECIPE / "hermes-desktop", source / "hermes-desktop")
    tree = source / "hermes-agent-0.23.1"
    resources = tree / "apps/desktop/release/linux-unpacked/resources"
    (resources / "app.asar.unpacked/dist/assets").mkdir(parents=True)
    (resources / "app.asar").write_text("asar")
    (resources / "app.asar.unpacked/dist/assets/main-abc123.css").write_text(".flex{display:flex}")
    (resources / "install-stamp.json").write_text('{"builtAt":"2026-11-14T00:00:00.000Z"}\n')
    (tree / "apps/desktop/assets").mkdir(parents=True)
    (tree / "apps/desktop/assets/icon.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    (tree / "LICENSE").write_text("MIT\n")


class SplitDeclaration(unittest.TestCase):
    def test_one_base_emits_both_outputs_in_order(self):
        self.assertEqual(_scalar(PKGBUILD, "pkgbase"), "hermes-agent")
        self.assertEqual(_array("pkgname"), ["hermes-agent", "hermes-agent-desktop"])
        for function in ("package_hermes-agent", "package_hermes-agent-desktop"):
            _function(function)

    def test_desktop_pins_the_sibling_output_not_a_bin_twin(self):
        depends = _array("depends", _function("package_hermes-agent-desktop"))
        self.assertIn("hermes-agent>=${pkgver}", depends)
        self.assertIn("${_electron}", depends)
        self.assertNotIn("conflicts=", _code())
        self.assertNotIn("provides=", _code())
        for entry in depends + _array("optdepends", _function("package_hermes-agent-desktop")):
            self.assertNotIn("-bin", entry)

    def test_x86_64_only_while_the_pnpm_pin_is(self):
        self.assertEqual(_array("arch"), ["x86_64"])
        self.assertIn("@pnpm/exe.linux-x64", PKGBUILD)


class ElectronWiring(unittest.TestCase):
    def test_launcher_names_the_system_runtime_and_the_agent_cli(self):
        electron = _scalar(PKGBUILD, "_electron")
        libdir = _scalar(PKGBUILD, "_libname")
        self.assertIn(f"exec /usr/bin/{electron} ", LAUNCHER)
        self.assertIn("export HERMES_DESKTOP_HERMES=/usr/bin/hermes", LAUNCHER)
        self.assertIn(f"export HERMES_DESKTOP_RESOURCES_PATH=/usr/lib/{libdir}", LAUNCHER)
        self.assertIn("export HERMES_DESKTOP_PACKAGE_MANAGED_RUNTIME=1", LAUNCHER)
        # The agent runtime is this recipe's own output; no AUR helper, no -bin twin.
        self.assertNotIn("AUR", LAUNCHER)
        self.assertNotIn("-bin", LAUNCHER)

    def test_named_runtime_is_published_by_this_tree(self):
        provider = ELECTRON_PROVIDER.read_text()
        self.assertEqual(_scalar(PKGBUILD, "_electron"), "electron" + _scalar(provider, "_major"))
        self.assertIn("_runtime=electron${_major}", provider)
        self.assertIn('provides=("${_runtime}=${pkgver}")', provider)

    def test_the_runtime_that_gets_staged_is_installed_while_building(self):
        # prepare() copies /usr/lib/electronNN over the locked electron package's
        # dist/ and check() loads node-pty under that binary, so the build root has
        # to hold the runtime. The desktop output's depends=() does not do it: the
        # resolver hands bootstrap/build/check requirements to the root and treats
        # split depends as installer metadata (electron44 resolves through
        # devario-libs/electron44-bin's provides).
        self.assertIn("${_electron}", _array("makedepends"))
        self.assertIn('! -s "/usr/lib/${_electron}/version"', _function("prepare"))

    def test_an_older_system_runtime_is_refused(self):
        prepare = _function("prepare")
        self.assertIn("${locked_electron%%.*} > ${system_electron%%.*}", prepare)
        self.assertIn('"/usr/lib/${_electron}/version"', prepare)
        # Upstream's packager admits only a dist/version naming its own lock.
        self.assertIn('"${electron_dir}/dist/version"', prepare)


class StoreAgainstDepends(unittest.TestCase):
    def test_every_stored_tool_is_a_dependency(self):
        self.assertEqual(sorted(_literal(SYSTEM_TOOLS, "TOOLS")), sorted(STORE_PACKAGES))
        self.assertEqual(_literal(SYSTEM_TOOLS, "ON_PATH"), ("node", "npm"))
        depends = _array("depends", _function("package_hermes-agent"))
        for package in STORE_PACKAGES.values():
            self.assertTrue(
                any(re.split(r"[<>=]", entry)[0] == package for entry in depends),
                f"system-tools.py stores {package}, depends=() does not require it",
            )

    def test_python_minor_is_pinned_by_both_the_venv_and_depends(self):
        # The venv only runs on the minor it was built for, so depends=() must
        # ask for that minor and no newer — and the interval must not be empty.
        low = tuple(map(int, _scalar(PKGBUILD, "_pyver").split(".")))
        high = tuple(map(int, _scalar(PKGBUILD, "_pymax").split(".")))
        self.assertLess(low, high)
        package = _function("package_hermes-agent")
        self.assertIn("python>=${_pyver}", package)
        self.assertIn("python<${_pymax}", package)
        self.assertIn('--python "/usr/bin/python${_pyver}"', _function("build"))
        self.assertIn("UV_PYTHON_DOWNLOADS=never", _function("build"))


class StampAndRuntimeDir(unittest.TestCase):
    def test_stamp_names_pacman_as_steward_and_the_store_as_runtime_dir(self):
        package = _function("package_hermes-agent")
        self.assertEqual(_scalar(PKGBUILD, "_optname"), "hermes-agent")
        self.assertIn("--update-mechanism external", package)
        self.assertIn('stamp["distribution"] = "pacman"', package)
        self.assertIn('stamp["runtimeDir"] = store', package)
        self.assertIn('"/opt/${_optname}/system-store/tools"', package)
        self.assertIn('venv/bin/python -B "$srcdir/system-tools.py"', package)

    def test_lazy_installs_leave_opt_and_the_agent_tree_sealed(self):
        package = _function("package_hermes-agent")
        self.assertIn("HERMES_DISABLE_LAZY_INSTALLS=1", package)
        self.assertIn('HERMES_LAZY_INSTALL_TARGET="$XDG_DATA_HOME/hermes-agent/python"', package)
        self.assertIn('os.environ.get("XDG_DATA_HOME")', AGENT_ENV)
        self.assertIn('"/opt/hermes-agent/apps/desktop/dist-webapp"', AGENT_ENV)
        self.assertIn('export HERMES_WEBAPP_DIST=/opt/${_optname}/apps/desktop/dist-webapp', package)
        self.assertEqual(_scalar(PKGBUILD, "_optname"), "hermes-agent")
        # No package hook, no shipped unit: config seeding stays in first-run.
        self.assertFalse(re.search(r"^install=", PKGBUILD, re.M))
        self.assertNotIn(".service", PKGBUILD)


class BuildGuards(unittest.TestCase):
    def test_version_drift_stops_the_build(self):
        self.assertIn("move _pnpmver and sha256sums_x86_64", _function("prepare"))
        self.assertIn("raise _uvmin", _function("check"))
        self.assertEqual(len(re.findall(r"^  patch --batch --fuzz=0", PKGBUILD, re.M)), 6)

    def test_the_icon_lands_in_a_directory_of_its_own_size(self):
        # assets/icon.png is 1024x1024; the AUR recipe installs it under a
        # hicolor size directory that disagrees with the bitmap.
        self.assertIn("hicolor/1024x1024/apps/${_upstream,,}.png", PKGBUILD)

    def test_builder_resources_are_allowlisted_and_the_renderer_is_styled(self):
        package = _function("package_hermes-agent-desktop")
        self.assertIn("unexpected electron-builder resource", package)
        for resource in ("app.asar", "app.asar.unpacked", "install-stamp.json", "icon.ico",
                         "app-update.yml", "default_app.asar"):
            self.assertIn(resource, package)
        self.assertIn(r"'\.flex{'", _function("check"))

    def test_strip_stays_out_of_makepkg_hands(self):
        self.assertIn("!strip", _array("options"))
        self.assertIn("strip --strip-unneeded", _function("package_hermes-agent"))
        self.assertIn("compileall", _function("package_hermes-agent"))
        package = _function("package_hermes-agent")
        self.assertIn('rm -f "$_optdir/venv/.lock"', package)
        self.assertIn("chmod -R a+rX", package)


class DesktopPackaging(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="devario-hermes-")
        self.addCleanup(self.temp.cleanup)
        self.srcdir = Path(self.temp.name)
        _fixture(self.srcdir)
        self.dest = self.srcdir / "pkg"
        self.dest.mkdir()

    def test_ships_resources_launcher_and_desktop_entry(self):
        result = _run_package(self.srcdir, self.dest)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        lib = self.dest / "usr/lib/hermes-agent-desktop"
        for path in (
            lib / "app.asar",
            lib / "app.asar.unpacked/dist/assets/main-abc123.css",
            lib / "install-stamp.json",
            self.dest / "usr/bin/hermes-desktop",
            self.dest / "usr/share/applications/hermes-desktop.desktop",
            self.dest / "usr/share/icons/hicolor/1024x1024/apps/hermes.png",
            self.dest / "usr/share/licenses/hermes-agent-desktop/LICENSE",
        ):
            self.assertTrue(path.is_file(), f"{path.relative_to(self.dest)} is missing")
        self.assertTrue(os.access(self.dest / "usr/bin/hermes-desktop", os.X_OK))
        desktop = (self.dest / "usr/share/applications/hermes-desktop.desktop").read_text()
        self.assertIn("Exec=/usr/bin/hermes-desktop %U", desktop)
        self.assertIn("MimeType=x-scheme-handler/hermes;", desktop)
        self.assertIn("StartupWMClass=Hermes", desktop)
        # The Icon= key must name the bitmap the recipe actually installs.
        icon = re.search(r"^Icon=(\S+)$", desktop, re.M).group(1)
        self.assertTrue(
            (self.dest / f"usr/share/icons/hicolor/1024x1024/apps/{icon}.png").is_file()
        )
        # Electron itself is never carried: the launcher runs /usr/bin/electronNN.
        self.assertFalse((lib / "electron").exists())

    def test_an_unexpected_builder_resource_stops_the_packaging(self):
        (self.srcdir / "hermes-agent-0.23.1/apps/desktop/release/linux-unpacked"
         "/resources/chrome_100_percent.pak").write_text("new resource")
        result = _run_package(self.srcdir, self.dest)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unexpected electron-builder resource", result.stdout + result.stderr)

    def test_a_missing_asar_stops_the_packaging(self):
        (self.srcdir / "hermes-agent-0.23.1/apps/desktop/release/linux-unpacked"
         "/resources/app.asar").unlink()
        result = _run_package(self.srcdir, self.dest)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing required app resources", result.stdout + result.stderr)

    @unittest.skipUnless(shutil.which("node"), "the launcher's own tests need node")
    def test_the_launcher_behaves_as_packaged(self):
        result = subprocess.run(
            ["node", str(RECIPE / "launcher.test.cjs")],
            capture_output=True, text=True,
            env={"PATH": os.pathsep.join(filter(None, [os.path.dirname(shutil.which("node")), "/usr/bin", "/bin"])),
                 "HOME": tempfile.gettempdir(), "TMPDIR": tempfile.gettempdir(),
                 "HERMES_LAUNCHER_PATH": str(RECIPE / "hermes-desktop")},
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        # node:test in either reporter format: four launcher cases, none failing.
        self.assertRegex(result.stdout, r"(?:#|\u2139) pass 4")
        self.assertNotRegex(result.stdout, r"(?:#|\u2139) fail [1-9]")


class PublishedMetadata(unittest.TestCase):
    """`.SRCINFO` is what the resolver and the builder read, not the shell variables."""

    def sections(self):
        text = (RECIPE / ".SRCINFO").read_text()
        parts = re.split(r"^pkgname = ", text, flags=re.M)
        self.assertEqual([p.splitlines()[0] for p in parts[1:]], ["hermes-agent", "hermes-agent-desktop"])
        return parts[1:]

    def test_version_dependency_intervals_are_not_empty(self):
        def number(value):
            return tuple(int(part) for part in re.findall(r"\d+", value.split("-", 1)[0]))

        for section in self.sections():
            above, below = {}, {}
            for dep in re.findall(r"^\tdepends = (\S+)$", section, re.M):
                match = re.fullmatch(r"([A-Za-z0-9@._+-]+?)([<>]=?)(.+)", dep)
                if not match:
                    continue
                name, operator, version = match.groups()
                (above if operator in (">", ">=") else below).setdefault(name, []).append(number(version))
            for name, floors in above.items():
                for ceiling in below.get(name, ()):
                    self.assertTrue(any(floor < ceiling for floor in floors),
                                    f".SRCINFO asks for {name}>={floors} and {name}<{ceiling}")

    def test_the_electron_runtime_reaches_the_isolated_build_root(self):
        base = (RECIPE / ".SRCINFO").read_text().split("pkgname = ", 1)[0]
        self.assertIn("\tmakedepends = electron44", base)

    def test_sibling_provisions_survive_the_split(self):
        agent, desktop = self.sections()
        self.assertIn("\tdepends = hermes-agent>=0.23.1", desktop)
        self.assertIn("\tdepends = electron44", desktop)
        self.assertIn("\tdepends = python>=3.14", agent)
        self.assertIn("\tdepends = python<3.15", agent)
        self.assertNotIn("\tconflicts = ", agent + desktop)
        self.assertNotIn("\tprovides = ", agent + desktop)


if __name__ == "__main__":
    unittest.main()
