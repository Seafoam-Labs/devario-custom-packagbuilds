# jxrlib

Imported whole from Arch at `1.4.7-1` (provenance in `DEVARIO-UPSTREAM.json`).
The git tag `1.4.7` resolves to `0e9a58411bc876a2737963c54748cfc40744a326`, and
`shelly build --updpkgsums` reproduces Arch's source checksum
`3786acfb9f99c57adc310a94e999f1044ae205d4d9555917383d55c05c2e02fa`.

Deviations from the upstream recipe:

  - `package()` strips `$pkgdir` from `libjxr.pc` instead of the hardcoded
    `/build/jxrlib/pkg/jxrlib`. The Makefile bakes `DIR_INSTALL` (the staged
    `$pkgdir/usr`) into `prefix=`, and Arch's literal sed only matches Arch's
    own makepkg root; anywhere else it is a no-op and the shipped pkg-config
    file points into the build root.
  - `makedepends` drops `cmake` and adds `python`. The build is plain make;
    cmake is never invoked. The Makefile's `libjxr.pc` rule runs `python -c`
    during `make install`, so python is needed at the package stage and must
    be a makedepend for clean build roots.
  - `.nvchecker.toml` drops `prefix = "v"`: upstream tags are bare versions
    (`1.4.7`, not `v1.4.7`), so the prefixed checker matches nothing.

Validation: the recipe's own `prepare`/`build`/`package` ran on the host
against the `1.4.7` tag; with the verbatim sed the installed `libjxr.pc`
keeps `prefix=<build root>/usr`, with the portable sed it reads `prefix=/usr`
and passes `pkg-config --validate`.
`shelly build --review-only` reports no findings and `--makesrcinfo`
reproduces the committed `.SRCINFO`. No isolated worker build has run.