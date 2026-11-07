# NVIDIA driver stack for Devario

Current-production NVIDIA stack for x86_64, promoted from the
`devario-bleeding-edge` `nvidia-utils` beta (`620.70.06-2`). This recipe
produces four packages at the same versions expected by Devario's
installer and target configuration helper:

- `nvidia-utils` — userspace driver, firmware, utilities, X driver, and
  Vulkan/EGL/OpenCL-adjacent payload, including the 32-bit driver libraries.
- `opencl-nvidia` — OpenCL implementation and ICD manifest.
- `lib32-opencl-nvidia` — 32-bit OpenCL implementation.
- `nvidia-open-dkms` — open kernel-module sources for DKMS.

`nvidia-utils` provides `lib32-nvidia-utils=620.70.06`,
`lib32-vulkan-driver`, `lib32-opengl-driver`, and `lib32-nvidia-libgl`. It
conflicts with and replaces the old standalone `lib32-nvidia-utils` and
`lib32-nvidia-libgl` packages, taking ownership of their driver libraries
under `/usr/lib32`. Its dependencies include `lib32-zlib`,
`lib32-gcc-libs`, and `lib32-libglvnd`. Requests for `lib32-nvidia-utils`
resolve through the versioned provide, so the standalone recipe retired
with this promotion.

## Publishing

Publish all four outputs together into `devario-core` and, in the same
repository refresh:

- remove the superseded `nvidia-utils` (615.78.08-1), `opencl-nvidia`
  (615.71.09-1), `nvidia-open-dkms` (615.78.08-1), and `lib32-nvidia-utils`
  (615.78.08-1) archives from the `devario-core` database, plus
  `lib32-nvidia-utils` from `devario-libs`;
- remove the `620.70.06-2` archives from `devario-bleeding-edge` so beta
  users move onto the promoted release instead of staying on the beta
  build.

These packages use the normal current-branch names rather than a versioned
`620xx` namespace; the higher version supersedes the 615 stack wherever
`devario-core` is enabled. The `1:580xx` legacy-branch packages in
`devario-libs` are unaffected.

## Upstream

`620.70.06` is the driver branch Devario currently ships. Sources:

- <https://download.nvidia.com/XFree86/Linux-x86_64/620.70.06/NVIDIA-Linux-x86_64-620.70.06.run>
- <https://download.nvidia.com/XFree86/NVIDIA-kernel-module-source/NVIDIA-kernel-module-source-620.70.06.tar.xz>

Both archives are pinned by SHA-512 in the PKGBUILD. The `.run` archive is
extracted with `--extract-only`; `nvidia-installer` is never executed.

## Packaging changes from 615

- Adds `libnvidia-wayland-client`, which the 620 userspace uses for
  `nvidia-settings` on Wayland.
- Adds the 620 NGX payload: `libnvidia-ngx-builtin-dlssd.so.310.9.0` and
  `ngx-builtins/nvngx_dlssd.dll`.
- Installs `supported-gpus/supported-gpus.json` under
  `/usr/share/doc/nvidia/`, which Devario's NVIDIA target helper reads for
  hardware selection.
- Keeps `NVreg_UseKernelSuspendNotifiers=1`, `/var/tmp` video-memory
  preservation, nouveau/nova blacklisting, and the existing suspend/hibernate
  service cleanup script.

## Linux 7.3 patch

`fix-runtime-D3-620.patch` is a rebased version of the runtime-D3 sysfs fix
the 615 DKMS recipe used. The 620.70.06 driver still calls `filp_open()`
without entering the initial filesystem context on Linux 7.3, so the patch
adds `scoped_with_init_fs()` for 7.3 and later. The patch applies cleanly to
the 620 source tarball.

All five modules were compiled against Devario `7.3.1-1.2-devario` headers
during beta validation.

## Build

From this directory:

```sh
shelly build --review-only --json PKGBUILD
shelly build --reviewed --nosign PKGBUILD
```

The same build includes the 32-bit libraries and the OpenCL split package.

Shelly review reports dynamic-command warnings for the DKMS module index
arithmetic and for the retained `vercmp` call in `nvidia-utils.install`.
Both are intentional: the arithmetic indexes the five DKMS module entries,
and the install script compares the previously installed driver version.

Regenerate metadata after recipe changes:

```sh
yes | shelly build --makesrcinfo PKGBUILD > .SRCINFO
```

An isolated build still needs the worker's `devario-core` and `devario-libs`
repositories available so its dependency closure can resolve `libglvnd`,
`egl-wayland`, `egl-wayland2`, `egl-gbm`, `egl-x11`, and `lib32-*` packages.

## Validation

- The beta `620.70.06-2` archives built, signed, and published from
  `devario-bleeding-edge` are the reference payload. The promoted recipe
  differs in `pkgdesc` and `pkgrel` only and needs one fresh `-3` build
  before publication.
- Both 64-bit and 32-bit archives contain the expected versioned libraries,
  firmware, ICD manifests, and NGX payload; SONAME links resolve inside the
  staged package.
- `nvidia-open-dkms` carries the patched source tree and a complete
  `dkms.conf` declaring all five modules with `kernel-open` build locations.
- Package versions match each other and the exact `nvidia-utils=620.70.06`
  dependency used by DKMS; the bundled multilib payload shares its version.
