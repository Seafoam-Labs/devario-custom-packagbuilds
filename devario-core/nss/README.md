# NSS for Shelly isolated builds

This recipe builds `nss` and `ca-certificates-mozilla` 3.131-1, based on
[Arch's NSS packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/nss/-/blob/main/PKGBUILD).

Arch uses an `hg+https` Mercurial source, which Shelly rejects with
`UnsupportedSourceProtocol`. This recipe uses Mozilla's HTTPS release archive
for the same `NSS_3_131_RTM` release instead. Its pinned SHA-256 digest matches
[Mozilla's published checksums](https://archive.mozilla.org/pub/security/nss/releases/NSS_3_131_RTM/src/SHA256SUMS).
The source paths account for the archive's extra `nss-3.131` directory.

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

Validation:

- Reproduced `UnsupportedSourceProtocol` with Arch's original recipe, which is
  why this recipe keeps the HTTPS archive.
- 3.131 folded Arch's system-NSPR `build.sh` fix upstream, so that patch is no
  longer a source. `patch -Np1 --dry-run` on the 3.131 tree reports the hunk as
  already applied, and `build.sh` guards the local `nspr.pc` read behind
  `no_local_nspr`.
- Shell syntax, `.SRCINFO` generation, and Shelly review completed with no
  findings.
- A host probe ran this recipe's own `prepare()`, `build()`, `package_nss()` and
  `package_ca-certificates-mozilla()` against the 3.131 archive, all cleanly. It
  used a signature-verified Arch GYP package extracted under a temp root; no host
  packages were installed.
- The probe's `nss.pc` reports `Version: 3.131` and satisfies
  `pkg-config --atleast-version=3.131 nss`, the check Firefox 159 fails on 3.130.
  The `mozilla-nss` alias resolves and the file validates.
- Its `Requires: nspr >= 4.40.0` resolves against the published `nspr` 4.40-1,
  whose `nspr.pc` declares `Version: 4.40.0`.
- The packaged NSS libraries carry the expected SONAMEs, the p11-kit trust
  symlink is in place, `certutil` runs, and headers and pkg-config metadata are
  installed.
- OpenSSL parsed the generated bundle's 172 certificates, built from
  `NSS_BUILTINS_LIBRARY_VERSION` 2.90.

The isolated worker build and both package archives still need verification on
Remora. NSS's full upstream test suite remains disabled, matching Arch's recipe;
the checks above are smoke tests. Full nspawn verification remains unavailable
locally because Shelly's coordinator requires an interactive sudo password in
this environment.
