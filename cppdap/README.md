# cppdap for Shelly

Based on [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/cppdap/-/blob/main/PKGBUILD), pinned to `1.58.0-3`. Copy the whole directory to the worker, including local patches and `keys/` where present.

Retains the shared-library and GCC 15 fixes, pinned to full commit IDs. Its recipe needs an existing CMake installation; use the bootstrap repository to break the CMake/cppdap dependency cycle. Upstream packaging has no `check()` hook.

From the repository root:

```sh
shelly build --review-only --json ./cppdap/PKGBUILD
shelly build --isolated --check ./cppdap/PKGBUILD
```

Bash syntax, generated metadata, source checksums, applicable signatures, and source preparation were validated. makepkg and Shelly metadata agree. See [the Zig build guide](../ZIG-BUILDS.md) for build order, bootstrap dependencies, review findings, and the exact limits of local build validation.
