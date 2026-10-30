# Strata Terminal

`strata-bin` packages the official Linux x86_64 Terminal/Control bundle, including
its private Python runtime, under `/opt/strata`. Release **0.2.8** uses Terminal
bundle build **0.1.54**; `strata --version` reports both numbers.
The package provides `strata`, `setup-strata`, and the alias `strata-setup`.
It does not include the desktop GUI, inference engines, or model weights.

## Build and install

From this directory:

```sh
shelly build ./PKGBUILD --reviewed
shelly install standard ./strata-bin-*.pkg.tar.zst
```

Alternatively, use `shelly build ./PKGBUILD --reviewed --install`. Add
`--sync-deps` if dependencies need to be installed.

## Easy NVIDIA setup

The helper is adapted from `~/Documents/setup-strata.sh`. Run it as your normal
user after installing the package and a working NVIDIA driver (580 or newer):

```sh
setup-strata --dry-run
setup-strata --setup-only
setup-strata
setup-strata --status
setup-strata --stop
```

Defaults match the original Ryzen 9950X3D / RTX 5090 32 GB / 128 GB RAM setup:
Qwen3.8-Flash-Next NVFP4, 64K context, one request, GPU vision, GPU 0, no tuning,
and 2560 MiB of VRAM reserved for other applications. The API listens locally
at `http://127.0.0.1:8080/v1`. These are large-model settings; use `strata launch`
for upstream's guided hardware selection, including supported AMD hardware.

```sh
setup-strata --quant q5 --context 128k
setup-strata --vision off --vram-reserve-mib 4096
setup-strata --data-dir /path/to/models --port 8081
setup-strata --help
```

Initial model downloads are approximately 128 GB for NVFP4, 158 GB for Q5,
111 GB for Q4, and 84 GB for IQ3, plus helpers and preparation space. Downloads
resume on rerun. Models default to `${XDG_DATA_HOME:-~/.local/share}/strata/models`;
Strata keeps engine components and run configurations in its user data folders.
`--setup-only` (also `--no-start`) prepares the engine/model without starting a
server and requires `--tune skip`. Package installation itself downloads no models
and starts no services.

The helper uses `/usr/bin/strata` so an existing `~/.local/bin/strata` does not
shadow it. Use `/usr/bin/strata` for direct commands if you also have a user-local
installation; existing user data is retained. `STRATA_BIN=/path/to/strata` can
override the helper's executable. Upgrade the package with Shelly; upstream
`strata update --no-control` updates the user-local engine. Upstream's plain
`strata update` can also install a newer user-local Control, which its launcher
will prefer automatically.

Sources: [Strata v0.2.8](https://github.com/Niko1221/Strata/releases/tag/v0.2.8),
[Terminal launch guide](https://github.com/Niko1221/Strata/blob/v0.2.8/docs/TERMINAL_LAUNCH.md).
The upstream application is MIT licensed; the adapted setup helper retains its
GPL-3.0-or-later license notice. Bundled dependency notices remain in the runtime.
