# Qt 5 translations for Devario

Builds `qt5-translations` 5.15.19-2 as an architecture-independent package.
The KDE Qt translations source is pinned to commit
`388e4f32ed4b28d92bd61b917ba0e6b910e2784d`. The version is fixed, so shallow
source checkouts do not change the package version.

The recipe uses `qmake-qt5` from `qt5-base` and Linguist tools from `qt5-tools`
to compile the upstream catalogs, including the generated English catalogs.
It installs `.qm` files under `/usr/share/qt/translations` and follows the Qt
suite's shared license layout. The package has no runtime dependencies.

From the repository root:

```sh
shelly build --review-only --json ./devario-libs/qt5-translations/PKGBUILD
shelly build --isolated ./devario-libs/qt5-translations/PKGBUILD
```

## Bootstrap order

The previous mandatory dependency created a Qt suite bootstrap cycle:
`qt5-base -> qt5-translations -> qt5-tools -> qt5-base`.
`qt5-base` release 3 makes translations optional, so it can be installed
before the catalogs and their build tools exist. Qt uses untranslated
messages until the catalogs are installed.

With the non-Qt prerequisites available, build and publish in this order:

1. `devario-core/qt5-base`: release 3, including matching private headers.
2. `devario-libs/qt5-declarative`.
3. `devario-libs/qt5-tools`.
4. `devario-libs/qt5-translations`.

Refresh the worker repository metadata after each publication before starting
the next build. Rebuild and publish base first: the old binary package still
requires translations even after the PKGBUILD is updated. Retry the failed
jobs in the order above once the corrected base package is available.
Install translations on desktop systems for localized Qt messages; they are
no longer pulled in as a mandatory dependency of base.

## Validation

Bash syntax and matching makepkg/Shelly metadata generation passed.
The recipe's prepare, build, and package functions compiled and staged all
345 expected catalogs from the pinned source archive, including generated
English catalogs. All installed catalogs had valid QM file headers, and the
license link pointed to `/usr/share/licenses/qt5-base`.

This host validation used Qt 5.15.19 qmake and a Qt 5.15.19 lrelease extracted
into a temporary directory, selected through qmake's `QT_TOOL.lrelease.binary`
override. No host packages were installed. An isolated Shelly build and final
package archive generation have not been run.
