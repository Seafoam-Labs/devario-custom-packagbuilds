# GCC and runtime split packages for Shelly

This is a custom version of
[Arch's GCC recipe](https://gitlab.archlinux.org/archlinux/packaging/packages/gcc/-/blob/main/PKGBUILD),
pinned to `16.2.1+r23+gd564253eb6c8-2`. Keep `c89`, `c99`, and both patch files
beside the PKGBUILD.

One build produces the complete 30-package compiler/runtime set, including:

| Package | Explicit provision |
| --- | --- |
| `libgcc` | `libgcc_s.so=1-64` |
| `libstdc++` | `libstdc++.so=6-64` |
| `libgomp` | `libgomp.so=1-64` |
| `libgfortran` | `libgfortran.so=5-64` |
| `libquadmath` | `libquadmath.so=0-64` |

Each of these packaging functions checks the actual library's ELF class and
SONAME before publishing its provision. Libraries are compiled from the pinned
GCC source, not copied from the worker's installed libraries. The compiler
packages retain exact-version dependencies on their matching runtime packages;
publish the complete set together, including the `gcc-libs` metapackage.

The full Arch bootstrap and language support are preserved. The isolated root
needs the declared bootstrap dependencies, including existing `gcc-ada`, `gcc-d`,
Rust, `lib32-glibc`, and `lib32-gcc-libs`; enable a repository that supplies them.
Allow substantial scratch space and build time. Arch's check step collects the
test summary without aborting on every GCC testsuite failure, so inspect that
summary before publication.

```sh
shelly build --review-only --json ./gcc/PKGBUILD
shelly build --isolated --check ./gcc/PKGBUILD
```

Shell syntax, split-package metadata, and local source checksums were checked.
Shelly review warnings refer to upstream command substitutions in `pkgver()` and
the compiler wrappers, and Makefile variable syntax inside the Ada patch. A full
GCC bootstrap has not been executed locally.

See [the dependency build guide](../DEPENDENCY-BUILDS.md) for repository setup.
See [the multilib build guide](../MULTILIB-BUILDS.md) for the new glibc,
Linux API headers, and binutils recipes and the toolchain rebuild order.
