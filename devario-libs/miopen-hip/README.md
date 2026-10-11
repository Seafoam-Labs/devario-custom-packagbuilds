MIOpen packaging notes (2026-10-11)

The native recipe is ROCm 7.2.4, package release 1. Every clean build currently
builds frugally-deep, rocMLIR 7.2.2, half, and then MIOpen. In particular,
rocMLIR is built in Release mode with `BUILD_FAT_LIBROCKCOMPILER=ON` and staged
into the temporary dependency prefix. MIOpen uses the targets returned by
`rocm-supported-gfx -e gfx1010,gfx1012,gfx1153`; it does not inherit the reduced
six-target list from the hipBLASLt recipe. Tests are removed during prepare
because they require an AMD GPU, and LTO is disabled.

On the Ryzen 7 3800X builder with 96 GB RAM, the earlier 3–6 hour clean-build
estimate was a planning estimate, not a measurement. The repeated compiler
build is the reason for the Arch binary stopgap. Future rebuilds need rocMLIR
packaged separately, with its installed compiler library and CMake metadata
reused by MIOpen. Verify ABI, runtime library packaging, and ROCm version
compatibility when doing that split. Then measure the remaining MIOpen build,
review its GPU coverage, and retain reusable build stages where upstream
supports them. Reducing GPU targets alone does not remove the rocMLIR build.
This restructuring has not been implemented in the PKGBUILD.

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
