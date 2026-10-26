# NVIDIA 580xx for Devario

Packages NVIDIA **580.178.04** with the active patches and desktop workarounds
from [CachyOS packaging commit 06cda345d91e5e80da524dcc2803c78aaf93f786](https://github.com/CachyOS/CachyOS-PKGBUILDS/tree/06cda345d91e5e80da524dcc2803c78aaf93f786/nvidia/nvidia-580xx).
NVIDIA's `.run` and open-module source archives retain CachyOS's pinned checksums.
The `.run` file is extracted only; `nvidia-installer` is never run.

Both recipes use **epoch 1** so the CachyOS baseline upgrades existing Devario
580.196.07 packages. Keep that epoch on subsequent releases. The driver version
inside binaries, firmware paths, support metadata and DKMS remains 580.178.04.
Package dependencies include the epoch; filenames are taken from repository
metadata rather than inferred from the upstream version.

This recipe produces:

- `nvidia-580xx-utils`: native graphics/compute libraries, GSP firmware,
  utilities, upstream GPU metadata, and system integration.
- `nvidia-580xx-dkms`: proprietary DKMS sources for older supported GPUs,
  including Maxwell, Pascal and Volta.
- `nvidia-580xx-open-dkms`: alternative open DKMS sources for GPUs listed in
  their README. It conflicts with the proprietary modules.
- `opencl-nvidia-580xx`: native OpenCL implementation and ICD manifest.

The companion `../lib32-nvidia-580xx-utils/PKGBUILD` produces
`lib32-nvidia-580xx-utils` and `lib32-opencl-nvidia-580xx`. Utilities require
exactly matching OpenCL and both multilib packages. Publish both recipes
together. Do not combine this stack with the current-branch NVIDIA libraries.
The leaf OpenCL/multilib packages avoid circular dependencies back to utilities,
as in CachyOS; the utility package pins the complete stack.

## CachyOS integration and Devario adaptations

The proprietary modules carry CachyOS's default atomic modesetting and KDE
hardware-cursor patches. The open modules carry the default modesetting and
IBT patches. Both DKMS templates permit PREEMPT_RT builds. The inactive 0003
and 0004 patches present in CachyOS's directory are not applied by its recipe
and are not imported here.

Utilities include CachyOS's application profile limiting VRAM reuse and the
KWin service override selecting egl-wayland2 only for KWin. The matching
`egl-wayland2` dependency is retained. For Aqueous, utilities also install
`/usr/share/uwsm/env-aqueous.d/60-nvidia-580xx-egl.sh`. UWSM exports its EGL
selection to session applications only when `/sys/module/nvidia/version`
starts with `580.`, the egl-wayland2 manifest exists, and
`__EGL_EXTERNAL_PLATFORM_CONFIG_FILENAMES` is unset. Explicit user values,
including an empty value, are preserved. The file is owned by the 580 utilities
package and is removed when that package is removed. Log out and back in after
installing the update. This changes EGL clients, not Aqueous's Vulkan renderer;
other driver branches receive no forced selection from this drop-in.

Devario preserves its explicit modeset
and fbdev options, VRAM preservation, and suspend/hibernate/resume services.
CachyOS's `NVreg_UseKernelSuspendNotifiers` option is not copied: it is absent
from these 580 module sources. The supported 580 VRAM-preservation mechanism
uses `NVreg_PreserveVideoMemoryAllocations=1` and `/var/tmp`.

Devario retains upstream `supported-gpus.json` for installer selection,
versioned provides, complete per-package licenses, safe SONAME links, and
DKMS's configured parallel job count. Open-module build identity uses Devario.
The previous recipe was adapted from
[Arch commit f9ae10b379f8b1d0832ec92bca1c12072aa123e9](https://gitlab.archlinux.org/archlinux/packaging/packages/nvidia-utils/-/tree/f9ae10b379f8b1d0832ec92bca1c12072aa123e9).
Existing contributor notices and patch authorship are retained.

## Build and ISO integration

From the repository root:

```sh
shelly build --review-only --json devario-libs/lib32-nvidia-580xx-utils/PKGBUILD
shelly build --reviewed --nosign devario-libs/lib32-nvidia-580xx-utils/PKGBUILD
shelly build --review-only --json devario-libs/nvidia-580xx-utils/PKGBUILD
shelly build --reviewed --nosign devario-libs/nvidia-580xx-utils/PKGBUILD
```

Use Shelly's `--isolated` option on the release build worker. Regenerate each
recipe's `.SRCINFO` with `shelly build --reviewed --makesrcinfo PKGBUILD` after
changes. Shelly's review warnings for integer arithmetic and Makefile syntax
inside the IBT patch have been inspected.

The `devario-os` repository stages all five proprietary-stack packages and their
signatures in the ISO's offline cache, validates their matching versions and
payloads, and installs them together through Shelly/RLPM when hardware needs
580. Shared multilib dependencies and the OpenCL loader are in the live package
closure. The live image continues to use the current open driver; the optional
580 open DKMS variant is available for manual selection and supported by target
update validation, but is not automatically selected or cached by the ISO.

Install headers matching every target kernel. DKMS/RLPM hooks compile modules
and Devario's normal boot-update workflow rebuilds initramfs. Package changes
do not load drivers or change host services during a build.

## Validation

The native and multilib recipes build all six archives using unprivileged
Shelly. The pinned upstream archive checksums and active patch application have
been verified. All five modules from each DKMS variant compile against Devario
`7.2.12-2.1-devario` headers, with matching driver versions, kernel vermagic and
expected proprietary/open licenses. All six archives have consistent epoch
metadata, package licenses and root ownership; all 93 symlinks resolve.

The five actual proprietary-stack archives pass ISO payload staging with fixture
signatures and dependency records; this exercises their real firmware, GPU tables,
OpenCL and multilib files without claiming production signature verification.
Devario profile validation and the assembler contract tests pass.
GPU rendering, suspend/resume, and a full signed offline ISO installation require
target-system validation before release.
