# Missing dependency builds for Shelly

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

All recipes pass Bash syntax checks and generate `.SRCINFO`. Seven have no
Shelly review findings. GCC's review warns about upstream command substitutions
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
