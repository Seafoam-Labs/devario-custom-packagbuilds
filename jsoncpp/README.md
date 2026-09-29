# jsoncpp for Shelly

Based on [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/jsoncpp/-/blob/main/PKGBUILD), pinned to `1.9.8-2`. Copy the whole directory to the worker, including local patches and `keys/` where present.

Produces `jsoncpp` and `jsoncpp-doc`. Includes shared and static libraries, documentation, and upstream tests. Explicitly provides `libjsoncpp.so=27-64` for Shelly and checks the installed ELF class and SONAME before packaging. Retains Arch's removal of the broken upstream CMake configuration. The documentation copy leaves ownership assignment to the package builder instead of preserving source-tree ownership under fakeroot.

From the repository root:

```sh
shelly build --review-only --json ./jsoncpp/PKGBUILD
shelly build --isolated --check ./jsoncpp/PKGBUILD
```

Bash syntax, generated metadata, source checksums, applicable signatures, and source preparation were validated. makepkg and Shelly metadata agree. See [the Zig build guide](../ZIG-BUILDS.md) for build order, bootstrap dependencies, review findings, and the exact limits of local build validation.
