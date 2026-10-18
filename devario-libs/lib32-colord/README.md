# lib32-colord

Arch-verbatim recipe at `1.4.8-1`, plus the same deviation as
`devario-core/colord`: `build()` passes `-D pnp_ids=/usr/share/hwdata/pnp.ids`,
`prepare()` applies `0001-quirk-pnp-ids-vendor-name.patch`, and `hwdata` joins
`depends`. The shared patch file is byte-identical to the one in that recipe.

The libcolord private test resolves an EDID vendor through the udev hwdb, which
no build root has compiled, so an unmodified `check()` aborts on `NULL == "LG"`.

Validation: configured with this recipe's own option set and run with
`/usr/lib/udev` masked, the suite aborts unpatched and passes with the
deviation. That probe ran 64-bit: `-m32` configure here stops at `gusb`, since
this host has no `lib32-libgusb` or `lib32-libgudev` .pc file. No `--isolated`
worker build has run, so the 32-bit suite itself is unverified.

`pkgrel` moves to 2 because published `lib32-colord` is a real `1.4.8-1` build,
not a seed record. This recipe has no committed `.SRCINFO`, so none was
regenerated.
