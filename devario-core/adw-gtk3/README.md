# adw-gtk3

Packages upstream v6.5's compiled light and dark GTK 3/4 themes as
`adw-gtk3` and `adw-gtk3-dark` under `/usr/share/themes`. GTK 4 support
requires GTK 4.20 or newer. Both upstream archives are pinned by SHA-256;
the matching source archive supplies the license and corresponding source.
No Sass compiler or network access from package functions is required.

From the package repository root:

```sh
shelly build --review-only --json ./devario-core/adw-gtk3/PKGBUILD
shelly build --isolated --check ./devario-core/adw-gtk3/PKGBUILD
```

After installation, select `adw-gtk3` or `adw-gtk3-dark` through GTK settings.
For Pearl, enable the managed GTK Material application profile to layer its
generated colors over this theme. The package installs theme assets; distro
selection belongs in the desktop's GTK and GSettings defaults.
