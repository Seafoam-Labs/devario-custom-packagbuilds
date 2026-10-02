# Ministream for isolated builds

This recipe builds GNOME's `ministream` 0.99.1-1 for Devario, adapted from
[Arch packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/ministream/-/blob/main/PKGBUILD).
Ministream is a lightweight AppStream metadata parser used by libadwaita.

When Shelly prints `ministream` followed by `An AUR dependency step is not
supported in this isolated build`, it has classified ministream as an AUR
dependency. The isolated builder requires this dependency to be available
as a binary package from one of its configured repositories.

Copy this entire directory to the worker. From this repository's root,
import the included upstream signing key as the worker account, then build:

```sh
gpg --show-keys --with-fingerprint ./devario-core/ministream/*.asc
gpg --import ./devario-core/ministream/*.asc
shelly build --review-only --json ./devario-core/ministream/PKGBUILD
shelly build --isolated --check ./devario-core/ministream/PKGBUILD
```

The expected fingerprint for Florian Leander Singer (sp1rit) is:

```text
BBDE032EAAFBFC627FB7E635B1F4055D8460CE34
```

The key comes from Arch's ministream packaging. Source signature verification
remains enabled. Build dependencies include AppStream, GLib development
tools, GObject introspection, libxml2, Meson, Ninja, and pkgconf; make these
available in the worker repositories first.

Publish the resulting `ministream-0.99.1-1-x86_64.pkg.tar.zst` and refresh
the repository database used by Remora/Shelly. Then retry the original
package in a fresh isolated root. Installing ministream on the host alone
does not make it available to that root. If a ministream package is already
published, check the worker's repository configuration and database instead.

## Validation

The 0.99.1 tag signature and Git archive BLAKE2 checksum match the recipe.
Bash syntax, makepkg and Shelly metadata generation, and Shelly review
passed with no findings. A native build, all 12 upstream subtests, and
staged installation passed. The staged library's ELF64/SONAME check confirms
the explicit `libministream.so=1-64` provision. Headers, `ministream.pc`, GIR,
and typelib files are installed. No host packages were installed.

The isolated worker build, package archive generation, and repository
publication have not been performed here.
