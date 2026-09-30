# libuv for Shelly

Based on [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/libuv/-/blob/main/PKGBUILD), pinned to `1.53.0-1`. Copy the whole directory to the worker, including local patches and `keys/` where present.

Retains the upstream signed Git tag, Autotools build, documentation, and test exclusions. Version 1.53.0 also requires `python-sphinx-copybutton` to generate documentation; provide it through the bootstrap repository.

The permitted upstream signing fingerprints are:

- `57353E0DBDAAA7E839B66A1AFF47D5E4AD8B4FDC`
- `94AE36675C464D64BAFA68DD7434390BDBE9B9C5`
- `612F0EAD9401622379DF4402F28C3C8DA33C03BE`
- `AEAD0A4B686767751A0E4AEF34A25FB128246514`
- `CFBB9CA9A5BEAFD70E2B3C5A79A67C55A3679C8B`

Import the supplied public keys as the build account after checking these fingerprints:

```sh
gpg --import libuv/keys/pgp/*.asc
```

From the repository root:

```sh
shelly build --review-only --json ./libuv/PKGBUILD
shelly build --isolated --check ./libuv/PKGBUILD
```

Bash syntax, generated metadata, source checksums, applicable signatures, and source preparation were validated. makepkg and Shelly metadata agree. See [the Zig build guide](../ZIG-BUILDS.md) for build order, bootstrap dependencies, review findings, and the exact limits of local build validation.
