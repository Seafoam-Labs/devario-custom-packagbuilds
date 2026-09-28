# nvidia-utils for Shelly

This x86_64 recipe packages NVIDIA's prebuilt driver utilities as
`nvidia-utils 615.71.09-2`. It is adapted from
[Arch's 615.71.09-1 packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/nvidia-utils/-/tree/f9ae10b379f8b1d0832ec92bca1c12072aa123e9)
at commit `f9ae10b379f8b1d0832ec92bca1c12072aa123e9`.

The recipe produces only `nvidia-utils`. Arch's `opencl-nvidia` and
`nvidia-open-dkms` split packages, the separate kernel-source download, and
DKMS preparation are omitted. Release `2` distinguishes this adaptation from
Arch's release `1`. The utility payload, dependencies, driver provisions,
configuration files, and install script are retained. Path quoting in the
source extraction and SONAME link helper is tightened.

All six bundled configuration sources and the NVIDIA `.run` archive retain
Arch's SHA-512 checksums. The installer is invoked with `--extract-only`;
packaging stages files under `$pkgdir`. `!strip` preserves the prebuilt
binaries. `LICENSE` in this directory covers the imported Arch packaging;
the NVIDIA driver license from the archive is installed with the package.

The package provides `opengl-driver`, `vulkan-driver`, and `nvidia-libgl`.
It retains Arch's conflict/replacement for `nvidia-libgl`. No additional
explicit `.so` provisions are required by the current request.

## Build on the worker

Copy the entire directory, including `nvidia-utils.install`, to the worker.
The build environment needs base-devel and repositories providing `libglvnd`,
`egl-wayland`, `egl-wayland2`, `egl-gbm`, and `egl-x11`. No NVIDIA GPU is needed
to build the archive. From the repository root:

```sh
shelly build --review-only --json ./nvidia-utils/PKGBUILD
shelly build --isolated --check ./nvidia-utils/PKGBUILD
```

There is no upstream `check()` suite for this binary repackaging recipe.
`--check` does not exercise the GPU. After recipe edits, regenerate metadata:

```sh
cd nvidia-utils
makepkg --printsrcinfo > .SRCINFO
```

Inspect the resulting archive before publishing:

```sh
bsdtar -xOf /path/to/nvidia-utils-615.71.09-2-x86_64.pkg.tar.zst .PKGINFO
bsdtar -tvf /path/to/nvidia-utils-615.71.09-2-x86_64.pkg.tar.zst usr/bin/nvidia-modprobe
```

`nvidia-modprobe` should be owned by root with mode `4755`, as in Arch's
recipe. Verify the driver provisions above in `.PKGINFO` and refresh the
worker's repository database after publishing the archive.

## Driver integration

Use an NVIDIA kernel driver with the same upstream version, `615.71.09`.
The local packaging release `-2` does not change that driver version.
Coordinate publication and installation with the matching kernel package;
this recipe does not supply kernel modules. Keep `lib32-nvidia-utils` and
`opencl-nvidia` on the matching release when those optional packages are used.
Confirm that the target GPU supports the selected driver branch before rollout.

The retained modprobe configuration enables open-module suspend notifiers.
The install script disables obsolete NVIDIA suspend services when upgrading
from versions older than `595.58.03-1`, and disables those services on removal.
These hooks run during package transactions, not during the build.

On a test machine running the matching kernel driver, check `nvidia-smi`,
`vulkaninfo --summary`, and OpenGL rendering (`glxinfo -B` in an X session).
Also verify the intended Wayland/Xorg session and suspend/resume behavior.

## Validation

Validated locally with Shelly `3.1.6r4747.g8d61a9e-1`:

- Bash syntax and generated `.SRCINFO`.
- HTTPS download and all seven SHA-512 source checksums.
- Shelly review: one warning for the retained install script's `vercmp`
  command substitution; its version comparison was inspected.
- Successful native, unprivileged Shelly build with `--check`, producing
  `nvidia-utils-615.71.09-2-x86_64.pkg.tar.zst`.
- Archive metadata, unchanged install script, root ownership and mode `4755`
  for `nvidia-modprobe`, and all 61 symlinks resolving inside the staged package.
- All 212 payload paths match Arch's published file manifest. Representative
  CUDA, NVML, EGL, and GLX libraries have the expected ELF64 class and SONAMEs.
  Hashes of `nvidia-smi`, NVML, and GLX binaries match the installed `615.71.09`
  reference binaries.

The isolated build was attempted but could not start because the execution
sandbox prevents sudo privilege elevation. The staged `nvidia-smi` could not
communicate with a running NVIDIA driver, so GPU functionality, graphics
sessions, and suspend/resume remain unverified. Run the isolated build and
hardware checks on the worker/test machine before rollout. No host packages
were installed or services changed during validation.
