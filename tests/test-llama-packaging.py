#!/usr/bin/env python3
"""Exercise GGML split-package ownership without a GPU or installed SDKs."""

from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECIPE = ROOT / "devario-libs/ggml/PKGBUILD"
PACKAGES = ("ggml", "ggml-cuda", "ggml-vulkan", "ggml-zendnn", "ggml-openvino")


class GgmlPackaging(unittest.TestCase):
    def test_split_packages_cover_install_without_overlapping_files(self):
        with tempfile.TemporaryDirectory(prefix="devario-ggml-") as directory:
            work = Path(directory)
            # Model the CMake install tree, including the CPU dispatch fallback.
            files = [
                "usr/include/ggml.h",
                "usr/lib/libggml.so.0.26.0",
                "usr/lib/cmake/ggml/ggml-config.cmake",
                "usr/lib/pkgconfig/ggml.pc",
                "usr/lib/ggml/libggml-cpu-x64.so",
                "usr/lib/ggml/libggml-cpu-haswell.so",
                *[f"usr/lib/ggml/lib{name}.so" for name in PACKAGES[1:]],
            ]
            for name in files:
                p = work / "staging" / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(name)
            (work / "staging/usr/lib/libggml.so").symlink_to("libggml.so.0.26.0")
            (work / "ggml").mkdir()
            (work / "ggml/LICENSE").write_text("fixture license")

            owners = {}
            for name in PACKAGES:
                dest = work / "packages" / name
                dest.mkdir(parents=True)
                subprocess.run(
                    [
                        "bash",
                        "-ec",
                        'source "$1"; cd "$2"; pkgname=$3; '
                        'pkgdir=$4; "package_$pkgname"',
                        "bash",
                        str(RECIPE),
                        str(work),
                        name,
                        str(dest),
                    ],
                    check=True,
                    capture_output=True,
                )
                for p in dest.rglob("*"):
                    if p.is_file() or p.is_symlink():
                        relative = p.relative_to(dest).as_posix()
                        self.assertNotIn(relative, owners, f"file conflict: {relative}")
                        owners[relative] = name

            for name in files + ["usr/lib/libggml.so"]:
                self.assertIn(name, owners, f"lost installed file: {name}")
            for name in PACKAGES[1:]:
                self.assertEqual(owners[f"usr/lib/ggml/lib{name}.so"], name)
            self.assertEqual(owners["usr/lib/ggml/libggml-cpu-x64.so"], "ggml")
            for name in PACKAGES:
                self.assertEqual(owners[f"usr/share/licenses/{name}/LICENSE"], name)

    def recipe_metadata(self):
        # No makepkg on this host: source the PKGBUILD and run each package_<name>
        # with only the file-install commands stubbed, then dump the resulting depends.
        output = subprocess.check_output(
            [
                "bash",
                "-c",
                """
set -e
source "$1"
for name in "${pkgname[@]}"; do
  (
    pkgname="$name"
    pkgdir="$PWD/pkg-$name"
    mkdir -p "$pkgdir"
    cp() { :; }
    rm() { :; }
    install() { :; }
    "package_$name"
    printf '==>%s\\n' "$name"
    for dep in "${depends[@]}"; do printf 'depends = %s\\n' "$dep"; done
  )
done
""",
                "bash",
                str(RECIPE),
            ],
            text=True,
        )
        sections = {}
        for block in output.split("==>")[1:]:
            lines = block.splitlines()
            sections[lines[0]] = [
                line.split(" = ", 1)[1]
                for line in lines[1:]
                if line.startswith("depends = ")
            ]
        return sections

    def test_cpu_install_does_not_require_accelerator_runtimes(self):
        sections = self.recipe_metadata()
        base = sections["ggml"]
        self.assertTrue(base)
        self.assertTrue(
            set(base).isdisjoint(
                {"cuda", "nccl", "zendnn", "openvino", "vulkan-icd-loader"}
            )
        )
        pin = subprocess.check_output(
            [
                "bash",
                "-c",
                'source "$1"; printf "%s-%s" "$pkgver" "$pkgrel"',
                "bash",
                str(RECIPE),
            ],
            text=True,
        )
        for name in PACKAGES[1:]:
            self.assertIn(f"ggml={pin}", sections[name])


if __name__ == "__main__":
    unittest.main()
