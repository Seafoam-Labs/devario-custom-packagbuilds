# zstd for Shelly

Based on [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/zstd/-/blob/main/PKGBUILD),
this recipe builds `zstd 1.6.0-1` with explicit `libzstd.so=1-64` and
bare `libzstd.so` provisions. The packaging function checks the installed
library's ELF64 class and SONAME before accepting the declared ABI.

Source checksums and upstream build settings are retained, as is signature
verification where present in Arch's recipe. The upstream manpage patch
(`6af3842118ea5325480b403213b2a9fbed3d3d74`, an upstream commit cherry-picked
to fix the 1.5.7 manpages) is no longer bundled: it is part of the released
1.6.0 sources, so re-applying it would be redundant and could conflict with
the new context.

Copy the whole directory to the worker. For signed sources, the invoking builder
account must have the release keys listed in `validpgpkeys` in its GPG keyring.

From the repository root:

```sh
shelly build --review-only --json ./zstd/PKGBUILD
shelly build --isolated --check ./zstd/PKGBUILD
```

Bash syntax, generated `.SRCINFO`, and any bundled source checksums passed
validation. The ABI helper accepted the installed host library and rejected a
wrong SONAME. Shelly review completed with warnings about dynamic shell expressions or Makefile variables in the retained upstream inputs; see [the ABI build guide](../ABI-BUILDS.md).
A full package build and upstream test run have not been performed.

See [the ABI build guide](../ABI-BUILDS.md) for build order and publication.
