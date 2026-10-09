# python-wheel for Shelly

Based on [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/python-wheel/-/blob/main/PKGBUILD), pinned to `0.48.0-2`. Copy the whole directory to the worker, including local patches and `keys/` where present.

Uses the regular upstream rebuild path with existing Python build, installer, and flit-core packages. The unused alternate Python-interpreter bootstrap branch was removed.

From the repository root:

```sh
shelly build --review-only --json ./devario-core/python-wheel/PKGBUILD
shelly build --isolated --no-check ./devario-core/python-wheel/PKGBUILD
```

Bash syntax, generated metadata, source checksums, applicable signatures, and source preparation were validated. makepkg and Shelly metadata agree. See [the Zig build guide](../../ZIG-BUILDS.md) for build order, bootstrap dependencies, review findings, and the exact limits of local build validation.
