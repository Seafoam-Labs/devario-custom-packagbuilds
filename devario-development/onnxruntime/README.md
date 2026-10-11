ONNX Runtime packaging notes (2026-10-11)

The current recipe is ONNX Runtime 1.29.0, package release 5. Devario builds
one CPU, one CUDA, and one ROCm/MIGraphX variant. Each produces a native
library package and a Python package, for six outputs from three builds:

- `onnxruntime-cpu` and `python-onnxruntime-cpu`.
- `onnxruntime-cuda` and `python-onnxruntime-cuda`.
- `onnxruntime-rocm` and `python-onnxruntime-rocm`.

All variants explicitly target the `x86-64-v3` CPU baseline, including CUDA
host compilation through NVCC. That baseline already includes AVX2 and FMA,
so the separate `-opt-cuda` and `-opt-rocm` builds and their `-march=haswell`
overrides were removed. The remaining CUDA and ROCm packages provide,
conflict with, and replace the corresponding retired names. CUDA also
retains migration support for the older `onnxruntime-opt` and
`python-onnxruntime-opt` names.

The CUDA build now uses exactly:

```text
CMAKE_CUDA_ARCHITECTURES=75-real;86-real;89-real;120-real
```

These four targets cover the requested GeForce RTX 20, 30, 40, and 50
generations. The table records the previous twelve native targets and the
selection made for this package. The numbers are GPU compute capabilities,
independent of the `x86-64-v3` host CPU baseline.

| Target | NVIDIA architecture and example products | Explicit target retained? |
| --- | --- | --- |
| `75` | Turing: GeForce RTX 20 series, T4 | Yes: RTX 20 coverage |
| `80` | Ampere: A100, A30 | No: data-center target |
| `86` | Ampere: GeForce RTX 30 series, RTX A6000 | Yes: RTX 30 coverage |
| `87` | Ampere: Jetson AGX Orin, Orin NX/Nano | No: Jetson target |
| `88` | Ampere variant; no product identified in NVIDIA's public GPU table | No: outside requested coverage |
| `89` | Ada: GeForce RTX 40 series, RTX 6000 Ada, L4/L40 | Yes: RTX 40 coverage |
| `90` | Hopper: H100, H200 | No: data-center target |
| `100` | Blackwell: B200, GB200 | No: data-center target |
| `103` | Blackwell: B300, GB300 | No: outside requested GeForce coverage |
| `110` | Blackwell: Jetson Thor T4000/T5000 | No: Jetson target |
| `120` | Blackwell: GeForce RTX 50 series, RTX PRO Blackwell | Yes: RTX 50 coverage |
| `121` | Blackwell: GB10 / DGX Spark | No: outside requested GeForce coverage |

Product mappings come from [NVIDIA's compute-capability table](https://developer.nvidia.com/cuda/gpus).
The Ampere classification of `88` is documented in the
[NVCC architecture reference](https://docs.nvidia.com/cuda/archive/13.2.0/cuda-compiler-driver-nvcc/index.html#gpu-feature-list).
A target can serve multiple product classes: retaining `75`, `86`, `89`,
and `120` is motivated by GeForce coverage, but also includes products that
share those compute capabilities. Removing an explicit target is not a
claim that every associated device is necessarily binary-incompatible.

The `-real` suffix requests native machine code for each selected target.
The former `121-virtual` entry, which requested PTX, was also removed. This
configuration requests no explicit PTX fallback for future GPU generations;
review and rebuild the target list when adding new hardware. The retained
set is not a universal NVIDIA target, and the removed data-center and
embedded targets are outside the intended package coverage.

This reduces the architecture-specific CUDA compilation workload, while
consolidation removes an entire duplicate CUDA build and a duplicate
ROCm/MIGraphX build. Build time does not scale directly with target count:
host compilation, shared dependencies, linking, and packaging still remain.
No full-build timing has been measured for the reduced configuration.

Training and Python support remain enabled, and unit tests remain disabled
in the recipe. The AMD variants use the installed MIGraphX dependency with
Composable Kernel disabled; this change does not alter their GPU selection.
The required dependency packages must be installed before building. Future target
changes should preserve the intended hardware coverage and be validated
with the resulting package on representative GPUs, in addition to checking
the generated CUDA architecture flags.

## Temporary Arch binary import

[`scripts/import-arch-onnxruntime.fish`](../../scripts/import-arch-onnxruntime.fish)
imports exactly the six packages listed above, pinned to Arch `1.29.0-3`.
Downloads total about 905 MB and are cached for resumable retries. Dependencies
are printed for review but are not imported automatically. All six alternatives
can be hosted in one repository; clients choose their backend according to the
packages' conflicts and dependencies.

The archives retain Arch's CPU flags, GPU targets, dependencies, and package
metadata. This stopgap does not incorporate the custom v3 baseline, four CUDA
targets, or `opt` replacement metadata described above. Existing `opt` repository
entries are preserved and need a separate migration decision. Keep the imported
release at `1.29.0-3`; the native `1.29.0-5` supersedes it when rebuilt. Clients
already running a newer package will not automatically downgrade.

Run these commands on the Remora host, from this checkout. The example uses
`devario-development`, where this recipe lives. Pass the actual existing database
path if this host publishes ONNX Runtime elsewhere (including `devario-libs`),
and use its actual `.gz`, `.xz`, or `.zst` suffix.

```fish
sudo systemctl stop remora.service
sudo install -o remora-worker -m 0644 scripts/import-arch-onnxruntime.fish /var/lib/remora/import-arch-onnxruntime.fish

sudo -u remora-worker env --chdir=/var/lib/remora \
    HOME=/var/lib/remora \
    GNUPGHOME=/var/lib/remora/.gnupg \
    XDG_CONFIG_HOME=/var/lib/remora/.config \
    SKIP_ARCH_SIGNATURE=1 \
    fish /var/lib/remora/import-arch-onnxruntime.fish \
    /srv/repositories/devario-development/x86_64/devario-development.db.tar.gz \
    BB62CD2725FD8E25558F900A84F94F672976872C
```

`SKIP_ARCH_SIGNATURE=1` bypasses upstream Arch signature verification. Set it to
`0` to require verification with `/usr/share/pacman/keyrings/archlinux.gpg`.
Either way, the script checks each archive's package name, version, and
architecture, signs all six unchanged archives with the supplied Devario key,
and builds and verifies signed `.db` and `.files` archives before publishing.
The worker account must have repository write access and access to that signing
key. The script requires Fish, curl, GPG, bsdtar, Shelly, systemctl, and coreutils.
Allow several GB of free space for the download cache and repository staging.

Keep other repository writers and mirror syncs paused during import. Publication
uses individual file renames, not one atomic transaction; remaining staged files
are retained for recovery if publication fails. Other package entries are
preserved. The script does not edit Remora's SQLite database or build status.
After a successful import, have the DB administrator reconcile the six artifacts
and the stopgap status for this recipe before restarting `remora.service` and
requesting the normal mirror sync, so the native build is not immediately
requeued.
