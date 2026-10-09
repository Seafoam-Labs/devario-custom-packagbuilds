# Build order — latest commit

Commit: `8a824477ae6f89e624f634d9deed265d6fd50825`. This list is pinned to that commit and compares it with its first parent.

**1,321 package outputs from 900 affected recipes, listed individually across 28 stages.**

- **1,311 outputs from 895 added recipe directories** — marked **Added recipe**.
- **1 added split output**, `python-maturin`, from an existing recipe — marked **Added split output**.
- **8 updated outputs** from existing recipes — marked **Updated**.
- **1 existing output**, `swig`, with added metadata and supporting files — marked **Metadata only**; its PKGBUILD is unchanged.

The four modified existing recipes are `maturin`, `jdk-openjdk`, `neovim`, and `texinfo`. The existing `swig` recipe received metadata and supporting files. All remaining recipes in the stage tables were added by this commit. This replaces the earlier hook-only scope.

## How to build

1. Use a working Devario builder with compatible base packages and published dependencies. Stages retain the application build plan recorded in this commit; dependencies outside this commit still need to be available.
2. Build stages **01 through 28**, publishing outputs and refreshing the builder repository between stages. Independent recipes in a stage can build in separate roots.
3. **Build each recipe once.** Multiple package rows sharing a recipe are split outputs from that build. Keep conflicting alternatives in separate roots.
4. Provision working seed packages for every flagged bootstrap group. Members of a cycle do not have a complete source-only order; keep seeds available until all replacements in that group are built.
5. The inherited application plan excludes test-only and optional dependency expansion; use its `--no-check` setting unless you separately provision test dependencies.

The 10 unchanged recipes used by the original dependency plan are listed after the stages. They must be available before the stages that consume them. No package builds or publication were performed to generate this list.

**Neovim:** stage 02 places it after the stage-01 `libutf8proc`, `luajit`, and `tree-sitter` outputs. Its remaining dependencies must already be available, including `lua51-mpack`, `lua51-lpeg`, `libluv`, `libvterm>=0.3.3`, `msgpack-c`, `unibilium`, the required shared-library providers, and the C, Lua, Markdown, query, Vim, and Vimdoc tree-sitter grammar packages. These prerequisites are not supplied by this commit. Hold Neovim if its isolated root cannot satisfy them. Texinfo is in stage 01 and requires existing `ncurses`, `gzip`, `perl`, and `sh` providers.

Machine-readable list: [LATEST-BUILD-ORDER.tsv](LATEST-BUILD-ORDER.tsv).

Jump to stage: [01](#stage-01) · [02](#stage-02) · [03](#stage-03) · [04](#stage-04) · [05](#stage-05) · [06](#stage-06) · [07](#stage-07) · [08](#stage-08) · [09](#stage-09) · [10](#stage-10) · [11](#stage-11) · [12](#stage-12) · [13](#stage-13) · [14](#stage-14) · [15](#stage-15) · [16](#stage-16) · [17](#stage-17) · [18](#stage-18) · [19](#stage-19) · [20](#stage-20) · [21](#stage-21) · [22](#stage-22) · [23](#stage-23) · [24](#stage-24) · [25](#stage-25) · [26](#stage-26) · [27](#stage-27) · [28](#stage-28)

## Stage 01

405 packages from 323 recipes.

| Package | Change in commit | Build recipe | Bootstrap / prerequisites |
| --- | --- | --- | --- |
| `aalib` | Added recipe | [devario-libs/aalib](devario-libs/aalib/PKGBUILD) | — |
| `acpica` | Added recipe | [devario-development/acpica](devario-development/acpica/PKGBUILD) | — |
| `ada` | Added recipe | [devario-libs/ada](devario-libs/ada/PKGBUILD) | — |
| `alembic` | Added recipe | [devario-libs/alembic](devario-libs/alembic/PKGBUILD) | — |
| `anari-sdk` | Added recipe | [devario-development/anari-sdk](devario-development/anari-sdk/PKGBUILD) | — |
| `apache-orc` | Added recipe | [devario-libs/apache-orc](devario-libs/apache-orc/PKGBUILD) | — |
| `argon2` | Added recipe | [devario-libs/argon2](devario-libs/argon2/PKGBUILD) | — |
| `arj` | Added recipe | [devario-development/arj](devario-development/arj/PKGBUILD) | — |
| `aspell` | Added recipe | [devario-utilities/aspell](devario-utilities/aspell/PKGBUILD) | — |
| `assimp` | Added recipe | [devario-libs/assimp](devario-libs/assimp/PKGBUILD) | — |
| `aws-c-common` | Added recipe | [devario-libs/aws-c-common](devario-libs/aws-c-common/PKGBUILD) | — |
| `benchmark` | Added recipe | [devario-libs/benchmark](devario-libs/benchmark/PKGBUILD) | — |
| `blosc` | Added recipe | [devario-libs/blosc](devario-libs/blosc/PKGBUILD) | — |
| `boxed-cpp` | Added recipe | [devario-libs/boxed-cpp](devario-libs/boxed-cpp/PKGBUILD) | — |
| `btrfs-assistant` | Added recipe | [devario-utilities/btrfs-assistant](devario-utilities/btrfs-assistant/PKGBUILD) | — |
| `bzip3` | Added recipe | [devario-development/bzip3](devario-development/bzip3/PKGBUILD) | — |
| `c-ares` | Added recipe | [devario-libs/c-ares](devario-libs/c-ares/PKGBUILD) | — |
| `cabextract` | Added recipe | [devario-utilities/cabextract](devario-utilities/cabextract/PKGBUILD) | — |
| `catch2` | Added recipe | [devario-libs/catch2](devario-libs/catch2/PKGBUILD) | — |
| `cbindgen` | Added recipe | [devario-libs/cbindgen](devario-libs/cbindgen/PKGBUILD) | — |
| `cdparanoia` | Added recipe | [devario-utilities/cdparanoia](devario-utilities/cdparanoia/PKGBUILD) | — |
| `cdrtools` | Added recipe | [devario-development/cdrtools](devario-development/cdrtools/PKGBUILD) | — |
| `chromaprint` | Added recipe | [devario-libs/chromaprint](devario-libs/chromaprint/PKGBUILD) | — |
| `chrono-date` | Added recipe | [devario-libs/chrono-date](devario-libs/chrono-date/PKGBUILD) | — |
| `chrpath` | Added recipe | [devario-development/chrpath](devario-development/chrpath/PKGBUILD) | — |
| `cli11` | Added recipe | [devario-development/cli11](devario-development/cli11/PKGBUILD) | — |
| `cliphist` | Added recipe | [devario-utilities/cliphist](devario-utilities/cliphist/PKGBUILD) | — |
| `cmocka` | Added recipe | [devario-development/cmocka](devario-development/cmocka/PKGBUILD) | — |
| `codelldb-bin` | Added recipe | [devario-development/codelldb-bin](devario-development/codelldb-bin/PKGBUILD) | — |
| `cppunit` | Added recipe | [devario-libs/cppunit](devario-libs/cppunit/PKGBUILD) | — |
| `cpuinfo` | Added recipe | [devario-libs/cpuinfo](devario-libs/cpuinfo/PKGBUILD) | — |
| `cudnn` | Added recipe | [devario-libs/cudnn](devario-libs/cudnn/PKGBUILD) | — |
| `cxxopts` | Added recipe | [devario-development/cxxopts](devario-development/cxxopts/PKGBUILD) | — |
| `directx-headers` | Added recipe | [devario-libs/directx-headers](devario-libs/directx-headers/PKGBUILD) | — |
| `discord` | Added recipe | [devario-gaming/discord](devario-gaming/discord/PKGBUILD) | — |
| `djvulibre` | Added recipe | [devario-libs/djvulibre](devario-libs/djvulibre/PKGBUILD) | — |
| `dlpack` | Added recipe | [devario-libs/dlpack](devario-libs/dlpack/PKGBUILD) | — |
| `docbook-dsssl` | Added recipe | [devario-utilities/docbook-dsssl](devario-utilities/docbook-dsssl/PKGBUILD) | — |
| `docbook-sgml31` | Added recipe | [devario-utilities/docbook-sgml31](devario-utilities/docbook-sgml31/PKGBUILD) | — |
| `docker-compose` | Added recipe | [devario-development/docker-compose](devario-development/docker-compose/PKGBUILD) | — |
| `doctest` | Added recipe | [devario-libs/doctest](devario-libs/doctest/PKGBUILD) | — |
| `dotconf` | Added recipe | [devario-libs/dotconf](devario-libs/dotconf/PKGBUILD) | — |
| `ed` | Added recipe | [devario-development/ed](devario-development/ed/PKGBUILD) | — |
| `ethtool` | Added recipe | [devario-utilities/ethtool](devario-utilities/ethtool/PKGBUILD) | — |
| `exiv2` | Added recipe | [devario-libs/exiv2](devario-libs/exiv2/PKGBUILD) | — |
| `faac` | Added recipe | [devario-development/faac](devario-development/faac/PKGBUILD) | — |
| `faad2` | Added recipe | [devario-development/faad2](devario-development/faad2/PKGBUILD) | — |
| `festival` | Added recipe | [devario-development/festival](devario-development/festival/PKGBUILD) | — |
| `ffcall` | Added recipe | [devario-libs/ffcall](devario-libs/ffcall/PKGBUILD) | — |
| `ffnvcodec-headers` | Added recipe | [devario-libs/ffnvcodec-headers](devario-libs/ffnvcodec-headers/PKGBUILD) | — |
| `fltk1.3` | Added recipe | [devario-development/fltk1.3](devario-development/fltk1.3/PKGBUILD) | — |
| `fluxer-canary-bin` | Added recipe | [devario-gaming/fluxer-canary-bin](devario-gaming/fluxer-canary-bin/PKGBUILD) | — |
| `fpc` | Added recipe | [devario-development/fpc](devario-development/fpc/PKGBUILD) | Seed: `fpc` |
| `fpc-src` | Added recipe | [devario-development/fpc-src](devario-development/fpc-src/PKGBUILD) | — |
| `freetds` | Added recipe | [devario-libs/freetds](devario-libs/freetds/PKGBUILD) | — |
| `fstrm` | Added recipe | [devario-libs/fstrm](devario-libs/fstrm/PKGBUILD) | — |
| `functional-plus` | Added recipe | [devario-libs/functional-plus](devario-libs/functional-plus/PKGBUILD) | — |
| `gamemode` | Added recipe | [devario-gaming/gamemode](devario-gaming/gamemode/PKGBUILD) | — |
| `gendesk` | Added recipe | [devario-development/gendesk](devario-development/gendesk/PKGBUILD) | — |
| `geos` | Added recipe | [devario-libs/geos](devario-libs/geos/PKGBUILD) | — |
| `github-cli` | Added recipe | [devario-development/github-cli](devario-development/github-cli/PKGBUILD) | — |
| `glew` | Added recipe | [devario-libs/glew](devario-libs/glew/PKGBUILD) | — |
| `glfw` | Added recipe | [devario-libs/glfw](devario-libs/glfw/PKGBUILD) | — |
| `glm` | Added recipe | [devario-libs/glm](devario-libs/glm/PKGBUILD) | — |
| `glow` | Added recipe | [devario-productivity/glow](devario-productivity/glow/PKGBUILD) | — |
| `gn` | Added recipe | [devario-development/gn](devario-development/gn/PKGBUILD) | — |
| `gnu-efi` | Added recipe | [devario-development/gnu-efi](devario-development/gnu-efi/PKGBUILD) | — |
| `go-tools` | Added recipe | [devario-development/go-tools](devario-development/go-tools/PKGBUILD) | — |
| `gperf` | Added recipe | [devario-development/gperf](devario-development/gperf/PKGBUILD) | — |
| `gpgmepp` | Added recipe | [devario-libs/gpgmepp](devario-libs/gpgmepp/PKGBUILD) | — |
| `gpu-screen-recorder` | Added recipe | [devario-entertainment/gpu-screen-recorder](devario-entertainment/gpu-screen-recorder/PKGBUILD) | — |
| `grabit-git` | Added recipe | [devario-utilities/grabit-git](devario-utilities/grabit-git/PKGBUILD) | — |
| `gsl` | Added recipe | [devario-libs/gsl](devario-libs/gsl/PKGBUILD) | — |
| `half` | Added recipe | [devario-libs/half](devario-libs/half/PKGBUILD) | — |
| `hdparm` | Added recipe | [devario-utilities/hdparm](devario-utilities/hdparm/PKGBUILD) | — |
| `hipblas-common` | Added recipe | [devario-libs/hipblas-common](devario-libs/hipblas-common/PKGBUILD) | — |
| `hiredis` | Added recipe | [devario-libs/hiredis](devario-libs/hiredis/PKGBUILD) | — |
| `hyphen` | Added recipe | [devario-libs/hyphen](devario-libs/hyphen/PKGBUILD) | — |
| `hyphen-en` | Added recipe | [devario-libs/hyphen](devario-libs/hyphen/PKGBUILD) | — |
| `iniparser` | Added recipe | [devario-libs/iniparser](devario-libs/iniparser/PKGBUILD) | — |
| `intltool` | Added recipe | [devario-development/intltool](devario-development/intltool/PKGBUILD) | — |
| `itstool` | Added recipe | [devario-development/itstool](devario-development/itstool/PKGBUILD) | — |
| `iw` | Added recipe | [devario-utilities/iw](devario-utilities/iw/PKGBUILD) | — |
| `java-environment-common` | Added recipe | [devario-libs/java-common](devario-libs/java-common/PKGBUILD) | — |
| `java-runtime-common` | Added recipe | [devario-libs/java-common](devario-libs/java-common/PKGBUILD) | — |
| `jbig2dec` | Added recipe | [devario-libs/jbig2dec](devario-libs/jbig2dec/PKGBUILD) | — |
| `karchive` | Added recipe | [devario-libs/karchive](devario-libs/karchive/PKGBUILD) | — |
| `kconfig` | Added recipe | [devario-libs/kconfig](devario-libs/kconfig/PKGBUILD) | — |
| `kglobalaccel` | Added recipe | [devario-libs/kglobalaccel](devario-libs/kglobalaccel/PKGBUILD) | — |
| `kirigami` | Added recipe | [devario-libs/kirigami](devario-libs/kirigami/PKGBUILD) | — |
| `kitemmodels` | Added recipe | [devario-libs/kitemmodels](devario-libs/kitemmodels/PKGBUILD) | — |
| `lact` | Added recipe | [devario-utilities/lact](devario-utilities/lact/PKGBUILD) | — |
| `ladspa` | Added recipe | [devario-development/ladspa](devario-development/ladspa/PKGBUILD) | — |
| `laszip2` | Added recipe | [devario-libs/laszip2](devario-libs/laszip2/PKGBUILD) | — |
| `lbzip2` | Added recipe | [devario-development/lbzip2](devario-development/lbzip2/PKGBUILD) | — |
| `lhasa` | Added recipe | [devario-development/lhasa](devario-development/lhasa/PKGBUILD) | — |
| `lib32-alsa-lib` | Added recipe | [devario-libs/lib32-alsa-lib](devario-libs/lib32-alsa-lib/PKGBUILD) | — |
| `lib32-attr` | Added recipe | [devario-libs/lib32-attr](devario-libs/lib32-attr/PKGBUILD) | — |
| `lib32-brotli` | Added recipe | [devario-libs/lib32-brotli](devario-libs/lib32-brotli/PKGBUILD) | — |
| `lib32-bzip2` | Added recipe | [devario-libs/lib32-bzip2](devario-libs/lib32-bzip2/PKGBUILD) | — |
| `lib32-expat` | Added recipe | [devario-libs/lib32-expat](devario-libs/lib32-expat/PKGBUILD) | — |
| `lib32-gmp` | Added recipe | [devario-libs/lib32-gmp](devario-libs/lib32-gmp/PKGBUILD) | — |
| `lib32-icu` | Added recipe | [devario-libs/lib32-icu](devario-libs/lib32-icu/PKGBUILD) | — |
| `lib32-json-c` | Added recipe | [devario-libs/lib32-json-c](devario-libs/lib32-json-c/PKGBUILD) | — |
| `lib32-libdisplay-info` | Added recipe | [devario-libs/lib32-libdisplay-info](devario-libs/lib32-libdisplay-info/PKGBUILD) | — |
| `lib32-libffi` | Added recipe | [devario-libs/lib32-libffi](devario-libs/lib32-libffi/PKGBUILD) | — |
| `lib32-libgpg-error` | Added recipe | [devario-libs/lib32-libgpg-error](devario-libs/lib32-libgpg-error/PKGBUILD) | — |
| `lib32-libndp` | Added recipe | [devario-libs/lib32-libndp](devario-libs/lib32-libndp/PKGBUILD) | — |
| `lib32-libnghttp2` | Added recipe | [devario-libs/lib32-libnghttp2](devario-libs/lib32-libnghttp2/PKGBUILD) | — |
| `lib32-libnghttp3` | Added recipe | [devario-libs/lib32-libnghttp3](devario-libs/lib32-libnghttp3/PKGBUILD) | — |
| `lib32-libogg` | Added recipe | [devario-libs/lib32-libogg](devario-libs/lib32-libogg/PKGBUILD) | — |
| `lib32-libtasn1` | Added recipe | [devario-libs/lib32-libtasn1](devario-libs/lib32-libtasn1/PKGBUILD) | — |
| `lib32-libunistring` | Added recipe | [devario-libs/lib32-libunistring](devario-libs/lib32-libunistring/PKGBUILD) | — |
| `lib32-libxau` | Added recipe | [devario-libs/lib32-libxau](devario-libs/lib32-libxau/PKGBUILD) | — |
| `lib32-libxcrypt` | Added recipe | [devario-libs/lib32-libxcrypt](devario-libs/lib32-libxcrypt/PKGBUILD) | — |
| `lib32-libxcrypt-compat` | Added recipe | [devario-libs/lib32-libxcrypt](devario-libs/lib32-libxcrypt/PKGBUILD) | — |
| `lib32-lm_sensors` | Added recipe | [devario-libs/lib32-lm_sensors](devario-libs/lib32-lm_sensors/PKGBUILD) | — |
| `lib32-ncurses` | Added recipe | [devario-libs/lib32-ncurses](devario-libs/lib32-ncurses/PKGBUILD) | — |
| `lib32-openssl` | Added recipe | [devario-libs/lib32-openssl](devario-libs/lib32-openssl/PKGBUILD) | — |
| `lib32-opus` | Added recipe | [devario-libs/lib32-opus](devario-libs/lib32-opus/PKGBUILD) | — |
| `lib32-speexdsp` | Added recipe | [devario-libs/lib32-speexdsp](devario-libs/lib32-speexdsp/PKGBUILD) | — |
| `lib32-spirv-tools` | Added recipe | [devario-libs/lib32-spirv-tools](devario-libs/lib32-spirv-tools/PKGBUILD) | — |
| `lib32-zlib` | Added recipe | [devario-libs/lib32-zlib](devario-libs/lib32-zlib/PKGBUILD) | — |
| `lib32-zstd` | Added recipe | [devario-libs/lib32-zstd](devario-libs/lib32-zstd/PKGBUILD) | — |
| `libaemu` | Added recipe | [devario-libs/libaemu](devario-libs/libaemu/PKGBUILD) | — |
| `libao` | Added recipe | [devario-libs/libao](devario-libs/libao/PKGBUILD) | — |
| `libburn` | Added recipe | [devario-libs/libburn](devario-libs/libburn/PKGBUILD) | — |
| `libcacard` | Added recipe | [devario-libs/libcacard](devario-libs/libcacard/PKGBUILD) | — |
| `libcue` | Added recipe | [devario-libs/libcue](devario-libs/libcue/PKGBUILD) | — |
| `libdca` | Added recipe | [devario-libs/libdca](devario-libs/libdca/PKGBUILD) | — |
| `libde265` | Added recipe | [devario-libs/libde265](devario-libs/libde265/PKGBUILD) | — |
| `libfreexl` | Added recipe | [devario-libs/libfreexl](devario-libs/libfreexl/PKGBUILD) | — |
| `libgme` | Added recipe | [devario-libs/libgme](devario-libs/libgme/PKGBUILD) | — |
| `libharu` | Added recipe | [devario-libs/libharu](devario-libs/libharu/PKGBUILD) | — |
| `libidn` | Added recipe | [devario-libs/libidn](devario-libs/libidn/PKGBUILD) | — |
| `libiscsi` | Added recipe | [devario-libs/libiscsi](devario-libs/libiscsi/PKGBUILD) | — |
| `libisofs` | Added recipe | [devario-libs/libisofs](devario-libs/libisofs/PKGBUILD) | — |
| `liblqr` | Added recipe | [devario-libs/liblqr](devario-libs/liblqr/PKGBUILD) | — |
| `libltc` | Added recipe | [devario-libs/libltc](devario-libs/libltc/PKGBUILD) | — |
| `libmaxminddb` | Added recipe | [devario-libs/libmaxminddb](devario-libs/libmaxminddb/PKGBUILD) | — |
| `libmicrodns` | Added recipe | [devario-libs/libmicrodns](devario-libs/libmicrodns/PKGBUILD) | — |
| `libmicrohttpd` | Added recipe | [devario-libs/libmicrohttpd](devario-libs/libmicrohttpd/PKGBUILD) | — |
| `libmms` | Added recipe | [devario-libs/libmms](devario-libs/libmms/PKGBUILD) | — |
| `libnfs` | Added recipe | [devario-libs/libnfs](devario-libs/libnfs/PKGBUILD) | — |
| `libpaper` | Added recipe | [devario-libs/libpaper](devario-libs/libpaper/PKGBUILD) | — |
| `libpfm` | Added recipe | [devario-libs/libpfm](devario-libs/libpfm/PKGBUILD) | — |
| `libreplaygain` | Added recipe | [devario-libs/libreplaygain](devario-libs/libreplaygain/PKGBUILD) | — |
| `libsass` | Added recipe | [devario-libs/libsass](devario-libs/libsass/PKGBUILD) | — |
| `libshout` | Added recipe | [devario-libs/libshout](devario-libs/libshout/PKGBUILD) | — |
| `libsigsegv` | Added recipe | [devario-libs/libsigsegv](devario-libs/libsigsegv/PKGBUILD) | — |
| `libsixel` | Added recipe | [devario-libs/libsixel](devario-libs/libsixel/PKGBUILD) | — |
| `libslirp` | Added recipe | [devario-libs/libslirp](devario-libs/libslirp/PKGBUILD) | — |
| `libsonic` | Added recipe | [devario-libs/libsonic](devario-libs/libsonic/PKGBUILD) | — |
| `libspiro` | Added recipe | [devario-libs/libspiro](devario-libs/libspiro/PKGBUILD) | — |
| `libsrtp` | Added recipe | [devario-libs/libsrtp](devario-libs/libsrtp/PKGBUILD) | — |
| `libsrtp-docs` | Added recipe | [devario-libs/libsrtp](devario-libs/libsrtp/PKGBUILD) | — |
| `libtlsrpt` | Added recipe | [devario-libs/libtlsrpt](devario-libs/libtlsrpt/PKGBUILD) | — |
| `libultrahdr` | Added recipe | [devario-libs/libultrahdr](devario-libs/libultrahdr/PKGBUILD) | — |
| `libuninameslist` | Added recipe | [devario-libs/libuninameslist](devario-libs/libuninameslist/PKGBUILD) | — |
| `libunrar` | Added recipe | [devario-utilities/unrar](devario-utilities/unrar/PKGBUILD) | — |
| `libutempter` | Added recipe | [devario-libs/libutempter](devario-libs/libutempter/PKGBUILD) | — |
| `libutf8proc` | Added recipe | [devario-libs/libutf8proc](devario-libs/libutf8proc/PKGBUILD) | — |
| `libvoikko` | Added recipe | [devario-libs/libvoikko](devario-libs/libvoikko/PKGBUILD) | — |
| `libwmf` | Added recipe | [devario-libs/libwmf](devario-libs/libwmf/PKGBUILD) | — |
| `libx86` | Added recipe | [devario-libs/libx86](devario-libs/libx86/PKGBUILD) | — |
| `libxnvctrl` | Added recipe | [devario-utilities/nvidia-settings](devario-utilities/nvidia-settings/PKGBUILD) | — |
| `libyuv` | Added recipe | [devario-libs/libyuv](devario-libs/libyuv/PKGBUILD) | — |
| `libzen` | Added recipe | [devario-libs/libzen](devario-libs/libzen/PKGBUILD) | — |
| `libzip` | Added recipe | [devario-libs/libzip](devario-libs/libzip/PKGBUILD) | — |
| `log4cplus` | Added recipe | [devario-libs/log4cplus](devario-libs/log4cplus/PKGBUILD) | — |
| `logrotate` | Added recipe | [devario-core/logrotate](devario-core/logrotate/PKGBUILD) | — |
| `lrzip` | Added recipe | [devario-development/lrzip](devario-development/lrzip/PKGBUILD) | — |
| `lsb-release` | Added recipe | [devario-utilities/lsb-release](devario-utilities/lsb-release/PKGBUILD) | — |
| `luajit` | Added recipe | [devario-libs/luajit](devario-libs/luajit/PKGBUILD) | — |
| `lynx` | Added recipe | [devario-development/lynx](devario-development/lynx/PKGBUILD) | — |
| `mbedtls3` | Added recipe | [devario-libs/mbedtls3](devario-libs/mbedtls3/PKGBUILD) | — |
| `micro` | Added recipe | [devario-core/micro](devario-core/micro/PKGBUILD) | — |
| `microsoft-gsl` | Added recipe | [devario-libs/microsoft-gsl](devario-libs/microsoft-gsl/PKGBUILD) | — |
| `mingw-w64-binutils` | Added recipe | [devario-development/mingw-w64-binutils](devario-development/mingw-w64-binutils/PKGBUILD) | — |
| `mingw-w64-headers` | Added recipe | [devario-libs/mingw-w64-headers](devario-libs/mingw-w64-headers/PKGBUILD) | — |
| `mingw-w64-tools` | Added recipe | [devario-development/mingw-w64-tools](devario-development/mingw-w64-tools/PKGBUILD) | — |
| `mmdblookup` | Added recipe | [devario-libs/libmaxminddb](devario-libs/libmaxminddb/PKGBUILD) | — |
| `mongo-c-driver` | Added recipe | [devario-libs/mongo-c-driver](devario-libs/mongo-c-driver/PKGBUILD) | — |
| `msgpack-cxx` | Added recipe | [devario-libs/msgpack-cxx](devario-libs/msgpack-cxx/PKGBUILD) | — |
| `mtools` | Added recipe | [devario-utilities/mtools](devario-utilities/mtools/PKGBUILD) | — |
| `mujs` | Added recipe | [devario-libs/mujs](devario-libs/mujs/PKGBUILD) | — |
| `multipath-tools` | Added recipe | [devario-utilities/multipath-tools](devario-utilities/multipath-tools/PKGBUILD) | — |
| `muparser` | Added recipe | [devario-libs/muparser](devario-libs/muparser/PKGBUILD) | — |
| `nano` | Added recipe | [devario-core/nano](devario-core/nano/PKGBUILD) | — |
| `ntsync-autoload` | Added recipe | [devario-utilities/ntsync-autoload](devario-utilities/ntsync-autoload/PKGBUILD) | — |
| `nvidia-settings` | Added recipe | [devario-utilities/nvidia-settings](devario-utilities/nvidia-settings/PKGBUILD) | — |
| `nvm` | Added recipe | [devario-development/nvm](devario-development/nvm/PKGBUILD) | — |
| `nvtop` | Added recipe | [devario-utilities/nvtop](devario-utilities/nvtop/PKGBUILD) | — |
| `ocaml` | Added recipe | [devario-development/ocaml](devario-development/ocaml/PKGBUILD) | — |
| `ocaml-compiler-libs` | Added recipe | [devario-development/ocaml](devario-development/ocaml/PKGBUILD) | — |
| `onednn` | Added recipe | [devario-libs/onednn](devario-libs/onednn/PKGBUILD) | — |
| `opencl-headers` | Added recipe | [devario-libs/opencl-headers](devario-libs/opencl-headers/PKGBUILD) | — |
| `openvr` | Added recipe | [devario-development/openvr](devario-development/openvr/PKGBUILD) | — |
| `openxr` | Added recipe | [devario-libs/openxr](devario-libs/openxr/PKGBUILD) | — |
| `osinfo-db-tools` | Added recipe | [devario-development/osinfo-db-tools](devario-development/osinfo-db-tools/PKGBUILD) | — |
| `otf-atkinsonhyperlegiblemono-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `otf-aurulent-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `otf-codenewroman-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `otf-comicshanns-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `otf-commit-mono-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `otf-droid-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `otf-firamono-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `otf-geist-mono-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `otf-hasklig-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `otf-hermit-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `otf-monaspace-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `otf-opendyslexic-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `otf-overpass-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `pangomm-2.48` | Added recipe | [devario-libs/pangomm-2.48](devario-libs/pangomm-2.48/PKGBUILD) | — |
| `pangomm-2.48-docs` | Added recipe | [devario-libs/pangomm-2.48](devario-libs/pangomm-2.48/PKGBUILD) | — |
| `parallel` | Added recipe | [devario-utilities/parallel](devario-utilities/parallel/PKGBUILD) | — |
| `parallel-docs` | Added recipe | [devario-utilities/parallel](devario-utilities/parallel/PKGBUILD) | — |
| `pcaudiolib` | Added recipe | [devario-libs/pcaudiolib](devario-libs/pcaudiolib/PKGBUILD) | — |
| `perl-archive-cpio` | Added recipe | [devario-libs/perl-archive-cpio](devario-libs/perl-archive-cpio/PKGBUILD) | — |
| `perl-archive-zip` | Added recipe | [devario-libs/perl-archive-zip](devario-libs/perl-archive-zip/PKGBUILD) | — |
| `perl-file-slurp` | Added recipe | [devario-libs/perl-file-slurp](devario-libs/perl-file-slurp/PKGBUILD) | — |
| `perl-file-which` | Added recipe | [devario-libs/perl-file-which](devario-libs/perl-file-which/PKGBUILD) | — |
| `perl-inc-latest` | Added recipe | [devario-libs/perl-inc-latest](devario-libs/perl-inc-latest/PKGBUILD) | — |
| `perl-io-string` | Added recipe | [devario-libs/perl-io-string](devario-libs/perl-io-string/PKGBUILD) | — |
| `perl-json` | Added recipe | [devario-libs/perl-json](devario-libs/perl-json/PKGBUILD) | — |
| `perl-locale-gettext` | Added recipe | [devario-libs/perl-locale-gettext](devario-libs/perl-locale-gettext/PKGBUILD) | — |
| `perl-mime-charset` | Added recipe | [devario-libs/perl-mime-charset](devario-libs/perl-mime-charset/PKGBUILD) | — |
| `perl-params-someutil` | Added recipe | [devario-libs/perl-params-someutil](devario-libs/perl-params-someutil/PKGBUILD) | — |
| `perl-parse-yapp` | Added recipe | [devario-libs/perl-parse-yapp](devario-libs/perl-parse-yapp/PKGBUILD) | — |
| `perl-pod-parser` | Added recipe | [devario-libs/perl-pod-parser](devario-libs/perl-pod-parser/PKGBUILD) | — |
| `perl-sgmls` | Added recipe | [devario-libs/perl-sgmls](devario-libs/perl-sgmls/PKGBUILD) | — |
| `perl-sort-versions` | Added recipe | [devario-libs/perl-sort-versions](devario-libs/perl-sort-versions/PKGBUILD) | — |
| `perl-sub-install` | Added recipe | [devario-libs/perl-sub-install](devario-libs/perl-sub-install/PKGBUILD) | — |
| `perl-term-readkey` | Added recipe | [devario-libs/perl-term-readkey](devario-libs/perl-term-readkey/PKGBUILD) | — |
| `perl-text-charwidth` | Added recipe | [devario-libs/perl-text-charwidth](devario-libs/perl-text-charwidth/PKGBUILD) | — |
| `perl-text-csv` | Added recipe | [devario-libs/perl-text-csv](devario-libs/perl-text-csv/PKGBUILD) | — |
| `perl-yaml-tiny` | Added recipe | [devario-libs/perl-yaml-tiny](devario-libs/perl-yaml-tiny/PKGBUILD) | — |
| `pkcs11-helper` | Added recipe | [devario-libs/pkcs11-helper](devario-libs/pkcs11-helper/PKGBUILD) | — |
| `plasma-wayland-protocols` | Added recipe | [devario-development/plasma-wayland-protocols](devario-development/plasma-wayland-protocols/PKGBUILD) | — |
| `poppler-data` | Added recipe | [devario-libs/poppler-data](devario-libs/poppler-data/PKGBUILD) | — |
| `potrace` | Added recipe | [devario-entertainment/potrace](devario-entertainment/potrace/PKGBUILD) | — |
| `proj` | Added recipe | [devario-libs/proj](devario-libs/proj/PKGBUILD) | — |
| `protobuf-c` | Added recipe | [devario-libs/protobuf-c](devario-libs/protobuf-c/PKGBUILD) | — |
| `publicsuffix-list` | Added recipe | [devario-development/publicsuffix-list](devario-development/publicsuffix-list/PKGBUILD) | — |
| `pugixml` | Added recipe | [devario-libs/pugixml](devario-libs/pugixml/PKGBUILD) | — |
| `qhull` | Added recipe | [devario-libs/qhull](devario-libs/qhull/PKGBUILD) | — |
| `qrencode` | Added recipe | [devario-libs/qrencode](devario-libs/qrencode/PKGBUILD) | — |
| `qt5-declarative` | Added recipe | [devario-libs/qt5-declarative](devario-libs/qt5-declarative/PKGBUILD) | Cycle G159 — seed packages required |
| `qt5-tools` | Added recipe | [devario-libs/qt5-tools](devario-libs/qt5-tools/PKGBUILD) | Cycle G159 — seed packages required |
| `qt5-translations` | Added recipe | [devario-libs/qt5-translations](devario-libs/qt5-translations/PKGBUILD) | Cycle G159 — seed packages required |
| `qt6-5compat` | Added recipe | [devario-libs/qt6-5compat](devario-libs/qt6-5compat/PKGBUILD) | — |
| `qt6-canvaspainter` | Added recipe | [devario-libs/qt6-canvaspainter](devario-libs/qt6-canvaspainter/PKGBUILD) | — |
| `qt6-charts` | Added recipe | [devario-libs/qt6-charts](devario-libs/qt6-charts/PKGBUILD) | — |
| `qt6-connectivity` | Added recipe | [devario-libs/qt6-connectivity](devario-libs/qt6-connectivity/PKGBUILD) | — |
| `qt6-datavis3d` | Added recipe | [devario-libs/qt6-datavis3d](devario-libs/qt6-datavis3d/PKGBUILD) | — |
| `qt6-networkauth` | Added recipe | [devario-libs/qt6-networkauth](devario-libs/qt6-networkauth/PKGBUILD) | — |
| `qt6-quicktimeline` | Added recipe | [devario-libs/qt6-quicktimeline](devario-libs/qt6-quicktimeline/PKGBUILD) | — |
| `qt6-remoteobjects` | Added recipe | [devario-libs/qt6-remoteobjects](devario-libs/qt6-remoteobjects/PKGBUILD) | — |
| `qt6-scxml` | Added recipe | [devario-libs/qt6-scxml](devario-libs/qt6-scxml/PKGBUILD) | — |
| `qt6-sensors` | Added recipe | [devario-libs/qt6-sensors](devario-libs/qt6-sensors/PKGBUILD) | — |
| `qt6-serialport` | Added recipe | [devario-libs/qt6-serialport](devario-libs/qt6-serialport/PKGBUILD) | — |
| `qt6-webchannel` | Added recipe | [devario-libs/qt6-webchannel](devario-libs/qt6-webchannel/PKGBUILD) | — |
| `qt6-websockets` | Added recipe | [devario-libs/qt6-websockets](devario-libs/qt6-websockets/PKGBUILD) | — |
| `qt6pas` | Added recipe | [devario-libs/qt6pas](devario-libs/qt6pas/PKGBUILD) | — |
| `range-v3` | Added recipe | [devario-libs/range-v3](devario-libs/range-v3/PKGBUILD) | — |
| `rapidjson` | Added recipe | [devario-development/rapidjson](devario-development/rapidjson/PKGBUILD) | — |
| `re2` | Added recipe | [devario-libs/re2](devario-libs/re2/PKGBUILD) | — |
| `reflection-cpp` | Added recipe | [devario-libs/reflection-cpp](devario-libs/reflection-cpp/PKGBUILD) | — |
| `riscv64-linux-gnu-linux-api-headers` | Added recipe | [devario-libs/riscv64-linux-gnu-linux-api-headers](devario-libs/riscv64-linux-gnu-linux-api-headers/PKGBUILD) | — |
| `rkcommon` | Added recipe | [devario-libs/rkcommon](devario-libs/rkcommon/PKGBUILD) | — |
| `rnnoise` | Added recipe | [devario-libs/rnnoise](devario-libs/rnnoise/PKGBUILD) | — |
| `robin-map` | Added recipe | [devario-libs/robin-map](devario-libs/robin-map/PKGBUILD) | — |
| `rocm-toolchain` | Added recipe | [devario-development/rocm-toolchain](devario-development/rocm-toolchain/PKGBUILD) | — |
| `roctracer` | Added recipe | [devario-libs/roctracer](devario-libs/roctracer/PKGBUILD) | — |
| `rpcsvc-proto` | Added recipe | [devario-development/rpcsvc-proto](devario-development/rpcsvc-proto/PKGBUILD) | — |
| `rpmextract` | Added recipe | [devario-development/rpmextract](devario-development/rpmextract/PKGBUILD) | — |
| `rtmpdump` | Added recipe | [devario-development/rtmpdump](devario-development/rtmpdump/PKGBUILD) | — |
| `ruby-kramdown` | Added recipe | [devario-libs/ruby-kramdown](devario-libs/ruby-kramdown/PKGBUILD) | — |
| `ruby-mini_portile2` | Added recipe | [devario-libs/ruby-mini_portile2](devario-libs/ruby-mini_portile2/PKGBUILD) | — |
| `ruby-mustache` | Added recipe | [devario-libs/ruby-mustache](devario-libs/ruby-mustache/PKGBUILD) | — |
| `ruby-rdiscount` | Added recipe | [devario-libs/ruby-rdiscount](devario-libs/ruby-rdiscount/PKGBUILD) | — |
| `rust-bindgen` | Added recipe | [devario-libs/rust-bindgen](devario-libs/rust-bindgen/PKGBUILD) | — |
| `rustup` | Added recipe | [devario-development/rustup](devario-development/rustup/PKGBUILD) | — |
| `s2n-tls` | Added recipe | [devario-libs/s2n-tls](devario-libs/s2n-tls/PKGBUILD) | — |
| `safeint` | Added recipe | [devario-libs/safeint](devario-libs/safeint/PKGBUILD) | — |
| `sdl12-compat` | Added recipe | [devario-libs/sdl12-compat](devario-libs/sdl12-compat/PKGBUILD) | — |
| `setconf` | Added recipe | [devario-development/setconf](devario-development/setconf/PKGBUILD) | — |
| `signify` | Added recipe | [devario-development/signify](devario-development/signify/PKGBUILD) | — |
| `simdutf` | Added recipe | [devario-libs/simdutf](devario-libs/simdutf/PKGBUILD) | — |
| `snapper` | Added recipe | [devario-utilities/snapper](devario-utilities/snapper/PKGBUILD) | — |
| `soundtouch` | Added recipe | [devario-libs/soundtouch](devario-libs/soundtouch/PKGBUILD) | — |
| `spice-protocol` | Added recipe | [devario-libs/spice-protocol](devario-libs/spice-protocol/PKGBUILD) | — |
| `spirv-llvm-translator` | Added recipe | [devario-development/spirv-llvm-translator](devario-development/spirv-llvm-translator/PKGBUILD) | — |
| `starship` | Added recipe | [devario-core/starship](devario-core/starship/PKGBUILD) | — |
| `suitesparse` | Added recipe | [devario-libs/suitesparse](devario-libs/suitesparse/PKGBUILD) | — |
| `suitesparse-graphblas` | Added recipe | [devario-libs/suitesparse](devario-libs/suitesparse/PKGBUILD) | — |
| `swig` | Metadata only | [devario-development/swig](devario-development/swig/PKGBUILD) | — |
| `sysfsutils` | Added recipe | [devario-utilities/sysfsutils](devario-utilities/sysfsutils/PKGBUILD) | — |
| `systemd-manager-tui` | Added recipe | [devario-utilities/systemd-manager-tui](devario-utilities/systemd-manager-tui/PKGBUILD) | — |
| `talloc` | Added recipe | [devario-libs/talloc](devario-libs/talloc/PKGBUILD) | — |
| `tcl` | Added recipe | [devario-development/tcl](devario-development/tcl/PKGBUILD) | — |
| `tdb` | Added recipe | [devario-libs/tdb](devario-libs/tdb/PKGBUILD) | — |
| `texi2html` | Added recipe | [devario-development/texi2html](devario-development/texi2html/PKGBUILD) | — |
| `texinfo` | Updated | [isolation-builder/texinfo](isolation-builder/texinfo/PKGBUILD) | Existing Devario dependencies required |
| `tidy` | Added recipe | [devario-utilities/tidy](devario-utilities/tidy/PKGBUILD) | — |
| `tinycdb` | Added recipe | [devario-libs/tinycdb](devario-libs/tinycdb/PKGBUILD) | — |
| `tinyxml2` | Added recipe | [devario-libs/tinyxml2](devario-libs/tinyxml2/PKGBUILD) | — |
| `tree-sitter` | Added recipe | [devario-development/tree-sitter](devario-development/tree-sitter/PKGBUILD) | — |
| `tree-sitter-cli` | Added recipe | [devario-development/tree-sitter](devario-development/tree-sitter/PKGBUILD) | — |
| `ttf-0xproto-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-3270-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-adwaitamono-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-agave-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-annotationmono-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-anonymouspro-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-arimo-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-bigblueterminal-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-bitstream-vera-mono-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-cascadia-code-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-cascadia-mono-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-cousine-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-d2coding-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-daddytime-mono-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-dejavu-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-envycoder-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-fantasque-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-firacode-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-go-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-gohu-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-googlesanscode-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-hack-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-heavydata-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-iawriter-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-ibmplex-mono-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-inconsolata-go-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-inconsolata-lgc-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-inconsolata-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-intone-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-iosevka-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-iosevkaterm-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-iosevkatermslab-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-jetbrains-mono-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-lekton-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-liberation-mono-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-lilex-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-martian-mono-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-meslo-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-monofur-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-monoid-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-mononoki-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-mplus-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-noto-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-profont-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-proggyclean-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-recursive-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-roboto` | Added recipe | [devario-libs/ttf-roboto](devario-libs/ttf-roboto/PKGBUILD) | — |
| `ttf-roboto-mono` | Added recipe | [devario-development/ttf-roboto-mono](devario-development/ttf-roboto-mono/PKGBUILD) | — |
| `ttf-roboto-mono-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-sharetech-mono-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-sourcecodepro-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-space-mono-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-terminus-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-tinos-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-ubuntu-mono-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-ubuntu-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-victor-mono-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-zed-mono-nerd` | Added recipe | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `twolame` | Added recipe | [devario-libs/twolame](devario-libs/twolame/PKGBUILD) | — |
| `uasm` | Added recipe | [devario-development/uasm](devario-development/uasm/PKGBUILD) | — |
| `uchardet` | Added recipe | [devario-libs/uchardet](devario-libs/uchardet/PKGBUILD) | — |
| `unace` | Added recipe | [devario-development/unace](devario-development/unace/PKGBUILD) | — |
| `unicode-character-database` | Added recipe | [devario-libs/unicode-character-database](devario-libs/unicode-character-database/PKGBUILD) | — |
| `unicode-cldr` | Added recipe | [devario-development/unicode-cldr](devario-development/unicode-cldr/PKGBUILD) | — |
| `unicode-cldr-annotations` | Added recipe | [devario-development/unicode-cldr](devario-development/unicode-cldr/PKGBUILD) | — |
| `unifdef` | Added recipe | [devario-development/unifdef](devario-development/unifdef/PKGBUILD) | — |
| `unrar` | Added recipe | [devario-utilities/unrar](devario-utilities/unrar/PKGBUILD) | — |
| `unzip` | Added recipe | [devario-utilities/unzip](devario-utilities/unzip/PKGBUILD) | — |
| `usbredir` | Added recipe | [devario-libs/usbredir](devario-libs/usbredir/PKGBUILD) | — |
| `utf8cpp` | Added recipe | [devario-development/utf8cpp](devario-development/utf8cpp/PKGBUILD) | — |
| `vc-intrinsics` | Added recipe | [devario-development/vc-intrinsics](devario-development/vc-intrinsics/PKGBUILD) | — |
| `verdict` | Added recipe | [devario-libs/verdict](devario-libs/verdict/PKGBUILD) | — |
| `virtiofsd` | Added recipe | [devario-utilities/virtiofsd](devario-utilities/virtiofsd/PKGBUILD) | — |
| `viskores` | Added recipe | [devario-libs/viskores](devario-libs/viskores/PKGBUILD) | — |
| `vscodium-bin` | Added recipe | [devario-development/vscodium-bin](devario-development/vscodium-bin/PKGBUILD) | — |
| `wavpack` | Added recipe | [devario-libs/wavpack](devario-libs/wavpack/PKGBUILD) | — |
| `webrtc-audio-processing` | Added recipe | [devario-libs/webrtc-audio-processing](devario-libs/webrtc-audio-processing/PKGBUILD) | — |
| `wildmidi` | Added recipe | [devario-libs/wildmidi](devario-libs/wildmidi/PKGBUILD) | — |
| `wlr-randr` | Added recipe | [devario-utilities/wlr-randr](devario-utilities/wlr-randr/PKGBUILD) | — |
| `wlrctl` | Added recipe | [devario-utilities/wlrctl](devario-utilities/wlrctl/PKGBUILD) | — |
| `woff2` | Added recipe | [devario-libs/woff2](devario-libs/woff2/PKGBUILD) | — |
| `wolfssl` | Added recipe | [devario-libs/wolfssl](devario-libs/wolfssl/PKGBUILD) | — |
| `wtype` | Added recipe | [devario-utilities/wtype](devario-utilities/wtype/PKGBUILD) | — |
| `xcur2png` | Added recipe | [devario-utilities/xcur2png](devario-utilities/xcur2png/PKGBUILD) | — |
| `xdg-user-dirs-gtk` | Added recipe | [devario-utilities/xdg-user-dirs-gtk](devario-utilities/xdg-user-dirs-gtk/PKGBUILD) | — |
| `xerces-c` | Added recipe | [devario-libs/xerces-c](devario-libs/xerces-c/PKGBUILD) | — |
| `xmlto` | Added recipe | [devario-development/xmlto](devario-development/xmlto/PKGBUILD) | — |
| `xorg-util-macros` | Added recipe | [devario-development/xorg-util-macros](devario-development/xorg-util-macros/PKGBUILD) | — |
| `xsimd` | Added recipe | [devario-libs/xsimd](devario-libs/xsimd/PKGBUILD) | — |
| `xtrans` | Added recipe | [devario-libs/xtrans](devario-libs/xtrans/PKGBUILD) | — |
| `zint` | Added recipe | [devario-libs/zint](devario-libs/zint/PKGBUILD) | — |
| `zint-qt` | Added recipe | [devario-libs/zint](devario-libs/zint/PKGBUILD) | — |
| `zip` | Added recipe | [devario-development/zip](devario-development/zip/PKGBUILD) | — |
| `zita-convolver` | Added recipe | [devario-libs/zita-convolver](devario-libs/zita-convolver/PKGBUILD) | — |
| `zopfli` | Added recipe | [devario-libs/zopfli](devario-libs/zopfli/PKGBUILD) | — |
| `zvbi` | Added recipe | [devario-libs/zvbi](devario-libs/zvbi/PKGBUILD) | — |

## Stage 02

156 packages from 139 recipes.

| Package | Change in commit | Build recipe | Bootstrap / prerequisites |
| --- | --- | --- | --- |
| `7zip` | Added recipe | [devario-utilities/7zip](devario-utilities/7zip/PKGBUILD) | — |
| `alsa-tools` | Added recipe | [devario-utilities/alsa-tools](devario-utilities/alsa-tools/PKGBUILD) | — |
| `aws-c-cal` | Added recipe | [devario-libs/aws-c-cal](devario-libs/aws-c-cal/PKGBUILD) | — |
| `aws-c-compression` | Added recipe | [devario-libs/aws-c-compression](devario-libs/aws-c-compression/PKGBUILD) | — |
| `aws-c-sdkutils` | Added recipe | [devario-libs/aws-c-sdkutils](devario-libs/aws-c-sdkutils/PKGBUILD) | — |
| `aws-checksums` | Added recipe | [devario-libs/aws-checksums](devario-libs/aws-checksums/PKGBUILD) | — |
| `bc` | Added recipe | [devario-utilities/bc](devario-utilities/bc/PKGBUILD) | — |
| `cava` | Added recipe | [devario-entertainment/cava](devario-entertainment/cava/PKGBUILD) | — |
| `clblast` | Added recipe | [devario-libs/clblast](devario-libs/clblast/PKGBUILD) | — |
| `clisp` | Added recipe | [devario-development/clisp](devario-development/clisp/PKGBUILD) | — |
| `composable-kernel` | Added recipe | [devario-libs/composable-kernel](devario-libs/composable-kernel/PKGBUILD) | — |
| `crypto++` | Added recipe | [devario-libs/crypto++](devario-libs/crypto++/PKGBUILD) | — |
| `dateutils` | Added recipe | [devario-development/dateutils](devario-development/dateutils/PKGBUILD) | — |
| `dnssec-anchors` | Added recipe | [devario-utilities/dnssec-anchors](devario-utilities/dnssec-anchors/PKGBUILD) | Cycle G537 — seed packages required |
| `dpkg` | Added recipe | [devario-development/dpkg](devario-development/dpkg/PKGBUILD) | — |
| `eigen` | Added recipe | [devario-libs/eigen](devario-libs/eigen/PKGBUILD) | — |
| `fast_float` | Added recipe | [devario-development/fast_float](devario-development/fast_float/PKGBUILD) | — |
| `flite` | Added recipe | [devario-development/flite](devario-development/flite/PKGBUILD) | — |
| `fluidsynth` | Added recipe | [devario-libs/fluidsynth](devario-libs/fluidsynth/PKGBUILD) | — |
| `gfxstream` | Added recipe | [devario-libs/gfxstream](devario-libs/gfxstream/PKGBUILD) | — |
| `glusterfs` | Added recipe | [devario-utilities/glusterfs](devario-utilities/glusterfs/PKGBUILD) | — |
| `gtkmm-4.0` | Added recipe | [devario-libs/gtkmm-4.0](devario-libs/gtkmm-4.0/PKGBUILD) | — |
| `gtkmm-4.0-docs` | Added recipe | [devario-libs/gtkmm-4.0](devario-libs/gtkmm-4.0/PKGBUILD) | — |
| `inetutils` | Added recipe | [devario-utilities/inetutils](devario-utilities/inetutils/PKGBUILD) | — |
| `jdk8-openjdk` | Added recipe | [devario-development/java8-openjdk](devario-development/java8-openjdk/PKGBUILD) | Seed: `java-environment=8` |
| `jre8-openjdk` | Added recipe | [devario-development/java8-openjdk](devario-development/java8-openjdk/PKGBUILD) | Seed: `java-environment=8` |
| `jre8-openjdk-headless` | Added recipe | [devario-development/java8-openjdk](devario-development/java8-openjdk/PKGBUILD) | Seed: `java-environment=8` |
| `js140` | Added recipe | [devario-libs/js140](devario-libs/js140/PKGBUILD) | — |
| `kcodecs` | Added recipe | [devario-libs/kcodecs](devario-libs/kcodecs/PKGBUILD) | — |
| `ldns` | Added recipe | [devario-libs/ldns](devario-libs/ldns/PKGBUILD) | Cycle G537 — seed packages required |
| `level-zero-headers` | Added recipe | [devario-development/level-zero](devario-development/level-zero/PKGBUILD) | — |
| `level-zero-loader` | Added recipe | [devario-development/level-zero](devario-development/level-zero/PKGBUILD) | — |
| `lib32-acl` | Added recipe | [devario-libs/lib32-acl](devario-libs/lib32-acl/PKGBUILD) | — |
| `lib32-cmocka` | Added recipe | [devario-development/lib32-cmocka](devario-development/lib32-cmocka/PKGBUILD) | — |
| `lib32-directx-headers` | Added recipe | [devario-libs/lib32-directx-headers](devario-libs/lib32-directx-headers/PKGBUILD) | — |
| `lib32-libasyncns` | Added recipe | [devario-libs/lib32-libasyncns](devario-libs/lib32-libasyncns/PKGBUILD) | — |
| `lib32-libgcrypt` | Added recipe | [devario-libs/lib32-libgcrypt](devario-libs/lib32-libgcrypt/PKGBUILD) | — |
| `lib32-libldap` | Added recipe | [devario-libs/lib32-libldap](devario-libs/lib32-libldap/PKGBUILD) | — |
| `lib32-libpciaccess` | Added recipe | [devario-libs/lib32-libpciaccess](devario-libs/lib32-libpciaccess/PKGBUILD) | — |
| `lib32-libpng` | Added recipe | [devario-libs/lib32-libpng](devario-libs/lib32-libpng/PKGBUILD) | — |
| `lib32-libssh2` | Added recipe | [devario-libs/lib32-libssh2](devario-libs/lib32-libssh2/PKGBUILD) | — |
| `lib32-libvorbis` | Added recipe | [devario-libs/lib32-libvorbis](devario-libs/lib32-libvorbis/PKGBUILD) | — |
| `lib32-libxdmcp` | Added recipe | [devario-libs/lib32-libxdmcp](devario-libs/lib32-libxdmcp/PKGBUILD) | — |
| `lib32-libxshmfence` | Added recipe | [devario-libs/lib32-libxshmfence](devario-libs/lib32-libxshmfence/PKGBUILD) | — |
| `lib32-nettle` | Added recipe | [devario-libs/lib32-nettle](devario-libs/lib32-nettle/PKGBUILD) | — |
| `lib32-nspr` | Added recipe | [devario-libs/lib32-nspr](devario-libs/lib32-nspr/PKGBUILD) | — |
| `lib32-p11-kit` | Added recipe | [devario-libs/lib32-p11-kit](devario-libs/lib32-p11-kit/PKGBUILD) | — |
| `lib32-readline` | Added recipe | [devario-libs/lib32-readline](devario-libs/lib32-readline/PKGBUILD) | — |
| `lib32-util-linux` | Added recipe | [devario-libs/lib32-util-linux](devario-libs/lib32-util-linux/PKGBUILD) | — |
| `libavtp` | Added recipe | [devario-libs/libavtp](devario-libs/libavtp/PKGBUILD) | — |
| `libcbor` | Added recipe | [devario-libs/libcbor](devario-libs/libcbor/PKGBUILD) | — |
| `libclc` | Added recipe | [devario-libs/libclc](devario-libs/libclc/PKGBUILD) | — |
| `libdc1394` | Added recipe | [devario-libs/libdc1394](devario-libs/libdc1394/PKGBUILD) | — |
| `libdv` | Added recipe | [devario-libs/libdv](devario-libs/libdv/PKGBUILD) | — |
| `libev` | Added recipe | [devario-libs/libev](devario-libs/libev/PKGBUILD) | — |
| `libgeotiff` | Added recipe | [devario-libs/libgeotiff](devario-libs/libgeotiff/PKGBUILD) | — |
| `libid3tag` | Added recipe | [devario-libs/libid3tag](devario-libs/libid3tag/PKGBUILD) | — |
| `libieee1284` | Added recipe | [devario-libs/libieee1284](devario-libs/libieee1284/PKGBUILD) | — |
| `libisoburn` | Added recipe | [devario-libs/libisoburn](devario-libs/libisoburn/PKGBUILD) | — |
| `libmediainfo` | Added recipe | [devario-libs/libmediainfo](devario-libs/libmediainfo/PKGBUILD) | — |
| `libmpcdec` | Added recipe | [devario-libs/musepack](devario-libs/musepack/PKGBUILD) | — |
| `libnet` | Added recipe | [devario-libs/libnet](devario-libs/libnet/PKGBUILD) | — |
| `librttopo` | Added recipe | [devario-libs/librttopo](devario-libs/librttopo/PKGBUILD) | — |
| `libunicode` | Added recipe | [devario-libs/libunicode](devario-libs/libunicode/PKGBUILD) | — |
| `libxmu` | Added recipe | [devario-libs/libxmu](devario-libs/libxmu/PKGBUILD) | — |
| `libxpm` | Added recipe | [devario-libs/libxpm](devario-libs/libxpm/PKGBUILD) | — |
| `libxpresent` | Added recipe | [devario-libs/libxpresent](devario-libs/libxpresent/PKGBUILD) | — |
| `lsscsi` | Added recipe | [devario-utilities/lsscsi](devario-utilities/lsscsi/PKGBUILD) | — |
| `mgard` | Added recipe | [devario-libs/mgard](devario-libs/mgard/PKGBUILD) | — |
| `mingw-w64-crt` | Added recipe | [devario-libs/mingw-w64-crt](devario-libs/mingw-w64-crt/PKGBUILD) | Cycle G467 — seed packages required |
| `mingw-w64-gcc` | Added recipe | [devario-development/mingw-w64-gcc](devario-development/mingw-w64-gcc/PKGBUILD) | Cycle G467 — seed packages required |
| `mingw-w64-winpthreads` | Added recipe | [devario-libs/mingw-w64-winpthreads](devario-libs/mingw-w64-winpthreads/PKGBUILD) | Cycle G467 — seed packages required |
| `musepack-tools` | Added recipe | [devario-libs/musepack](devario-libs/musepack/PKGBUILD) | — |
| `neon` | Added recipe | [devario-libs/neon](devario-libs/neon/PKGBUILD) | — |
| `neovim` | Updated | [devario-development/neovim](devario-development/neovim/PKGBUILD) | External prerequisites required; see Neovim note below |
| `netcdf` | Added recipe | [devario-libs/netcdf](devario-libs/netcdf/PKGBUILD) | — |
| `nodejs` | Added recipe | [devario-development/nodejs](devario-development/nodejs/PKGBUILD) | — |
| `nodejs-lts-iron` | Added recipe | [devario-development/nodejs-lts-iron](devario-development/nodejs-lts-iron/PKGBUILD) | — |
| `nodejs-lts-krypton` | Added recipe | [devario-development/nodejs-lts-krypton](devario-development/nodejs-lts-krypton/PKGBUILD) | — |
| `nwg-look` | Added recipe | [devario-utilities/nwg-look](devario-utilities/nwg-look/PKGBUILD) | — |
| `ocaml-findlib` | Added recipe | [devario-libs/ocaml-findlib](devario-libs/ocaml-findlib/PKGBUILD) | — |
| `ocamlbuild` | Added recipe | [devario-libs/ocamlbuild](devario-libs/ocamlbuild/PKGBUILD) | — |
| `opam` | Added recipe | [devario-development/opam](devario-development/opam/PKGBUILD) | — |
| `openjdk8-doc` | Added recipe | [devario-development/java8-openjdk](devario-development/java8-openjdk/PKGBUILD) | Seed: `java-environment=8` |
| `openjdk8-src` | Added recipe | [devario-development/java8-openjdk](devario-development/java8-openjdk/PKGBUILD) | Seed: `java-environment=8` |
| `openrgb` | Added recipe | [devario-utilities/openrgb](devario-utilities/openrgb/PKGBUILD) | — |
| `opensp` | Added recipe | [devario-libs/opensp](devario-libs/opensp/PKGBUILD) | — |
| `openvpn` | Added recipe | [devario-utilities/openvpn](devario-utilities/openvpn/PKGBUILD) | — |
| `osinfo-db` | Added recipe | [devario-libs/osinfo-db](devario-libs/osinfo-db/PKGBUILD) | — |
| `patchutils` | Added recipe | [devario-development/patchutils](devario-development/patchutils/PKGBUILD) | — |
| `perl-data-optlist` | Added recipe | [devario-libs/perl-data-optlist](devario-libs/perl-data-optlist/PKGBUILD) | — |
| `perl-font-ttf` | Added recipe | [devario-libs/perl-font-ttf](devario-libs/perl-font-ttf/PKGBUILD) | — |
| `perl-module-build` | Added recipe | [devario-libs/perl-module-build](devario-libs/perl-module-build/PKGBUILD) | — |
| `perl-text-wrapi18n` | Added recipe | [devario-libs/perl-text-wrapi18n](devario-libs/perl-text-wrapi18n/PKGBUILD) | — |
| `perl-unicode-linebreak` | Added recipe | [devario-libs/perl-unicode-linebreak](devario-libs/perl-unicode-linebreak/PKGBUILD) | — |
| `podofo` | Added recipe | [devario-libs/podofo](devario-libs/podofo/PKGBUILD) | — |
| `podofo-tools` | Added recipe | [devario-libs/podofo](devario-libs/podofo/PKGBUILD) | — |
| `popsicle` | Added recipe | [devario-utilities/popsicle](devario-utilities/popsicle/PKGBUILD) | — |
| `postfix` | Added recipe | [devario-development/postfix](devario-development/postfix/PKGBUILD) | — |
| `postfix-cdb` | Added recipe | [devario-development/postfix](devario-development/postfix/PKGBUILD) | — |
| `postfix-ldap` | Added recipe | [devario-development/postfix](devario-development/postfix/PKGBUILD) | — |
| `postfix-lmdb` | Added recipe | [devario-development/postfix](devario-development/postfix/PKGBUILD) | — |
| `postfix-mongodb` | Added recipe | [devario-development/postfix](devario-development/postfix/PKGBUILD) | — |
| `postfix-mysql` | Added recipe | [devario-development/postfix](devario-development/postfix/PKGBUILD) | — |
| `postfix-pcre` | Added recipe | [devario-development/postfix](devario-development/postfix/PKGBUILD) | — |
| `postfix-pgsql` | Added recipe | [devario-development/postfix](devario-development/postfix/PKGBUILD) | — |
| `postfix-sqlite` | Added recipe | [devario-development/postfix](devario-development/postfix/PKGBUILD) | — |
| `proton-ge-custom-bin` | Added recipe | [devario-gaming/proton-ge-custom-bin](devario-gaming/proton-ge-custom-bin/PKGBUILD) | — |
| `python-beautifulsoup4` | Added recipe | [devario-libs/python-beautifulsoup4](devario-libs/python-beautifulsoup4/PKGBUILD) | Cycle G408 — seed packages required |
| `python-click` | Added recipe | [devario-libs/python-click](devario-libs/python-click/PKGBUILD) | — |
| `python-cloudpickle` | Added recipe | [devario-libs/python-cloudpickle](devario-libs/python-cloudpickle/PKGBUILD) | — |
| `python-dnspython` | Added recipe | [devario-libs/python-dnspython](devario-libs/python-dnspython/PKGBUILD) | — |
| `python-idna` | Added recipe | [devario-libs/python-idna](devario-libs/python-idna/PKGBUILD) | — |
| `python-mdurl` | Added recipe | [devario-libs/python-mdurl](devario-libs/python-mdurl/PKGBUILD) | — |
| `python-mypy_extensions` | Added recipe | [devario-development/python-mypy_extensions](devario-development/python-mypy_extensions/PKGBUILD) | — |
| `python-py-cpuinfo2` | Added recipe | [devario-libs/python-py-cpuinfo2](devario-libs/python-py-cpuinfo2/PKGBUILD) | — |
| `python-pyparsing` | Added recipe | [devario-libs/python-pyparsing](devario-libs/python-pyparsing/PKGBUILD) | — |
| `python-roman-numerals-py` | Added recipe | [devario-libs/python-roman-numerals-py](devario-libs/python-roman-numerals-py/PKGBUILD) | — |
| `python-soupsieve` | Added recipe | [devario-libs/python-soupsieve](devario-libs/python-soupsieve/PKGBUILD) | Cycle G408 — seed packages required |
| `python-sphinx-alabaster-theme` | Added recipe | [devario-development/python-sphinx-alabaster-theme](devario-development/python-sphinx-alabaster-theme/PKGBUILD) | — |
| `python-sphinxcontrib-applehelp` | Added recipe | [devario-development/python-sphinxcontrib-applehelp](devario-development/python-sphinxcontrib-applehelp/PKGBUILD) | — |
| `python-sphinxcontrib-devhelp` | Added recipe | [devario-development/python-sphinxcontrib-devhelp](devario-development/python-sphinxcontrib-devhelp/PKGBUILD) | — |
| `python-sphinxcontrib-htmlhelp` | Added recipe | [devario-development/python-sphinxcontrib-htmlhelp](devario-development/python-sphinxcontrib-htmlhelp/PKGBUILD) | — |
| `python-sphinxcontrib-qthelp` | Added recipe | [devario-development/python-sphinxcontrib-qthelp](devario-development/python-sphinxcontrib-qthelp/PKGBUILD) | — |
| `python-sphinxcontrib-serializinghtml` | Added recipe | [devario-development/python-sphinxcontrib-serializinghtml](devario-development/python-sphinxcontrib-serializinghtml/PKGBUILD) | — |
| `qt5-x11extras` | Added recipe | [devario-libs/qt5-x11extras](devario-libs/qt5-x11extras/PKGBUILD) | — |
| `qt6-3d` | Added recipe | [devario-libs/qt6-3d](devario-libs/qt6-3d/PKGBUILD) | — |
| `qt6-httpserver` | Added recipe | [devario-libs/qt6-httpserver](devario-libs/qt6-httpserver/PKGBUILD) | — |
| `qt6-positioning` | Added recipe | [devario-libs/qt6-positioning](devario-libs/qt6-positioning/PKGBUILD) | — |
| `qt6-quick3d` | Added recipe | [devario-libs/qt6-quick3d](devario-libs/qt6-quick3d/PKGBUILD) | — |
| `qt6-serialbus` | Added recipe | [devario-libs/qt6-serialbus](devario-libs/qt6-serialbus/PKGBUILD) | — |
| `read-edid` | Added recipe | [devario-utilities/read-edid](devario-utilities/read-edid/PKGBUILD) | — |
| `riscv64-linux-gnu-binutils` | Added recipe | [devario-development/riscv64-linux-gnu-binutils](devario-development/riscv64-linux-gnu-binutils/PKGBUILD) | — |
| `rocfft` | Added recipe | [devario-libs/rocfft](devario-libs/rocfft/PKGBUILD) | — |
| `rocm-opencl-runtime` | Added recipe | [devario-libs/rocm-opencl-runtime](devario-libs/rocm-opencl-runtime/PKGBUILD) | — |
| `rocprim` | Added recipe | [devario-libs/rocprim](devario-libs/rocprim/PKGBUILD) | — |
| `rocrand` | Added recipe | [devario-libs/rocrand](devario-libs/rocrand/PKGBUILD) | — |
| `ruby-kramdown-parser-gfm` | Added recipe | [devario-libs/ruby-kramdown-parser-gfm](devario-libs/ruby-kramdown-parser-gfm/PKGBUILD) | — |
| `ruby-nokogiri` | Added recipe | [devario-libs/ruby-nokogiri](devario-libs/ruby-nokogiri/PKGBUILD) | — |
| `sassc` | Added recipe | [devario-development/sassc](devario-development/sassc/PKGBUILD) | — |
| `sbsigntools` | Added recipe | [devario-development/sbsigntools](devario-development/sbsigntools/PKGBUILD) | — |
| `seabios` | Added recipe | [devario-utilities/seabios](devario-utilities/seabios/PKGBUILD) | — |
| `seabios-docs` | Added recipe | [devario-utilities/seabios](devario-utilities/seabios/PKGBUILD) | — |
| `sound-theme-freedesktop` | Added recipe | [devario-libs/sound-theme-freedesktop](devario-libs/sound-theme-freedesktop/PKGBUILD) | — |
| `sz` | Added recipe | [devario-libs/sz](devario-libs/sz/PKGBUILD) | — |
| `taglib` | Added recipe | [devario-libs/taglib](devario-libs/taglib/PKGBUILD) | — |
| `tevent` | Added recipe | [devario-libs/tevent](devario-libs/tevent/PKGBUILD) | — |
| `tk` | Added recipe | [devario-libs/tk](devario-libs/tk/PKGBUILD) | — |
| `unbound` | Added recipe | [devario-development/unbound](devario-development/unbound/PKGBUILD) | Cycle G537 — seed packages required |
| `unicode-emoji` | Added recipe | [devario-libs/unicode-emoji](devario-libs/unicode-emoji/PKGBUILD) | — |
| `vde2` | Added recipe | [devario-utilities/vde2](devario-utilities/vde2/PKGBUILD) | — |
| `wget` | Added recipe | [devario-utilities/wget](devario-utilities/wget/PKGBUILD) | — |
| `xorg-xdpyinfo` | Added recipe | [devario-utilities/xorg-xdpyinfo](devario-utilities/xorg-xdpyinfo/PKGBUILD) | — |
| `xorg-xrandr` | Added recipe | [devario-utilities/xorg-xrandr](devario-utilities/xorg-xrandr/PKGBUILD) | — |
| `yelp-xsl` | Added recipe | [devario-libs/yelp-xsl](devario-libs/yelp-xsl/PKGBUILD) | — |
| `zziplib` | Added recipe | [devario-libs/zziplib](devario-libs/zziplib/PKGBUILD) | — |

## Stage 03

75 packages from 53 recipes.

| Package | Change in commit | Build recipe | Bootstrap / prerequisites |
| --- | --- | --- | --- |
| `alsa-plugins` | Added recipe | [devario-libs/alsa-plugins](devario-libs/alsa-plugins/PKGBUILD) | — |
| `aws-c-io` | Added recipe | [devario-libs/aws-c-io](devario-libs/aws-c-io/PKGBUILD) | — |
| `cgns` | Added recipe | [devario-development/cgns](devario-development/cgns/PKGBUILD) | — |
| `dune` | Added recipe | [devario-development/dune](devario-development/dune/PKGBUILD) | Cycle G423 — seed packages required |
| `efitools` | Added recipe | [devario-utilities/efitools](devario-utilities/efitools/PKGBUILD) | — |
| `hipcub` | Added recipe | [devario-libs/hipcub](devario-libs/hipcub/PKGBUILD) | — |
| `hipfft` | Added recipe | [devario-libs/hipfft](devario-libs/hipfft/PKGBUILD) | — |
| `hiprand` | Added recipe | [devario-libs/hiprand](devario-libs/hiprand/PKGBUILD) | — |
| `ispc` | Added recipe | [devario-development/ispc](devario-development/ispc/PKGBUILD) | — |
| `jdk-openjdk` | Updated | [devario-development/jdk-openjdk](devario-development/jdk-openjdk/PKGBUILD) | Seed: `java-environment>=22` |
| `jdk11-openjdk` | Added recipe | [devario-development/java11-openjdk](devario-development/java11-openjdk/PKGBUILD) | Seed: `java-environment=11` |
| `jdk17-openjdk` | Added recipe | [devario-development/java17-openjdk](devario-development/java17-openjdk/PKGBUILD) | Seed: `java-environment=17` |
| `jdk21-openjdk` | Added recipe | [devario-development/java21-openjdk](devario-development/java21-openjdk/PKGBUILD) | Seed: `java-environment=21` |
| `jdk25-openjdk` | Added recipe | [devario-development/java25-openjdk](devario-development/java25-openjdk/PKGBUILD) | Seed: `java-environment=25` |
| `jre-openjdk` | Updated | [devario-development/jdk-openjdk](devario-development/jdk-openjdk/PKGBUILD) | Seed: `java-environment>=22` |
| `jre-openjdk-headless` | Updated | [devario-development/jdk-openjdk](devario-development/jdk-openjdk/PKGBUILD) | Seed: `java-environment>=22` |
| `jre11-openjdk` | Added recipe | [devario-development/java11-openjdk](devario-development/java11-openjdk/PKGBUILD) | Seed: `java-environment=11` |
| `jre11-openjdk-headless` | Added recipe | [devario-development/java11-openjdk](devario-development/java11-openjdk/PKGBUILD) | Seed: `java-environment=11` |
| `jre17-openjdk` | Added recipe | [devario-development/java17-openjdk](devario-development/java17-openjdk/PKGBUILD) | Seed: `java-environment=17` |
| `jre17-openjdk-headless` | Added recipe | [devario-development/java17-openjdk](devario-development/java17-openjdk/PKGBUILD) | Seed: `java-environment=17` |
| `jre21-openjdk` | Added recipe | [devario-development/java21-openjdk](devario-development/java21-openjdk/PKGBUILD) | Seed: `java-environment=21` |
| `jre21-openjdk-headless` | Added recipe | [devario-development/java21-openjdk](devario-development/java21-openjdk/PKGBUILD) | Seed: `java-environment=21` |
| `jre25-openjdk` | Added recipe | [devario-development/java25-openjdk](devario-development/java25-openjdk/PKGBUILD) | Seed: `java-environment=25` |
| `jre25-openjdk-headless` | Added recipe | [devario-development/java25-openjdk](devario-development/java25-openjdk/PKGBUILD) | Seed: `java-environment=25` |
| `lib32-e2fsprogs` | Added recipe | [devario-libs/lib32-e2fsprogs](devario-libs/lib32-e2fsprogs/PKGBUILD) | — |
| `lib32-libavtp` | Added recipe | [devario-libs/lib32-libavtp](devario-libs/lib32-libavtp/PKGBUILD) | — |
| `lib32-libdrm` | Added recipe | [devario-libs/lib32-libdrm](devario-libs/lib32-libdrm/PKGBUILD) | — |
| `lib32-libxcb` | Added recipe | [devario-libs/lib32-libxcb](devario-libs/lib32-libxcb/PKGBUILD) | — |
| `lib32-libxml2` | Added recipe | [devario-libs/lib32-libxml2](devario-libs/lib32-libxml2/PKGBUILD) | — |
| `lib32-pcre2` | Added recipe | [devario-libs/lib32-pcre2](devario-libs/lib32-pcre2/PKGBUILD) | — |
| `lib32-pixman` | Added recipe | [devario-libs/lib32-pixman](devario-libs/lib32-pixman/PKGBUILD) | — |
| `lib32-sqlite` | Added recipe | [devario-libs/lib32-sqlite](devario-libs/lib32-sqlite/PKGBUILD) | — |
| `libnbd` | Added recipe | [devario-libs/libnbd](devario-libs/libnbd/PKGBUILD) | — |
| `libspatialite` | Added recipe | [devario-libs/libspatialite](devario-libs/libspatialite/PKGBUILD) | — |
| `libxaw` | Added recipe | [devario-libs/libxaw](devario-libs/libxaw/PKGBUILD) | — |
| `mjpegtools` | Added recipe | [devario-development/mjpegtools](devario-development/mjpegtools/PKGBUILD) | — |
| `node-gyp` | Added recipe | [devario-development/node-gyp](devario-development/node-gyp/PKGBUILD) | Cycle G012 — seed packages required |
| `nodejs-nopt` | Added recipe | [devario-libs/nodejs-nopt](devario-libs/nodejs-nopt/PKGBUILD) | Cycle G012 — seed packages required |
| `ocaml-csexp` | Added recipe | [devario-libs/ocaml-csexp](devario-libs/ocaml-csexp/PKGBUILD) | Cycle G423 — seed packages required |
| `ocaml-pp` | Added recipe | [devario-libs/ocaml-pp](devario-libs/ocaml-pp/PKGBUILD) | Cycle G423 — seed packages required |
| `ocaml-re` | Added recipe | [devario-libs/ocaml-re](devario-libs/ocaml-re/PKGBUILD) | Cycle G423 — seed packages required |
| `ocaml-result` | Added recipe | [devario-libs/ocaml-result](devario-libs/ocaml-result/PKGBUILD) | Cycle G423 — seed packages required |
| `openal` | Added recipe | [devario-libs/openal](devario-libs/openal/PKGBUILD) | — |
| `openal-examples` | Added recipe | [devario-libs/openal](devario-libs/openal/PKGBUILD) | — |
| `openjade` | Added recipe | [devario-utilities/openjade](devario-utilities/openjade/PKGBUILD) | — |
| `openjdk-doc` | Updated | [devario-development/jdk-openjdk](devario-development/jdk-openjdk/PKGBUILD) | Seed: `java-environment>=22` |
| `openjdk-src` | Updated | [devario-development/jdk-openjdk](devario-development/jdk-openjdk/PKGBUILD) | Seed: `java-environment>=22` |
| `openjdk11-doc` | Added recipe | [devario-development/java11-openjdk](devario-development/java11-openjdk/PKGBUILD) | Seed: `java-environment=11` |
| `openjdk11-src` | Added recipe | [devario-development/java11-openjdk](devario-development/java11-openjdk/PKGBUILD) | Seed: `java-environment=11` |
| `openjdk17-doc` | Added recipe | [devario-development/java17-openjdk](devario-development/java17-openjdk/PKGBUILD) | Seed: `java-environment=17` |
| `openjdk17-src` | Added recipe | [devario-development/java17-openjdk](devario-development/java17-openjdk/PKGBUILD) | Seed: `java-environment=17` |
| `openjdk21-doc` | Added recipe | [devario-development/java21-openjdk](devario-development/java21-openjdk/PKGBUILD) | Seed: `java-environment=21` |
| `openjdk21-src` | Added recipe | [devario-development/java21-openjdk](devario-development/java21-openjdk/PKGBUILD) | Seed: `java-environment=21` |
| `openjdk25-doc` | Added recipe | [devario-development/java25-openjdk](devario-development/java25-openjdk/PKGBUILD) | Seed: `java-environment=25` |
| `openjdk25-src` | Added recipe | [devario-development/java25-openjdk](devario-development/java25-openjdk/PKGBUILD) | Seed: `java-environment=25` |
| `perl-sub-exporter` | Added recipe | [devario-libs/perl-sub-exporter](devario-libs/perl-sub-exporter/PKGBUILD) | — |
| `po4a` | Added recipe | [devario-development/po4a](devario-development/po4a/PKGBUILD) | — |
| `pulseaudio-alsa` | Added recipe | [devario-libs/alsa-plugins](devario-libs/alsa-plugins/PKGBUILD) | — |
| `python-markdown-it-py` | Added recipe | [devario-libs/python-markdown-it-py](devario-libs/python-markdown-it-py/PKGBUILD) | — |
| `qt5pas` | Added recipe | [devario-libs/qt5pas](devario-libs/qt5pas/PKGBUILD) | — |
| `qt6-graphs` | Added recipe | [devario-libs/qt6-graphs](devario-libs/qt6-graphs/PKGBUILD) | — |
| `qt6-location` | Added recipe | [devario-libs/qt6-location](devario-libs/qt6-location/PKGBUILD) | — |
| `qwen-code-bin` | Added recipe | [devario-development/qwen-code-bin](devario-development/qwen-code-bin/PKGBUILD) | — |
| `riscv64-linux-gnu-gcc` | Added recipe | [devario-development/riscv64-linux-gnu-gcc](devario-development/riscv64-linux-gnu-gcc/PKGBUILD) | Cycle G512 — seed packages required |
| `riscv64-linux-gnu-glibc` | Added recipe | [devario-libs/riscv64-linux-gnu-glibc](devario-libs/riscv64-linux-gnu-glibc/PKGBUILD) | Cycle G512 — seed packages required |
| `rocthrust` | Added recipe | [devario-libs/rocthrust](devario-libs/rocthrust/PKGBUILD) | — |
| `ruby-ronn-ng` | Added recipe | [devario-libs/ruby-ronn-ng](devario-libs/ruby-ronn-ng/PKGBUILD) | — |
| `semver` | Added recipe | [devario-libs/semver](devario-libs/semver/PKGBUILD) | Cycle G012 — seed packages required |
| `spice` | Added recipe | [devario-libs/spice](devario-libs/spice/PKGBUILD) | — |
| `xclip` | Added recipe | [devario-utilities/xclip](devario-utilities/xclip/PKGBUILD) | — |
| `xorg-xauth` | Added recipe | [devario-development/xorg-xauth](devario-development/xorg-xauth/PKGBUILD) | — |
| `xorg-xeyes` | Added recipe | [devario-utilities/xorg-xeyes](devario-utilities/xorg-xeyes/PKGBUILD) | — |
| `xorg-xinput` | Added recipe | [devario-utilities/xorg-xinput](devario-utilities/xorg-xinput/PKGBUILD) | — |
| `xorg-xkill` | Added recipe | [devario-utilities/xorg-xkill](devario-utilities/xorg-xkill/PKGBUILD) | — |
| `yarn` | Added recipe | [devario-development/yarn](devario-development/yarn/PKGBUILD) | Seed: `yarn` |

## Stage 04

33 packages from 28 recipes.

| Package | Change in commit | Build recipe | Bootstrap / prerequisites |
| --- | --- | --- | --- |
| `aws-c-event-stream` | Added recipe | [devario-libs/aws-c-event-stream](devario-libs/aws-c-event-stream/PKGBUILD) | — |
| `aws-c-http` | Added recipe | [devario-libs/aws-c-http](devario-libs/aws-c-http/PKGBUILD) | — |
| `cline-cli` | Added recipe | [devario-development/cline-cli](devario-development/cline-cli/PKGBUILD) | — |
| `docbook-utils` | Added recipe | [devario-development/docbook-utils](devario-development/docbook-utils/PKGBUILD) | — |
| `embree` | Added recipe | [devario-libs/embree](devario-libs/embree/PKGBUILD) | — |
| `espeak-ng` | Added recipe | [devario-utilities/espeak-ng](devario-utilities/espeak-ng/PKGBUILD) | — |
| `git-lfs` | Added recipe | [devario-development/git-lfs](devario-development/git-lfs/PKGBUILD) | — |
| `groovy` | Added recipe | [devario-development/groovy](devario-development/groovy/PKGBUILD) | — |
| `lazarus` | Added recipe | [devario-development/lazarus](devario-development/lazarus/PKGBUILD) | — |
| `lazarus-qt5` | Added recipe | [devario-development/lazarus](devario-development/lazarus/PKGBUILD) | — |
| `lazarus-qt6` | Added recipe | [devario-development/lazarus](devario-development/lazarus/PKGBUILD) | — |
| `lib32-keyutils` | Added recipe | [devario-libs/lib32-keyutils](devario-libs/lib32-keyutils/PKGBUILD) | Cycle G672 — seed packages required |
| `lib32-krb5` | Added recipe | [devario-libs/lib32-krb5](devario-libs/lib32-krb5/PKGBUILD) | Cycle G672 — seed packages required |
| `lib32-libx11` | Added recipe | [devario-libs/lib32-libx11](devario-libs/lib32-libx11/PKGBUILD) | — |
| `lib32-llvm` | Added recipe | [devario-libs/lib32-llvm](devario-libs/lib32-llvm/PKGBUILD) | — |
| `lib32-llvm-libs` | Added recipe | [devario-libs/lib32-llvm](devario-libs/lib32-llvm/PKGBUILD) | — |
| `lib32-wayland` | Added recipe | [devario-libs/lib32-wayland](devario-libs/lib32-wayland/PKGBUILD) | — |
| `lib32-xcb-util-keysyms` | Added recipe | [devario-libs/lib32-xcb-util-keysyms](devario-libs/lib32-xcb-util-keysyms/PKGBUILD) | — |
| `lib32-xz` | Added recipe | [devario-libs/lib32-xz](devario-libs/lib32-xz/PKGBUILD) | — |
| `libvirt` | Added recipe | [devario-libs/libvirt](devario-libs/libvirt/PKGBUILD) | — |
| `libvirt-storage-gluster` | Added recipe | [devario-libs/libvirt](devario-libs/libvirt/PKGBUILD) | — |
| `libvirt-storage-iscsi-direct` | Added recipe | [devario-libs/libvirt](devario-libs/libvirt/PKGBUILD) | — |
| `marked` | Added recipe | [devario-libs/marked](devario-libs/marked/PKGBUILD) | — |
| `mpv` | Added recipe | [devario-entertainment/mpv](devario-entertainment/mpv/PKGBUILD) | — |
| `ocaml-bigarray-compat` | Added recipe | [devario-libs/ocaml-bigarray-compat](devario-libs/ocaml-bigarray-compat/PKGBUILD) | — |
| `ocaml-stdlib-shims` | Added recipe | [devario-libs/ocaml-stdlib-shims](devario-libs/ocaml-stdlib-shims/PKGBUILD) | — |
| `ocaml-topkg` | Added recipe | [devario-libs/ocaml-topkg](devario-libs/ocaml-topkg/PKGBUILD) | — |
| `openimagedenoise` | Added recipe | [devario-libs/openimagedenoise](devario-libs/openimagedenoise/PKGBUILD) | — |
| `perl-sub-prototype` | Added recipe | [devario-libs/perl-sub-prototype](devario-libs/perl-sub-prototype/PKGBUILD) | — |
| `pnpm` | Added recipe | [devario-development/pnpm](devario-development/pnpm/PKGBUILD) | Seed: `pnpm` |
| `python-mdit_py_plugins` | Added recipe | [devario-libs/python-mdit_py_plugins](devario-libs/python-mdit_py_plugins/PKGBUILD) | — |
| `python-rich` | Added recipe | [devario-libs/python-rich](devario-libs/python-rich/PKGBUILD) | — |
| `typescript` | Added recipe | [devario-development/typescript](devario-development/typescript/PKGBUILD) | — |

## Stage 05

95 packages from 91 recipes.

| Package | Change in commit | Build recipe | Bootstrap / prerequisites |
| --- | --- | --- | --- |
| `asciidoc` | Added recipe | [devario-development/asciidoc](devario-development/asciidoc/PKGBUILD) | — |
| `aws-c-auth` | Added recipe | [devario-libs/aws-c-auth](devario-libs/aws-c-auth/PKGBUILD) | — |
| `aws-c-mqtt` | Added recipe | [devario-libs/aws-c-mqtt](devario-libs/aws-c-mqtt/PKGBUILD) | — |
| `capstone` | Added recipe | [devario-libs/capstone](devario-libs/capstone/PKGBUILD) | — |
| `conduit-llnl` | Added recipe | [devario-libs/conduit-llnl](devario-libs/conduit-llnl/PKGBUILD) | — |
| `dtc` | Added recipe | [devario-utilities/dtc](devario-utilities/dtc/PKGBUILD) | — |
| `flatbuffers` | Added recipe | [devario-libs/flatbuffers](devario-libs/flatbuffers/PKGBUILD) | — |
| `ghostscript` | Added recipe | [devario-utilities/ghostscript](devario-utilities/ghostscript/PKGBUILD) | Cycle G039 — seed packages required |
| `github-desktop` | Added recipe | [devario-development/github-desktop](devario-development/github-desktop/PKGBUILD) | — |
| `gyp` | Added recipe | [devario-development/gyp](devario-development/gyp/PKGBUILD) | — |
| `i2c-tools` | Added recipe | [devario-utilities/i2c-tools](devario-utilities/i2c-tools/PKGBUILD) | — |
| `ijs` | Added recipe | [devario-libs/ijs](devario-libs/ijs/PKGBUILD) | Cycle G039 — seed packages required |
| `lib32-clang` | Added recipe | [devario-libs/lib32-clang](devario-libs/lib32-clang/PKGBUILD) | — |
| `lib32-libxext` | Added recipe | [devario-libs/lib32-libxext](devario-libs/lib32-libxext/PKGBUILD) | — |
| `lib32-libxfixes` | Added recipe | [devario-libs/lib32-libxfixes](devario-libs/lib32-libxfixes/PKGBUILD) | — |
| `lib32-libxrender` | Added recipe | [devario-libs/lib32-libxrender](devario-libs/lib32-libxrender/PKGBUILD) | — |
| `lib32-spirv-llvm-translator` | Added recipe | [devario-libs/lib32-spirv-llvm-translator](devario-libs/lib32-spirv-llvm-translator/PKGBUILD) | — |
| `liblouis` | Added recipe | [devario-libs/liblouis](devario-libs/liblouis/PKGBUILD) | — |
| `libspeechd` | Added recipe | [devario-utilities/speech-dispatcher](devario-utilities/speech-dispatcher/PKGBUILD) | — |
| `libvirt-python` | Added recipe | [devario-libs/libvirt-python](devario-libs/libvirt-python/PKGBUILD) | — |
| `mallard-ducktype` | Added recipe | [devario-development/mallard-ducktype](devario-development/mallard-ducktype/PKGBUILD) | — |
| `marked-man` | Added recipe | [devario-development/marked-man](devario-development/marked-man/PKGBUILD) | — |
| `mercurial` | Added recipe | [devario-development/mercurial](devario-development/mercurial/PKGBUILD) | — |
| `net-snmp` | Added recipe | [devario-utilities/net-snmp](devario-utilities/net-snmp/PKGBUILD) | — |
| `ocaml-integers` | Added recipe | [devario-libs/ocaml-integers](devario-libs/ocaml-integers/PKGBUILD) | — |
| `perl-sub-override` | Added recipe | [devario-libs/perl-sub-override](devario-libs/perl-sub-override/PKGBUILD) | — |
| `python-accessible-pygments` | Added recipe | [devario-libs/python-accessible-pygments](devario-libs/python-accessible-pygments/PKGBUILD) | — |
| `python-appdirs` | Added recipe | [devario-libs/python-appdirs](devario-libs/python-appdirs/PKGBUILD) | — |
| `python-argcomplete` | Added recipe | [devario-libs/python-argcomplete](devario-libs/python-argcomplete/PKGBUILD) | — |
| `python-cachetools` | Added recipe | [devario-libs/python-cachetools](devario-libs/python-cachetools/PKGBUILD) | — |
| `python-capstone` | Added recipe | [devario-libs/capstone](devario-libs/capstone/PKGBUILD) | — |
| `python-certifi` | Added recipe | [devario-libs/python-certifi](devario-libs/python-certifi/PKGBUILD) | — |
| `python-cppy` | Added recipe | [devario-libs/python-cppy](devario-libs/python-cppy/PKGBUILD) | — |
| `python-cycler` | Added recipe | [devario-libs/python-cycler](devario-libs/python-cycler/PKGBUILD) | — |
| `python-dbusmock` | Added recipe | [devario-development/python-dbusmock](devario-development/python-dbusmock/PKGBUILD) | — |
| `python-distlib` | Added recipe | [devario-libs/python-distlib](devario-libs/python-distlib/PKGBUILD) | — |
| `python-evdev` | Added recipe | [devario-libs/python-evdev](devario-libs/python-evdev/PKGBUILD) | — |
| `python-filelock` | Added recipe | [devario-libs/python-filelock](devario-libs/python-filelock/PKGBUILD) | — |
| `python-flatbuffers` | Added recipe | [devario-libs/flatbuffers](devario-libs/flatbuffers/PKGBUILD) | — |
| `python-fonttools` | Added recipe | [devario-libs/python-fonttools](devario-libs/python-fonttools/PKGBUILD) | — |
| `python-fsspec` | Added recipe | [devario-libs/python-fsspec](devario-libs/python-fsspec/PKGBUILD) | — |
| `python-gast` | Added recipe | [devario-libs/python-gast](devario-libs/python-gast/PKGBUILD) | — |
| `python-gmpy2` | Added recipe | [devario-libs/python-gmpy2](devario-libs/python-gmpy2/PKGBUILD) | — |
| `python-greenlet` | Added recipe | [devario-libs/python-greenlet](devario-libs/python-greenlet/PKGBUILD) | — |
| `python-h11` | Added recipe | [devario-libs/python-h11](devario-libs/python-h11/PKGBUILD) | — |
| `python-httplib2` | Added recipe | [devario-libs/python-httplib2](devario-libs/python-httplib2/PKGBUILD) | — |
| `python-imagesize` | Added recipe | [devario-libs/python-imagesize](devario-libs/python-imagesize/PKGBUILD) | — |
| `python-iniconfig` | Added recipe | [devario-libs/python-iniconfig](devario-libs/python-iniconfig/PKGBUILD) | — |
| `python-inputs` | Added recipe | [devario-libs/python-inputs](devario-libs/python-inputs/PKGBUILD) | — |
| `python-joblib` | Added recipe | [devario-libs/python-joblib](devario-libs/python-joblib/PKGBUILD) | — |
| `python-librt` | Added recipe | [devario-libs/python-librt](devario-libs/python-librt/PKGBUILD) | — |
| `python-magic` | Added recipe | [devario-libs/python-magic](devario-libs/python-magic/PKGBUILD) | — |
| `python-markdown` | Added recipe | [devario-libs/python-markdown](devario-libs/python-markdown/PKGBUILD) | — |
| `python-markupsafe` | Added recipe | [devario-libs/python-markupsafe](devario-libs/python-markupsafe/PKGBUILD) | — |
| `python-mpi4py` | Added recipe | [devario-libs/python-mpi4py](devario-libs/python-mpi4py/PKGBUILD) | — |
| `python-msgpack` | Added recipe | [devario-libs/python-msgpack](devario-libs/python-msgpack/PKGBUILD) | — |
| `python-nodeenv` | Added recipe | [devario-libs/python-nodeenv](devario-libs/python-nodeenv/PKGBUILD) | — |
| `python-pefile` | Added recipe | [devario-libs/python-pefile](devario-libs/python-pefile/PKGBUILD) | — |
| `python-py3c` | Added recipe | [devario-libs/python-py3c](devario-libs/python-py3c/PKGBUILD) | — |
| `python-pyclipper` | Added recipe | [devario-libs/python-pyclipper](devario-libs/python-pyclipper/PKGBUILD) | — |
| `python-pycparser` | Added recipe | [devario-libs/python-pycparser](devario-libs/python-pycparser/PKGBUILD) | — |
| `python-pycryptodomex` | Added recipe | [devario-libs/python-pycryptodomex](devario-libs/python-pycryptodomex/PKGBUILD) | — |
| `python-pytz` | Added recipe | [devario-libs/python-pytz](devario-libs/python-pytz/PKGBUILD) | — |
| `python-pyzstd` | Added recipe | [devario-libs/python-pyzstd](devario-libs/python-pyzstd/PKGBUILD) | — |
| `python-scikit-build-core` | Added recipe | [devario-libs/python-scikit-build-core](devario-libs/python-scikit-build-core/PKGBUILD) | — |
| `python-semantic-version` | Added recipe | [devario-libs/python-semantic-version](devario-libs/python-semantic-version/PKGBUILD) | — |
| `python-setuptools-reproducible` | Added recipe | [devario-development/python-setuptools-reproducible](devario-development/python-setuptools-reproducible/PKGBUILD) | — |
| `python-simplejson` | Added recipe | [devario-libs/python-simplejson](devario-libs/python-simplejson/PKGBUILD) | — |
| `python-six` | Added recipe | [devario-libs/python-six](devario-libs/python-six/PKGBUILD) | — |
| `python-smartypants` | Added recipe | [devario-libs/python-smartypants](devario-libs/python-smartypants/PKGBUILD) | — |
| `python-snowballstemmer` | Added recipe | [devario-libs/python-snowballstemmer](devario-libs/python-snowballstemmer/PKGBUILD) | — |
| `python-sphinxcontrib-jsmath` | Added recipe | [devario-development/python-sphinxcontrib-jsmath](devario-development/python-sphinxcontrib-jsmath/PKGBUILD) | — |
| `python-text-unidecode` | Added recipe | [devario-libs/python-text-unidecode](devario-libs/python-text-unidecode/PKGBUILD) | — |
| `python-thrift` | Added recipe | [devario-libs/thrift](devario-libs/thrift/PKGBUILD) | — |
| `python-toml` | Added recipe | [devario-libs/python-toml](devario-libs/python-toml/PKGBUILD) | — |
| `python-ufonormalizer` | Added recipe | [devario-libs/python-ufonormalizer](devario-libs/python-ufonormalizer/PKGBUILD) | — |
| `python-ujson` | Added recipe | [devario-libs/python-ujson](devario-libs/python-ujson/PKGBUILD) | — |
| `python-unicodedata2` | Added recipe | [devario-libs/python-unicodedata2](devario-libs/python-unicodedata2/PKGBUILD) | — |
| `python-urllib3` | Added recipe | [devario-libs/python-urllib3](devario-libs/python-urllib3/PKGBUILD) | — |
| `python-vdf` | Added recipe | [devario-libs/python-vdf](devario-libs/python-vdf/PKGBUILD) | — |
| `python-versioneer` | Added recipe | [devario-libs/python-versioneer](devario-libs/python-versioneer/PKGBUILD) | — |
| `python-webencodings` | Added recipe | [devario-libs/python-webencodings](devario-libs/python-webencodings/PKGBUILD) | — |
| `python-xxhash` | Added recipe | [devario-libs/python-xxhash](devario-libs/python-xxhash/PKGBUILD) | — |
| `python-zope-event` | Added recipe | [devario-libs/python-zope-event](devario-libs/python-zope-event/PKGBUILD) | — |
| `python-zope-interface` | Added recipe | [devario-libs/python-zope-interface](devario-libs/python-zope-interface/PKGBUILD) | — |
| `python-zopfli` | Added recipe | [devario-libs/python-zopfli](devario-libs/python-zopfli/PKGBUILD) | — |
| `python-zstandard` | Added recipe | [devario-libs/python-zstandard](devario-libs/python-zstandard/PKGBUILD) | — |
| `reflector` | Added recipe | [devario-utilities/reflector](devario-utilities/reflector/PKGBUILD) | — |
| `scons` | Added recipe | [devario-development/scons](devario-development/scons/PKGBUILD) | — |
| `speech-dispatcher` | Added recipe | [devario-utilities/speech-dispatcher](devario-utilities/speech-dispatcher/PKGBUILD) | — |
| `thrift` | Added recipe | [devario-libs/thrift](devario-libs/thrift/PKGBUILD) | — |
| `ufw` | Added recipe | [devario-core/ufw](devario-core/ufw/PKGBUILD) | — |
| `vesktop` | Added recipe | [devario-gaming/vesktop](devario-gaming/vesktop/PKGBUILD) | — |
| `vkbasalt-cli` | Added recipe | [devario-gaming/vkbasalt-cli](devario-gaming/vkbasalt-cli/PKGBUILD) | — |
| `zfp` | Added recipe | [devario-libs/zfp](devario-libs/zfp/PKGBUILD) | — |

## Stage 06

50 packages from 44 recipes.

| Package | Change in commit | Build recipe | Bootstrap / prerequisites |
| --- | --- | --- | --- |
| `aws-c-s3` | Added recipe | [devario-libs/aws-c-s3](devario-libs/aws-c-s3/PKGBUILD) | — |
| `blosc2` | Added recipe | [devario-libs/blosc2](devario-libs/blosc2/PKGBUILD) | — |
| `cifs-utils` | Added recipe | [devario-utilities/cifs-utils](devario-utilities/cifs-utils/PKGBUILD) | Cycle G650 — seed packages required |
| `colm` | Added recipe | [devario-development/colm](devario-development/colm/PKGBUILD) | — |
| `gradle` | Added recipe | [devario-development/gradle](devario-development/gradle/PKGBUILD) | — |
| `gradle-doc` | Added recipe | [devario-development/gradle](devario-development/gradle/PKGBUILD) | — |
| `gradle-src` | Added recipe | [devario-development/gradle](devario-development/gradle/PKGBUILD) | — |
| `ldb` | Added recipe | [devario-utilities/samba](devario-utilities/samba/PKGBUILD) | Cycle G650 — seed packages required |
| `lib32-libxinerama` | Added recipe | [devario-libs/lib32-libxinerama](devario-libs/lib32-libxinerama/PKGBUILD) | — |
| `lib32-libxrandr` | Added recipe | [devario-libs/lib32-libxrandr](devario-libs/lib32-libxrandr/PKGBUILD) | — |
| `lib32-libxss` | Added recipe | [devario-libs/lib32-libxss](devario-libs/lib32-libxss/PKGBUILD) | — |
| `lib32-libxxf86vm` | Added recipe | [devario-libs/lib32-libxxf86vm](devario-libs/lib32-libxxf86vm/PKGBUILD) | — |
| `lib32-nss` | Added recipe | [devario-libs/lib32-nss](devario-libs/lib32-nss/PKGBUILD) | — |
| `libspectre` | Added recipe | [devario-libs/libspectre](devario-libs/libspectre/PKGBUILD) | — |
| `libtraceevent` | Added recipe | [devario-libs/libtraceevent](devario-libs/libtraceevent/PKGBUILD) | — |
| `libtraceevent-docs` | Added recipe | [devario-libs/libtraceevent](devario-libs/libtraceevent/PKGBUILD) | — |
| `libwbclient` | Added recipe | [devario-utilities/samba](devario-utilities/samba/PKGBUILD) | Cycle G650 — seed packages required |
| `nanobind` | Added recipe | [devario-libs/nanobind](devario-libs/nanobind/PKGBUILD) | — |
| `nasm` | Added recipe | [devario-development/nasm](devario-development/nasm/PKGBUILD) | — |
| `ocaml-ctypes` | Added recipe | [devario-libs/ocaml-ctypes](devario-libs/ocaml-ctypes/PKGBUILD) | — |
| `paraview-catalyst` | Added recipe | [devario-libs/paraview-catalyst](devario-libs/paraview-catalyst/PKGBUILD) | — |
| `pastebinit` | Added recipe | [devario-utilities/pastebinit](devario-utilities/pastebinit/PKGBUILD) | — |
| `patool` | Added recipe | [devario-utilities/patool](devario-utilities/patool/PKGBUILD) | — |
| `python-babel` | Added recipe | [devario-libs/python-babel](devario-libs/python-babel/PKGBUILD) | — |
| `python-beniget` | Added recipe | [devario-libs/python-beniget](devario-libs/python-beniget/PKGBUILD) | — |
| `python-booleanoperations` | Added recipe | [devario-libs/python-booleanoperations](devario-libs/python-booleanoperations/PKGBUILD) | — |
| `python-cffi` | Added recipe | [devario-libs/python-cffi](devario-libs/python-cffi/PKGBUILD) | — |
| `python-dateutil` | Added recipe | [devario-libs/python-dateutil](devario-libs/python-dateutil/PKGBUILD) | — |
| `python-fontmath` | Added recipe | [devario-libs/python-fontmath](devario-libs/python-fontmath/PKGBUILD) | — |
| `python-fontpens` | Added recipe | [devario-libs/python-fontpens](devario-libs/python-fontpens/PKGBUILD) | — |
| `python-fs` | Added recipe | [devario-libs/python-fs](devario-libs/python-fs/PKGBUILD) | — |
| `python-html5lib` | Added recipe | [devario-libs/python-html5lib](devario-libs/python-html5lib/PKGBUILD) | — |
| `python-jinja` | Added recipe | [devario-libs/python-jinja](devario-libs/python-jinja/PKGBUILD) | — |
| `python-kiwisolver` | Added recipe | [devario-libs/python-kiwisolver](devario-libs/python-kiwisolver/PKGBUILD) | — |
| `python-mako` | Added recipe | [devario-libs/python-mako](devario-libs/python-mako/PKGBUILD) | — |
| `python-mpmath` | Added recipe | [devario-libs/python-mpmath](devario-libs/python-mpmath/PKGBUILD) | — |
| `python-pytest` | Added recipe | [devario-development/python-pytest](devario-development/python-pytest/PKGBUILD) | — |
| `python-python-discovery` | Added recipe | [devario-libs/python-python-discovery](devario-libs/python-python-discovery/PKGBUILD) | — |
| `python-setuptools-rust` | Added recipe | [devario-development/python-setuptools-rust](devario-development/python-setuptools-rust/PKGBUILD) | — |
| `python-slugify` | Added recipe | [devario-libs/python-slugify](devario-libs/python-slugify/PKGBUILD) | — |
| `python-sphinx-theme-builder` | Added recipe | [devario-development/python-sphinx-theme-builder](devario-development/python-sphinx-theme-builder/PKGBUILD) | — |
| `python-tensile` | Added recipe | [devario-libs/python-tensile](devario-libs/python-tensile/PKGBUILD) | — |
| `python-typogrify` | Added recipe | [devario-libs/python-typogrify](devario-libs/python-typogrify/PKGBUILD) | — |
| `python-wsproto` | Added recipe | [devario-libs/python-wsproto](devario-libs/python-wsproto/PKGBUILD) | — |
| `python-xlib` | Added recipe | [devario-libs/python-xlib](devario-libs/python-xlib/PKGBUILD) | — |
| `rebuild-detector` | Added recipe | [devario-development/rebuild-detector](devario-development/rebuild-detector/PKGBUILD) | — |
| `samba` | Added recipe | [devario-utilities/samba](devario-utilities/samba/PKGBUILD) | Cycle G650 — seed packages required |
| `serf` | Added recipe | [devario-libs/serf](devario-libs/serf/PKGBUILD) | — |
| `smbclient` | Added recipe | [devario-utilities/samba](devario-utilities/samba/PKGBUILD) | Cycle G650 — seed packages required |
| `strip-nondeterminism` | Added recipe | [devario-development/strip-nondeterminism](devario-development/strip-nondeterminism/PKGBUILD) | — |

## Stage 07

48 packages from 26 recipes.

| Package | Change in commit | Build recipe | Bootstrap / prerequisites |
| --- | --- | --- | --- |
| `adios2` | Added recipe | [devario-development/adios2](devario-development/adios2/PKGBUILD) | — |
| `aws-crt-cpp` | Added recipe | [devario-libs/aws-crt-cpp](devario-libs/aws-crt-cpp/PKGBUILD) | — |
| `bootconfig` | Added recipe | [devario-utilities/linux-tools](devario-utilities/linux-tools/PKGBUILD) | — |
| `bpf` | Added recipe | [devario-utilities/linux-tools](devario-utilities/linux-tools/PKGBUILD) | — |
| `brltty` | Added recipe | [devario-utilities/brltty](devario-utilities/brltty/PKGBUILD) | — |
| `brltty-udev-generic` | Added recipe | [devario-utilities/brltty](devario-utilities/brltty/PKGBUILD) | — |
| `bun` | Added recipe | [devario-development/bun](devario-development/bun/PKGBUILD) | — |
| `cpupower` | Added recipe | [devario-utilities/linux-tools](devario-utilities/linux-tools/PKGBUILD) | — |
| `dracut-brltty` | Added recipe | [devario-utilities/brltty](devario-utilities/brltty/PKGBUILD) | — |
| `edk2-aarch64` | Added recipe | [devario-utilities/edk2](devario-utilities/edk2/PKGBUILD) | — |
| `edk2-ovmf` | Added recipe | [devario-utilities/edk2](devario-utilities/edk2/PKGBUILD) | — |
| `edk2-riscv64` | Added recipe | [devario-utilities/edk2](devario-utilities/edk2/PKGBUILD) | — |
| `edk2-shell` | Added recipe | [devario-utilities/edk2](devario-utilities/edk2/PKGBUILD) | — |
| `gi-docgen` | Added recipe | [devario-libs/gi-docgen](devario-libs/gi-docgen/PKGBUILD) | — |
| `gjs` | Added recipe | [devario-libs/gjs](devario-libs/gjs/PKGBUILD) | — |
| `hyperv` | Added recipe | [devario-utilities/linux-tools](devario-utilities/linux-tools/PKGBUILD) | — |
| `intel-speed-select` | Added recipe | [devario-utilities/linux-tools](devario-utilities/linux-tools/PKGBUILD) | — |
| `java-brltty` | Added recipe | [devario-utilities/brltty](devario-utilities/brltty/PKGBUILD) | — |
| `java-hamcrest` | Added recipe | [devario-libs/java-hamcrest](devario-libs/java-hamcrest/PKGBUILD) | — |
| `kcpuid` | Added recipe | [devario-utilities/linux-tools](devario-utilities/linux-tools/PKGBUILD) | — |
| `lib32-flac` | Added recipe | [devario-libs/lib32-flac](devario-libs/lib32-flac/PKGBUILD) | — |
| `libavif` | Added recipe | [devario-libs/libavif](devario-libs/libavif/PKGBUILD) | — |
| `libtracefs` | Added recipe | [devario-libs/libtracefs](devario-libs/libtracefs/PKGBUILD) | — |
| `libtracefs-docs` | Added recipe | [devario-libs/libtracefs](devario-libs/libtracefs/PKGBUILD) | — |
| `linux-tools-meta` | Added recipe | [devario-utilities/linux-tools](devario-utilities/linux-tools/PKGBUILD) | — |
| `maturin` | Updated | [devario-core/maturin](devario-core/maturin/PKGBUILD) | — |
| `ocaml-brltty` | Added recipe | [devario-utilities/brltty](devario-utilities/brltty/PKGBUILD) | — |
| `openh264` | Added recipe | [devario-libs/openh264](devario-libs/openh264/PKGBUILD) | — |
| `openvdb` | Added recipe | [devario-libs/openvdb](devario-libs/openvdb/PKGBUILD) | — |
| `perf` | Added recipe | [devario-utilities/linux-tools](devario-utilities/linux-tools/PKGBUILD) | — |
| `pybind11` | Added recipe | [devario-libs/pybind11](devario-libs/pybind11/PKGBUILD) | — |
| `python-brltty` | Added recipe | [devario-utilities/brltty](devario-utilities/brltty/PKGBUILD) | — |
| `python-cbor2` | Added recipe | [devario-libs/python-cbor2](devario-libs/python-cbor2/PKGBUILD) | — |
| `python-defcon` | Added recipe | [devario-libs/python-defcon](devario-libs/python-defcon/PKGBUILD) | — |
| `python-gevent` | Added recipe | [devario-libs/python-gevent](devario-libs/python-gevent/PKGBUILD) | — |
| `python-libcst` | Added recipe | [devario-libs/python-libcst](devario-libs/python-libcst/PKGBUILD) | — |
| `python-maturin` | Added split output | [devario-core/maturin](devario-core/maturin/PKGBUILD) | — |
| `python-pandas` | Added recipe | [devario-libs/python-pandas](devario-libs/python-pandas/PKGBUILD) | — |
| `python-pytest-playwright` | Added recipe | [devario-development/python-pytest-playwright](devario-development/python-pytest-playwright/PKGBUILD) | — |
| `python-pythran` | Added recipe | [devario-libs/python-pythran](devario-libs/python-pythran/PKGBUILD) | — |
| `python-sympy` | Added recipe | [devario-libs/python-sympy](devario-libs/python-sympy/PKGBUILD) | — |
| `subversion` | Added recipe | [devario-development/subversion](devario-development/subversion/PKGBUILD) | — |
| `tcl-brltty` | Added recipe | [devario-utilities/brltty](devario-utilities/brltty/PKGBUILD) | — |
| `tmon` | Added recipe | [devario-utilities/linux-tools](devario-utilities/linux-tools/PKGBUILD) | — |
| `towncrier` | Added recipe | [devario-development/towncrier](devario-development/towncrier/PKGBUILD) | — |
| `turbostat` | Added recipe | [devario-utilities/linux-tools](devario-utilities/linux-tools/PKGBUILD) | — |
| `usbip` | Added recipe | [devario-utilities/linux-tools](devario-utilities/linux-tools/PKGBUILD) | — |
| `x86_energy_perf_policy` | Added recipe | [devario-utilities/linux-tools](devario-utilities/linux-tools/PKGBUILD) | — |

## Stage 08

29 packages from 19 recipes.

| Package | Change in commit | Build recipe | Bootstrap / prerequisites |
| --- | --- | --- | --- |
| `aws-sdk-cpp` | Added recipe | [devario-libs/aws-sdk-cpp](devario-libs/aws-sdk-cpp/PKGBUILD) | — |
| `aws-sdk-cpp-core` | Added recipe | [devario-libs/aws-sdk-cpp](devario-libs/aws-sdk-cpp/PKGBUILD) | — |
| `aws-sdk-cpp-ec2` | Added recipe | [devario-libs/aws-sdk-cpp](devario-libs/aws-sdk-cpp/PKGBUILD) | — |
| `aws-sdk-cpp-firehose` | Added recipe | [devario-libs/aws-sdk-cpp](devario-libs/aws-sdk-cpp/PKGBUILD) | — |
| `aws-sdk-cpp-iam` | Added recipe | [devario-libs/aws-sdk-cpp](devario-libs/aws-sdk-cpp/PKGBUILD) | — |
| `aws-sdk-cpp-kinesis` | Added recipe | [devario-libs/aws-sdk-cpp](devario-libs/aws-sdk-cpp/PKGBUILD) | — |
| `aws-sdk-cpp-s3` | Added recipe | [devario-libs/aws-sdk-cpp](devario-libs/aws-sdk-cpp/PKGBUILD) | — |
| `cudnn-frontend` | Added recipe | [devario-libs/cudnn-frontend](devario-libs/cudnn-frontend/PKGBUILD) | — |
| `junit` | Added recipe | [devario-libs/junit](devario-libs/junit/PKGBUILD) | — |
| `lib32-libsndfile` | Added recipe | [devario-libs/lib32-libsndfile](devario-libs/lib32-libsndfile/PKGBUILD) | — |
| `libheif` | Added recipe | [devario-libs/libheif](devario-libs/libheif/PKGBUILD) | — |
| `libxdp` | Added recipe | [devario-utilities/xdp-tools](devario-utilities/xdp-tools/PKGBUILD) | — |
| `ndctl` | Added recipe | [devario-libs/ndctl](devario-libs/ndctl/PKGBUILD) | — |
| `netpbm` | Added recipe | [devario-utilities/netpbm](devario-utilities/netpbm/PKGBUILD) | — |
| `opencode` | Added recipe | [devario-development/opencode](devario-development/opencode/PKGBUILD) | — |
| `openvkl` | Added recipe | [devario-libs/openvkl](devario-libs/openvkl/PKGBUILD) | — |
| `powertop` | Added recipe | [devario-utilities/powertop](devario-utilities/powertop/PKGBUILD) | — |
| `python-ast-serialize` | Added recipe | [devario-libs/python-ast-serialize](devario-libs/python-ast-serialize/PKGBUILD) | — |
| `python-contourpy` | Added recipe | [devario-libs/python-contourpy](devario-libs/python-contourpy/PKGBUILD) | — |
| `python-cryptography` | Added recipe | [devario-libs/python-cryptography](devario-libs/python-cryptography/PKGBUILD) | — |
| `python-cudnn-frontend` | Added recipe | [devario-libs/cudnn-frontend](devario-libs/cudnn-frontend/PKGBUILD) | — |
| `python-mutatormath` | Added recipe | [devario-libs/python-mutatormath](devario-libs/python-mutatormath/PKGBUILD) | — |
| `python-orjson` | Added recipe | [devario-libs/python-orjson](devario-libs/python-orjson/PKGBUILD) | — |
| `python-uv` | Added recipe | [devario-development/uv](devario-development/uv/PKGBUILD) | — |
| `python-uv-build` | Added recipe | [devario-development/uv](devario-development/uv/PKGBUILD) | — |
| `qt6-webengine` | Added recipe | [devario-libs/qt6-webengine](devario-libs/qt6-webengine/PKGBUILD) | — |
| `sdl2_image` | Added recipe | [devario-libs/sdl2_image](devario-libs/sdl2_image/PKGBUILD) | — |
| `uv` | Added recipe | [devario-development/uv](devario-development/uv/PKGBUILD) | — |
| `xdp-tools` | Added recipe | [devario-utilities/xdp-tools](devario-utilities/xdp-tools/PKGBUILD) | — |

## Stage 09

11 packages from 9 recipes.

| Package | Change in commit | Build recipe | Bootstrap / prerequisites |
| --- | --- | --- | --- |
| `ant` | Added recipe | [devario-development/ant](devario-development/ant/PKGBUILD) | — |
| `ant-doc` | Added recipe | [devario-development/ant](devario-development/ant/PKGBUILD) | — |
| `fig2dev` | Added recipe | [devario-development/fig2dev](devario-development/fig2dev/PKGBUILD) | — |
| `gd` | Added recipe | [devario-libs/gd](devario-libs/gd/PKGBUILD) | — |
| `hspell` | Added recipe | [devario-development/hspell](devario-development/hspell/PKGBUILD) | — |
| `hunspell-he` | Added recipe | [devario-development/hspell](devario-development/hspell/PKGBUILD) | — |
| `imlib2` | Added recipe | [devario-libs/imlib2](devario-libs/imlib2/PKGBUILD) | — |
| `lib32-libsamplerate` | Added recipe | [devario-libs/lib32-libsamplerate](devario-libs/lib32-libsamplerate/PKGBUILD) | — |
| `mypy` | Added recipe | [devario-development/mypy](devario-development/mypy/PKGBUILD) | — |
| `ospray` | Added recipe | [devario-development/ospray](devario-development/ospray/PKGBUILD) | — |
| `qt6-webview` | Added recipe | [devario-libs/qt6-webview](devario-libs/qt6-webview/PKGBUILD) | — |

## Stage 10

40 packages from 7 recipes.

| Package | Change in commit | Build recipe | Bootstrap / prerequisites |
| --- | --- | --- | --- |
| `libcaca` | Added recipe | [devario-libs/libcaca](devario-libs/libcaca/PKGBUILD) | — |
| `libgphoto2` | Added recipe | [devario-libs/libgphoto2](devario-libs/libgphoto2/PKGBUILD) | — |
| `libgphoto2-docs` | Added recipe | [devario-libs/libgphoto2](devario-libs/libgphoto2/PKGBUILD) | — |
| `libsynctex` | Added recipe | [devario-utilities/texlive-bin](devario-utilities/texlive-bin/PKGBUILD) | — |
| `php` | Added recipe | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `php-apache` | Added recipe | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `php-cgi` | Added recipe | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `php-dblib` | Added recipe | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `php-embed` | Added recipe | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `php-enchant` | Added recipe | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `php-fpm` | Added recipe | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `php-gd` | Added recipe | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `php-legacy` | Added recipe | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-apache` | Added recipe | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-cgi` | Added recipe | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-dblib` | Added recipe | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-embed` | Added recipe | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-enchant` | Added recipe | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-fpm` | Added recipe | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-gd` | Added recipe | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-odbc` | Added recipe | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-pgsql` | Added recipe | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-phpdbg` | Added recipe | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-pspell` | Added recipe | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-snmp` | Added recipe | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-sodium` | Added recipe | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-sqlite` | Added recipe | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-tidy` | Added recipe | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-xsl` | Added recipe | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-odbc` | Added recipe | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `php-pgsql` | Added recipe | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `php-phpdbg` | Added recipe | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `php-snmp` | Added recipe | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `php-sodium` | Added recipe | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `php-sqlite` | Added recipe | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `php-tidy` | Added recipe | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `php-xsl` | Added recipe | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `python-charset-normalizer` | Added recipe | [devario-libs/python-charset-normalizer](devario-libs/python-charset-normalizer/PKGBUILD) | — |
| `sonnet` | Added recipe | [devario-libs/sonnet](devario-libs/sonnet/PKGBUILD) | — |
| `texlive-bin` | Added recipe | [devario-utilities/texlive-bin](devario-utilities/texlive-bin/PKGBUILD) | — |

## Stage 11

56 packages from 7 recipes.

| Package | Change in commit | Build recipe | Bootstrap / prerequisites |
| --- | --- | --- | --- |
| `check` | Added recipe | [devario-libs/check](devario-libs/check/PKGBUILD) | — |
| `check-docs` | Added recipe | [devario-libs/check](devario-libs/check/PKGBUILD) | — |
| `dvisvgm` | Added recipe | [devario-utilities/dvisvgm](devario-utilities/dvisvgm/PKGBUILD) | Cycle G101 — seed packages required |
| `grpc` | Added recipe | [devario-libs/grpc](devario-libs/grpc/PKGBUILD) | — |
| `grpc-cli` | Added recipe | [devario-libs/grpc](devario-libs/grpc/PKGBUILD) | — |
| `openai-codex` | Added recipe | [devario-development/openai-codex](devario-development/openai-codex/PKGBUILD) | — |
| `openai-codex-voice` | Added recipe | [devario-development/openai-codex](devario-development/openai-codex/PKGBUILD) | — |
| `php-grpc` | Added recipe | [devario-libs/grpc](devario-libs/grpc/PKGBUILD) | — |
| `php-legacy-grpc` | Added recipe | [devario-libs/grpc](devario-libs/grpc/PKGBUILD) | — |
| `python-grpcio` | Added recipe | [devario-libs/grpc](devario-libs/grpc/PKGBUILD) | — |
| `python-grpcio-tools` | Added recipe | [devario-libs/grpc](devario-libs/grpc/PKGBUILD) | — |
| `python-requests` | Added recipe | [devario-libs/python-requests](devario-libs/python-requests/PKGBUILD) | — |
| `qt6-multimedia` | Added recipe | [devario-libs/qt6-multimedia](devario-libs/qt6-multimedia/PKGBUILD) | — |
| `qt6-multimedia-ffmpeg` | Added recipe | [devario-libs/qt6-multimedia](devario-libs/qt6-multimedia/PKGBUILD) | — |
| `qt6-multimedia-gstreamer` | Added recipe | [devario-libs/qt6-multimedia](devario-libs/qt6-multimedia/PKGBUILD) | — |
| `texlive-basic` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-bibtexextra` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-binextra` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-context` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-doc` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-fontsextra` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-fontsrecommended` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-fontutils` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-formatsextra` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-games` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-humanities` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langarabic` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langchinese` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langcjk` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langcyrillic` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langczechslovak` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langenglish` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langeuropean` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langfrench` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langgerman` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langgreek` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langitalian` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langjapanese` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langkorean` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langother` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langpolish` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langportuguese` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langspanish` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-latex` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-latexextra` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-latexrecommended` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-luatex` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-mathscience` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-meta` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-metapost` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-music` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-pictures` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-plaingeneric` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-pstricks` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-publishers` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-xetex` | Added recipe | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |

## Stage 12

22 packages from 22 recipes.

| Package | Change in commit | Build recipe | Bootstrap / prerequisites |
| --- | --- | --- | --- |
| `arrow` | Added recipe | [devario-libs/arrow](devario-libs/arrow/PKGBUILD) | — |
| `bind` | Added recipe | [devario-utilities/bind](devario-utilities/bind/PKGBUILD) | — |
| `contour` | Added recipe | [devario-utilities/contour](devario-utilities/contour/PKGBUILD) | — |
| `dblatex` | Added recipe | [devario-development/dblatex](devario-development/dblatex/PKGBUILD) | — |
| `define` | Added recipe | [devario-productivity/define](devario-productivity/define/PKGBUILD) | — |
| `electron43` | Added recipe | [devario-libs/electron43](devario-libs/electron43/PKGBUILD) | — |
| `fontforge` | Added recipe | [devario-libs/fontforge](devario-libs/fontforge/PKGBUILD) | — |
| `gl2ps` | Added recipe | [devario-libs/gl2ps](devario-libs/gl2ps/PKGBUILD) | — |
| `python-distro` | Added recipe | [devario-libs/python-distro](devario-libs/python-distro/PKGBUILD) | — |
| `python-pooch` | Added recipe | [devario-libs/python-pooch](devario-libs/python-pooch/PKGBUILD) | — |
| `python-pyudev` | Added recipe | [devario-libs/python-pyudev](devario-libs/python-pyudev/PKGBUILD) | — |
| `python-sphinx-argparse` | Added recipe | [devario-development/python-sphinx-argparse](devario-development/python-sphinx-argparse/PKGBUILD) | — |
| `python-sphinx-autodoc-typehints` | Added recipe | [devario-development/python-sphinx-autodoc-typehints](devario-development/python-sphinx-autodoc-typehints/PKGBUILD) | — |
| `python-sphinx-basic-ng` | Added recipe | [devario-development/python-sphinx-basic-ng](devario-development/python-sphinx-basic-ng/PKGBUILD) | — |
| `python-sphinx-copybutton` | Added recipe | [devario-development/python-sphinx-copybutton](devario-development/python-sphinx-copybutton/PKGBUILD) | — |
| `python-sphinx-inline-tabs` | Added recipe | [devario-development/python-sphinx-inline-tabs](devario-development/python-sphinx-inline-tabs/PKGBUILD) | — |
| `python-sphinx-issues` | Added recipe | [devario-development/python-sphinx-issues](devario-development/python-sphinx-issues/PKGBUILD) | — |
| `python-sphinxcontrib-jquery` | Added recipe | [devario-development/python-sphinxcontrib-jquery](devario-development/python-sphinxcontrib-jquery/PKGBUILD) | — |
| `python-sphinxcontrib-mermaid` | Added recipe | [devario-development/python-sphinxcontrib-mermaid](devario-development/python-sphinxcontrib-mermaid/PKGBUILD) | — |
| `python-sphinxcontrib-towncrier` | Added recipe | [devario-development/python-sphinxcontrib-towncrier](devario-development/python-sphinxcontrib-towncrier/PKGBUILD) | — |
| `qt6-speech` | Added recipe | [devario-libs/qt6-speech](devario-libs/qt6-speech/PKGBUILD) | — |
| `virglrenderer` | Added recipe | [devario-libs/virglrenderer](devario-libs/virglrenderer/PKGBUILD) | — |

## Stage 13

16 packages from 13 recipes.

| Package | Change in commit | Build recipe | Bootstrap / prerequisites |
| --- | --- | --- | --- |
| `podman-desktop` | Added recipe | [devario-development/podman-desktop](devario-development/podman-desktop/PKGBUILD) | — |
| `pyside6` | Added recipe | [devario-libs/pyside6](devario-libs/pyside6/PKGBUILD) | — |
| `pyside6-tools` | Added recipe | [devario-libs/pyside6](devario-libs/pyside6/PKGBUILD) | — |
| `python-pip` | Added recipe | [devario-libs/python-pip](devario-libs/python-pip/PKGBUILD) | — |
| `python-pyarrow` | Added recipe | [devario-libs/python-pyarrow](devario-libs/python-pyarrow/PKGBUILD) | — |
| `python-scipy` | Added recipe | [devario-libs/python-scipy](devario-libs/python-scipy/PKGBUILD) | — |
| `python-sphinx-furo` | Added recipe | [devario-development/python-sphinx-furo](devario-development/python-sphinx-furo/PKGBUILD) | — |
| `python-sphinx_rtd_theme` | Added recipe | [devario-development/python-sphinx_rtd_theme](devario-development/python-sphinx_rtd_theme/PKGBUILD) | — |
| `python-userpath` | Added recipe | [devario-libs/python-userpath](devario-libs/python-userpath/PKGBUILD) | — |
| `python-virtualenv` | Added recipe | [devario-libs/python-virtualenv](devario-libs/python-virtualenv/PKGBUILD) | — |
| `ragel` | Added recipe | [devario-development/ragel](devario-development/ragel/PKGBUILD) | — |
| `rutabaga-ffi` | Added recipe | [devario-libs/rutabaga-ffi](devario-libs/rutabaga-ffi/PKGBUILD) | — |
| `shiboken6` | Added recipe | [devario-libs/pyside6](devario-libs/pyside6/PKGBUILD) | — |
| `shiboken6-generator` | Added recipe | [devario-libs/pyside6](devario-libs/pyside6/PKGBUILD) | — |
| `solaar` | Added recipe | [devario-utilities/solaar](devario-utilities/solaar/PKGBUILD) | — |
| `ttf-liberation` | Added recipe | [devario-libs/ttf-liberation](devario-libs/ttf-liberation/PKGBUILD) | — |

## Stage 14

7 packages from 6 recipes.

| Package | Change in commit | Build recipe | Bootstrap / prerequisites |
| --- | --- | --- | --- |
| `blueprint-compiler` | Added recipe | [devario-development/blueprint-compiler](devario-development/blueprint-compiler/PKGBUILD) | — |
| `chromium` | Added recipe | [devario-browser/chromium](devario-browser/chromium/PKGBUILD) | — |
| `kguiaddons` | Added recipe | [devario-libs/kguiaddons](devario-libs/kguiaddons/PKGBUILD) | — |
| `python-lxml` | Added recipe | [devario-libs/python-lxml](devario-libs/python-lxml/PKGBUILD) | — |
| `python-lxml-docs` | Added recipe | [devario-libs/python-lxml](devario-libs/python-lxml/PKGBUILD) | — |
| `python-pipx` | Added recipe | [devario-development/python-pipx](devario-development/python-pipx/PKGBUILD) | — |
| `rocblas` | Added recipe | [devario-libs/rocblas](devario-libs/rocblas/PKGBUILD) | — |

## Stage 15

7 packages from 7 recipes.

| Package | Change in commit | Build recipe | Bootstrap / prerequisites |
| --- | --- | --- | --- |
| `breeze-icons` | Added recipe | [devario-libs/breeze-icons](devario-libs/breeze-icons/PKGBUILD) | — |
| `kcolorscheme` | Added recipe | [devario-libs/kcolorscheme](devario-libs/kcolorscheme/PKGBUILD) | — |
| `lib32-vulkan-icd-loader` | Added recipe | [devario-libs/lib32-vulkan-icd-loader](devario-libs/lib32-vulkan-icd-loader/PKGBUILD) | — |
| `python-fontparts` | Added recipe | [devario-libs/python-fontparts](devario-libs/python-fontparts/PKGBUILD) | — |
| `python-steam` | Added recipe | [devario-libs/python-steam](devario-libs/python-steam/PKGBUILD) | — |
| `rocsparse` | Added recipe | [devario-libs/rocsparse](devario-libs/rocsparse/PKGBUILD) | — |
| `yelp-tools` | Added recipe | [devario-development/yelp-tools](devario-development/yelp-tools/PKGBUILD) | — |

## Stage 16

9 packages from 9 recipes.

| Package | Change in commit | Build recipe | Bootstrap / prerequisites |
| --- | --- | --- | --- |
| `gtk-doc` | Added recipe | [devario-libs/gtk-doc](devario-libs/gtk-doc/PKGBUILD) | — |
| `hipsparse` | Added recipe | [devario-libs/hipsparse](devario-libs/hipsparse/PKGBUILD) | — |
| `kconfigwidgets` | Added recipe | [devario-libs/kconfigwidgets](devario-libs/kconfigwidgets/PKGBUILD) | — |
| `kiconthemes` | Added recipe | [devario-libs/kiconthemes](devario-libs/kiconthemes/PKGBUILD) | — |
| `ksvg` | Added recipe | [devario-libs/ksvg](devario-libs/ksvg/PKGBUILD) | — |
| `protonup-qt` | Added recipe | [devario-gaming/protonup-qt](devario-gaming/protonup-qt/PKGBUILD) | — |
| `python-ufoprocessor` | Added recipe | [devario-libs/python-ufoprocessor](devario-libs/python-ufoprocessor/PKGBUILD) | — |
| `rocsolver` | Added recipe | [devario-libs/rocsolver](devario-libs/rocsolver/PKGBUILD) | — |
| `zenity` | Added recipe | [devario-utilities/zenity](devario-utilities/zenity/PKGBUILD) | — |

## Stage 17

26 packages from 19 recipes.

| Package | Change in commit | Build recipe | Bootstrap / prerequisites |
| --- | --- | --- | --- |
| `afdko` | Added recipe | [devario-libs/afdko](devario-libs/afdko/PKGBUILD) | — |
| `dbus-glib` | Added recipe | [devario-libs/dbus-glib](devario-libs/dbus-glib/PKGBUILD) | — |
| `gnome-desktop` | Added recipe | [devario-libs/gnome-desktop](devario-libs/gnome-desktop/PKGBUILD) | — |
| `gnome-desktop-4` | Added recipe | [devario-libs/gnome-desktop](devario-libs/gnome-desktop/PKGBUILD) | — |
| `gnome-desktop-common` | Added recipe | [devario-libs/gnome-desktop](devario-libs/gnome-desktop/PKGBUILD) | — |
| `gnome-desktop-docs` | Added recipe | [devario-libs/gnome-desktop](devario-libs/gnome-desktop/PKGBUILD) | — |
| `hipblas` | Added recipe | [devario-libs/hipblas](devario-libs/hipblas/PKGBUILD) | — |
| `hipsolver` | Added recipe | [devario-libs/hipsolver](devario-libs/hipsolver/PKGBUILD) | — |
| `kirigami-addons` | Added recipe | [devario-libs/kirigami-addons](devario-libs/kirigami-addons/PKGBUILD) | — |
| `lib32-libidn2` | Added recipe | [devario-libs/lib32-libidn2](devario-libs/lib32-libidn2/PKGBUILD) | — |
| `libcanberra` | Added recipe | [devario-libs/libcanberra](devario-libs/libcanberra/PKGBUILD) | — |
| `libgsf` | Added recipe | [devario-libs/libgsf](devario-libs/libgsf/PKGBUILD) | — |
| `libgsf-docs` | Added recipe | [devario-libs/libgsf](devario-libs/libgsf/PKGBUILD) | — |
| `libgxps` | Added recipe | [devario-libs/libgxps](devario-libs/libgxps/PKGBUILD) | — |
| `libiptcdata` | Added recipe | [devario-libs/libiptcdata](devario-libs/libiptcdata/PKGBUILD) | — |
| `libraqm` | Added recipe | [devario-libs/libraqm](devario-libs/libraqm/PKGBUILD) | — |
| `phodav` | Added recipe | [devario-libs/phodav](devario-libs/phodav/PKGBUILD) | — |
| `poppler` | Added recipe | [devario-libs/poppler](devario-libs/poppler/PKGBUILD) | — |
| `poppler-glib` | Added recipe | [devario-libs/poppler](devario-libs/poppler/PKGBUILD) | — |
| `poppler-qt5` | Added recipe | [devario-libs/poppler](devario-libs/poppler/PKGBUILD) | — |
| `poppler-qt6` | Added recipe | [devario-libs/poppler](devario-libs/poppler/PKGBUILD) | — |
| `qqc2-desktop-style` | Added recipe | [devario-libs/qqc2-desktop-style](devario-libs/qqc2-desktop-style/PKGBUILD) | — |
| `raptor` | Added recipe | [devario-libs/raptor](devario-libs/raptor/PKGBUILD) | — |
| `rocalution` | Added recipe | [devario-libs/rocalution](devario-libs/rocalution/PKGBUILD) | — |
| `totem-pl-parser` | Added recipe | [devario-libs/totem-pl-parser](devario-libs/totem-pl-parser/PKGBUILD) | — |
| `vala` | Added recipe | [devario-development/vala](devario-development/vala/PKGBUILD) | Seed: `vala` |

## Stage 18

50 packages from 25 recipes.

| Package | Change in commit | Build recipe | Bootstrap / prerequisites |
| --- | --- | --- | --- |
| `easyeffects` | Added recipe | [devario-entertainment/easyeffects](devario-entertainment/easyeffects/PKGBUILD) | — |
| `gdal` | Added recipe | [devario-libs/gdal](devario-libs/gdal/PKGBUILD) | — |
| `gexiv2` | Added recipe | [devario-libs/gexiv2](devario-libs/gexiv2/PKGBUILD) | — |
| `gexiv2-common` | Added recipe | [devario-libs/gexiv2](devario-libs/gexiv2/PKGBUILD) | — |
| `gexiv2-docs` | Added recipe | [devario-libs/gexiv2](devario-libs/gexiv2/PKGBUILD) | — |
| `gnome-autoar` | Added recipe | [devario-libs/gnome-autoar](devario-libs/gnome-autoar/PKGBUILD) | — |
| `gnome-autoar-docs` | Added recipe | [devario-libs/gnome-autoar](devario-libs/gnome-autoar/PKGBUILD) | — |
| `gtk-vnc` | Added recipe | [devario-libs/gtk-vnc](devario-libs/gtk-vnc/PKGBUILD) | — |
| `gtk-vnc-docs` | Added recipe | [devario-libs/gtk-vnc](devario-libs/gtk-vnc/PKGBUILD) | — |
| `gupnp-dlna` | Added recipe | [devario-libs/gupnp-dlna](devario-libs/gupnp-dlna/PKGBUILD) | — |
| `gvim` | Added recipe | [devario-development/vim](devario-development/vim/PKGBUILD) | — |
| `hipblaslt` | Added recipe | [devario-libs/hipblaslt](devario-libs/hipblaslt/PKGBUILD) | — |
| `ibus` | Added recipe | [devario-utilities/ibus](devario-utilities/ibus/PKGBUILD) | — |
| `imagemagick` | Added recipe | [devario-entertainment/imagemagick](devario-entertainment/imagemagick/PKGBUILD) | — |
| `lib32-gnutls` | Added recipe | [devario-libs/lib32-gnutls](devario-libs/lib32-gnutls/PKGBUILD) | — |
| `lib32-libpsl` | Added recipe | [devario-libs/lib32-libpsl](devario-libs/lib32-libpsl/PKGBUILD) | — |
| `libappindicator` | Added recipe | [devario-core/libappindicator](devario-core/libappindicator/PKGBUILD) | — |
| `libibus` | Added recipe | [devario-utilities/ibus](devario-utilities/ibus/PKGBUILD) | — |
| `liblrdf` | Added recipe | [devario-libs/liblrdf](devario-libs/liblrdf/PKGBUILD) | — |
| `libmanette` | Added recipe | [devario-libs/libmanette](devario-libs/libmanette/PKGBUILD) | — |
| `libmanette-docs` | Added recipe | [devario-libs/libmanette](devario-libs/libmanette/PKGBUILD) | — |
| `libnma` | Added recipe | [devario-core/libnma](devario-core/libnma/PKGBUILD) | — |
| `libnma-common` | Added recipe | [devario-core/libnma](devario-core/libnma/PKGBUILD) | — |
| `libnma-gtk4` | Added recipe | [devario-core/libnma](devario-core/libnma/PKGBUILD) | — |
| `libosinfo` | Added recipe | [devario-libs/libosinfo](devario-libs/libosinfo/PKGBUILD) | — |
| `libportal` | Added recipe | [devario-libs/libportal](devario-libs/libportal/PKGBUILD) | — |
| `libportal-docs` | Added recipe | [devario-libs/libportal](devario-libs/libportal/PKGBUILD) | — |
| `libportal-gtk3` | Added recipe | [devario-libs/libportal](devario-libs/libportal/PKGBUILD) | — |
| `libportal-gtk4` | Added recipe | [devario-libs/libportal](devario-libs/libportal/PKGBUILD) | — |
| `libportal-qt5` | Added recipe | [devario-libs/libportal](devario-libs/libportal/PKGBUILD) | — |
| `libportal-qt6` | Added recipe | [devario-libs/libportal](devario-libs/libportal/PKGBUILD) | — |
| `libvirt-glib` | Added recipe | [devario-libs/libvirt-glib](devario-libs/libvirt-glib/PKGBUILD) | — |
| `ollama` | Added recipe | [devario-development/ollama](devario-development/ollama/PKGBUILD) | — |
| `ollama-cuda` | Added recipe | [devario-development/ollama](devario-development/ollama/PKGBUILD) | — |
| `ollama-docs` | Added recipe | [devario-development/ollama](devario-development/ollama/PKGBUILD) | — |
| `ollama-rocm` | Added recipe | [devario-development/ollama](devario-development/ollama/PKGBUILD) | — |
| `ollama-vulkan` | Added recipe | [devario-development/ollama](devario-development/ollama/PKGBUILD) | — |
| `pavucontrol` | Added recipe | [devario-utilities/pavucontrol](devario-utilities/pavucontrol/PKGBUILD) | — |
| `python-gdal` | Added recipe | [devario-libs/gdal](devario-libs/gdal/PKGBUILD) | — |
| `python-pillow` | Added recipe | [devario-libs/python-pillow](devario-libs/python-pillow/PKGBUILD) | — |
| `sane` | Added recipe | [devario-development/sane](devario-development/sane/PKGBUILD) | — |
| `spice-gtk` | Added recipe | [devario-libs/spice-gtk](devario-libs/spice-gtk/PKGBUILD) | — |
| `vim` | Added recipe | [devario-development/vim](devario-development/vim/PKGBUILD) | — |
| `vim-runtime` | Added recipe | [devario-development/vim](devario-development/vim/PKGBUILD) | — |
| `vte-common` | Added recipe | [devario-libs/vte3](devario-libs/vte3/PKGBUILD) | — |
| `vte-docs` | Added recipe | [devario-libs/vte3](devario-libs/vte3/PKGBUILD) | — |
| `vte3` | Added recipe | [devario-libs/vte3](devario-libs/vte3/PKGBUILD) | — |
| `vte3-utils` | Added recipe | [devario-libs/vte3](devario-libs/vte3/PKGBUILD) | — |
| `vte4` | Added recipe | [devario-libs/vte3](devario-libs/vte3/PKGBUILD) | — |
| `vte4-utils` | Added recipe | [devario-libs/vte3](devario-libs/vte3/PKGBUILD) | — |

## Stage 19

98 packages from 13 recipes.

| Package | Change in commit | Build recipe | Bootstrap / prerequisites |
| --- | --- | --- | --- |
| `lib32-libngtcp2` | Added recipe | [devario-libs/lib32-libngtcp2](devario-libs/lib32-libngtcp2/PKGBUILD) | — |
| `liblas` | Added recipe | [devario-libs/liblas](devario-libs/liblas/PKGBUILD) | — |
| `localsearch` | Added recipe | [devario-utilities/localsearch](devario-utilities/localsearch/PKGBUILD) | — |
| `localsearch-testutils` | Added recipe | [devario-utilities/localsearch](devario-utilities/localsearch/PKGBUILD) | — |
| `miopen-hip` | Added recipe | [devario-libs/miopen-hip](devario-libs/miopen-hip/PKGBUILD) | — |
| `network-manager-applet` | Added recipe | [devario-core/network-manager-applet](devario-core/network-manager-applet/PKGBUILD) | — |
| `nm-connection-editor` | Added recipe | [devario-core/network-manager-applet](devario-core/network-manager-applet/PKGBUILD) | — |
| `pdal` | Added recipe | [devario-libs/pdal](devario-libs/pdal/PKGBUILD) | — |
| `proton-cachyos-native` | Added recipe | [devario-gaming/proton-cachyos-native](devario-gaming/proton-cachyos-native/PKGBUILD) | — |
| `python-matplotlib` | Added recipe | [devario-libs/python-matplotlib](devario-libs/python-matplotlib/PKGBUILD) | — |
| `python-pywal` | Added recipe | [devario-development/python-pywal](devario-development/python-pywal/PKGBUILD) | — |
| `qemu-audio-alsa` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-audio-dbus` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-audio-jack` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-audio-oss` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-audio-pa` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-audio-pipewire` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-audio-sdl` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-audio-spice` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-base` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-block-curl` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-block-dmg` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-block-iscsi` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-block-nfs` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-block-ssh` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-chardev-baum` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-chardev-spice` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-common` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-desktop` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-docs` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-emulators-full` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-full` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-guest-agent` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-hw-display-qxl` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-hw-display-virtio-gpu` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-hw-display-virtio-gpu-gl` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-hw-display-virtio-gpu-pci` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-hw-display-virtio-gpu-pci-gl` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-hw-display-virtio-gpu-pci-rutabaga` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-hw-display-virtio-gpu-rutabaga` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-hw-display-virtio-vga` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-hw-display-virtio-vga-gl` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-hw-display-virtio-vga-rutabaga` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-hw-s390x-virtio-gpu-ccw` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-hw-uefi-vars` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-hw-usb-host` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-hw-usb-redirect` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-hw-usb-smartcard` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-img` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-pr-helper` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-aarch64` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-alpha` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-alpha-firmware` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-arm` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-arm-firmware` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-avr` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-hexagon` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-hppa` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-hppa-firmware` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-loongarch64` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-m68k` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-microblaze` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-microblaze-firmware` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-mips` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-or1k` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-ppc` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-ppc-firmware` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-riscv` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-riscv-firmware` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-rx` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-s390x` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-s390x-firmware` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-sh4` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-sparc` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-sparc-firmware` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-tricore` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-x86` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-x86-firmware` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-xtensa` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-tests` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-tools` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-ui-curses` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-ui-dbus` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-ui-egl-headless` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-ui-gtk` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-ui-opengl` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-ui-sdl` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-ui-spice-app` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-ui-spice-core` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-user` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-user-binfmt` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-user-static` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-user-static-binfmt` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-vhost-user-gpu` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-vmsr-helper` | Added recipe | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `wine` | Added recipe | [devario-gaming/wine](devario-gaming/wine/PKGBUILD) | — |
| `wine-cachyos-opt` | Added recipe | [devario-gaming/wine-cachyos-opt](devario-gaming/wine-cachyos-opt/PKGBUILD) | — |
| `zbar` | Added recipe | [devario-libs/zbar](devario-libs/zbar/PKGBUILD) | — |

## Stage 20

16 packages from 6 recipes.

| Package | Change in commit | Build recipe | Bootstrap / prerequisites |
| --- | --- | --- | --- |
| `goverlay` | Added recipe | [devario-gaming/goverlay](devario-gaming/goverlay/PKGBUILD) | — |
| `lib32-curl` | Added recipe | [devario-libs/lib32-curl](devario-libs/lib32-curl/PKGBUILD) | — |
| `lib32-libcurl-compat` | Added recipe | [devario-libs/lib32-curl](devario-libs/lib32-curl/PKGBUILD) | — |
| `lib32-libcurl-gnutls` | Added recipe | [devario-libs/lib32-curl](devario-libs/lib32-curl/PKGBUILD) | — |
| `libnautilus-extension` | Added recipe | [devario-utilities/nautilus](devario-utilities/nautilus/PKGBUILD) | — |
| `libnautilus-extension-docs` | Added recipe | [devario-utilities/nautilus](devario-utilities/nautilus/PKGBUILD) | — |
| `migraphx` | Added recipe | [devario-libs/migraphx](devario-libs/migraphx/PKGBUILD) | — |
| `nautilus` | Added recipe | [devario-utilities/nautilus](devario-utilities/nautilus/PKGBUILD) | — |
| `rocm-hip-libraries` | Added recipe | [devario-development/rocm-hip-sdk](devario-development/rocm-hip-sdk/PKGBUILD) | — |
| `rocm-hip-runtime` | Added recipe | [devario-development/rocm-hip-sdk](devario-development/rocm-hip-sdk/PKGBUILD) | — |
| `rocm-hip-sdk` | Added recipe | [devario-development/rocm-hip-sdk](devario-development/rocm-hip-sdk/PKGBUILD) | — |
| `rocm-language-runtime` | Added recipe | [devario-development/rocm-hip-sdk](devario-development/rocm-hip-sdk/PKGBUILD) | — |
| `rocm-ml-libraries` | Added recipe | [devario-development/rocm-hip-sdk](devario-development/rocm-hip-sdk/PKGBUILD) | — |
| `rocm-ml-sdk` | Added recipe | [devario-development/rocm-hip-sdk](devario-development/rocm-hip-sdk/PKGBUILD) | — |
| `rocm-opencl-sdk` | Added recipe | [devario-development/rocm-hip-sdk](devario-development/rocm-hip-sdk/PKGBUILD) | — |
| `winetricks` | Added recipe | [devario-gaming/winetricks](devario-gaming/winetricks/PKGBUILD) | — |

## Stage 21

13 packages from 4 recipes.

| Package | Change in commit | Build recipe | Bootstrap / prerequisites |
| --- | --- | --- | --- |
| `file-roller` | Added recipe | [devario-utilities/file-roller](devario-utilities/file-roller/PKGBUILD) | — |
| `lib32-libelf` | Added recipe | [devario-libs/lib32-libelf](devario-libs/lib32-libelf/PKGBUILD) | — |
| `onnxruntime-cpu` | Added recipe | [devario-development/onnxruntime](devario-development/onnxruntime/PKGBUILD) | — |
| `onnxruntime-cuda` | Added recipe | [devario-development/onnxruntime](devario-development/onnxruntime/PKGBUILD) | — |
| `onnxruntime-opt-cuda` | Added recipe | [devario-development/onnxruntime](devario-development/onnxruntime/PKGBUILD) | — |
| `onnxruntime-opt-rocm` | Added recipe | [devario-development/onnxruntime](devario-development/onnxruntime/PKGBUILD) | — |
| `onnxruntime-rocm` | Added recipe | [devario-development/onnxruntime](devario-development/onnxruntime/PKGBUILD) | — |
| `protontricks` | Added recipe | [devario-gaming/protontricks](devario-gaming/protontricks/PKGBUILD) | — |
| `python-onnxruntime-cpu` | Added recipe | [devario-development/onnxruntime](devario-development/onnxruntime/PKGBUILD) | — |
| `python-onnxruntime-cuda` | Added recipe | [devario-development/onnxruntime](devario-development/onnxruntime/PKGBUILD) | — |
| `python-onnxruntime-opt-cuda` | Added recipe | [devario-development/onnxruntime](devario-development/onnxruntime/PKGBUILD) | — |
| `python-onnxruntime-opt-rocm` | Added recipe | [devario-development/onnxruntime](devario-development/onnxruntime/PKGBUILD) | — |
| `python-onnxruntime-rocm` | Added recipe | [devario-development/onnxruntime](devario-development/onnxruntime/PKGBUILD) | — |

## Stage 22

5 packages from 5 recipes.

| Package | Change in commit | Build recipe | Bootstrap / prerequisites |
| --- | --- | --- | --- |
| `lib32-dbus` | Added recipe | [devario-libs/lib32-dbus](devario-libs/lib32-dbus/PKGBUILD) | Cycle G688 — seed packages required |
| `lib32-glib2` | Added recipe | [devario-libs/lib32-glib2](devario-libs/lib32-glib2/PKGBUILD) | Cycle G688 — seed packages required |
| `lib32-systemd` | Added recipe | [devario-libs/lib32-systemd](devario-libs/lib32-systemd/PKGBUILD) | Cycle G688 — seed packages required |
| `opencascade` | Added recipe | [devario-development/opencascade](devario-development/opencascade/PKGBUILD) | Cycle G364 — seed packages required |
| `vtk` | Added recipe | [devario-libs/vtk](devario-libs/vtk/PKGBUILD) | Cycle G364 — seed packages required |

## Stage 23

36 packages from 11 recipes.

| Package | Change in commit | Build recipe | Bootstrap / prerequisites |
| --- | --- | --- | --- |
| `lib32-cairo` | Added recipe | [devario-libs/lib32-cairo](devario-libs/lib32-cairo/PKGBUILD) | Cycle G714 — seed packages required |
| `lib32-fontconfig` | Added recipe | [devario-libs/lib32-fontconfig](devario-libs/lib32-fontconfig/PKGBUILD) | Cycle G714 — seed packages required |
| `lib32-freetype2` | Added recipe | [devario-libs/lib32-freetype2](devario-libs/lib32-freetype2/PKGBUILD) | Cycle G714 — seed packages required |
| `lib32-harfbuzz` | Added recipe | [devario-libs/lib32-harfbuzz](devario-libs/lib32-harfbuzz/PKGBUILD) | Cycle G714 — seed packages required |
| `lib32-harfbuzz-cairo` | Added recipe | [devario-libs/lib32-harfbuzz](devario-libs/lib32-harfbuzz/PKGBUILD) | Cycle G714 — seed packages required |
| `lib32-harfbuzz-icu` | Added recipe | [devario-libs/lib32-harfbuzz](devario-libs/lib32-harfbuzz/PKGBUILD) | Cycle G714 — seed packages required |
| `lib32-libglvnd` | Added recipe | [devario-libs/lib32-libglvnd](devario-libs/lib32-libglvnd/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-libnm` | Added recipe | [devario-libs/lib32-libnm](devario-libs/lib32-libnm/PKGBUILD) | — |
| `lib32-libpipewire` | Added recipe | [devario-libs/lib32-pipewire](devario-libs/lib32-pipewire/PKGBUILD) | — |
| `lib32-libpulse` | Added recipe | [devario-libs/lib32-libpulse](devario-libs/lib32-libpulse/PKGBUILD) | — |
| `lib32-libva` | Added recipe | [devario-libs/lib32-libva](devario-libs/lib32-libva/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-mesa` | Added recipe | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-opencl-mesa` | Added recipe | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-pipewire` | Added recipe | [devario-libs/lib32-pipewire](devario-libs/lib32-pipewire/PKGBUILD) | — |
| `lib32-pipewire-jack` | Added recipe | [devario-libs/lib32-pipewire](devario-libs/lib32-pipewire/PKGBUILD) | — |
| `lib32-pipewire-netjack2` | Added recipe | [devario-libs/lib32-pipewire](devario-libs/lib32-pipewire/PKGBUILD) | — |
| `lib32-pipewire-v4l2` | Added recipe | [devario-libs/lib32-pipewire](devario-libs/lib32-pipewire/PKGBUILD) | — |
| `lib32-vulkan-asahi` | Added recipe | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-vulkan-broadcom` | Added recipe | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-vulkan-dzn` | Added recipe | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-vulkan-freedreno` | Added recipe | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-vulkan-gfxstream` | Added recipe | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-vulkan-intel` | Added recipe | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-vulkan-mesa-implicit-layers` | Added recipe | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-vulkan-mesa-layers` | Added recipe | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-vulkan-nouveau` | Added recipe | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-vulkan-panfrost` | Added recipe | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-vulkan-powervr` | Added recipe | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-vulkan-radeon` | Added recipe | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-vulkan-swrast` | Added recipe | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-vulkan-virtio` | Added recipe | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `opencv` | Added recipe | [devario-libs/opencv](devario-libs/opencv/PKGBUILD) | — |
| `opencv-cuda` | Added recipe | [devario-libs/opencv](devario-libs/opencv/PKGBUILD) | — |
| `opencv-samples` | Added recipe | [devario-libs/opencv](devario-libs/opencv/PKGBUILD) | — |
| `python-opencv` | Added recipe | [devario-libs/opencv](devario-libs/opencv/PKGBUILD) | — |
| `python-opencv-cuda` | Added recipe | [devario-libs/opencv](devario-libs/opencv/PKGBUILD) | — |

## Stage 24

2 packages from 2 recipes.

| Package | Change in commit | Build recipe | Bootstrap / prerequisites |
| --- | --- | --- | --- |
| `lib32-alsa-plugins` | Added recipe | [devario-libs/lib32-alsa-plugins](devario-libs/lib32-alsa-plugins/PKGBUILD) | — |
| `zxing-cpp` | Added recipe | [devario-libs/zxing-cpp](devario-libs/zxing-cpp/PKGBUILD) | — |

## Stage 25

6 packages from 4 recipes.

| Package | Change in commit | Build recipe | Bootstrap / prerequisites |
| --- | --- | --- | --- |
| `proton-cachyos-slr` | Added recipe | [devario-gaming/proton-cachyos-slr](devario-gaming/proton-cachyos-slr/PKGBUILD) | — |
| `umu-launcher` | Added recipe | [devario-gaming/umu-launcher](devario-gaming/umu-launcher/PKGBUILD) | — |
| `webkit2gtk-4.1` | Added recipe | [devario-development/webkit2gtk-4.1](devario-development/webkit2gtk-4.1/PKGBUILD) | — |
| `webkit2gtk-4.1-docs` | Added recipe | [devario-development/webkit2gtk-4.1](devario-development/webkit2gtk-4.1/PKGBUILD) | — |
| `webkitgtk-6.0` | Added recipe | [devario-libs/webkitgtk-6.0](devario-libs/webkitgtk-6.0/PKGBUILD) | — |
| `webkitgtk-6.0-docs` | Added recipe | [devario-libs/webkitgtk-6.0](devario-libs/webkitgtk-6.0/PKGBUILD) | — |

## Stage 26

2 packages from 2 recipes.

| Package | Change in commit | Build recipe | Bootstrap / prerequisites |
| --- | --- | --- | --- |
| `font-manager` | Added recipe | [devario-utilities/font-manager](devario-utilities/font-manager/PKGBUILD) | — |
| `glade` | Added recipe | [devario-development/glade](devario-development/glade/PKGBUILD) | — |

## Stage 27

3 packages from 2 recipes.

| Package | Change in commit | Build recipe | Bootstrap / prerequisites |
| --- | --- | --- | --- |
| `gtksourceview4` | Added recipe | [devario-libs/gtksourceview4](devario-libs/gtksourceview4/PKGBUILD) | — |
| `libhandy` | Added recipe | [devario-core/libhandy](devario-core/libhandy/PKGBUILD) | — |
| `libhandy-docs` | Added recipe | [devario-core/libhandy](devario-core/libhandy/PKGBUILD) | — |

## Stage 28

5 packages from 4 recipes.

| Package | Change in commit | Build recipe | Bootstrap / prerequisites |
| --- | --- | --- | --- |
| `meld` | Added recipe | [devario-development/meld](devario-development/meld/PKGBUILD) | — |
| `seahorse` | Added recipe | [devario-core/seahorse](devario-core/seahorse/PKGBUILD) | — |
| `virt-install` | Added recipe | [devario-development/virt-manager](devario-development/virt-manager/PKGBUILD) | — |
| `virt-manager` | Added recipe | [devario-development/virt-manager](devario-development/virt-manager/PKGBUILD) | — |
| `xpad` | Added recipe | [devario-gaming/xpad](devario-gaming/xpad/PKGBUILD) | — |

## Unchanged prerequisites from the original plan

These outputs were not added or modified by this commit. Their stage numbers show where they sit in the original plan; have them available at those points when building from that plan.

| Original stage | Package | Recipe |
| --- | --- | --- |
| 01 | `python-autocommand` | [devario-core/python-autocommand](devario-core/python-autocommand/PKGBUILD) |
| 01 | `python-jaraco.context` | [devario-core/python-jaraco.context](devario-core/python-jaraco.context/PKGBUILD) |
| 01 | `python-more-itertools` | [devario-core/python-more-itertools](devario-core/python-more-itertools/PKGBUILD) |
| 01 | `python-platformdirs` | [devario-core/python-platformdirs](devario-core/python-platformdirs/PKGBUILD) |
| 01 | `python-pyproject-hooks` | [devario-core/python-pyproject-hooks](devario-core/python-pyproject-hooks/PKGBUILD) |
| 02 | `python-hatch-fancy-pypi-readme` | [devario-core/python-hatch-fancy-pypi-readme](devario-core/python-hatch-fancy-pypi-readme/PKGBUILD) |
| 02 | `python-jaraco.functools` | [devario-core/python-jaraco.functools](devario-core/python-jaraco.functools/PKGBUILD) |
| 03 | `python-jaraco.text` | [devario-core/python-jaraco.text](devario-core/python-jaraco.text/PKGBUILD) |
| 04 | `python-jaraco.collections` | [devario-core/python-jaraco.collections](devario-core/python-jaraco.collections/PKGBUILD) |
| 05 | `python-attrs` | [devario-core/python-attrs](devario-core/python-attrs/PKGBUILD) |

## Cycle seed groups

The labels below retain the original plan’s group identifiers. Each listed cycle needs a compatible seed set before its stage. Recipe metadata defines the required versions and virtual providers; a group label does not waive those constraints.

| Stage | Group | Member recipes |
| --- | --- | --- |
| 01 | G159 | `devario-libs/qt5-declarative`, `devario-libs/qt5-tools`, `devario-libs/qt5-translations` |
| 02 | G408 | `devario-libs/python-beautifulsoup4`, `devario-libs/python-soupsieve` |
| 02 | G467 | `devario-development/mingw-w64-gcc`, `devario-libs/mingw-w64-crt`, `devario-libs/mingw-w64-winpthreads` |
| 02 | G537 | `devario-development/unbound`, `devario-libs/ldns`, `devario-utilities/dnssec-anchors` |
| 03 | G012 | `devario-development/node-gyp`, `devario-libs/nodejs-nopt`, `devario-libs/semver` |
| 03 | G423 | `devario-development/dune`, `devario-libs/ocaml-csexp`, `devario-libs/ocaml-pp`, `devario-libs/ocaml-re`, `devario-libs/ocaml-result` |
| 03 | G512 | `devario-development/riscv64-linux-gnu-gcc`, `devario-libs/riscv64-linux-gnu-glibc` |
| 04 | G672 | `devario-libs/lib32-keyutils`, `devario-libs/lib32-krb5` |
| 05 | G039 | `devario-libs/ijs`, `devario-utilities/ghostscript` |
| 06 | G650 | `devario-utilities/cifs-utils`, `devario-utilities/samba` |
| 11 | G101 | `devario-utilities/dvisvgm`, `devario-utilities/texlive-texmf` |
| 22 | G364 | `devario-development/opencascade`, `devario-libs/vtk` |
| 22 | G688 | `devario-libs/lib32-dbus`, `devario-libs/lib32-glib2`, `devario-libs/lib32-systemd` |
| 23 | G714 | `devario-libs/lib32-cairo`, `devario-libs/lib32-fontconfig`, `devario-libs/lib32-freetype2`, `devario-libs/lib32-harfbuzz` |
| 23 | G734 | `devario-libs/lib32-libglvnd`, `devario-libs/lib32-libva`, `devario-libs/lib32-mesa` |

## Inventory verification

Every recipe directory touched by the commit is represented, including the metadata-only SWIG change. Output names come from the committed `.SRCINFO` files; existing output names were compared with the parent commit’s `PKGBUILD` declarations. Each of the 1,321 outputs appears exactly once. Stage and bootstrap labels are inherited from the committed application plan, with the Neovim and Texinfo placements explained above. This is an inventory and ordering update, not a fresh dependency-resolution or build-success report.
