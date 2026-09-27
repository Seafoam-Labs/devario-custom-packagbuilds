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
| [openssl](openssl/PKGBUILD) | `3.6.4-2` | `libcrypto.so=3-64` |
| [xz](xz/PKGBUILD) | `5.8.4-2` | `liblzma.so=5-64` |
| [mpfr](mpfr/PKGBUILD) | `4.2.2-2` | `libmpfr.so=6-64` |
| [ncurses](ncurses/PKGBUILD) | `6.6-3` | `libncursesw.so=6-64` |
| [readline](readline/PKGBUILD) | `8.3.6-2` | `libreadline.so=8-64` |
| [xxhash](xxhash/PKGBUILD) | `0.8.4-2` | `libxxhash.so=0-64` |
| [zstd](zstd/PKGBUILD) | `1.5.7-6` | `libzstd.so=1-64` |

The recipes also retain the bare library provides. OpenSSL continues to provide
`libcrypto.so`, `libcrypto.so=3-64`, and `libssl.so=3-64`. Curl also builds Arch's
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
