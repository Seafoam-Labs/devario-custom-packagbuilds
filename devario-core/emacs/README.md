# emacs for Shelly

Based on [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/emacs/-/blob/main/PKGBUILD), pinned to `31.1-2`. Copy the whole directory to the worker, including local patches and `keys/` where present.

One build produces `emacs`, `emacs-nox`, and `emacs-wayland`. Install only one variant; the latter two provide `emacs` and conflict with it. Native compilation needs `libgccjit`, supplied by the existing GCC recipe. The upstream source list includes the two Tree-sitter patches, but its current `prepare()` does not apply them. Upstream packaging has no `check()` hook.

Emacs' `configure` aborts the X11 build when `X11/xpm.h` is missing (`The following required libraries were not found: libXpm`). Arch's recipe does not declare it, so `libxpm` is a `makedepends` here and only the `emacs` output depends on it: `emacs-nox` builds `--without-x`, and the `--with-pgtk` wayland build links neither libXpm nor X11.

The permitted upstream signing fingerprints are:

- `17E90D521672C04631B1183EE78DAE0F3115E06B`
- `CEA1DE21AB108493CC9C65742E82323B8F4353EE`
- `8DC2487E51ABDD90B5C4753F0F56D0553B6D411B`

Import the supplied public keys as the build account after checking these fingerprints:

```sh
gpg --import emacs/keys/pgp/*.asc
```

From the repository root:

```sh
shelly build --review-only --json ./emacs/PKGBUILD
shelly build --isolated --check ./emacs/PKGBUILD
```

Bash syntax, generated metadata, source checksums, applicable signatures, and source preparation were validated. makepkg and Shelly metadata agree. See [the Zig build guide](../ZIG-BUILDS.md) for build order, bootstrap dependencies, review findings, and the exact limits of local build validation.
