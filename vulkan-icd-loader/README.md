# Vulkan ICD loader for Shelly

Builds Vulkan Loader 1.4.364 with XCB, Xlib, Xrandr, and Wayland support.
The source archive is pinned by SHA-256. Upstream dependency downloads and
the upstream test suite (which requires a separate GoogleTest source tree)
are disabled.

Build and publish [vulkan-headers](../vulkan-headers/PKGBUILD) first. The isolated
build must install `vulkan-headers>=1.4.364`, including
`/usr/share/cmake/VulkanHeaders/VulkanHeadersConfig.cmake`. Installing headers
only on the host does not make them available inside the build root.

The versioned build dependency supplies the `Vulkan::Headers` target. CMake
also requires successful VulkanHeaders discovery, so absent or incompatible
headers cause an immediate dependency error instead of a later missing-target
error during generation.

From the repository root:

```sh
shelly build --review-only --json ./vulkan-icd-loader/PKGBUILD
shelly build --isolated ./vulkan-icd-loader/PKGBUILD
```

The installed loader needs a Vulkan driver for the GPU at runtime.

Validated Bash syntax, generated `.SRCINFO`, source checksum, and a complete
local `makepkg --nodeps --cleanbuild` build using the staged 1.4.364 headers
through `CMAKE_PREFIX_PATH`. Shelly's review reported no findings. The package
exports `libvulkan.so=1-64`; its only ELF shared-library dependency is
`libc.so.6`. The isolated worker build and upstream test suite were not run.
