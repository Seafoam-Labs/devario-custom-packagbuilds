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
                    ["bash", "-ec", 'source "$1"; cd "$2"; pkgname=$3; '
                     'pkgdir=$4; "package_$pkgname"', "bash", str(RECIPE),
                     str(work), name, str(dest)], check=True, capture_output=True,
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

    def test_cpu_install_does_not_require_accelerator_runtimes(self):
        metadata = subprocess.check_output(
            ["makepkg", "--printsrcinfo"], cwd=RECIPE.parent, text=True
        )
        base = metadata.split("\npkgname = ggml\n", 1)[1].split("\npkgname = ", 1)[0]
        dependencies = [line.split(" = ", 1)[1] for line in base.splitlines()
                        if line.strip().startswith("depends = ")]
        self.assertTrue(set(dependencies).isdisjoint(
            {"cuda", "nccl", "zendnn", "openvino", "vulkan-icd-loader"}
        ))
        for name in PACKAGES[1:]:
            section = metadata.split(f"\npkgname = {name}\n", 1)[1].split("\npkgname = ", 1)[0]
            self.assertIn("depends = ggml=0.26.0-3", section)


if __name__ == "__main__":
    unittest.main()
