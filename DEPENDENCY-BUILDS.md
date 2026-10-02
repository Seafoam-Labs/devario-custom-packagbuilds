# Missing dependency builds for Shelly

For Zig 0.16 and its LLVM 21, CMake, GCC, and Python prerequisites, see
[the Zig build guide](ZIG-BUILDS.md).

These x86_64 recipes are adapted from the corresponding
[Arch Linux packaging repositories](https://gitlab.archlinux.org/archlinux/packaging/packages).
Each directory includes its PKGBUILD, generated `.SRCINFO`, and required local
source files. Copy whole directories to the Remora worker.

For curl, GPGME, libarchive, OpenSSL, XZ, MPFR, ncurses, readline, xxHash,
and Zstandard with explicit ABI provisions, see [the ABI build guide](ABI-BUILDS.md).
That guide records their separate validation status and suggested build order.

| Build directory | Requested packages or provisions |
| --- | --- |
| [gtksourceview5](gtksourceview5/PKGBUILD) | `gtksourceview5` (also produces documentation) |
| [enchant](enchant/PKGBUILD) | `enchant` |
| [hunspell](hunspell/PKGBUILD) | `hunspell` |
| [jq](jq/PKGBUILD) | `jq` |
| [numactl](numactl/PKGBUILD) | `numactl` |
| [gcc](gcc/PKGBUILD) | `libgcc`, `libstdc++`, `libgomp`, `libgfortran`, `libquadmath`, plus the matching compiler suite |
| [dbus](dbus/PKGBUILD) | `dbus`, providing `libdbus-1.so=3-64` |
| [glib2](glib2/PKGBUILD) | `glib2`, providing `libglib-2.0.so=0-64` (also produces development tools and documentation) |
| [nvidia-utils](nvidia-utils/PKGBUILD) | `nvidia-utils`, providing `opengl-driver`, `vulkan-driver`, and `nvidia-libgl` |

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
bsdtar -xOf /path/to/glib2-2.88.3-2-x86_64.pkg.tar.zst .PKGINFO | grep '^provides = '
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
has not been run.

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
