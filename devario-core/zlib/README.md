# zlib for Shelly isolated builds

This recipe builds `zlib`, `zlib-static`, and `minizip` version `1:1.3.2-4`,
based on [Arch's zlib packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/zlib/-/blob/main/PKGBUILD).

The checksum failure comes from GitHub's generated patch for commit
`36ff1be48ef696cc67b0855f7c8537ce0276210d`. Its `index` line now uses ten-character
Git object hashes; changing just those abbreviations back to nine characters
reproduces **both of Arch's original SHA-512 and BLAKE2 checksums exactly**.
The code change still only adds the missing `ints.h` to minizip's installed
headers.

The matching patch is bundled as `minizip-install-ints-h.patch`, eliminating the
unstable patch download. All original checksums and release signature
verification remain enabled. The recipe declares the autotools dependencies,
builds minizip against the newly built zlib, and installs the static library
directly so split packaging does not depend on function order. It also removes
libtool metadata containing temporary build paths.

Upload `PKGBUILD` and `minizip-install-ints-h.patch` together into Remora. Import
the bundled release key as the builder account after checking its fingerprint
against `validpgpkeys`:

```sh
cd zlib
gpg --import 5ED46A6721D365587791E2AA783FCD8E58BCAFBA.asc
shelly build --review-only --json ./PKGBUILD
shelly build --isolated --check ./PKGBUILD
```

Validation:

- Release signature verified; source and bundled patch matched both original
  checksum sets.
- Shell syntax and `.SRCINFO` checks passed. Shelly review completed with
  dynamic-command warnings for Makefile variable syntax in the patch.
- Shelly's native unprivileged builder produced all three package archives.
- Upstream zlib static, shared, and 64-bit tests passed; minizip's archive
  creation/extraction/comparison test passed.
- Programs built against the packaged shared and static libraries reported
  zlib 1.3.2 and passed compression/decompression round trips. Packaged minizip
  headers compiled, including the restored `ints.h`; package contents were
  checked for the intended library split.

Full isolated nspawn verification remains unavailable locally because Shelly's
privileged coordinator requires an interactive sudo password. Run the isolated
command above on the Remora worker. No host packages were installed for testing.
