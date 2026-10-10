# Qt 5 base for Devario

Builds `qt5-base` and `qt5-xcb-private-headers` 5.15.19+kde+r96-2 for
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
SQL drivers. `qt5-translations` is a runtime dependency; an existing Qt 5
translations package is needed when provisioning the build. Keep the Qt 5
suite compatible when publishing upgrades.

Printing support is explicitly enabled with `-cups` and builds against
`libcups`, which supplies the headers and library. Do not add the `cups`
daemon to `makedepends`: it pulls in `cups-filters -> libcupsfilters ->
poppler`, whose split build requires Qt 5 and Qt 6, creating a build cycle.
The Qt 6 recipe uses the same library-only dependency. See the
[Poppler build notes](../../devario-libs/poppler/README.md) for build order.

## Validation

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
