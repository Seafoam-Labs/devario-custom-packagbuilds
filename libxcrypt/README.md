# libxcrypt for Shelly isolated builds

This recipe builds `libxcrypt` and `libxcrypt-compat` 4.5.2-2, preserving Arch's
hash selection and the `libcrypt.so.2` / `libcrypt.so.1` package split.

The supplied log ends with `crypt-sm3-yescrypt.lo` failing and `cc1: all warnings
being treated as errors`; it does not include the diagnostic before that line.
This recipe addresses both upstream's blanket `-Werror` and the known
glibc 2.43+ const-correctness issue in the SM3/GOST yescrypt wrappers. The latter
fix removes an unnecessary const cast on a writable buffer, as documented by
[Linux From Scratch](https://www.linuxfromscratch.org/lfs/view/13.0-systemd/chapter08/libxcrypt.html).
Warnings remain enabled, and the caller's build flags are preserved.

Sources use the upstream release tarball, Arch's SHA-256 checksum, and the
upstream detached signature. All downloads happen through `source=()`; the build
and test functions need no network access. `perl` is explicitly declared for
source generation and tests inside the isolated root.

Upload this directory to Remora. Import the bundled public key as the account
that runs the builder, after checking its fingerprint against `validpgpkeys`:

```sh
cd libxcrypt
gpg --import 678CE3FEE430311596DB8C16F52E98007594C21D.asc
shelly build --review-only --json ./PKGBUILD
shelly build --isolated --check ./PKGBUILD
```

The bundled key is from Arch's packaging repository. It is now expired, but was
valid when this release was signed; both makepkg and Shelly verified the release
signature during validation. Shelly reports an expired-key warning. Signature
verification has not been disabled.

Validation on GCC 16.2.1 and glibc 2.44:

- `bash -n`, `.SRCINFO` generation, and Shelly review passed (no findings).
- makepkg built both archives with the host's optimization and LTO flags.
- Shelly's native unprivileged builder verified the sources, built both
  archives, and passed both test suites.
- Main library tests: 38 passed, 14 skipped, zero failures.
- Compatibility library tests: 41 passed, 14 skipped, zero failures.

The isolated invocation could not start because its sudo elevation required an
interactive password in this environment. A full nspawn build still needs to
be run on the Remora worker.
