# Missing dependency builds for Shelly

For Zig 0.16 and its LLVM 21, CMake, GCC, and Python prerequisites, see
[the Zig build guide](ZIG-BUILDS.md).

Devario is an independent operating system. These x86_64 recipes are adapted
from the corresponding
[Arch Linux packaging repositories](https://gitlab.archlinux.org/archlinux/packaging/packages).
Those links record recipe provenance.
Each directory includes its PKGBUILD, generated `.SRCINFO`, and required local
source files. Copy whole directories to the Remora worker.

For curl, GPGME, libarchive, OpenSSL, XZ, MPFR, ncurses, readline, xxHash,
and Zstandard with explicit ABI provisions, see [the ABI build guide](ABI-BUILDS.md).
That guide records their separate validation status and suggested build order.

For `llvm22` and `llvm22-libs` version `22.1.8-3`, see the
[LLVM 22 build guide](devario-core/llvm22/README.md). The recipe provides
versioned tools and declares `libLLVM.so=22.1-64` explicitly for Shelly.

| Build directory | Requested packages or provisions |
| --- | --- |
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
