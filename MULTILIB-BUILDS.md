# Multilib build dependencies

## Missing 32-bit audio, Brotli, and ICU ABI providers

The isolated-root errors for ALSA plugins, curl, libxml2, and PipeWire identify
four missing versioned provisions. Failures for libelf, Wayland, LLVM, Mesa,
libglvnd, and libva cascade through those dependencies; retry resolution after
publishing these providers before changing the dependent recipes.

| Recipe | Rebuild release | Provision required by the reported failure |
| --- | --- | --- |
| [lib32-alsa-lib](devario-libs/lib32-alsa-lib/PKGBUILD) | `1.2.16.1-2` | `libasound.so=2-32` |
| [lib32-brotli](devario-libs/lib32-brotli/PKGBUILD) | `1.2.0-3` | `libbrotlidec.so=1-32` |
| [lib32-icu](devario-libs/lib32-icu/PKGBUILD) | `78.3-2` | `libicuuc.so=78-32` |
| [lib32-opus](devario-libs/lib32-opus/PKGBUILD) | `1.6.1-2` | `libopus.so=0-32` |

All four recipes retain bare library provisions and now explicitly advertise
their versioned 32-bit ABIs. This includes ALSA topology, Brotli common/encoder,
and the other ICU libraries already listed in their provides arrays. Packaging
checks every advertised library for ELF32 and the expected SONAME, returning
failure for an incorrect architecture or ABI. Source versions, checksums,
patches, and signature verification remain unchanged.

With a working multilib toolchain and each recipe's declared dependencies
available, these four providers can be built independently. In particular,
`lib32-alsa-lib` requires native `alsa-lib=1.2.16.1`. Copy the complete recipe
directories, including bundled patches and signing keys, to the worker. For
each recipe, run from its directory, for example:

```sh
cd devario-libs/lib32-alsa-lib
shelly build --review-only --json "$PWD/PKGBUILD"
shelly build --isolated --check "$PWD/PKGBUILD"
```

Publish all four rebuilt packages and refresh the worker repository database
before retrying the original package in a fresh isolated root. Verify that the
archives' `.PKGINFO` and the refreshed database contain the exact provisions
listed above. Editing PKGBUILDs or `.SRCINFO` alone does not update published
packages. Existing consumers do not need rebuilding solely for this metadata
repair when their required SONAMEs match.

Validation: all four recipes pass Bash syntax checks and makepkg/Shelly metadata
generation with the expected bare and versioned provisions. All 12 ABI checks
accept matching host ELF32 libraries and reject wrong SONAMEs, matching native
ELF64 libraries, and an executable without a SONAME. Both bundled ICU patches
match their declared SHA-512 checksums. Shelly reviews complete; Brotli's only
finding concerns its existing `$(nproc)` test parallelism, which was inspected
before generating metadata with `--reviewed`. Full source builds, remote source
verification, publication, and isolated provisioning remain unverified.

## Multilib toolchain for compiler-rt21

`compiler-rt21` intentionally builds i386 runtimes, including RTSanitizerCommon.
Its isolated root needs working 32-bit headers, startup objects, libraries,
linker support, and a compiler that can use them.

| Recipe | Version | Packages needed here |
| --- | --- | --- |
| [linux-api-headers](linux-api-headers/PKGBUILD) | `7.2-1` | Linux userspace API headers |
| [glibc](glibc/PKGBUILD) | `2.44+r50+g1848099f063e-1` | `glibc`, `lib32-glibc`; also produces `glibc-locales` |
| [binutils](binutils/PKGBUILD) | `2.47-4` | assembler, linker and binary utilities |
| [gcc](gcc/PKGBUILD) (existing) | `16.2.1+r23+gd564253eb6c8-2` | `gcc`, `lib32-gcc-libs` and the native runtime packages |

`lib32-gcc-libs` is already an output of the GCC split recipe. Build that recipe
as a whole: `package_gcc()` stages files used by the other packaging functions.
There is no separate `gcc-multilib` or `lib32-gcc-libs` recipe to build.
Likewise, build `glibc/PKGBUILD` to produce both libc variants from one source.
The lib32 package requires the matching glibc version; publish and install them
together. The new libc recipe is newer than the initially inspected host libc,
so do not install its lib32 output alongside the older native libc.

## Bootstrap and build order

These recipes rebuild an existing toolchain; they are not a bootstrap from an
empty root. Seed the worker's repositories with a coherent base-devel toolchain,
`glibc`, `lib32-glibc`, and `lib32-gcc-libs`, plus each recipe's declared build
dependencies. GCC also needs its existing Ada and D frontends and Rust.
Installing these packages only on the host does not populate an isolated root.

The upstream toolchain rebuild order is:

1. `linux-api-headers`
2. `glibc` (native and lib32 outputs)
3. `binutils`
4. `gcc` (including `lib32-gcc-libs`)
5. Rebuild `glibc`, then `binutils`, then `gcc` using the new toolchain.
6. Build `compiler-rt21` with the resulting packages available in its root.

Copy each entire recipe directory, including patches, hooks, and `keys/`.
For example, from the repository root:

```sh
shelly build --review-only --json ./glibc/PKGBUILD
shelly build --isolated --check ./glibc/PKGBUILD
```

Publish the outputs and refresh the worker's repository database between stages.
Use the supplied signing keys, checking their fingerprints against each recipe's
`validpgpkeys`, where source signature verification applies. The glibc and
binutils sources use pinned Git commits and checksums; Linux uses a checksummed
tarball and detached signature.

## Verify the actual compiler-rt root

Copy and run this probe **inside the isolated root**, before starting the build:

```sh
bash check-multilib.sh
# If the build selects Clang, test those exact compiler executables too:
bash check-multilib.sh clang clang++
```

The script lives at [compiler-rt21/check-multilib.sh](compiler-rt21/check-multilib.sh).
It compiles and links 32-bit C and C++ programs, verifies ELF32, then exercises
pthreads, C++ exceptions, and the dynamic loader. A failure means the root's
toolchain is still incomplete or inconsistent. Passing is a prerequisite, not
a guarantee that every compiler-rt target will build.

## Validation performed

All three new recipes pass Bash syntax checks and generate `.SRCINFO`. All 17
bundled source files and patches match their upstream checksums. The multilib
probe passes with the installed host GCC toolchain outside the execution sandbox
(the sandbox blocks 32-bit execution with SIGSYS). Full toolchain rebuilds,
upstream test suites, remote source checksum/signature verification, and an
isolated compiler-rt build have not been run. Binutils' upstream `check()`
collects failures without failing the build; inspect its test results before
publishing.
