# GLib for Shelly

Based on [Arch's glib2 recipe](https://gitlab.archlinux.org/archlinux/packaging/packages/glib2/-/blob/main/PKGBUILD),
this builds `2.88.3-2` as `glib2`, `glib2-devel`, and `glib2-docs`.
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

As the Remora worker account, import the keys before invoking Shelly:

```sh
gpg --import ./glib2/*.asc
shelly build --isolated --check ./glib2/PKGBUILD
```

Source verification and a native Shelly build succeeded: 398 tests passed and
seven were skipped. All three split archives were produced, and the runtime
archive's `.PKGINFO` contains all six explicit ABI provisions.

Use a build path without the substring `valid`: upstream's markup
test checks that substring in the entire fixture filename to decide whether XML
should be valid. The standard isolated path `/build/work/...` avoids this issue.

See [the dependency build guide](../DEPENDENCY-BUILDS.md) for build ordering,
isolated-build limits, and publishing the updated ABI provision.
