# Vulkan Headers

Packages [Khronos Vulkan-Headers](https://github.com/KhronosGroup/Vulkan-Headers/tree/v1.4.364)
at `1.4.364-1`, including C/C++ headers, the API registry, and the installed
`Vulkan::Headers` CMake target. This architecture-independent package has no
runtime dependencies. Compiled C++ modules and upstream tests are disabled in
the package build.

Build and install:

```sh
cd vulkan-headers
makepkg -si
```

Or build with Shelly from the repository root:

```sh
shelly build --review-only --json ./vulkan-headers/PKGBUILD
shelly build --isolated ./vulkan-headers/PKGBUILD
```

Use the installed target in CMake:

```cmake
find_package(VulkanHeaders CONFIG REQUIRED)
target_link_libraries(your_target PRIVATE Vulkan::Headers)
```

The headers do not supply the Vulkan loader library; applications calling Vulkan
entry points also need a loader, normally provided by `vulkan-icd-loader`.

Validated locally with Bash syntax checking, generated `.SRCINFO`, SHA-256 source
verification, and a complete makepkg build (dependency checks skipped). Upstream's
installed-package integration example also compiled successfully against the
staged package, resolving `Vulkan::Headers` and compiling its C and C++ consumers.
An isolated Shelly build has not been run.
