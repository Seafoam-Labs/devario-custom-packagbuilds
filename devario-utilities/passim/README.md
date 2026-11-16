# passim

Imported whole from Arch at `0.1.13-1` (provenance in `DEVARIO-UPSTREAM.json`).
Source is a signed git tag, key `163EB50119225DB3DF8F49EA17ACBA8DFA970E17`,
Richard Hughes <richard@hughsie.com>.

Deviation from the upstream recipe, one mechanism:

  - `package()` declares `libpassim.so=1-64` next to the bare provision and
    probes the installed ELF64/SONAME, so Shelly carries the pinned form.
    `fwupd` names `libpassim.so` bare until this package publishes.

All other depends and makedepends resolve against published providers
(glib2, libsoup3, avahi, cmake, systemd, gobject-introspection).

Validation: `shelly build --review-only` on the host; no isolated worker build
has run, so the build itself is unverified here.