# Venus Vulkan guest driver

This recipe builds only the VirtIO Vulkan driver from Mesa 26.2.4 for x86_64
Devario guests. It installs `libvulkan_virtio.so`, `virtio_icd.json`, and the
upstream license. Wayland and X11 presentation are enabled. Existing Mesa
packages continue to supply OpenGL, physical GPU drivers, and Vulkan layers.

Package release 2 includes `0001-venus-preserve-drm-identity-for-wlroots.patch`.
Mesa's NVIDIA WSI workaround hides the guest DRM identity that wlroots needs to
match its Vulkan renderer to the display device. The patch preserves that
identity for instances whose engine name is `wlroots` and which do not enable
`VK_KHR_surface`. NVIDIA WSI clients retain the existing workaround, and the
upstream Gamescope exception is unchanged. The change is confined to Venus.

The version and epoch match the inspected Devario repository snapshot. The
implicit Vulkan layers dependency is pinned to the same upstream Mesa version;
update these packages together when moving to another Mesa release. This recipe
does not require rebuilding unrelated Mesa drivers for the current snapshot.

The source checksum and release signing fingerprint were checked against the
[official Arch Mesa recipe](https://gitlab.archlinux.org/archlinux/packaging/packages/mesa/-/blob/main/PKGBUILD).
The source archive is downloaded from the Mesa release server and verified with
SHA-256 and its detached signature. Make the upstream release key available to
the build account, verifying fingerprint
`57551DE15B968F6341C248F68D8E31AFC32428A6` before importing it.

From the package repository root:

```sh
shelly build --review-only --json ./devario-core/vulkan-virtio/PKGBUILD
shelly build --isolated ./devario-core/vulkan-virtio/PKGBUILD
```

Build and publish the signed package through the normal Devario repository
workflow before adding it to a release ISO. The guest driver also requires a
Venus-capable host configuration; packaging alone does not enable accelerated
Vulkan. See the OS repository's `docs/VENUS-VIRTIO-PLAN.md` for host setup and
live/installed image acceptance.

Validation on 2026-10-05: source SHA-256 matched upstream metadata and the
detached signature verified successfully. The recipe's build and package
functions completed in a temporary directory on the development host. The
three-file payload, ICD library reference, dynamic library dependencies, and
exported Vulkan ICD entry point were checked. Bash syntax and Shelly metadata
generation passed; Shelly review reported no findings. A clean isolated package
build, signed publication, ISO integration, and VM graphics acceptance remain
pending.

Validation of release 2 on 2026-10-06: the patch applied without fuzz to the
checksum-verified Mesa 26.2.4 archive. The recipe's `prepare()`, `build()`, and
`package()` functions completed on the development host with no compiler
warnings. Generated metadata, patch checksum, upgrade ordering, ICD reference,
and the three-file payload passed checks; Shelly review reported no findings.
Six real-driver probes in an NVIDIA RTX 5090 / proprietary 615.71.09 Venus VM
confirmed the original wlroots failure, restored guest DRM identity with the
patched renderer, retained the workaround for unnamed clients, other engines,
and wlroots instances enabling `VK_KHR_surface`, and preserved the Gamescope
exception. These probes test device identity, not full desktop acceptance.
An isolated signed package build and full NVIDIA desktop, greeter, client, and
installer acceptance are still required before publication.
