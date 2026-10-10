# Missing dependency builds for Shelly

Build and publish `devario-installer/devario-base` 3-15 before the next ISO
rebuild to include `devario-productivity` and `devario-libs` in `/etc/shelly.conf`.
The default configuration no longer includes `devario-scx`.

Build and publish `devario-core/netcat` 1.238_1-1 before the next ISO rebuild.
It packages Debian's OpenBSD netcat port as `netcat`, provides `openbsd-netcat`,
and installs `nc`, `netcat`, and `nc.openbsd`. The recipe applies the upstream
Linux patches, includes both BSD licenses and runs the upstream client/server
checks. Devario's ISO and repository package lists now also include `ripgrep`.

Build and publish `devario-core/power-profiles-daemon` 0.30-1 before the next
Devario ISO rebuild. The recipe uses the checksum-pinned upstream release,
includes D-Bus activation and polkit policy, and runs upstream tests through
Meson. The ISO now requests this package and starts it alongside UPower in
live and installed sessions so Pearl can show battery status and power profiles.

For the current core-only ISO, upload the complete recipe directories below.
These releases move system hooks and their helpers to `/usr/share/rlpm/`,
public key bundles to `/usr/share/shelly/keyrings/`, and mutable state and
configuration to Shelly paths. They require the patched Shelly CLI/key tools
built with `-Dpath-profile=devario` and support for `HookDirMode = Replace`.

| Rebuild recipe | Release | Location |
| --- | --- | --- |
| glibc | 2.44+r50+g1848099f063e-2 | `devario-core/glibc` |
| glib2 | 2.90.0-2 | `devario-core/glib2` |
| dbus | 1.16.2-3 | `devario-core/dbus` |
| systemd | 262-8 | `devario-core/systemd` |
| devario-dracut | 112-5 | `devario-core/devario-dracut` |
| devario-keyring | 20260923-2 | `devario-installer/devario-keyring` |
| devario-boot | 1-7 | `devario-installer/devario-boot` |
| devario-base | 3-12 | `devario-installer/devario-base` |

`devario-boot` 1-7 replaces installed Limine with systemd-boot. Build and
publish it before `devario-base` 3-12, which requires that release. Installation
now requires 64-bit UEFI and a FAT EFI System Partition at `/boot`. The live ISO
retains its BIOS Syslinux support, so `syslinux` remains in the rebuild list.
The boot recipe retains the legacy hook mask and migrates an existing Devario
Limine marker only after successful UEFI deployment.

`devario-base` 3-12 also requires Fish and `shadow>=4.20.0.arch1-3`.
Build and publish `devario-core/fish` 4.9.3-1 and `devario-core/shadow`
4.20.0.arch1-3 before base and ISO assembly. The Shadow release sets
`useradd`'s default shell to `/usr/bin/fish`; the ISO profile applies the
same default to the live user and Calamares-created accounts.

A subsequent audit of the complete signed repository file inventory found
17 additional recipe bases. Their recipes and supporting files are now in
`devario-core`, imported from the upstream packaging tags matching the published
versions. Each PKGBUILD records its upstream packaging commit. Hook/helper
installation paths, hook commands, and install-script references now use
`/usr/share/rlpm/`; package releases and bundled-source checksums are updated.

| Additional rebuild recipe | New version | Location |
| --- | --- | --- |
| accountsservice | 26.27.3-2 | [recipe](devario-core/accountsservice/PKGBUILD) |
| appstream | 1.2.1-2 | [recipe](devario-core/appstream/PKGBUILD) |
| ca-certificates | 20240618-2 | [recipe](devario-core/ca-certificates/PKGBUILD) |
| dconf | 51.0-2 | [recipe](devario-core/dconf/PKGBUILD) |
| desktop-file-utils | 0.28-2 | [recipe](devario-core/desktop-file-utils/PKGBUILD) |
| dkms | 3.4.3-3 | [recipe](devario-core/dkms/PKGBUILD) |
| fontconfig | 2:2.18.3-3 | [recipe](devario-core/fontconfig/PKGBUILD) |
| gdk-pixbuf2 | 2.44.8-2 | [recipe](devario-core/gdk-pixbuf2/PKGBUILD) |
| gtk3 | 1:3.24.52-3 | [recipe](devario-core/gtk3/PKGBUILD) |
| gtk4 | 1:4.24.1-2 | [recipe](devario-core/gtk4/PKGBUILD) |
| gvfs | 1.62.0-4 | [recipe](devario-core/gvfs/PKGBUILD) |
| kmod | 34.2-2 | [recipe](devario-core/kmod/PKGBUILD) |
| man-db | 2.13.1-4 | [recipe](devario-core/man-db/PKGBUILD) |
| openssh | 10.5p1-2 | [recipe](devario-core/openssh/PKGBUILD) |
| perl | 5.42.3-2 | [recipe](devario-core/perl/PKGBUILD) |
| shared-mime-info | 2.5.1-3 | [recipe](devario-core/shared-mime-info/PKGBUILD) |
| syslinux | 6.04.pre3.r3.g05ac953c-6 | [recipe](devario-core/syslinux/PKGBUILD) |

Publish all matching split outputs together, including `ca-certificates-utils`
from `ca-certificates` and `gtk-update-icon-cache` from `gtk4`. Keep each complete
recipe directory, including any `keys/pgp` public keys, when uploading to Remora.
Perl's old-module hook now reads `/var/lib/shelly/local` directly for package
ownership; it no longer requires the legacy package-manager command. DKMS's
hook debugging variable is now `DKMS_RLPM_HOOK_DEBUG`.
The imported install scripts also avoid the unavailable `vercmp` executable:
CA certificate migration checks the old directory directly, fresh dconf and
fontconfig installs retain their initialization, and obsolete pre-Devario
upgrade notices/migrations are removed.

Validation for these 17 recipes: metadata generation and Shelly review completed,
32 shell files passed syntax checks, and all 81 checksums for 70 bundled source
files matched. Four Perl hook fixture tests passed. Shelly's static review still
reports dynamic-command warnings in upstream helper scripts and patch text.
Full isolated compilation and publication have not been performed.

The published `systemd` and `devario-dracut` archives also still use old paths;
the local recipes above already include their fixes. Rebuilding devario-dracut
also restores its `initramfs` provision, avoiding the old `dracut-git` provider.

The published Shelly CLI at `832de83c` supports explicit configuration but still
uses the old public key directory. Build upstream revision
`1913c78d272f6b8c53531d02181f024b78708d2b` or newer with the Devario profile.

Build each split recipe once and publish its matching outputs together;
`glibc` includes `lib32-glibc`. Build boot after dracut, and base after boot
and keyring. Keep using the existing published bootstrap dependencies for
cycles among glib2, D-Bus, and systemd.

The ISO workflow now prepares an isolated Python validation environment from
hash-pinned upstream wheels. The 15 Python recipes from the previous work are
optional and are no longer required for the ISO or Remora build list.
Publish `nbd` 3.27.1-4 to `devario-core` if still missing; its existing recipe
needs no additional path changes. The original local list is the eight rebuild targets above plus `nbd`; the
additional recipes listed above must also be rebuilt and published before ISO construction.
The ISO uses the published `devario-desktop` and stable `pearl-greeter`;
`devario-aqueous-desktop` and `seafoam-keyring` are not default ISO requirements.

Validation for the eight path updates: Bash syntax, regenerated makepkg
metadata, and 68 bundled-source checksums passed. Staged package functions
for base, boot, and keyring produced the expected paths and boot hook masks.
The OS repository's three matching recipes are synchronized. Full compilation,
isolated Remora builds, and publication of these releases remain to be done.
The ISO builder and verification script path migration is now implemented.
Repository publication remains separate from these local source changes.

For Zig 0.16 and its LLVM 21, CMake, GCC, and Python prerequisites, see
[the Zig build guide](ZIG-BUILDS.md).

Devario is an independent operating system. These x86_64 recipes are adapted
from the corresponding
[Arch Linux packaging repositories](https://gitlab.archlinux.org/archlinux/packaging/packages).
Those links record recipe provenance.
Each directory includes its PKGBUILD, generated `.SRCINFO`, and required local
source files. Copy whole directories to the Remora worker.

## Remaining ISO runtime and OS-owned recipes

General runtime recipes are available under `devario-core/`:

| Directory | Version | Build/publish order |
| --- | --- | --- |
| `composefs` | 1.0.8-1 | Before provisioning ostree/Flatpak consumers |
| `ding-libs` | 0.7.0-1 | Before GSSProxy; an additional missing runtime dependency |
| `gssproxy` | 0.9.2-4 | After ding-libs; before NFS consumers |
| `rpcbind` | 1.3.1-3 | Before NFS consumers |
| `libmalcontent` | 0.14.0-5 | Before Flatpak; library-only bootstrap avoids the Flatpak UI cycle |
| `xdg-dbus-proxy` | 0.1.9-2 | Before Flatpak; declares D-Bus for its tests |
| `inter-font` | 4.1-1 | Existing recipe; publish before Calamares |

OS-owned live USB and installer recipes are in
[`devario-installer/`](devario-installer/README.md):

| Directory | Version | Build/publish order |
| --- | --- | --- |
| `devario-filesystem` | 1-1 | Before OS metapackages |
| `devario-keyring` | 20260923-2 | Before OS metapackages |
| `seafoam-keyring` | 20260923-1 | Before OS metapackages |
| `devario-boot` | 1-7 | Before devario-base; requires published devario-dracut |
| `devario-base` | 3-12 | After filesystem, boot, devario-keyring, Fish, and Shadow |
| `devario-aqueous-desktop` | 1-8 | Requires the five published Aqueous 1.0.0-1 components |
| `ckbcomp` | 1.248-1 | Before Calamares |
| `calamares` | 3.4.2-6 | After ckbcomp and Inter; explicitly declares CMake |

The eight OS-owned directories in `devario-installer/` are self-contained copies from `devario-os`
commit `63f329223e0851a5f05519b849bb250d560833e2`. All referenced hooks,
configuration, patches, desktop files, and public key material are included.
The desktop recipe's Aqueous pins and Calamares's explicit CMake dependency
are updated in this package repository. The base, boot, and keyring recipes are synchronized with the OS checkout
for this path migration; future edits do not automatically synchronize. Exact provenance is in
[iso-packages-upstream.json](devario-core/iso-packages-upstream.json).

These copies are an alternative worker build route. The OS repository's
`scripts/build-packages.sh` and `scripts/build-packages-nspawn.sh` can also build
the OS-owned packages from their own recipes. The ISO assembler consumes
completed signed packages in the staged `devario-core` closure; it does not
compile PKGBUILDs. Public repository publication is not required for a local
ISO, but the staged repository must contain the required artifacts, dependencies,
and matching signed metadata.
The `devario-installer/` source folder does not change that binary repository name.

Review and build each complete recipe directory, publishing and refreshing
the worker repository between prerequisite stages:

```sh
gpg --import devario-core/ding-libs/keys/pgp/*.asc
shelly build --review-only --json ./devario-core/ding-libs/PKGBUILD
shelly build --isolated --check ./devario-core/ding-libs/PKGBUILD
```

GSSProxy still declares the missing build dependency `po4a` for translated
documentation. Ding-libs declares missing test dependency `check`; its configure
script otherwise omits some tests. These were absent from the inspected signed
2026-10-02 databases and are not runtime dependencies of the ISO.

Validation: all sources pass their declared checksums, including the signed
ding-libs release. Local makepkg builds succeeded for all listed recipes except
Calamares, whose source verification and both patches passed preparation.
Composefs's six Meson tests and the D-Bus proxy suite passed outside the sandbox,
where temporary directories and local sockets are available. Ding-libs passed
14 tests without its optional Check-based coverage. GSSProxy's upstream
`test_proxymech` target built; its local build lacked po4a translations.
Libmalcontent built using temporary GLib development tools and its GIR typelib
loaded successfully; the library-only bootstrap deliberately omits upstream
documentation and test targets. Full isolated worker builds and an ISO install
remain unverified.

Shelly review findings in the imported OS sources were inspected: runtime boot,
GPU, and migration scripts contain command substitutions; `devario-report.sh`
uses sudo when invoked to collect system logs. Packaging installs these files
without executing them. The keyring findings identify binary public-key data:
both bundles match the OS source and contain no secret-key packets. GSSProxy's
remaining warning is backtick notation in an upstream patch description.

After including these recipes, the metadata audit selects 637 packages with
zero missing runtime requirements against the inspected signed databases.
This is a dependency-name/version check, not proof of conflict-free installation
or ISO readiness. The Shelly assembler integration and builder provisioning
issues from the readiness audit still require separate work.

## ISO runtime packages added on 2026-10-02

| Recipe | Outputs | Purpose |
| --- | --- | --- |
| [flatpak](devario-core/flatpak/PKGBUILD) | `flatpak` and `flatpak-docs` 1:1.18.4-3 | Shelly's Flatpak backend |
| [inxi](devario-core/inxi/PKGBUILD) | `inxi` 3.3.41.1-3 | Devario system reports |
| [nbd](devario-core/nbd/PKGBUILD) | `nbd` 3.27.1-4 | Live image network block devices |
| [nfs-utils](devario-core/nfs-utils/PKGBUILD) | `nfs-utils` and `nfsidmap` 3.1.1-3 | Live image NFS support |
| [tpm2-tools](devario-core/tpm2-tools/PKGBUILD) | `tpm2-tools` 5.8-2 | Dracut TPM support |

[spandsp](devario-core/spandsp/PKGBUILD) is also updated to `0.0.6-6` to
provide `libspandsp.so` and `libspandsp.so=2-64` for PipeWire. Its packaging
function verifies the ELF class and SONAME before publication. The existing
[inter-font](devario-core/inter-font/PKGBUILD) recipe supplies the remaining
missing installer font package.

The five new recipes preserve Arch's supporting files, packaging licenses,
source checksums, and upstream signing keys, except that inxi uses a pinned,
checksummed Git commit. Codeberg's generated inxi archive no longer matches
Arch's recorded checksum; its complete file contents were compared with the
release commit and found identical. Per-package READMEs record the exact Arch
packaging commits and validation results.

Import the bundled public keys as the worker account before verifying signed
sources:

```sh
gpg --import devario-core/flatpak/keys/pgp/*.asc \
  devario-core/nfs-utils/keys/pgp/*.asc \
  devario-core/tpm2-tools/keys/pgp/*.asc
```

Then review and build each selected directory, for example:

```sh
shelly build --review-only --json ./devario-core/tpm2-tools/PKGBUILD
shelly build --isolated --check ./devario-core/tpm2-tools/PKGBUILD
```

The signed repository databases inspected on 2026-10-02 still lack these
prerequisites. They must be supplied separately; these recipes do not make
the repository dependency closure complete:

| Consumer | Missing runtime prerequisites | Missing build/test prerequisites |
| --- | --- | --- |
| flatpak | `libmalcontent`, `xdg-dbus-proxy` | `gtk-doc`, `python-pyparsing`, `xmlto` |
| nbd | None in the inspected databases | `autoconf-archive`, `docbook-utils`, `perl-sgmls` |
| nfs-utils | `rpcbind`, `gssproxy`; `nfsidmap` is produced by this recipe | `rpcsvc-proto` |
| tpm2-tools | Publish the existing `tpm2-tss` 4.2.0-3 recipe's explicit ABI provisions | `autoconf-archive`, `cmocka`; tests also need `expect`, `swtpm`, `tpm2-abrmd` |

These are direct dependency checks against the inspected database snapshot,
not a complete recursive bootstrap audit. Inxi's declared dependencies were
available. Publish both NFS outputs together. Publish the updated `tpm2-tss`
before building `tpm2-tools`. `cmocka` is a build dependency because unit-test
binaries are enabled at configure time even when `check()` is skipped.

All six changed recipes pass Bash syntax, generated makepkg metadata, Shelly
metadata generation, and Shelly review. All source checksums pass, and Flatpak,
NFS, and TPM upstream signatures verify with the bundled keys. Local makepkg
builds of inxi and spandsp succeeded; the installed inxi command reports its
version and spandsp's archive carries its versioned library provision.
NBD's three upstream fixes apply, but preparation on this host stops at the
missing declared `autoconf-archive` dependency. Flatpak, NFS, TPM, and complete
NBD builds have not been run. Isolated worker builds remain required.

Flatpak and NBD retain Arch's disabled integration-test policy because those
tests hang or fail in package-build containers. Flatpak release 3 explicitly
disables test compilation and installation through Meson; omitting `check()`
alone left `socat` required at configure time in release 2. An invocation with
`--check` does not provide runtime or
network-device acceptance for either package.

For curl, GPGME, libarchive, OpenSSL, XZ, MPFR, ncurses, readline, xxHash,
and Zstandard with explicit ABI provisions, see [the ABI build guide](ABI-BUILDS.md).
That guide records their separate validation status and suggested build order.

For `llvm22` and `llvm22-libs` version `22.1.8-3`, see the
[LLVM 22 build guide](devario-core/llvm22/README.md). The recipe provides
versioned tools and declares `libLLVM.so=22.1-64` explicitly for Shelly.

| Build directory | Requested packages or provisions |
| --- | --- |
| [libusb](devario-core/libusb/PKGBUILD) | `libusb`, explicitly providing `libusb-1.0.so=0-64` for libgusb |
| [qt5-base](devario-core/qt5-base/PKGBUILD) | `qt5-base` and matching `qt5-xcb-private-headers` 5.15.19+kde+r96 |
| [libdex](devario-core/libdex/PKGBUILD) | `libdex` 1.2.0, providing `libdex-1.so=1-64`; also produces `libdex-docs` |
| [python-tqdm](devario-core/python-tqdm/PKGBUILD) | `python-tqdm` 4.70.1, required by the local Meson recipe |
| [ministream](devario-core/ministream/PKGBUILD) | `ministream` 0.99.1, providing `libministream.so=1-64` for consumers such as libadwaita |
| [inter-font](devario-core/inter-font/PKGBUILD) | `inter-font`, supplying the Pearl installer’s Inter font family |
| [glycin](devario-core/glycin/PKGBUILD) | `glycin` 2.2.1 for gdk-pixbuf requiring `glycin-2 >= 2.2.alpha.7`; also produces GTK4 integration and documentation |
| [gtksourceview5](gtksourceview5/PKGBUILD) | `gtksourceview5` (also produces documentation) |
| [enchant](enchant/PKGBUILD) | `enchant` |
| [hunspell](hunspell/PKGBUILD) | `hunspell` |
| [jq](jq/PKGBUILD) | `jq` |
| [numactl](numactl/PKGBUILD) | `numactl` |
| [gcc](gcc/PKGBUILD) | `libgcc`, `libstdc++`, `libgomp`, `libgfortran`, `libquadmath`, plus the matching compiler suite |
| [dbus](dbus/PKGBUILD) | `dbus`, providing `libdbus-1.so=3-64` |
| [glib2](glib2/PKGBUILD) | `glib2`, providing `libglib-2.0.so=0-64` (also produces development tools and documentation) |
| [nvidia-utils](nvidia-utils/PKGBUILD) | `nvidia-utils`, providing `opengl-driver`, `vulkan-driver`, and `nvidia-libgl` |

For the gdk-pixbuf error finding glycin 2.1.0, follow the
[glycin build guide](devario-core/glycin/README.md). Build and publish glycin
2.2.1 first, refresh the worker repository, then retry gdk-pixbuf in a fresh
isolated root. Its worker recipe should require `glycin>=2.2.1`.

If Shelly lists `ministream` before refusing an AUR dependency step in an
isolated build, follow the [ministream build guide](devario-core/ministream/README.md).
Build and publish ministream to the worker repository first, refresh its
database, and retry the dependent package in a fresh isolated root.

For NVIDIA's binary utilities, see the [nvidia-utils build guide](nvidia-utils/README.md)
for separate validation results and driver integration requirements. This recipe
produces only `nvidia-utils 615.71.09-2`; the matching `615.71.09` kernel driver
must be supplied separately. Make `libglvnd`, `egl-wayland`, `egl-wayland2`,
`egl-gbm`, and `egl-x11` available to the worker before building it. Coordinate
driver publication and upgrades, including matching multilib/OpenCL packages
where used.

The library provisions are explicit because Shelly's native packager preserves
bare `.so` provisions without adding the SONAME version. Each modified provision
has an ELF64/SONAME check in the packaging function. Source checksums remain
enabled, and D-Bus and GLib retain signed-tag verification.

## Build on the worker

Import the supplied upstream public keys **as the account that invokes Shelly**,
after comparing the fingerprints with the package README files:

```sh
gpg --import dbus/*.asc glib2/*.asc
```

Review and build a recipe from this repository's root, for example:

```sh
shelly build --review-only --json ./hunspell/PKGBUILD
shelly build --isolated --check ./hunspell/PKGBUILD
```

Repeat with the directory names in the table. Run the GCC recipe once to produce
all five requested GCC runtime packages. Its full compiler bootstrap takes much
more time and disk space than the other recipes; see [gcc/README.md](gcc/README.md).

The isolated root must have access to repositories containing the declared build
dependencies. Build and publish the GCC outputs together, then build the other
recipes using that repository. Build Hunspell before Enchant, and GLib (including
`glib2-devel`) before GtkSourceView. D-Bus and GLib use each other during building;
an existing compatible package from a bootstrap repository is needed to start
that cycle. These recipes assume an existing working toolchain and package
repository, rather than bootstrapping a distribution from an empty root.

After building, publish the resulting archives and refresh the repository
database used by Remora/Shelly. Editing `.SRCINFO` alone does not update installed
packages or repository dependency resolution. The ABI provisions must appear in
the new packages' `.PKGINFO` and in the repository database. For example:

```sh
bsdtar -xOf /path/to/dbus-1.16.2-2-x86_64.pkg.tar.zst .PKGINFO | grep '^provides = '
bsdtar -xOf /path/to/glib2-2.90.0-1-x86_64.pkg.tar.zst .PKGINFO | grep '^provides = '
```

Compiler architecture flags come from the worker's Shelly configuration. These
recipes declare `arch=(x86_64)` and do not impose `-march=native` or a v3 baseline.

## Validation

The original eight recipes above pass Bash syntax checks and generate `.SRCINFO`.
Seven have no Shelly review findings. GCC's review warns about upstream command substitutions
and Makefile variables in its patch; those inputs were inspected and retained.
Checksums for the included patches and scripts match the upstream recipes.

Native, unprivileged Shelly builds with checks enabled succeeded for Hunspell,
jq, numactl, Enchant, GtkSourceView, D-Bus, and GLib. The generated archives'
`.PKGINFO` contains the expected ABI provisions, including both D-Bus and GLib
requirements above. Temporary build tools were
extracted under `/tmp`; no host packages were installed. Full GCC compilation
has not been run. GLib has since been updated to 2.90.0; its current validation
status is recorded in the [GLib build guide](devario-core/glib2/README.md).

Full `--isolated` nspawn verification is unavailable in this environment because
Shelly's privileged coordinator needs an interactive sudo password. Run the
isolated commands on the worker before publishing the packages.

## Qt 6.12 version alignment

The published `qt6-declarative 6.12.0-1` archive contains QML but omits Qt Quick
and Quick Widgets, preventing Calamares from loading `libQt6QuickWidgets.so.6`.
Build and publish `devario-core/qt6-shadertools` and
`devario-core/qt6-languageserver` (both 6.12.0-1) first, then rebuild
`devario-core/qt6-declarative` as 6.12.0-2 in a fresh isolated root. These new
recipes pin Qt build inputs to 6.12.0. The declarative recipe requires the
ShaderToolsTools CMake package and rejects staged packages missing QML, Quick,
or Quick Widgets libraries. Upstream source checksums are retained; Bash syntax
and generated metadata were checked, but these new recipes have not been compiled.

The [qt6-base recipe](devario-core/qt6-base/PKGBUILD) builds Qt 6.12.0 and its
`qt6-xcb-private-headers` split package. The local
[tools](devario-core/qt6-tools/PKGBUILD) and
[translations](devario-core/qt6-translations/PKGBUILD) recipes now also use
6.12.0. Qt's CMake compatibility checks remain enabled.

Recipes are adapted from official Arch packaging:
[base](https://gitlab.archlinux.org/archlinux/packaging/packages/qt6-base),
[tools](https://gitlab.archlinux.org/archlinux/packaging/packages/qt6-tools), and
[translations](https://gitlab.archlinux.org/archlinux/packaging/packages/qt6-translations).
Base includes its two upstream patches and QtWebEngine CMake detection backport.
Tools no longer applies the old LLVM 22 patch; it retains the pinned qlitehtml
commit and checksum used by the previous local recipe.

Build and publish base first. Make `qt6-declarative=6.12.0` available from the
worker repository before building tools, then build translations. Tools pins
both base and declarative to 6.12.0 as runtime dependencies; translations pins
base, declarative, and tools to 6.12.0 as build dependencies.
Refresh the worker repository between stages and use clean isolated build roots.
An existing translations package is needed to provision consumers of the new
base during this cycle, because base depends on translations. Publish the
matching Qt suite together for downstream use.

Qt 6.12's `lrelease` links to QtQml through LinguistProject and TrLib when tools
is built with QML support. Tools `6.12.0-3` therefore requires declarative at
runtime. Translations `6.12.0-3` also explicitly requests declarative so isolated
builds work with tools packages that still have the older dependency metadata.
This fixes `lrelease: error while loading shared libraries: libQt6Qml.so.6`.
Sync the updated translations PKGBUILD into the worker's selected package
directory (the reported failure uses `default/qt6-translations`), then retry in
a fresh root. Publish the corrected tools package for other `lrelease` users.

Validation: all three recipes pass Bash syntax, makepkg/Shelly metadata, and
Shelly review. Base's bundled patches match their declared checksums. Full
builds and remote-source checksum verification have not been run.

## Calamares build dependency: litehtml

The core-only Calamares build requires `qt6-tools`, whose `litehtml` dependency
was absent from `devario-core`. These two complete recipe directories supply
that dependency and its HTML parser:

| Build and publish order | Release | Directory |
| --- | --- | --- |
| 1. gumbo-parser | 0.13.2-2 | [devario-core/gumbo-parser](devario-core/gumbo-parser/PKGBUILD) |
| 2. litehtml | 0.10-2 | [devario-core/litehtml](devario-core/litehtml/PKGBUILD) |

Upload each complete directory to the Devario build worker. Publish
`gumbo-parser` to `devario-core` and refresh the worker repository before building
`litehtml` in a fresh root. Then publish `litehtml` and rerun `devario-os/build-iso.sh`
with a fresh repository snapshot. Use the Devario x86-64-v3 build environment
for the published packages.

Litehtml 0.10 matches the system-library integration in the existing Qt 6.12
tools recipe. It builds against the separately packaged Gumbo library and
removes the upstream CMake lookup for a Gumbo config file that Gumbo does not
install. Both recipes include explicit SONAME provisions and reject unexpected
library ABI versions during packaging.

Recipes are adapted from official Arch packaging for
[litehtml](https://gitlab.archlinux.org/archlinux/packaging/packages/litehtml) and
[gumbo-parser](https://gitlab.archlinux.org/archlinux/packaging/packages/gumbo-parser).
Litehtml retains the upstream packaging checksum. The current Codeberg Gumbo
archive has a different compressed checksum from the Arch recipe; all 92 tracked
source files were compared with upstream release tag `0.13.2`, commit
`322c54c178590ba42b8b04e8c0e4840595a1f717`, before pinning its current SHA-256.

Validation: both source checksums, Bash syntax, matching makepkg/Shelly metadata,
and Shelly review passed. Both recipes' build and package functions completed
locally; Gumbo passed all 184 tests. A separate CMake consumer discovered, linked,
and ran against the staged libraries. The staged libraries have the expected
SONAMEs and no temporary build-directory RPATHs. Adding these outputs to the
retained core snapshot's dependency model resolves Qt tools and all declared
build/check dependencies of these recipes. Isolated worker builds and
publication remain to be done.

## Noto fonts source directory

[noto-fonts](devario-core/noto-fonts/PKGBUILD) release `1:2026.10.01-2` fixes
the `cd: notofonts: No such file or directory` failure in both split-package
functions. The original source URL ends in `notofonts.github.io`. Makepkg's
Git filename handling truncates at `.git`, giving `notofonts`, while Shelly
retains `notofonts.github.io` because it only removes a terminal `.git` suffix.
The explicit `notofonts::` source alias makes both builders create the directory
the recipe expects. Both packaging functions now use `$srcdir/notofonts`.

The recipe retains the monthly release tag, upstream SHA-256 checksums, all
four fontconfig files, and the `noto-fonts` / `noto-fonts-extra` split from
[Arch packaging commit 0851acf360a933d18d8ae511c50229028686950b](https://gitlab.archlinux.org/archlinux/packaging/packages/noto-fonts/-/commit/0851acf360a933d18d8ae511c50229028686950b).
The tag resolves to `025970232f4f8ff349310d9785431e87d20ed27c`, matching the
checkout shown in the worker's failure. Copy the whole directory to the worker
and retry:

```sh
shelly build --isolated ./devario-core/noto-fonts/PKGBUILD
```

Validation: all five source checksums passed. A local makepkg build from the
pinned release produced both archives: 621 fonts in `noto-fonts` and 1,550 in
`noto-fonts-extra`, matching the source selections without overlapping package
payloads. All four fontconfig symlinks resolve correctly, and the upstream
license is included. Bash syntax and makepkg/Shelly metadata checks passed;
Shelly review reported no findings. A full isolated Shelly build remains
unverified.

## GTK3 bindings blocking the ISO dependency audit

The 2026-10-05 ISO run `20261005T164652Z-75817` selected 644 packages but
reported six unresolved requirements. Its published `atkmm` 2.36.4 and
`cairomm` 1.19.1 belonged to incompatible ABI branches. GParted, gtkmm3, and
pangomm still require `libatkmm-1.6.so` and `libcairomm-1.0.so`. The newer
packages also introduced unavailable glibmm-2.68 and libsigc++-3.0 dependencies.

The corrected recipes follow the GTK3 branches in the official
[atkmm packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/atkmm)
and [cairomm packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/cairomm),
retaining their pinned Git tags and upstream packaging BLAKE2 checksums:

| Recipe | Corrected version | Required library |
| --- | --- | --- |
| [atkmm](devario-core/atkmm/PKGBUILD) | `1:2.28.5-1` | `libatkmm-1.6.so.1` |
| [cairomm](devario-core/cairomm/PKGBUILD) | `1:1.14.6-1` | `libcairomm-1.0.so.1` |

Epoch 1 makes these corrections upgrades over the already-published versions.
Both recipes use the existing glibmm/libsigc++ ABI family, publish bare and
explicit `=1-64` library provisions, and verify the real ELF64 SONAME before
packaging succeeds. Do not substitute the newer ABI libraries with symlinks or
metadata-only provides. The newer bindings now have distinct packages, listed
below, so both generations can coexist.

Build `mm-common` first if it is not yet published, then build both corrected
recipes and publish their matching runtime and documentation outputs:

```sh
shelly build --isolated --check ./devario-core/cairomm/PKGBUILD
shelly build --isolated --check ./devario-core/atkmm/PKGBUILD
```

After signing and publishing the replacement archives and refreshing the hosted
repository database, retry the ISO build using a fresh repository snapshot.
The retained failed run still contains the incompatible archives. Its six local
installer packages are not the cause, and changing only their metadata or
rerunning against the same snapshot cannot fix the failure.

The validation and remaining release steps for both generations are recorded
below. Keep the epoch when refreshing the corrected GTK3 packages.

## Parallel C++ binding packages

These recipes preserve the newer ABI stack without replacing GTK3's package
names, headers, libraries, pkg-config files, or documentation:

| Recipe | Version | Outputs |
| --- | --- | --- |
| [mm-common](devario-core/mm-common/PKGBUILD) | `1.0.8-1` | `mm-common` |
| [libsigc++-3.0](devario-core/libsigc++-3.0/PKGBUILD) | `3.8.1-1` | `libsigc++-3.0`, `libsigc++-3.0-docs` |
| [glibmm-2.68](devario-core/glibmm-2.68/PKGBUILD) | `2.90.0-1` | `glibmm-2.68`, `glibmm-2.68-docs` |
| [cairomm-1.16](devario-core/cairomm-1.16/PKGBUILD) | `1.19.1-1` | `cairomm-1.16`, `cairomm-1.16-docs` |
| [atkmm-2.36](devario-core/atkmm-2.36/PKGBUILD) | `2.36.4-1` | `atkmm-2.36`, `atkmm-2.36-docs` |

Package suffixes identify the ABI, not the upstream release number. The newer
atkmm and cairomm recipes preserve the source versions previously published
under the wrong names. Each library recipe checks its actual ELF64 SONAME and
provides only its own library ABI; none provides, replaces, or conflicts with
the legacy package names. Documentation packages also have separate names.

The new recipes follow official Arch packaging for
[atkmm-2.36](https://gitlab.archlinux.org/archlinux/packaging/packages/atkmm-2.36),
[cairomm-1.16](https://gitlab.archlinux.org/archlinux/packaging/packages/cairomm-1.16),
[glibmm-2.68](https://gitlab.archlinux.org/archlinux/packaging/packages/glibmm-2.68),
[libsigc++-3.0](https://gitlab.archlinux.org/archlinux/packaging/packages/libsigcplusplus-3.0),
and [mm-common](https://gitlab.archlinux.org/archlinux/packaging/packages/mm-common).
The cairomm 1.19.1 tag and checksum come from this repository's previous
cairomm recipe. Every source remains pinned and checksum-verified.

`glibmm-2.68` explicitly requires `glib2>=2.89.4`, matching its upstream
build requirement. The retained repository already has GLib 2.90.0.
`mm-common` uses the existing legacy libsigc++ and its documentation to bootstrap;
there is no dependency on the new sigc++ package. It builds without network
access using a separately downloaded, checksum-pinned GCC documentation tag.
It requires `libxslt` for the C++ documentation tools and makes the unrelated
GTK C documentation generator `gtk-doc` optional.

Build and publish in this order, refreshing the worker's repository database
between dependency stages. Publish runtime and documentation outputs together:

1. `mm-common`, using existing `libsigc++` and `libsigc++-docs`.
2. Corrected `atkmm` and `cairomm`, including their `-docs` outputs.
3. `libsigc++-3.0`, including `libsigc++-3.0-docs`.
4. `glibmm-2.68` and `cairomm-1.16`, including their `-docs` outputs.
5. `atkmm-2.36`, after the new GLibmm runtime and documentation are available.

For example, from this repository root:

```sh
shelly build --isolated --check ./devario-core/mm-common/PKGBUILD
# Publish mm-common before building the dependent recipes.
shelly build --isolated --check ./devario-core/libsigc++-3.0/PKGBUILD
# Publish both sigc++ outputs before building the next stage.
shelly build --isolated --check ./devario-core/glibmm-2.68/PKGBUILD
shelly build --isolated --check ./devario-core/cairomm-1.16/PKGBUILD
# Publish the new GLibmm outputs before building atkmm-2.36.
shelly build --isolated --check ./devario-core/atkmm-2.36/PKGBUILD
```

Installations containing the mistakenly named modern libraries must upgrade
`atkmm`, `cairomm`, and their documentation to the corrected epoch-1 packages
before, or in the same transaction as, installing the parallel modern packages.
Otherwise the old incorrect archives still own the modern paths. Do not add
`conflicts` or `replaces` against the correctly named legacy packages to work
around that transitional state. After publication, a fresh ISO snapshot should
select the corrected legacy packages for GParted. The optional modern stack
does not need to be added to the live ISO to repair its dependency closure.

Validation on 2026-10-05:

- All seven recipe source checksums and the extra GCC tag-file checksum passed.
- All seven recipes completed native build and package-function runs under
  `/tmp`, using staged build dependencies without installing them on the host.
- Sigc++ passed 42 upstream tests, modern cairomm passed 7, and GLibmm passed 35
  with 2 expected failures. The GLibmm package check explicitly excludes
  `giomm_tls_client_test`, which connects to `www.gnome.org` and fails without
  DNS/network access. The test remains available for separate network testing.
  Atkmm and mm-common define no Meson tests in these configurations.
- File inventories for 17 runtime/documentation payloads, including the existing
  legacy GLibmm and sigc++ archives, have no overlapping non-directory paths.
- `tests/test-gtk3-binding-abi.py` checks both generations' ABI guards, rejection
  of wrong/missing ELF libraries, separate package identities/provisions, and
  upgrade ordering for the corrected legacy packages.
- Bash syntax, regenerated `.SRCINFO`, and Shelly review passed. Shelly reported
  no review findings for the new recipes.
- A metadata projection resolves all runtime, build, and check dependencies
  against the retained repository: 175 selected packages, zero unresolved
  requirements. The earlier ISO projection remains 644 selected packages with
  zero unresolved requirements after correcting the two legacy providers.

These are native staged builds and metadata audits, not signed release builds.
Clean isolated package builds, signed publication, a fresh repository audit,
and the ISO rebuild remain required before the reported ISO failure is fixed
in published artifacts.

## mupdf dependency chain

`devario-utilities/mupdf` fails `--resolve-dependencies` on six names. Four new
`devario-libs` recipes cover the three that had no recipe plus the OCR data
`tesseract` requires at install time; `unzip`, `zint` and `zxing-cpp` already
have recipes that are simply not published yet.

```sh
shelly build --isolated --check ./devario-libs/cmark-gfm/PKGBUILD
shelly build --isolated --check ./devario-libs/leptonica/PKGBUILD
# Publish leptonica before tesseract, which depends on it globally.
shelly build --isolated --check ./devario-libs/tesseract/PKGBUILD
shelly build --isolated --check ./devario-libs/tesseract-data/PKGBUILD
shelly build --isolated --check ./devario-utilities/unzip/PKGBUILD
shelly build --isolated --check ./devario-libs/zint/PKGBUILD
# Publish zint before zxing-cpp, which depends on it globally.
shelly build --isolated --check ./devario-libs/zxing-cpp/PKGBUILD
```

`tesseract` and `tesseract-data` require each other, but only through
`depends+=()` inside `package_*()`. Shelly plans global `depends` plus
makedepends, so neither side enters the other's build root and the cycle
resolves at install time as it does in Arch. For the same reason
`tesseract-data` can be built before `tesseract` is published.

`leptonica` declares each `.so` requirement in the form its published provider
actually advertises. Published `libpng` and `zlib` carry only bare provisions,
so `libpng16.so` and `libz.so` stay bare; porting either provider to an explicit
versioned provision would let those two match the rest.

Still blocked: `zxing-cpp` makedepends on `opencv`, whose global makedepends
include `java-environment`. Nothing published provides `java-environment` or
`java-runtime`, and every local JDK recipe pins `java-environment` to its own
version, so `zxing-cpp` and therefore `mupdf` cannot build until that bootstrap
is resolved. Every other recipe above is buildable now.

Validation on 2026-10-10:

- All four source checksums were recomputed from downloaded upstream tarballs and
  match the official Arch recipes. The 668 MiB `tessdata` archive is used in full
  only as a source; two files are installed from it.
- `bash -n`, regenerated `.SRCINFO`, and `shelly build --review-only --json` all
  passed for the four recipes, with no review findings.
- `tesseract-data` was rejected by Shelly review while it still used upstream's
  `pkgname=("${_langs[@]/#/tesseract-data-}")` array expansion
  (`UnsupportedArrayExpansion`); the two packages are now written out explicitly.
- Every `depends`, `makedepends` and `checkdepends` entry in the four `.SRCINFO`
  files, at pkgbase and per-package level, resolves against the published
  repositories once the four recipes and their declared provisions are counted as
  available.
- The three SONAME values in the explicit provisions come from the sources:
  `SOVERSION` in cmark-gfm's `src/` and `extensions/` CMakeLists, and
  `-version-info 6:0:0` in leptonica's `src/Makefile.am`. Each `package()`
  re-checks ELF64 and the SONAME before packaging.

No isolated build, publication, or `mupdf` build has been performed for this
change.
