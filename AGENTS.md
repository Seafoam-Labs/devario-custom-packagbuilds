# Devario custom PKGBUILDs

PKGBUILD recipes for the Devario Linux distribution, mostly adapted from the official Arch Linux packaging repositories. Recipes are built and published by the Remora worker (Shelly, a makepkg-compatible builder) to repo.seafoam-labs.org — not on this machine.

## Layout

- One directory per recipe: `PKGBUILD`, generated `.SRCINFO`, local patches/keys, REUSE metadata. Groups: `devario-core`, `devario-libs`, `devario-utilities`, `devario-development`, `devario-browser`, `devario-gaming`, `devario-entertainment`, `devario-productivity`, `devario-theme`, `devario-bleeding-edge`, `devario-scx{,-dev}`, `devario-installer` (see its README), `default/`, `isolation-builder/` (base-devel bootstrap).
- Root guides are the build-order and plan authority: `ABI-BUILDS.md`, `DEPENDENCY-BUILDS.md`, `BUILDER-ORDER.md`, `LATEST-BUILD-ORDER.{md,tsv}`, `HOOK-BUILDS.md`, `MULTILIB-BUILDS.md`, `NATIVE-COMPATIBILITY.md`, `GOOGLE-API-KEYS.md`. `audits/` holds dated snapshots — read each report's scope header before trusting its numbers. `chunks/` (untracked) holds the ordered Arch import batches. `tests/` runs with `python3 tests/<name>.py`.

## Core rules

- Recipes mirror Arch official packaging; a failure is usually dependency drift against current Arch or upstream, not a broken recipe — diff against the upstream packaging repo before patching. Every local deviation gets a one-line comment naming the mechanism.
- Verify locally with `shelly build --review-only --json ./<group>/<recipe>/PKGBUILD`; full `--isolated` builds and publishing happen on the worker. Copy whole recipe directories to the worker (local sources and keys required); import keys as the account that invokes Shelly after checking fingerprints against `validpgpkeys`.
- A PKGBUILD edit that changes metadata regenerates `.SRCINFO` in the same commit. Bump `pkgrel` exactly once per fix and never past a revision that was never published — check what is published first (`https://repo.seafoam-labs.org/api/v1/packages?repository=<id>`; there are fourteen repositories). Every count in this tree's guides and notes is a point-in-time reading; re-query live.
- ABI-critical libraries declare both the bare name and the versioned provision (`libfoo.so` + `libfoo.so=<soname>-64`) with an ELF64/SONAME probe in `package()`; a consumer names the pinned form only after its provider publishes the versioned provision. Keep source checksums and signature verification enabled (`SKIP` only for detached signatures verified against their source).
- Worker builds run `--no-check`: `checkdepends` never enter the dependency plan and are never installed — anything `build()` loads (meson required deps, a Rakefile top-level require) must be in `makedepends`.
- Import hooks and shipped `.hook` files must install to `usr/share/rlpm/hooks`; Arch's `usr/share/libalpm/hooks` path is inert on Devario.
- A new recipe is not done until its licensing trio exists: `REUSE.toml` covering every file, `LICENSE` with the holder on line one, `LICENSES/<SPDX-ID>.txt` per id; `license=()` holds real SPDX identifiers matching upstream.
- Group a recipe by the kind of package it ships, not by what consumes it. Deleting a recipe does not unpublish its package; moving a recipe between groups leaves a duplicate publication — drop the old copy deliberately.
- Never `git add -A` here; stage explicit paths. Recipe files carry pre-existing 100644↔100755 mode drift — keep mode-only changes out of content commits (`git update-index --chmod=-x`). Commit subjects are short and lowercase, naming the package and the mechanism.

## On-demand detail (hidden skills — load with @id)

- `@devario-published-state` — probing the fourteen repos (API vs `.db`, reverse deps, publish lifecycle, provider-first staging).
- `@devario-import-batches` — the `chunks/` generator chain, batch dispatch rules, worker handoff bundles, Arch source-host pitfalls.
- `@shelly-host-probing` — verifying recipes on this workstation (SRCINFO capture, layout probes, toolchain shims).
- `@shelly-worker-environment` — isolated build root quirks and `IncompleteDependencyPlan` triage.
- `@remora-worker` — queueing jobs, host-build option, worker permissions, auto-update behavior.
- `@devario-abi-soname` — pinning decisions, virtual-provide trap, mm-family epoch supersede.
- `@devario-licensing` — REUSE audit scripting, deliberate gaps, license-array parser traps.
- `@devario-rocm-recipes` — GPU_TARGETS mechanics and ROCm build verification.
- `@devario-ruby-recipes` — bundled-gem provides, RubyGems 4 breakages, cycle breaking.
- `@devario-browser-repacks` — NSS trust module, repack payload facts, API-key policy.
- `@devario-settled-decisions` — per-package decisions not to re-propose (cargo, grub, openssl-3, dotnet…).
