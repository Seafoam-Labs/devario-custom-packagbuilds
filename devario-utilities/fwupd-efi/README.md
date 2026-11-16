# fwupd-efi

Imported whole from Arch at `1.9-1` (provenance in `DEVARIO-UPSTREAM.json`),
without deviation. Source is a signed git tag, keys
`163EB50119225DB3DF8F49EA17ACBA8DFA970E17` (Richard Hughes) and
`0B0B6E494E9D5EFB39180D9A2D192CA624770276` (Mario Limonciello).

The SBAT distro fields keep Arch's values, as the other boot-path recipes in
this tree do (efibootmgr's `EFIDIR=arch`). `gnu-efi` and `python-pefile`
makedepends resolve from `devario-development/gnu-efi` (unpublished at import
time) and the published `python-pefile`. Runtime consumer:
`devario-utilities/fwupd`.

Validation: `shelly build --review-only` on the host; no isolated worker build
has run, so the build itself is unverified here.