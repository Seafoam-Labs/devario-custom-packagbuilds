# GLib for Shelly

Based on [Arch's glib2 recipe](https://gitlab.archlinux.org/archlinux/packaging/packages/glib2/-/blob/main/PKGBUILD),
this builds `2.90.0-1` as `glib2`, `glib2-devel`, and `glib2-docs`.
The main package explicitly provides `libglib-2.0.so=0-64` and the corresponding
versioned provisions for Gio, GIRepository, GModule, GObject, and GThread.
Packaging verifies each ELF64 library's `.so.0` SONAME.

Keep both patches, all four hooks, and both public keys with the recipe. The
signed upstream tag remains verified; GVDB is checked out at the parent source's
submodule commit from the already retrieved local repository. `prepare()` does
not need an additional network fetch.

The included Arch-packaged keys have primary fingerprints:

```text
53EF3DC3B63E2899271BD26322E8091EEA11BBB7  Emmanuele Bassi
923B7025EE03C1C59F42684CF0942E894B2EAFA0  Philip Withnall
```

From this repository's root, as the Remora worker account, import the keys
before invoking Shelly:

```sh
gpg --import ./devario-core/glib2/*.asc
shelly build --isolated --check ./devario-core/glib2/PKGBUILD
```

For 2.90.0, the signed tag and Git archive BLAKE2 checksum were verified.
Both patches apply, and preparation checks out GVDB at the release's pinned
submodule commit without network access. Bash syntax, makepkg and Shelly
metadata generation, and Meson configuration with all recipe options passed.
Shelly review reported no findings. Documentation tooling was extracted into
`/tmp` for the configuration check; no host packages were installed.

Full compilation, tests, and package generation have not been rerun for 2.90.0.
The previous 2.88.3 native Shelly build passed 398 tests with seven skipped,
produced all three split archives, and confirmed all six ABI provisions in
the runtime archive's `.PKGINFO`.

Use a build path without the substring `valid`: upstream's markup
test checks that substring in the entire fixture filename to decide whether XML
should be valid. The standard isolated path `/build/work/...` avoids this issue.

See [the dependency build guide](../../DEPENDENCY-BUILDS.md) for build ordering,
isolated-build limits, and publishing the updated ABI provision.
