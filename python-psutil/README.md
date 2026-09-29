# python-psutil for Shelly

Based on [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/python-psutil/-/blob/main/PKGBUILD), pinned to `7.2.2-1`. Copy the whole directory to the worker, including local patches and `keys/` where present.

Retains the upstream wheel build and tests in a temporary virtual environment, including its exclusions for tests unsuitable for a build chroot.

From the repository root:

```sh
shelly build --review-only --json ./python-psutil/PKGBUILD
shelly build --isolated --check ./python-psutil/PKGBUILD
```

Bash syntax, generated metadata, source checksums, applicable signatures, and source preparation were validated. makepkg and Shelly metadata agree. See [the Zig build guide](../ZIG-BUILDS.md) for build order, bootstrap dependencies, review findings, and the exact limits of local build validation.
