# Plymouth for Devario

Builds Plymouth 26.134.222 from the upstream release archive, with DRM,
framebuffer, X11 preview, text renderers, password prompts and systemd units.
The pinned keyboard-layout fix preserves `KEYMAP` when `XKBLAYOUT` is unset.

The recipe is adapted from [Arch's Plymouth packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/plymouth).
It uses a checksummed release tarball and bundled upstream patch instead of
a Git checkout. It keeps Arch's Adwaita font selection, omits Arch artwork
and mkinitcpio hooks, and replaces `plymouth-update-initrd` with Devario's
`/usr/lib/devario/boot-update`. The latter is supplied by the required
`devario-boot` package and preserves Devario's fallback images and boot entries.
Packaging attribution is retained in `PKGBUILD` and `LICENSE.packaging`.

From the repository root:

```sh
shelly build --isolated --check ./devario-core/plymouth/PKGBUILD
```

Publish Plymouth to the worker's enabled repository and refresh its metadata
before building `devario-plymouth-theme`. All direct build/runtime dependency
names were present in the public `devario-core` database on 2026-10-13.

Devario OS enables this package in its live and installed boot profiles.
`devario-boot` 1-10 adds `splash` to installed boot arguments and rebuilds
installed initramfs images when Plymouth or the Devario theme is updated.
The ISO overlay selects the theme; see the adjacent theme's README.

Validation: the release checksum and patch were verified; a native compilation
and package archive build succeeded using existing host libraries, with
dependency installation disabled. An isolated Devario worker build and physical
boot tests are still required. Upstream defines no Meson test suite.
