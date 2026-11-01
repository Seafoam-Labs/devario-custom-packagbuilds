MIOpen packaging notes (2026-11-01)

The native recipe is ROCm 7.2.4, package release 2. Every clean build now
builds frugally-deep, half, and then MIOpen; the pinned rocMLIR compiler comes
from `devario-libs/rocmlir`. Tags `rocm-7.2.2` and `rocm-7.2.3` point at the
same rocMLIR commit, so MIOpen's previous 7.2.2 pin and MIGraphX's 7.2.3 pin
resolve to the same package. MIOpen finds `rocMLIR::rockCompiler` through
`rocMLIR_DIR=/opt/rocm/lib/cmake/rocmlir` and links the static archive into
`libMIOpen.so`; `rocmlir` is a makedepend, and the package copies the rocMLIR
and LLVM notices because that code is redistributed in the binary.

MIOpen builds device code for `gfx11-generic` and `gfx12-generic` instead of
the 20-entry `rocm-supported-gfx -e gfx1010,gfx1012,gfx1153` list, the same
coverage decision `migraphx` carries: gfx1100-1103 and gfx1150-1153 for the
first target, gfx1200/1201 for the second. `GPU_TARGETS` becomes one
`--offload-arch` per entry and MIOpen links `hip::device` into the library, so
the arch list multiplied every translation unit's compile; the four
`ck_header_only` layernorm instances are the only sources that emit device
code. Tests are removed during prepare because they require an AMD GPU, and
LTO is disabled.

The earlier 3–6 hour clean-build estimate on the Ryzen 7 3800X with 96 GB RAM
was a planning estimate, not a measurement. The multi-hour LLVM/MLIR compiler
build now happens once in `rocmlir`, not on every MIOpen pkgrel. Measure the
remaining MIOpen build and validate the installed package with representative
model compilation and inference on the retained GPUs.

Use [`import-arch-miopen-hip.fish`](../../scripts/import-arch-miopen-hip.fish)
to import `miopen-hip-7.2.4-1-x86_64.pkg.tar.zst` from the Arch Linux Archive.
The package is pinned to the recipe's ROCm version, rather than following
whatever version happens to be latest. The Arch archive is about 291 MB and
is imported unchanged, so its GPU targets and build options remain Arch's.
Its ROCm dependencies must already be available at compatible versions; the
script prints the declared dependencies but does not install or rebuild them.

Run on the Remora host with Fish, curl, GnuPG, bsdtar,
Shelly, systemctl, and the usual coreutils installed. The worker account must
have write access to the repository and access to the existing Devario signing
key. This is a standalone script; Remora's SQLite state and build status are
managed separately by the DB admin. From this repository checkout, run:

```fish
sudo install -m 644 scripts/import-arch-miopen-hip.fish /var/lib/remora/
and sudo systemctl stop remora.service
and sudo -u remora-worker env --chdir=/var/lib/remora \
    HOME=/var/lib/remora \
    GNUPGHOME=/var/lib/remora/.gnupg \
    XDG_CONFIG_HOME=/var/lib/remora/.config \
    SKIP_ARCH_SIGNATURE=1 \
    fish /var/lib/remora/import-arch-miopen-hip.fish \
    /srv/repositories/devario-libs/x86_64/devario-libs.db.tar.gz \
    BB62CD2725FD8E25558F900A84F94F672976872C
```

Use the existing repository database's compression suffix if it is `.xz` or
`.zst`. The example explicitly bypasses Arch signature verification because
the builder's Arch keyring failed with an invalid-packet error during the
hipBLASLt import. Remove `SKIP_ARCH_SIGNATURE=1` to require Arch verification.
Devario package and database signing and verification always run. Devario
re-signing does not establish Arch provenance when Arch verification is skipped.

The script checks package name, version, and architecture, stages the updated
repository database while preserving other entries, and signs and verifies
the package, database, and files archive before publishing. It updates the
pacman repository archives only; it does not read or write `remora.db`, change
build jobs, or request mirror synchronization.

After a successful import, have the DB admin record the Arch binary import in
Remora and resolve any superseded MIOpen jobs before restarting the worker.
Preserve the distinction between an imported binary and a successful native
build. Then run `sudo systemctl start remora.service` and request the normal
mirror sync. If the web service was stopped during earlier attempts, restart
it with `sudo systemctl start remora-web.service` as well.

Downloads are cached under `/var/lib/remora/.cache/devario-arch-stopgap` with
the environment above. The worker stays stopped if the import fails. Rerun
after correcting the error to reuse the download cache. If a file rename
fails partway through publication, the script prints the retained staging
directory for recovery.
