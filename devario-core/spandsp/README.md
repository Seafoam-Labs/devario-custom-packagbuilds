# spandsp for Shelly

This recipe builds spandsp `0.0.6-6`, replacing the failing soft-switch.org
download with Fedora's HTTPS lookaside cache. The archive matches the SHA-512
in [Arch's original recipe](https://github.com/archlinux/svntogit-packages/blob/packages/spandsp/trunk/PKGBUILD).
TLS certificate verification and source checksum verification remain enabled.
The MD5-shaped component of the Fedora URL is only a cache locator.

The recipe keeps the 0.0.6 release and its `libspandsp.so.2` ABI. It selects
GNU C17 explicitly so the old source builds with recent GCC versions that
default to C23.

Release 6 adds both `libspandsp.so` and `libspandsp.so=2-64` provisions for
PipeWire consumers. Packaging checks the installed library's ELF64 class and
`libspandsp.so.2` SONAME. Publish the rebuilt archive and refresh the repository
database; editing `.SRCINFO` alone does not fix dependency resolution.

Copy this directory to the Remora worker and use its PKGBUILD in place of
`/var/lib/remora/build/devario-core/spandsp/PKGBUILD`. From this repository's root:

```sh
shelly build --review-only --json ./devario-core/spandsp/PKGBUILD
shelly build --isolated --check ./devario-core/spandsp/PKGBUILD
```

Validated locally: HTTPS download with certificate verification, SHA-512 match,
Bash syntax, generated `.SRCINFO`, Shelly review (no findings), compilation with
GCC 16, and staged installation. The installed library has SONAME
`libspandsp.so.2`. `make check` succeeds, but the default upstream configuration
does not enable its optional test programs. An isolated Remora build has not
been run here.

Release 6 additionally passed a local makepkg build and `make check`; its
archive's `.PKGINFO` contains `libspandsp.so=2-64`. Makepkg expands the bare
provision to the same versioned value, whereas Shelly preserves the explicit
bare and versioned entries.
