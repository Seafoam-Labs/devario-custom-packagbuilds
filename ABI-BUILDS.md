# Explicit library ABI builds for Shelly

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

## Rust bootstrap compiler cannot load LLVM

An undefined symbol with version `LLVM_23.1` from `librustc_driver` while
running `/usr/bin/rustc -vV` means the installed bootstrap compiler cannot load
against the libraries in the build root. Adding another SONAME provision will
not repair that binary incompatibility.

The x86_64 Rust recipe now explicitly requires `rust-bootstrap=1:1.97.1`
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
[Binutils](devario-core/binutils/PKGBUILD) release `2.47-5` adds
`libsframe.so=3-64` for BPF. Both retain bare library provisions and verify the
packaged ELF64 SONAME before publishing. Rebuild and publish the providers and
refresh the worker repository; existing package metadata will not change just
by updating these recipes.

Systemd itself build-depends on libfido2 and BPF, so the systemd build root needs
an existing compatible libudev provider to bootstrap this dependency cycle.
Build binutils first to supply libsframe. Recipe syntax and generated metadata
were checked; full builds and isolated provisioning remain unverified.

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
