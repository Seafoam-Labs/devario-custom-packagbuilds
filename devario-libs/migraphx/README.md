MIGraphX packaging notes (2026-11-01)

The native recipe is MIGraphX 7.2.3, package release 8. It no longer builds
rocMLIR inline. The pinned compiler comes from `devario-libs/rocmlir`, which
builds the same rocMLIR tree with `BUILD_FAT_LIBROCKCOMPILER=ON` and installs
`librockCompiler.a`, its headers, and `rocmlir-config.cmake` under `/opt/rocm`.
MIGraphX finds `rocMLIR::rockCompiler` through `rocMLIR_DIR` and links the
static archive into `libmigraphx_gpu.so`. `rocmlir` is therefore a makedepend,
not a runtime dependency; `hsa-rocr` remains a runtime dependency through the
exported target.

Device code is built for `gfx11-generic` and `gfx12-generic` instead of the
complete `rocm-supported-gfx` list. This follows `rocsolver` and
`composable-kernel`, which already use `gfx11-generic`. The generic targets
cover gfx1100-1103 and gfx1150-1153, and gfx1200/1201. Review the supported
GPU set before widening or narrowing that list; `GPU_TARGETS` becomes one
`--offload-arch` per entry in the device library.

The recipe still disables tests, Python bindings, Composable Kernel
integration, hipBLASLt integration, and LTO. The local patch guards a
hipBLASLt-specific call so the disabled integration can build. A clean build
now measures only the MIGraphX host and device stages; the multi-hour
LLVM/MLIR compiler build happens once in `rocmlir`, not on every `migraphx`
pkgrel. The observed clean build before the split was 3h45m on the Ryzen 7
3800X with 96 GB RAM, almost all of it the compiler stage.

MIOpen 7.2.4 pins the same rocMLIR commit: tags `rocm-7.2.2` and `rocm-7.2.3`
are the same tree, and that is the tree MIGraphX 7.2.3 selects. MIOpen can
adopt the `rocmlir` package in a follow-up; it still builds its own compiler
until that change is validated.

The temporary workaround is the standalone
[`import-arch-migraphx.fish`](../../scripts/import-arch-migraphx.fish) script.
It imports the unchanged Arch `migraphx-7.2.3-7-x86_64.pkg.tar.zst` archive,
matching the local recipe version. Arch's package metadata lists an archive
size of about 66 MB. The importer checks package name, version, and
architecture, prints dependencies, preserves other repository entries, and
signs and verifies the package, database, and files archive with the Devario
key before publishing. Compatible runtime dependencies, including MIOpen
and protobuf, must be available; the script does not install them.

Run on the Remora host with Fish, curl, GnuPG, bsdtar, Shelly, systemctl, and
the usual coreutils installed. The worker account needs repository write
access and the existing Devario signing key. From this checkout:

```fish
sudo install -m 644 scripts/import-arch-migraphx.fish /var/lib/remora/
and sudo systemctl stop remora.service
and sudo -u remora-worker env --chdir=/var/lib/remora \
    HOME=/var/lib/remora \
    GNUPGHOME=/var/lib/remora/.gnupg \
    XDG_CONFIG_HOME=/var/lib/remora/.config \
    SKIP_ARCH_SIGNATURE=1 \
    fish /var/lib/remora/import-arch-migraphx.fish \
    /srv/repositories/devario-libs/x86_64/devario-libs.db.tar.gz \
    BB62CD2725FD8E25558F900A84F94F672976872C
```

Use the existing repository database's compression suffix if it is `.xz` or
`.zst`. The example explicitly skips Arch signature verification to work
around the builder's invalid-packet Arch keyring error. Remove
`SKIP_ARCH_SIGNATURE=1` to require it. Devario signing and verification
always run; re-signing does not establish Arch provenance when verification
of the Arch signature was skipped.

The script updates only the pacman repository archives. Remora's SQLite
state and build status are managed separately by the DB admin. After the
import succeeds, have the admin record the binary import and resolve any
superseded MIGraphX jobs. Then run `sudo systemctl start remora.service`
and request the normal mirror sync. An imported binary should not be
recorded as a successful native compilation.

Downloads are cached under `/var/lib/remora/.cache/devario-arch-stopgap` with
the environment above. The worker stays stopped if the import fails; fix
the reported error and rerun to reuse the cache. If a publication rename
fails partway through, the script retains and prints the staging directory
for recovery. No automatic Remora database edits or mirror uploads occur.
