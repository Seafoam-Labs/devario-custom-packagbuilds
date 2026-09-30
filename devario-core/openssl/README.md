# OpenSSL for Shelly

Based on [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/openssl/-/blob/main/PKGBUILD),
this recipe builds `openssl 3.6.4-2` with explicit library provisions:

```bash
provides=('libcrypto.so' 'libcrypto.so=3-64' 'libssl.so=3-64')
```

The packaging function checks both installed libraries for ELF64 and the
corresponding `.so.3` SONAME. Arch's source checksums, release signature
verification, build options, and upstream tests are retained. The required
`ca-dir.patch` is bundled with its original checksum.

Copy the entire directory to the worker. The account invoking the builder must
have the release signing key available in its GPG keyring; allowed fingerprints
are listed in `validpgpkeys` in the PKGBUILD.

From this repository's root:

```sh
shelly build --review-only --json ./openssl/PKGBUILD
shelly build --isolated --check ./openssl/PKGBUILD
```

After building, publish the resulting package and refresh the repository
database so dependency resolution sees the new provisions.

Validation: Bash syntax and `.SRCINFO` generation passed, and the bundled
patch matches its declared SHA-256 checksum. Shelly review completed with only
warnings about Arch's `$(nproc)` test parallelism. A full build and upstream
test run have not been performed.
