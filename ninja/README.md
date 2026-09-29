# ninja for Shelly

Based on [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/ninja/-/blob/main/PKGBUILD), pinned to `1.13.2-3`. Copy the whole directory to the worker, including local patches and `keys/` where present.

Uses the upstream CMake build and CTest suite and packages shell completions, Vim syntax, and the Python helper. Supply CMake, gtest, Python, and re2c on the build worker.

From the repository root:

```sh
shelly build --review-only --json ./ninja/PKGBUILD
shelly build --isolated --check ./ninja/PKGBUILD
```

Bash syntax, generated metadata, source checksums, applicable signatures, and source preparation were validated. makepkg and Shelly metadata agree. See [the Zig build guide](../ZIG-BUILDS.md) for build order, bootstrap dependencies, review findings, and the exact limits of local build validation.
