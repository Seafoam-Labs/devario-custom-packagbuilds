# python-sphinx for Shelly

Based on [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/python-sphinx/-/blob/main/PKGBUILD), pinned to `9.1.0-2`. Copy the whole directory to the worker, including local patches and `keys/` where present.

Retains upstream man-page generation. Install its declared Python runtime dependencies before building. Package tests and their TeX dependencies are omitted.

From the repository root:

```sh
shelly build --review-only --json ./devario-core/python-sphinx/PKGBUILD
shelly build --isolated --no-check ./devario-core/python-sphinx/PKGBUILD
```

Bash syntax, generated metadata, source checksums, applicable signatures, and source preparation were validated. makepkg and Shelly metadata agree. See [the Zig build guide](../../ZIG-BUILDS.md) for build order, bootstrap dependencies, review findings, and the exact limits of local build validation.
