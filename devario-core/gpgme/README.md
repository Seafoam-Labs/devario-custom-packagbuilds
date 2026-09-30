# gpgme for Shelly

Based on [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/gpgme/-/blob/main/PKGBUILD),
this recipe builds `gpgme 2.2.0-2` with explicit `libgpgme.so=45-64` and
bare `libgpgme.so` provisions. The packaging function checks the installed
library's ELF64 class and SONAME before accepting the declared ABI.

Source checksums and upstream build settings are retained, as is signature
verification where present in Arch's recipe. 
Copy the whole directory to the worker. For signed sources, the invoking builder
account must have the release keys listed in `validpgpkeys` in its GPG keyring.

From the repository root:

```sh
shelly build --review-only --json ./gpgme/PKGBUILD
shelly build --isolated --check ./gpgme/PKGBUILD
```

Bash syntax, generated `.SRCINFO`, and any bundled source checksums passed
validation. The ABI helper accepted the installed host library and rejected a
wrong SONAME. Shelly review completed without findings.
A full package build and upstream test run have not been performed.

See [the ABI build guide](../ABI-BUILDS.md) for build order and publication.
