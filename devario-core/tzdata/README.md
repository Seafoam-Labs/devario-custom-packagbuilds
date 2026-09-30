# tzdata for Shelly isolated builds

This recipe builds `tzdata 2026d-2`, based on
[Arch's tzdata recipe](https://gitlab.archlinux.org/archlinux/packaging/packages/tzdata/-/blob/main/PKGBUILD).

The `tzcode2026d.tar.gz` and `tzdata2026d.tar.gz` archives share nine identical
files, including `calendars` and `Makefile`. Shelly's automatic extractor rejects
the second copy with `UnsafeSourceArchivePath`. The PKGBUILD marks both archives
as `noextract` and combines them with `tar` in a dedicated directory during
`prepare()`. Both archives retain Arch's SHA-512 checksums and upstream signature
verification. `noextract` changes extraction only.

Upload this directory to Remora. Import the bundled public key as the account
that runs the builder, after checking its fingerprint against `validpgpkeys`:

```sh
cd tzdata
gpg --import 7E3792A9D8ACF7D633BC1588ED97E90E62AA7E34.asc
shelly build --review-only --json ./PKGBUILD
shelly build --isolated --check ./PKGBUILD
```

The public key comes from Arch's packaging repository. Shelly reports an
expired-key warning but successfully verifies both release signatures. That
warning is separate from the extraction failure; verification remains enabled.

Validation:

- Reproduced the exact `calendars` extraction error with Arch's original recipe.
- Shell syntax, `.SRCINFO` generation, and Shelly review passed (no findings).
- Shelly's native unprivileged builder verified both archives and produced
  `tzdata-2026d-2-x86_64.pkg.tar.zst`.
- Upstream `make check` passed with the external HTML validator disabled.
- Checked the main, POSIX, and leap-second zoneinfo trees, release metadata,
  tools, license, and New York winter/summer offsets. `/etc/localtime` is not
  packaged, preserving the administrator's timezone selection.

The full isolated nspawn build remains unverified locally: Shelly's privileged
coordinator requires an interactive sudo password in this environment. Run the
isolated command above on the Remora worker.
