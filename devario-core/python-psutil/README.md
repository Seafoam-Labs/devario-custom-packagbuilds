# python-psutil for Shelly

Based on [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/python-psutil/-/blob/main/PKGBUILD), pinned to `7.2.2-2`. Copy the whole directory to the worker, including local patches and `keys/` where present.

Retains the upstream wheel build. Package tests and test-only dependencies are omitted.

From the repository root:

```sh
shelly build --review-only --json ./devario-core/python-psutil/PKGBUILD
shelly build --isolated --no-check ./devario-core/python-psutil/PKGBUILD
```

Bash syntax, generated metadata, source checksums, applicable signatures, and source preparation were validated. makepkg and Shelly metadata agree. See [the Zig build guide](../../ZIG-BUILDS.md) for build order, bootstrap dependencies, review findings, and the exact limits of local build validation.
