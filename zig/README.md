# Zig 0.16 for Shelly

This recipe builds `zig 0.16.0-1` for x86_64 from the
[official release source](https://ziglang.org/download/0.16.0/release-notes.html),
using [Arch's Zig packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/zig/-/blob/main/PKGBUILD).
It installs `/usr/bin/zig`, the standard library and toolchain resources under
`/usr/lib/zig`, and the MIT license. Copy this entire directory to the worker;
`skip-futex2-test.patch` must stay beside the PKGBUILD.

The build needs `cmake`, `llvm21`, `llvm21-libs`, `clang21`, and `lld21`, in
addition to the usual base build tools. Checks also require `lib32-glibc`.
The versioned LLVM 21 packages are required even when newer LLVM packages are
installed. The resulting compiler dynamically links to the LLVM 21 toolchain,
so `clang21`, `lld21`, and `llvm21-libs` remain runtime dependencies.

The recipe retains Arch's upstream relocation fix and the patch that skips
three futex2 tests blocked by build-chroot syscall filters. Every source has a
pinned SHA-256 checksum. Zig's cache stays inside the build directory.

From this repository's root:

```sh
shelly build --review-only --json ./zig/PKGBUILD
shelly build --isolated --check ./zig/PKGBUILD
```

Alternatively, with the declared dependencies installed:

```sh
cd zig
makepkg --cleanbuild --check
```

This package uses the normal `zig` package name and `/usr/bin/zig`; it replaces
an installed `zig` package rather than installing a second compiler alongside
it. The final Zig compiler targets baseline x86_64, Linux 6.6+, and glibc 2.40+,
matching Arch's recipe. C/C++ compilation flags still come from the worker.

See [the dependency build guide](../DEPENDENCY-BUILDS.md) for worker repository
setup. Enable repositories providing the versioned LLVM packages and
`lib32-glibc` before building.

Validation completed: Bash syntax, matching makepkg/Shelly metadata, Shelly
review with no findings, all source checksums, source extraction, patch
application, and CMake configuration with LLVM 21.1.8. The LLVM development
tools used for configuration were extracted under `/tmp`; no host packages
were installed. A full compiler build and upstream test run have not been
performed locally.
