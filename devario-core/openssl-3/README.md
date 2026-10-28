# OpenSSL 3.5 LTS compatibility package for Shelly

Based on [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/openssl-3/-/blob/main/PKGBUILD),
this recipe builds `openssl-3 3.5.9-1`: the 3.5 LTS headers, import libraries,
pkg-config files and CMake package config, installed under
`/usr/include/openssl-3` and `/usr/lib/openssl-3`. Arch's source pin, release
signature verification, `Configure` options and header-path rewrites are retained
unchanged. The recipe has no test phase; `build()` runs `make build_libs` only.

## Deviation from upstream

Arch wrote this recipe for the OpenSSL 4 transition, where `openssl` carries the
`libcrypto.so.4` SONAME. Its `package()` moves `libcrypto.so.3` and
`libssl.so.3` into `/usr/lib` and repoints the dev symlinks at `../`. Devario's
[openssl](../openssl/PKGBUILD) is still `3.6.5` and already owns both paths, so
this recipe leaves the 3.5 libraries where `install_dev` puts them, inside
`/usr/lib/openssl-3`, and keeps the `libcrypto.so -> libcrypto.so.3` symlinks
`install_dev` created. The staged tree then contains nothing under `/usr/lib`
except `openssl-3/`, so the two packages install side by side.

Because no library from this package lands on the loader path, upstream's
`provides=('libcrypto.so' 'libssl.so')` is dropped as well. Fourteen published
`devario-core` packages depend on bare `libcrypto.so` and eight on bare
`libssl.so`; leaving the claim in place would let pacman satisfy them with a
package that does not expose either name. The versioned `libcrypto.so=3-64` and
`libssl.so=3-64` provisions stay with `openssl` alone.

Consumers take the include and library directories from
`/usr/lib/openssl-3/pkgconfig` (upstream's `sed` rewrites) and record
`NEEDED libcrypto.so.3`, which the loader satisfies from `openssl` at runtime.
Revert both deviations when `openssl` moves to the 4.x ABI, at which point
upstream's relocation into `/usr/lib` becomes correct here too.

## Building

Copy the whole directory to the worker. `validpgpkeys` trusts the OpenSSL release
key `B146647E45A7B33947AB226B2A2C87D161692D40`, already required by the `openssl`
recipe, so the account invoking the builder needs no new key import.

From this repository's root:

```sh
shelly build --review-only --json ./devario-core/openssl-3/PKGBUILD
shelly build --isolated --check ./devario-core/openssl-3/PKGBUILD
```

Publish the archive and refresh the worker's repository database before building
anything that names `openssl-3`. Upstream `python` does, and configures its `_ssl`
module with `PKG_CONFIG_PATH=/usr/lib/openssl-3/pkgconfig`.

## Validation

Shelly 3.1.9 review completed with no findings, and `bash -n` passed.
`.SRCINFO` was generated with `shelly build --makesrcinfo` and diffs against
Arch's copy only by the two removed `provides` lines. The source checksum was
recomputed from the release tarball and matches the pin; the detached signature is
verified against it.

A host probe build was performed: `Configure` with the recipe's exact options,
`make depend build_libs`, then the recipe's own `package()` run with `pkgdir`
pointed at a scratch directory. It produced `/usr/lib/openssl-3/libcrypto.so.3`
(real 7.7 MB ELF64) with `libcrypto.so -> libcrypto.so.3` beside it, the same for
`libssl`, nothing else in `/usr/lib`, headers at
`/usr/include/openssl-3/openssl/`, and both `sed` rewrites applied; the recipe's
`_verify_soname` guard passed on both libraries. A probe program compiled against
that staged tree linked to `NEEDED libcrypto.so.3`/`libssl.so.3`, resolved both
from `/usr/lib` at runtime, and ran.

A full `shelly build --isolated` and publication have not been performed; the
recipe is not yet in any Devario repository.
