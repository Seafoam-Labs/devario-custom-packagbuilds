# Venus Vulkan guest driver

This recipe builds only the VirtIO Vulkan driver from Mesa 26.2.4 for x86_64
Devario guests. It installs `libvulkan_virtio.so`, `virtio_icd.json`, and the
upstream license. Wayland and X11 presentation are enabled. Existing Mesa
packages continue to supply OpenGL, physical GPU drivers, and Vulkan layers.

Package release 3 includes `0001-venus-preserve-identity-use-wsi-blit-policy.patch`.
It replaces release 2's engine-name exception. Venus keeps its public DRM/PCI
identity for all applications; its WSI device explicitly requests the PRIME
buffer-blit path for NVIDIA instead of falsifying device properties. The older
NVIDIA-driver software-WSI restriction remains in place. No application or engine
name selects the workaround.

The recipe builds only Venus, including its private copy of Mesa's common WSI.
This does not patch the WSI embedded in other installed Vulkan drivers.
`check()` compiles and runs the production Venus initialization and WSI selection
functions with test doubles to check identity preservation, the NVIDIA copy
policy, the older-driver restriction, unaffected native paths, and initialization
failure. It does not require a GPU.

This patch addresses device identification and WSI path selection. The recorded
Zink modifier, memory-allocation, and synchronization errors remain separate
acceptance work. A successful build or policy test does not qualify the package
for automatic VM rollout.

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

Validation of release 3 on 2026-10-07: the replacement patch applied without fuzz
or offsets to the checksum-verified Mesa 26.2.4 archive. The recipe's `prepare()`,
`build()`, `check()`, and `package()` functions completed in a temporary directory
on the development host; compilation reported no warnings. The policy tests,
source/patch/test checksums, regenerated `.SRCINFO`, package upgrade ordering,
ICD library reference, exported ICD entry point, and exact three-file payload
passed. Shelly review reported no findings. This run did not repeat signature
verification of the unchanged source archive or the release 2 VM identity probes.
An isolated signed package build and full VM/client acceptance remain pending.
