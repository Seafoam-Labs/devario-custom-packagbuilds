# JSON-GLib for Shelly

Builds `json-glib` and `json-glib-docs` 1.10.8-2, adapted from
[Arch packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/json-glib/-/blob/main/PKGBUILD).
The runtime package explicitly provides `libjson-glib-1.0.so=0-64`, satisfying
libgusb's dependency. Packaging verifies the library is ELF64 with SONAME
`libjson-glib-1.0.so.0`. The release number is incremented for the corrected
package metadata.

Keep the included upstream signing key with the recipe. Its fingerprint is
`53EF3DC3B63E2899271BD26322E8091EEA11BBB7` (Emmanuele Bassi).
From the repository root, as the worker account:

```sh
gpg --import ./devario-core/json-glib/*.asc
shelly build --review-only --json ./devario-core/json-glib/PKGBUILD
shelly build --isolated --check ./devario-core/json-glib/PKGBUILD
```

Publish the rebuilt json-glib package and refresh the repository database
used by the worker before retrying libgusb. Updating the recipe or `.SRCINFO`
alone does not update the binary repository's library provisions.

Validation: signed source verification, source checksum, Bash syntax,
makepkg/Shelly metadata generation, and Shelly review passed with no
findings. A native makepkg build passed all 18 test targets and produced
both split archives. The runtime archive's `.PKGINFO` contains
`provides = libjson-glib-1.0.so=0-64`, and its library has the expected
SONAME. Temporary copies of missing build tools were used without
installing host packages. An isolated worker build remains unverified.
