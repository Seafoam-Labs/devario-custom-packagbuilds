# python-setuptools for Shelly

Based on [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/python-setuptools/-/blob/main/PKGBUILD), pinned to `1:84.0.0-2`. Copy the whole directory to the worker, including local patches and `keys/` where present.

Retains epoch `1`, upstream devendoring, and the no-isolation test patch. The unused alternate Python-interpreter bootstrap branch was removed. This is a regular rebuild and requires existing Python build, installer, and setuptools packages.

Arch's downloaded recipe had a mismatched Git-source checksum. The replacement BLAKE2 checksum was calculated only after verifying the `v84.0.0` release tag, which resolves to `72e919a8b10aaafc041205d4e3ae0e6a2e1e5f87`, against Jason R. Coombs' key `CE380CF3044959B8F377DA03708E6CB181B4C47E`. The recipe now requires this signature on every source verification and has release `2`.

The permitted upstream signing fingerprints are:

- `CE380CF3044959B8F377DA03708E6CB181B4C47E`

Import the supplied public keys as the build account after checking these fingerprints:

```sh
gpg --import python-setuptools/keys/pgp/*.asc
```

From the repository root:

```sh
shelly build --review-only --json ./python-setuptools/PKGBUILD
shelly build --isolated --check ./python-setuptools/PKGBUILD
```

Bash syntax, generated metadata, source checksums, applicable signatures, and source preparation were validated. makepkg and Shelly metadata agree. See [the Zig build guide](../ZIG-BUILDS.md) for build order, bootstrap dependencies, review findings, and the exact limits of local build validation.
