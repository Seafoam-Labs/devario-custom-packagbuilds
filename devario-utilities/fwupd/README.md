# fwupd

Imported whole from Arch at `2.1.9-1` (provenance in `DEVARIO-UPSTREAM.json`).
Source is a signed git tag, key `163EB50119225DB3DF8F49EA17ACBA8DFA970E17`,
Richard Hughes <richard@hughsie.com>. Split outputs: `fwupd`, `fwupd-docs`.

Deviations from the upstream recipe:

  - `package_fwupd()` declares `libfwupd.so=3-64` next to the bare provision and
    probes the installed ELF64/SONAME, so Shelly carries the pinned form.
  - `makedepends` names `gnu-efi` instead of `gnu-efi-libs`: this tree ships
    gnu-efi 4.x as one package that replaces the Arch split.

Dependency notes at import time (2026-11-16, live databases):

  - `pandoc` resolves through the published `pandoc-bin` (devario-core).
  - The bare `.so` depends (`libcurl.so`, `libmm-glib.so`, `libqmi-glib.so`)
    resolve against published providers; `libpassim.so` comes from
    `devario-utilities/passim`, imported in the same pass and unpublished, so it
    stays bare until passim publishes.
  - `fwupd-efi` is a runtime depend, imported alongside in
    `devario-utilities/fwupd-efi`.

Validation: `shelly build --review-only` on the host; no isolated worker build
has run, so the build itself is unverified here.