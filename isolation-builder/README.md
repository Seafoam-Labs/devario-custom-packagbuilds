# Isolation builder bootstrap packages

All 31 originally requested package names were absent from the live `devario-core`
package list when checked on 2026-09-29. The original 17 package-base directories
cover them; `dwz` and `help2man` bring the total to 19 directories and supply
additional build dependencies for debugedit.
The repository query was:
<https://repo.seafoam-labs.org/api/v1/packages?repository=devario-core>.

Each directory contains a PKGBUILD, generated `.SRCINFO`, and its required local
patches, scripts, hooks, and upstream signing keys where supplied. Copy the whole
directory to the build worker. `sources.json` records the Arch packaging commits
used as a base and the upstream release for the custom dwz recipe; GCC is a
standalone copy of this repository's existing custom GCC recipe,
including its explicit ABI provisions and SONAME checks.

## Package mapping

| Build directory | Requested outputs |
| --- | --- |
| [autoconf](autoconf/PKGBUILD) | `autoconf` |
| [automake](automake/PKGBUILD) | `automake` |
| [bison](bison/PKGBUILD) | `bison` |
| [boost](boost/PKGBUILD) | `boost-libs` |
| [cpio](cpio/PKGBUILD) | `cpio` |
| [debugedit](debugedit/PKGBUILD) | `debugedit` |
| [dwz](dwz/PKGBUILD) | `dwz` |
| [fakeroot](fakeroot/PKGBUILD) | `fakeroot` |
| [flex](flex/PKGBUILD) | `flex` |
| [gcc](gcc/PKGBUILD) | `gcc`, `gcc-libs`, `libasan`, `libatomic`, `libgcc`, `libgfortran`, `libgomp`, `libhwasan`, `liblsan`, `libobjc`, `libquadmath`, `libstdc++`, `libtsan`, `libubsan` |
| [gdb](gdb/PKGBUILD) | `gdb`, `gdb-common` |
| [gettext](gettext/PKGBUILD) | `gettext` |
| [help2man](help2man/PKGBUILD) | `help2man` |
| [libtool](libtool/PKGBUILD) | `libtool` |
| [m4](m4/PKGBUILD) | `m4` |
| [pkgconf](pkgconf/PKGBUILD) | `pkgconf` |
| [source-highlight](source-highlight/PKGBUILD) | `source-highlight` |
| [texinfo](texinfo/PKGBUILD) | `texinfo` |
| [which](which/PKGBUILD) | `which` |

Split packages share a build: do not build each GCC runtime separately. The GCC
recipe also produces the other compiler frontends and runtime packages listed in
its `.SRCINFO`. Boost additionally produces `boost` headers, needed to build
source-highlight and GDB. Libtool additionally produces `lib32-libltdl`. Upstream
split builds are preserved so their outputs stay consistent.

## Building

These are normal distribution recipes, not a toolchain bootstrap from an empty
root. Start in an existing compatible build environment or use a seed repository
that supplies the missing bootstrap tools. An isolated build cannot install its
own missing prerequisites before those packages have been built and published.
The requested list is not the complete transitive build dependency closure.

GCC retains the full language and multilib build, requiring existing `gcc-ada`,
`gcc-d`, Rust, `lib32-glibc`, and `lib32-gcc-libs`, among its declared dependencies.
Libtool also needs the multilib toolchain. Pkgconf requires Meson and its Ninja
backend. Test dependencies are additional when checks are enabled. See each
`.SRCINFO` for the complete declared dependencies of that recipe.

Useful ordering constraints once the seed environment is available:

- Build and publish GCC with its matching runtimes together; rebuild libtool
  after changing GCC.
- Build Boost before source-highlight, then GDB (with gdb-common), then debugedit.
- Build cpio, dwz, and help2man before debugedit.
- Help2man requires `perl-locale-gettext` and its dependencies in the build root.
  Build and publish help2man before m4, flex, and libtool.
- Build m4 before autoconf, and autoconf before automake. Some source preparation
  uses existing autotools/gettext, so this ordering does not remove seed needs.

Import the supplied signing keys into the build account's GnuPG keyring after
checking their fingerprints against `validpgpkeys` in the corresponding recipe.
Keep the upstream source checksum and signature verification enabled.

From the repository root, for example:

```sh
shelly build --review-only --json ./isolation-builder/m4/PKGBUILD
shelly build --isolated --check ./isolation-builder/m4/PKGBUILD
```

Publish the resulting packages and refresh the repository database before using
them to satisfy dependencies of subsequent isolated builds.

For the libfido2/libudev bootstrap cycle, use the standalone
[systemd-libs recipe](../devario-core/systemd-libs/PKGBUILD) under `devario-core`.
If its own isolated root cannot be provisioned, build it once on a working host
without `--isolated`, publish the package, and refresh the worker repository.
Then build the full [systemd recipe](../devario-core/systemd/PKGBUILD) in isolation. See the
[ABI build guide](../ABI-BUILDS.md#libfido2-and-bpf-build-root-providers) for build
order and validation.

## Validation

The original 17-directory import was validated as follows:

- All 17 PKGBUILDs pass `bash -n` and `makepkg --printsrcinfo`.
- Generated metadata covers all 31 requested names.
- All 14 local `source` files exist and match their declared checksums.
- Shelly review completed for all 17 recipes. Fourteen have no findings; Boost,
  Flex, and GCC have static-review warnings about command substitutions and
  patch text. The recipes retain those upstream constructs.
- Full source downloads, compilation, test suites, and isolated builds have not
  been run. This is recipe validation, not a claim of successful package builds.

For the added dwz and help2man recipes:

- Source archives match their SHA-512 checksums and verify against the supplied
  upstream signing keys.
- Bash syntax, generated `.SRCINFO`, and Shelly static review pass.
- Both `build()` and `package()` functions completed locally, installing into
  temporary staging directories. Help2man's Perl gettext dependency was built
  separately under `/tmp` for this check. That temporary module passed its load
  and binding tests, but its three translation tests failed locally; translated
  output is not validated by this check.
- The staged help2man executable successfully generated a man page from the
  staged dwz executable.
- Isolated builds and the dwz upstream test suite have not been run.
