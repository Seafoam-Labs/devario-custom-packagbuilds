# NSS for Shelly isolated builds

This recipe builds `nss` and `ca-certificates-mozilla` 3.130-2, based on
[Arch's NSS packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/nss/-/blob/main/PKGBUILD).

Arch uses an `hg+https` Mercurial source, which Shelly rejects with
`UnsupportedSourceProtocol`. This recipe uses Mozilla's HTTPS release archive
for the same `NSS_3_130_RTM` release instead. Its pinned SHA-256 digest matches
[Mozilla's published checksums](https://archive.mozilla.org/pub/security/nss/releases/NSS_3_130_RTM/src/SHA256SUMS).
The source paths account for the archive's extra `nss-3.130` directory.

Arch's system-NSPR patch and certificate conversion scripts are included
unchanged and checksummed. The recipe preserves system NSPR/SQLite use, libpkix,
the p11-kit trust-module symlink, and the separate Mozilla CA package. GYP,
Ninja, OpenSSL, Perl, pkgconf, and Python are declared build dependencies.
Scripts are invoked through their interpreters so uploaded executable modes
are not required.

Upload **all four build inputs** together into Remora:

- `PKGBUILD`
- `0001-Fix-generating-nss.pc-with-system-nspr.patch`
- `bundle.sh`
- `certdata2pem.py`

Then run:

```sh
cd nss
shelly build --review-only --json ./PKGBUILD
shelly build --isolated ./PKGBUILD
```

Validation:

- Reproduced `UnsupportedSourceProtocol` with Arch's original recipe.
- Shell syntax, `.SRCINFO` generation, and Shelly review completed. Review
  flags command substitutions in Arch's patch as dynamic commands.
- Shelly's native unprivileged builder verified the source checksums and built
  both package archives with GCC 16.2.1.
- The packaged `certutil` created and read a temporary SQL certificate database.
- The packaged NSS library reported version 3.130, initialized, generated random
  bytes, and shut down successfully. Headers, pkg-config metadata, and the
  p11-kit symlink were checked.
- OpenSSL parsed the generated bundle's 172 certificates successfully.

Local testing used a signature-verified Arch GYP package extracted under `/tmp`;
no host packages were installed. The isolated worker installs the declared
dependencies normally. NSS's full upstream test suite remains disabled, matching
Arch's recipe; the checks above are smoke tests. Full nspawn verification remains
unavailable locally because Shelly's coordinator requires an interactive sudo
password in this environment.
