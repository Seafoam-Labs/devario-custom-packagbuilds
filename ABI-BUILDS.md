# Explicit library ABI builds for Shelly

## Wine bootstrap: sane requires libtiff and libxml2 ABIs

The `wine-cachyos-opt` isolated root installs `sane` as a build dependency.
Sane requires `libtiff.so=6-64` and `libxml2.so=16-64`. The published
[devario-core database](https://repo.seafoam-labs.org/devario-core/x86_64/devario-core.db)
checked on 2026-10-09 contains `libtiff` 4.7.2-1 and `libxml2` 2.15.4-1
with only bare library provisions, so neither satisfies those requirements.

| Recipe | Required release | Explicit provision |
| --- | --- | --- |
| [libtiff](devario-core/libtiff/PKGBUILD) | `4.7.2-2` | `libtiff.so=6-64`, `libtiffxx.so=6-64` |
| [libxml2](devario-core/libxml2/PKGBUILD) | `2.15.4-2` | `libxml2.so=16-64` |

The new libtiff recipe retains the sources, checksums, signed-tag verification,
and signing keys from the [official Arch recipe](https://gitlab.archlinux.org/archlinux/packaging/packages/libtiff/-/commit/9661343dd63b9f1ddad74dde22f3137183dad258).
Both recipes retain bare provisions and verify ELF64 SONAMEs before packaging.
The existing libxml2 release-2 recipe already contains its ABI fix.

Copy the complete recipe directories to Remora. With their declared dependencies
available (including ICU for libxml2), build each provider from its directory:

```sh
(cd devario-core/libtiff && shelly build --isolated --check "$PWD/PKGBUILD")
(cd devario-core/libxml2 && shelly build --isolated --check "$PWD/PKGBUILD")
```

Publish the resulting packages, including the matching `libxml2-docs` split
output, and refresh the worker's repository database. Confirm that both the
package archives' `.PKGINFO` and the refreshed database advertise the exact
provisions above. Then retry `wine-cachyos-opt` in a fresh isolated root.
Neither Wine nor sane needs a recipe change for these two missing provisions;
editing source metadata alone does not repair the published packages.

Validation: both recipes pass Bash syntax checks, makepkg/Shelly metadata
generation, and Shelly review without findings when invoked from their recipe
directories. The ABI helpers accept the matching host ELF64 libraries and
reject incorrect SONAMEs; libtiff also rejects an executable without a SONAME.
Full source builds, remote source signature/checksum verification, publication,
and isolated Wine provisioning have not been performed for this update.

## Provider overview

These x86_64 recipes provide the requested ABI dependencies. The numbers after
`.so=` describe the library's SONAME major version and ELF bitness, not the
upstream package release version. Each packaging function checks the installed
library for ELF64 and the corresponding SONAME, failing if it does not match.

| Recipe | Package version | Required provision |
| --- | --- | --- |
| [curl](curl/PKGBUILD) | `8.22.0-2` | `libcurl.so=4-64` |
| [gpgme](gpgme/PKGBUILD) | `2.2.0-2` | `libgpgme.so=45-64` |
| [libarchive](libarchive/PKGBUILD) | `3.8.9-2` | `libarchive.so=13-64` |
| [openssl](devario-core/openssl/PKGBUILD) | `3.6.4-3` | `libcrypto.so=3-64`, `libssl.so=3-64` |
| [libgit2](devario-core/libgit2/PKGBUILD) | `1:1.9.7-2` | `libgit2.so=1.9-64` |
| [libssh2](devario-core/libssh2/PKGBUILD) | `1.11.1-8` | `libssh2.so=1-64` |
| [sqlite](devario-core/sqlite/PKGBUILD) | `3.53.4-2` | `libsqlite3.so=0-64` |
| [xz](xz/PKGBUILD) | `5.8.4-2` | `liblzma.so=5-64` |
| [mpfr](mpfr/PKGBUILD) | `4.2.2-2` | `libmpfr.so=6-64` |
| [ncurses](ncurses/PKGBUILD) | `6.6-3` | `libncursesw.so=6-64` |
| [readline](readline/PKGBUILD) | `8.3.6-2` | `libreadline.so=8-64` |
| [xxhash](xxhash/PKGBUILD) | `0.8.4-2` | `libxxhash.so=0-64` |
| [zstd](zstd/PKGBUILD) | `1.5.7-6` | `libzstd.so=1-64` |

The recipes also retain the bare library provides. OpenSSL continues to provide
`libcrypto.so`, `libcrypto.so=3-64`, `libssl.so`, and `libssl.so=3-64`. Curl also builds Arch's
`libcurl-compat` and `libcurl-gnutls` split packages; `libcurl.so=4-64` is provided
by `curl` itself.

## Build

Copy entire recipe directories to the worker so local patches and configuration
files are available. Recipes keep the official Arch source checksums and signed
source verification where present. Import the appropriate upstream release keys
into the GPG keyring of the account invoking Shelly, checking the fingerprints
against `validpgpkeys` and the upstream project's published keys.

Start with a working base-devel toolchain and repositories containing the
recipes' declared dependencies. A useful build order within this set is:

1. `xz`, then `zstd`, then `openssl`.
2. `ncurses`, then `readline`.
3. `mpfr`, `xxhash`, and `gpgme`.
4. `libarchive` and `curl`.

Review and build each recipe, for example:

```sh
shelly build --review-only --json ./curl/PKGBUILD
shelly build --isolated --check ./curl/PKGBUILD
```

Publish successful builds and refresh the worker's repository database before
building their dependents. Editing `.SRCINFO` alone does not update a published
package. Check the resulting archive metadata, for example:

```sh
bsdtar -xOf /path/to/curl-8.22.0-2-x86_64.pkg.tar.zst .PKGINFO | grep '^provides = '
```

## Validation

All ten PKGBUILDs pass Bash syntax checks and generate `.SRCINFO` containing the
requested explicit ABI and bare library provisions. Every bundled patch and
configuration file matches all of its declared checksums. ABI helpers accepted
the corresponding installed host libraries and rejected incorrect SONAMEs;
these checks do not substitute for building the new packages.

Shelly review completed for every recipe. Some reviews warn about upstream
shell substitutions, computed commands, or Makefile variables in patches.
The warnings were inspected; source checksums and signatures remain enabled.
No full package builds or upstream test suites were run for this set, and remote
source checksums and signatures have not been reverified during this task.

## Rust dependency providers

For Rust's missing `libgit2.so=1.9-64`, `libsqlite3.so=0-64`,
`libssh2.so=1-64`, and `libssl.so=3-64`, build and publish these recipes in
order, refreshing the worker repository database between dependent builds:

1. `devario-core/openssl` (already had the versioned SSL provision; release 3
   also supplies the bare SSL provision and propagates ABI check failures).
2. `devario-core/libssh2` and `devario-core/sqlite`.
3. `devario-core/libgit2`.
4. Retry the Rust build after all four providers are available.

For example, from this repository's root:

```sh
shelly build --review-only --json ./devario-core/libssh2/PKGBUILD
shelly build --isolated --check ./devario-core/libssh2/PKGBUILD
```

SQLite retains the Arch split packages (`sqlite-tcl`, `sqlite-analyzer`,
`lemon`, and `sqlite-doc`); the required ABI provision belongs to `sqlite`.
Its `--soname=legacy` configuration produces `libsqlite3.so.0`. Libssh2
retains the official Arch patches and signed Git source. Its signing key is
listed in `validpgpkeys`; make it available to the build account before building.
The new recipes come from the official Arch
[libssh2](https://gitlab.archlinux.org/archlinux/packaging/packages/libssh2) and
[SQLite](https://gitlab.archlinux.org/archlinux/packaging/packages/sqlite)
packaging repositories, with their original source checksums retained.

Validation for this update: all four recipes pass Bash syntax checks and
`.SRCINFO` generation. Bundled patches and license files match their declared
checksums. ABI helpers accept the matching host ELF64 libraries and reject an
incorrect SONAME. Shelly review completes for all four; its warnings refer to
backticks in patch descriptions, a quoted Makefile variable in SQLite's sed
expression, and OpenSSL's existing `nproc` substitutions. Full package builds,
remote source verification, and upstream test suites have not been run for
this update. Build and publish the packages before expecting Rust dependency
resolution to change; recipe metadata alone does not update the repository.

## Cargo cannot load libllhttp.so.9.3

llhttp 9.4.3 installs `libllhttp.so.9.4`, replacing the 9.3 ABI. Existing
libgit2 binaries linked to `libllhttp.so.9.3` must be rebuilt; Cargo loads
libgit2 and fails before wasm-tools can run its prepare step.

The updated recipes make this dependency explicit:

- `llhttp` 9.4.3-4 provides `libllhttp.so=9.4-64` and verifies its ELF64 SONAME.
- `libgit2` 1:1.9.7-3 requires `llhttp>=9.4.3` and `libllhttp.so=9.4-64`, and
  refuses to package a library that does not link to `libllhttp.so.9.4`.

Build and publish llhttp first, refresh the worker repository database, then
build and publish libgit2. Refresh the database again and retry wasm-tools in
a fresh isolated root with the rebuilt libgit2. The recipes alone do not
replace already-published binaries. Do not symlink the old SONAME to the new
one: rebuild its consumers against the correct library.

Local validation: llhttp repackaging and its ABI metadata checks passed.
libgit2 built against staged llhttp 9.4.3 and passed all five enabled CTest
suites. The new linkage check rejects the host's old libgit2 and accepts the
rebuilt one. A cached distribution Cargo 1.96.0 starts with the rebuilt
libraries, and the dynamic loader resolves libgit2 plus llhttp 9.4 from staging.
The isolated worker and the full wasm-tools build have not been rerun.

## Rust bootstrap compiler cannot load LLVM

An undefined symbol with version `LLVM_23.1` from `librustc_driver` while
running `/usr/bin/rustc -vV` means the installed bootstrap compiler cannot load
against the libraries in the build root. Adding another SONAME provision will
not repair that binary incompatibility.

The x86_64 Rust recipe now explicitly requires `rust-bootstrap=1:1.98.0`
instead of the generic `rust` build dependency. The existing
[rust-bootstrap recipe](devario-core/rust-bootstrap/PKGBUILD) packages official
Rust binaries and conflicts with the repository `rust` package, so the isolated
root must select the bootstrap package as its compiler. Other supported
architectures retain their system Rust build dependency.

Build and publish `rust-bootstrap` first, refresh the worker repository database,
and retry Rust in a fresh isolated root:

```sh
shelly build --isolated ./devario-core/rust-bootstrap/PKGBUILD
# Publish rust-bootstrap and refresh the worker repository before continuing.
shelly build --isolated ./devario-core/rust/PKGBUILD
```

Rust checks `/usr/bin/rustc -vV` and `/usr/bin/cargo --version` before starting
bootstrap. This change addresses the failing seed compiler; the final compiler
still links to the declared system LLVM 23 libraries. A complete source build
and a runtime check of its output on the worker are still required.

### Stage1 cannot find `core` or `std`

Rust release 4 also corrects the system-stage0 patch to use bootstrap's detected
`initial_relative_libdir` when copying the seed standard libraries. Official
Rust can select `/usr/lib64/rustlib` through the system's `lib64 -> lib` symlink.
The previous patch always copied to `stage0-sysroot/lib/rustlib`, leaving the
selected `stage0-sysroot/lib64/rustlib` empty and causing E0463.

A local regression check using an official compiler reproduced E0463 with the
old copy layout and compiled a crate using `std` with the corrected layout.
The patch was checked against Rust 1.98.1 bootstrap sources. Retry with the
updated Rust recipe and patch in a clean build directory so no old bootstrap
binary or stage0 sysroot is reused. This fix does not require rebuilding
`rust-bootstrap`. A full multi-target Rust build remains unverified.

## Rust 1.99.0 dependency refresh (2026-10-07)

The Rust recipe and all seven split packages now use 1.99.0. Its x86_64
bootstrap package uses the official 1.98.0 compiler pinned in the release's
`src/stage0`; it deliberately follows that bootstrap requirement rather than
using the newest compiler. The signed bootstrap manifest and component hashes
are recorded in `devario-core/rust-bootstrap/provenance.json`.

| Recipe | Version |
| --- | --- |
| `rust` | `1:1.99.0-1` |
| `rust-bootstrap` | `1:1.98.0-1` |
| `llvm`, `clang`, `lld`, `compiler-rt`, `wasi-compiler-rt` | `23.1.3-1` |
| `aarch64-linux-gnu-gcc` | `16.2.0-1` |
| `aarch64-linux-gnu-linux-api-headers` | `7.2.9-1` |
| `wasm-tools` | `1.261.0-1` |
| `llhttp` | `9.4.3-4` |
| `libgit2` | `1:1.9.7-3` |

llhttp release 2 declares Clang as a build dependency. Its `make release`
step compiles generated C code using `CLANG ?= clang`, before the CMake build;
a base-devel-only isolated root otherwise fails with `clang: No such file or directory`.
Release 3 also runs `make -j1 release`: upstream declares `clean` and `all` as
sibling prerequisites, so parallel cleanup can delete the compiler output
directory. The subsequent CMake build retains parallelism. LTO is disabled
because the release Makefile does not pass its flags to the Clang link step.
A local full package build with `MAKEFLAGS=-j32` and
`CMAKE_BUILD_PARALLEL_LEVEL=32`, followed by a linked HTTP parser smoke test,
passed. The isolated worker build has not been rerun.

The new `devario-core/llvm` recipe supplies `llvm` and `llvm-libs`, matching
Rust's exact 23.1.3 dependencies. It retains separate LLVM component builds to
fit the existing Clang, LLD, and compiler-rt recipes. The versioned `llvm21` and
`llvm22` packages continue to serve their existing consumers.

AArch64 binutils/glibc, musl, wasi-libc, wasm-component-ld,
wasm-pkg-tools, and wit-bindgen were checked and retain their current versions.
The existing local ABI provisions, musl target selection, bootstrap libdir fix,
and compiler-rt build fixes are preserved. Rust's three LLVM 23 compatibility
patches are already incorporated upstream and have been removed; the remaining
patches were checked against 1.99.0. PGO now uses the upstream `[pgo]`
configuration table, with compiler failures still propagated immediately.

Using a working bootstrap repository, build and publish LLVM/LLVM libraries
before their consumers, and provide matching compiler-rt, Clang, LLD, and WASI
runtime packages before Rust. Update the AArch64 toolchain and WebAssembly
providers as well. Build `rust-bootstrap` before Rust, refresh the worker
repository database between dependency stages, and rebuild Rust in a fresh
isolated root. The cross-GCC/glibc and WASI libc/runtime dependency cycles still
require existing seed packages; this update does not bootstrap an empty system.

Validation results are recorded in `devario-core/rust-dependencies-validation.json`.
All 19 recipes passed Bash syntax, metadata consistency, and Shelly review;
review warnings remain for dynamic commands and existing dependency-fetch hooks.
All 11 new or changed recipes passed source checksum/signature verification.
Rust's eight patches apply to 1.99.0, and Clang/compiler-rt patches apply to
LLVM 23.1.3. Unchanged recipes did not have their remote sources reverified.
The bootstrap binary package built successfully; its Rust/Cargo/rustfmt tools,
native executable, three WebAssembly targets, and stage0 `lib64` sysroot smoke
tests passed. Full Rust, LLVM, and cross-toolchain builds remain untested.

## OSTree and Flatpak dependency providers

| Recipe | Output package | Version | Explicit ABI provisions |
| --- | --- | --- | --- |
| [Avahi](devario-core/avahi/PKGBUILD) | `avahi` | `1:0.9rc5-2` | `libavahi-client.so=3-64`, `libavahi-common.so=3-64`, `libavahi-glib.so=1-64` |
| [systemd](devario-core/systemd/PKGBUILD) | `systemd-libs` | `262-6` | `libsystemd.so=0-64`, `libudev.so=1-64` |
| [OSTree](devario-core/ostree/PKGBUILD) | `ostree` | `2026.4-2` | `libostree-1.so=1-64` |

These recipes retain the upstream Arch package layout, dependencies, patches,
source checksums, and systemd signed-tag verification. Original packaging:
[Avahi](https://gitlab.archlinux.org/archlinux/packaging/packages/avahi),
[systemd](https://gitlab.archlinux.org/archlinux/packaging/packages/systemd),
[OSTree](https://gitlab.archlinux.org/archlinux/packaging/packages/ostree).
Copy whole directories, including the systemd install script, hooks, and boot
configuration files. Each explicit ABI has an ELF64/SONAME packaging check.

Build and publish systemd (including `systemd-libs`) first, then Avahi, then
OSTree. Refresh the worker repository database between dependent stages.
The systemd recipe produces the full split set: `systemd`, `systemd-libs`,
`systemd-resolvconf`, `systemd-sysvcompat`, `systemd-tests`, and `systemd-ukify`.
The `libsystemd.so=0-64` provision belongs only to `systemd-libs`.

A working bootstrap repository must supply the declared dependencies. In
particular, systemd itself is a systemd build dependency; an existing systemd
package is needed to start. Avahi and OSTree also use systemd during building.
Systemd keeps Arch's build requirements, including multilib GCC libraries,
LLVM/Clang, BPF tooling, and kernel headers providing `/usr/src/linux/vmlinux.h`.
Make the upstream signing keys listed in `validpgpkeys` available to the build
account before building systemd.

From this repository's root, review and build each recipe, for example:

```sh
shelly build --review-only --json ./devario-core/systemd/PKGBUILD
shelly build --isolated --check ./devario-core/systemd/PKGBUILD
```

Before building OSTree, also publish the existing curl and OpenSSL recipes so
`libcurl.so=4-64` and `libcrypto.so=3-64` are available. OSTree's other declared
dependencies must resolve as well. After publishing OSTree, retry Flatpak.
Confirm the ABI provisions in the resulting archives' `.PKGINFO` and the
worker repository database; adding recipes alone does not fix provisioning.

Validation: all three PKGBUILDs pass Bash syntax checks and both makepkg and
Shelly metadata generation. All 20 local source-file checksums match their declarations; the Devario
boot configuration and splash checksums replace their upstream Arch values. ABI helpers accept the corresponding host libraries and
reject incorrect SONAMEs. Shelly reviews complete; findings concern Makefile
variables in the Avahi patch, systemd install-script substitutions and its
binary splash image, and OSTree patch text and its `curl` dependency entry.
The systemd install script and hook also pass shell syntax checks. Full builds,
upstream test suites, and remote-source checksum/signature verification have
not been run for these additions.

Systemd release 3 replaces the Arch splash with `splash-devario.bmp`, converted
losslessly from `devario-os/docs/assets/devario-fish-logo-transparent-v2.png`.
It preserves the original 1253 × 839 dimensions and RGBA pixels, including
transparency, and installs to `/usr/share/systemd/bootctl/splash-devario.bmp`.

Systemd release 5 installs the boot-entry example as `devario.conf`, titled
`Devario`, with the `linux-devario` kernel and initramfs paths used by
Devario. The bundled `loader.conf` selects `default devario.conf`. The example
still requires system-specific root partition and filesystem parameters.

### Host CPU flags reaching cross targets

Rust release 5 clears inherited global Rust/Rustdoc flags (including Cargo's
encoded and build-level environment variants), together with the C/C++ flags,
before invoking bootstrap. This prevents worker-wide `-C target-cpu=x86-64-v3`
flags from reaching ARM and WebAssembly targets; bootstrap configuration still
controls the build's optimization. Target-specific configuration is retained.
The PGO build, workload, profile merge, and final install now explicitly return
on failure so later steps do not obscure the first failing command.

The reported “not a recognized processor” lines are warnings. The original
fatal error still needs to be identified from earlier worker log lines; this
change does not establish that the full build will succeed.

## libfido2 and BPF build-root providers

Systemd release `262-6` adds `libudev.so=1-64` to `systemd-libs` for libfido2.
[Binutils](devario-core/binutils/PKGBUILD) release `2.47-7` provides
`libsframe.so=3-64` for BPF. Both retain bare library provisions and verify the
packaged ELF64 SONAME before publishing. Rebuild and publish the providers and
refresh the worker repository; existing package metadata will not change just
by updating these recipes.

Systemd release `262-7` uses `linux-devario-headers` instead of `linux-headers`
and reads its BPF type header from `/usr/src/linux-devario/vmlinux.h`. The
published `linux-devario-headers-7.2.8-1.1` archive was checked against its
repository SHA-256 on 2026-10-01 and contains that header through its
`/usr/src/linux-devario` symlink. The separate `linux-api-headers` dependency
continues to supply userspace kernel headers. This corrects kernel selection;
the worker's generic `FileConflicts` message does not identify the conflicting
paths or establish that the header package caused the provisioning failure.

Systemd itself build-depends on libfido2 and BPF. To break the libfido2/libudev
cycle, build and publish the standalone
[systemd-libs bootstrap](devario-core/systemd-libs/PKGBUILD) first. It
produces `systemd-libs-262-5.1` with both versioned ABI provisions without declaring
systemd, libfido2, PAM, or BPF as recipe dependencies. The published `262-1`
package was checked on 2026-10-01 and had only the bare library provisions.

For the reported failure while provisioning the bootstrap's own isolated root,
build this package once outside isolation on an existing compatible build host
with its build tools and dependencies installed. Shelly provisions baseline
packages independently of the recipe: its RLPM-only profile explicitly includes
systemd, while its libalpm-enabled profile installs base and base-devel. Removing
systemd from the recipe therefore does not remove it from the isolated root.
The new package's ABI provisions and file ownership fixes cannot take effect
until its archive has been built and published. Use the worker's target CPU
flags when preparing that archive.

Refresh the worker repository after publishing the bootstrap libraries. Build
binutils to supply libsframe if needed, then rebuild the full systemd split
set. Its `262-7` release replaces the temporary `262-5.1` libraries package.
The bootstrap also ships NSS modules, headers, and pkg-config files; normal
systemd daemons and documentation continue to come from the full build.

Use bootstrap release `262-5.1` or later: the original `262-5` included
`/usr/share/pkgconfig/systemd.pc` and `udev.pc`, which are owned by the main
systemd package and caused `FileConflicts` during provisioning. The corrected
bootstrap retains only the library-specific pkg-config files.

Both are independent recipes under `devario-core`; no mode switch is needed.
The bootstrap uses a SHA-256-pinned upstream source archive and builds only the
client libraries, four NSS modules, headers, and library pkg-config files. Its
build dependencies are gperf, Meson, Ninja, and Python/Jinja; journal compression
and gcrypt support remain enabled.

```sh
shelly build --review-only --json ./devario-core/systemd-libs/PKGBUILD
# Initial bootstrap on a working host; omit --isolated.
shelly build ./devario-core/systemd-libs/PKGBUILD
# Publish systemd-libs 262-5.1 and refresh the worker repository.
shelly build --isolated --check ./devario-core/systemd/PKGBUILD
```

Once provisioning succeeds with the corrected repository packages, the
standalone systemd-libs recipe can also be built in isolation. A `FileConflicts`
failure that persists after publishing the corrected archive needs the actual
conflicting paths; the generic `rlpm` subject does not identify them.

The bootstrap source archive passed its SHA-256 check. A native makepkg build
produced `systemd-libs-262-5.1-x86_64.pkg.tar.zst` with both versioned ABI
provisions. Gperf was extracted from the host package cache into `/tmp`;
`--nodeps` allowed that temporary tool without installing host packages.
The rebuilt archive has no file overlaps with `systemd-262-1`; all 31 payload
files belong to the normal systemd-libs package. All six libraries have the
expected SONAMEs and do not link to the private libsystemd-shared library.
A C consumer compiled against the packaged headers and ran with the new
libudev and libsystemd. Bash syntax, makepkg/Shelly metadata, and Shelly review
passed. The bootstrap disables the upstream test suite; full systemd builds
and isolated provisioning remain unverified.

## TPM2 provider for the Devario kernel build root

[tpm2-tss](devario-core/tpm2-tss/PKGBUILD) release `4.2.0-3` supplies the
versioned library provisions required by the existing `tpm2-tools` package:

| Library | Explicit provision |
| --- | --- |
| ESAPI | `libtss2-esys.so=0-64` |
| FAPI | `libtss2-fapi.so=1-64` |
| Marshalling | `libtss2-mu.so=0-64` |
| Return codes | `libtss2-rc.so=0-64` |
| System API | `libtss2-sys.so=1-64` |
| TCTI loader | `libtss2-tctildr.so=0-64` |
| Null TCTI | `libtss2-tcti-null.so=0-64` |

The Devario repository checked on 2026-10-01 published `tpm2-tss-4.2.0-2`
with only bare library provisions. The new recipe retains those names, adds
the exact ABI values, and verifies all seven packaged ELF64 SONAMEs before
creating an archive. The `tpm2-tools`, `devario-dracut`, `initramfs`,
`linux-devario`, and `linux-devario-headers` errors are downstream of this
missing provider metadata; they do not require duplicate recipes.

The recipe is based on [Arch packaging commit
608d3ed4aa216f1ae9e76ccde010a4ca995b05ca](https://gitlab.archlinux.org/archlinux/packaging/packages/tpm2-tss/-/commit/608d3ed4aa216f1ae9e76ccde010a4ca995b05ca).
It retains the signed upstream `4.2.0` tag, source checksums, the patch that
locks the tss system account, factory configuration, tmpfiles rules, signing
keys, and the upstream unit/integration test configuration.

The `swtpm` test dependency also requires `libseccomp.so=2-64`. Devario's
published `libseccomp-2.6.0-1` had only the bare provision when checked on
2026-10-01. The new [libseccomp recipe](devario-core/libseccomp/PKGBUILD),
release `2.6.0-2`, retains the bare name and adds the exact ABI provision,
verified against the packaged ELF64 `libseccomp.so.2` SONAME. It keeps Arch's
Python split package, signed source tag, source checksums, strict-aliasing
fix, and upstream tests from [packaging commit
95a18e64bdd767620a8d8f06ad95eb6c55e49340](https://gitlab.archlinux.org/archlinux/packaging/packages/libseccomp/-/commit/95a18e64bdd767620a8d8f06ad95eb6c55e49340).
The library's only runtime dependency is glibc, so it can be built before
the TPM packages.

Copy each entire recipe directory and import its source-signing keys as the
build account when needed. Build and publish libseccomp before running the
tpm2-tss checks, then publish tpm2-tss before retrying systemd:

```sh
shelly build --review-only --json ./devario-core/libseccomp/PKGBUILD
shelly build --isolated --check ./devario-core/libseccomp/PKGBUILD
# Publish libseccomp 2.6.0-2 and refresh the worker repository.
shelly build --review-only --json ./devario-core/tpm2-tss/PKGBUILD
shelly build --isolated --check ./devario-core/tpm2-tss/PKGBUILD
# Publish tpm2-tss 4.2.0-3 and refresh the worker repository.
shelly build --isolated --check ./devario-core/systemd/PKGBUILD
```

This recipe does not depend on `linux-devario-headers` or `tpm2-tools`. If the
worker's baseline root independently pulls in the broken dependency chain,
build this initial provider on an existing compatible host without
`--isolated`, publish it, and then retry isolation.

Libseccomp validation: source checksums and the signed tag passed verification.
Both split packages built locally with x86-64-v3 flags, and the Python binding
loaded successfully. The library archive contains `libseccomp.so=2-64` and an
ELF64 library with SONAME `libseccomp.so.2`, without a temporary build RPATH.
The regression run passed 7,933 checks and skipped 46 architecture-specific
checks. Its 40 Valgrind checks could not run on this host: supplying matching
loader debug symbols resolved the initial startup error, but Valgrind then
failed on an unsupported AVX-512 instruction in the host's glibc loader.
Packaging completed with `--nocheck` after that diagnosis; the recipe retains
the full `check()` function and requires a Valgrind-compatible environment to
validate those memory checks. Bash syntax and makepkg/Shelly metadata passed,
and Shelly review reported no findings. Isolated provisioning is unverified.

TPM2 validation: upstream source checksums and the signed tag passed verification.
A local makepkg build with x86-64-v3 flags completed, including 259 passing
upstream test programs and 12 skips, with no failures. Missing build/test tools
were extracted into `/tmp`; no host packages were installed. The socket-based
tests ran outside the restricted validation sandbox. All seven packaged
libraries have the expected ELF64 SONAMEs, the archive contains their exact
ABI provisions, and no temporary build paths remain in their RPATHs.
Bash syntax and makepkg/Shelly metadata checks passed. Shelly's three review
warnings concern backticks in the upstream patch's descriptive text. Full
isolated provisioning and the subsequent systemd build remain unverified.

## MariaDB and PostgreSQL dependency providers

| Recipe | Explicit provision |
| --- | --- |
| [liburing](devario-core/liburing/PKGBUILD) | `liburing.so=2-64` |
| [libxcrypt](devario-core/libxcrypt/PKGBUILD) | `libcrypt.so=2-64` in `libxcrypt`; ABI 1 in `libxcrypt-compat` |
| [PCRE2](devario-core/pcre2/PKGBUILD) | `libpcre2-8.so=0-64` |
| [ICU 78.3](devario-core/icu/PKGBUILD) | `libicui18n.so=78-64`, `libicuuc.so=78-64` |
| [Kerberos](devario-core/krb5/PKGBUILD) | `libgssapi_krb5.so=2-64` |
| [libxml2](devario-core/libxml2/PKGBUILD) | `libxml2.so=16-64` |
| [LZ4](devario-core/lz4/PKGBUILD) | `liblz4.so=1-64` |
| [PAM](devario-core/pam/PKGBUILD) | `libpam.so=0-64` |

The existing systemd recipe already supplies `libsystemd.so=0-64` from
`systemd-libs`. Its continued appearance in the worker error means a resolvable
built provider is still needed in that worker's repository.

The new [PostgreSQL recipe](devario-core/postgresql/PKGBUILD) produces
`postgresql`, `postgresql-libs`, and `postgresql-docs` at version 18.6, satisfying
`postgresql-libs>=18.6`. That error can also be a consequence of the existing
libraries package having unresolved Kerberos/LZ4 dependencies. The split recipe
allows rebuilding a matching server and client library set if necessary.

New recipes retain the source checksums, signatures where present, and local
patches/configuration from their corresponding
[official Arch packaging repositories](https://gitlab.archlinux.org/archlinux/packaging/packages).
Copy whole recipe directories. Import the upstream signing keys specified in
`validpgpkeys` for signed sources before building.

With declared prerequisites available, build liburing, libxcrypt, PCRE2, ICU,
LZ4, and Kerberos first; libxml2 follows ICU. PAM needs libxcrypt and
systemd-libs. PAM/systemd have a bootstrap cycle, so supply an existing compatible
package to start. Then rebuild PostgreSQL if needed. Publish each completed
provider and refresh the worker repository before retrying its consumers.
These recipes do not supply every transitive prerequisite in their dependency
arrays; those must be available from the bootstrap repository.

All nine recipes pass Bash syntax and makepkg/Shelly metadata generation.
Local source checksums match their declarations. The explicit ABI helpers were
checked against matching host libraries and rejected incorrect SONAMEs.
Shelly reports no findings for the eight library recipes; PostgreSQL findings
refer to upstream Makefile syntax in its patch and substitutions in its database
check script. Full package builds, database tests, isolated provisioning, and
remote-source verification have not been run.

## Binutils PGO coverage mismatch

Binutils release `2.47-7` disables its PGO training/use cycle while retaining
LTO, fat LTO objects, and the worker's CPU flags. The full worker log identifies
`ld/ldbuildid.c:119` (`generate_build_id`) failing with
`-Werror=coverage-mismatch`: the generated profile counters and control flow do
not match the profile-use compilation. The preceding missing-profile warnings
in gprofng were not the fatal error. The reason for the profile mismatch itself
has not been established.

A clean local build using GCC 16.2.1, `-O2 -march=x86-64-v3 -mtune=generic`,
LTO, and 12 jobs passed with PGO disabled. The earlier local PGO run lacked
DejaGNU's `runtest`, so it did not reproduce the worker's training conditions.
The recipe retains full-log capture and failure diagnostics. Use a clean build
root for the worker retry. This local build does not verify isolated worker
provisioning or replace the upstream test suite.

## Image codec providers for chafa and libheif

| Recipe | Output package | Version | Explicit ABI provisions |
| --- | --- | --- | --- |
| [aom](devario-core/aom/PKGBUILD) | `aom` | `3.15.1-2` | `libaom.so=3-64` |
| [libwebp](devario-core/libwebp/PKGBUILD) | `libwebp` | `1.6.0-3` | `libsharpyuv.so=0-64`, `libwebp.so=7-64`, `libwebpdecoder.so=3-64`, `libwebpdemux.so=2-64`, `libwebpmux.so=3-64` |
| [x264](devario-core/x264/PKGBUILD) | `x264` | `3:0.165.r3222.b35605a-3` | `libx264.so=165-64` |
| [x265](devario-core/x265/PKGBUILD) | `x265` | `4.3-2` | `libx265.so=217-64` |

Harfbuzz build-depends on `chafa`, which requires `libheif`, whose Arch metadata
requires all eight provisions above. The published copies of these four packages
carried only bare `.so` provisions, so the harfbuzz isolated root failed with
`UnsatisfiedDependencies` before compiling anything. Resolution takes the
provisions of the same-named package from the highest priority repository, which
hid Arch's versioned values; `libopenh264.so=8-64` and `libde265` resolved
because no repository package of those names exists. Other repository packages
with the same gap will fail the same way for any Arch dependent that names a
versioned provision, so a `PROVIDES` diff against Arch's databases is the check
that finds them.

The recipes come from the official Arch packaging repositories for
[aom](https://gitlab.archlinux.org/archlinux/packaging/packages/aom),
[libwebp](https://gitlab.archlinux.org/archlinux/packaging/packages/libwebp),
[x264](https://gitlab.archlinux.org/archlinux/packaging/packages/x264), and
[x265](https://gitlab.archlinux.org/archlinux/packaging/packages/x265), keeping
their patches, checksums, split packages, `validpgpkeys`, and x264's
commit-pinned Git source. Import the two signing keys as the build account after
checking the fingerprints in `validpgpkeys`:
`B002F08B74A148DAA01F7123A48E86DB0B830498` (AOMedia) and
`6B0E6B70976DE303EDF2F601F9C3D6BDB8232B5D` (WebP).

None of the four depends on the others, so build them in any order, publish all
four, refresh the worker repository, and only then retry harfbuzz:

```sh
for r in aom libwebp x264 x265; do
  shelly build --review-only --json ./devario-core/$r/PKGBUILD
  shelly build --isolated --check ./devario-core/$r/PKGBUILD
done
```

Confirm each archive's `.PKGINFO` carries the versioned provisions before
publishing, then check the refreshed repository database. `aom-docs` and
`libwebp-utils` are already published, so the four recipes produce six
replacement archives.

Validation: all four pass Bash syntax checks, generate `.SRCINFO` carrying both
bare and versioned provisions, and complete Shelly review. The only findings are
two warnings about the `$(nproc)` substitution in libwebp's upstream `check()`.
Both bundled patches match their declared upstream checksums, and both exported
keys match the fingerprints in `validpgpkeys`. Every ABI helper accepts the
matching host library and rejects a wrong SONAME. A libalpm transaction for
`chafa` against a copy of the repository database carrying these provisions
resolves, with all four satisfied by the repository copies rather than Arch's.
Full package builds, isolated provisioning, and the harfbuzz retry have not been
run.

## Fish check dependencies: tmux and wget

Fish's isolated build root includes tmux and wget for the upstream test suite.
Their versioned shared-library requirements are supplied by these recipes:

| Recipe | Output package | Version | Required provision |
| --- | --- | --- | --- |
| [libevent](devario-core/libevent/PKGBUILD) | `libevent` | `2.1.13-4` | `libevent_core-2.1.so=7-64` |
| [libidn2](devario-core/libidn2/PKGBUILD) | `libidn2` | `2.3.8-2` | `libidn2.so=0-64` |
| [util-linux](devario-core/util-linux/PKGBUILD) | `util-linux-libs` | `2.42.4-3` | `libuuid.so=1-64` |
| [libpsl](devario-core/libpsl/PKGBUILD) | `libpsl` | `0.21.5-3` | `libpsl.so=5-64` |
| [nettle](devario-core/nettle/PKGBUILD) | `nettle` | `4.0-2` | `libnettle.so=9-64` |

Libevent and util-linux retain their existing package splits and gain explicit
ABI provisions. Libidn2, libpsl, and nettle are new recipes adapted from the
official Arch packaging repositories, retaining their signed release sources,
checksums, and bundled upstream public keys. Nettle also explicitly provides
`libhogweed.so=7-64`. All five retain their bare library provisions and check
the staged ELF64 library's SONAME before packaging can succeed.

Build and publish libidn2 before libpsl. Libevent, util-linux, and nettle can be
built independently using their declared prerequisites. Publish matching split
outputs together, including `util-linux-libs` from util-linux and `libevent-docs`
from libevent. Copy complete recipe directories, including `keys/pgp` and local
support files, to the worker.

Refresh the worker's repository database after publishing these packages, then
retry `devario-core/fish`. Updating PKGBUILDs or `.SRCINFO` alone cannot repair
an existing repository archive's metadata. Confirm the corresponding
`provides =` lines in each new archive's `.PKGINFO` before publishing.

Validation: all five recipes pass Bash syntax checks, and both makepkg and
Shelly metadata contain the requested versioned provisions on the correct
output packages. ABI helpers accept matching host libraries and reject wrong
SONAMEs and executables without SONAMEs. Checksums and release signatures for
all three new sources verify. Nettle's signature verifies with the pinned key,
although GPG warns that the release key has since expired. Signature verification
remains enabled. Shelly review reports no findings for the new
recipes or util-linux; libevent retains the known false positives for backticks
inside a C comment in its existing patch. Full compilation, isolated-root
provisioning, and repository publication have not been performed for this set.

## OpenJDK font and image library providers

The staged libraries have the correct ELF64 SONAMEs, but their old package
metadata supplies only unversioned library names. These recipes retain those
names and add the exact provisions required by `jdk-openjdk`:

| Recipe | New version | Required provision |
| --- | --- | --- |
| [freetype2](devario-core/freetype2/PKGBUILD) | `2.14.3-2` | `libfreetype.so=6-64` |
| [harfbuzz](devario-core/harfbuzz/PKGBUILD) | `14.5.1-2` | `libharfbuzz.so=0-64` |
| [libjpeg-turbo](devario-core/libjpeg-turbo/PKGBUILD) | `3.2.0-3` | `libjpeg.so=8-64` |
| [lcms2](devario-core/lcms2/PKGBUILD) | `2.19.1-2` | `liblcms2.so=2-64` |

HarfBuzz also adds `=0-64` to its existing subset, GObject, raster, vector,
Cairo, and ICU library provisions; libjpeg-turbo adds `libturbojpeg.so=0-64`.
The Cairo and ICU provisions belong to their corresponding split packages.
Each explicit provision has a packaging check for ELF64 and the expected
SONAME, with a mismatch stopping packaging.

The recipes use the official Arch packaging tags matching the staged releases:
[FreeType 2.14.3-1](https://gitlab.archlinux.org/archlinux/packaging/packages/freetype2/-/tree/2.14.3-1),
[HarfBuzz 14.5.1-1](https://gitlab.archlinux.org/archlinux/packaging/packages/harfbuzz/-/tree/14.5.1-1),
[libjpeg-turbo 3.2.0-2](https://gitlab.archlinux.org/archlinux/packaging/packages/libjpeg-turbo/-/tree/3.2.0-2),
and [Little CMS 2.19.1-1](https://gitlab.archlinux.org/archlinux/packaging/packages/lcms2/-/tree/2.19.1-1).
Each PKGBUILD records the upstream packaging commit. Source checksums,
signature verification where present, patches, licenses, signing keys, and
split packages are retained. Copy the complete recipe directories to Remora.

Build libjpeg-turbo before lcms2. FreeType and HarfBuzz have mutual build
dependencies; use the existing compatible packages to bootstrap their rebuilds.
HarfBuzz's chafa dependency also needs the codec providers described above.
Publish matching split outputs together, refresh the worker's repository
database, and retry the OpenJDK consumer only after these providers are
available. Editing recipes or `.SRCINFO` does not update published archives.

Validation: all four recipes pass Bash syntax checks and makepkg/Shelly metadata
generation with the expected bare and versioned provisions. All four bundled
source-file checksums and six signing-key fingerprints match their declarations.
All 11 ABI checks accept the staged libraries and reject incorrect SONAMEs and
an executable without a SONAME. Shelly review reports no findings for HarfBuzz
or lcms2; FreeType warnings concern backticks in an upstream patch comment, and
libjpeg-turbo's warning concerns its existing `$(nproc)` substitution.
Full builds, upstream tests, and isolated provisioning have not been run for
this update. Remote source verification is recorded below for FreeType only.

### FreeType source download TLS failure

The FreeType recipe now uses the project's official SourceForge mirror for all
three release archives and their detached signatures. This avoids the worker's
failing `download-mirror.savannah.gnu.org` endpoint. The alternate location is
listed on [FreeType's download page](https://freetype.org/download.html).
All three archives downloaded over verified HTTPS, matched the recipe's
original BLAKE2 checksums, and passed signature verification with the bundled
Werner Lemberg key. The source filenames, checksums, signing key, ABI provisions,
and package release remain unchanged; `.SRCINFO` contains the new URLs.

The original Savannah URL also works from the development host, so the worker's
underlying TLS failure has not been reproduced or diagnosed. Copy the updated
recipe to Remora and retry. If verified HTTPS downloads fail at SourceForge as
well, investigate the build root's clock, CA trust store, and TLS backend.
Certificate and signature verification remain enabled. The remote worker retry
has not been performed here.
