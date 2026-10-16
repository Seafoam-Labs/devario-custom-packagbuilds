# Vorta dependency build order

The Vorta worker reported `IncompleteDependencyPlan` because `borg`,
`python-peewee`, `python-pyqt6`, and `python-secretstorage` were unavailable.
Their recipes are now included, along with the missing supporting packages
`python-pkgconfig`, `python-pyqt6-sip`, and `python-jeepney`.

Build each stage with `--no-check`, publish its package outputs to the indicated
Devario repository, and refresh the worker's repository databases before the
next stage. Merely copying these recipes does not make their packages available
to an isolated Vorta build. These stages assume the existing runtime and build
dependencies in the configured Devario repositories are available.

| Stage | Package output | Recipe |
| --- | --- | --- |
| 1 | `python-pkgconfig` | [devario-libs/python-pkgconfig](devario-libs/python-pkgconfig/PKGBUILD) |
| 1 | `python-pyqt6-sip` | [devario-libs/python-pyqt6-sip](devario-libs/python-pyqt6-sip/PKGBUILD) |
| 1 | `python-jeepney` | [devario-libs/python-jeepney](devario-libs/python-jeepney/PKGBUILD) |
| 1 | `python-peewee` | [devario-libs/python-peewee](devario-libs/python-peewee/PKGBUILD) |
| 2 | `borg` | [devario-utilities/borg](devario-utilities/borg/PKGBUILD) |
| 2 | `python-pyqt6` | [devario-libs/pyqt6](devario-libs/pyqt6/PKGBUILD) |
| 2 | `python-secretstorage` | [devario-libs/python-secretstorage](devario-libs/python-secretstorage/PKGBUILD) |
| 3 | `vorta` | [devario-utilities/vorta](devario-utilities/vorta/PKGBUILD) |

For example, start from the repository root with:

```sh
shelly build devario-libs/python-pkgconfig/PKGBUILD --sync-deps --no-check
```

Test-only and optional dependencies are outside this build plan. In particular,
`python-pytest-qt` is needed for Vorta's optional unit tests, and `python-pyfuse3`
is needed for mounting Borg archives. Neither is needed to build Vorta or to
create and restore backups without mounting them.

## Packaging details

The dependency recipes are adapted from the corresponding
[Arch packaging projects](https://gitlab.archlinux.org/archlinux/packaging/packages),
retaining their contributor attribution. Source archives are pinned by checksum.
PyQt6 includes the packaging project's `qt-6.12.patch`, which removes obsolete
Qt event enums so PyQt6 6.11 builds against Devario's Qt 6.12. Its command-line
tools install in `/usr/bin`, matching the existing PyQt5 recipe. A second patch,
adapted from this repository's PyQt5 recipe, delays creation of the dbus-python
support module until SIP 6.17 has validated the ABI version. Without it,
configuration fails when the declared `dbus-python` dependency is installed.

Borg uses the prebuilt manual pages supplied in its release archive, avoiding
an unnecessary Sphinx theme dependency. Jeepney's build backend constraint is
relaxed to accept the flit-core 4 recipe already present in this repository.
No package installation or repository publication is performed by these files.

## Validation

All eight recipes pass shell syntax, source checksum verification, `.SRCINFO`
generation, and Shelly review. Required runtime and build dependency names
resolve against the local Devario repository database snapshot plus these new
recipes. Test-only and optional dependencies are excluded from that check.

All seven dependencies were built and staged in temporary directories. PyQt6
was compiled against the Qt 6.12 modules available on the host; its D-Bus support
was checked separately with the system Python and SIP 6.17. Borg passed a local
init/create/check/extract round trip, and Vorta passed five upstream settings
and main-window tests using the newly built libraries. Jeepney also built with
flit-core 4.1. A full isolated worker build and publication remain to be done.
