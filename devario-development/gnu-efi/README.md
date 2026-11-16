# gnu-efi

Imported whole from Arch at `4.0.4-1` (provenance in `DEVARIO-UPSTREAM.json`),
without deviation. `4.0.4` is the latest upstream release (2025-12-06); the
source tarball's sha512 and b2 checksums were re-verified against GitHub at
review time (2026-11-16).

The single package replaces Arch's historical `gnu-efi-libs` split
(`conflicts`/`provides`/`replaces`), so consumers name `gnu-efi` directly:
`devario-utilities/fwupd`, `devario-utilities/fwupd-efi`,
`devario-utilities/efitools`, `devario-development/sbsigntools`.

Compatibility notes for the fwupd stack:

  - `gnu-efi.pc` carries `efi_machine_type_name` and `gnu_efi_arch`, which
    fwupd-efi 1.9's meson reads; `4.0.4` satisfies its `>= 3.0.18` requirement.
  - 4.x installs `crt0-efi-*.o`, the static libs and linker scripts flat into
    `/usr/lib` (no `gnuefi/` subdir as in 3.0.x); fwupd-efi's meson falls back
    to the pkg-config `libdir` for that layout. Arch ships this exact pair.

State at review: unpublished in every repository, and no legacy `gnu-efi-libs`
provider exists anywhere. Build and publish on the worker before `fwupd-efi`;
`efitools` and `sbsigntools` are also still folder-only.

Validation: `shelly build --review-only` reports no findings and `.SRCINFO`
regenerates identically. No isolated worker build has run, so the build itself
is unverified here.