# Fluxer Canary binary package

This recipe packages the Linux Canary tarballs published in
[Fluxer's package repository](https://pkgs.fluxer.com), using the download
endpoints documented in the [upstream repository](https://github.com/fluxerapp/fluxer).
Both x86_64 and aarch64 builds use versioned URLs and verified SHA-256 checksums.

`.nvchecker.toml` tracks the version in the `Content-Disposition` header of
the latest published x64 Canary tarball. Run `nvchecker -c .nvchecker.toml`
from this directory to check for updates. When updating, confirm that both
architecture tarballs are published, update `pkgver` and both checksums,
reset `pkgrel` to `1`, and regenerate `.SRCINFO`:

```sh
shelly build --makesrcinfo ./PKGBUILD > .SRCINFO
```

The build uses the pinned release; checking for updates does not modify the
recipe automatically.
