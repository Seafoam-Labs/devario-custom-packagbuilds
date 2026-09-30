# libgcrypt for Shelly isolated builds

This recipe builds `libgcrypt 1.12.4-2`, based on
[Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/libgcrypt/-/blob/main/PKGBUILD).

The release's `.sig` file contains two signatures:

| Signer | Primary fingerprint |
| --- | --- |
| Werner Koch | `6DAA6E64A76D2840571B4902528897B826403ADA` |
| Niibe Yutaka | `AC8E115BF73E2D8D47FA9908E98E9B2D19C6C8BD` |

Arch's recipe lists only Werner's key. Shelly exports only the keys listed in
`validpgpkeys` into the isolated root, leaving Niibe's signature without a key.
This recipe lists both signers and includes both public keys, exported from
[GnuPG's published release-key bundle](https://gnupg.org/signature_key.asc).
Both signatures were verified against the unchanged release tarball. The
original source checksum and signature verification remain enabled.

Import **both keys as the account that invokes Shelly** (the Remora worker
account for automated builds), after checking their fingerprints above:

```sh
cd libgcrypt
gpg --import ./6DAA6E64A76D2840571B4902528897B826403ADA.asc \
             ./AC8E115BF73E2D8D47FA9908E98E9B2D19C6C8BD.asc
shelly build --review-only --json ./PKGBUILD
shelly build --isolated --check ./PKGBUILD
```

Importing into root's or pacman's keyring does not populate the invoking user's
source-signing keyring. `validpgpkeys` identifies allowed keys; it does not itself
import them. Importing from `prepare()` would be too late because source
verification runs first. For unattended Remora builds, do the import once before
launching the build. Upload the directory together so both key files and these
instructions are available alongside the PKGBUILD.

The recipe declares autotools and documentation build dependencies, retains
Arch's disabled static library and PadLock support, and keeps its two test
exclusions (`t-secmem` and `t-sexp`) for systemd/libseccomp chroots. Other upstream
tests remain enabled. Libtool metadata is removed as with makepkg's default
`!libtool` cleanup.

Validation:

- Reproduced `MissingPgpKey` using Arch's recipe with only Werner's key.
- Shell syntax, `.SRCINFO` generation, and Shelly review passed (no findings).
- Shelly's native unprivileged builder verified the sources and produced
  `libgcrypt-1.12.4-2-x86_64.pkg.tar.zst`. Upstream reported 39 tests passed and
  two large-data tests skipped, in addition to Arch's two exclusions above.
  Testing used a fresh keyring containing exactly the two listed keys, matching
  the public keys available to the isolated guest.
- The packaged library and pkg-config metadata report version `1.12.4`; a
  SHA-256 known-answer test against the packaged library passed.

Full isolated nspawn verification remains unavailable locally because Shelly's
privileged coordinator requires an interactive sudo password. Run the isolated
command above on the Remora worker. No host packages were installed for testing.
