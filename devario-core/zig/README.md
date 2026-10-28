# Zig 0.17 for Shelly

This recipe builds `zig 0.17.0-1` for x86_64 from the
[official release source](https://ziglang.org/download/0.17.0/release-notes.html).
The archive checksum matches the [upstream index](https://ziglang.org/download/index.json).
It installs `/usr/bin/zig`, `/usr/lib/zig`, and the MIT license.

For Zig 0.16, use [zig-0.16](../zig-0.16/README.md). That package provides
`zig=0.16.0`, preserving existing dependency pins. The two packages conflict
because they install the same compiler command and library paths.

## Prerequisites and build order

Zig 0.17 requires LLVM 22. LLVM 21 and 23 cannot substitute for it.
Build and publish these recipes in order, refreshing the worker repository
between stages:

1. [llvm22](../llvm22/PKGBUILD), producing `llvm22` and `llvm22-libs` at `22.1.8-3`.
2. [clang22](../clang22/README.md) and [lld22](../lld22/README.md), each at
   `22.1.8-1`, built against that LLVM release.
3. This `zig` recipe with checks enabled. Checks require `lib32-glibc`.

The build requires CMake and searches `/usr/lib/llvm22` first. Runtime
dependencies pin the matching Clang, LLD, and LLVM libraries. Packaging runs
`zig version` with `LD_BIND_NOW=1` to detect unresolved startup symbols,
including when the full tests are disabled. The compiler targets baseline
x86_64, Linux 6.6+, and glibc 2.40+.

Copy this entire directory to the worker, including `skip-futex2-test.patch`.
The patch skips three futex2 tests blocked by build-chroot syscall filters.
The 0.16 relocation backport is omitted because 0.17 already includes it.

```sh
shelly build --review-only --json ./devario-core/zig/PKGBUILD
shelly build --isolated --check ./devario-core/zig/PKGBUILD
```

See [the dependency build guide](../../DEPENDENCY-BUILDS.md) for worker setup.

## Validation

Bash syntax, Shelly metadata generation and review, source checksums, and
`prepare()` passed for both Zig recipes. Shelly review reported no findings.
The source's CMake LLVM version check and build-test options were inspected.
Full compiler builds, CMake configuration, and upstream test execution have
not been performed for these changes; CMake and the LLVM SDKs are absent from
the local environment.
