MIGraphX packaging notes (2026-10-11)

The native recipe is MIGraphX 7.2.3, package release 7. Each clean build first
builds rocMLIR at commit `6671a1ee31d44e1f2f7743a26a71ffc4ce9169bf`, selected
from MIGraphX's upstream requirements. It enables `BUILD_FAT_LIBROCKCOMPILER`
and disables shared libraries, builds the static compiler and its required
LLVM/MLIR components, then installs them into a temporary dependency prefix.
Only after that does it configure and compile MIGraphX. Installing the
MIOpen binary does not supply or skip this separate compiler build.

The recipe already disables tests, Python bindings, Composable Kernel
integration, hipBLASLt integration, and LTO. The local patch guards a
hipBLASLt-specific call so the disabled integration can build. GPU targets
still come from the complete `rocm-supported-gfx` output.

The earlier estimate for a clean build on the Ryzen 7 3800X with 96 GB RAM
was 2–5 hours of compilation and linking, assuming SSD storage, about 16
parallel jobs, and installed dependencies. That was a planning estimate,
not a benchmark; downloads and isolated-root preparation are additional.

Future native rebuilds need the rocMLIR compilation separated from MIGraphX:

1. Package the compatible pinned rocMLIR static compiler, headers, CMake
   metadata, and any libraries needed by downstream linking. Confirm that
   the exported `rocMLIR::rockCompiler` target works from an installed prefix.
2. Change MIGraphX to depend on that package and find its installed CMake
   configuration. Remove the bundled rocMLIR checkout, `build-mlir` stage,
   and temporary dependency-prefix wiring once the external package is
   validated. Adjust license installation to preserve the notices needed
   for compiler code statically linked into the resulting package.
3. Check whether MIOpen can consume the same compiler package by comparing
   its required revision and build options. Do not assume arbitrary rocMLIR
   versions or the libraries bundled inside a MIOpen binary are compatible.
4. Review GPU coverage separately. Reducing `GPU_TARGETS` can reduce device
   compilation, but does not remove the bundled LLVM/MLIR compiler stage.
5. Measure each stage on the builder and validate the installed package with
   representative model compilation and inference on the retained GPUs.
   Keep backend changes separate from the dependency split so regressions
   can be attributed to the relevant change.

This restructuring is not implemented in the current PKGBUILD. Installing
several output packages from the same monolithic build would still repeat
the expensive compiler build; its artifacts must become reusable inputs.

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
