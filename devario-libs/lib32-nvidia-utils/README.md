# lib32-nvidia-utils

Packages NVIDIA's 32-bit driver libraries for x86_64 systems, pinned to
`615.71.09` to match `devario-core/nvidia-utils`. The dependency
`nvidia-utils=615.71.09` permits the native package's local release `-2`.
Update both driver versions together.

The recipe is adapted from [Arch Linux's lib32-nvidia-utils PKGBUILD](https://gitlab.archlinux.org/archlinux/packaging/packages/lib32-nvidia-utils/-/blob/main/PKGBUILD),
retrieved on 2026-10-16 (upstream version `615.78.08-1`; downloaded recipe
SHA-256 `a05b3f41a191dd7e040598ea6c456532a995b541eb2bf3822386c7686816029b`).
It produces only `lib32-nvidia-utils`, omitting Arch's `lib32-opencl-nvidia`
split package. The NVIDIA archive URL and SHA-512 checksum match the local
native recipe. Extraction runs in `prepare()`, and the SONAME link helper
uses the quoted implementation from that native recipe.

Libraries are installed under `/usr/lib32`, including OpenGL/EGL, Vulkan,
GBM, VDPAU, CUDA, video encoding/decoding, and optical flow support.
GLVND dispatch libraries come from `lib32-libglvnd`. Vendor manifests and
the NVIDIA license come from the required native `nvidia-utils` package;
the license directory links to that package. `!strip` preserves the vendor
binaries. The bundled `LICENSE` covers the adapted Arch packaging.

Build from the repository root with base-devel and the declared dependencies
available:

```sh
shelly build --review-only --json ./devario-libs/lib32-nvidia-utils/PKGBUILD
shelly build --isolated --check ./devario-libs/lib32-nvidia-utils/PKGBUILD
```

Regenerate metadata after recipe changes:

```sh
shelly build --makesrcinfo ./devario-libs/lib32-nvidia-utils/PKGBUILD > devario-libs/lib32-nvidia-utils/.SRCINFO
```

Validation performed locally: Bash syntax, generated `.SRCINFO`, Shelly
review with no findings, NVIDIA archive SHA-512 verification, and successful
execution of `prepare()` and `package()` in a temporary staging directory.
All 21 staged libraries are ELF32; all 36 library symlinks resolve within
the staged package. The license symlink targets the native package as intended.
A complete isolated package build and GPU runtime tests have not been run.
There is no upstream `check()` suite for this binary repackaging recipe;
validate with a 32-bit OpenGL/Vulkan application on a system running the
matching NVIDIA kernel driver.
