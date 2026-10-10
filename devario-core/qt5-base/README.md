# Qt 5 base for Devario

Builds `qt5-base` and `qt5-xcb-private-headers` 5.15.19+kde+r96-3 for
x86_64, adapted from [Arch packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/qt5-base/-/blob/main/PKGBUILD).
The KDE Qt 5 source is pinned to commit
`fbed962c3195ab3952fa54d40e012ad1a4fdc42b`. Its version is fixed to that
revision, so metadata does not depend on Git history depth.

Copy this whole directory, including both qmake patches, to the worker.
From this repository's root:

```sh
shelly build --review-only --json ./devario-core/qt5-base/PKGBUILD
shelly build --isolated ./devario-core/qt5-base/PKGBUILD
```

The patches make qmake honor the worker's compiler/linker flags, enable
LTO, and leave stripping to the packager. Qt 5 headers, plugins, data, and
compatibility tool symlinks use the upstream Qt 5 packaging layout.
Private XCB headers require the exact matching base package release.

The worker repository must provide all declared dependencies, including
`mariadb-libs`, `postgresql-libs`, and `unixodbc` for the explicitly enabled
SQL drivers. `qt5-translations` is optional: Qt works without the catalogs,
using untranslated messages until they are installed. Making it a hard
dependency prevents installing base to build the translation tools.

With other prerequisites available, build and publish each package in order:
`qt5-base` (and matching private headers), `qt5-declarative`, `qt5-tools`,
then `qt5-translations`. Refresh the worker repository metadata after each
publication. In particular, rebuild and publish base release 3 first; changing
the recipe alone does not fix the dependencies in an already published base
package. See the [translations build notes](../../devario-libs/qt5-translations/README.md).

Printing support is explicitly enabled with `-cups` and builds against
`libcups`, which supplies the headers and library. Do not add the `cups`
daemon to `makedepends`: it pulls in `cups-filters -> libcupsfilters ->
poppler`, whose split build requires Qt 5 and Qt 6, creating a build cycle.
The Qt 6 recipe uses the same library-only dependency. See the
[Poppler build notes](../../devario-libs/poppler/README.md) for build order.

## Validation

The evaluated metadata for base, declarative, tools, and translations now
sorts in that order with no required dependency cycle among them. Restoring
the old base-to-translations requirement reproduces the cycle. The regenerated
base metadata matches Shelly's output, and the private headers require release
3. A Qt 5 runtime probe confirmed that missing catalogs fall back to source
messages. Full builds of the updated Qt suite have not been run.

The pinned source Git archive checksum and both patch checksums match the
upstream recipe. Both patches apply cleanly. Bash syntax and makepkg/Shelly
metadata generation passed. Shelly review flags qmake expressions in
`qmake-cflags.patch` as dynamic commands; these are the inspected upstream
expressions that read compiler/linker flags.

Qt's qmake bootstrap compiled with the host compiler. Configuration with
the recipe's options reached dependency checks, then stopped because this
host lacks the MariaDB, PostgreSQL, and ODBC development libraries. Those
packages remain required in `makedepends`. Full Qt compilation, package
generation, and isolated builds have not been run. No host packages were
installed.
