# readline for Shelly

Based on [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/readline/-/blob/main/PKGBUILD),
this recipe builds `readline 8.3.6-2` with explicit `libreadline.so=8-64` and
bare `libreadline.so` provisions. The packaging function checks the installed
library's ELF64 class and SONAME before accepting the declared ABI.

Source checksums and upstream build settings are retained, as is signature
verification where present in Arch's recipe. Arch's `inputrc` is bundled. All six upstream point patches and their signatures remain in the source list. The progress message uses `printf` so Shelly does not need makepkg's `msg2` helper.

Copy the whole directory to the worker. For signed sources, the invoking builder
account must have the release keys listed in `validpgpkeys` in its GPG keyring.

From the repository root:

```sh
shelly build --review-only --json ./readline/PKGBUILD
shelly build --isolated --check ./readline/PKGBUILD
```

Bash syntax, generated `.SRCINFO`, and any bundled source checksums passed
validation. The ABI helper accepted the installed host library and rejected a
wrong SONAME. Shelly review completed with warnings about dynamic shell expressions or Makefile variables in the retained upstream inputs; see [the ABI build guide](../ABI-BUILDS.md).
A full package build and upstream test run have not been performed.

See [the ABI build guide](../ABI-BUILDS.md) for build order and publication.
