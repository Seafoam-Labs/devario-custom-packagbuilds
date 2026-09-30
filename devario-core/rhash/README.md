# rhash for Shelly

Based on [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/rhash/-/blob/main/PKGBUILD), pinned to `1.4.6-2`. Copy the whole directory to the worker, including local patches and `keys/` where present.

Explicitly provides `librhash.so=1-64` for Shelly and checks the installed ELF class and SONAME. Retains upstream command-line and library tests and signed-source verification.

The permitted upstream signing fingerprints are:

- `2875F6B1C2D27A4F0C8AF60B2A714497E37363AE`

Import the supplied public keys as the build account after checking these fingerprints:

```sh
gpg --import rhash/keys/pgp/*.asc
```

From the repository root:

```sh
shelly build --review-only --json ./rhash/PKGBUILD
shelly build --isolated --check ./rhash/PKGBUILD
```

Bash syntax, generated metadata, source checksums, applicable signatures, and source preparation were validated. makepkg and Shelly metadata agree. See [the Zig build guide](../ZIG-BUILDS.md) for build order, bootstrap dependencies, review findings, and the exact limits of local build validation.
