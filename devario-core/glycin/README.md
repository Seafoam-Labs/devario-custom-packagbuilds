# Glycin for gdk-pixbuf

This recipe builds `glycin`, `glycin-gtk4`, and `glycin-docs` 2.2.1-1 for
Devario. It addresses gdk-pixbuf's Meson error requiring `glycin-2 >=
2.2.alpha.7` when the worker supplies 2.1.0. `glycin-2` is the pkg-config
module installed by the `glycin` package.

The recipe is adapted from [Arch packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/glycin/-/blob/main/PKGBUILD)
and uses the [GNOME 2.2.1 release archive](https://download.gnome.org/sources/glycin/2.2/),
with its published SHA-256 checksum. The archive includes the test images;
no Git submodule checkout or 2.1-specific cherry-picks are needed. Cargo
dependencies are fetched using the release lockfile during preparation.

From this repository's root:

```sh
shelly build --review-only --json ./devario-core/glycin/PKGBUILD
shelly build --isolated --check ./devario-core/glycin/PKGBUILD
```

The worker needs Rust >= 1.93, GTK4 >= 4.16, libheif >= 1.20, and libjxl
>= 0.11.1, along with the other declared dependencies. An existing GTK4 /
gdk-pixbuf stack can bootstrap this build. The recipe retains sandboxed
loading and the upstream packaging exclusion for HEIC encoder tests.

Publish the new glycin outputs, refresh the repository database used by
Remora/Shelly, and rebuild gdk-pixbuf in a fresh isolated root. Check inside
that build root:

```sh
pkg-config --modversion glycin-2
pkg-config --atleast-version=2.2.alpha.7 glycin-2
```

The first command should report 2.2.1 and the second should succeed. If it
still reports 2.1.0, inspect `pkg-config --variable=pcfiledir glycin-2` and
the worker's selected repository/root. Updating the host package alone does
not update an isolated root. In the worker's gdk-pixbuf PKGBUILD, constrain
the runtime dependency to `glycin>=2.2.1` so dependency resolution rejects
the old library before Meson runs. Keep Meson's version check enabled.

The packages explicitly provide `libglycin-2.so=0-64` and
`libglycin-gtk4-2.so=0-64`, guarded by ELF64/SONAME checks. GTK4 integration
requires the exact matching glycin package release.

## Validation

Bash syntax, makepkg metadata generation, Shelly metadata generation, source
checksum verification, and the locked Cargo dependency fetch passed. Shelly's
review reports the expected `cargo fetch` warning for network access during
preparation. Compilation and tests use the fetched dependencies offline.

Meson configuration passed with documentation disabled for the local check.
Its generated `glycin-2.pc` reports 2.2.1 and passes the exact
`>=2.2.alpha.7` pkg-config comparison. Configuration with the recipe's full
options stopped at this host's missing `gi-docgen`, which is declared as a
build dependency. Full compilation, tests, and isolated builds have not been
run; use the worker command above before publishing.
