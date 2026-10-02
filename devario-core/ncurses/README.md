# ncurses for Shelly

Based on [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/ncurses/-/blob/main/PKGBUILD),
this recipe builds `ncurses 6.6-4` with explicit `libncursesw.so=6-64` and
bare `libncursesw.so` provisions. The packaging function checks the installed
library's ELF64 class and SONAME before accepting the declared ABI.

The package excludes `/usr/share/terminfo/g/ghostty`, which is owned by
`ghostty-terminfo` in Devario. This lets both packages install together when
Shelly provisions the Aqueous session build root.

Source checksums and upstream build settings are retained, as is signature
verification where present in Arch's recipe. Both required Arch patches are bundled. The other ncurses library provisions and linker scripts are retained.

Copy the whole directory to the worker. For signed sources, the invoking builder
account must have the release keys listed in `validpgpkeys` in its GPG keyring.

From the repository root:

```sh
shelly build --review-only --json ./ncurses/PKGBUILD
shelly build --isolated --check ./ncurses/PKGBUILD
```

Bash syntax, generated `.SRCINFO`, and any bundled source checksums passed
validation. The ABI helper accepted the installed host library and rejected a
wrong SONAME. Shelly review completed with warnings about dynamic shell expressions or Makefile variables in the retained upstream inputs; see [the ABI build guide](../ABI-BUILDS.md).
A full package build and upstream test run have not been performed.

See [the ABI build guide](../ABI-BUILDS.md) for build order and publication.
