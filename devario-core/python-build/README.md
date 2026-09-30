# python-build for Shelly

Based on [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/python-build/-/blob/main/PKGBUILD), pinned to `1.6.0-1`. Copy the whole directory to the worker, including local patches and `keys/` where present.

Uses the regular upstream rebuild path. An existing `python-build`, `python-installer`, and `python-flit-core` must be available in the bootstrap repository. The unused alternate Python-interpreter bootstrap branch was removed; it required a different source list and checksums.

From the repository root:

```sh
shelly build --review-only --json ./python-build/PKGBUILD
shelly build --isolated --check ./python-build/PKGBUILD
```

Bash syntax, generated metadata, source checksums, applicable signatures, and source preparation were validated. makepkg and Shelly metadata agree. See [the Zig build guide](../ZIG-BUILDS.md) for build order, bootstrap dependencies, review findings, and the exact limits of local build validation.
