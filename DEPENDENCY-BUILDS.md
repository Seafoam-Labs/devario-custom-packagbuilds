# Missing dependency builds for Shelly

## dbus-python needs python-tomli (2026-10-26)

The worker's `devario-core/dbus-python` dependency plan reports `python-tomli`
twice as `not_in_repositories` and twice as `not_in_environment`. These entries
name one missing provider. No local recipe existed, and Shelly's cached
repository search returned no package.

Build and publish [python-tomli](devario-core/python-tomli/PKGBUILD) `2.5.0-1`,
refresh the worker's repository metadata, then retry `dbus-python`. Upload both
the new `PKGBUILD` and `.SRCINFO`; uploading the recipe alone does not satisfy
the dependency. The worker's `dbus-python` recipe is not present in this checkout
and was not modified.

The recipe builds the pure-Python wheel from the checksum-pinned
[upstream source release](https://pypi.org/project/tomli/2.5.0/). It requires
`python-build`, `python-installer`, and `python-flit-core>=3.12,<5`, matching
upstream's backend requirements. All are present in the cached repository
catalogs. Python's standard-library `tomllib` does not provide the separately
named `tomli` import or satisfy the package dependency.

Validation: source SHA-256, Bash syntax, Shelly metadata generation and review
(no findings), and the recipe's build and staged package functions passed.
Validation used checksum-verified repository build tools extracted under `/tmp`
without host installation. Staged imports, version metadata, string/file TOML
parsing, decimal handling, invalid-input rejection, license, and typing marker
checks passed. The source archive does not include upstream tests. Shelly's
isolated dependency resolution stopped at repository refresh with `SyncDbFailed`;
no isolated build or repository publication was performed.

## btop man page needs lowdown, and lowdown needs bmake (2026-10-26)

[btop](devario-utilities/btop/PKGBUILD) lists `lowdown` in `makedepends` to
render `btop.1` from `manpage.md`. `lowdown` was published in neither Devario
repository and had no local recipe, so
[devario-libs/lowdown](devario-libs/lowdown/PKGBUILD) `3.2.1-1` was added from
the Arch packaging recipe.

lowdown's `Makefile` is bmake-only: GNU make stops at `Makefile:153: *** missing
separator` on the upstream `.ifdef` block, so `bmake` is a hard build dependency
rather than a preference. `bmake` is unpublished too, and has no local recipe.
Its `boot-strap op=build` runs the unit tests automatically, and
`unit-tests/varname-dot-make-jobs.mk` shells out to `bc` — that is why Arch
declares `bc` as a bmake makedepend, and it is why the bmake probe failed here
until `bc` was accounted for. `bc`'s own `check()` needs `ed`.

Recipes exist for the lower two rungs but nothing in this chain is published:

| Stage | Recipe directory | Required by |
| --- | --- | --- |
| 1 | `devario-development/ed` | bc |
| 2 | `devario-utilities/bc` | bmake |
| 3 | `devario-development/bmake` | lowdown |
| 4 | `devario-libs/lowdown` | btop |
| 5 | `devario-utilities/btop` | final application |

lowdown's runtime dependency `libmd` `1.3.0-1` and makedepend `git` are already
published in `devario-core`, so only stages 1–4 need queueing. btop
itself is not blocked by this chain: its Makefile prints `Command 'lowdown' not
found: skipping generating man page` and guards the install step with
`ifneq ($(wildcard btop.1),)`, so btop can be built ahead of stages 1–4 at the
cost of shipping no man page.

Validated on the host rather than in isolation: bmake 20260912 built here, and
driving lowdown 3.2.1 with it produced `liblowdown.so.5` with SONAME
`liblowdown.so.5` (ELF64) under the staged install, and `bmake regress` passed
with no failures. The lowdown recipe therefore declares `liblowdown.so=5-64`
beside the bare provision and refuses to package a stale value. bmake's source
archive matches the recipe checksum and verifies against `keys/pgp`
`7E228507C26D8DC164F531BFBA54C8AF755A2A99` (sigs@crufty.net). Import that key
into the builder account before the isolated bmake build; neither recipe has had
a `--isolated` run yet, since the host has no `bmake` and the chain above is
what an isolated root would have to install first.

## ProtonUp-Qt dependency publication (2026-10-23)

The worker's `IncompleteDependencyPlan` for
[protonup-qt](devario-gaming/protonup-qt/PKGBUILD) names `python-inputs`,
`python-steam`, and `python-zstandard`. All three already have recipes under
`devario-libs`; they must be built and published before the worker can resolve
ProtonUp-Qt's isolated environment. The `not_in_repositories` and
`not_in_environment` entries describe the same three missing providers.

The local repository database snapshot from October 22 also lacks eight
transitive prerequisites. Build and publish the following stages, refreshing
the worker's repository databases between stages. Packages already available
in the worker's current repositories can be skipped. Recipes within a stage
do not depend on one another.

| Stage | Recipe directories | Required by |
| --- | --- | --- |
| 1 | `devario-development/signify`; `devario-libs/python-inputs`; `devario-libs/python-zstandard`; `devario-libs/python-greenlet`; `devario-libs/python-zope-event`; `devario-libs/python-pycryptodomex`; `devario-libs/python-h11` | later stages and ProtonUp-Qt |
| 2 | `devario-libs/libev`; `devario-libs/python-wsproto` | gevent and Steam |
| 3 | `devario-libs/python-gevent` | Steam |
| 4 | `devario-libs/python-steam` | ProtonUp-Qt |
| 5 | `devario-gaming/protonup-qt` | final application |

`python-steam` release `2.0.0.alpha1-5` adds the missing `protobuf` build
dependency: its `prepare()` invokes `make pb_compile`, which runs `protoc`.
The existing `python-protobuf` runtime dependency provides Python bindings,
not the compiler.

Shell syntax passes and Shelly review completes for the three direct dependency
recipes; the inputs review flags the word `docker` in a patch subject, which
does not execute Docker. Steam's `.SRCINFO` has been regenerated. Dependency availability above
was checked against the cached repository databases, not a live worker plan:
local isolated dependency resolution could not refresh repositories
(`SyncDbFailed`). Builds and publication remain necessary; recipe edits alone
do not make these dependencies available to the worker.

## pcp PMDA dependency publication (2026-10-20)

The worker's `IncompleteDependencyPlan` for [pcp](devario-utilities/pcp/PKGBUILD)
7.2.2-1 names nine missing packages: `python-openpyxl`, `python-jsonpointer`,
`libvirt-python`, `perl-net-snmp`, `perl-xml-libxml`, `perl-yaml-libyaml`,
`perl-dbd-mysql`, `python-psycopg2` and `libvarlink`. Eight are new recipes.
`libvirt-python` already has one, and it needs the existing but unpublished
`libvirt`, which needs `libnbd`. Fourteen more unpublished Perl and Python
modules are transitive dependencies, so the wave imports 22 recipes and
publishes 25 names.

Build and publish in this order, refreshing the worker repository database
between stages. The stage 1 recipes do not depend on one another. The
`Depends on` column lists only wave dependencies; every other dependency
already publishes.

| Stage | Recipe | Release | Depends on |
| --- | --- | --- | --- |
| 1 | [libnbd](devario-libs/libnbd/PKGBUILD) (existing) | `1.24.3-1` | - |
| 1 | [libvarlink](devario-libs/libvarlink/PKGBUILD) | `24.0.1-1` | - |
| 1 | [perl-crypt-des](devario-libs/perl-crypt-des/PKGBUILD) | `2.09-2` | - |
| 1 | [perl-digest-sha1](devario-libs/perl-digest-sha1/PKGBUILD) | `2.13-23` | - |
| 1 | [perl-dbi](devario-libs/perl-dbi/PKGBUILD) | `1.656-2` | - |
| 1 | [perl-ffi-checklib](devario-libs/perl-ffi-checklib/PKGBUILD) | `0.31-8` | - |
| 1 | [perl-file-chdir](devario-libs/perl-file-chdir/PKGBUILD) | `0.1011-6` | - |
| 1 | [perl-path-tiny](devario-libs/perl-path-tiny/PKGBUILD) | `0.150-2` | - |
| 1 | [perl-xml-namespacesupport](devario-libs/perl-xml-namespacesupport/PKGBUILD) | `1.12-6` | - |
| 1 | [perl-xml-sax-base](devario-libs/perl-xml-sax-base/PKGBUILD) | `1.09-6` | - |
| 1 | [perl-yaml-libyaml](devario-libs/perl-yaml-libyaml/PKGBUILD) | `0.910.0-2` | - |
| 1 | [python-et-xmlfile](devario-libs/python-et-xmlfile/PKGBUILD) | `2.0.0-3` | - |
| 1 | [python-jsonpointer](devario-libs/python-jsonpointer/PKGBUILD) | `3.4-1` | - |
| 1 | [python-psycopg2](devario-libs/python-psycopg2/PKGBUILD) | `2.9.13-1` | - |
| 2 | [libvirt](devario-libs/libvirt/PKGBUILD) (existing) | `12.8.0-1` | `libnbd` |
| 2 | [perl-alien-build](devario-libs/perl-alien-build/PKGBUILD) | `2.88-1` | `perl-ffi-checklib`, `perl-file-chdir`, `perl-path-tiny` |
| 2 | [perl-dbd-mysql](devario-libs/perl-dbd-mysql/PKGBUILD) | `4.055-2` | `perl-dbi` |
| 2 | [perl-digest-hmac](devario-libs/perl-digest-hmac/PKGBUILD) | `1.05-3` | `perl-digest-sha1` |
| 2 | [perl-xml-sax](devario-libs/perl-xml-sax/PKGBUILD) | `1.02-2` | `perl-xml-sax-base`, `perl-xml-namespacesupport` |
| 2 | [python-openpyxl](devario-libs/python-openpyxl/PKGBUILD) | `3.1.5-3` | `python-et-xmlfile` |
| 3 | [libvirt-python](devario-libs/libvirt-python/PKGBUILD) (existing) | `12.8.0-1` | `libvirt` |
| 3 | [perl-alien-build-plugin-download-gitlab](devario-libs/perl-alien-build-plugin-download-gitlab/PKGBUILD) | `0.01-7` | `perl-alien-build`, `perl-path-tiny` |
| 3 | [perl-net-snmp](devario-libs/perl-net-snmp/PKGBUILD) | `6.0.1-15` | `perl-digest-hmac`, `perl-digest-sha1`, `perl-crypt-des` |
| 4 | [perl-alien-libxml2](devario-libs/perl-alien-libxml2/PKGBUILD) | `0.20-6` | `perl-alien-build`, `perl-alien-build-plugin-download-gitlab` |
| 5 | [perl-xml-libxml](devario-libs/perl-xml-libxml/PKGBUILD) | `2.0213-2` | `perl-alien-libxml2`, `perl-xml-sax`, `perl-xml-namespacesupport` |
| 6 | [pcp](devario-utilities/pcp/PKGBUILD) | `7.2.2-1` | all nine names |

`libnbd` verifies its source with `validpgpkeys`; its recipe does not vendor the
key, so import fingerprint `F7774FB1AD074A7E8C8767EA91738F73E1B768A0` on the
worker if it is not already in the keyring.

`perl-yaml-libyaml` drops `DESTDIR` from `PERL_MM_OPT` and passes it to
`make install`, because Shelly gives `package()` a different `$pkgdir` from
`build()`.

Validation: each recipe's committed `.SRCINFO` regenerates identically, and
`shelly build --review-only` exits 0 for all 22 imports. The only findings are
dynamic-command warnings in `perl-xml-libxml`'s install scriptlet,
`python-psycopg2`'s `check()`, and 16 lines of `python-et-xmlfile`'s test
patch. No isolated build or publication was performed.

## QEMU build dependency publication (2026-10-19)

The worker's `IncompleteDependencyPlan` for [qemu](devario-utilities/qemu/PKGBUILD)
names 14 missing packages: `brltty`, `capstone`, `dtc`, `libxdp`,
`multipath-tools`, `ndctl`, `rutabaga-ffi`, `sdl2_image`, `spice-protocol`,
`spice`, `usbredir`, `vde2`, `virglrenderer` and `vte3`. All 14 names are
covered by existing recipes, so nothing needs importing. `libxdp` is the
second output of the [xdp-tools](devario-utilities/xdp-tools/PKGBUILD) pkgbase.
None of the 14 names has a record in any Devario repository, so publication is
the whole gap.

Build and publish in this order, refreshing the worker repository database
between stages. The stage 1 recipes do not depend on one another.

| Stage | Recipe | Release | Output needed by qemu |
| --- | --- | --- | --- |
| 1 | [brltty](devario-utilities/brltty/PKGBUILD) | `6.9.1-3` | `brltty` |
| 1 | [capstone](devario-libs/capstone/PKGBUILD) | `5.0.9-1` | `capstone` |
| 1 | [dtc](devario-utilities/dtc/PKGBUILD) | `1.8.1-1` | `dtc` |
| 1 | [multipath-tools](devario-utilities/multipath-tools/PKGBUILD) | `0.15.1-1` | `multipath-tools` |
| 1 | [ndctl](devario-libs/ndctl/PKGBUILD) | `85-1` | `ndctl` |
| 1 | [sdl2_image](devario-libs/sdl2_image/PKGBUILD) | `2.8.12-2` | `sdl2_image` |
| 1 | [spice-protocol](devario-libs/spice-protocol/PKGBUILD) | `0.14.5-1` | `spice-protocol` |
| 1 | [usbredir](devario-libs/usbredir/PKGBUILD) | `0.15.0-1` | `usbredir` |
| 1 | [vde2](devario-utilities/vde2/PKGBUILD) | `2.3.3-10` | `vde2` |
| 1 | [virglrenderer](devario-libs/virglrenderer/PKGBUILD) | `1.3.0-2` | `virglrenderer` |
| 1 | [vte3](devario-libs/vte3/PKGBUILD) | `0.84.1-1` | `vte3` |
| 1 | [xdp-tools](devario-utilities/xdp-tools/PKGBUILD) | `1.6.3-2` | `libxdp` |
| 2 | [spice](devario-libs/spice/PKGBUILD) | `0.16.0-4` | `spice` |
| 2 | [rutabaga-ffi](devario-libs/rutabaga-ffi/PKGBUILD) | `0.1.85-1` | `rutabaga-ffi` |
| 3 | [qemu](devario-utilities/qemu/PKGBUILD) | `11.1.2-2` | all outputs |

`spice` needs `spice-protocol`, and `rutabaga-ffi` needs `virglrenderer`. Every
other dependency of the 14 resolves to a published Devario package or Arch
`core`/`extra`, including `gfxstream` for `rutabaga-ffi` and `wolfssl` for
`vde2`, which provides `libwolfssl.so`.

Validation: each recipe's committed `.SRCINFO` regenerates identically, and
`shelly build --review-only` exits 0 for all 14 and for qemu. The only findings
are brltty's 70 dynamic-command warnings, which come from text inside
`brltty-6.4-x11_autostart.patch`. No isolated build or publication was
performed.

## gvfs GIO backend dependency closure (2026-10-19)

The worker failed `devario-core/gvfs` with `CascadeDependenciesChanged` on
`libgoa`, `libmtp`, `msgraph` and `wsdd`. None had a recipe on any branch or a
published record anywhere. Closing them takes eight pkgbases imported verbatim
from Arch packaging: `gnome-online-accounts` to `devario-core` beside gvfs,
`libmtp`, `librest`, `msgraph`, `python-defusedxml`, `python-systemd` and
`uhttpmock` to `devario-libs`, and `wsdd` to `devario-utilities`.

`libgoa` is a split of the `gnome-online-accounts` pkgbase, which also produces
`gnome-online-accounts` and `libgoa-docs`. Four imports are themselves
plan-gating: `librest` for `gnome-online-accounts`, `uhttpmock` for `msgraph`,
and `python-defusedxml` plus `python-systemd` for `wsdd`. The published
`gvfs-goa`, `gvfs-mtp`, `gvfs-onedrive` and `gvfs-wsdd` `.PKGINFO` depends name
only the package names, so the split names are enough to resolve them.

Build and publish in this order, refreshing the worker repository database
between stages:

1. [librest](devario-libs/librest/PKGBUILD) 0.10.2-2,
   [libmtp](devario-libs/libmtp/PKGBUILD) 1.1.23-1,
   [uhttpmock](devario-libs/uhttpmock/PKGBUILD) 0.11.0-2,
   [python-defusedxml](devario-libs/python-defusedxml/PKGBUILD) 0.7.1-8,
   [python-systemd](devario-libs/python-systemd/PKGBUILD) 236-1.
2. [gnome-online-accounts](devario-core/gnome-online-accounts/PKGBUILD) 3.58.1-1,
   then [wsdd](devario-utilities/wsdd/PKGBUILD) 0.9-2.
3. [msgraph](devario-libs/msgraph/PKGBUILD) 0.3.5-1.
4. Retry [gvfs](devario-core/gvfs/PKGBUILD).

`gnome-online-accounts`, `msgraph` and `librest` are the only deviations from
upstream: each adds both bare and versioned SONAME provisions plus
`_verify_soname` checks, because Shelly preserves the bare form that Arch would
version. Nothing in the wave publishes yet.

## Thunar Xfce stack dependency closure (2026-10-19)

The worker failed `devario-utilities/thunar` with `IncompleteDependencyPlan` on
`exo`, `libxfce4ui` and `xfce4-panel`. Those three drag the rest of the Xfce
desktop stack with them, so closing thunar takes ten pkgbases, all imported
verbatim from Arch packaging: eight shared libraries to `devario-libs`,
`xfce4-panel` to `devario-utilities` beside thunar, and `valabind` to
`devario-development` beside vala. None of the ten had a recipe or a published
record, and every other name in the closure already publishes, including the
existing Xfce siblings `libxfce4util`, `xfconf` and `xfce4-dev-tools`. `sh`
resolves through the published `bash` provision and `libvala-0.56.so` through
the `vala` provision.

Build and publish in this order, refreshing the worker repository database
between stages:

1. [libgtop](devario-libs/libgtop/PKGBUILD) 2.41.3-2,
   [startup-notification](devario-libs/startup-notification/PKGBUILD) 0.12-9,
   [valabind](devario-development/valabind/PKGBUILD) 2.1.0-1.
2. [libxfce4ui](devario-libs/libxfce4ui/PKGBUILD) 4.20.2-1,
   [libwnck3](devario-libs/libwnck3/PKGBUILD) 43.3-1,
   [gtk-layer-shell](devario-libs/gtk-layer-shell/PKGBUILD) 0.10.1-1.
3. [exo](devario-libs/exo/PKGBUILD) 4.20.0-2,
   [garcon](devario-libs/garcon/PKGBUILD) 4.20.0-2,
   [libxfce4windowing](devario-libs/libxfce4windowing/PKGBUILD) 4.20.7-1.
4. [xfce4-panel](devario-utilities/xfce4-panel/PKGBUILD) 4.20.8-1, then rebuild
   [thunar](devario-utilities/thunar/PKGBUILD).

`xfce4-panel` is a thunar `makedepends`, not an optdepends: thunar builds the
`thunar-tpa` panel plugin against libxfce4panel. `valabind` is the opposite
case, a `gtk-layer-shell` `makedepends` its meson build never reads. Both still
gate the plan, which resolves every global `makedepends` name.

## Proton VPN and libei dependency closure (2026-10-19)

Two worker plan failures named six absent names. `python-distro` was stale: it
published as `1.9.0-5` in `devario-libs` on 2026-10-19, so that line needs only
a worker repository refresh. The other five have no provider anywhere, and
resolving them transitively took 65 pkgbases imported verbatim from Arch: 56 to
`devario-libs`, 8 to `devario-utilities`, and `libei` to `devario-core`, the
repository where its record already ships.

`devario-core/libei` had no recipe at all. Published `libei 1.6.0-1` is an
`Unknown Packager` seed, so the import at `1.6.0-2` supplies the missing source
of truth and supersedes the seed without downgrading it. `proton-vpn-gtk-app`
needed no change: upstream is also `4.18.7-1`, and its
`python-proton-vpn-api-core>=5.8.1` floor is satisfied by `5.8.7`.

Only 29 of the 65 gate the plan, which covers global `depends` plus
`makedepends`. The other 36 are `checkdepends` legs of those 29, so they gate
only a job that runs its own test suite.

Build and publish in this order, refreshing the worker repository database
between levels:

1. [openvpn](devario-utilities/openvpn/PKGBUILD) 2.7.8-2, from the existing
   committed but unpublished recipe, as a `networkmanager-openvpn` makedepend.
2. The 17 pkgbases with no in-wave prerequisite: `bcc`,
   `networkmanager-openvpn`, `python-aiohappyeyeballs`, `python-bcrypt`,
   `python-dbus-fast`, `python-expandvars`, `python-fido2`, `python-gnupg`,
   `python-jaraco.classes`, `python-multidict`, `python-pynacl`,
   `python-pyopenssl`, `python-sentry_sdk`, `python-shtab`, `python-structlog`,
   `python-zipp`, `wireguard-tools`.
3. `libei` (publish both `libei` and `libei-docs`), `python-frozenlist`,
   `python-importlib-metadata`, `python-keyring`, `python-propcache`.
4. `python-aiosignal`, `python-yarl`. Then `python-aiohttp`.
5. `python-proton-core`. Then `python-proton-keyring-linux` and
   `python-proton-vpn-api-core`, which carries the rust and `protun` legs.
6. [proton-vpn-daemon](devario-utilities/proton-vpn-daemon/PKGBUILD), then
   [proton-vpn-gtk-app](devario-utilities/proton-vpn-gtk-app/PKGBUILD).

All four `bcc` splits and both `libei` splits publish together, since each
split pins its sibling by exact version.

`proton-vpn-daemon.install` is the only deviation from upstream in the wave;
its unguarded `systemctl` calls abort isolated roots, so see that recipe's
`README.md`.

Two limits. The `checkdepends` legs are not a closed set: those 36 recipes name
16 further absent names, concentrated in `python-twisted` and `gunicorn`, and
closing even those transitively balloons to some 630 pkgbases, so run the wave
with checks off.
Second, `meson`'s two long-standing absent makedepends narrow to one: this wave
supplies [python-aiohttp](devario-libs/python-aiohttp/PKGBUILD), leaving
`python-strictyaml` still without a recipe anywhere in the tree.

Validation: every recipe regenerates its committed `.SRCINFO` blob-identically
to what Arch ships, `shelly build --review-only` exits 0 for all 65, every local
source file and `keys/pgp` bundle landed, `LICENSES/0BSD.txt` is a regular file
as this tree commits it, and `makepkg --geninteg` reproduced the recorded
checksums for all six pinned git sources on the critical path. No isolated
build or publication was performed.

## IBus Unicode data dependencies (2026-10-18)

The three recipes already exist locally. An IBus `IncompleteDependencyPlan`
reporting these packages as `not_in_repositories` and `not_in_environment`
requires building and publishing their package outputs before retrying IBus.

1. Build/publish [unicode-character-database](devario-libs/unicode-character-database/PKGBUILD)
   18.0.0-2, then [unicode-emoji](devario-libs/unicode-emoji/PKGBUILD) 17.0-2.
2. Build [unicode-cldr](devario-development/unicode-cldr/PKGBUILD) 48.2-1
   and publish both `unicode-cldr` and `unicode-cldr-annotations` outputs.
   This recipe can be built independently of the other Unicode recipes.
3. Refresh worker repository/recipe metadata, then retry `devario-utilities/ibus`.

The character database's UCD and Unihan checksums were corrected against the
versioned Unicode 18.0.0 downloads. Emoji sources now use Unicode's HTTPS
`Public/17.0.0/emoji/` directory, with corrected sequence/test checksums.
Both changed recipes have regenerated `.SRCINFO`; CLDR needed no changes.

Validation: all source checksums, Bash syntax, makepkg metadata, and all four
staged package functions passed. The staged Unicode/emoji/CLDR data paths and
licenses were checked, with no overlapping payload files. No isolated IBus
build or repository publication was performed.

## llama.cpp inference backends (2026-10-14)

Added ten package bases for CPU, CUDA, Vulkan, ZenDNN, and OpenVINO.
The live Devario catalog was checked before adding recipes: shaderc, glslang,
Mesa/Vulkan drivers, opencl-nvidia, CUDA, CCCL, NCCL, oneTBB, and the common
build tools are already published. They do not need duplicate recipes.
The catalog and dependency-provider results are recorded in
[`audits/llama-backends-2026-10-14.json`](audits/llama-backends-2026-10-14.json).
This distinguishes published packages from recipes that still need building.

| Recipe | Outputs and role |
| --- | --- |
| [llama-cpp](devario-development/llama-cpp/PKGBUILD) | CLI, server, web UI, tools, and libllama; uses system GGML |
| [ggml](devario-libs/ggml/PKGBUILD) | `ggml` with CPU dispatch, plus `ggml-cuda`, `ggml-vulkan`, `ggml-zendnn`, and `ggml-openvino` |
| [zendnn](devario-libs/zendnn/PKGBUILD) | ZenDNN and its checksum-pinned private math dependencies |
| [openvino](devario-libs/openvino/PKGBUILD) | C++ runtime and `openvino-intel-gpu-plugin`; Intel CPU/NPU plugins disabled |
| [opencl-clhpp](devario-libs/opencl-clhpp/PKGBUILD) | OpenCL C++ headers, including `CL/cl2.hpp` required by GGML's OpenVINO backend |
| [intel-graphics-compiler](devario-libs/intel-graphics-compiler/PKGBUILD) | Intel GPU compiler |
| [intel-gmmlib](devario-libs/intel-gmmlib/PKGBUILD) | Intel GPU memory manager |
| [intel-metee](devario-libs/intel-metee/PKGBUILD) | Management transport library and documentation |
| [igsc](devario-libs/igsc/PKGBUILD) | GPU firmware-management library required when building the compute runtime |
| [intel-compute-runtime](devario-libs/intel-compute-runtime/PKGBUILD) | Intel OpenCL/Level Zero GPU driver |

Build/publish dependency order, after satisfying each recipe's existing Devario
dependencies:

1. `intel-metee`, `intel-gmmlib`, `intel-graphics-compiler`, and `zendnn`
   can be prepared independently. Build `igsc` after `intel-metee`.
2. Build `intel-compute-runtime` after `intel-graphics-compiler`,
   `intel-gmmlib`, and `igsc`.
3. Build/publish `openvino` and `openvino-intel-gpu-plugin`. The GPU plugin
   runtime dependencies are supplied by the Intel graphics packages above.
4. Build/publish `opencl-clhpp` using the existing `opencl-headers` package.
   Build `ggml` after `zendnn`, `openvino`, and `opencl-clhpp`, with the existing CUDA and
   Vulkan SDK packages installed. Publish all five split outputs together.
5. Build `llama-cpp` against GGML 0.26.0. The backend packages require the
   exact matching GGML package release; rebuild them together on upgrades.

CPU users install `llama-cpp` and its normal dependencies. GPU/alternative
CPU backends are optional additions. `ggml-openvino` requires the Intel GPU
plugin and its graphics driver dependencies. Use `llama-cli --list-devices`
to find its devices; `GGML_OPENVINO_DEVICE` selects a listed OpenVINO device
when multiple Intel GPUs are present. A matching NVIDIA kernel module is
required for CUDA; a GPU ICD is required for Vulkan. The server units are
installed but not enabled automatically.

GGML builds with `GGML_NATIVE=OFF` and runtime-dispatched CPU variants, so
the 3800X build host does not restrict the distributed CPU binaries to Zen 2.
CUDA uses upstream's non-native architecture list for the installed toolkit.
For a deliberately narrower local build, set `DEVARIO_CUDA_ARCHITECTURES`
to a CMake architecture list; doing so changes the GPUs that package supports.
The installed CUDA 13.4 host compiler guard accepts GCC through version 16.

ZenDNN is pinned to the revision selected by GGML 0.26.0. Its AOCL-DLP,
AOCL-Utils, oneDNN 3.12, LIBXSMM, and JSON sources are explicit, checksummed
inputs. Its private SDK lives under `/opt/zendnn`, preserving the existing
system oneDNN package. Only the ZenDNN library directory is added to the
loader configuration. The build serializes dependency projects and defaults
each project's parallelism to eight jobs; `CMAKE_BUILD_PARALLEL_LEVEL`
overrides that limit. All math dependency downloads happen in source
acquisition, not implicitly inside CMake. The optional FBGEMM, parlooper,
benchmarks, and documentation builds are disabled.

OpenVINO builds only the Intel GPU hardware plugin. Its Intel CPU and NPU
plugins, their private submodule downloads, and the separate NPU compiler
and driver recipes are omitted. Native GGML CPU dispatch and AMD ZenDNN
remain available. Python bindings, conversion utilities, and their
training-framework dependencies are omitted. Relevant upstream source pins,
patches, signing keys, and recipe licensing are retained;
`DEVARIO-UPSTREAM.json` records the imported recipe revisions.

For a Ryzen 7 3800X (8 cores/16 threads), 96 GB RAM, and SSD storage, allow
roughly 2–5 hours for the five GGML backends plus llama.cpp when their
dependencies are already installed. This is a planning estimate, not a
benchmark. A first source build of the Intel GPU compiler and OpenVINO
can extend that to an overnight or longer job; the graphics compiler
includes a substantial LLVM build. Start the large compiler builds one at a
time with 8–12 jobs. RAM capacity does not remove the CPU-time cost.

Validation includes shell syntax, generated `.SRCINFO`, bundled-source
checksums, Shelly review parsing, and split-package ownership fixtures:
`python tests/test-llama-packaging.py`. GGML's CPU variants and llama.cpp's
CLI/server compiled against staged system GGML; the UI was disabled for
this compile check. ZenDNN and all five private dependencies built, its
`package()` staged successfully, and GGML's ZenDNN module linked and loaded.
Two focused CPU ADD cases and two ZenDNN F32 matrix-multiplication cases
passed numerical checks. The ZenDNN checks disabled adaptive fallback to
exercise its kernels on small tensors. These are build-host smoke checks,
not performance measurements or verification on a Ryzen 3800X.
The audit records the checks and their limits. These recipes have not been
published or verified by a full isolated build of every GPU dependency.

## Aqueous desktop dependencies

Use `devario-desktop` from Aqueous's `packaging/devario/aqueous-desktop/PKGBUILD`
and publish its matching split outputs together. Pearl's maintained recipes
supply `pearl` and `pearl-greeter`. This repository no longer carries a separate
desktop metapackage. OS login and GPU defaults are delivered by
`devario-system-integration` 1-1; publish it before Aqueous 1.0.5-2. Existing
ISO installs need the [one-time adoption](devario-installer/devario-system-integration/README.md)
before upgrading to the new desktop dependency.

Publish `bolt`, `boltctl`, and `python-pyudev` before rebuilding the ISO.
The pyudev recipe declares `python` and `systemd-libs` as runtime dependencies.
Its source checksum, build, staged packaging, import, and PCI device enumeration
passed in the 2026-10-14 validation; no isolated worker build or publication
was performed. Pearl provides `pearl-capture-picker=1` without a separate recipe.

## Neovim's remaining closure (2026-10-14)

`devario-development/neovim` named twelve more unsatisfied dependency names
with no recipe in the tree or on `origin/main`: `lua51-lpeg`, `lua51-mpack`,
`msgpack-c`, `libvterm`, `unibilium` together with its `libunibilium.so`
provider, and the `tree-sitter-c`, `-lua`, `-markdown`, `-query`, `-vim` and
`-vimdoc` grammar packages. Thirteen Arch pkgbases supply them, because two
of the twelve are split names: `lua51-lpeg` comes from `lpeg` and
`lua51-mpack` from `lua-mpack`.

Two of the thirteen became necessary on the way in, both because Shelly
plans global depends and makedepends. `lua-mpack` carries a global
`depends=('libmpack')`, a different project from `msgpack-c`, so an
unsatisfied `libmpack` blocks that whole pkgbase exactly as `lua51` once
blocked `libluv`. `lpeg` has `luarocks` in `makedepends` and runs `luarocks
install` inside `_package()`, so it cannot be packaged without it. Neither
name is published or packaged today.

The imports keep Arch's source pins, checksums, signing keys and packaging
licenses from Arch's
[lpeg](https://gitlab.archlinux.org/archlinux/packaging/packages/lpeg),
[lua-mpack](https://gitlab.archlinux.org/archlinux/packaging/packages/lua-mpack),
[libmpack](https://gitlab.archlinux.org/archlinux/packaging/packages/libmpack),
[msgpack-c](https://gitlab.archlinux.org/archlinux/packaging/packages/msgpack-c),
[libvterm](https://gitlab.archlinux.org/archlinux/packaging/packages/libvterm),
[unibilium](https://gitlab.archlinux.org/archlinux/packaging/packages/unibilium),
[luarocks](https://gitlab.archlinux.org/archlinux/packaging/packages/luarocks)
and grammar packages. `lpeg`, `libmpack`, `lua-mpack`, `msgpack-c`,
`libvterm` and `unibilium` are shared libraries or Lua modules and sit in
`devario-libs` beside `libluv` and `msgpack-cxx`; `luarocks` and the six
grammars sit in `devario-development` beside `tree-sitter` and `neovim`.
Nine of the thirteen generated `.SRCINFO` files regenerate byte-identical to
Arch's own.

Four of the thirteen are shared libraries and so depart from Arch's text.
Shelly publishes a declared provision exactly as written while Arch's makepkg
silently versions a bare one, so `unibilium`, `msgpack-c`, `libvterm` and
`libmpack` name the SONAME form beside the bare one and refuse to package an
unexpected ELF class or soname. The four versions were read from Arch's built
`libvterm-0.3.3-2`, `unibilium-2.1.4-1`, `msgpack-c-7.0.2-1` and
`libmpack-1.0.5-4` archives, from `.PKGINFO` and `readelf`, not from recipe
text. The six grammars carry versioned sonames as well, but nothing links
them by `.so` name, so they stay verbatim.

`msgpack-c` departs once more. Its `build()` passed
`-DMSGPACK_BUILD_TESTS=ON` and `test/CMakeLists.txt` opens with
`FIND_PACKAGE (GTest REQUIRED)`, so the worker's `--no-check` mode dies at
configure before compiling anything because `gtest` is a `checkdepend` and
never installs. The option is now `OFF`, and the `check()` and
`checkdepends=('gtest')` that then had nothing to run are gone, the way
`systemd-libs` disables its suite.

Build and publish in this order. Everything in a stage is independent of its
peers.

| Stage | Recipe | Release | Purpose |
| --- | --- | --- | --- |
| 1 | [libmpack](devario-libs/libmpack/PKGBUILD) | `1.0.5-4` | msgpack in C |
| 1 | [luarocks](devario-development/luarocks/PKGBUILD) | `3.13.0-5` | the build tool `lpeg` packages through |
| 1 | [unibilium](devario-libs/unibilium/PKGBUILD) | `2.1.4-1` | terminfo parser, `libunibilium.so` |
| 1 | [msgpack-c](devario-libs/msgpack-c/PKGBUILD) | `7.0.2-1` | serialization library |
| 1 | [libvterm](devario-libs/libvterm/PKGBUILD) | `0.3.3-2` | terminal emulator library |
| 1 | [tree-sitter-c](devario-development/tree-sitter-c/PKGBUILD) | `0.24.1-2` | C grammar |
| 1 | [tree-sitter-lua](devario-development/tree-sitter-lua/PKGBUILD) | `0.5.0-3` | Lua grammar |
| 1 | [tree-sitter-markdown](devario-development/tree-sitter-markdown/PKGBUILD) | `0.5.3-2` | Markdown grammar, two libraries |
| 1 | [tree-sitter-query](devario-development/tree-sitter-query/PKGBUILD) | `0.8.0-2` | query grammar |
| 1 | [tree-sitter-vim](devario-development/tree-sitter-vim/PKGBUILD) | `0.8.1-3` | Vimscript grammar |
| 1 | [tree-sitter-vimdoc](devario-development/tree-sitter-vimdoc/PKGBUILD) | `4.1.0-2` | Vim help grammar |
| 2 | [lpeg](devario-libs/lpeg/PKGBUILD) | `1.1.0-5` | five outputs, needs `luarocks` |
| 2 | [lua-mpack](devario-libs/lua-mpack/PKGBUILD) | `1.0.13-2` | five outputs, needs `libmpack` |
| 3 | [neovim](devario-development/neovim/PKGBUILD) | `0.12.5-2` | the consumer |

Verified on this machine: all thirteen sources download and match their
declared checksums, and `shelly build --review-only --json` reports no
findings for twelve of them. `luarocks` reports only `warning` findings, all
of them its own shipped hooks and completion files calling `luarocks`, which
is that package's job. Its tarball signature verifies against the imported
`keys/pgp/8460980B2B79786DE0C7FCC83FD8F43C2BB3C478.asc`, which is not in this
host's keyring, so that import belongs to the account that invokes Shelly.

`luarocks` is the one recipe that departs in its file layout as well. It ships
five manifest-rebuild hooks, and Arch installs them under
`usr/share/libalpm/hooks`. This tree's hook contract puts package hooks in
`/usr/share/rlpm/hooks`, which is what `HookDirMode = Replace` leaves the
installed system reading, so an `usr/share/libalpm` hook is dead there; the
five land under `usr/share/rlpm/hooks` instead, as `neovim` and `texinfo`
already do, and `tests/test-hook-layout.py` is what holds that line. The move
also takes them out of the worker's way: the hook directory a build root scans
is compiled into the shelly binary, and this host's `shelly 3.1.6` carries
`/usr/share/libalpm/hooks`, so a hook left at Arch's path could fire during
root provisioning, which is how `packagekit`'s hook once killed a consumer's
build. Neither destination is reached by the `luarocks` transaction itself: the
published splits ship no `usr/lib/luarocks` paths, so the hooks' path trigger
never matches, and the scriptlet's `post_install` is guarded by a directory
test that the package never creates.

Nothing here is published yet, so neovim's plan still reports these names
missing until stages 1 and 2 land. Two install-time gaps survive: published
`lua51-luarocks` and `lua52-luarocks` depend on `lua51-compat53` and
`lua52-compat53`, which no repository carries and no recipe packages.
Neither reaches neovim or `lpeg`, which need only the `luarocks` command.
PackageKit's former ALPM hook is now replaced by a native hook; see the Shelly
backend change below. Other recipes can still fail the hook-layout check.

## PackageKit through Shelly (2026-10-19)

`devario-libs/packagekit` 1.4.0-3 builds the Devario `shelly` backend and depends
on `shelly>=3.1.8` and Python. It no longer builds or links the ALPM backend,
depends on pacman, or installs a separate pacman configuration. The GLib library
split remains available to existing PackageKit consumers.

The backend calls `/usr/bin/shelly` with `/etc/shelly.conf` and an immutable
`NativePackageBackend=rlpm` configuration. PackageKit continues to handle D-Bus
authorization. The helper sanitizes its environment and protocol output, checks
requested package names and versions, and uses Shelly for repository queries,
metadata, synchronization, installs and removals. A native
`/usr/share/rlpm/hooks/90-packagekit-refresh.hook` notifies PackageKit after CLI
transactions, tolerating absent system buses and unavailable daemons.

Update requests must select the full current standard update set; the backend
runs `shelly upgrade standard`, never individual partial upgrades. Transactions
are not automatically retried or forcibly cancelled. Simulation, download-only,
offline-update preparation, local-file installs, repository editing and other
unimplemented roles or flags are not supported. In particular, clients that
require a simulated transaction before installing will receive `not-supported`;
the backend never treats a simulation as permission to change packages. Signature
verification uses the system's Shelly repository policy.

Validation:

```sh
python3 tests/test-packagekit-shelly.py
PACKAGEKIT_SOURCE=/path/to/PackageKit-1.4.0 python3 tests/test-packagekit-shelly.py
```

The optional source check applies the Meson patch and compiles the backend
against upstream headers. The remaining tests cover the helper protocol,
pagination, transaction arguments, stale and unsafe IDs, unsupported flags,
failure propagation, package staging and the native hook. A full package build
and D-Bus integration test in a disposable Devario system remain release checks.

## Libluv for Neovim (2026-10-14)

`devario-development/neovim` names `libluv`, which no Devario repository
publishes and for which this tree carried no recipe. Arch builds `libluv` as
a six-output pkgbase, one shared library plus a module per Lua series, and
its global `makedepends` cover every series, including `lua51` and `lua53`,
neither of which this tree packages. Three new recipes close the set.

The imports are Arch's
[libluv](https://gitlab.archlinux.org/archlinux/packaging/packages/libluv),
[lua51](https://gitlab.archlinux.org/archlinux/packaging/packages/lua51) and
[lua53](https://gitlab.archlinux.org/archlinux/packaging/packages/lua53)
recipe directories copied verbatim, patches, checksums and packaging licenses
included. `lua51` and `lua53` sit beside the existing `lua52` recipe in
`devario-core`; `libluv` is a shared library and lands in `devario-libs`.

Only `libluv` departs from Arch's text: `package_libluv()` declares
`libluv.so` and `libluv.so=1-64` and refuses to publish an unexpected ELF
class or SONAME, because Shelly publishes a declared provision exactly as
written. A host build of the shared-library configuration reproduces Arch's
`libluv.so.1`, whose only recorded needs are `libuv.so.1` and `libc.so.6`.

Build and publish in this order, satisfying the other declared dependencies
before each build. Recipes in the same stage can be built independently.

| Stage | Recipe | Release | Purpose |
| --- | --- | --- | --- |
| 1 | [lua51](devario-core/lua51/PKGBUILD) | `5.1.5-13` | Lua 5.1 interpreter and headers |
| 1 | [lua53](devario-core/lua53/PKGBUILD) | `5.3.6-4` | Lua 5.3 interpreter and headers |
| 2 | [libluv](devario-libs/libluv/PKGBUILD) | `1.52.1-1` | libuv bindings, six outputs |

Every other `libluv` prerequisite is already published: `lua` 5.5.1, `lua52`,
`lua54`, `luajit`, `libuv`, `cmake` and `ninja`. The module builds read
`/usr/bin/lua<ver>` and `/usr/include/lua<ver>`, and the probe-built `lua51`
and `lua53` archives supply those paths the way the published `lua52` and
`lua54` already do.

The twelve names that still kept neovim out are in the section above.

## Kitty terminal, Slang, and their closure (2026-10-14)

The `kitty` terminal recipe needs four names that no Devario repository
publishes: `librsync` as a hard dependency of the installed package, and
`shader-slang`, `simde`, and `ttf-nerd-fonts-symbols-mono` as makedepends.
`shader-slang` in turn needs `miniz` and `unordered_dense`. Six newly
imported recipes supply the whole set.

The imports retain the source pins, checksums, patches, signing keys,
attribution, and packaging licenses from Arch's
[librsync](https://gitlab.archlinux.org/archlinux/packaging/packages/librsync),
[miniz](https://gitlab.archlinux.org/archlinux/packaging/packages/miniz),
[unordered_dense](https://gitlab.archlinux.org/archlinux/packaging/packages/unordered_dense),
[simde](https://gitlab.archlinux.org/archlinux/packaging/packages/simde),
[ttf-nerd-fonts-symbols](https://gitlab.archlinux.org/archlinux/packaging/packages/ttf-nerd-fonts-symbols),
and
[shader-slang](https://gitlab.archlinux.org/archlinux/packaging/packages/shader-slang)
packaging repositories, and `kitty` itself is
[Arch's recipe](https://gitlab.archlinux.org/archlinux/packaging/packages/kitty)
copied the same way. Copy each complete recipe directory to the worker.

Only `librsync` departs from Arch's text: it adds the versioned
`librsync.so=2-64` provision and a SONAME check, because Shelly publishes a
declared provision exactly as written. The other five are unmodified.

Build and publish in this order, satisfying the other declared dependencies
before each build. Recipes in the same stage can be built independently.

| Stage | Recipe | Release | Purpose |
| --- | --- | --- | --- |
| 1 | [unordered_dense](devario-libs/unordered_dense/PKGBUILD) | `5.3.2-1` | Header-only map for Slang |
| 1 | [miniz](devario-libs/miniz/PKGBUILD) | `3.1.2-1` | Zip codec for Slang |
| 1 | [simde](devario-libs/simde/PKGBUILD) | `0.8.2-1` | SIMD headers for kitty |
| 1 | [librsync](devario-libs/librsync/PKGBUILD) | `1:2.3.4-2` | kitty delta transport |
| 1 | [ttf-nerd-fonts-symbols](devario-libs/ttf-nerd-fonts-symbols/PKGBUILD) | `3.5.1-1` | Symbols font, three outputs |
| 2 | [shader-slang](devario-core/shader-slang/PKGBUILD) | `2026.18.2-2` | Slang compiler for kitty |
| 3 | [kitty](devario-utilities/kitty/PKGBUILD) | `0.49.2-1` | Terminal, terminfo, shell integration |

For each recipe, run `shelly build --isolated --check ./path/to/PKGBUILD`,
publish its binary outputs to an enabled worker repository, and refresh the
worker's metadata before the next dependent stage. Publish all three
`ttf-nerd-fonts-symbols` outputs before the kitty build that names
`ttf-nerd-fonts-symbols-mono`, and publish the three kitty outputs
together: `kitty` requires the matching `kitty-terminfo` and
`kitty-shell-integration` packages. Uploading recipes alone does not
satisfy the repository checks.

Every other dependency name of these seven recipes resolves to a published
package. `python3` and `libgl` resolve through the published `python` and
`libglvnd` provisions, and kitty's three optdepends are already published.

## Imake, Yasm and WASI C++ dependencies (2026-10-13)

The repeated `not_in_repositories` and `not_in_environment` entries for
`imake`, `yasm`, `wasi-libc++`, and `wasi-libc++abi` identify four missing
binary packages. Three newly imported recipes supply them; the WASI recipe
produces both C++ outputs. The additional `xorg-font-util` recipe supplies
an otherwise missing imake build prerequisite.

The imports retain the source pins, checksums, patches, signing keys,
attribution, and packaging licenses from Arch's
[imake](https://gitlab.archlinux.org/archlinux/packaging/packages/imake),
[yasm](https://gitlab.archlinux.org/archlinux/packaging/packages/yasm),
[wasi-libcplusplus](https://gitlab.archlinux.org/archlinux/packaging/packages/wasi-libcplusplus),
and [xorg-font-util](https://gitlab.archlinux.org/archlinux/packaging/packages/xorg-font-util)
packaging repositories. Copy each complete recipe directory to the worker.

Build and publish in this order, satisfying the other declared dependencies
before each build. Recipes in the same stage can be built independently.

| Stage | Recipe | Release | Purpose |
| --- | --- | --- | --- |
| 1, if missing | [xorg-util-macros](devario-development/xorg-util-macros/PKGBUILD) | `1.20.2-1` | X.Org build macros |
| 1, if missing | [xmlto](devario-development/xmlto/PKGBUILD) | `0.0.29-1` | Yasm documentation |
| 1 | [wasi-libc++](devario-core/wasi-libc++/PKGBUILD) | `23.1.1-1` | Both `wasi-libc++` and `wasi-libc++abi` |
| 2 | [xorg-font-util](devario-development/xorg-font-util/PKGBUILD) | `1.4.2-1` | Imake build prerequisite |
| 2 | [yasm](devario-development/yasm/PKGBUILD) | `1.3.0-9` | Assembler |
| 3 | [imake](devario-development/imake/PKGBUILD) | `1.0.11-1` | X.Org build utilities |

For each recipe, run `shelly build --isolated --check ./path/to/PKGBUILD`,
publish its binary outputs to an enabled worker repository, and refresh
the worker's metadata before the next dependent stage. Publish both WASI
outputs together: `wasi-libc++` requires the matching
`wasi-libc++abi=23.1.1-1` package. Then retry the original blocked build.
Uploading recipes alone does not satisfy the repository checks.

The saved 2026-10-08 catalogs lack `xorg-util-macros`, `xorg-font-util`, and
`xmlto`; the worker's current enabled repositories are authoritative.
All other direct dependency names of these recipes resolve to saved binary
providers or the WASI split output. WASI requires existing `wasi-libc` and
`wasi-compiler-rt` packages, plus the LLVM tools and `wasm-component-ld`.
Those providers are in the saved catalogs. If absent on the worker, restore
compatible seed packages before rebuilding: the existing WASI libc/runtime
recipes have a dependency cycle. Yasm's checked build also requires systemd.

Validation: the four imports pass shell syntax checks, generated `.SRCINFO`
comparison, and Shelly review with no findings. All downloaded sources and
bundled patches pass their declared checksums; the X.Org and LLVM source
signatures pass verification with the bundled keys. Isolated builds and
binary publication have not been performed.

## Systemd: quota, kexec, FIDO2 and PE dependencies (2026-10-13)

The worker's `IncompleteDependencyPlan` for `devario-core/systemd` names
four missing binary packages: `quota-tools`, `kexec-tools`, `libfido2`, and
`python-pefile`. The repeated entries correspond to systemd's six split
outputs and the repository/environment checks. Uploading a recipe does not
satisfy these checks; its binary must be published in an enabled worker
repository before systemd is provisioned.

Recipes for quota-tools, kexec-tools, and libfido2 are now included, imported
from their Arch packaging repositories with source checksums, signing keys,
attribution, and packaging licenses intact:
[quota-tools](https://gitlab.archlinux.org/archlinux/packaging/packages/quota-tools),
[kexec-tools](https://gitlab.archlinux.org/archlinux/packaging/packages/kexec-tools),
and [libfido2](https://gitlab.archlinux.org/archlinux/packaging/packages/libfido2).
The existing python-pefile recipe needs no change.

Build and publish in this order, satisfying the other declared dependencies
before each build. Entries in the same stage may be built independently.

| Stage | Recipe | Release | Needed by |
| --- | --- | --- | --- |
| 1, if missing | [rpcsvc-proto](devario-development/rpcsvc-proto/PKGBUILD) | `1.4.4-2` | quota-tools |
| 1, if missing | [libcbor](devario-libs/libcbor/PKGBUILD) | `0.14.0-1` | libfido2 |
| 2 | [quota-tools](devario-core/quota-tools/PKGBUILD) | `1:4.11-1` | systemd |
| 2 | [kexec-tools](devario-core/kexec-tools/PKGBUILD) | `2.0.32-1` | systemd |
| 2 | [libfido2](devario-libs/libfido2/PKGBUILD) | `1.17.0-1` | systemd |
| 2 | [python-pefile](devario-libs/python-pefile/PKGBUILD) | `2024.8.26-2` | systemd and systemd-ukify |
| 3 | [systemd](devario-core/systemd/PKGBUILD) | `262-9` | Full split package set |

`rpcsvc-proto` and `libcbor` were absent from the saved 2026-10-08 binary
catalogs; all other direct dependency names of the four recipes were present.
The worker's current repositories are authoritative. Libcbor also needs
`cmocka` for its build/tests. Libfido2 needs existing `systemd` and
`systemd-libs` packages: use the existing systemd seed and the
[systemd-libs bootstrap procedure](ABI-BUILDS.md#libfido2-and-bpf-build-root-providers)
if the library provider is unavailable. Building the full systemd recipe
first would reintroduce the dependency cycle.

The subsequent quota-tools worker failure confirms that `rpcsvc-proto` is
missing from its repositories and environment. Its existing `1.4.4-2`
recipe declares only `glibc` as a package dependency and uses the standard
base-devel tools (including Autoconf and Automake). Build it first:

```sh
shelly build --isolated --check ./devario-development/rpcsvc-proto/PKGBUILD
```

Publish the resulting `rpcsvc-proto` binary to a repository enabled on the
worker and refresh its metadata before retrying quota-tools:

```sh
shelly build --isolated --check ./devario-core/quota-tools/PKGBUILD
```

The rpcsvc-proto recipe passes shell syntax, generated `.SRCINFO` comparison,
and Shelly review with no findings; no recipe change is needed for this
dependency-plan error. Its isolated build and publication remain worker steps.

The subsequent libfido2 worker failure confirms that `libcbor` is also
missing. Both `libcbor` and `libcbor.so` are satisfied by the single libcbor
binary: its existing recipe explicitly declares `provides=('libcbor.so')`.
Build and publish it before retrying libfido2:

```sh
shelly build --isolated --check ./devario-libs/libcbor/PKGBUILD
# Publish libcbor and refresh the worker's repository metadata first.
shelly build --isolated --check ./devario-libs/libfido2/PKGBUILD
```

Libcbor requires `glibc`, `cmake`, and `cmocka`. If cmocka is unavailable on
the worker, build and publish the existing
[cmocka recipe](devario-development/cmocka/PKGBUILD) first. Libcbor's shell
syntax, generated `.SRCINFO`, and Shelly review pass with no findings;
no recipe change is needed for these two missing dependency names. Its
isolated build and publication remain worker steps.

After the user reported building the prerequisites, a live public-index check
on 2026-10-13 found `cmocka-2.0.2-1` and `rpcsvc-proto-1.4.4-2` in
`devario-development`, and `quota-tools-1:4.11-1` in `devario-core`.
However, libcbor was absent from both the origin and mirror
`devario-libs.db` indexes, the core/development indexes, and the
[public libcbor search](https://repo.seafoam-labs.org/api/v1/packages?q=libcbor).
This confirms a public availability gap, but does not establish whether the
libcbor job failed during building, signing, publication, or repository sync.
Inspect that job's final output and artifact/publication status before
rebuilding or changing dependency declarations. Refreshing worker metadata
alone cannot expose a package absent from its upstream index.

The libcbor job log subsequently showed `DownloadSizeMismatch` during
`shellystrap` provisioning, followed by `IsolatedBootstrapFailed`. Compilation
never started. In this log, “Publishing downloads” means publishing verified
bootstrap downloads into the build-root cache, not publishing libcbor to a
repository. `Package: rlpm` names the backend, not the failing archive.
The download implementation processes the batch before returning its first
failure, so the final successful `which` entry does not identify that archive.

On 2026-10-13, a dependency traversal of current core/development/libs indexes
and Shelly's RLPM bootstrap targets plus libcbor's dependencies resolved 175
packages, matching the log's total. All 175 public mirror payloads were then
downloaded and matched their indexed byte counts and SHA-256 hashes (about
509 MB total). This does not establish which metadata or mirror the worker
used at failure time, nor does it verify package signatures or provisioning.
Retry libcbor in a fresh isolated job against current metadata. If it still
fails, retain the full download log and worker repository configuration to
identify the failed filename and compare its expected/actual size and hash.
Do not change libcbor's dependency declarations or disable integrity checks
to work around this provisioning failure.

Copy each complete recipe directory, including `keys/` where present, and
refresh the worker's repository metadata after publishing each prerequisite
stage. Then retry:

```sh
shelly build --isolated --check ./devario-core/systemd/PKGBUILD
```

Validation: all four dependency recipes pass `bash -n`, generated `.SRCINFO`
comparison, and Shelly review with no findings. Downloaded sources pass all
declared checksums; kexec-tools' signed tag and libfido2's detached signature
verify with the bundled keys. Libfido2 verification reports that the signing
key has expired, while accepting the source signature. Every direct dependency name resolves to a
local recipe or saved binary-catalog provider. Isolated builds and binary
publication have not been performed.

## Fastfetch: image, display, JavaScript and Xfce dependencies (2026-10-13)

The worker reports `chafa`, `ddcutil`, `efl`, `quickjs-ng`, and `xfconf`
as both `not_in_repositories` and `not_in_environment` while provisioning
`devario-core/fastfetch`. These are five missing binary packages. Recipes
for all five are now under `devario-core`, together with four missing
prerequisite recipes needed by EFL and Xfconf.

Build and publish in this order, provisioning each recipe's other declared
dependencies first. Recipes in the same stage do not depend on one another.

| Stage | Recipe | Release | Needed by |
| --- | --- | --- | --- |
| 1 | [chafa](devario-core/chafa/PKGBUILD) | `1.18.3-1` | Fastfetch |
| 1 | [ddcutil](devario-core/ddcutil/PKGBUILD) | `3.0.2-1` | Fastfetch |
| 1 | [quickjs-ng](devario-core/quickjs-ng/PKGBUILD) | `0.17.0-1` | Fastfetch |
| 1 | [lua52](devario-core/lua52/PKGBUILD) | `5.2.4-8` | EFL |
| 1 | [scim](devario-core/scim/PKGBUILD) | `1.4.18-6` | EFL |
| 1 | [xfce4-dev-tools](devario-core/xfce4-dev-tools/PKGBUILD) | `4.20.0-2` | libxfce4util, Xfconf |
| 2 | [efl](devario-core/efl/PKGBUILD) | `1.28.1-4` | Fastfetch |
| 2 | [libxfce4util](devario-core/libxfce4util/PKGBUILD) | `4.20.1-1` | Xfconf |
| 3 | [xfconf](devario-core/xfconf/PKGBUILD) | `4.20.0-2` | Fastfetch |
| 4 | [fastfetch](devario-core/fastfetch/PKGBUILD) | `2.69.0-3` | Devario terminal welcome |

Other prerequisites already have local recipes but were absent from the
saved binary catalogs: `gtk-doc`, `libavif`, `libheif`, `i2c-tools`,
`libspectre`, `poppler`, `texlive-basic`, `texlive-fontutils`, and `vala`.
Check their availability on the worker before starting the stages above.
The two TeX Live outputs come from `devario-utilities/texlive-texmf`.
Use the existing Vala bootstrap workflow if Vala is not yet available.
The inventory comparison uses the saved 2026-10-08 catalogs; the worker's
current enabled repositories remain authoritative for binary availability
and version constraints.

The existing [i2c-tools recipe](devario-utilities/i2c-tools/PKGBUILD),
`4.4-4`, supplies ddcutil's I2C dependency. Build and publish it before
ddcutil if its binary is unavailable:

```sh
shelly build --isolated --check ./devario-utilities/i2c-tools/PKGBUILD
```

SCIM `1.4.18-6` patches the IMdkit transport address callback with its
three-argument prototype and removes the obsolete function-pointer cast
from the table's null sentinel. This fixes the GCC 16 errors in
`i18nMethod.c` without changing compiler defaults or suppressing diagnostics.
See GCC's [C23 porting notes](https://gcc.gnu.org/gcc-15/porting_to.html)
for the changed meaning of empty parameter lists.

All nine imports retain upstream source pins, checksums, attribution, and
packaging licenses. Copy each entire recipe directory to the worker:
Lua 5.2 includes its shared-library patch, pkg-config template, and license;
SCIM includes its callback patch and installation scriptlet; Chafa includes
the public key for its signed Git tag. These recipes retain Fastfetch's optional detection
features and do not require the Pacman executable.

For example, after publishing the prerequisites:

```sh
shelly build --isolated --check ./devario-core/quickjs-ng/PKGBUILD
```

Publish the resulting binaries to the worker's enabled repository and refresh
its metadata between stages, then retry Fastfetch's dependency plan.
Uploading recipes alone does not satisfy `not_in_repositories`.

Validation: all nine recipes pass shell syntax, generated `.SRCINFO`
comparison, Shelly review parsing, and downloaded-source checksum validation.
Chafa's signed Git tag also passes verification with its bundled public key.
Their declared runtime, build, and
check dependency names resolve to a local recipe or a saved binary-catalog
provider. Isolated builds and signed binary publication remain worker steps.

SCIM validation: reproduced the original failure with GCC 16, then passed
the patched recipe's full build and staged install using the worker's
optimization and linker flags. The affected translation unit also passes
C17 and C23 syntax checks with incompatible-pointer diagnostics treated as
errors, including the optional TCP and DECnet table entries. SCIM's source
and patch checksums, metadata, and Shelly review pass. The existing
`i2c-tools` recipe passes shell syntax, metadata comparison, bundled-file
checksum verification, and Shelly review.

## Thrift: Emacs Tree-sitter dependency (2026-10-11)

The worker's `IncompleteDependencyPlan: emacs-nox: libtree-sitter.so
(unsatisfied_dependency)` occurs while provisioning Thrift's build
dependencies. [Thrift](devario-libs/thrift/PKGBUILD) uses `emacs-nox` to
byte-compile `contrib/thrift.el`; Emacs in turn requires the Tree-sitter
shared library. Keep both dependency declarations.

The existing [tree-sitter recipe](devario-development/tree-sitter/PKGBUILD)
`0.26.9-1` and its `.SRCINFO` already declare `libtree-sitter.so` in the
`tree-sitter` output's `provides`. The separate `tree-sitter-cli` output
does not provide this library.

1. Build and publish `tree-sitter` from that split recipe (stage 01),
   provisioning its own build dependencies first. Ensure the library output
   is included in the worker's enabled binary repository.
2. Refresh the worker's repository metadata and resolve `emacs-nox` with
   its full runtime dependencies. If Emacs is not yet published, build
   [the Emacs recipe](devario-core/emacs/PKGBUILD) after Tree-sitter and
   publish its `emacs-nox` output. Install only one Emacs variant in the root.
3. Retry `devario-libs/thrift` (stage 05), then its consumers such as Arrow.

If Tree-sitter is already published, check that the worker sees its library
output and `provides` metadata. Match the built Emacs package's actual ABI
requirement: the local host's cached repository metadata lists
`libtree-sitter.so=0.26-64` for both Tree-sitter's provision and Emacs's
dependency. This host metadata does not establish worker availability.
Uploading recipes alone cannot supply the missing binary dependency.

Validation: Tree-sitter, core Emacs, and Thrift pass `bash -n`; all three
checked-in `.SRCINFO` files exactly match fresh `makepkg --printsrcinfo`
output. No recipe changes, isolated builds, binary publication, or live
worker repository checks were performed.

## Arrow dependency plan (2026-10-11)

The worker reports `grpc`, `re2`, and `thrift` missing from both its enabled
binary repositories and isolated environment when provisioning
[arrow](devario-libs/arrow/PKGBUILD) `25.0.1-7`. All three recipes already
exist and produce the required package names. Arrow selects system
dependencies with `ARROW_DEPENDENCY_SOURCE=SYSTEM`; its dependency
declarations do not need renaming or removal.

Build and publish these prerequisites in the stages from
[the repository build order](LATEST-BUILD-ORDER.md), skipping packages
already available to the worker:

| Stage | Recipe | Required output / release |
| --- | --- | --- |
| 01 | [re2](devario-libs/re2/PKGBUILD) | `re2` `2:2025.11.05-7` |
| 05 | [thrift](devario-libs/thrift/PKGBUILD) | `thrift` `0.22.0-6` |
| 11 | [grpc](devario-libs/grpc/PKGBUILD) | `grpc` `1.84.0-2` |
| 12 | [arrow](devario-libs/arrow/PKGBUILD) | `arrow` `25.0.1-7` |

Publish re2 before building gRPC, which also requires it. Build each split
recipe once: Thrift also builds Python bindings, and gRPC builds Python and
PHP bindings plus its CLI. Provision each recipe's full build requirements,
including Thrift's `emacs-nox` and `qt5-base`, and gRPC's `php`, `php-legacy`,
and Python build tools. The gRPC recipe requires the installed protobuf
version to match its pinned `36.1`. This table covers the reported missing
packages, not their complete transitive dependency closure.

RE2 release `2:2025.11.05-7` moves `gtest` and `benchmark` from
`checkdepends` to `makedepends`: `RE2_BUILD_TESTING=ON` requires both during
`build()`, even when the worker skips `check()`. The previous release could
fail CMake configuration because `benchmarkConfig.cmake` was missing.
Build and publish [benchmark](devario-libs/benchmark/PKGBUILD) first if it
is unavailable to the worker. The reported build already found GTest
`1.18.0`; keep that dependency available as well. Upload the updated RE2
recipe and `.SRCINFO` and retry.

Publish the resulting binary packages to the worker's enabled repository
and refresh its repository metadata before provisioning consumers. If the
packages are already published, check repository enablement and refresh
the worker's metadata before retrying Arrow. Uploading recipes alone does
not supply the missing binaries.

Validation: all four recipes pass `bash -n`, and their checked-in
`.SRCINFO` files exactly match fresh `makepkg --printsrcinfo` output.
RE2's dependency metadata and release were updated; no isolated builds,
binary publication, or live worker repository checks were performed.

## VTK dependency plan (2026-10-11)

The worker reports 19 distinct missing build dependencies for
[vtk](devario-libs/vtk/PKGBUILD) `9.7.1-2`. Each appears twice because it is
absent from both the enabled binary repositories and the isolated environment.
All 19 already have recipes here, with package names matching VTK's
`makedepends`. Uploading recipes alone does not satisfy these requirements.
The modules enabled by this recipe require these dependencies during the
build, even where they are optional for users of the resulting package.

Build and publish the following prerequisites in the stages from
[the repository build order](LATEST-BUILD-ORDER.md). This table is a subset
for the reported failure, not a complete transitive dependency queue: provision
each recipe's own runtime/build requirements first, using the full order when
those packages are also unpublished. Skip outputs already available from the
worker's enabled repositories. Use `--no-check` for this queue, as in the
full build order; this does not omit dependencies declared in `makedepends`.

| Stage | Recipes to build and publish |
| --- | --- |
| 01 | [cli11](devario-development/cli11/PKGBUILD), [openvr](devario-development/openvr/PKGBUILD), [proj](devario-libs/proj/PKGBUILD), [utf8cpp](devario-development/utf8cpp/PKGBUILD), [viskores](devario-libs/viskores/PKGBUILD) |
| 02 | [netcdf](devario-libs/netcdf/PKGBUILD) |
| 03 | [cgns](devario-development/cgns/PKGBUILD) |
| 04 | [openimagedenoise](devario-libs/openimagedenoise/PKGBUILD) |
| 05 | [python-mpi4py](devario-libs/python-mpi4py/PKGBUILD) |
| 06 | [paraview-catalyst](devario-libs/paraview-catalyst/PKGBUILD) |
| 07 | [adios2](devario-development/adios2/PKGBUILD), [openvdb](devario-libs/openvdb/PKGBUILD) |
| 09 | [ospray](devario-development/ospray/PKGBUILD) |
| 12 | [gl2ps](devario-libs/gl2ps/PKGBUILD) |
| 18 | [gdal](devario-libs/gdal/PKGBUILD) |
| 19 | [liblas](devario-libs/liblas/PKGBUILD), [pdal](devario-libs/pdal/PKGBUILD), [python-matplotlib](devario-libs/python-matplotlib/PKGBUILD) |
| 22 | [opencascade](devario-development/opencascade/PKGBUILD) as the seed, then [vtk](devario-libs/vtk/PKGBUILD), then opencascade again |

Publish completed dependencies and refresh the worker's repository metadata
before provisioning their consumers. In particular, ADIOS2 needs mpi4py and
ParaView Catalyst; OSPRay needs Open Image Denoise; GDAL needs PROJ and netCDF;
libLAS and PDAL need GDAL. Build split recipes once and publish their outputs.

OpenCascade and VTK need each other to build: OpenCascade's IVtk toolkits link
VTK at runtime, while VTK's OCCT I/O module needs OpenCascade at configure
time. Shelly resolves both arrays before the build starts, so an isolated root
can provision neither recipe while both are unpublished, and reordering the two
full recipes cannot break that. OpenCascade is the seeded side because its VTK
use is additive: upstream excludes only TKIVtk and TKIVtkDraw when `USE_VTK=OFF`
and unsets the whole `3RDPARTY_VTK` cache group, so the recipe's
`3RDPARTY_VTK_INCLUDE_DIR` is inert and needs no edit, and TKDraw's one
`HAVE_VTK` site at this tag is a string in a DRAW version command. The excluded
toolkits are the only VTK consumers in the tree: `src/TKIVtk/EXTERNLIB` names
`CSF_VTK`, `vtkCommonCore` and `vtkRenderingCore`, so IVtk links VTK and VTK
cannot consume IVtk. The seed therefore ships every toolkit VTK's OCCT I/O
module needs.

The seed ran: OpenCascade published as `1:7.9.3-4` with VTK support off, and
the recipe is now restored to upstream `USE_VTK=ON` with the `vtk` depends and
`pkgrel=5`. Nothing between the seed and the republish can consume IVtk, and no
recipe here does. Do not queue `1:7.9.3-5` before VTK publishes: its global
`vtk` depends is what the seed removed, so an earlier attempt fails dependency
resolution and leaves the seed as the published package.

Validation: VTK and all 19 reported dependency recipes pass `bash -n`, and
all 20 checked-in `.SRCINFO` files exactly match fresh
`makepkg --printsrcinfo` output. Isolated builds, binary publication, and the
worker's repository state were not checked on 2026-10-11.

Re-queried against the packages API on 2026-10-12, `opencascade` `1:7.9.3-4` is
published in devario-development as the seed and `vtk` is not. The seed's
repository record carries the nine non-VTK depends and its file list contains no
IVtk path, so `USE_VTK=OFF` took effect. Those 67 `libTK*` kits are the ones VTK
links; the republish adds only libTKIVtk and libTKIVtkDraw.
`gl2ps` published the same morning, `onnxruntime` comes from the
`onnxruntime-cpu`, `-cuda` and `-rocm` splits, `java-environment=11` from
`jdk11-openjdk`, and with `liblas` published at 09:26 all 69 of VTK's pkgbase
entries resolve. VTK was still in the worker queue when this restore was
committed.

## rocThrust and its dependency builds (2026-10-10)

[rocthrust](devario-libs/rocthrust/PKGBUILD) now packages `10.0-1` from the
checksum-pinned `therock-10.0` component archive, matching the existing
[rocprim](devario-libs/rocprim/PKGBUILD) `10.0-1` recipe. Both component
archives report library version `4.6.0`; `10.0` is their release archive
version. The rocThrust recipe requires `rocprim>=10.0`, explicitly selects
the installed rocPRIM package, and installs headers and CMake targets into
`/opt/rocm`. Tests, examples, and benchmarks are disabled for this package.
The source is the component archive rather than the entire ROCm libraries
repository.

All required ROCm dependency recipes already exist. Build the following in
stage order, skipping packages already published to the worker's enabled
repositories. Build each split recipe once and publish its outputs before
starting dependent stages.

| Stage | Recipe | Required outputs / release |
| --- | --- | --- |
| 1 | [rocm-core](devario-core/rocm-core/PKGBUILD) | `rocm-core` `7.2.4-1` |
| 1 | [rocm-toolchain](devario-development/rocm-toolchain/PKGBUILD) | `rocm-toolchain` `0.4.0-2`, providing `rocm-supported-gfx` |
| 2 | [rocm-cmake](devario-core/rocm-cmake/PKGBUILD) | `rocm-cmake` `7.2.4-1` |
| 3 | [rocm-llvm](devario-core/rocm-llvm/PKGBUILD) | `2:7.2.4-3`: `rocm-llvm`, `rocm-llvm-libs`, `rocm-mlir-libs`, `rocm-llvm-tools`, `rocm-llvm-headers`, `rocm-llvm-static`, `rocm-device-libs`, and `comgr` |
| 3 | [rocprofiler-register](devario-core/rocprofiler-register/PKGBUILD) | `rocprofiler-register` `7.2.4-1` |
| 4 | [hsa-rocr](devario-core/hsa-rocr/PKGBUILD) | `hsa-rocr` `7.2.4-2` (also provides `hsakmt-roct`) |
| 5 | [rocminfo](devario-core/rocminfo/PKGBUILD) | `rocminfo` `7.2.4-1` |
| 6 | [hip-runtime](devario-core/hip-runtime/PKGBUILD) | `hip-runtime-amd` `7.2.4-2` |
| 7 | [rocprim](devario-libs/rocprim/PKGBUILD) | `rocprim` `10.0-1` |
| 8 | [rocthrust](devario-libs/rocthrust/PKGBUILD) | `rocthrust` `10.0-1` |

Use an existing base development environment and provision the ordinary
runtime/build dependencies declared by these recipes: `bash`, `cmake`,
`cuda`, `fmt`, `gcc-libs`, `git`, `glibc`, `google-glog`, `libdrm`, `libedit`,
`libelf`, `libffi`, `libgcc`, `libstdc++`, `libxml2`, `mesa`, `ncurses`,
`ninja`, `numactl`, `patchelf`, `pciutils`, `perl`, `python`,
`python-cppheaderparser`, `python-prettytable`, `python-pyaml`,
`python-pyelftools`, `xxd`, `zlib`, and `zstd`. Resolve their ordinary
dependencies from the worker repositories. The existing
[tinyxxd](devario-core/tinyxxd/PKGBUILD) recipe provides `xxd`.
The HIP split recipe builds both AMD and NVIDIA outputs, so it needs `cuda`
at build time even when only `hip-runtime-amd` is wanted.

This order assumes checks are disabled (`shelly build --no-check` or
`makepkg --nocheck`): rocm-cmake's checks need an existing rocm-llvm package.
rocThrust itself needs `rocm-core`, `hip-runtime-amd`, and `rocprim` at
runtime, plus `cmake`, `rocm-cmake`, `rocm-toolchain`, and `rocm-llvm` to
build. rocRAND, Google Test, Google Benchmark, and SQLite are dependencies
of optional upstream client builds and are not needed for the packaged
headers. Refresh repository metadata after publishing each stage; recipe
uploads alone do not supply dependencies to an isolated build root.

Validation: all ten recipes pass `bash -n` and regenerate their checked-in
`.SRCINFO` exactly; Shelly and makepkg agree on the updated rocThrust
metadata. Both component archive SHA-256 checksums were verified. The
rocPRIM and rocThrust `build()` and `package()` functions completed in a
temporary root using packaged ROCm `7.2.4` dependencies, with `gfx1030` as
the validation target. An external CMake consumer found `rocthrust 4.6`,
linked its object target to `roc::rocthrust`, and compiled host/device
vector, sort, and reduction code for `gfx1030`. No GPU execution, full
toolchain rebuild, binary package publication, or host installation was
performed.

## rocSOLVER dependency plan (2026-10-10)

The worker's `IncompleteDependencyPlan` reports `rocblas` and `rocsparse`
missing from both its repositories and build environment. Both recipes already
exist here, and rocSOLVER's dependency names match their package outputs.
The subsequent rocSPARSE dependency plan also reports `rocprim` missing.
Its existing recipe produces `rocprim` `10.0-1`; no dependency rename is
needed. rocSPARSE requires both rocPRIM and rocBLAS, so build and publish in
this order (skip prerequisites already available in the worker repository):

| Order | Recipe | Release |
| --- | --- | --- |
| 1 | [rocprim](devario-libs/rocprim/PKGBUILD) | `10.0-1` |
| 2 | [rocblas](devario-libs/rocblas/PKGBUILD) | `7.2.4-5` |
| 3 | [rocsparse](devario-libs/rocsparse/PKGBUILD) | `7.2.4-1` |
| 4 | [rocsolver](devario-libs/rocsolver/PKGBUILD) | `7.2.4-1` |

rocPRIM requires `rocm-core` and `hip-runtime-amd`, plus `cmake`, `rocm-cmake`,
`rocm-toolchain`, and `rocm-llvm` at build time. Make these available in its
isolated root before building it.

Use the updated rocBLAS recipe described below. Publish each dependency's
built archive to the worker's enabled `devario-libs` repository and refresh
its repository metadata before starting the next recipe. If the archives are
already published, check that the worker enables that repository and has
refreshed its metadata. Uploading recipes alone does not make their binary
packages available to an isolated build.

Validation: all four recipes pass `bash -n`, and Shelly-generated metadata
matches their checked-in `.SRCINFO` files. No recipe changes are needed for
this reported dependency failure. Builds and publication were not performed.

## rocBLAS bundled Tensile selection (2026-10-10)

Retry [rocblas](devario-libs/rocblas/PKGBUILD) with release `7.2.4-5`.
Its previous configuration set `BUILD_WITH_PIP=OFF`, which bypasses the
`Tensile_TEST_LOCAL_PATH` handling in the
[pinned upstream CMakeLists](https://github.com/ROCm/rocm-libraries/blob/dabb6df2b988f8eabed1e2fecefaaf4e818bc7ef/projects/rocblas/CMakeLists.txt).
CMake instead found the system `python-tensile` package's Tensile 4.47.0,
which fails rocBLAS's exact 4.45.0 requirement.

The recipe now sets `Tensile_DIR` and `Tensile_ROOT` to the matching Tensile
4.45.0 already included in the pinned ROCm source tree. `PYTHONPATH` puts
that source tree first so its generator cannot import a different installed
Tensile. The unused `python-tensile`, `python-virtualenv`, and `python-wheel`
build requirements are removed; `python-rich`, declared by bundled Tensile's
`requirements.txt`, is added. The exact version check remains enforced, and
`BUILD_WITH_PIP=OFF` still prevents configure-time installation.

Validation: shell syntax and metadata checks passed; makepkg and Shelly emit
matching `.SRCINFO`. Shelly review reports only the existing dynamic-command
warnings for CPU count and GPU target detection. A focused CMake project using
the pinned Tensile sources and temporary ROCm 7.2.4 packages successfully ran
`find_package(Tensile 4.45.0 EXACT REQUIRED HIP LLVM)` and generated the
`TensileHost` target for `gfx1030`. The bundled Python module reported 4.45.0,
and `TensileCreateLibrary --help` completed with its Python dependencies.
Full rocBLAS compilation and GPU kernel generation were not run. Upload the
updated recipe and `.SRCINFO`, refresh worker recipe metadata, and retry.

Build and publish `devario-installer/devario-base` 3-15 before the next ISO
rebuild to include `devario-productivity` and `devario-libs` in `/etc/shelly.conf`.
The default configuration no longer includes `devario-scx`.

Build and publish `devario-core/netcat` 1.238_1-1 before the next ISO rebuild.
It packages Debian's OpenBSD netcat port as `netcat`, provides `openbsd-netcat`,
and installs `nc`, `netcat`, and `nc.openbsd`. The recipe applies the upstream
Linux patches, includes both BSD licenses and runs the upstream client/server
checks. Devario's ISO and repository package lists now also include `ripgrep`.

Build and publish `devario-core/power-profiles-daemon` 0.30-1 before the next
Devario ISO rebuild. The recipe uses the checksum-pinned upstream release,
includes D-Bus activation and polkit policy, and runs upstream tests through
Meson. The ISO now requests this package and starts it alongside UPower in
live and installed sessions so Pearl can show battery status and power profiles.

For the current core-only ISO, upload the complete recipe directories below.
These releases move system hooks and their helpers to `/usr/share/rlpm/`,
public key bundles to `/usr/share/shelly/keyrings/`, and mutable state and
configuration to Shelly paths. They require the patched Shelly CLI/key tools
built with `-Dpath-profile=devario` and support for `HookDirMode = Replace`.

| Rebuild recipe | Release | Location |
| --- | --- | --- |
| glibc | 2.44+r50+g1848099f063e-2 | `devario-core/glibc` |
| glib2 | 2.90.0-2 | `devario-core/glib2` |
| dbus | 1.16.2-3 | `devario-core/dbus` |
| systemd | 262-8 | `devario-core/systemd` |
| devario-dracut | 112-5 | `devario-core/devario-dracut` |
| devario-keyring | 20260923-2 | `devario-installer/devario-keyring` |
| devario-boot | 1-7 | `devario-installer/devario-boot` |
| devario-base | 3-12 | `devario-installer/devario-base` |

`devario-boot` 1-7 replaces installed Limine with systemd-boot. Build and
publish it before `devario-base` 3-12, which requires that release. Installation
now requires 64-bit UEFI and a FAT EFI System Partition at `/boot`. The live ISO
retains its BIOS Syslinux support, so `syslinux` remains in the rebuild list.
The boot recipe retains the legacy hook mask and migrates an existing Devario
Limine marker only after successful UEFI deployment.

`devario-base` 3-12 also requires Fish and `shadow>=4.20.0.arch1-3`.
Build and publish `devario-core/fish` 4.9.3-1 and `devario-core/shadow`
4.20.0.arch1-3 before base and ISO assembly. The Shadow release sets
`useradd`'s default shell to `/usr/bin/fish`; the ISO profile applies the
same default to the live user and Calamares-created accounts.

A subsequent audit of the complete signed repository file inventory found
17 additional recipe bases. Their recipes and supporting files are now in
`devario-core`, imported from the upstream packaging tags matching the published
versions. Each PKGBUILD records its upstream packaging commit. Hook/helper
installation paths, hook commands, and install-script references now use
`/usr/share/rlpm/`; package releases and bundled-source checksums are updated.

| Additional rebuild recipe | New version | Location |
| --- | --- | --- |
| accountsservice | 26.27.3-2 | [recipe](devario-core/accountsservice/PKGBUILD) |
| appstream | 1.2.1-2 | [recipe](devario-core/appstream/PKGBUILD) |
| ca-certificates | 20240618-2 | [recipe](devario-core/ca-certificates/PKGBUILD) |
| dconf | 51.0-2 | [recipe](devario-core/dconf/PKGBUILD) |
| desktop-file-utils | 0.28-2 | [recipe](devario-core/desktop-file-utils/PKGBUILD) |
| dkms | 3.4.3-3 | [recipe](devario-core/dkms/PKGBUILD) |
| fontconfig | 2:2.18.3-3 | [recipe](devario-core/fontconfig/PKGBUILD) |
| gdk-pixbuf2 | 2.44.8-2 | [recipe](devario-core/gdk-pixbuf2/PKGBUILD) |
| gtk3 | 1:3.24.52-3 | [recipe](devario-core/gtk3/PKGBUILD) |
| gtk4 | 1:4.24.1-2 | [recipe](devario-core/gtk4/PKGBUILD) |
| gvfs | 1.62.0-4 | [recipe](devario-core/gvfs/PKGBUILD) |
| kmod | 34.2-2 | [recipe](devario-core/kmod/PKGBUILD) |
| man-db | 2.13.1-4 | [recipe](devario-core/man-db/PKGBUILD) |
| openssh | 10.5p1-2 | [recipe](devario-core/openssh/PKGBUILD) |
| perl | 5.42.3-2 | [recipe](devario-core/perl/PKGBUILD) |
| shared-mime-info | 2.5.1-3 | [recipe](devario-core/shared-mime-info/PKGBUILD) |
| syslinux | 6.04.pre3.r3.g05ac953c-6 | [recipe](devario-core/syslinux/PKGBUILD) |

Publish all matching split outputs together, including `ca-certificates-utils`
from `ca-certificates` and `gtk-update-icon-cache` from `gtk4`. Keep each complete
recipe directory, including any `keys/pgp` public keys, when uploading to Remora.
Perl's old-module hook now reads `/var/lib/shelly/local` directly for package
ownership; it no longer requires the legacy package-manager command. DKMS's
hook debugging variable is now `DKMS_RLPM_HOOK_DEBUG`.
The imported install scripts also avoid the unavailable `vercmp` executable:
CA certificate migration checks the old directory directly, fresh dconf and
fontconfig installs retain their initialization, and obsolete pre-Devario
upgrade notices/migrations are removed.

Validation for these 17 recipes: metadata generation and Shelly review completed,
32 shell files passed syntax checks, and all 81 checksums for 70 bundled source
files matched. Four Perl hook fixture tests passed. Shelly's static review still
reports dynamic-command warnings in upstream helper scripts and patch text.
Full isolated compilation and publication have not been performed.

The published `systemd` and `devario-dracut` archives also still use old paths;
the local recipes above already include their fixes. Rebuilding devario-dracut
also restores its `initramfs` provision, avoiding the old `dracut-git` provider.

The published Shelly CLI at `832de83c` supports explicit configuration but still
uses the old public key directory. Build upstream revision
`1913c78d272f6b8c53531d02181f024b78708d2b` or newer with the Devario profile.

Build each split recipe once and publish its matching outputs together;
`glibc` includes `lib32-glibc`. Build boot after dracut, and base after boot
and keyring. Keep using the existing published bootstrap dependencies for
cycles among glib2, D-Bus, and systemd.

The ISO workflow now prepares an isolated Python validation environment from
hash-pinned upstream wheels. The 15 Python recipes from the previous work are
optional and are no longer required for the ISO or Remora build list.
Publish `nbd` 3.27.1-4 to `devario-core` if still missing; its existing recipe
needs no additional path changes. The original local list is the eight rebuild targets above plus `nbd`; the
additional recipes listed above must also be rebuilt and published before ISO construction.
The ISO uses the published `devario-desktop` and stable `pearl-greeter`;
`seafoam-keyring` is not a default ISO requirement.

Validation for the eight path updates: Bash syntax, regenerated makepkg
metadata, and 68 bundled-source checksums passed. Staged package functions
for base, boot, and keyring produced the expected paths and boot hook masks.
The OS repository's three matching recipes are synchronized. Full compilation,
isolated Remora builds, and publication of these releases remain to be done.
The ISO builder and verification script path migration is now implemented.
Repository publication remains separate from these local source changes.

For Zig 0.16 and its LLVM 21, CMake, GCC, and Python prerequisites, see
[the Zig build guide](ZIG-BUILDS.md).

Devario is an independent operating system. These x86_64 recipes are adapted
from the corresponding
[Arch Linux packaging repositories](https://gitlab.archlinux.org/archlinux/packaging/packages).
Those links record recipe provenance.
Each directory includes its PKGBUILD, generated `.SRCINFO`, and required local
source files. Copy whole directories to the Remora worker.

## Remaining ISO runtime and OS-owned recipes

General runtime recipes are available under `devario-core/`:

| Directory | Version | Build/publish order |
| --- | --- | --- |
| `composefs` | 1.0.8-1 | Before provisioning ostree/Flatpak consumers |
| `ding-libs` | 0.7.0-1 | Before GSSProxy; an additional missing runtime dependency |
| `gssproxy` | 0.9.2-4 | After ding-libs; before NFS consumers |
| `rpcbind` | 1.3.1-3 | Before NFS consumers |
| `libmalcontent` | 0.14.0-5 | Before Flatpak; library-only bootstrap avoids the Flatpak UI cycle |
| `xdg-dbus-proxy` | 0.1.9-2 | Before Flatpak; declares D-Bus for its tests |
| `inter-font` | 4.1-1 | Existing recipe; publish before Calamares |

OS-owned live USB and installer recipes are in
[`devario-installer/`](devario-installer/README.md):

| Directory | Version | Build/publish order |
| --- | --- | --- |
| `devario-filesystem` | 1-2 | Before OS metapackages; identifies the OS as Devario |
| `devario-keyring` | 20260923-2 | Before OS metapackages |
| `seafoam-keyring` | 20260923-1 | Before OS metapackages |
| `devario-boot` | 1-7 | Before devario-base; requires published devario-dracut |
| `devario-base` | 3-12 | After filesystem, boot, devario-keyring, Fish, and Shadow |
| `devario-system-integration` | 1-1 | Publish before Aqueous devario-desktop 1.0.5-2; migrate existing overlay files before upgrading |
| `ckbcomp` | 1.248-1 | Before Calamares |
| `calamares` | 3.4.2-6 | After ckbcomp and Inter; explicitly declares CMake |

The eight OS-owned directories in `devario-installer/` are self-contained copies
from `devario-os`. Most originated at commit
`63f329223e0851a5f05519b849bb250d560833e2`; the integration package was added
from the working tree on 2026-10-22. Its [migration instructions](devario-installer/devario-system-integration/README.md)
cover adoption of unowned ISO files and legacy desktop ownership. All referenced hooks,
configuration, patches, desktop files, and public key material are included.
Calamares's explicit CMake dependency is updated in this package repository. The base, boot, and keyring recipes are synchronized with the OS checkout
for this path migration; future edits do not automatically synchronize. Exact provenance is in
[iso-packages-upstream.json](devario-core/iso-packages-upstream.json).

These copies are an alternative worker build route. The OS repository's
`scripts/build-packages.sh` and `scripts/build-packages-nspawn.sh` can also build
the OS-owned packages from their own recipes. The ISO assembler consumes
completed signed packages in the staged `devario-core` closure; it does not
compile PKGBUILDs. Public repository publication is not required for a local
ISO, but the staged repository must contain the required artifacts, dependencies,
and matching signed metadata.
The `devario-installer/` source folder does not change that binary repository name.

Review and build each complete recipe directory, publishing and refreshing
the worker repository between prerequisite stages:

```sh
gpg --import devario-core/ding-libs/keys/pgp/*.asc
shelly build --review-only --json ./devario-core/ding-libs/PKGBUILD
shelly build --isolated --check ./devario-core/ding-libs/PKGBUILD
```

GSSProxy still declares the missing build dependency `po4a` for translated
documentation. Ding-libs declares missing test dependency `check`; its configure
script otherwise omits some tests. These were absent from the inspected signed
2026-10-02 databases and are not runtime dependencies of the ISO.

Validation: all sources pass their declared checksums, including the signed
ding-libs release. Local makepkg builds succeeded for all listed recipes except
Calamares, whose source verification and both patches passed preparation.
Composefs's six Meson tests and the D-Bus proxy suite passed outside the sandbox,
where temporary directories and local sockets are available. Ding-libs passed
14 tests without its optional Check-based coverage. GSSProxy's upstream
`test_proxymech` target built; its local build lacked po4a translations.
Libmalcontent built using temporary GLib development tools and its GIR typelib
loaded successfully; the library-only bootstrap deliberately omits upstream
documentation and test targets. Full isolated worker builds and an ISO install
remain unverified.

Shelly review findings in the imported OS sources were inspected: runtime boot,
GPU, and migration scripts contain command substitutions; `devario-report.sh`
uses sudo when invoked to collect system logs. Packaging installs these files
without executing them. The keyring findings identify binary public-key data:
both bundles match the OS source and contain no secret-key packets. GSSProxy's
remaining warning is backtick notation in an upstream patch description.

After including these recipes, the metadata audit selects 637 packages with
zero missing runtime requirements against the inspected signed databases.
This is a dependency-name/version check, not proof of conflict-free installation
or ISO readiness. The Shelly assembler integration and builder provisioning
issues from the readiness audit still require separate work.

## ISO runtime packages added on 2026-10-02

| Recipe | Outputs | Purpose |
| --- | --- | --- |
| [flatpak](devario-core/flatpak/PKGBUILD) | `flatpak` and `flatpak-docs` 1:1.18.4-3 | Shelly's Flatpak backend |
| [inxi](devario-core/inxi/PKGBUILD) | `inxi` 3.3.41.1-3 | Devario system reports |
| [nbd](devario-core/nbd/PKGBUILD) | `nbd` 3.27.1-4 | Live image network block devices |
| [nfs-utils](devario-core/nfs-utils/PKGBUILD) | `nfs-utils` and `nfsidmap` 3.1.1-3 | Live image NFS support |
| [tpm2-tools](devario-core/tpm2-tools/PKGBUILD) | `tpm2-tools` 5.8-2 | Dracut TPM support |

[spandsp](devario-core/spandsp/PKGBUILD) is also updated to `0.0.6-6` to
provide `libspandsp.so` and `libspandsp.so=2-64` for PipeWire. Its packaging
function verifies the ELF class and SONAME before publication. The existing
[inter-font](devario-core/inter-font/PKGBUILD) recipe supplies the remaining
missing installer font package.

The five new recipes preserve Arch's supporting files, packaging licenses,
source checksums, and upstream signing keys, except that inxi uses a pinned,
checksummed Git commit. Codeberg's generated inxi archive no longer matches
Arch's recorded checksum; its complete file contents were compared with the
release commit and found identical. Per-package READMEs record the exact Arch
packaging commits and validation results.

Import the bundled public keys as the worker account before verifying signed
sources:

```sh
gpg --import devario-core/flatpak/keys/pgp/*.asc \
  devario-core/nfs-utils/keys/pgp/*.asc \
  devario-core/tpm2-tools/keys/pgp/*.asc
```

Then review and build each selected directory, for example:

```sh
shelly build --review-only --json ./devario-core/tpm2-tools/PKGBUILD
shelly build --isolated --check ./devario-core/tpm2-tools/PKGBUILD
```

The signed repository databases inspected on 2026-10-02 still lack these
prerequisites. They must be supplied separately; these recipes do not make
the repository dependency closure complete:

| Consumer | Missing runtime prerequisites | Missing build/test prerequisites |
| --- | --- | --- |
| flatpak | `libmalcontent`, `xdg-dbus-proxy` | `gtk-doc`, `python-pyparsing`, `xmlto` |
| nbd | None in the inspected databases | `autoconf-archive`, `docbook-utils`, `perl-sgmls` |
| nfs-utils | `rpcbind`, `gssproxy`; `nfsidmap` is produced by this recipe | `rpcsvc-proto` |
| tpm2-tools | Publish the existing `tpm2-tss` 4.2.0-3 recipe's explicit ABI provisions | `autoconf-archive`, `cmocka`; tests also need `expect`, `swtpm`, `tpm2-abrmd` |

These are direct dependency checks against the inspected database snapshot,
not a complete recursive bootstrap audit. Inxi's declared dependencies were
available. Publish both NFS outputs together. Publish the updated `tpm2-tss`
before building `tpm2-tools`. `cmocka` is a build dependency because unit-test
binaries are enabled at configure time even when `check()` is skipped.

All six changed recipes pass Bash syntax, generated makepkg metadata, Shelly
metadata generation, and Shelly review. All source checksums pass, and Flatpak,
NFS, and TPM upstream signatures verify with the bundled keys. Local makepkg
builds of inxi and spandsp succeeded; the installed inxi command reports its
version and spandsp's archive carries its versioned library provision.
NBD's three upstream fixes apply, but preparation on this host stops at the
missing declared `autoconf-archive` dependency. Flatpak, NFS, TPM, and complete
NBD builds have not been run. Isolated worker builds remain required.

Flatpak and NBD retain Arch's disabled integration-test policy because those
tests hang or fail in package-build containers. Flatpak release 3 explicitly
disables test compilation and installation through Meson; omitting `check()`
alone left `socat` required at configure time in release 2. An invocation with
`--check` does not provide runtime or
network-device acceptance for either package.

For curl, GPGME, libarchive, OpenSSL, XZ, MPFR, ncurses, readline, xxHash,
and Zstandard with explicit ABI provisions, see [the ABI build guide](ABI-BUILDS.md).
That guide records their separate validation status and suggested build order.

For `llvm22` and `llvm22-libs` version `22.1.8-3`, see the
[LLVM 22 build guide](devario-core/llvm22/README.md). The recipe provides
versioned tools and declares `libLLVM.so=22.1-64` explicitly for Shelly.

| Build directory | Requested packages or provisions |
| --- | --- |
| [libusb](devario-core/libusb/PKGBUILD) | `libusb`, explicitly providing `libusb-1.0.so=0-64` for libgusb |
| [qt5-base](devario-core/qt5-base/PKGBUILD) | `qt5-base` and matching `qt5-xcb-private-headers` 5.15.19+kde+r96 |
| [libdex](devario-core/libdex/PKGBUILD) | `libdex` 1.2.0, providing `libdex-1.so=1-64`; also produces `libdex-docs` |
| [python-tqdm](devario-core/python-tqdm/PKGBUILD) | `python-tqdm` 4.70.1, required by the local Meson recipe |
| [ministream](devario-core/ministream/PKGBUILD) | `ministream` 0.99.1, providing `libministream.so=1-64` for consumers such as libadwaita |
| [inter-font](devario-core/inter-font/PKGBUILD) | `inter-font`, supplying the Pearl installer’s Inter font family |
| [glycin](devario-core/glycin/PKGBUILD) | `glycin` 2.2.1 for gdk-pixbuf requiring `glycin-2 >= 2.2.alpha.7`; also produces GTK4 integration and documentation |
| [gtksourceview5](devario-core/gtksourceview5/PKGBUILD) | `gtksourceview5` (also produces documentation) |
| [enchant](devario-core/enchant/PKGBUILD) | `enchant` |
| [hunspell](devario-core/hunspell/PKGBUILD) | `hunspell` |
| [jq](devario-core/jq/PKGBUILD) | `jq` |
| [numactl](devario-core/numactl/PKGBUILD) | `numactl` |
| [gcc](devario-core/gcc/PKGBUILD) | `libgcc`, `libstdc++`, `libgomp`, `libgfortran`, `libquadmath`, plus the matching compiler suite |
| [dbus](devario-core/dbus/PKGBUILD) | `dbus`, providing `libdbus-1.so=3-64` |
| [glib2](devario-core/glib2/PKGBUILD) | `glib2`, providing `libglib-2.0.so=0-64` (also produces development tools and documentation) |
| [nvidia-utils](devario-core/nvidia-utils/PKGBUILD) | `nvidia-utils`, providing `opengl-driver`, `vulkan-driver`, and `nvidia-libgl` |

For the gdk-pixbuf error finding glycin 2.1.0, follow the
[glycin build guide](devario-core/glycin/README.md). Build and publish glycin
2.2.1 first, refresh the worker repository, then retry gdk-pixbuf in a fresh
isolated root. Its worker recipe should require `glycin>=2.2.1`.

If Shelly lists `ministream` before refusing an AUR dependency step in an
isolated build, follow the [ministream build guide](devario-core/ministream/README.md).
Build and publish ministream to the worker repository first, refresh its
database, and retry the dependent package in a fresh isolated root.

For NVIDIA's binary utilities, see the [nvidia-utils build guide](devario-core/nvidia-utils/README.md)
for separate validation results and driver integration requirements. This recipe
produces only `nvidia-utils`; the matching kernel module sources are packaged by
the standalone [nvidia-open-dkms recipe](devario-core/nvidia-open-dkms/README.md).
Both recipes currently target `615.78.08`. Make `libglvnd`, `egl-wayland`, `egl-wayland2`,
`egl-gbm`, and `egl-x11` available to the worker before building it. Coordinate
driver publication and upgrades, including matching multilib/OpenCL packages
where used.

The library provisions are explicit because Shelly's native packager preserves
bare `.so` provisions without adding the SONAME version. Each modified provision
has an ELF64/SONAME check in the packaging function. Source checksums remain
enabled, and D-Bus and GLib retain signed-tag verification.

## Build on the worker

Import the supplied upstream public keys **as the account that invokes Shelly**,
after comparing the fingerprints with the package README files:

```sh
gpg --import dbus/*.asc glib2/*.asc
```

Review and build a recipe from this repository's root, for example:

```sh
shelly build --review-only --json ./hunspell/PKGBUILD
shelly build --isolated --check ./hunspell/PKGBUILD
```

Repeat with the directory names in the table. Run the GCC recipe once to produce
all five requested GCC runtime packages. Its full compiler bootstrap takes much
more time and disk space than the other recipes; see [gcc/README.md](devario-core/gcc/README.md).

The isolated root must have access to repositories containing the declared build
dependencies. Build and publish the GCC outputs together, then build the other
recipes using that repository. Build Hunspell before Enchant, and GLib (including
`glib2-devel`) before GtkSourceView. D-Bus and GLib use each other during building;
an existing compatible package from a bootstrap repository is needed to start
that cycle. These recipes assume an existing working toolchain and package
repository, rather than bootstrapping a distribution from an empty root.

After building, publish the resulting archives and refresh the repository
database used by Remora/Shelly. Editing `.SRCINFO` alone does not update installed
packages or repository dependency resolution. The ABI provisions must appear in
the new packages' `.PKGINFO` and in the repository database. For example:

```sh
bsdtar -xOf /path/to/dbus-1.16.2-2-x86_64.pkg.tar.zst .PKGINFO | grep '^provides = '
bsdtar -xOf /path/to/glib2-2.90.0-1-x86_64.pkg.tar.zst .PKGINFO | grep '^provides = '
```

Compiler architecture flags come from the worker's Shelly configuration. These
recipes declare `arch=(x86_64)` and do not impose `-march=native` or a v3 baseline.

## Validation

The original eight recipes above pass Bash syntax checks and generate `.SRCINFO`.
Seven have no Shelly review findings. GCC's review warns about upstream command substitutions
and Makefile variables in its patch; those inputs were inspected and retained.
Checksums for the included patches and scripts match the upstream recipes.

Native, unprivileged Shelly builds with checks enabled succeeded for Hunspell,
jq, numactl, Enchant, GtkSourceView, D-Bus, and GLib. The generated archives'
`.PKGINFO` contains the expected ABI provisions, including both D-Bus and GLib
requirements above. Temporary build tools were
extracted under `/tmp`; no host packages were installed. Full GCC compilation
has not been run. GLib has since been updated to 2.90.0; its current validation
status is recorded in the [GLib build guide](devario-core/glib2/README.md).

Full `--isolated` nspawn verification is unavailable in this environment because
Shelly's privileged coordinator needs an interactive sudo password. Run the
isolated commands on the worker before publishing the packages.

## Qt 6.12 version alignment

The published `qt6-declarative 6.12.0-1` archive contains QML but omits Qt Quick
and Quick Widgets, preventing Calamares from loading `libQt6QuickWidgets.so.6`.
Build and publish `devario-core/qt6-shadertools` and
`devario-core/qt6-languageserver` (both 6.12.0-1) first, then rebuild
`devario-core/qt6-declarative` as 6.12.0-2 in a fresh isolated root. These new
recipes pin Qt build inputs to 6.12.0. The declarative recipe requires the
ShaderToolsTools CMake package and rejects staged packages missing QML, Quick,
or Quick Widgets libraries. Upstream source checksums are retained; Bash syntax
and generated metadata were checked, but these new recipes have not been compiled.

The [qt6-base recipe](devario-core/qt6-base/PKGBUILD) builds Qt 6.12.0 and its
`qt6-xcb-private-headers` split package. The local
[tools](devario-core/qt6-tools/PKGBUILD) and
[translations](devario-core/qt6-translations/PKGBUILD) recipes now also use
6.12.0. Qt's CMake compatibility checks remain enabled.

Recipes are adapted from official Arch packaging:
[base](https://gitlab.archlinux.org/archlinux/packaging/packages/qt6-base),
[tools](https://gitlab.archlinux.org/archlinux/packaging/packages/qt6-tools), and
[translations](https://gitlab.archlinux.org/archlinux/packaging/packages/qt6-translations).
Base includes its two upstream patches and QtWebEngine CMake detection backport.
Tools no longer applies the old LLVM 22 patch; it retains the pinned qlitehtml
commit and checksum used by the previous local recipe.

Build and publish base first. Make `qt6-declarative=6.12.0` available from the
worker repository before building tools, then build translations. Tools pins
both base and declarative to 6.12.0 as runtime dependencies; translations pins
base, declarative, and tools to 6.12.0 as build dependencies.
Refresh the worker repository between stages and use clean isolated build roots.
An existing translations package is needed to provision consumers of the new
base during this cycle, because base depends on translations. Publish the
matching Qt suite together for downstream use.

Qt 6.12's `lrelease` links to QtQml through LinguistProject and TrLib when tools
is built with QML support. Tools `6.12.0-3` therefore requires declarative at
runtime. Translations `6.12.0-3` also explicitly requests declarative so isolated
builds work with tools packages that still have the older dependency metadata.
This fixes `lrelease: error while loading shared libraries: libQt6Qml.so.6`.
Sync the updated translations PKGBUILD into the worker's selected package
directory (the reported failure uses `default/qt6-translations`), then retry in
a fresh root. Publish the corrected tools package for other `lrelease` users.

Validation: all three recipes pass Bash syntax, makepkg/Shelly metadata, and
Shelly review. Base's bundled patches match their declared checksums. Full
builds and remote-source checksum verification have not been run.

## Calamares build dependency: litehtml

The core-only Calamares build requires `qt6-tools`, whose `litehtml` dependency
was absent from `devario-core`. These two complete recipe directories supply
that dependency and its HTML parser:

| Build and publish order | Release | Directory |
| --- | --- | --- |
| 1. gumbo-parser | 0.13.2-2 | [devario-core/gumbo-parser](devario-core/gumbo-parser/PKGBUILD) |
| 2. litehtml | 0.10-2 | [devario-core/litehtml](devario-core/litehtml/PKGBUILD) |

Upload each complete directory to the Devario build worker. Publish
`gumbo-parser` to `devario-core` and refresh the worker repository before building
`litehtml` in a fresh root. Then publish `litehtml` and rerun `devario-os/build-iso.sh`
with a fresh repository snapshot. Use the Devario x86-64-v3 build environment
for the published packages.

Litehtml 0.10 matches the system-library integration in the existing Qt 6.12
tools recipe. It builds against the separately packaged Gumbo library and
removes the upstream CMake lookup for a Gumbo config file that Gumbo does not
install. Both recipes include explicit SONAME provisions and reject unexpected
library ABI versions during packaging.

Recipes are adapted from official Arch packaging for
[litehtml](https://gitlab.archlinux.org/archlinux/packaging/packages/litehtml) and
[gumbo-parser](https://gitlab.archlinux.org/archlinux/packaging/packages/gumbo-parser).
Litehtml retains the upstream packaging checksum. The current Codeberg Gumbo
archive has a different compressed checksum from the Arch recipe; all 92 tracked
source files were compared with upstream release tag `0.13.2`, commit
`322c54c178590ba42b8b04e8c0e4840595a1f717`, before pinning its current SHA-256.

Validation: both source checksums, Bash syntax, matching makepkg/Shelly metadata,
and Shelly review passed. Both recipes' build and package functions completed
locally; Gumbo passed all 184 tests. A separate CMake consumer discovered, linked,
and ran against the staged libraries. The staged libraries have the expected
SONAMEs and no temporary build-directory RPATHs. Adding these outputs to the
retained core snapshot's dependency model resolves Qt tools and all declared
build/check dependencies of these recipes. Isolated worker builds and
publication remain to be done.

## Noto fonts source directory

[noto-fonts](devario-core/noto-fonts/PKGBUILD) release `1:2026.10.01-2` fixes
the `cd: notofonts: No such file or directory` failure in both split-package
functions. The original source URL ends in `notofonts.github.io`. Makepkg's
Git filename handling truncates at `.git`, giving `notofonts`, while Shelly
retains `notofonts.github.io` because it only removes a terminal `.git` suffix.
The explicit `notofonts::` source alias makes both builders create the directory
the recipe expects. Both packaging functions now use `$srcdir/notofonts`.

The recipe retains the monthly release tag, upstream SHA-256 checksums, all
four fontconfig files, and the `noto-fonts` / `noto-fonts-extra` split from
[Arch packaging commit 0851acf360a933d18d8ae511c50229028686950b](https://gitlab.archlinux.org/archlinux/packaging/packages/noto-fonts/-/commit/0851acf360a933d18d8ae511c50229028686950b).
The tag resolves to `025970232f4f8ff349310d9785431e87d20ed27c`, matching the
checkout shown in the worker's failure. Copy the whole directory to the worker
and retry:

```sh
shelly build --isolated ./devario-core/noto-fonts/PKGBUILD
```

Validation: all five source checksums passed. A local makepkg build from the
pinned release produced both archives: 621 fonts in `noto-fonts` and 1,550 in
`noto-fonts-extra`, matching the source selections without overlapping package
payloads. All four fontconfig symlinks resolve correctly, and the upstream
license is included. Bash syntax and makepkg/Shelly metadata checks passed;
Shelly review reported no findings. A full isolated Shelly build remains
unverified.

## GTK3 bindings blocking the ISO dependency audit

The 2026-10-05 ISO run `20261005T164652Z-75817` selected 644 packages but
reported six unresolved requirements. Its published `atkmm` 2.36.4 and
`cairomm` 1.19.1 belonged to incompatible ABI branches. GParted, gtkmm3, and
pangomm still require `libatkmm-1.6.so` and `libcairomm-1.0.so`. The newer
packages also introduced unavailable glibmm-2.68 and libsigc++-3.0 dependencies.

The corrected recipes follow the GTK3 branches in the official
[atkmm packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/atkmm)
and [cairomm packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/cairomm),
retaining their pinned Git tags and upstream packaging BLAKE2 checksums:

| Recipe | Corrected version | Required library |
| --- | --- | --- |
| [atkmm](devario-core/atkmm/PKGBUILD) | `1:2.28.5-1` | `libatkmm-1.6.so.1` |
| [cairomm](devario-core/cairomm/PKGBUILD) | `1:1.14.6-1` | `libcairomm-1.0.so.1` |

Epoch 1 makes these corrections upgrades over the already-published versions.
Both recipes use the existing glibmm/libsigc++ ABI family, publish bare and
explicit `=1-64` library provisions, and verify the real ELF64 SONAME before
packaging succeeds. Do not substitute the newer ABI libraries with symlinks or
metadata-only provides. The newer bindings now have distinct packages, listed
below, so both generations can coexist.

Build `mm-common` first if it is not yet published, then build both corrected
recipes and publish their matching runtime and documentation outputs:

```sh
shelly build --isolated --check ./devario-core/cairomm/PKGBUILD
shelly build --isolated --check ./devario-core/atkmm/PKGBUILD
```

After signing and publishing the replacement archives and refreshing the hosted
repository database, retry the ISO build using a fresh repository snapshot.
The retained failed run still contains the incompatible archives. Its six local
installer packages are not the cause, and changing only their metadata or
rerunning against the same snapshot cannot fix the failure.

The validation and remaining release steps for both generations are recorded
below. Keep the epoch when refreshing the corrected GTK3 packages.

## Parallel C++ binding packages

These recipes preserve the newer ABI stack without replacing GTK3's package
names, headers, libraries, pkg-config files, or documentation:

| Recipe | Version | Outputs |
| --- | --- | --- |
| [mm-common](devario-core/mm-common/PKGBUILD) | `1.0.8-1` | `mm-common` |
| [libsigc++-3.0](devario-core/libsigc++-3.0/PKGBUILD) | `3.8.1-1` | `libsigc++-3.0`, `libsigc++-3.0-docs` |
| [glibmm-2.68](devario-core/glibmm-2.68/PKGBUILD) | `2.90.0-1` | `glibmm-2.68`, `glibmm-2.68-docs` |
| [cairomm-1.16](devario-core/cairomm-1.16/PKGBUILD) | `1.19.1-1` | `cairomm-1.16`, `cairomm-1.16-docs` |
| [atkmm-2.36](devario-core/atkmm-2.36/PKGBUILD) | `2.36.4-1` | `atkmm-2.36`, `atkmm-2.36-docs` |

Package suffixes identify the ABI, not the upstream release number. The newer
atkmm and cairomm recipes preserve the source versions previously published
under the wrong names. Each library recipe checks its actual ELF64 SONAME and
provides only its own library ABI; none provides, replaces, or conflicts with
the legacy package names. Documentation packages also have separate names.

The new recipes follow official Arch packaging for
[atkmm-2.36](https://gitlab.archlinux.org/archlinux/packaging/packages/atkmm-2.36),
[cairomm-1.16](https://gitlab.archlinux.org/archlinux/packaging/packages/cairomm-1.16),
[glibmm-2.68](https://gitlab.archlinux.org/archlinux/packaging/packages/glibmm-2.68),
[libsigc++-3.0](https://gitlab.archlinux.org/archlinux/packaging/packages/libsigcplusplus-3.0),
and [mm-common](https://gitlab.archlinux.org/archlinux/packaging/packages/mm-common).
The cairomm 1.19.1 tag and checksum come from this repository's previous
cairomm recipe. Every source remains pinned and checksum-verified.

`glibmm-2.68` explicitly requires `glib2>=2.89.4`, matching its upstream
build requirement. The retained repository already has GLib 2.90.0.
`mm-common` uses the existing legacy libsigc++ and its documentation to bootstrap;
there is no dependency on the new sigc++ package. It builds without network
access using a separately downloaded, checksum-pinned GCC documentation tag.
It requires `libxslt` for the C++ documentation tools and makes the unrelated
GTK C documentation generator `gtk-doc` optional.

Build and publish in this order, refreshing the worker's repository database
between dependency stages. Publish runtime and documentation outputs together:

1. `mm-common`, using existing `libsigc++` and `libsigc++-docs`.
2. Corrected `atkmm` and `cairomm`, including their `-docs` outputs.
3. `libsigc++-3.0`, including `libsigc++-3.0-docs`.
4. `glibmm-2.68` and `cairomm-1.16`, including their `-docs` outputs.
5. `atkmm-2.36`, after the new GLibmm runtime and documentation are available.

For example, from this repository root:

```sh
shelly build --isolated --check ./devario-core/mm-common/PKGBUILD
# Publish mm-common before building the dependent recipes.
shelly build --isolated --check ./devario-core/libsigc++-3.0/PKGBUILD
# Publish both sigc++ outputs before building the next stage.
shelly build --isolated --check ./devario-core/glibmm-2.68/PKGBUILD
shelly build --isolated --check ./devario-core/cairomm-1.16/PKGBUILD
# Publish the new GLibmm outputs before building atkmm-2.36.
shelly build --isolated --check ./devario-core/atkmm-2.36/PKGBUILD
```

Installations containing the mistakenly named modern libraries must upgrade
`atkmm`, `cairomm`, and their documentation to the corrected epoch-1 packages
before, or in the same transaction as, installing the parallel modern packages.
Otherwise the old incorrect archives still own the modern paths. Do not add
`conflicts` or `replaces` against the correctly named legacy packages to work
around that transitional state. After publication, a fresh ISO snapshot should
select the corrected legacy packages for GParted. The optional modern stack
does not need to be added to the live ISO to repair its dependency closure.

Validation on 2026-10-05:

- All seven recipe source checksums and the extra GCC tag-file checksum passed.
- All seven recipes completed native build and package-function runs under
  `/tmp`, using staged build dependencies without installing them on the host.
- Sigc++ passed 42 upstream tests, modern cairomm passed 7, and GLibmm passed 35
  with 2 expected failures. The GLibmm package check explicitly excludes
  `giomm_tls_client_test`, which connects to `www.gnome.org` and fails without
  DNS/network access. The test remains available for separate network testing.
  Atkmm and mm-common define no Meson tests in these configurations.
- File inventories for 17 runtime/documentation payloads, including the existing
  legacy GLibmm and sigc++ archives, have no overlapping non-directory paths.
- `tests/test-gtk3-binding-abi.py` checks both generations' ABI guards, rejection
  of wrong/missing ELF libraries, separate package identities/provisions, and
  upgrade ordering for the corrected legacy packages.
- Bash syntax, regenerated `.SRCINFO`, and Shelly review passed. Shelly reported
  no review findings for the new recipes.
- A metadata projection resolves all runtime, build, and check dependencies
  against the retained repository: 175 selected packages, zero unresolved
  requirements. The earlier ISO projection remains 644 selected packages with
  zero unresolved requirements after correcting the two legacy providers.

These are native staged builds and metadata audits, not signed release builds.
Clean isolated package builds, signed publication, a fresh repository audit,
and the ISO rebuild remain required before the reported ISO failure is fixed
in published artifacts.

## mupdf dependency chain

`devario-utilities/mupdf` fails `--resolve-dependencies` on six names. Four new
`devario-libs` recipes cover the three that had no recipe plus the OCR data
`tesseract` requires at install time; `unzip`, `zint` and `zxing-cpp` already
have recipes that are simply not published yet.

```sh
shelly build --isolated --check ./devario-libs/cmark-gfm/PKGBUILD
shelly build --isolated --check ./devario-libs/leptonica/PKGBUILD
# Publish leptonica before tesseract, which depends on it globally.
shelly build --isolated --check ./devario-libs/tesseract/PKGBUILD
shelly build --isolated --check ./devario-libs/tesseract-data/PKGBUILD
shelly build --isolated --check ./devario-utilities/unzip/PKGBUILD
shelly build --isolated --check ./devario-libs/zint/PKGBUILD
# Publish zint before zxing-cpp, which depends on it globally.
shelly build --isolated --check ./devario-libs/zxing-cpp/PKGBUILD
```

`tesseract` and `tesseract-data` require each other, but only through
`depends+=()` inside `package_*()`. Shelly plans global `depends` plus
makedepends, so neither side enters the other's build root and the cycle
resolves at install time as it does in Arch. For the same reason
`tesseract-data` can be built before `tesseract` is published.

`leptonica` declares each `.so` requirement in the form its published provider
actually advertises. Published `libpng` and `zlib` carry only bare provisions,
so `libpng16.so` and `libz.so` stay bare; porting either provider to an explicit
versioned provision would let those two match the rest.

`zxing-cpp` no longer waits on `java-environment`, and published `opencv` installs
into the isolated root. Its first worker build failed one step later, at the link of
the `ZXingOpenCV` demo: the builder's `LDFLAGS` lack the `--as-needed` Arch carries, so
ld kept every OpenCV module and had to resolve the `vtk` and `hdf5` references that
`opencv` leaves to its optdepends. The recipe appends that flag. Naming `vtk`, `hdf5`
and `openmpi` in `makedepends` also links, but only by pulling the whole VTK and MPI
closure into the root for a binary that is never installed. Probe-verified against the
published `opencv` archive; no isolated worker build has run since.

Validation on 2026-10-10:

- All four source checksums were recomputed from downloaded upstream tarballs and
  match the official Arch recipes. The 668 MiB `tessdata` archive is used in full
  only as a source; two files are installed from it.
- `bash -n`, regenerated `.SRCINFO`, and `shelly build --review-only --json` all
  passed for the four recipes, with no review findings.
- `tesseract-data` was rejected by Shelly review while it still used upstream's
  `pkgname=("${_langs[@]/#/tesseract-data-}")` array expansion
  (`UnsupportedArrayExpansion`); the two packages are now written out explicitly.
- Every `depends`, `makedepends` and `checkdepends` entry in the four `.SRCINFO`
  files, at pkgbase and per-package level, resolves against the published
  repositories once the four recipes and their declared provisions are counted as
  available.
- The three SONAME values in the explicit provisions come from the sources:
  `SOVERSION` in cmark-gfm's `src/` and `extensions/` CMakeLists, and
  `-version-info 6:0:0` in leptonica's `src/Makefile.am`. Each `package()`
  re-checks ELF64 and the SONAME before packaging.

No isolated build, publication, or `mupdf` build has been performed for this
change.

## Libffado dependency plan (2026-10-10)

Retry `libxml++` with release `3.2.6-2`. Its tutorial generation needs
`docbook-xsl`, now explicitly listed in `makedepends`. This package supplies
the stylesheet and XML catalog mapping for
`http://docbook.sourceforge.net/release/xsl/current/html/chunk.xsl`. Without
that mapping, the HTML generation step exits with code 4 after the library
has already linked. Keep both the library and documentation split outputs.

Validation reproduced the same exit-4 failure using the pinned 3.2.6 tutorial
helper with XML catalogs disabled. With the installed DocBook catalog, the
same helper generated all seven tutorial HTML pages while `xsltproc --nonet`
prohibited network access. Shell syntax passed and `.SRCINFO` was regenerated
with makepkg, preserving the documentation package's empty dependencies.
Shelly's metadata agrees apart from omitting that empty override.
A full isolated build was not run. Upload the updated recipe and
metadata, ensure `docbook-xsl` is available to the worker, and retry.

The worker's `IncompleteDependencyPlan` for `libxml++`, `dbus-c++`,
`libconfig`, and `python-pyqt5` requires publishing those packages before
retrying libffado. Their dependency names are correct. Thirteen recipes were
added from the official Arch packaging repositories, retaining their source
checksums, patches, and licensing files. Each recipe records its packaging
archive in `DEVARIO-UPSTREAM.json`.

The additions include PyQt5's SIP tools, Python OpenGL bindings, and five Qt5
modules. Libffado retains its mixer support. Against the inspected
`devario-core`, `devario-libs`, `devario-development`, and `devario-utilities`
repository catalogs, six existing recipes also need publication. The following
order covers the unpublished prerequisites; publish each recipe's outputs and
refresh the worker's repository metadata before building its consumers.

| Order | Recipe | Status |
| --- | --- | --- |
| 1 | [dbus-c++](devario-libs/dbus-c++/PKGBUILD) | Added |
| 2 | [libconfig](devario-libs/libconfig/PKGBUILD) | Added |
| 3 | [libxml++](devario-libs/libxml++/PKGBUILD) | Added; also produces libxml++-docs |
| 4 | [sip](devario-development/sip/PKGBUILD) | Added |
| 5 | [pyqt-builder](devario-development/pyqt-builder/PKGBUILD) | Added |
| 6 | [pyopengl](devario-libs/pyopengl/PKGBUILD) | Added; produces python-opengl |
| 7 | [python-pyqt5-sip](devario-libs/python-pyqt5-sip/PKGBUILD) | Added |
| 8 | [qt5-multimedia](devario-libs/qt5-multimedia/PKGBUILD) | Added |
| 9 | [qt5-serialport](devario-libs/qt5-serialport/PKGBUILD) | Added |
| 10 | [chrpath](devario-development/chrpath/PKGBUILD) | Existing, unpublished |
| 11 | [flite](devario-development/flite/PKGBUILD) | Existing, unpublished |
| 12 | [libsonic](devario-libs/libsonic/PKGBUILD) | Existing, unpublished |
| 13 | [espeak-ng](devario-utilities/espeak-ng/PKGBUILD) | Existing, unpublished |
| 14 | [speech-dispatcher](devario-utilities/speech-dispatcher/PKGBUILD) | Existing, unpublished; publish libspeechd too |
| 15 | [qt5-speech](devario-libs/qt5-speech/PKGBUILD) | Added |
| 16 | [qt5-svg](devario-libs/qt5-svg/PKGBUILD) | Added |
| 17 | [qt5-x11extras](devario-libs/qt5-x11extras/PKGBUILD) | Existing, unpublished |
| 18 | [qt5-xmlpatterns](devario-libs/qt5-xmlpatterns/PKGBUILD) | Added |
| 19 | [pyqt5](devario-libs/pyqt5/PKGBUILD) | Added; produces python-pyqt5 |
| 20 | [libffado](devario-libs/libffado/PKGBUILD) | Retry after prerequisites are published |

The dependency-name/provision check recursively included runtime, build, and
check requirements. It found no remaining missing names or cycles among these
unpublished recipes once the catalog's published providers were included.
This is a catalog check, not an isolated-worker build or an ABI audit.

Validation:

- All thirteen new recipes passed `bash -n` and `makepkg --verifysource`,
  including their pinned Git sources and local patches.
- `.SRCINFO` was generated with makepkg and checked against Shelly's metadata.
  Shelly omits the explicit empty `depends` field for libxml++-docs; the other
  emitted fields match. The Qt5 `pkgver()` functions were reviewed before
  metadata generation.
- `dbus-c++`, `libconfig`, `python-pyqt5-sip`, and `python-opengl` completed
  local builds and staged packaging. The C++ libraries expose
  `libdbus-c++-1.so.0` and `libconfig++.so.15`.

Full libxml++, PyQt5, Qt5 module, and libffado builds have not been run. No host
packages were installed and no packages were published. Adding recipes alone
does not satisfy the worker's `not_in_repositories` checks.

## Qt5 Multimedia GStreamer dependency plan (2026-10-10)

Retry [qt5-multimedia](devario-libs/qt5-multimedia/PKGBUILD) with release
`5.15.19+kde+r2-2`. The previous recipe required the full `gst-plugins-bad`
bundle at build time, pulling in its 15 unpublished runtime dependencies:
`faac`, `faad2`, `libavtp`, `libdc1394`, `liblrdf`, `libmpcdec`, `mjpegtools`,
`neon`, `qrencode`, `rtmpdump`, `soundtouch`, `wildmidi`, `zbar`, `zvbi`, and
`zxing-cpp`.

The pinned Qt source's photography configure test uses
`gst/interfaces/photography.h` and `-lgstphotography-1.0`; its camerabin backend
also links this library. These development files and the shared library belong
to [gst-plugins-bad-libs](https://archlinux.org/packages/extra/x86_64/gst-plugins-bad-libs/files/).
The recipe now requires `gst-plugins-bad-libs` at runtime (which also installs it
for the build), and retains `gst-plugins-bad` as an optional camera/plugin
dependency. No Qt features are disabled. Using the full optional bundle still
requires publishing its missing dependencies.

The earlier libffado catalog check above stopped at published packages and
therefore missed this broken transitive dependency chain. A recursive check of
published runtime requirements using the cached 2026-10-10 repository catalogs
reproduced all 15 worker errors with the old Qt recipe. With the corrected
recipe, all 191 packages reached from its runtime and build requirements
resolve, including version constraints and provisions. Installed dependencies'
own build/check requirements and optional dependencies are not installation
requirements and were excluded.

Validation: `bash -n` passed, `.SRCINFO` was regenerated with makepkg and matches
Shelly's output, and Shelly review completed with only the existing dynamic
command warning in `pkgver()`. No full Qt build or repository publication was
performed. Upload the updated recipe and `.SRCINFO`, refresh the worker's
recipe metadata, and retry `qt5-multimedia` before continuing the libffado plan.

## Qt5 Speech dependency plan (2026-10-10)

The worker's `IncompleteDependencyPlan` for `qt5-multimedia`, `flite`, and
`speech-dispatcher` requires building and publishing their existing recipes
before retrying [qt5-speech](devario-libs/qt5-speech/PKGBUILD). The repeated
`not_in_repositories` and `not_in_environment` entries refer to the same three
requirements. Uploading recipe files alone does not make their binary packages
available to an isolated build.

Use this subset of the libffado build order above, skipping prerequisites
already available in the worker's repositories:

| Order | Recipe | Required publication |
| --- | --- | --- |
| 1 | [qt5-multimedia](devario-libs/qt5-multimedia/PKGBUILD) | `qt5-multimedia` 5.15.19+kde+r2-2, including the GStreamer dependency correction above |
| 2 | [chrpath](devario-development/chrpath/PKGBUILD) | Before flite |
| 3 | [flite](devario-development/flite/PKGBUILD) | Before qt5-speech |
| 4 | [libsonic](devario-libs/libsonic/PKGBUILD) | Before espeak-ng |
| 5 | [espeak-ng](devario-utilities/espeak-ng/PKGBUILD) | Before speech-dispatcher |
| 6 | [speech-dispatcher](devario-utilities/speech-dispatcher/PKGBUILD) | Publish both `speech-dispatcher` and `libspeechd` 0.12.1-4 |
| 7 | [qt5-speech](devario-libs/qt5-speech/PKGBUILD) | Retry after all three reported requirements resolve |

Publish each prerequisite and refresh the worker's repository metadata before
building its consumers. Speech Dispatcher's runtime package requires the exact
matching `libspeechd` release, which contains the headers, shared library, and
pkg-config file. Flite and Speech Dispatcher remain build requirements even
though selecting their TTS backends is optional at runtime.

Validation: all seven recipes passed `bash -n`; their checked-in `.SRCINFO`
files match fresh `makepkg --printsrcinfo` output. No recipe change is needed
for this error. No isolated build or repository publication was performed.

## Libsonic shared-library compilation (2026-10-10)

Retry [libsonic](devario-libs/libsonic/PKGBUILD) with release `0.2.0-3`.
The bundled `ldflags.patch` removed upstream's `-fPIC`, causing the worker's
shared-library link to fail with `R_X86_64_PC32` relocations against `stderr`.
The patch now preserves `-fPIC` while retaining the worker's compiler flags.
It also passes the SONAME option separately from `LDFLAGS`, so linking does
not depend on the last linker flag's format. Both patch checksums and
`.SRCINFO` are updated.

Validation: source and patch SHA-512/BLAKE2 checksums passed, as did shell
syntax and metadata generation. Native compilation and staged packaging
succeeded with the worker's reported compiler/linker flags. The resulting
library has SONAME `libsonic.so.0` and no text relocations; the staged CLI
processed a generated WAV file at twice its original speed. Shelly review
completed with dynamic-command warnings for Makefile expressions in the
patch. No isolated worker build or publication was performed.

Upload the complete updated recipe directory, including `ldflags.patch` and
`.SRCINFO`, refresh worker recipe metadata, and rebuild. Publish libsonic
before continuing with espeak-ng and speech-dispatcher.

## Git LFS man pages after the Ruby 4.0 upgrade (2026-10-10)

The published `asciidoctor` 2.0.26-1 package contains its gem and gemspec under
`/usr/lib/ruby/gems/3.4.0`. The published Ruby 4.0.7 runtime searches
`/usr/lib/ruby/gems/4.0.0`, so its launcher fails with
`Gem::GemNotFoundException` during Git LFS's `make man` target.

Build and publish [asciidoctor](devario-core/asciidoctor/PKGBUILD) 2.0.26-2
with Ruby 4.0 first. Refresh worker metadata, then rebuild
[git-lfs](devario-development/git-lfs/PKGBUILD) 3.8.0-2. Asciidoctor now
requires `ruby>=4.0` and `ruby<4.1`, and uses `Gem.default_dir` so an inherited
`GEM_HOME` cannot select its package installation directory. Git LFS requires
`asciidoctor>=2.0.26-2` to prevent reuse of the stale package. A future Ruby
minor-version upgrade requires rebuilding Asciidoctor and updating this range.

The failure was reproduced with the published packages in a temporary mount
namespace. Asciidoctor's sources passed both declared checksums; its build and
manual staged package function completed using Ruby 4.0.7. The rebuilt launcher
then ran without gem-path overrides, and Git LFS v3.8.0's complete `make man`
target passed, producing 36 man pages plus HTML documentation. The makepkg
fakeroot packaging attempt encountered an ownership-preservation error in the
local namespace, so staged packaging was rerun without fakeroot. The full
Asciidoctor test suite and Git LFS Go build/tests were not rerun; no host package
installation or repository publication was performed.

## Libffado provisioning: PyQt5 `/usr/sbin` conflict (2026-10-10)

The published `python-pyqt5-5.15.11-8` archive contains a real `usr/sbin/`
directory and `pylupdate5`, `pyrcc5`, and `pyuic5` beneath it. The published
`filesystem-2025.10.12-1` owns `usr/sbin` as a symlink to `bin`. This is a
directory/symlink conflict during isolated-root provisioning, before libffado
compilation. Both archives were downloaded and matched their repository
SHA-256 checksums. The generic `Package: rlpm` error labels the backend; it
does not name the conflicting package.

SIP 6.17 defaults its scripts directory to the directory of `sys.executable`.
[PyQt5](devario-libs/pyqt5/PKGBUILD) release `5.15.11-9` now passes
`--scripts-dir /usr/bin` explicitly. [Libffado](devario-libs/libffado/PKGBUILD)
release `2.5.0-3` requires `python-pyqt5>=5.15.11-9` during the build so the
worker cannot reuse the conflicting archive. Both `.SRCINFO` files are updated.

Rebuild and publish `python-pyqt5` from the updated `devario-libs/pyqt5`
recipe, refresh the worker's repository and recipe metadata, then retry
libffado in a fresh isolated root. Do not overwrite the filesystem symlink.

Validation: Bash syntax and makepkg/Shelly metadata agree. PyQt5 review has
no findings; libffado retains its existing warning about the Python
site-packages lookup. The PyQt5 source and bundled patch checksums passed.
With checksum-verified SIP 6.17 and PyQt-builder 1.20 packages extracted into
`/tmp`, a QtCore-only configuration generated the Makefiles, and the real
`install_scripts` target staged all three executables under `usr/bin` without
creating `usr/sbin`. Full PyQt5 compilation, isolated provisioning, libffado
compilation, and publication were not performed.

Alternatively, the published `5.15.11-8` archive can be repacked without
recompilation: move the three scripts from `usr/sbin` to `usr/bin`, remove
the real `usr/sbin` directory, update the Python dist-info `RECORD` paths,
bump the package version to `5.15.11-9`, and regenerate `.MTREE`. A local
unsigned archive was prepared this way, preserving the original compiler
environment and PKGBUILD hash in `.BUILDINFO` with a repacking note. All 833
non-metadata payload files remain byte-identical, and all 888 manifest paths
and 836 file checksums were verified. Its SHA-256 is
`57ffea3e4f19262c7a5b33d22282b387b4e04b23131e29dc680cb0b51fb29526`.
Sign and publish that archive through the normal repository process, then
refresh the worker and retry libffado. The original archive's signature
cannot be reused for the repacked archive. This alternative was not installed
or tested in an isolated root.
