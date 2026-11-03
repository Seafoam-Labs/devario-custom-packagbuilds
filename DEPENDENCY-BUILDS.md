# Missing dependency builds for Shelly

Current state of the gaps that block worker builds, plus the rules that explain them.
This is not a log. Dated incident write-ups, worker transcripts and validation trails
live in this file's git history; each recipe records its own deviations in a `PKGBUILD`
comment or its `README.md`.

State was read live on 2026-11-03 against the fourteen x86_64 package databases (3317
records, 3254 distinct names, 6484 provision strings) and the 2111 recipe folders in this
tree. Re-query before acting on any row.

## How a dependency plan fails, and what closes it

- The plan covers every output's global `depends` plus `makedepends`, and those packages'
  hard dependencies. `checkdepends` and `optdepends` never enter it, and a `--no-check`
  build does not install `checkdepends`, so anything a build or package stage actually
  needs must be a `makedepend`. `msgpack-c` died at CMake configure because `gtest` sat
  only in `checkdepends`; `flatpak` needs `socat` at configure time.
- `not_in_repositories` and `not_in_environment` lines naming the same package are one
  missing provider reported twice, not two gaps.
- A `not_in_repositories` name has neither a published package nor a recipe folder here.
  Names that own a folder still plan, because the plan builds them. So the two failure
  shapes need opposite remedies: no folder means import a recipe, a folder means build
  and publish it. The contrast is also the fastest way to tell a plan gap from a recipe
  bug.
- A `libfoo.so=N-64` depend can fail while its provider is pinned only locally. Shelly's
  packager preserves a declared bare `.so` provision as written where Arch's makepkg
  versions it, so the versioned string does not exist until the pinned provider
  publishes. Publish the provider; never loosen the consumer's pin, which is the
  tree-sitter 0.27 break. See [ABI-BUILDS.md](ABI-BUILDS.md).
- `depends+=()` inside `package_*()` is install-time only, so a split pair may name each
  other without a build cycle (`tesseract` and `tesseract-data`, as in Arch).
- A published package can already be unsatisfiable at install time because a `%DEPENDS%`
  name provides nothing anywhere. That takes a new recipe, not a recipe edit.
- Publishing is what closes a gap. Build each split recipe once, publish the outputs that
  pin siblings by exact version together, then refresh the worker's repository database
  before the next stage. Uploading a recipe, or editing `.SRCINFO`, changes nothing
  published.

## Checking state

- Published names, versions and provisions:
  `https://repo.seafoam-labs.org/api/v1/packages?repository=<repo>`, using `default` for
  the `seafoam-labs` repository. `/api/v1/repositories` lists all fourteen with counts.
  Records carry `provides` but **no depends field**, so the API cannot show who consumes a
  name.
- Reverse lookups need the signed databases:
  `https://mirrors.seafoam-labs.org/<repo>/x86_64/<repo>.db` is a gzipped tar of
  `<pkgname>-<pkgver>-<pkgrel>/desc` text blocks (`%NAME%`, `%DEPENDS%`, `%PROVIDES%`),
  not a sqlite file, and `%DEPENDS%` entries are `%DELIM%`-separated inside one line.
- Include all fourteen repositories when checking. `7zip`, `a52dec`,
  `aarch64-linux-gnu-binutils` and `aardvark-dns` are provided only by
  `devario-bleeding-edge`, so a nine-repository check reports them as false gaps.
- The last full publication audit is
  [`audits/devario-core-2026-10-05/report.txt`](audits/devario-core-2026-10-05/report.txt);
  its scope predates the installer and scx groups.

## Open: publish queue for the Wayland substrate, the portal and GameOpti

Five references had neither a published package nor a recipe: `mdbook`,
`python-libevdev`, `geoclue`, `python-sphinxext-opengraph` and `python-py7zr`. Twelve
recipes closed that on 2026-11-03, forked verbatim from the Arch packaging repositories:
the five plus `python-py7zr`'s runtime closure. Eight are byte-identical to upstream;
[mdbook](devario-development/mdbook/PKGBUILD),
[python-inflate64](devario-libs/python-inflate64/PKGBUILD),
[multivolumefile](devario-libs/python-multivolumefile/PKGBUILD) and
[pyppmd](devario-libs/python-pyppmd/PKGBUILD) change only their `license` array to valid
SPDX identifiers, each named in a comment. Of the 90 `depends` and `makedepends` entries
the twelve declare, 83 resolve against packages Devario already publishes and the other 7
are the batch's own edges, so nothing in the queue needs a recipe that does not exist
yet. Nothing is built or published yet.

| Stage | Publish | Unblocks |
| --- | --- | --- |
| 1 | [mdbook](devario-development/mdbook/PKGBUILD) `0.5.4-1`, [python-libevdev](devario-libs/python-libevdev/PKGBUILD) `0.13.1-1`, [geoclue](devario-core/geoclue/PKGBUILD) `2.8.2-2`, [python-sphinxext-opengraph](devario-development/python-sphinxext-opengraph/PKGBUILD) `0.13.0-1`, [python-brotlicffi](devario-libs/python-brotlicffi/PKGBUILD), [python-inflate64](devario-libs/python-inflate64/PKGBUILD), [python-multivolumefile](devario-libs/python-multivolumefile/PKGBUILD), [python-pybcj](devario-libs/python-pybcj/PKGBUILD), [python-pyppmd](devario-libs/python-pyppmd/PKGBUILD), [python-cjkwrap](devario-libs/python-cjkwrap/PKGBUILD) | stage 2 |
| 2 | [wayland](devario-core/wayland/PKGBUILD) `1.26.0-2`, [libinput](devario-core/libinput/PKGBUILD) `1.32.0-2`, [libwacom](devario-core/libwacom/PKGBUILD) `2.20.0-1`, [xdg-desktop-portal](devario-core/xdg-desktop-portal/PKGBUILD) `1.22.1-2`, [python-texttable](devario-libs/python-texttable/PKGBUILD) `1.7.2-1`, [python-py7zr](devario-libs/python-py7zr/PKGBUILD) `1.1.4-1` | stage 3 |
| 3 | [wlroots0.20](devario-core/wlroots0.20/PKGBUILD) `0.20.2-2`, [game-optimization-linux-git](devario-gaming/game-optimization-linux-git/PKGBUILD) | GameOpti |

`python-texttable` sits in stage 2 rather than 1 because its `python-cjkwrap` makedepend
is itself new. `mdbook`'s `cargo` makedepend resolves through published `rust 1:1.99.0-1`.

Published `wayland` is `1.26.0-1` and its `%PROVIDES%` carries only
`libwayland-client.so`, `libwayland-cursor.so`, `libwayland-egl.so` and
`libwayland-server.so`, so [wlroots0.20](devario-core/wlroots0.20/PKGBUILD)'s
`libwayland-client.so=0-64` and `libwayland-server.so=0-64` cannot resolve until stage 2
publishes `1.26.0-2`. It is the only recipe in the tree naming a versioned wayland
provision, so publishing closes both entries with no other consumer affected. Reverting
those two depends to the bare names is the wrong fix.

`libwacom` names `python-libevdev` in `makedepends`, so it is blocked even though no
worker report named it; [xorgproto](devario-core/xorgproto/PKGBUILD) names it only in
`checkdepends` and stays unblocked. `geoclue` reaches the four recipes that advertise it
([webkit2gtk-4.1](devario-development/webkit2gtk-4.1/PKGBUILD),
[webkitgtk-6.0](devario-libs/webkitgtk-6.0/PKGBUILD),
[wpewebkit](devario-libs/wpewebkit/PKGBUILD),
[qt6-positioning](devario-libs/qt6-positioning/PKGBUILD)) through `optdepends` alone, and
its recipe carries `provides=(geoclue2=<pkgver>-<pkgrel>)` as Arch does, so those option
strings resolve once it publishes.

The worker labels the gaming row `devario-gaming/game-optimization-install`; the folder
and pkgbase here are `game-optimization-linux-git`, which installs
`/usr/bin/game-optimization-install-runner` and provides `game-optimization-linux`.

## Open: published packages whose depends nothing provides

Read 2026-11-03 across all fourteen databases. Every row is an install-time gap today,
independent of any worker plan.

Recipe present, output unpublished (12):

| Reference | Consumer |
| --- | --- |
| `hipcub`, `hipfft`, `hiprand`, `hipsolver`, `hipsparse`, `rocalution`, `rocfft` ([devario-libs](devario-libs/) siblings) | `rocm-hip-sdk`, `rocm-hip-libraries` |
| [rocm-opencl-runtime](devario-libs/rocm-opencl-runtime/PKGBUILD) | `rocm-opencl-sdk` |
| [python-fsspec](devario-libs/python-fsspec/PKGBUILD), [python-pyarrow](devario-libs/python-pyarrow/PKGBUILD) | `python-gdal` |
| [python-libevdev](devario-libs/python-libevdev/PKGBUILD) | `libinput-tools` `1.32.0-1` |
| [python-tomli-w](devario-libs/python-tomli-w/PKGBUILD) | `bubblejail-git` |

No recipe anywhere (15):

| Reference | Consumer |
| --- | --- |
| `xf86-input-libinput` | `xorg-server` |
| `lua51-compat53`, `lua52-compat53` | `lua51-luarocks`, `lua52-luarocks` |
| `libwpe`, `wpebackend-fdo` | `gst-plugin-wpe` |
| `vamp-host`, `vamp-plugin-sdk` | `rubberband-vamp` |
| `libpanel` | `sysprof` |
| `liblphobos` | `btdu` |
| `lirc` | `pulseaudio-lirc` |
| `nautilus-python` | `ghostty-nautilus` |
| `perl-dbd-mariadb` | `mariadb-mytop` |
| `python-pyinotify` | `ds-inhibit` |
| `python-cattrs` | `bubblejail-git` |
| `dgop` | `dms-shell` |

`python-strictyaml` also names no provider and owns no recipe. It reaches a plan only as
a `makedepends` of the published [meson](devario-core/meson/PKGBUILD) recipe, so rebuilding
meson is where it bites; its other consumer `python-sphinx-hawkmoth` names it in
`checkdepends`, which stays out of a `--no-check` plan.

## Standing orders

**Qt 6.12.** Publish `qt6-base`, then `qt6-declarative=6.12.0`, then `qt6-tools`, then
`qt6-translations`. An existing translations package must be available to provision the
new base, because base depends on translations. `lrelease` links QtQml through
LinguistProject and TrLib when tools builds QML support, so tools and translations need
declarative at runtime. Publish the matching suite together.

**GGML backends.** [ggml](devario-libs/ggml/PKGBUILD) builds `ggml` plus `ggml-cuda`,
`ggml-vulkan`, `ggml-zendnn` and `ggml-openvino`; publish all five splits together and
rebuild them with the matching GGML release, since the backend packages require that
exact release. Order: `intel-metee` then `igsc`, with `intel-gmmlib` and
`intel-graphics-compiler` independent, then `intel-compute-runtime`, then `openvino`,
then `opencl-clhpp` using published `opencl-headers`, then `ggml` after `zendnn`,
`openvino` and `opencl-clhpp`, then [llama-cpp](devario-development/llama-cpp/PKGBUILD).
GGML builds `GGML_NATIVE=OFF` with runtime CPU dispatch, so the build host does not
restrict the distributed binaries; set `DEVARIO_CUDA_ARCHITECTURES` only to narrow CUDA
deliberately. ZenDNN keeps its private SDK under `/opt/zendnn` so the system oneDNN stays
usable, and OpenVINO ships only the Intel GPU plugin. `llama-cli --list-devices` lists
OpenVINO devices and `GGML_OPENVINO_DEVICE` selects one. Allow 2 to 5 hours for the five
backends plus llama.cpp on a 3800X-class host with dependencies installed, and overnight
for a first Intel GPU compiler or OpenVINO build; start those two one at a time.

**Aqueous desktop.** Build `devario-desktop` from Aqueous's
`packaging/devario/aqueous-desktop/PKGBUILD` and publish its matching splits together.
Pearl's maintained recipes supply `pearl` and `pearl-greeter`, and Pearl provides
`pearl-capture-picker=1` with no recipe here. Publish `devario-system-integration` before
Aqueous `1.0.5-2`; existing ISO installs need its
[one-time adoption](devario-installer/devario-system-integration/README.md) first.

**Everything that used to be a standing order here now has one canonical home:** ISO and
installer build order in [`devario-installer/README.md`](devario-installer/README.md),
ABI-pinned libraries and the mm-family two-generation naming in
[ABI-BUILDS.md](ABI-BUILDS.md), package hook placement in
[HOOK-BUILDS.md](HOOK-BUILDS.md), full stage queues in
[BUILDER-ORDER.md](BUILDER-ORDER.md) and [LATEST-BUILD-ORDER.md](LATEST-BUILD-ORDER.md),
and per-recipe provenance and validation in each recipe's `README.md`.

## Build on the worker

Import the supplied upstream public keys **as the account that invokes Shelly**, after
comparing fingerprints against `validpgpkeys` and the recipe READMEs:

```sh
gpg --import dbus/*.asc glib2/*.asc
```

Review, then build in an isolated root, from the repository root:

```sh
shelly build --review-only --json ./devario-core/hunspell/PKGBUILD
shelly build --isolated --check ./devario-core/hunspell/PKGBUILD
```

The isolated root must reach repositories holding the declared build dependencies. After
building, publish the archives, refresh the database Remora and Shelly use, then confirm
the provisions landed in the new `.PKGINFO`:

```sh
bsdtar -xOf /path/to/dbus-1.16.2-2-x86_64.pkg.tar.zst .PKGINFO | grep '^provides = '
```

Builder-wide CFLAGS and LDFLAGS come from `/etc/shellybuild.conf` on the worker; these
recipes declare `arch=(x86_64)` and impose no `-march=native` or v3 baseline. Run the GCC
recipe once for all five runtime libraries; its full compiler bootstrap costs far more
time and disk than the others ([gcc/README.md](devario-core/gcc/README.md)). Build Hunspell
before Enchant and GLib with `glib2-devel` before GtkSourceView; D-Bus and GLib use each
other during building, so an existing compatible package from a bootstrap repository
starts that cycle. Nothing here bootstraps a distribution from an empty root.

## Validation status of the first ABI set

Native, unprivileged Shelly builds with checks enabled succeeded for Hunspell, jq,
numactl, Enchant, GtkSourceView, D-Bus and GLib, and those archives carry the expected ABI
provisions. Seven of the eight recipes review clean; GCC warns on upstream command
substitutions and Makefile variables in its patch, inspected and retained. Full GCC
compilation has not been run, and current per-package status is in the recipe READMEs,
notably [glib2](devario-core/glib2/README.md).

Full `--isolated` nspawn verification is unavailable on this host because Shelly's
privileged coordinator needs an interactive sudo password, so the isolated runs belong to
the worker before publishing.

## Closed

Each line is a gap this file used to describe at length. All closures were verified
published on 2026-11-03; the transcripts, probes and validation trails are in this file's
git history.

| Date | Gap | Closed by |
| --- | --- | --- |
| 2026-10-30 | `emacs` and `emacs-wayland` depended on a `libotf` nothing published | `libotf 0.9.16-6` (devario-libs); the `libxaw` drop and the `autoreconf -fiv` requirement are recorded in the recipe |
| 2026-10-27 | PAM documentation needed DocBook 5 catalogs and an HTML-to-text renderer | `docbook5-xml 5.1-6`, `w3m 0.5.6-3`, then `pam 1.7.3-4` |
| 2026-10-26 | `libsoup3` tests needed Quart and its HTTP/2 stack | nine Python recipes through `python-quart 0.23.1-1` |
| 2026-10-26 | `dbus-python` needed `python-tomli` | `python-tomli 2.5.0-1` |
| 2026-10-26 | `btop`'s man page needed `lowdown`, which builds only with `bmake` | `ed`, `bc`, `bmake 20260912-1`, `lowdown 3.2.1-1`, `btop 1.4.8-1`. NetBSD replaced the crufty.net mirror whose duplicate leaf certificate Shelly's downloader rejects, and the recipe verifies the relative `liblowdown.so` link instead of re-creating it as an absolute path that dangles in `$pkgdir` |
| 2026-10-23 | ProtonUp-Qt needed three Python providers and their closure | `protonup-qt 2.16.0-1` via `signify`, `libev` and `python-steam 2.0.0.alpha1-5`, whose `make pb_compile` needs `protobuf` rather than only the Python bindings |
| 2026-10-20 | `pcp` PMDA plugins needed 25 names | `pcp 7.2.2-1` on 22 imports through `libnbd`/`libvirt`/`libvirt-python` and the Perl alien chain; `perl-yaml-libyaml` passes `DESTDIR` to `make install` because Shelly gives `package()` a different `$pkgdir` from `build()` |
| 2026-10-19 | `qemu` named 14 unplannable packages | `qemu 11.1.3-1` splits; all 14 already had recipes and needed only publication, and `libxdp` is an [xdp-tools](devario-utilities/xdp-tools/PKGBUILD) output |
| 2026-10-19 | `gvfs` failed `CascadeDependenciesChanged` on four backends | eight Arch imports: `libgoa 3.58.1-1` (a `gnome-online-accounts` split), `msgraph 0.3.5-1`, `wsdd 0.9-2`, `libmtp`, `librest`, `uhttpmock`, `python-defusedxml`, `python-systemd` |
| 2026-10-19 | `thunar` needed most of the Xfce stack | ten imports including `exo 4.20.0-2`, `garcon`, `xfce4-panel`, `valabind`. `xfce4-panel` is a `makedepends` because thunar builds `thunar-tpa` against libxfce4panel; `valabind` is one meson never reads, and both still gate the plan |
| 2026-10-19 | Proton VPN and `libei` needed 65 pkgbases | `proton-vpn-daemon`, `proton-vpn-gtk-app` and `libei 1.6.0-2`, which supersedes the `Unknown Packager` seed. Only 29 gated the plan; the rest were `checkdepends` legs, whose own closure would balloon past 600 pkgbases, so run such waves with checks off. The unguarded `systemctl` calls are handled in [proton-vpn-daemon/README.md](devario-utilities/proton-vpn-daemon/README.md) |
| 2026-10-18 | IBus needed Unicode data providers | `unicode-character-database 18.0.0-2`, `unicode-emoji 17.0-2`, `unicode-cldr 48.2-1`, then `ibus 1.5.34-2` |
| 2026-10-14 | llama.cpp backends had no providers | `llama-cpp 0.8.0-1`, `ggml 0.28.0-1`, `openvino 2026.4.1-2`, `zendnn` and the Intel graphics chain; provider inventory in [`audits/llama-backends-2026-10-14.json`](audits/llama-backends-2026-10-14.json) |
| 2026-10-14 | Neovim named twelve unplannable providers | thirteen imports, then `neovim 0.12.6-2`. `lpeg` needs `luarocks` as a `makedepends` because it packages through it, and `lua-mpack` carries a global `libmpack` depend, a different project from `msgpack-c`. Four libraries added versioned provisions beside the bare name, with versions read from Arch's built archives rather than recipe text. `luarocks` moved its five manifest hooks to `/usr/share/rlpm/hooks` ([HOOK-BUILDS.md](HOOK-BUILDS.md)). `lua51-compat53` and `lua52-compat53` stay open above |
| 2026-10-19 | PackageKit's ALPM backend was dead on a rlpm system | `packagekit 1.4.0-3` with the Shelly backend and a native refresh hook; `python3 tests/test-packagekit-shelly.py` covers the helper protocol |
| 2026-10-14 | `libluv` was an unpublishable six-output pkgbase | `lua51 5.1.5-13`, `lua53 5.3.6-4`, then `libluv 1.52.1-1` |
| 2026-10-14 | `kitty` needed four providers and Slang two more | six imports, then `kitty 0.49.2-1`; publish the three `ttf-nerd-fonts-symbols` outputs and the three kitty outputs with their matching releases |
| 2026-10-13 | `imake`, `yasm` and the WASI C++ libraries were unplannable | four imports plus [xorg-font-util](devario-development/xorg-font-util/PKGBUILD): `wasi-libc++ 23.1.4-1` covering both outputs, `imake 1.0.11-1`, `yasm 1.3.0-9` |
| 2026-10-13 | `systemd` splits needed four providers | `quota-tools`, `kexec-tools`, `libfido2 1.17.0-1`, `python-pefile`, then `systemd 262-9`, with `rpcsvc-proto` and `libcbor` first. libcbor's own failure was `DownloadSizeMismatch` during shellystrap provisioning, not a compile error, and needed no recipe change |
| 2026-10-13 | Fastfetch needed five providers and EFL and Xfconf four more | nine imports, `fastfetch 2.70.0-1`, `efl 1.28.1-4`; SCIM's IMdkit callback prototype patch is the GCC 16 C23 fix, named in its recipe |
| 2026-10-11 | Thrift's Emacs byte-compile step could not resolve `libtree-sitter.so` | publish the `tree-sitter` split, then `emacs-nox`, then `thrift 0.22.0-6` |
| 2026-10-11 | `arrow` needed grpc, re2 and thrift | `arrow 25.0.1-8`; `re2 2:2025.11.05-7` moved `gtest` and `benchmark` into `makedepends` because `RE2_BUILD_TESTING=ON` needs both during `build()` |
| 2026-10-11 | `vtk` reported 19 unplannable build dependencies | `vtk 9.7.1-3` on 19 existing recipes. The VTK and OpenCascade cycle cannot be reordered, because Shelly resolves both arrays before the build starts: it broke by publishing `opencascade 1:7.9.3-4` seeded with `USE_VTK=OFF`, then VTK, then the `1:7.9.3-5` restore |
| 2026-10-10 | ROCm header and solver chains unplannable | `rocprim 10.0-1`, `rocthrust 10.0-1`, `rocsolver 7.2.4-1` via `rocblas`/`rocsparse`. [hip-runtime](devario-core/hip-runtime/PKGBUILD) builds AMD and NVIDIA outputs, so it needs `cuda` even for AMD-only, and rocm-cmake's checks need a published rocm-llvm, so build the chain with checks off |
| 2026-10-10 | rocBLAS found Tensile 4.47.0 instead of its exact 4.45.0 | `rocblas 7.2.4-5` points `Tensile_DIR` and `Tensile_ROOT` at the bundled source and puts it first on `PYTHONPATH` |
| 2026-10-10 | `libxml++` tutorial generation exited 4 without a DocBook catalog | `libxml++ 3.2.6-2` with `docbook-xsl` as a `makedepends` |
| 2026-10-10 | libffado needed 13 imports and 7 publications | `libffado 2.5.0-3` through the Qt5, PyQt5 and speech chain. `qt5-multimedia 5.15.19+kde+r2-2` needs only `gst-plugins-bad-libs`, not the 15-dependency `gst-plugins-bad` bundle, because the photography headers live in the libs split; `libsonic 0.2.0-3` keeps `-fPIC` in its `ldflags.patch` and passes the SONAME option outside `LDFLAGS` |
| 2026-10-10 | PyQt5 staged SIP scripts under `usr/sbin`, conflicting with `filesystem`'s symlink | `python-pyqt5 5.15.11-9` passes `--scripts-dir /usr/bin`, and `libffado` requires that release so the worker cannot reuse the conflicting archive. Do not overwrite the filesystem symlink |
| 2026-10-10 | `asciidoctor`'s gem stayed under Ruby 3.4 paths, breaking Git LFS `make man` | `asciidoctor 2.0.26-2` bounded to Ruby 4.0 through `Gem.default_dir`, then `git-lfs 3.8.0-3`, which requires that release; a Ruby minor upgrade needs both rebuilt |
| 2026-10-02 | ISO runtime closure and the OS-owned recipes | `flatpak`, `inxi`, `nbd 3.27.1-4`, `nfs-utils`, `tpm2-tools`, `spandsp 0.0.6-6`, then `devario-base 3-20`, `devario-boot 1-16`, `devario-dracut 112-9`, `devario-keyring 20260923-3`, `netcat`, `power-profiles-daemon 0.30-7`. The move of hooks and helpers to `/usr/share/rlpm/` and keyrings to `/usr/share/shelly/keyrings/` needs Shelly built with `-Dpath-profile=devario` and `HookDirMode = Replace` |
| 2026-10-05 | The ISO closure selected incompatible `atkmm` and `cairomm` ABI branches | epoch-1 `atkmm 1:2.28.5-1` and `cairomm 1:1.14.6-1` beside the modern `mm-common 1.0.8-3`, `libsigc++-3.0 3.8.1-1`, `glibmm-2.68 2.90.0-1`, `cairomm-1.16 1.19.1-1`, `atkmm-2.36 2.36.4-1`; coexistence and upgrade ordering in [ABI-BUILDS.md](ABI-BUILDS.md) |
| 2026-10-05 | Calamares needed `qt6-tools`, which needed an HTML parser | `gumbo-parser 0.14.1-1`, `litehtml 0.10-3` |
| undated | `noto-fonts` packaging failed on a truncated Git checkout name | `noto-fonts 1:2026.11.01-1` aliases the source `notofonts::`, because makepkg truncates at `.git` while Shelly only strips a terminal `.git` |
| undated | `mupdf` failed `--resolve-dependencies` on six names | `mupdf 1.28.5-2` on `cmark-gfm`, `leptonica`, `tesseract` with its data splits, `unzip`, `zint`, `zxing-cpp`. `zxing-cpp` appends `--as-needed` because the builder's `LDFLAGS` omit it and ld otherwise must resolve the `vtk` and `hdf5` references `opencv` leaves to its optdepends |

## Provenance

Devario is an independent operating system. These x86_64 recipes are adapted from the
corresponding [Arch Linux packaging repositories](https://gitlab.archlinux.org/archlinux/packaging/packages),
which is what the recipe links record. Each directory keeps its PKGBUILD, generated
`.SRCINFO` and required local sources; copy whole directories, including any `keys/pgp`
material, to the worker.
