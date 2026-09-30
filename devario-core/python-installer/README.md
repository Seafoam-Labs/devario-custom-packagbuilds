# python-installer for Shelly

Based on [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/python-installer/-/blob/main/PKGBUILD), pinned to `1.0.1-1`. Copy the whole directory to the worker, including local patches and `keys/` where present.

Uses the regular upstream rebuild path with existing Python build, installer, and flit-core packages. The unused alternate Python-interpreter bootstrap branch was removed. Windows launcher executables are removed from the installed package.

From the repository root:

```sh
shelly build --review-only --json ./python-installer/PKGBUILD
shelly build --isolated --check ./python-installer/PKGBUILD
```

Bash syntax, generated metadata, source checksums, applicable signatures, and source preparation were validated. makepkg and Shelly metadata agree. See [the Zig build guide](../ZIG-BUILDS.md) for build order, bootstrap dependencies, review findings, and the exact limits of local build validation.
