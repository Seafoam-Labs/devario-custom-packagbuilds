# colord

Imported whole from Arch at `1.4.8-2` (provenance in `DEVARIO-UPSTREAM.json`).
Source is a signed git tag, key `163EB50119225DB3DF8F49EA17ACBA8DFA970E17`,
Richard Hughes <richard@hughsie.com>.

Deviation from the upstream recipe, one mechanism:

  - `build()` adds `-D pnp_ids=/usr/share/hwdata/pnp.ids` and `prepare()` applies
    `0002-quirk-pnp-ids-vendor-name.patch`, so EDID vendor names resolve from
    hwdata instead of a compiled udev hwdb, which build roots never have. The
    patch is what keeps the fallback path quirked like the hwdb path, so both
    answer `LG` and not `LG Electronics`. `hwdata` joins the runtime depends of
    `colord` and `libcolord`.

Validation: on the host, `1.4.8` built with `lib/colord` and its tests (daemon,
sane, vapi and docs off, since this machine has no argyllcms, vala or sane)
passes the suite with the deviation, and still passes with `/usr/lib/udev`
masked to reproduce a worker root, where the same masked run without the
deviation aborts `/colord/edid` on `NULL == "LG"`. `shelly build --review-only`
reports no findings. No `--isolated` worker build has run, so the full option
set is unverified here; published `colord` is still the seed `1.4.8-1`.

`devario-libs/lib32-colord` runs the same `check()` and carries the same gap.
