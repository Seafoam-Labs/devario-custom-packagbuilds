# NSS for Shelly isolated builds

This recipe builds `nss` and `ca-certificates-mozilla` 3.131.1-1, based on
[Arch's NSS packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/nss/-/blob/main/PKGBUILD).

Arch uses an `hg+https` Mercurial source, which Shelly rejects with
`UnsupportedSourceProtocol`. This recipe uses Mozilla's HTTPS release archive
for the `NSS_3_131_1_RTM` security release instead. Its pinned SHA-256 digest matches
[Mozilla's published checksums](https://archive.mozilla.org/pub/security/nss/releases/NSS_3_131_1_RTM/src/SHA256SUMS).
The source paths account for the archive's extra `nss-3.131.1` directory.

Arch's certificate conversion scripts are included unchanged and checksummed.
The recipe preserves system NSPR/SQLite use, libpkix, the p11-kit trust-module
symlink, and the separate Mozilla CA package. GYP, Ninja, OpenSSL, Perl, pkgconf,
and Python are declared build dependencies. Scripts are invoked through their
interpreters so uploaded executable modes are not required.

Upload **all three build inputs** together into Remora:

- `PKGBUILD`
- `bundle.sh`
- `certdata2pem.py`

Then run:

```sh
cd nss
shelly build --review-only --json ./PKGBUILD
shelly build --isolated ./PKGBUILD
```

Security update (2026-10-21):

- NSS 3.131.1 includes Mozilla's trust-store response to the
  [eMudhra intermediate-certificate compromise](https://blog.mozilla.org/security/2026/10/20/protecting-firefox-users-following-the-compromise-of-emudhra-intermediate-certificates/).
- Compared with 3.131, the release removes `emSign ECC Root CA - G3`,
  `emSign Root CA - C1`, and `emSign ECC Root CA - C3` from its built-in trust
  data. The latter two removals are also documented in
  [Mozilla bug 2083709](https://bugzilla.mozilla.org/show_bug.cgi?id=2083709).
- This recipe produces both `nss` and `ca-certificates-mozilla`. Publish both:
  the Mozilla CA split package supplies the system trust data used through
  p11-kit. The companion `devario-libs/lib32-nss` recipe is also updated to
  3.131.1-1.

Validation for 3.131.1-1:

- Downloaded the official 3.131 and 3.131.1 archives and verified their SHA-256
  digests against Mozilla's corresponding `SHA256SUMS` files.
- Regenerated both NSS recipes' `.SRCINFO` files with Shelly; both Shelly
  reviews completed with no findings.
- Ran this recipe's `prepare()`, certificate conversion, bundle generation,
  and `package_ca-certificates-mozilla()` against both versions in temporary
  directories.
- OpenSSL parsed all 169 certificates in the new packaged bundle (previously
  172). SHA-256 fingerprints confirm that exactly the three roots listed above
  disappeared, with all other certificates preserved. The built-in trust data
  version is now 2.92.
- The existing lib32 assembly patch applies to 3.131.1 without fuzz.

Full NSS library compilation, upstream tests, and isolated package builds were
not run for this update; the local environment lacks GYP. Both recipes retain
`--disable-tests`. Verify the isolated builds on Remora before publishing.
