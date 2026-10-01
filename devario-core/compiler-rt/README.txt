compiler-rt 23.1.1-2 for Devario Core

Source packaging:
https://gitlab.archlinux.org/archlinux/packaging/packages/compiler-rt
Commit: bd056b1aae566ddd9f982d5a5b9ccae93e50099c

This unversioned package supplies compiler-rt for the Clang and Rust 23.1.1
toolchain requirements. Runtime libraries install under /usr/lib/clang/23.
The separate compiler-rt21 recipe serves LLVM 21 users.

Copy the complete directory, including the libc++ i386 chrono patch and
keys/pgp public keys, to the worker. Sources retain upstream checksums and
signature verification. Import the listed public keys as the build account
after checking their fingerprints against validpgpkeys.

Build prerequisites: a working base-devel environment, LLVM 23.1.1, CMake,
Ninja, Python, and lib32-gcc-libs with its matching lib32-glibc dependency.
The recipe builds 32-bit runtimes as well as x86_64 runtimes and preserves
static libraries. Build this before Clang 23 and Rust; GCC can bootstrap it.
Shelly's isolated source-key import must have working GPG/keyboxd support.

Build efficiency in release -2:
- package() uses cmake --install instead of ninja install, avoiding a second
  traversal of the build graph and its BUILD_ALWAYS libc++ external projects.
- build() uses cmake --build and defaults CMAKE_BUILD_PARALLEL_LEVEL to nproc
  (all CPUs available to the build process), including nested CMake builds.
  An explicit nonempty worker value overrides this default.
- Test targets are explicitly disabled, matching the standalone upstream
  default and the absence of a check() hook; this alone is not a speedup.

All upstream runtime families and supported x86_64/i386 outputs remain enabled.
The libc++/libc++abi sub-builds used by libFuzzer remain required. Repeated Ninja
progress counters from those separate builds do not necessarily indicate a loop.
The full signed LLVM source archive is retained. This change reduces packaging
work; it does not make source downloads smaller. No end-to-end speedup has been
measured on the worker. If compilation is swapping, set a lower
CMAKE_BUILD_PARALLEL_LEVEL in the worker's build environment.

From the repository root:
  shelly build --review-only --json ./devario-core/compiler-rt/PKGBUILD
  shelly build --isolated ./devario-core/compiler-rt/PKGBUILD

Validation: Bash syntax, source and patch checksums, upstream source signature,
patch dry-run, Shelly review, and matching makepkg/Shelly metadata. Full
compilation and an isolated worker build have not been run. The upstream
recipe has no check() hook; --check does not add a compiler-rt test suite.
