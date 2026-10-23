# NVIDIA 580xx for Devario

Packages NVIDIA **580.196.07**, the latest Linux x86_64 580-series display
driver verified on 2026-10-22, from the
[official NVIDIA release directory](https://download.nvidia.com/XFree86/Linux-x86_64/580.196.07/).
The `.run` archive is pinned with NVIDIA's published SHA-256 checksum and is
used only for extraction; `nvidia-installer` is never run.

This split PKGBUILD produces:

- `nvidia-580xx-utils`: native graphics/compute libraries, GSP firmware,
  command-line utilities, and system integration.
- `nvidia-580xx-dkms`: proprietary kernel sources for DKMS, including
  `nvidia`, `nvidia-modeset`, `nvidia-drm`, `nvidia-uvm`, and `nvidia-peermem`.
- `opencl-nvidia-580xx`: optional OpenCL implementation and ICD manifest.

The proprietary modules support the older GPUs retained by the 580 branch,
including Maxwell, Pascal, and Volta. Check the release's supported GPU list
for the specific device. The existing `nvidia-utils` recipe remains on its
current branch; installing this alternative conflicts with that package.
DKMS and OpenCL depend on exactly the same 580xx utility version.

## Build

From the repository root, with base-devel available:

```sh
shelly build --review-only --json devario-libs/nvidia-580xx-utils/PKGBUILD
shelly build --reviewed --nosign devario-libs/nvidia-580xx-utils/PKGBUILD
```

For release builds, use Shelly's `--isolated` option on the build worker.
Regenerate metadata after changes:

```sh
shelly build --reviewed --makesrcinfo devario-libs/nvidia-580xx-utils/PKGBUILD > devario-libs/nvidia-580xx-utils/.SRCINFO
```

Install the utility and DKMS packages together with headers matching every
target kernel. Devario's DKMS/RLPM hooks compile the modules during package
transactions. Rebuild the target's initramfs through its normal boot-update
workflow before rebooting. This recipe does not alter the ISO's driver
selection or GPU detection policy.

The utility install hook enables NVIDIA's suspend, hibernate, resume, and
suspend-then-hibernate services, paired with
`NVreg_PreserveVideoMemoryAllocations=1`. `/var/tmp` must have enough space
for saved video memory. The 595+ open-module suspend-notifier setting is
deliberately absent. DRM modesetting and fbdev are enabled.

32-bit libraries are not included. Applications requiring them need a matching
580xx multilib package; the repository's `lib32-nvidia-utils` for the newer
driver cannot be mixed with this version.

## Provenance and validation

Adapted from the `../../devario-core/nvidia-utils` recipe, originally based on
[Arch packaging commit f9ae10b379f8b1d0832ec92bca1c12072aa123e9](https://gitlab.archlinux.org/archlinux/packaging/packages/nvidia-utils/-/tree/f9ae10b379f8b1d0832ec92bca1c12072aa123e9).
The bundled `LICENSE` covers that packaging; each output installs NVIDIA's
driver license. The payload is adjusted to the actual 580 archive, and the
DKMS configuration is generated from its supplied template.

Validated locally:

- Bash syntax, Shelly review, generated `.SRCINFO`, and all source checksums.
  Shelly flags the DKMS loop's integer increment as dynamic command
  construction; it was reviewed and is ordinary shell arithmetic.
- Successful native, unprivileged Shelly build of all three package archives.
- Archive dependency/conflict metadata, distinct payloads, all 59 symlinks,
  utility archive root ownership, and `nvidia-modprobe` mode `4755`.
- Representative binaries match the downloaded archive byte for byte.
- All five modules compile from the packaged DKMS sources against Devario
  `7.2.12-2.1-devario` headers, using the generated DKMS make command.

No driver was installed or loaded, and no host services were changed.
An isolated build, a full DKMS install transaction, GPU rendering, and
suspend/resume still need validation on a target system before publication.
