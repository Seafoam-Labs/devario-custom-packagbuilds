# NVIDIA 620.70.06 beta for Devario

Bleeding-edge NVIDIA beta stack for x86_64. This recipe produces four
packages at the same versions expected by Devario's installer and target
configuration helper:

- `nvidia-utils` — userspace driver, firmware, utilities, X driver, and
  Vulkan/EGL/OpenCL-adjacent payload, including the 32-bit driver libraries.
- `opencl-nvidia` — OpenCL implementation and ICD manifest.
- `lib32-opencl-nvidia` — 32-bit OpenCL implementation.
- `nvidia-open-dkms` — open kernel-module sources for DKMS.

Starting with `620.70.06-2`, `nvidia-utils` provides
`lib32-nvidia-utils=620.70.06`, `lib32-vulkan-driver`, `lib32-opengl-driver`,
and `lib32-nvidia-libgl`. It conflicts with and replaces the old standalone
`lib32-nvidia-utils` and `lib32-nvidia-libgl` packages, taking ownership of
their driver libraries under `/usr/lib32`. Its dependencies include
`lib32-zlib`, `lib32-gcc-libs`, and `lib32-libglvnd`.

Publish all four outputs together and remove the old bleeding-edge
`lib32-nvidia-utils` archive from the repository database. Requests for
`lib32-nvidia-utils` can then resolve through the versioned provide.

These packages intentionally use the normal current-branch names rather than
a versioned `620xx` namespace. Publishing them from `devario-bleeding-edge`
supersedes the `615.78.08` packages in `devario-core` by version only for
repositories where the bleeding-edge repository is enabled. Keep both
repositories available during the transition; do not publish this recipe into
`devario-core` until the beta is promoted.

## Upstream

`620.70.06` is NVIDIA's current Linux beta driver. The stable driver remains
on another branch, so this recipe is deliberately isolated in
`devario-bleeding-edge`.

Sources:

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
used by `devario-core/nvidia-open-dkms` for 615.78.08. The 620.70.06 beta
still calls `filp_open()` without entering the initial filesystem context on
Linux 7.3, so the patch adds `scoped_with_init_fs()` for 7.3 and later. The
patch applies cleanly to the 620 source tarball.

All five modules were compiled against Devario
`7.3.1-1.2-devario` headers during validation.

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

An isolated build still needs the worker's `devario-bleeding-edge` and
`devario-core` repositories available so its dependency closure can resolve
`libglvnd`, `egl-wayland`, `egl-wayland2`, `egl-gbm`, `egl-x11`, and
`lib32-*` packages.

## Validation

- Before the consolidation, native unprivileged Shelly builds completed for
  all five separate archives. The consolidated four-output recipe requires
  a fresh build before publication.
- Both 64-bit and 32-bit archives contain the expected versioned libraries,
  firmware, ICD manifests, and NGX payload; SONAME links resolve inside the
  staged package.
- `nvidia-open-dkms` carries the patched source tree and a complete
  `dkms.conf` declaring all five modules with `kernel-open` build locations.
- The patched 620 source compiled all five modules against Devario
  `7.3.1-1.2-devario` headers.
- Package versions match each other and the exact `nvidia-utils=620.70.06`
  dependency used by DKMS; the bundled multilib payload shares its version.

Not yet tested: GPU runtime on 620.70.06, Wayland/Xorg sessions,
suspend/resume, 32-bit graphics, and a signed ISO install. These require
hardware validation before the beta is promoted.
