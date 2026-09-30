# python-sphinx for Shelly

Based on [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/python-sphinx/-/blob/main/PKGBUILD), pinned to `9.1.0-1`. Copy the whole directory to the worker, including local patches and `keys/` where present.

Retains upstream man-page generation and tests. Install its declared Python runtime dependencies before building. The complete check dependencies include TeX packages; they are needed only when running the check hook.

From the repository root:

```sh
shelly build --review-only --json ./python-sphinx/PKGBUILD
shelly build --isolated --check ./python-sphinx/PKGBUILD
```

Bash syntax, generated metadata, source checksums, applicable signatures, and source preparation were validated. makepkg and Shelly metadata agree. See [the Zig build guide](../ZIG-BUILDS.md) for build order, bootstrap dependencies, review findings, and the exact limits of local build validation.
