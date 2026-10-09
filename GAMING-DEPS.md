# devario-gaming-meta dependency availability

Working note, 2026-10-09. Delete once every row below is published.

`devario-gaming/devario-gaming-meta` declares 23 depends. This note tracks which an installed
Devario can resolve and what has to be built for the rest. There is no Arch fallback, so an
absent name has to come from this tree.

## How to measure

An installed Devario resolves against all eleven published repositories. One unfiltered request
covers the whole fleet:

    curl -s https://repo.seafoam-labs.org/api/v1/packages

Returns 1488 entries, each with `name`, `version`, `provides` and `repositoryId`. A name resolves
if it equals a `name` or a `provides` entry with any `=version` suffix stripped.
`/api/v1/repositories` lists the repositories with their package counts; the spec is at
`/openapi/v1.json`.

The `repository=` parameter filters by repository **id**, not name. `seafoam-labs`'s id is
`default`, so `?repository=seafoam-labs` returns a bare `[]` that looks like "not indexed" but is
only a wrong parameter.

Counts below were measured 2026-10-09 against an index stamped `2026-10-09T11:01:26Z`.
Re-measure rather than trusting them.

## Availability matrix

`core`, `libs` and `gaming` are `devario-core`, `devario-libs` and `devario-gaming`.

| Dependency | Published | Recipe | Action |
| --- | --- | --- | --- |
| `giflib` | core 6.1.3-3 | `devario-core/giflib` | none |
| `gst-plugins-base-libs` | core 1.28.7-2 | none | none now; not rebuildable, see item 4 |
| `libjpeg-turbo` | core 3.2.0-3 | `devario-core/libjpeg-turbo` | none |
| `libva` | core 2.24.1-1 | none | none now; see item 4 |
| `libxslt` | core 1.1.45-2 | `devario-core/libxslt` | none |
| `mpg123` | core 1.33.7-1 | none | none now; not rebuildable, see item 4 |
| `opencl-icd-loader` | core, via `ocl-icd` 2.3.5-1 | none | none |
| `vulkan-tools` | core 1.4.363.0-1 | `devario-core/vulkan-tools` | none |
| `glfw` | libs 1:3.5.1-1 | `devario-libs/glfw` | none |
| `alsa-plugins` | absent | `devario-libs/alsa-plugins` | build, stage 03 |
| `openal` | absent | `devario-libs/openal` | build, stage 03 |
| `ttf-liberation` | absent | `devario-libs/ttf-liberation` | build, stage 13 |
| `wine-cachyos-opt` | absent | `devario-gaming/wine-cachyos-opt` | build, stage 19 |
| `winetricks` | absent | `devario-gaming/winetricks` | build, stage 20 |
| `protontricks` | absent | `devario-gaming/protontricks` | build, stage 21 |
| `lib32-libva` | absent | `devario-libs/lib32-libva` | build, stage 23 cycle G734, needs seeds |
| `lib32-alsa-plugins` | absent | `devario-libs/lib32-alsa-plugins` | build, stage 24 |
| `proton-cachyos-slr` | absent | `devario-gaming/proton-cachyos-slr` | build, stage 25 |
| `umu-launcher` | absent | `devario-gaming/umu-launcher` | build, stage 25 |
| `lib32-gtk3` | absent | `devario-libs/lib32-gtk3` | blocked, 13 missing recipes |
| `lib32-libjpeg-turbo` | absent | `devario-libs/lib32-libjpeg-turbo` | blocked on `lib32-expat`, `nasm` |
| `lib32-ocl-icd` | absent | `devario-libs/lib32-ocl-icd` | blocked on `lib32-mesa` |
| `lib32-opencl-icd-loader` | absent | provides of `devario-libs/lib32-ocl-icd` | covered by that recipe |

9 resolve today, 10 have a recipe that is not published, and 3 recipes were written for the rest
but are not buildable yet. The final row is not a package of its own; it is a provides of the last
of those 3.

Thirteen `lib32-` names are published: four in `devario-core` (`lib32-gcc-libs`, `lib32-glibc`,
`lib32-libltdl`, `lib32-rust-libs`) and nine in `devario-libs` (`lib32-alsa-lib`, `lib32-attr`,
`lib32-brotli`, `lib32-icu`, `lib32-libdisplay-info`, `lib32-ncurses`, `lib32-opus`,
`lib32-speexdsp`, `lib32-spirv-tools`), against 96 `lib32-*` recipe directories in the tree. None
of the six lib32 names this closure needs is among them.

## Work items

### 1. Builds, in stage order

Each is an existing recipe whose output is unpublished. Build on the worker, publish, refresh the
repository database, then re-query before moving on.

- [ ] stage 03 `devario-libs/alsa-plugins`, also produces `pulseaudio-alsa`
- [ ] stage 03 `devario-libs/openal`, also produces `openal-examples`
- [ ] stage 13 `devario-libs/ttf-liberation`
- [ ] stage 19 `devario-gaming/wine-cachyos-opt`, needs item 2 first
- [ ] stage 20 `devario-gaming/winetricks`
- [ ] stage 21 `devario-gaming/protontricks`
- [ ] stage 23 `devario-libs/lib32-libva`, cycle G734 with `lib32-libglvnd` and `lib32-mesa`, so
      working seeds are required before the stage
- [ ] stage 24 `devario-libs/lib32-alsa-plugins`, which needs `lib32-pipewire` built first because
      that is where its `lib32-jack` dependency comes from
- [ ] stage 25 `devario-gaming/proton-cachyos-slr`
- [ ] stage 25 `devario-gaming/umu-launcher`

### 2. Prerequisites for item 1

Unpublished `depends` and `makedepends` of those ten recipes, from their committed `.SRCINFO`.
`dep` is a runtime dependency of at least one target, `make` is build-time only.

| Package | Kind | Stage | Recipe |
| --- | --- | --- | --- |
| `cabextract` | dep | 01 | `devario-utilities/cabextract` |
| `lsb-release` | dep | 01 | `devario-utilities/lsb-release` |
| `unzip` | dep, make | 01 | `devario-utilities/unzip` |
| `fluidsynth` | make | 02 | `devario-libs/fluidsynth` |
| `libavtp` | make | 02 | `devario-libs/libavtp` |
| `mingw-w64-gcc` | make | 02 | `devario-development/mingw-w64-gcc` |
| `xorg-xrandr` | dep | 02 | `devario-utilities/xorg-xrandr` |
| `lib32-libavtp` | make | 03 | `devario-libs/lib32-libavtp` |
| `lib32-libdrm` | dep | 03 | `devario-libs/lib32-libdrm` |
| `lib32-libxcb` | dep | 03 | `devario-libs/lib32-libxcb` |
| `alsa-plugins` | dep | 03 | `devario-libs/alsa-plugins` |
| `openal` | dep | 03 | `devario-libs/openal` |
| `lib32-libx11` | dep | 04 | `devario-libs/lib32-libx11` |
| `lib32-wayland` | dep | 04 | `devario-libs/lib32-wayland` |
| `lib32-libxext` | dep | 05 | `devario-libs/lib32-libxext` |
| `lib32-libxfixes` | dep | 05 | `devario-libs/lib32-libxfixes` |
| `python-fonttools` | make | 05 | `devario-libs/python-fonttools` |
| `python-pyzstd` | dep | 05 | `devario-libs/python-pyzstd` |
| `python-urllib3` | dep | 05 | `devario-libs/python-urllib3` |
| `python-vdf` | dep | 05 | `devario-libs/python-vdf` |
| `python-xxhash` | dep | 05 | `devario-libs/python-xxhash` |
| `python-xlib` | dep | 06 | `devario-libs/python-xlib` |
| `samba` | make | 06 | `devario-utilities/samba` |
| `python-cbor2` | dep | 07 | `devario-libs/python-cbor2` |
| `maturin` | make | 07 | `devario-core/maturin` |
| `lib32-libsamplerate` | make | 09 | `devario-libs/lib32-libsamplerate` |
| `libgphoto2` | make | 10 | `devario-libs/libgphoto2` |
| `fontforge` | make | 12 | `devario-libs/fontforge` |
| `python-pip` | make | 13 | `devario-libs/python-pip` |
| `zenity` | dep | 16 | `devario-utilities/zenity` |
| `python-pillow` | dep | 18 | `devario-libs/python-pillow` |
| `sane` | make | 18 | `devario-development/sane` |
| `wine` | dep | 19 | `devario-gaming/wine` |
| `winetricks` | dep | 20 | `devario-gaming/winetricks` |
| `lib32-dbus` | make | 22 | `devario-libs/lib32-dbus` |
| `lib32-libglvnd` | make | 23 | `devario-libs/lib32-libglvnd`, also provides `lib32-libgl` (dep) |
| `lib32-libpulse` | make | 23 | `devario-libs/lib32-libpulse` |
| `lib32-mesa` | make | 23 | `devario-libs/lib32-mesa` |

Already published and therefore not work, despite appearing in those `.SRCINFO` files:
`lib32-alsa-lib` and `lib32-speexdsp` and `opencl-headers` and `unixodbc` in `devario-libs`,
`ruby` and `python` in `devario-development`, `gcc-multilib` and `lib32-glibc` in `devario-core`.

### 3. The three written lib32 recipes

`devario-libs/lib32-gtk3` 1:3.24.52-1, `devario-libs/lib32-libjpeg-turbo` 3.2.0-1 and
`devario-libs/lib32-ocl-icd` 2.3.5-1 were added 2026-10-09, each ported from the Arch multilib
pkgbase of the same name and carrying a `DEVARIO-UPSTREAM.json` naming the source commit. Their
local deviations are commented in the recipes; they are not repeated here. None has been built.
Multilib recipes cannot be probed on this machine, whose sandbox blocks 32-bit execution, so all
three need an isolated run on the worker.

- [ ] `lib32-ocl-icd`: only `lib32-mesa` (stage 23) is still missing. Verify its
      `lib32-opencl-icd-loader` provision in the packaged `.PKGINFO`, not just the PKGBUILD.
- [ ] `lib32-libjpeg-turbo`: needs unpublished `lib32-expat` and `nasm`.
- [ ] `lib32-gtk3`: 13 of its 27 depends have no recipe anywhere in the tree, and each carries its
      own lib32 chain, so this is a subtree rather than a list: `lib32-at-spi2-core`,
      `lib32-colord`, `lib32-fribidi`, `lib32-gdk-pixbuf2`, `lib32-libcups`, `lib32-libepoxy`,
      `lib32-librsvg`, `lib32-libxcomposite`, `lib32-libxcursor`, `lib32-libxdamage`,
      `lib32-libxi`, `lib32-libxkbcommon`, `lib32-pango`.
- [ ] `lib32-gtk3`: of its 27 depends, 12 have recipes and none is published: `lib32-cairo`,
      `lib32-fontconfig`, `lib32-glib2`, `lib32-harfbuzz`, `lib32-libgl` (a provides of
      `devario-libs/lib32-libglvnd`), `lib32-libx11`, `lib32-libxext`, `lib32-libxfixes`,
      `lib32-libxinerama`, `lib32-libxrandr`, `lib32-wayland`, `lib32-zlib`. `sassc` is an
      unpublished makedepends.

### 4. Provision and provenance checks

- [ ] Published `libva` 2.24.1-1 advertises `libva.so`, `libva-drm.so`, `libva-glx.so`,
      `libva-wayland.so` and `libva-x11.so` with no SONAME version, and `devario-libs/lib32-libva`
      depends on those bare names. Decide whether to add versioned provisions before building the
      lib32 side, since a bare name in a Devario repository shadows Arch's versioned one and breaks
      resolution for anything expecting `libva.so=2-64`.
- [ ] `gst-plugins-base-libs`, `libva` and `mpg123` are published but have no recipe in this tree,
      and `git log --diff-filter=D` shows none was ever deleted here. 1006 of the 1460 distinct
      published names are in that position, so they came from outside this repository. Record where
      they come from, or import the recipes, before anything depends on rebuilding them.

### 5. Closure verification

- [ ] Re-run the availability query and confirm all 23 names resolve by name or provides.
- [ ] Install `devario-gaming-meta` into an isolated root against the published repositories. This
      is the acceptance test, and it catches a missing provides that name matching would not.
- [ ] Regenerate `LATEST-BUILD-ORDER.md`, `LATEST-BUILD-ORDER.tsv` and `BUILDER-ORDER.md`. They are
      pinned snapshots with hardcoded output and stage counts, so a new recipe belongs in a
      regeneration rather than an inserted row. The meta goes in the last stage, behind everything
      it depends on.

## Open decisions

Settled 2026-10-09: all eleven repositories are enabled on an installed system, there is no Arch
fallback, and `lib32-*` stays in separate recipe directories matching the 93 that were already
there rather than as extra split outputs on the native recipes.

1. **Do the four level-2 `make`-only chains that pull in texlive, samba, ghostscript and the ruby
   doc tooling get built, or are those targets built with a reduced dependency set?** A full
   recursive pass over `depends` and `makedepends` reaches 263 recipes through `wine-cachyos-opt`,
   `fontforge`, `samba` and `ruby-ronn-ng`. That is what the build-order documents track, and it is
   out of scope here.
2. **Does `devario-gaming-meta` keep `wine-cachyos-opt` and `proton-cachyos-slr` as hard depends**,
   given they drag in the `wine` and `mingw-w64-gcc` chains, or should the meta depend on the local
   `wine` and leave the CachyOS variants optional?
3. **How far does the `lib32-gtk3` cascade get taken?** Its 13 missing depends each carry their own
   lib32 chain, which may make it the most expensive item in this closure. The alternative is to
   drop `lib32-gtk3` from the meta and let games that need 32-bit GTK pull it in individually.
