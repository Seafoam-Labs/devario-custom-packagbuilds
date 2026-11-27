# PolyStrata

`polystrata` packages [PolyStrata](https://github.com/simplexai-labs/PolyStrata),
a fork of [Strata](https://github.com/Niko1221/Strata) that runs large MoE models
(Qwen3.8-Flash-Next, GLM 5.3 Flash, DeepSeek V4 Flash, Inkling 2 and more) on an
NVIDIA or AMD GPU through its `strata-poly` engine. The recipe follows the
[AUR `polystrata` recipe](https://aur.archlinux.org/packages/polystrata); see
`DEVARIO-UPSTREAM.json` for the pinned AUR revision and the local changes.

This directory holds `PKGBUILD`, the generated `.SRCINFO`, the launcher source
`polystrata.sh`, and this README. Nothing is compiled at package time, so the
recipe is `arch=('any')` and the build tools are runtime dependencies: the
engine has to be built for the specific GPU on the specific machine.

## What the package installs

```
/opt/polystrata                    the tagged upstream tree (terminal/, engine/, docs/, setup.sh)
/usr/bin/polystrata                launcher -> ~/PolyStrata + upstream ./setup.sh
/usr/bin/polystrata-update         symlink to polystrata; runs ./setup.sh --update
/usr/share/licenses/polystrata/     upstream MIT LICENSE
```

The upstream release asset for Linux is a source snapshot, and its
`setup.sh`/`setup.py` write their venv, the compiled engine and the model files
next to themselves without root. The package therefore ships a read-only tree
under `/opt` and a launcher that copies it into `~/PolyStrata` on the first run
(or when the package version changes), then runs upstream's own `setup.sh`
there. `POLYSTRATA_HOME` moves that location; a folder that already exists
there but was not created by the package is left alone.

## First run

`polystrata` sets up if needed and then starts the server; later runs just
start it. It needs the network and a lot of disk: the venv pulls its Python
packages (and NVIDIA's CUDA wheels) from PyPI, and the model files are tens of
GB. `gcc`, `git` and, for NVIDIA, `cuda` are needed only when the engine is
compiled:

| Dependency       | Role                                                            |
|------------------|-----------------------------------------------------------------|
| `python`         | the private venv (3.10+, `ensurepip`)                            |
| `gcc`, `git`     | engine build on this PC                                          |
| `cuda` (opt)     | NVIDIA engine; upstream builds with CUDA 13.0                     |
| `rocm-hip-sdk`   | AMD engine through a system ROCm 7 in `/opt/rocm`; otherwise ROCm is downloaded into the venv on first start |

On x86-64 Linux with an NVIDIA driver 580 or newer, upstream's `setup.py` first
tries a ready-made CUDA 13 engine rather than compiling. Its release asset is
named after a hash of the engine and vision sources in the checkout, so the
packaged tree has to be the exact tagged source. That is verified for the pin
here: replaying `terminal/setup.py:source_hash()` over this tag's source
snapshot gives `b616a87312ca9b34` (engine), `7ab3349c0a9d9b7b` (vision) and
`a5588664228fc21e` for the pair, which are exactly the hashes in
`strata-poly-linux-x64-cuda13-a5588664228fc21e.tar.gz` and its `BUILD.json`
(sm_75/80/86/89/120). Re-run that check after a version bump if you want the
first run to skip the compile; with a mismatch upstream falls back to building
the engine for your card.

The launcher also guards `POLYSTRATA_HOME`: a folder already there that has no
version stamp (for example a plain `git clone`) is left alone and `polystrata`
exits with an error until the folder is removed or `POLYSTRATA_HOME` points
elsewhere. This is a local hardening of the AUR launcher, which only warned
and then ran that folder's own `setup.sh`.

Upstream quirks worth knowing, both one-time: the first AMD start can report
"ROCm was installed but its compiler is missing" while it unpacks its
toolchain — run `polystrata` again — and the engine compile needs scratch space
in `/tmp`, which on a small tmpfs surfaces as a "broken CXX compiler".

## Build and install

From this directory:

```sh
shelly build --reviewed ./PKGBUILD
shelly install standard ./polystrata-*.pkg.tar.zst
```

The package build downloads only the two `source=()` entries; the network work
happens when the user runs `polystrata`, not during the build.

## Updating

1. Set `_tag` to the upstream tag and reset `pkgrel`; `pkgver` (hyphens
   replaced by dots) and the extracted-tree paths in `package()` derive from
   `_tag`.
2. Re-hash the sources: `shelly build --updpkgsums PKGBUILD` rewrites the
   `sha256sums` in `PKGBUILD` and in `.SRCINFO`. `polystrata.sh` needs no
   change — its version stamp comes from `@@PKGVER@@`/`@@PKGREL@@` in
   `prepare()`.
3. Regenerate the metadata file: `printf 'y\n' | shelly build --makesrcinfo
   PKGBUILD >.SRCINFO`.

Sources: [PolyStrata v0.2.20-poly.6](https://github.com/simplexai-labs/PolyStrata/releases/tag/v0.2.20-poly.6),
[terminal quick start](https://github.com/simplexai-labs/PolyStrata/blob/v0.2.20-poly.6/docs/TERMINAL_QUICKSTART.md),
[install notes](https://github.com/simplexai-labs/PolyStrata/blob/v0.2.20-poly.6/docs/INSTALL.md).
Upstream is MIT licensed; the recipe files are 0BSD (see `REUSE.toml`), and
`polystrata.sh` is the AUR launcher with one local change: the
unmanaged-directory guard exits instead of running that folder's `setup.sh`.
