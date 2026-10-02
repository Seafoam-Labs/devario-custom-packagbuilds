# Devario live USB and installer packages

This folder contains the eight OS-owned recipes and their supporting files:

| Recipe | Build order |
| --- | --- |
| [devario-filesystem](devario-filesystem/PKGBUILD) | Before devario-base |
| [devario-keyring](devario-keyring/PKGBUILD) | Before devario-base |
| [seafoam-keyring](seafoam-keyring/PKGBUILD) | Before devario-base |
| [devario-boot](devario-boot/PKGBUILD) | After devario-dracut; before devario-base |
| [devario-base](devario-base/PKGBUILD) | After filesystem, boot, and both keyrings |
| [devario-aqueous-desktop](devario-aqueous-desktop/PKGBUILD) | After the five Aqueous 1.0.0-1 components |
| [ckbcomp](ckbcomp/PKGBUILD) | Before Calamares |
| [calamares](calamares/PKGBUILD) | After ckbcomp and inter-font |

Copy complete recipe directories to a worker. From this repository's root,
review and build a recipe with:

```sh
shelly build --review-only --json ./devario-installer/ckbcomp/PKGBUILD
shelly build --isolated --check ./devario-installer/ckbcomp/PKGBUILD
```

General runtime dependencies remain in `../devario-core/`. The source folder
name does not change the ISO's binary repository: completed signed packages
must still be included in its staged `devario-core` repository with their
dependencies and matching signed metadata.

These recipes are copies of the OS repository's recipes with local packaging
adjustments. The OS repository can also build its own copies using
`scripts/build-packages.sh` or `scripts/build-packages-nspawn.sh`. Its ISO
assembler consumes completed packages. The two sets of recipes do not
automatically synchronize.

See [dependency build notes](../DEPENDENCY-BUILDS.md) for prerequisites and
validation limitations. Shared [provenance](../devario-core/iso-packages-upstream.json)
and [validation records](../devario-core/iso-packages-validation.json) cover both
the runtime recipes and these OS packages.
