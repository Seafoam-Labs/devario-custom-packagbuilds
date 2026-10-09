# Shelly/RLPM hook audit — 2026-10-08

For every package added or updated in commit `8a82447`, use [the commit build order](LATEST-BUILD-ORDER.md): 1,321 outputs from 900 affected recipes, individually listed in stages and labeled by change type.

The audit checked **1,250 local recipe directories** and **66 bundled hook
files from 30 recipes**, plus rebuild-detector's generated upstream hook.
Two older recipes still installed hooks under the legacy directory; those
are corrected. The new application recipes already installed their package
hooks under RLPM.

## Devario's hook contract

The active configuration in
[devario-os/packages/devario-base/shelly.conf](../Devario/devario-os/packages/devario-base/shelly.conf)
and both ISO transaction configurations specifies:

```ini
HookDirMode = Replace
HookDir = /usr/share/rlpm/hooks/
HookDir = /etc/shelly.d/hooks/
```

Package hooks belong in `/usr/share/rlpm/hooks`. Shared hook helpers belong
in `/usr/share/rlpm/scripts`, and each hook's `Exec` must point to the installed
helper or an ordinary command supplied by its dependencies. Hooks retain the
compatible `[Trigger]`/`[Action]` format, including `NeedsTargets` where needed;
their commands do not need a `shelly` wrapper.

`Replace` removes the default hook search directories. The administrator
directory comes last, preserving filename overrides and `/dev/null` masks.
The [Devario boot recipe](devario-installer/devario-boot/PKGBUILD) uses these
masks for superseded kernel/initramfs hooks. The ISO builder generates the
same order with paths inside its isolated target root.

## Recipes to rebuild

| Recipe | Release | Correction |
| --- | --- | --- |
| [Neovim](devario-development/neovim/PKGBUILD) | 0.12.5-2 | Install `nvimdoc.hook` and its helper under RLPM; update `Exec` to the native helper path. |
| [Texinfo](isolation-builder/texinfo/PKGBUILD) | 7.3-2 | Install both documentation-index hooks under RLPM. |
| [TeX Live collections](devario-utilities/texlive-texmf/PKGBUILD) | 2026.1-3 | Keep collection metadata installation, hook targets, and helper reads together under `/var/lib/texmf/devario/installedpkgs`. |

The changed local-file checksums, release numbers, and `.SRCINFO` files are
updated. Rebuild the TeX Live collection outputs together so their shared
metadata path remains consistent. These changes have not been published.

The historical `shelly-storage-migrate` utility still contains legacy paths
for migration and rollback. The active base recipe does not package or enable
that utility; those references are not active hook installation destinations.
Likewise, rebuild-detector's preparation step mentions the old hook directory
as the text to replace in its upstream Makefile. Its staged package was verified
to install `/usr/share/rlpm/hooks/rebuild-detector.hook`.

## Verification

- Six package hook-layout tests passed, including staged Neovim and Texinfo
  hook installation and a TeX Live collection/helper fixture. Application
  compilation commands are stubbed in the Neovim and Texinfo fixtures.
- Twelve ISO builder tests passed, including replacement of default hook
  directories and administrator override order.
- The `devario-os` storage migration tests passed, including fresh base-package
  staging; they do not activate migration on the host.
- All three changed recipes passed metadata, shell syntax, local checksums,
  and Shelly review parsing. The 908-recipe expansion report remains passing.

Run `python tests/test-hook-layout.py` to repeat the local hook checks. The
[audit summary](audits/hook-layout-2026-10-08/summary.json),
[hook inventory](audits/hook-layout-2026-10-08/hooks.json), and
[recipe validation](audits/hook-layout-2026-10-08/validation.json) retain the
evidence. The inventory covers checked-in recipe material; full rebuilt
archives and the published binary repositories still need their file-path
audit before deployment, as `devario-os` already does during ISO staging.
