# python-myst-parser for Shelly

Based on [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/python-myst-parser/-/blob/main/PKGBUILD), pinned to `5.1.0-1`. Copy the whole directory to the worker, including local patches and `keys/` where present.

Retains the upstream flit-core constraint adjustment and test exclusions. Build after Sphinx, with its declared Markdown and Python runtime dependencies available.

From the repository root:

```sh
shelly build --review-only --json ./python-myst-parser/PKGBUILD
shelly build --isolated --check ./python-myst-parser/PKGBUILD
```

Bash syntax, generated metadata, source checksums, applicable signatures, and source preparation were validated. makepkg and Shelly metadata agree. See [the Zig build guide](../ZIG-BUILDS.md) for build order, bootstrap dependencies, review findings, and the exact limits of local build validation.
