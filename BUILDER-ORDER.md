# Devario builder order

For the three recipes changed in the latest hook audit, use [the latest-only build order](LATEST-BUILD-ORDER.md), with all 43 package outputs listed individually.

Each stage below lists every package by name, with its build recipe and bootstrap requirement. The order covers **908 recipes in 28 stages**: the 896 new recipes and 12 reused existing recipes from this application expansion.

## Follow this sequence

1. Start with a working Devario builder and the published dependency packages recorded in the [repository snapshot](audits/application-expansion-2026-10-08/repository-snapshot.json). This is an expansion of that repository, not a build from an empty system.
2. Read [bootstrap-order.txt](audits/application-expansion-2026-10-08/bootstrap-order.txt). Make the required seed packages available to the isolated builder before starting each flagged group. An installed host tool alone does not satisfy a dependency inside an isolated root.
3. Build **stage 01**, then **02**, continuing through **28**. Independent groups within a stage may run in parallel in separate roots. The group numbers preserve the earlier manifest identifiers; follow stage order in this plan.
4. Publish completed dependency packages to the builder repository and refresh its metadata before provisioning dependent groups. For a cyclic group, retain its working seeds until all replacement packages have been built and the group can be published together.
5. Use `--no-check` for this queue. Build split recipes once and publish their outputs; install only compatible alternatives in each root. Test-only and optional dependency expansions are separate.

If a bootstrap group cannot be provisioned, stop that group and its dependents. Unrelated groups can continue. The TSV lists the exact previous groups and bootstrap groups each recipe needs; do not bypass dependency checking to force progress.

## Packages by stage

**1329 package outputs from 908 recipes.** Every package is listed individually below. Rows sharing a recipe are split outputs: **build that recipe once**, then publish its outputs. The scope remains 896 new recipes plus 12 reused existing recipes.

Work through stages 01–28. Publish dependencies and refresh the builder repository before the next stage. Independent groups within a stage can build in parallel. A bootstrap label means the group needs seed packages before it can build; see [bootstrap-order.txt](audits/application-expansion-2026-10-08/bootstrap-order.txt).

Jump to stage: [01](#stage-01) · [02](#stage-02) · [03](#stage-03) · [04](#stage-04) · [05](#stage-05) · [06](#stage-06) · [07](#stage-07) · [08](#stage-08) · [09](#stage-09) · [10](#stage-10) · [11](#stage-11) · [12](#stage-12) · [13](#stage-13) · [14](#stage-14) · [15](#stage-15) · [16](#stage-16) · [17](#stage-17) · [18](#stage-18) · [19](#stage-19) · [20](#stage-20) · [21](#stage-21) · [22](#stage-22) · [23](#stage-23) · [24](#stage-24) · [25](#stage-25) · [26](#stage-26) · [27](#stage-27) · [28](#stage-28)

### Stage 01

409 packages from 327 recipes.

| Package | Build recipe | Bootstrap requirement |
| --- | --- | --- |
| `aalib` | [devario-libs/aalib](devario-libs/aalib/PKGBUILD) | — |
| `acpica` | [devario-development/acpica](devario-development/acpica/PKGBUILD) | — |
| `ada` | [devario-libs/ada](devario-libs/ada/PKGBUILD) | — |
| `alembic` | [devario-libs/alembic](devario-libs/alembic/PKGBUILD) | — |
| `anari-sdk` | [devario-development/anari-sdk](devario-development/anari-sdk/PKGBUILD) | — |
| `apache-orc` | [devario-libs/apache-orc](devario-libs/apache-orc/PKGBUILD) | — |
| `argon2` | [devario-libs/argon2](devario-libs/argon2/PKGBUILD) | — |
| `arj` | [devario-development/arj](devario-development/arj/PKGBUILD) | — |
| `aspell` | [devario-utilities/aspell](devario-utilities/aspell/PKGBUILD) | — |
| `assimp` | [devario-libs/assimp](devario-libs/assimp/PKGBUILD) | — |
| `aws-c-common` | [devario-libs/aws-c-common](devario-libs/aws-c-common/PKGBUILD) | — |
| `benchmark` | [devario-libs/benchmark](devario-libs/benchmark/PKGBUILD) | — |
| `blosc` | [devario-libs/blosc](devario-libs/blosc/PKGBUILD) | — |
| `boxed-cpp` | [devario-libs/boxed-cpp](devario-libs/boxed-cpp/PKGBUILD) | — |
| `btrfs-assistant` | [devario-utilities/btrfs-assistant](devario-utilities/btrfs-assistant/PKGBUILD) | — |
| `bzip3` | [devario-development/bzip3](devario-development/bzip3/PKGBUILD) | — |
| `c-ares` | [devario-libs/c-ares](devario-libs/c-ares/PKGBUILD) | — |
| `cabextract` | [devario-utilities/cabextract](devario-utilities/cabextract/PKGBUILD) | — |
| `catch2` | [devario-libs/catch2](devario-libs/catch2/PKGBUILD) | — |
| `cbindgen` | [devario-libs/cbindgen](devario-libs/cbindgen/PKGBUILD) | — |
| `cdparanoia` | [devario-utilities/cdparanoia](devario-utilities/cdparanoia/PKGBUILD) | — |
| `cdrtools` | [devario-development/cdrtools](devario-development/cdrtools/PKGBUILD) | — |
| `chromaprint` | [devario-libs/chromaprint](devario-libs/chromaprint/PKGBUILD) | — |
| `chrono-date` | [devario-libs/chrono-date](devario-libs/chrono-date/PKGBUILD) | — |
| `chrpath` | [devario-development/chrpath](devario-development/chrpath/PKGBUILD) | — |
| `cli11` | [devario-development/cli11](devario-development/cli11/PKGBUILD) | — |
| `cliphist` | [devario-utilities/cliphist](devario-utilities/cliphist/PKGBUILD) | — |
| `cmocka` | [devario-development/cmocka](devario-development/cmocka/PKGBUILD) | — |
| `codelldb-bin` | [devario-development/codelldb-bin](devario-development/codelldb-bin/PKGBUILD) | — |
| `cppunit` | [devario-libs/cppunit](devario-libs/cppunit/PKGBUILD) | — |
| `cpuinfo` | [devario-libs/cpuinfo](devario-libs/cpuinfo/PKGBUILD) | — |
| `cudnn` | [devario-libs/cudnn](devario-libs/cudnn/PKGBUILD) | — |
| `cxxopts` | [devario-development/cxxopts](devario-development/cxxopts/PKGBUILD) | — |
| `directx-headers` | [devario-libs/directx-headers](devario-libs/directx-headers/PKGBUILD) | — |
| `discord` | [devario-gaming/discord](devario-gaming/discord/PKGBUILD) | — |
| `djvulibre` | [devario-libs/djvulibre](devario-libs/djvulibre/PKGBUILD) | — |
| `dlpack` | [devario-libs/dlpack](devario-libs/dlpack/PKGBUILD) | — |
| `docbook-dsssl` | [devario-utilities/docbook-dsssl](devario-utilities/docbook-dsssl/PKGBUILD) | — |
| `docbook-sgml31` | [devario-utilities/docbook-sgml31](devario-utilities/docbook-sgml31/PKGBUILD) | — |
| `docker-compose` | [devario-development/docker-compose](devario-development/docker-compose/PKGBUILD) | — |
| `doctest` | [devario-libs/doctest](devario-libs/doctest/PKGBUILD) | — |
| `dotconf` | [devario-libs/dotconf](devario-libs/dotconf/PKGBUILD) | — |
| `ed` | [devario-development/ed](devario-development/ed/PKGBUILD) | — |
| `ethtool` | [devario-utilities/ethtool](devario-utilities/ethtool/PKGBUILD) | — |
| `exiv2` | [devario-libs/exiv2](devario-libs/exiv2/PKGBUILD) | — |
| `faac` | [devario-development/faac](devario-development/faac/PKGBUILD) | — |
| `faad2` | [devario-development/faad2](devario-development/faad2/PKGBUILD) | — |
| `festival` | [devario-development/festival](devario-development/festival/PKGBUILD) | — |
| `ffcall` | [devario-libs/ffcall](devario-libs/ffcall/PKGBUILD) | — |
| `ffnvcodec-headers` | [devario-libs/ffnvcodec-headers](devario-libs/ffnvcodec-headers/PKGBUILD) | — |
| `fltk1.3` | [devario-development/fltk1.3](devario-development/fltk1.3/PKGBUILD) | — |
| `fluxer-canary-bin` | [devario-gaming/fluxer-canary-bin](devario-gaming/fluxer-canary-bin/PKGBUILD) | — |
| `fpc` | [devario-development/fpc](devario-development/fpc/PKGBUILD) | Seed: `fpc` |
| `fpc-src` | [devario-development/fpc-src](devario-development/fpc-src/PKGBUILD) | — |
| `freetds` | [devario-libs/freetds](devario-libs/freetds/PKGBUILD) | — |
| `fstrm` | [devario-libs/fstrm](devario-libs/fstrm/PKGBUILD) | — |
| `functional-plus` | [devario-libs/functional-plus](devario-libs/functional-plus/PKGBUILD) | — |
| `gamemode` | [devario-gaming/gamemode](devario-gaming/gamemode/PKGBUILD) | — |
| `gendesk` | [devario-development/gendesk](devario-development/gendesk/PKGBUILD) | — |
| `geos` | [devario-libs/geos](devario-libs/geos/PKGBUILD) | — |
| `github-cli` | [devario-development/github-cli](devario-development/github-cli/PKGBUILD) | — |
| `glew` | [devario-libs/glew](devario-libs/glew/PKGBUILD) | — |
| `glfw` | [devario-libs/glfw](devario-libs/glfw/PKGBUILD) | — |
| `glm` | [devario-libs/glm](devario-libs/glm/PKGBUILD) | — |
| `glow` | [devario-productivity/glow](devario-productivity/glow/PKGBUILD) | — |
| `gn` | [devario-development/gn](devario-development/gn/PKGBUILD) | — |
| `gnu-efi` | [devario-development/gnu-efi](devario-development/gnu-efi/PKGBUILD) | — |
| `go-tools` | [devario-development/go-tools](devario-development/go-tools/PKGBUILD) | — |
| `gperf` | [devario-development/gperf](devario-development/gperf/PKGBUILD) | — |
| `gpgmepp` | [devario-libs/gpgmepp](devario-libs/gpgmepp/PKGBUILD) | — |
| `gpu-screen-recorder` | [devario-entertainment/gpu-screen-recorder](devario-entertainment/gpu-screen-recorder/PKGBUILD) | — |
| `grabit-git` | [devario-utilities/grabit-git](devario-utilities/grabit-git/PKGBUILD) | — |
| `gsl` | [devario-libs/gsl](devario-libs/gsl/PKGBUILD) | — |
| `half` | [devario-libs/half](devario-libs/half/PKGBUILD) | — |
| `hdparm` | [devario-utilities/hdparm](devario-utilities/hdparm/PKGBUILD) | — |
| `hipblas-common` | [devario-libs/hipblas-common](devario-libs/hipblas-common/PKGBUILD) | — |
| `hiredis` | [devario-libs/hiredis](devario-libs/hiredis/PKGBUILD) | — |
| `hyphen` | [devario-libs/hyphen](devario-libs/hyphen/PKGBUILD) | — |
| `hyphen-en` | [devario-libs/hyphen](devario-libs/hyphen/PKGBUILD) | — |
| `iniparser` | [devario-libs/iniparser](devario-libs/iniparser/PKGBUILD) | — |
| `intltool` | [devario-development/intltool](devario-development/intltool/PKGBUILD) | — |
| `itstool` | [devario-development/itstool](devario-development/itstool/PKGBUILD) | — |
| `iw` | [devario-utilities/iw](devario-utilities/iw/PKGBUILD) | — |
| `java-environment-common` | [devario-libs/java-common](devario-libs/java-common/PKGBUILD) | — |
| `java-runtime-common` | [devario-libs/java-common](devario-libs/java-common/PKGBUILD) | — |
| `jbig2dec` | [devario-libs/jbig2dec](devario-libs/jbig2dec/PKGBUILD) | — |
| `karchive` | [devario-libs/karchive](devario-libs/karchive/PKGBUILD) | — |
| `kconfig` | [devario-libs/kconfig](devario-libs/kconfig/PKGBUILD) | — |
| `kglobalaccel` | [devario-libs/kglobalaccel](devario-libs/kglobalaccel/PKGBUILD) | — |
| `kirigami` | [devario-libs/kirigami](devario-libs/kirigami/PKGBUILD) | — |
| `kitemmodels` | [devario-libs/kitemmodels](devario-libs/kitemmodels/PKGBUILD) | — |
| `lact` | [devario-utilities/lact](devario-utilities/lact/PKGBUILD) | — |
| `ladspa` | [devario-development/ladspa](devario-development/ladspa/PKGBUILD) | — |
| `laszip2` | [devario-libs/laszip2](devario-libs/laszip2/PKGBUILD) | — |
| `lbzip2` | [devario-development/lbzip2](devario-development/lbzip2/PKGBUILD) | — |
| `lhasa` | [devario-development/lhasa](devario-development/lhasa/PKGBUILD) | — |
| `lib32-alsa-lib` | [devario-libs/lib32-alsa-lib](devario-libs/lib32-alsa-lib/PKGBUILD) | — |
| `lib32-attr` | [devario-libs/lib32-attr](devario-libs/lib32-attr/PKGBUILD) | — |
| `lib32-brotli` | [devario-libs/lib32-brotli](devario-libs/lib32-brotli/PKGBUILD) | — |
| `lib32-bzip2` | [devario-libs/lib32-bzip2](devario-libs/lib32-bzip2/PKGBUILD) | — |
| `lib32-expat` | [devario-libs/lib32-expat](devario-libs/lib32-expat/PKGBUILD) | — |
| `lib32-gmp` | [devario-libs/lib32-gmp](devario-libs/lib32-gmp/PKGBUILD) | — |
| `lib32-icu` | [devario-libs/lib32-icu](devario-libs/lib32-icu/PKGBUILD) | — |
| `lib32-json-c` | [devario-libs/lib32-json-c](devario-libs/lib32-json-c/PKGBUILD) | — |
| `lib32-libdisplay-info` | [devario-libs/lib32-libdisplay-info](devario-libs/lib32-libdisplay-info/PKGBUILD) | — |
| `lib32-libffi` | [devario-libs/lib32-libffi](devario-libs/lib32-libffi/PKGBUILD) | — |
| `lib32-libgpg-error` | [devario-libs/lib32-libgpg-error](devario-libs/lib32-libgpg-error/PKGBUILD) | — |
| `lib32-libndp` | [devario-libs/lib32-libndp](devario-libs/lib32-libndp/PKGBUILD) | — |
| `lib32-libnghttp2` | [devario-libs/lib32-libnghttp2](devario-libs/lib32-libnghttp2/PKGBUILD) | — |
| `lib32-libnghttp3` | [devario-libs/lib32-libnghttp3](devario-libs/lib32-libnghttp3/PKGBUILD) | — |
| `lib32-libogg` | [devario-libs/lib32-libogg](devario-libs/lib32-libogg/PKGBUILD) | — |
| `lib32-libtasn1` | [devario-libs/lib32-libtasn1](devario-libs/lib32-libtasn1/PKGBUILD) | — |
| `lib32-libunistring` | [devario-libs/lib32-libunistring](devario-libs/lib32-libunistring/PKGBUILD) | — |
| `lib32-libxau` | [devario-libs/lib32-libxau](devario-libs/lib32-libxau/PKGBUILD) | — |
| `lib32-libxcrypt` | [devario-libs/lib32-libxcrypt](devario-libs/lib32-libxcrypt/PKGBUILD) | — |
| `lib32-libxcrypt-compat` | [devario-libs/lib32-libxcrypt](devario-libs/lib32-libxcrypt/PKGBUILD) | — |
| `lib32-lm_sensors` | [devario-libs/lib32-lm_sensors](devario-libs/lib32-lm_sensors/PKGBUILD) | — |
| `lib32-ncurses` | [devario-libs/lib32-ncurses](devario-libs/lib32-ncurses/PKGBUILD) | — |
| `lib32-openssl` | [devario-libs/lib32-openssl](devario-libs/lib32-openssl/PKGBUILD) | — |
| `lib32-opus` | [devario-libs/lib32-opus](devario-libs/lib32-opus/PKGBUILD) | — |
| `lib32-speexdsp` | [devario-libs/lib32-speexdsp](devario-libs/lib32-speexdsp/PKGBUILD) | — |
| `lib32-spirv-tools` | [devario-libs/lib32-spirv-tools](devario-libs/lib32-spirv-tools/PKGBUILD) | — |
| `lib32-zlib` | [devario-libs/lib32-zlib](devario-libs/lib32-zlib/PKGBUILD) | — |
| `lib32-zstd` | [devario-libs/lib32-zstd](devario-libs/lib32-zstd/PKGBUILD) | — |
| `libaemu` | [devario-libs/libaemu](devario-libs/libaemu/PKGBUILD) | — |
| `libao` | [devario-libs/libao](devario-libs/libao/PKGBUILD) | — |
| `libburn` | [devario-libs/libburn](devario-libs/libburn/PKGBUILD) | — |
| `libcacard` | [devario-libs/libcacard](devario-libs/libcacard/PKGBUILD) | — |
| `libcue` | [devario-libs/libcue](devario-libs/libcue/PKGBUILD) | — |
| `libdca` | [devario-libs/libdca](devario-libs/libdca/PKGBUILD) | — |
| `libde265` | [devario-libs/libde265](devario-libs/libde265/PKGBUILD) | — |
| `libfreexl` | [devario-libs/libfreexl](devario-libs/libfreexl/PKGBUILD) | — |
| `libgme` | [devario-libs/libgme](devario-libs/libgme/PKGBUILD) | — |
| `libharu` | [devario-libs/libharu](devario-libs/libharu/PKGBUILD) | — |
| `libidn` | [devario-libs/libidn](devario-libs/libidn/PKGBUILD) | — |
| `libiscsi` | [devario-libs/libiscsi](devario-libs/libiscsi/PKGBUILD) | — |
| `libisofs` | [devario-libs/libisofs](devario-libs/libisofs/PKGBUILD) | — |
| `liblqr` | [devario-libs/liblqr](devario-libs/liblqr/PKGBUILD) | — |
| `libltc` | [devario-libs/libltc](devario-libs/libltc/PKGBUILD) | — |
| `libmaxminddb` | [devario-libs/libmaxminddb](devario-libs/libmaxminddb/PKGBUILD) | — |
| `libmicrodns` | [devario-libs/libmicrodns](devario-libs/libmicrodns/PKGBUILD) | — |
| `libmicrohttpd` | [devario-libs/libmicrohttpd](devario-libs/libmicrohttpd/PKGBUILD) | — |
| `libmms` | [devario-libs/libmms](devario-libs/libmms/PKGBUILD) | — |
| `libnfs` | [devario-libs/libnfs](devario-libs/libnfs/PKGBUILD) | — |
| `libpaper` | [devario-libs/libpaper](devario-libs/libpaper/PKGBUILD) | — |
| `libpfm` | [devario-libs/libpfm](devario-libs/libpfm/PKGBUILD) | — |
| `libreplaygain` | [devario-libs/libreplaygain](devario-libs/libreplaygain/PKGBUILD) | — |
| `libsass` | [devario-libs/libsass](devario-libs/libsass/PKGBUILD) | — |
| `libshout` | [devario-libs/libshout](devario-libs/libshout/PKGBUILD) | — |
| `libsigsegv` | [devario-libs/libsigsegv](devario-libs/libsigsegv/PKGBUILD) | — |
| `libsixel` | [devario-libs/libsixel](devario-libs/libsixel/PKGBUILD) | — |
| `libslirp` | [devario-libs/libslirp](devario-libs/libslirp/PKGBUILD) | — |
| `libsonic` | [devario-libs/libsonic](devario-libs/libsonic/PKGBUILD) | — |
| `libspiro` | [devario-libs/libspiro](devario-libs/libspiro/PKGBUILD) | — |
| `libsrtp` | [devario-libs/libsrtp](devario-libs/libsrtp/PKGBUILD) | — |
| `libsrtp-docs` | [devario-libs/libsrtp](devario-libs/libsrtp/PKGBUILD) | — |
| `libtlsrpt` | [devario-libs/libtlsrpt](devario-libs/libtlsrpt/PKGBUILD) | — |
| `libultrahdr` | [devario-libs/libultrahdr](devario-libs/libultrahdr/PKGBUILD) | — |
| `libuninameslist` | [devario-libs/libuninameslist](devario-libs/libuninameslist/PKGBUILD) | — |
| `libunrar` | [devario-utilities/unrar](devario-utilities/unrar/PKGBUILD) | — |
| `libutempter` | [devario-libs/libutempter](devario-libs/libutempter/PKGBUILD) | — |
| `libutf8proc` | [devario-libs/libutf8proc](devario-libs/libutf8proc/PKGBUILD) | — |
| `libvoikko` | [devario-libs/libvoikko](devario-libs/libvoikko/PKGBUILD) | — |
| `libwmf` | [devario-libs/libwmf](devario-libs/libwmf/PKGBUILD) | — |
| `libx86` | [devario-libs/libx86](devario-libs/libx86/PKGBUILD) | — |
| `libxnvctrl` | [devario-utilities/nvidia-settings](devario-utilities/nvidia-settings/PKGBUILD) | — |
| `libyuv` | [devario-libs/libyuv](devario-libs/libyuv/PKGBUILD) | — |
| `libzen` | [devario-libs/libzen](devario-libs/libzen/PKGBUILD) | — |
| `libzip` | [devario-libs/libzip](devario-libs/libzip/PKGBUILD) | — |
| `log4cplus` | [devario-libs/log4cplus](devario-libs/log4cplus/PKGBUILD) | — |
| `logrotate` | [devario-core/logrotate](devario-core/logrotate/PKGBUILD) | — |
| `lrzip` | [devario-development/lrzip](devario-development/lrzip/PKGBUILD) | — |
| `lsb-release` | [devario-utilities/lsb-release](devario-utilities/lsb-release/PKGBUILD) | — |
| `luajit` | [devario-libs/luajit](devario-libs/luajit/PKGBUILD) | — |
| `lynx` | [devario-development/lynx](devario-development/lynx/PKGBUILD) | — |
| `mbedtls3` | [devario-libs/mbedtls3](devario-libs/mbedtls3/PKGBUILD) | — |
| `micro` | [devario-core/micro](devario-core/micro/PKGBUILD) | — |
| `microsoft-gsl` | [devario-libs/microsoft-gsl](devario-libs/microsoft-gsl/PKGBUILD) | — |
| `mingw-w64-binutils` | [devario-development/mingw-w64-binutils](devario-development/mingw-w64-binutils/PKGBUILD) | — |
| `mingw-w64-headers` | [devario-libs/mingw-w64-headers](devario-libs/mingw-w64-headers/PKGBUILD) | — |
| `mingw-w64-tools` | [devario-development/mingw-w64-tools](devario-development/mingw-w64-tools/PKGBUILD) | — |
| `mmdblookup` | [devario-libs/libmaxminddb](devario-libs/libmaxminddb/PKGBUILD) | — |
| `mongo-c-driver` | [devario-libs/mongo-c-driver](devario-libs/mongo-c-driver/PKGBUILD) | — |
| `msgpack-cxx` | [devario-libs/msgpack-cxx](devario-libs/msgpack-cxx/PKGBUILD) | — |
| `mtools` | [devario-utilities/mtools](devario-utilities/mtools/PKGBUILD) | — |
| `mujs` | [devario-libs/mujs](devario-libs/mujs/PKGBUILD) | — |
| `multipath-tools` | [devario-utilities/multipath-tools](devario-utilities/multipath-tools/PKGBUILD) | — |
| `muparser` | [devario-libs/muparser](devario-libs/muparser/PKGBUILD) | — |
| `nano` | [devario-core/nano](devario-core/nano/PKGBUILD) | — |
| `ntsync-autoload` | [devario-utilities/ntsync-autoload](devario-utilities/ntsync-autoload/PKGBUILD) | — |
| `nvidia-settings` | [devario-utilities/nvidia-settings](devario-utilities/nvidia-settings/PKGBUILD) | — |
| `nvm` | [devario-development/nvm](devario-development/nvm/PKGBUILD) | — |
| `nvtop` | [devario-utilities/nvtop](devario-utilities/nvtop/PKGBUILD) | — |
| `ocaml` | [devario-development/ocaml](devario-development/ocaml/PKGBUILD) | — |
| `ocaml-compiler-libs` | [devario-development/ocaml](devario-development/ocaml/PKGBUILD) | — |
| `onednn` | [devario-libs/onednn](devario-libs/onednn/PKGBUILD) | — |
| `opencl-headers` | [devario-libs/opencl-headers](devario-libs/opencl-headers/PKGBUILD) | — |
| `openvr` | [devario-development/openvr](devario-development/openvr/PKGBUILD) | — |
| `openxr` | [devario-libs/openxr](devario-libs/openxr/PKGBUILD) | — |
| `osinfo-db-tools` | [devario-development/osinfo-db-tools](devario-development/osinfo-db-tools/PKGBUILD) | — |
| `otf-atkinsonhyperlegiblemono-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `otf-aurulent-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `otf-codenewroman-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `otf-comicshanns-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `otf-commit-mono-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `otf-droid-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `otf-firamono-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `otf-geist-mono-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `otf-hasklig-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `otf-hermit-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `otf-monaspace-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `otf-opendyslexic-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `otf-overpass-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `pangomm-2.48` | [devario-libs/pangomm-2.48](devario-libs/pangomm-2.48/PKGBUILD) | — |
| `pangomm-2.48-docs` | [devario-libs/pangomm-2.48](devario-libs/pangomm-2.48/PKGBUILD) | — |
| `parallel` | [devario-utilities/parallel](devario-utilities/parallel/PKGBUILD) | — |
| `parallel-docs` | [devario-utilities/parallel](devario-utilities/parallel/PKGBUILD) | — |
| `pcaudiolib` | [devario-libs/pcaudiolib](devario-libs/pcaudiolib/PKGBUILD) | — |
| `perl-archive-cpio` | [devario-libs/perl-archive-cpio](devario-libs/perl-archive-cpio/PKGBUILD) | — |
| `perl-archive-zip` | [devario-libs/perl-archive-zip](devario-libs/perl-archive-zip/PKGBUILD) | — |
| `perl-file-slurp` | [devario-libs/perl-file-slurp](devario-libs/perl-file-slurp/PKGBUILD) | — |
| `perl-file-which` | [devario-libs/perl-file-which](devario-libs/perl-file-which/PKGBUILD) | — |
| `perl-inc-latest` | [devario-libs/perl-inc-latest](devario-libs/perl-inc-latest/PKGBUILD) | — |
| `perl-io-string` | [devario-libs/perl-io-string](devario-libs/perl-io-string/PKGBUILD) | — |
| `perl-json` | [devario-libs/perl-json](devario-libs/perl-json/PKGBUILD) | — |
| `perl-locale-gettext` | [devario-libs/perl-locale-gettext](devario-libs/perl-locale-gettext/PKGBUILD) | — |
| `perl-mime-charset` | [devario-libs/perl-mime-charset](devario-libs/perl-mime-charset/PKGBUILD) | — |
| `perl-params-someutil` | [devario-libs/perl-params-someutil](devario-libs/perl-params-someutil/PKGBUILD) | — |
| `perl-parse-yapp` | [devario-libs/perl-parse-yapp](devario-libs/perl-parse-yapp/PKGBUILD) | — |
| `perl-pod-parser` | [devario-libs/perl-pod-parser](devario-libs/perl-pod-parser/PKGBUILD) | — |
| `perl-sgmls` | [devario-libs/perl-sgmls](devario-libs/perl-sgmls/PKGBUILD) | — |
| `perl-sort-versions` | [devario-libs/perl-sort-versions](devario-libs/perl-sort-versions/PKGBUILD) | — |
| `perl-sub-install` | [devario-libs/perl-sub-install](devario-libs/perl-sub-install/PKGBUILD) | — |
| `perl-term-readkey` | [devario-libs/perl-term-readkey](devario-libs/perl-term-readkey/PKGBUILD) | — |
| `perl-text-charwidth` | [devario-libs/perl-text-charwidth](devario-libs/perl-text-charwidth/PKGBUILD) | — |
| `perl-text-csv` | [devario-libs/perl-text-csv](devario-libs/perl-text-csv/PKGBUILD) | — |
| `perl-yaml-tiny` | [devario-libs/perl-yaml-tiny](devario-libs/perl-yaml-tiny/PKGBUILD) | — |
| `pkcs11-helper` | [devario-libs/pkcs11-helper](devario-libs/pkcs11-helper/PKGBUILD) | — |
| `plasma-wayland-protocols` | [devario-development/plasma-wayland-protocols](devario-development/plasma-wayland-protocols/PKGBUILD) | — |
| `poppler-data` | [devario-libs/poppler-data](devario-libs/poppler-data/PKGBUILD) | — |
| `potrace` | [devario-entertainment/potrace](devario-entertainment/potrace/PKGBUILD) | — |
| `proj` | [devario-libs/proj](devario-libs/proj/PKGBUILD) | — |
| `protobuf-c` | [devario-libs/protobuf-c](devario-libs/protobuf-c/PKGBUILD) | — |
| `publicsuffix-list` | [devario-development/publicsuffix-list](devario-development/publicsuffix-list/PKGBUILD) | — |
| `pugixml` | [devario-libs/pugixml](devario-libs/pugixml/PKGBUILD) | — |
| `python-autocommand` | [devario-core/python-autocommand](devario-core/python-autocommand/PKGBUILD) | — |
| `python-jaraco.context` | [devario-core/python-jaraco.context](devario-core/python-jaraco.context/PKGBUILD) | — |
| `python-more-itertools` | [devario-core/python-more-itertools](devario-core/python-more-itertools/PKGBUILD) | — |
| `python-platformdirs` | [devario-core/python-platformdirs](devario-core/python-platformdirs/PKGBUILD) | — |
| `python-pyproject-hooks` | [devario-core/python-pyproject-hooks](devario-core/python-pyproject-hooks/PKGBUILD) | — |
| `qhull` | [devario-libs/qhull](devario-libs/qhull/PKGBUILD) | — |
| `qrencode` | [devario-libs/qrencode](devario-libs/qrencode/PKGBUILD) | — |
| `qt5-declarative` | [devario-libs/qt5-declarative](devario-libs/qt5-declarative/PKGBUILD) | Cycle G159 — seed packages required |
| `qt5-tools` | [devario-libs/qt5-tools](devario-libs/qt5-tools/PKGBUILD) | Cycle G159 — seed packages required |
| `qt5-translations` | [devario-libs/qt5-translations](devario-libs/qt5-translations/PKGBUILD) | Cycle G159 — seed packages required |
| `qt6-5compat` | [devario-libs/qt6-5compat](devario-libs/qt6-5compat/PKGBUILD) | — |
| `qt6-canvaspainter` | [devario-libs/qt6-canvaspainter](devario-libs/qt6-canvaspainter/PKGBUILD) | — |
| `qt6-charts` | [devario-libs/qt6-charts](devario-libs/qt6-charts/PKGBUILD) | — |
| `qt6-connectivity` | [devario-libs/qt6-connectivity](devario-libs/qt6-connectivity/PKGBUILD) | — |
| `qt6-datavis3d` | [devario-libs/qt6-datavis3d](devario-libs/qt6-datavis3d/PKGBUILD) | — |
| `qt6-networkauth` | [devario-libs/qt6-networkauth](devario-libs/qt6-networkauth/PKGBUILD) | — |
| `qt6-quicktimeline` | [devario-libs/qt6-quicktimeline](devario-libs/qt6-quicktimeline/PKGBUILD) | — |
| `qt6-remoteobjects` | [devario-libs/qt6-remoteobjects](devario-libs/qt6-remoteobjects/PKGBUILD) | — |
| `qt6-scxml` | [devario-libs/qt6-scxml](devario-libs/qt6-scxml/PKGBUILD) | — |
| `qt6-sensors` | [devario-libs/qt6-sensors](devario-libs/qt6-sensors/PKGBUILD) | — |
| `qt6-serialport` | [devario-libs/qt6-serialport](devario-libs/qt6-serialport/PKGBUILD) | — |
| `qt6-webchannel` | [devario-libs/qt6-webchannel](devario-libs/qt6-webchannel/PKGBUILD) | — |
| `qt6-websockets` | [devario-libs/qt6-websockets](devario-libs/qt6-websockets/PKGBUILD) | — |
| `qt6pas` | [devario-libs/qt6pas](devario-libs/qt6pas/PKGBUILD) | — |
| `range-v3` | [devario-libs/range-v3](devario-libs/range-v3/PKGBUILD) | — |
| `rapidjson` | [devario-development/rapidjson](devario-development/rapidjson/PKGBUILD) | — |
| `re2` | [devario-libs/re2](devario-libs/re2/PKGBUILD) | — |
| `reflection-cpp` | [devario-libs/reflection-cpp](devario-libs/reflection-cpp/PKGBUILD) | — |
| `riscv64-linux-gnu-linux-api-headers` | [devario-libs/riscv64-linux-gnu-linux-api-headers](devario-libs/riscv64-linux-gnu-linux-api-headers/PKGBUILD) | — |
| `rkcommon` | [devario-libs/rkcommon](devario-libs/rkcommon/PKGBUILD) | — |
| `rnnoise` | [devario-libs/rnnoise](devario-libs/rnnoise/PKGBUILD) | — |
| `robin-map` | [devario-libs/robin-map](devario-libs/robin-map/PKGBUILD) | — |
| `rocm-toolchain` | [devario-development/rocm-toolchain](devario-development/rocm-toolchain/PKGBUILD) | — |
| `roctracer` | [devario-libs/roctracer](devario-libs/roctracer/PKGBUILD) | — |
| `rpcsvc-proto` | [devario-development/rpcsvc-proto](devario-development/rpcsvc-proto/PKGBUILD) | — |
| `rpmextract` | [devario-development/rpmextract](devario-development/rpmextract/PKGBUILD) | — |
| `rtmpdump` | [devario-development/rtmpdump](devario-development/rtmpdump/PKGBUILD) | — |
| `ruby-kramdown` | [devario-libs/ruby-kramdown](devario-libs/ruby-kramdown/PKGBUILD) | — |
| `ruby-mini_portile2` | [devario-libs/ruby-mini_portile2](devario-libs/ruby-mini_portile2/PKGBUILD) | — |
| `ruby-mustache` | [devario-libs/ruby-mustache](devario-libs/ruby-mustache/PKGBUILD) | — |
| `ruby-rdiscount` | [devario-libs/ruby-rdiscount](devario-libs/ruby-rdiscount/PKGBUILD) | — |
| `rust-bindgen` | [devario-libs/rust-bindgen](devario-libs/rust-bindgen/PKGBUILD) | — |
| `rustup` | [devario-development/rustup](devario-development/rustup/PKGBUILD) | — |
| `s2n-tls` | [devario-libs/s2n-tls](devario-libs/s2n-tls/PKGBUILD) | — |
| `safeint` | [devario-libs/safeint](devario-libs/safeint/PKGBUILD) | — |
| `sdl12-compat` | [devario-libs/sdl12-compat](devario-libs/sdl12-compat/PKGBUILD) | — |
| `setconf` | [devario-development/setconf](devario-development/setconf/PKGBUILD) | — |
| `signify` | [devario-development/signify](devario-development/signify/PKGBUILD) | — |
| `simdutf` | [devario-libs/simdutf](devario-libs/simdutf/PKGBUILD) | — |
| `snapper` | [devario-utilities/snapper](devario-utilities/snapper/PKGBUILD) | — |
| `soundtouch` | [devario-libs/soundtouch](devario-libs/soundtouch/PKGBUILD) | — |
| `spice-protocol` | [devario-libs/spice-protocol](devario-libs/spice-protocol/PKGBUILD) | — |
| `spirv-llvm-translator` | [devario-development/spirv-llvm-translator](devario-development/spirv-llvm-translator/PKGBUILD) | — |
| `starship` | [devario-core/starship](devario-core/starship/PKGBUILD) | — |
| `suitesparse` | [devario-libs/suitesparse](devario-libs/suitesparse/PKGBUILD) | — |
| `suitesparse-graphblas` | [devario-libs/suitesparse](devario-libs/suitesparse/PKGBUILD) | — |
| `swig` | [devario-development/swig](devario-development/swig/PKGBUILD) | — |
| `sysfsutils` | [devario-utilities/sysfsutils](devario-utilities/sysfsutils/PKGBUILD) | — |
| `systemd-manager-tui` | [devario-utilities/systemd-manager-tui](devario-utilities/systemd-manager-tui/PKGBUILD) | — |
| `talloc` | [devario-libs/talloc](devario-libs/talloc/PKGBUILD) | — |
| `tcl` | [devario-development/tcl](devario-development/tcl/PKGBUILD) | — |
| `tdb` | [devario-libs/tdb](devario-libs/tdb/PKGBUILD) | — |
| `texi2html` | [devario-development/texi2html](devario-development/texi2html/PKGBUILD) | — |
| `tidy` | [devario-utilities/tidy](devario-utilities/tidy/PKGBUILD) | — |
| `tinycdb` | [devario-libs/tinycdb](devario-libs/tinycdb/PKGBUILD) | — |
| `tinyxml2` | [devario-libs/tinyxml2](devario-libs/tinyxml2/PKGBUILD) | — |
| `tree-sitter` | [devario-development/tree-sitter](devario-development/tree-sitter/PKGBUILD) | — |
| `tree-sitter-cli` | [devario-development/tree-sitter](devario-development/tree-sitter/PKGBUILD) | — |
| `ttf-0xproto-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-3270-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-adwaitamono-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-agave-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-annotationmono-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-anonymouspro-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-arimo-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-bigblueterminal-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-bitstream-vera-mono-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-cascadia-code-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-cascadia-mono-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-cousine-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-d2coding-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-daddytime-mono-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-dejavu-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-envycoder-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-fantasque-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-firacode-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-go-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-gohu-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-googlesanscode-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-hack-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-heavydata-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-iawriter-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-ibmplex-mono-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-inconsolata-go-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-inconsolata-lgc-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-inconsolata-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-intone-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-iosevka-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-iosevkaterm-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-iosevkatermslab-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-jetbrains-mono-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-lekton-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-liberation-mono-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-lilex-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-martian-mono-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-meslo-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-monofur-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-monoid-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-mononoki-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-mplus-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-noto-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-profont-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-proggyclean-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-recursive-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-roboto` | [devario-libs/ttf-roboto](devario-libs/ttf-roboto/PKGBUILD) | — |
| `ttf-roboto-mono` | [devario-development/ttf-roboto-mono](devario-development/ttf-roboto-mono/PKGBUILD) | — |
| `ttf-roboto-mono-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-sharetech-mono-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-sourcecodepro-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-space-mono-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-terminus-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-tinos-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-ubuntu-mono-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-ubuntu-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-victor-mono-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `ttf-zed-mono-nerd` | [devario-libs/nerd-fonts](devario-libs/nerd-fonts/PKGBUILD) | — |
| `twolame` | [devario-libs/twolame](devario-libs/twolame/PKGBUILD) | — |
| `uasm` | [devario-development/uasm](devario-development/uasm/PKGBUILD) | — |
| `uchardet` | [devario-libs/uchardet](devario-libs/uchardet/PKGBUILD) | — |
| `unace` | [devario-development/unace](devario-development/unace/PKGBUILD) | — |
| `unicode-character-database` | [devario-libs/unicode-character-database](devario-libs/unicode-character-database/PKGBUILD) | — |
| `unicode-cldr` | [devario-development/unicode-cldr](devario-development/unicode-cldr/PKGBUILD) | — |
| `unicode-cldr-annotations` | [devario-development/unicode-cldr](devario-development/unicode-cldr/PKGBUILD) | — |
| `unifdef` | [devario-development/unifdef](devario-development/unifdef/PKGBUILD) | — |
| `unrar` | [devario-utilities/unrar](devario-utilities/unrar/PKGBUILD) | — |
| `unzip` | [devario-utilities/unzip](devario-utilities/unzip/PKGBUILD) | — |
| `usbredir` | [devario-libs/usbredir](devario-libs/usbredir/PKGBUILD) | — |
| `utf8cpp` | [devario-development/utf8cpp](devario-development/utf8cpp/PKGBUILD) | — |
| `vc-intrinsics` | [devario-development/vc-intrinsics](devario-development/vc-intrinsics/PKGBUILD) | — |
| `verdict` | [devario-libs/verdict](devario-libs/verdict/PKGBUILD) | — |
| `virtiofsd` | [devario-utilities/virtiofsd](devario-utilities/virtiofsd/PKGBUILD) | — |
| `viskores` | [devario-libs/viskores](devario-libs/viskores/PKGBUILD) | — |
| `vscodium-bin` | [devario-development/vscodium-bin](devario-development/vscodium-bin/PKGBUILD) | — |
| `wavpack` | [devario-libs/wavpack](devario-libs/wavpack/PKGBUILD) | — |
| `webrtc-audio-processing` | [devario-libs/webrtc-audio-processing](devario-libs/webrtc-audio-processing/PKGBUILD) | — |
| `wildmidi` | [devario-libs/wildmidi](devario-libs/wildmidi/PKGBUILD) | — |
| `wlr-randr` | [devario-utilities/wlr-randr](devario-utilities/wlr-randr/PKGBUILD) | — |
| `wlrctl` | [devario-utilities/wlrctl](devario-utilities/wlrctl/PKGBUILD) | — |
| `woff2` | [devario-libs/woff2](devario-libs/woff2/PKGBUILD) | — |
| `wolfssl` | [devario-libs/wolfssl](devario-libs/wolfssl/PKGBUILD) | — |
| `wtype` | [devario-utilities/wtype](devario-utilities/wtype/PKGBUILD) | — |
| `xcur2png` | [devario-utilities/xcur2png](devario-utilities/xcur2png/PKGBUILD) | — |
| `xdg-user-dirs-gtk` | [devario-utilities/xdg-user-dirs-gtk](devario-utilities/xdg-user-dirs-gtk/PKGBUILD) | — |
| `xerces-c` | [devario-libs/xerces-c](devario-libs/xerces-c/PKGBUILD) | — |
| `xmlto` | [devario-development/xmlto](devario-development/xmlto/PKGBUILD) | — |
| `xorg-util-macros` | [devario-development/xorg-util-macros](devario-development/xorg-util-macros/PKGBUILD) | — |
| `xsimd` | [devario-libs/xsimd](devario-libs/xsimd/PKGBUILD) | — |
| `xtrans` | [devario-libs/xtrans](devario-libs/xtrans/PKGBUILD) | — |
| `zint` | [devario-libs/zint](devario-libs/zint/PKGBUILD) | — |
| `zint-qt` | [devario-libs/zint](devario-libs/zint/PKGBUILD) | — |
| `zip` | [devario-development/zip](devario-development/zip/PKGBUILD) | — |
| `zita-convolver` | [devario-libs/zita-convolver](devario-libs/zita-convolver/PKGBUILD) | — |
| `zopfli` | [devario-libs/zopfli](devario-libs/zopfli/PKGBUILD) | — |
| `zvbi` | [devario-libs/zvbi](devario-libs/zvbi/PKGBUILD) | — |

### Stage 02

157 packages from 140 recipes.

| Package | Build recipe | Bootstrap requirement |
| --- | --- | --- |
| `7zip` | [devario-utilities/7zip](devario-utilities/7zip/PKGBUILD) | — |
| `alsa-tools` | [devario-utilities/alsa-tools](devario-utilities/alsa-tools/PKGBUILD) | — |
| `aws-c-cal` | [devario-libs/aws-c-cal](devario-libs/aws-c-cal/PKGBUILD) | — |
| `aws-c-compression` | [devario-libs/aws-c-compression](devario-libs/aws-c-compression/PKGBUILD) | — |
| `aws-c-sdkutils` | [devario-libs/aws-c-sdkutils](devario-libs/aws-c-sdkutils/PKGBUILD) | — |
| `aws-checksums` | [devario-libs/aws-checksums](devario-libs/aws-checksums/PKGBUILD) | — |
| `bc` | [devario-utilities/bc](devario-utilities/bc/PKGBUILD) | — |
| `cava` | [devario-entertainment/cava](devario-entertainment/cava/PKGBUILD) | — |
| `clblast` | [devario-libs/clblast](devario-libs/clblast/PKGBUILD) | — |
| `clisp` | [devario-development/clisp](devario-development/clisp/PKGBUILD) | — |
| `composable-kernel` | [devario-libs/composable-kernel](devario-libs/composable-kernel/PKGBUILD) | — |
| `crypto++` | [devario-libs/crypto++](devario-libs/crypto++/PKGBUILD) | — |
| `dateutils` | [devario-development/dateutils](devario-development/dateutils/PKGBUILD) | — |
| `dnssec-anchors` | [devario-utilities/dnssec-anchors](devario-utilities/dnssec-anchors/PKGBUILD) | Cycle G537 — seed packages required |
| `dpkg` | [devario-development/dpkg](devario-development/dpkg/PKGBUILD) | — |
| `eigen` | [devario-libs/eigen](devario-libs/eigen/PKGBUILD) | — |
| `fast_float` | [devario-development/fast_float](devario-development/fast_float/PKGBUILD) | — |
| `flite` | [devario-development/flite](devario-development/flite/PKGBUILD) | — |
| `fluidsynth` | [devario-libs/fluidsynth](devario-libs/fluidsynth/PKGBUILD) | — |
| `gfxstream` | [devario-libs/gfxstream](devario-libs/gfxstream/PKGBUILD) | — |
| `glusterfs` | [devario-utilities/glusterfs](devario-utilities/glusterfs/PKGBUILD) | — |
| `gtkmm-4.0` | [devario-libs/gtkmm-4.0](devario-libs/gtkmm-4.0/PKGBUILD) | — |
| `gtkmm-4.0-docs` | [devario-libs/gtkmm-4.0](devario-libs/gtkmm-4.0/PKGBUILD) | — |
| `inetutils` | [devario-utilities/inetutils](devario-utilities/inetutils/PKGBUILD) | — |
| `jdk8-openjdk` | [devario-development/java8-openjdk](devario-development/java8-openjdk/PKGBUILD) | Seed: `java-environment=8` |
| `jre8-openjdk` | [devario-development/java8-openjdk](devario-development/java8-openjdk/PKGBUILD) | Seed: `java-environment=8` |
| `jre8-openjdk-headless` | [devario-development/java8-openjdk](devario-development/java8-openjdk/PKGBUILD) | Seed: `java-environment=8` |
| `js140` | [devario-libs/js140](devario-libs/js140/PKGBUILD) | — |
| `kcodecs` | [devario-libs/kcodecs](devario-libs/kcodecs/PKGBUILD) | — |
| `ldns` | [devario-libs/ldns](devario-libs/ldns/PKGBUILD) | Cycle G537 — seed packages required |
| `level-zero-headers` | [devario-development/level-zero](devario-development/level-zero/PKGBUILD) | — |
| `level-zero-loader` | [devario-development/level-zero](devario-development/level-zero/PKGBUILD) | — |
| `lib32-acl` | [devario-libs/lib32-acl](devario-libs/lib32-acl/PKGBUILD) | — |
| `lib32-cmocka` | [devario-development/lib32-cmocka](devario-development/lib32-cmocka/PKGBUILD) | — |
| `lib32-directx-headers` | [devario-libs/lib32-directx-headers](devario-libs/lib32-directx-headers/PKGBUILD) | — |
| `lib32-libasyncns` | [devario-libs/lib32-libasyncns](devario-libs/lib32-libasyncns/PKGBUILD) | — |
| `lib32-libgcrypt` | [devario-libs/lib32-libgcrypt](devario-libs/lib32-libgcrypt/PKGBUILD) | — |
| `lib32-libldap` | [devario-libs/lib32-libldap](devario-libs/lib32-libldap/PKGBUILD) | — |
| `lib32-libpciaccess` | [devario-libs/lib32-libpciaccess](devario-libs/lib32-libpciaccess/PKGBUILD) | — |
| `lib32-libpng` | [devario-libs/lib32-libpng](devario-libs/lib32-libpng/PKGBUILD) | — |
| `lib32-libssh2` | [devario-libs/lib32-libssh2](devario-libs/lib32-libssh2/PKGBUILD) | — |
| `lib32-libvorbis` | [devario-libs/lib32-libvorbis](devario-libs/lib32-libvorbis/PKGBUILD) | — |
| `lib32-libxdmcp` | [devario-libs/lib32-libxdmcp](devario-libs/lib32-libxdmcp/PKGBUILD) | — |
| `lib32-libxshmfence` | [devario-libs/lib32-libxshmfence](devario-libs/lib32-libxshmfence/PKGBUILD) | — |
| `lib32-nettle` | [devario-libs/lib32-nettle](devario-libs/lib32-nettle/PKGBUILD) | — |
| `lib32-nspr` | [devario-libs/lib32-nspr](devario-libs/lib32-nspr/PKGBUILD) | — |
| `lib32-p11-kit` | [devario-libs/lib32-p11-kit](devario-libs/lib32-p11-kit/PKGBUILD) | — |
| `lib32-readline` | [devario-libs/lib32-readline](devario-libs/lib32-readline/PKGBUILD) | — |
| `lib32-util-linux` | [devario-libs/lib32-util-linux](devario-libs/lib32-util-linux/PKGBUILD) | — |
| `libavtp` | [devario-libs/libavtp](devario-libs/libavtp/PKGBUILD) | — |
| `libcbor` | [devario-libs/libcbor](devario-libs/libcbor/PKGBUILD) | — |
| `libclc` | [devario-libs/libclc](devario-libs/libclc/PKGBUILD) | — |
| `libdc1394` | [devario-libs/libdc1394](devario-libs/libdc1394/PKGBUILD) | — |
| `libdv` | [devario-libs/libdv](devario-libs/libdv/PKGBUILD) | — |
| `libev` | [devario-libs/libev](devario-libs/libev/PKGBUILD) | — |
| `libgeotiff` | [devario-libs/libgeotiff](devario-libs/libgeotiff/PKGBUILD) | — |
| `libid3tag` | [devario-libs/libid3tag](devario-libs/libid3tag/PKGBUILD) | — |
| `libieee1284` | [devario-libs/libieee1284](devario-libs/libieee1284/PKGBUILD) | — |
| `libisoburn` | [devario-libs/libisoburn](devario-libs/libisoburn/PKGBUILD) | — |
| `libmediainfo` | [devario-libs/libmediainfo](devario-libs/libmediainfo/PKGBUILD) | — |
| `libmpcdec` | [devario-libs/musepack](devario-libs/musepack/PKGBUILD) | — |
| `libnet` | [devario-libs/libnet](devario-libs/libnet/PKGBUILD) | — |
| `librttopo` | [devario-libs/librttopo](devario-libs/librttopo/PKGBUILD) | — |
| `libunicode` | [devario-libs/libunicode](devario-libs/libunicode/PKGBUILD) | — |
| `libxmu` | [devario-libs/libxmu](devario-libs/libxmu/PKGBUILD) | — |
| `libxpm` | [devario-libs/libxpm](devario-libs/libxpm/PKGBUILD) | — |
| `libxpresent` | [devario-libs/libxpresent](devario-libs/libxpresent/PKGBUILD) | — |
| `lsscsi` | [devario-utilities/lsscsi](devario-utilities/lsscsi/PKGBUILD) | — |
| `mgard` | [devario-libs/mgard](devario-libs/mgard/PKGBUILD) | — |
| `mingw-w64-crt` | [devario-libs/mingw-w64-crt](devario-libs/mingw-w64-crt/PKGBUILD) | Cycle G467 — seed packages required |
| `mingw-w64-gcc` | [devario-development/mingw-w64-gcc](devario-development/mingw-w64-gcc/PKGBUILD) | Cycle G467 — seed packages required |
| `mingw-w64-winpthreads` | [devario-libs/mingw-w64-winpthreads](devario-libs/mingw-w64-winpthreads/PKGBUILD) | Cycle G467 — seed packages required |
| `musepack-tools` | [devario-libs/musepack](devario-libs/musepack/PKGBUILD) | — |
| `neon` | [devario-libs/neon](devario-libs/neon/PKGBUILD) | — |
| `netcdf` | [devario-libs/netcdf](devario-libs/netcdf/PKGBUILD) | — |
| `nodejs` | [devario-development/nodejs](devario-development/nodejs/PKGBUILD) | — |
| `nodejs-lts-iron` | [devario-development/nodejs-lts-iron](devario-development/nodejs-lts-iron/PKGBUILD) | — |
| `nodejs-lts-krypton` | [devario-development/nodejs-lts-krypton](devario-development/nodejs-lts-krypton/PKGBUILD) | — |
| `nwg-look` | [devario-utilities/nwg-look](devario-utilities/nwg-look/PKGBUILD) | — |
| `ocaml-findlib` | [devario-libs/ocaml-findlib](devario-libs/ocaml-findlib/PKGBUILD) | — |
| `ocamlbuild` | [devario-libs/ocamlbuild](devario-libs/ocamlbuild/PKGBUILD) | — |
| `opam` | [devario-development/opam](devario-development/opam/PKGBUILD) | — |
| `openjdk8-doc` | [devario-development/java8-openjdk](devario-development/java8-openjdk/PKGBUILD) | Seed: `java-environment=8` |
| `openjdk8-src` | [devario-development/java8-openjdk](devario-development/java8-openjdk/PKGBUILD) | Seed: `java-environment=8` |
| `openrgb` | [devario-utilities/openrgb](devario-utilities/openrgb/PKGBUILD) | — |
| `opensp` | [devario-libs/opensp](devario-libs/opensp/PKGBUILD) | — |
| `openvpn` | [devario-utilities/openvpn](devario-utilities/openvpn/PKGBUILD) | — |
| `osinfo-db` | [devario-libs/osinfo-db](devario-libs/osinfo-db/PKGBUILD) | — |
| `patchutils` | [devario-development/patchutils](devario-development/patchutils/PKGBUILD) | — |
| `perl-data-optlist` | [devario-libs/perl-data-optlist](devario-libs/perl-data-optlist/PKGBUILD) | — |
| `perl-font-ttf` | [devario-libs/perl-font-ttf](devario-libs/perl-font-ttf/PKGBUILD) | — |
| `perl-module-build` | [devario-libs/perl-module-build](devario-libs/perl-module-build/PKGBUILD) | — |
| `perl-text-wrapi18n` | [devario-libs/perl-text-wrapi18n](devario-libs/perl-text-wrapi18n/PKGBUILD) | — |
| `perl-unicode-linebreak` | [devario-libs/perl-unicode-linebreak](devario-libs/perl-unicode-linebreak/PKGBUILD) | — |
| `podofo` | [devario-libs/podofo](devario-libs/podofo/PKGBUILD) | — |
| `podofo-tools` | [devario-libs/podofo](devario-libs/podofo/PKGBUILD) | — |
| `popsicle` | [devario-utilities/popsicle](devario-utilities/popsicle/PKGBUILD) | — |
| `postfix` | [devario-development/postfix](devario-development/postfix/PKGBUILD) | — |
| `postfix-cdb` | [devario-development/postfix](devario-development/postfix/PKGBUILD) | — |
| `postfix-ldap` | [devario-development/postfix](devario-development/postfix/PKGBUILD) | — |
| `postfix-lmdb` | [devario-development/postfix](devario-development/postfix/PKGBUILD) | — |
| `postfix-mongodb` | [devario-development/postfix](devario-development/postfix/PKGBUILD) | — |
| `postfix-mysql` | [devario-development/postfix](devario-development/postfix/PKGBUILD) | — |
| `postfix-pcre` | [devario-development/postfix](devario-development/postfix/PKGBUILD) | — |
| `postfix-pgsql` | [devario-development/postfix](devario-development/postfix/PKGBUILD) | — |
| `postfix-sqlite` | [devario-development/postfix](devario-development/postfix/PKGBUILD) | — |
| `proton-ge-custom-bin` | [devario-gaming/proton-ge-custom-bin](devario-gaming/proton-ge-custom-bin/PKGBUILD) | — |
| `python-beautifulsoup4` | [devario-libs/python-beautifulsoup4](devario-libs/python-beautifulsoup4/PKGBUILD) | Cycle G408 — seed packages required |
| `python-click` | [devario-libs/python-click](devario-libs/python-click/PKGBUILD) | — |
| `python-cloudpickle` | [devario-libs/python-cloudpickle](devario-libs/python-cloudpickle/PKGBUILD) | — |
| `python-dnspython` | [devario-libs/python-dnspython](devario-libs/python-dnspython/PKGBUILD) | — |
| `python-hatch-fancy-pypi-readme` | [devario-core/python-hatch-fancy-pypi-readme](devario-core/python-hatch-fancy-pypi-readme/PKGBUILD) | — |
| `python-idna` | [devario-libs/python-idna](devario-libs/python-idna/PKGBUILD) | — |
| `python-jaraco.functools` | [devario-core/python-jaraco.functools](devario-core/python-jaraco.functools/PKGBUILD) | — |
| `python-mdurl` | [devario-libs/python-mdurl](devario-libs/python-mdurl/PKGBUILD) | — |
| `python-mypy_extensions` | [devario-development/python-mypy_extensions](devario-development/python-mypy_extensions/PKGBUILD) | — |
| `python-py-cpuinfo2` | [devario-libs/python-py-cpuinfo2](devario-libs/python-py-cpuinfo2/PKGBUILD) | — |
| `python-pyparsing` | [devario-libs/python-pyparsing](devario-libs/python-pyparsing/PKGBUILD) | — |
| `python-roman-numerals-py` | [devario-libs/python-roman-numerals-py](devario-libs/python-roman-numerals-py/PKGBUILD) | — |
| `python-soupsieve` | [devario-libs/python-soupsieve](devario-libs/python-soupsieve/PKGBUILD) | Cycle G408 — seed packages required |
| `python-sphinx-alabaster-theme` | [devario-development/python-sphinx-alabaster-theme](devario-development/python-sphinx-alabaster-theme/PKGBUILD) | — |
| `python-sphinxcontrib-applehelp` | [devario-development/python-sphinxcontrib-applehelp](devario-development/python-sphinxcontrib-applehelp/PKGBUILD) | — |
| `python-sphinxcontrib-devhelp` | [devario-development/python-sphinxcontrib-devhelp](devario-development/python-sphinxcontrib-devhelp/PKGBUILD) | — |
| `python-sphinxcontrib-htmlhelp` | [devario-development/python-sphinxcontrib-htmlhelp](devario-development/python-sphinxcontrib-htmlhelp/PKGBUILD) | — |
| `python-sphinxcontrib-qthelp` | [devario-development/python-sphinxcontrib-qthelp](devario-development/python-sphinxcontrib-qthelp/PKGBUILD) | — |
| `python-sphinxcontrib-serializinghtml` | [devario-development/python-sphinxcontrib-serializinghtml](devario-development/python-sphinxcontrib-serializinghtml/PKGBUILD) | — |
| `qt5-x11extras` | [devario-libs/qt5-x11extras](devario-libs/qt5-x11extras/PKGBUILD) | — |
| `qt6-3d` | [devario-libs/qt6-3d](devario-libs/qt6-3d/PKGBUILD) | — |
| `qt6-httpserver` | [devario-libs/qt6-httpserver](devario-libs/qt6-httpserver/PKGBUILD) | — |
| `qt6-positioning` | [devario-libs/qt6-positioning](devario-libs/qt6-positioning/PKGBUILD) | — |
| `qt6-quick3d` | [devario-libs/qt6-quick3d](devario-libs/qt6-quick3d/PKGBUILD) | — |
| `qt6-serialbus` | [devario-libs/qt6-serialbus](devario-libs/qt6-serialbus/PKGBUILD) | — |
| `read-edid` | [devario-utilities/read-edid](devario-utilities/read-edid/PKGBUILD) | — |
| `riscv64-linux-gnu-binutils` | [devario-development/riscv64-linux-gnu-binutils](devario-development/riscv64-linux-gnu-binutils/PKGBUILD) | — |
| `rocfft` | [devario-libs/rocfft](devario-libs/rocfft/PKGBUILD) | — |
| `rocm-opencl-runtime` | [devario-libs/rocm-opencl-runtime](devario-libs/rocm-opencl-runtime/PKGBUILD) | — |
| `rocprim` | [devario-libs/rocprim](devario-libs/rocprim/PKGBUILD) | — |
| `rocrand` | [devario-libs/rocrand](devario-libs/rocrand/PKGBUILD) | — |
| `ruby-kramdown-parser-gfm` | [devario-libs/ruby-kramdown-parser-gfm](devario-libs/ruby-kramdown-parser-gfm/PKGBUILD) | — |
| `ruby-nokogiri` | [devario-libs/ruby-nokogiri](devario-libs/ruby-nokogiri/PKGBUILD) | — |
| `sassc` | [devario-development/sassc](devario-development/sassc/PKGBUILD) | — |
| `sbsigntools` | [devario-development/sbsigntools](devario-development/sbsigntools/PKGBUILD) | — |
| `seabios` | [devario-utilities/seabios](devario-utilities/seabios/PKGBUILD) | — |
| `seabios-docs` | [devario-utilities/seabios](devario-utilities/seabios/PKGBUILD) | — |
| `sound-theme-freedesktop` | [devario-libs/sound-theme-freedesktop](devario-libs/sound-theme-freedesktop/PKGBUILD) | — |
| `sz` | [devario-libs/sz](devario-libs/sz/PKGBUILD) | — |
| `taglib` | [devario-libs/taglib](devario-libs/taglib/PKGBUILD) | — |
| `tevent` | [devario-libs/tevent](devario-libs/tevent/PKGBUILD) | — |
| `tk` | [devario-libs/tk](devario-libs/tk/PKGBUILD) | — |
| `unbound` | [devario-development/unbound](devario-development/unbound/PKGBUILD) | Cycle G537 — seed packages required |
| `unicode-emoji` | [devario-libs/unicode-emoji](devario-libs/unicode-emoji/PKGBUILD) | — |
| `vde2` | [devario-utilities/vde2](devario-utilities/vde2/PKGBUILD) | — |
| `wget` | [devario-utilities/wget](devario-utilities/wget/PKGBUILD) | — |
| `xorg-xdpyinfo` | [devario-utilities/xorg-xdpyinfo](devario-utilities/xorg-xdpyinfo/PKGBUILD) | — |
| `xorg-xrandr` | [devario-utilities/xorg-xrandr](devario-utilities/xorg-xrandr/PKGBUILD) | — |
| `yelp-xsl` | [devario-libs/yelp-xsl](devario-libs/yelp-xsl/PKGBUILD) | — |
| `zziplib` | [devario-libs/zziplib](devario-libs/zziplib/PKGBUILD) | — |

### Stage 03

76 packages from 54 recipes.

| Package | Build recipe | Bootstrap requirement |
| --- | --- | --- |
| `alsa-plugins` | [devario-libs/alsa-plugins](devario-libs/alsa-plugins/PKGBUILD) | — |
| `aws-c-io` | [devario-libs/aws-c-io](devario-libs/aws-c-io/PKGBUILD) | — |
| `cgns` | [devario-development/cgns](devario-development/cgns/PKGBUILD) | — |
| `dune` | [devario-development/dune](devario-development/dune/PKGBUILD) | Cycle G423 — seed packages required |
| `efitools` | [devario-utilities/efitools](devario-utilities/efitools/PKGBUILD) | — |
| `hipcub` | [devario-libs/hipcub](devario-libs/hipcub/PKGBUILD) | — |
| `hipfft` | [devario-libs/hipfft](devario-libs/hipfft/PKGBUILD) | — |
| `hiprand` | [devario-libs/hiprand](devario-libs/hiprand/PKGBUILD) | — |
| `ispc` | [devario-development/ispc](devario-development/ispc/PKGBUILD) | — |
| `jdk-openjdk` | [devario-development/jdk-openjdk](devario-development/jdk-openjdk/PKGBUILD) | Seed: `java-environment>=22` |
| `jdk11-openjdk` | [devario-development/java11-openjdk](devario-development/java11-openjdk/PKGBUILD) | Seed: `java-environment=11` |
| `jdk17-openjdk` | [devario-development/java17-openjdk](devario-development/java17-openjdk/PKGBUILD) | Seed: `java-environment=17` |
| `jdk21-openjdk` | [devario-development/java21-openjdk](devario-development/java21-openjdk/PKGBUILD) | Seed: `java-environment=21` |
| `jdk25-openjdk` | [devario-development/java25-openjdk](devario-development/java25-openjdk/PKGBUILD) | Seed: `java-environment=25` |
| `jre-openjdk` | [devario-development/jdk-openjdk](devario-development/jdk-openjdk/PKGBUILD) | Seed: `java-environment>=22` |
| `jre-openjdk-headless` | [devario-development/jdk-openjdk](devario-development/jdk-openjdk/PKGBUILD) | Seed: `java-environment>=22` |
| `jre11-openjdk` | [devario-development/java11-openjdk](devario-development/java11-openjdk/PKGBUILD) | Seed: `java-environment=11` |
| `jre11-openjdk-headless` | [devario-development/java11-openjdk](devario-development/java11-openjdk/PKGBUILD) | Seed: `java-environment=11` |
| `jre17-openjdk` | [devario-development/java17-openjdk](devario-development/java17-openjdk/PKGBUILD) | Seed: `java-environment=17` |
| `jre17-openjdk-headless` | [devario-development/java17-openjdk](devario-development/java17-openjdk/PKGBUILD) | Seed: `java-environment=17` |
| `jre21-openjdk` | [devario-development/java21-openjdk](devario-development/java21-openjdk/PKGBUILD) | Seed: `java-environment=21` |
| `jre21-openjdk-headless` | [devario-development/java21-openjdk](devario-development/java21-openjdk/PKGBUILD) | Seed: `java-environment=21` |
| `jre25-openjdk` | [devario-development/java25-openjdk](devario-development/java25-openjdk/PKGBUILD) | Seed: `java-environment=25` |
| `jre25-openjdk-headless` | [devario-development/java25-openjdk](devario-development/java25-openjdk/PKGBUILD) | Seed: `java-environment=25` |
| `lib32-e2fsprogs` | [devario-libs/lib32-e2fsprogs](devario-libs/lib32-e2fsprogs/PKGBUILD) | — |
| `lib32-libavtp` | [devario-libs/lib32-libavtp](devario-libs/lib32-libavtp/PKGBUILD) | — |
| `lib32-libdrm` | [devario-libs/lib32-libdrm](devario-libs/lib32-libdrm/PKGBUILD) | — |
| `lib32-libxcb` | [devario-libs/lib32-libxcb](devario-libs/lib32-libxcb/PKGBUILD) | — |
| `lib32-libxml2` | [devario-libs/lib32-libxml2](devario-libs/lib32-libxml2/PKGBUILD) | — |
| `lib32-pcre2` | [devario-libs/lib32-pcre2](devario-libs/lib32-pcre2/PKGBUILD) | — |
| `lib32-pixman` | [devario-libs/lib32-pixman](devario-libs/lib32-pixman/PKGBUILD) | — |
| `lib32-sqlite` | [devario-libs/lib32-sqlite](devario-libs/lib32-sqlite/PKGBUILD) | — |
| `libnbd` | [devario-libs/libnbd](devario-libs/libnbd/PKGBUILD) | — |
| `libspatialite` | [devario-libs/libspatialite](devario-libs/libspatialite/PKGBUILD) | — |
| `libxaw` | [devario-libs/libxaw](devario-libs/libxaw/PKGBUILD) | — |
| `mjpegtools` | [devario-development/mjpegtools](devario-development/mjpegtools/PKGBUILD) | — |
| `node-gyp` | [devario-development/node-gyp](devario-development/node-gyp/PKGBUILD) | Cycle G012 — seed packages required |
| `nodejs-nopt` | [devario-libs/nodejs-nopt](devario-libs/nodejs-nopt/PKGBUILD) | Cycle G012 — seed packages required |
| `ocaml-csexp` | [devario-libs/ocaml-csexp](devario-libs/ocaml-csexp/PKGBUILD) | Cycle G423 — seed packages required |
| `ocaml-pp` | [devario-libs/ocaml-pp](devario-libs/ocaml-pp/PKGBUILD) | Cycle G423 — seed packages required |
| `ocaml-re` | [devario-libs/ocaml-re](devario-libs/ocaml-re/PKGBUILD) | Cycle G423 — seed packages required |
| `ocaml-result` | [devario-libs/ocaml-result](devario-libs/ocaml-result/PKGBUILD) | Cycle G423 — seed packages required |
| `openal` | [devario-libs/openal](devario-libs/openal/PKGBUILD) | — |
| `openal-examples` | [devario-libs/openal](devario-libs/openal/PKGBUILD) | — |
| `openjade` | [devario-utilities/openjade](devario-utilities/openjade/PKGBUILD) | — |
| `openjdk-doc` | [devario-development/jdk-openjdk](devario-development/jdk-openjdk/PKGBUILD) | Seed: `java-environment>=22` |
| `openjdk-src` | [devario-development/jdk-openjdk](devario-development/jdk-openjdk/PKGBUILD) | Seed: `java-environment>=22` |
| `openjdk11-doc` | [devario-development/java11-openjdk](devario-development/java11-openjdk/PKGBUILD) | Seed: `java-environment=11` |
| `openjdk11-src` | [devario-development/java11-openjdk](devario-development/java11-openjdk/PKGBUILD) | Seed: `java-environment=11` |
| `openjdk17-doc` | [devario-development/java17-openjdk](devario-development/java17-openjdk/PKGBUILD) | Seed: `java-environment=17` |
| `openjdk17-src` | [devario-development/java17-openjdk](devario-development/java17-openjdk/PKGBUILD) | Seed: `java-environment=17` |
| `openjdk21-doc` | [devario-development/java21-openjdk](devario-development/java21-openjdk/PKGBUILD) | Seed: `java-environment=21` |
| `openjdk21-src` | [devario-development/java21-openjdk](devario-development/java21-openjdk/PKGBUILD) | Seed: `java-environment=21` |
| `openjdk25-doc` | [devario-development/java25-openjdk](devario-development/java25-openjdk/PKGBUILD) | Seed: `java-environment=25` |
| `openjdk25-src` | [devario-development/java25-openjdk](devario-development/java25-openjdk/PKGBUILD) | Seed: `java-environment=25` |
| `perl-sub-exporter` | [devario-libs/perl-sub-exporter](devario-libs/perl-sub-exporter/PKGBUILD) | — |
| `po4a` | [devario-development/po4a](devario-development/po4a/PKGBUILD) | — |
| `pulseaudio-alsa` | [devario-libs/alsa-plugins](devario-libs/alsa-plugins/PKGBUILD) | — |
| `python-jaraco.text` | [devario-core/python-jaraco.text](devario-core/python-jaraco.text/PKGBUILD) | — |
| `python-markdown-it-py` | [devario-libs/python-markdown-it-py](devario-libs/python-markdown-it-py/PKGBUILD) | — |
| `qt5pas` | [devario-libs/qt5pas](devario-libs/qt5pas/PKGBUILD) | — |
| `qt6-graphs` | [devario-libs/qt6-graphs](devario-libs/qt6-graphs/PKGBUILD) | — |
| `qt6-location` | [devario-libs/qt6-location](devario-libs/qt6-location/PKGBUILD) | — |
| `qwen-code-bin` | [devario-development/qwen-code-bin](devario-development/qwen-code-bin/PKGBUILD) | — |
| `riscv64-linux-gnu-gcc` | [devario-development/riscv64-linux-gnu-gcc](devario-development/riscv64-linux-gnu-gcc/PKGBUILD) | Cycle G512 — seed packages required |
| `riscv64-linux-gnu-glibc` | [devario-libs/riscv64-linux-gnu-glibc](devario-libs/riscv64-linux-gnu-glibc/PKGBUILD) | Cycle G512 — seed packages required |
| `rocthrust` | [devario-libs/rocthrust](devario-libs/rocthrust/PKGBUILD) | — |
| `ruby-ronn-ng` | [devario-libs/ruby-ronn-ng](devario-libs/ruby-ronn-ng/PKGBUILD) | — |
| `semver` | [devario-libs/semver](devario-libs/semver/PKGBUILD) | Cycle G012 — seed packages required |
| `spice` | [devario-libs/spice](devario-libs/spice/PKGBUILD) | — |
| `xclip` | [devario-utilities/xclip](devario-utilities/xclip/PKGBUILD) | — |
| `xorg-xauth` | [devario-development/xorg-xauth](devario-development/xorg-xauth/PKGBUILD) | — |
| `xorg-xeyes` | [devario-utilities/xorg-xeyes](devario-utilities/xorg-xeyes/PKGBUILD) | — |
| `xorg-xinput` | [devario-utilities/xorg-xinput](devario-utilities/xorg-xinput/PKGBUILD) | — |
| `xorg-xkill` | [devario-utilities/xorg-xkill](devario-utilities/xorg-xkill/PKGBUILD) | — |
| `yarn` | [devario-development/yarn](devario-development/yarn/PKGBUILD) | Seed: `yarn` |

### Stage 04

34 packages from 29 recipes.

| Package | Build recipe | Bootstrap requirement |
| --- | --- | --- |
| `aws-c-event-stream` | [devario-libs/aws-c-event-stream](devario-libs/aws-c-event-stream/PKGBUILD) | — |
| `aws-c-http` | [devario-libs/aws-c-http](devario-libs/aws-c-http/PKGBUILD) | — |
| `cline-cli` | [devario-development/cline-cli](devario-development/cline-cli/PKGBUILD) | — |
| `docbook-utils` | [devario-development/docbook-utils](devario-development/docbook-utils/PKGBUILD) | — |
| `embree` | [devario-libs/embree](devario-libs/embree/PKGBUILD) | — |
| `espeak-ng` | [devario-utilities/espeak-ng](devario-utilities/espeak-ng/PKGBUILD) | — |
| `git-lfs` | [devario-development/git-lfs](devario-development/git-lfs/PKGBUILD) | — |
| `groovy` | [devario-development/groovy](devario-development/groovy/PKGBUILD) | — |
| `lazarus` | [devario-development/lazarus](devario-development/lazarus/PKGBUILD) | — |
| `lazarus-qt5` | [devario-development/lazarus](devario-development/lazarus/PKGBUILD) | — |
| `lazarus-qt6` | [devario-development/lazarus](devario-development/lazarus/PKGBUILD) | — |
| `lib32-keyutils` | [devario-libs/lib32-keyutils](devario-libs/lib32-keyutils/PKGBUILD) | Cycle G672 — seed packages required |
| `lib32-krb5` | [devario-libs/lib32-krb5](devario-libs/lib32-krb5/PKGBUILD) | Cycle G672 — seed packages required |
| `lib32-libx11` | [devario-libs/lib32-libx11](devario-libs/lib32-libx11/PKGBUILD) | — |
| `lib32-llvm` | [devario-libs/lib32-llvm](devario-libs/lib32-llvm/PKGBUILD) | — |
| `lib32-llvm-libs` | [devario-libs/lib32-llvm](devario-libs/lib32-llvm/PKGBUILD) | — |
| `lib32-wayland` | [devario-libs/lib32-wayland](devario-libs/lib32-wayland/PKGBUILD) | — |
| `lib32-xcb-util-keysyms` | [devario-libs/lib32-xcb-util-keysyms](devario-libs/lib32-xcb-util-keysyms/PKGBUILD) | — |
| `lib32-xz` | [devario-libs/lib32-xz](devario-libs/lib32-xz/PKGBUILD) | — |
| `libvirt` | [devario-libs/libvirt](devario-libs/libvirt/PKGBUILD) | — |
| `libvirt-storage-gluster` | [devario-libs/libvirt](devario-libs/libvirt/PKGBUILD) | — |
| `libvirt-storage-iscsi-direct` | [devario-libs/libvirt](devario-libs/libvirt/PKGBUILD) | — |
| `marked` | [devario-libs/marked](devario-libs/marked/PKGBUILD) | — |
| `mpv` | [devario-entertainment/mpv](devario-entertainment/mpv/PKGBUILD) | — |
| `ocaml-bigarray-compat` | [devario-libs/ocaml-bigarray-compat](devario-libs/ocaml-bigarray-compat/PKGBUILD) | — |
| `ocaml-stdlib-shims` | [devario-libs/ocaml-stdlib-shims](devario-libs/ocaml-stdlib-shims/PKGBUILD) | — |
| `ocaml-topkg` | [devario-libs/ocaml-topkg](devario-libs/ocaml-topkg/PKGBUILD) | — |
| `openimagedenoise` | [devario-libs/openimagedenoise](devario-libs/openimagedenoise/PKGBUILD) | — |
| `perl-sub-prototype` | [devario-libs/perl-sub-prototype](devario-libs/perl-sub-prototype/PKGBUILD) | — |
| `pnpm` | [devario-development/pnpm](devario-development/pnpm/PKGBUILD) | Seed: `pnpm` |
| `python-jaraco.collections` | [devario-core/python-jaraco.collections](devario-core/python-jaraco.collections/PKGBUILD) | — |
| `python-mdit_py_plugins` | [devario-libs/python-mdit_py_plugins](devario-libs/python-mdit_py_plugins/PKGBUILD) | — |
| `python-rich` | [devario-libs/python-rich](devario-libs/python-rich/PKGBUILD) | — |
| `typescript` | [devario-development/typescript](devario-development/typescript/PKGBUILD) | — |

### Stage 05

96 packages from 92 recipes.

| Package | Build recipe | Bootstrap requirement |
| --- | --- | --- |
| `asciidoc` | [devario-development/asciidoc](devario-development/asciidoc/PKGBUILD) | — |
| `aws-c-auth` | [devario-libs/aws-c-auth](devario-libs/aws-c-auth/PKGBUILD) | — |
| `aws-c-mqtt` | [devario-libs/aws-c-mqtt](devario-libs/aws-c-mqtt/PKGBUILD) | — |
| `capstone` | [devario-libs/capstone](devario-libs/capstone/PKGBUILD) | — |
| `conduit-llnl` | [devario-libs/conduit-llnl](devario-libs/conduit-llnl/PKGBUILD) | — |
| `dtc` | [devario-utilities/dtc](devario-utilities/dtc/PKGBUILD) | — |
| `flatbuffers` | [devario-libs/flatbuffers](devario-libs/flatbuffers/PKGBUILD) | — |
| `ghostscript` | [devario-utilities/ghostscript](devario-utilities/ghostscript/PKGBUILD) | Cycle G039 — seed packages required |
| `github-desktop` | [devario-development/github-desktop](devario-development/github-desktop/PKGBUILD) | — |
| `gyp` | [devario-development/gyp](devario-development/gyp/PKGBUILD) | — |
| `i2c-tools` | [devario-utilities/i2c-tools](devario-utilities/i2c-tools/PKGBUILD) | — |
| `ijs` | [devario-libs/ijs](devario-libs/ijs/PKGBUILD) | Cycle G039 — seed packages required |
| `lib32-clang` | [devario-libs/lib32-clang](devario-libs/lib32-clang/PKGBUILD) | — |
| `lib32-libxext` | [devario-libs/lib32-libxext](devario-libs/lib32-libxext/PKGBUILD) | — |
| `lib32-libxfixes` | [devario-libs/lib32-libxfixes](devario-libs/lib32-libxfixes/PKGBUILD) | — |
| `lib32-libxrender` | [devario-libs/lib32-libxrender](devario-libs/lib32-libxrender/PKGBUILD) | — |
| `lib32-spirv-llvm-translator` | [devario-libs/lib32-spirv-llvm-translator](devario-libs/lib32-spirv-llvm-translator/PKGBUILD) | — |
| `liblouis` | [devario-libs/liblouis](devario-libs/liblouis/PKGBUILD) | — |
| `libspeechd` | [devario-utilities/speech-dispatcher](devario-utilities/speech-dispatcher/PKGBUILD) | — |
| `libvirt-python` | [devario-libs/libvirt-python](devario-libs/libvirt-python/PKGBUILD) | — |
| `mallard-ducktype` | [devario-development/mallard-ducktype](devario-development/mallard-ducktype/PKGBUILD) | — |
| `marked-man` | [devario-development/marked-man](devario-development/marked-man/PKGBUILD) | — |
| `mercurial` | [devario-development/mercurial](devario-development/mercurial/PKGBUILD) | — |
| `net-snmp` | [devario-utilities/net-snmp](devario-utilities/net-snmp/PKGBUILD) | — |
| `ocaml-integers` | [devario-libs/ocaml-integers](devario-libs/ocaml-integers/PKGBUILD) | — |
| `perl-sub-override` | [devario-libs/perl-sub-override](devario-libs/perl-sub-override/PKGBUILD) | — |
| `python-accessible-pygments` | [devario-libs/python-accessible-pygments](devario-libs/python-accessible-pygments/PKGBUILD) | — |
| `python-appdirs` | [devario-libs/python-appdirs](devario-libs/python-appdirs/PKGBUILD) | — |
| `python-argcomplete` | [devario-libs/python-argcomplete](devario-libs/python-argcomplete/PKGBUILD) | — |
| `python-attrs` | [devario-core/python-attrs](devario-core/python-attrs/PKGBUILD) | — |
| `python-cachetools` | [devario-libs/python-cachetools](devario-libs/python-cachetools/PKGBUILD) | — |
| `python-capstone` | [devario-libs/capstone](devario-libs/capstone/PKGBUILD) | — |
| `python-certifi` | [devario-libs/python-certifi](devario-libs/python-certifi/PKGBUILD) | — |
| `python-cppy` | [devario-libs/python-cppy](devario-libs/python-cppy/PKGBUILD) | — |
| `python-cycler` | [devario-libs/python-cycler](devario-libs/python-cycler/PKGBUILD) | — |
| `python-dbusmock` | [devario-development/python-dbusmock](devario-development/python-dbusmock/PKGBUILD) | — |
| `python-distlib` | [devario-libs/python-distlib](devario-libs/python-distlib/PKGBUILD) | — |
| `python-evdev` | [devario-libs/python-evdev](devario-libs/python-evdev/PKGBUILD) | — |
| `python-filelock` | [devario-libs/python-filelock](devario-libs/python-filelock/PKGBUILD) | — |
| `python-flatbuffers` | [devario-libs/flatbuffers](devario-libs/flatbuffers/PKGBUILD) | — |
| `python-fonttools` | [devario-libs/python-fonttools](devario-libs/python-fonttools/PKGBUILD) | — |
| `python-fsspec` | [devario-libs/python-fsspec](devario-libs/python-fsspec/PKGBUILD) | — |
| `python-gast` | [devario-libs/python-gast](devario-libs/python-gast/PKGBUILD) | — |
| `python-gmpy2` | [devario-libs/python-gmpy2](devario-libs/python-gmpy2/PKGBUILD) | — |
| `python-greenlet` | [devario-libs/python-greenlet](devario-libs/python-greenlet/PKGBUILD) | — |
| `python-h11` | [devario-libs/python-h11](devario-libs/python-h11/PKGBUILD) | — |
| `python-httplib2` | [devario-libs/python-httplib2](devario-libs/python-httplib2/PKGBUILD) | — |
| `python-imagesize` | [devario-libs/python-imagesize](devario-libs/python-imagesize/PKGBUILD) | — |
| `python-iniconfig` | [devario-libs/python-iniconfig](devario-libs/python-iniconfig/PKGBUILD) | — |
| `python-inputs` | [devario-libs/python-inputs](devario-libs/python-inputs/PKGBUILD) | — |
| `python-joblib` | [devario-libs/python-joblib](devario-libs/python-joblib/PKGBUILD) | — |
| `python-librt` | [devario-libs/python-librt](devario-libs/python-librt/PKGBUILD) | — |
| `python-magic` | [devario-libs/python-magic](devario-libs/python-magic/PKGBUILD) | — |
| `python-markdown` | [devario-libs/python-markdown](devario-libs/python-markdown/PKGBUILD) | — |
| `python-markupsafe` | [devario-libs/python-markupsafe](devario-libs/python-markupsafe/PKGBUILD) | — |
| `python-mpi4py` | [devario-libs/python-mpi4py](devario-libs/python-mpi4py/PKGBUILD) | — |
| `python-msgpack` | [devario-libs/python-msgpack](devario-libs/python-msgpack/PKGBUILD) | — |
| `python-nodeenv` | [devario-libs/python-nodeenv](devario-libs/python-nodeenv/PKGBUILD) | — |
| `python-pefile` | [devario-libs/python-pefile](devario-libs/python-pefile/PKGBUILD) | — |
| `python-py3c` | [devario-libs/python-py3c](devario-libs/python-py3c/PKGBUILD) | — |
| `python-pyclipper` | [devario-libs/python-pyclipper](devario-libs/python-pyclipper/PKGBUILD) | — |
| `python-pycparser` | [devario-libs/python-pycparser](devario-libs/python-pycparser/PKGBUILD) | — |
| `python-pycryptodomex` | [devario-libs/python-pycryptodomex](devario-libs/python-pycryptodomex/PKGBUILD) | — |
| `python-pytz` | [devario-libs/python-pytz](devario-libs/python-pytz/PKGBUILD) | — |
| `python-pyzstd` | [devario-libs/python-pyzstd](devario-libs/python-pyzstd/PKGBUILD) | — |
| `python-scikit-build-core` | [devario-libs/python-scikit-build-core](devario-libs/python-scikit-build-core/PKGBUILD) | — |
| `python-semantic-version` | [devario-libs/python-semantic-version](devario-libs/python-semantic-version/PKGBUILD) | — |
| `python-setuptools-reproducible` | [devario-development/python-setuptools-reproducible](devario-development/python-setuptools-reproducible/PKGBUILD) | — |
| `python-simplejson` | [devario-libs/python-simplejson](devario-libs/python-simplejson/PKGBUILD) | — |
| `python-six` | [devario-libs/python-six](devario-libs/python-six/PKGBUILD) | — |
| `python-smartypants` | [devario-libs/python-smartypants](devario-libs/python-smartypants/PKGBUILD) | — |
| `python-snowballstemmer` | [devario-libs/python-snowballstemmer](devario-libs/python-snowballstemmer/PKGBUILD) | — |
| `python-sphinxcontrib-jsmath` | [devario-development/python-sphinxcontrib-jsmath](devario-development/python-sphinxcontrib-jsmath/PKGBUILD) | — |
| `python-text-unidecode` | [devario-libs/python-text-unidecode](devario-libs/python-text-unidecode/PKGBUILD) | — |
| `python-thrift` | [devario-libs/thrift](devario-libs/thrift/PKGBUILD) | — |
| `python-toml` | [devario-libs/python-toml](devario-libs/python-toml/PKGBUILD) | — |
| `python-ufonormalizer` | [devario-libs/python-ufonormalizer](devario-libs/python-ufonormalizer/PKGBUILD) | — |
| `python-ujson` | [devario-libs/python-ujson](devario-libs/python-ujson/PKGBUILD) | — |
| `python-unicodedata2` | [devario-libs/python-unicodedata2](devario-libs/python-unicodedata2/PKGBUILD) | — |
| `python-urllib3` | [devario-libs/python-urllib3](devario-libs/python-urllib3/PKGBUILD) | — |
| `python-vdf` | [devario-libs/python-vdf](devario-libs/python-vdf/PKGBUILD) | — |
| `python-versioneer` | [devario-libs/python-versioneer](devario-libs/python-versioneer/PKGBUILD) | — |
| `python-webencodings` | [devario-libs/python-webencodings](devario-libs/python-webencodings/PKGBUILD) | — |
| `python-xxhash` | [devario-libs/python-xxhash](devario-libs/python-xxhash/PKGBUILD) | — |
| `python-zope-event` | [devario-libs/python-zope-event](devario-libs/python-zope-event/PKGBUILD) | — |
| `python-zope-interface` | [devario-libs/python-zope-interface](devario-libs/python-zope-interface/PKGBUILD) | — |
| `python-zopfli` | [devario-libs/python-zopfli](devario-libs/python-zopfli/PKGBUILD) | — |
| `python-zstandard` | [devario-libs/python-zstandard](devario-libs/python-zstandard/PKGBUILD) | — |
| `reflector` | [devario-utilities/reflector](devario-utilities/reflector/PKGBUILD) | — |
| `scons` | [devario-development/scons](devario-development/scons/PKGBUILD) | — |
| `speech-dispatcher` | [devario-utilities/speech-dispatcher](devario-utilities/speech-dispatcher/PKGBUILD) | — |
| `thrift` | [devario-libs/thrift](devario-libs/thrift/PKGBUILD) | — |
| `ufw` | [devario-core/ufw](devario-core/ufw/PKGBUILD) | — |
| `vesktop` | [devario-gaming/vesktop](devario-gaming/vesktop/PKGBUILD) | — |
| `vkbasalt-cli` | [devario-gaming/vkbasalt-cli](devario-gaming/vkbasalt-cli/PKGBUILD) | — |
| `zfp` | [devario-libs/zfp](devario-libs/zfp/PKGBUILD) | — |

### Stage 06

50 packages from 44 recipes.

| Package | Build recipe | Bootstrap requirement |
| --- | --- | --- |
| `aws-c-s3` | [devario-libs/aws-c-s3](devario-libs/aws-c-s3/PKGBUILD) | — |
| `blosc2` | [devario-libs/blosc2](devario-libs/blosc2/PKGBUILD) | — |
| `cifs-utils` | [devario-utilities/cifs-utils](devario-utilities/cifs-utils/PKGBUILD) | Cycle G650 — seed packages required |
| `colm` | [devario-development/colm](devario-development/colm/PKGBUILD) | — |
| `gradle` | [devario-development/gradle](devario-development/gradle/PKGBUILD) | — |
| `gradle-doc` | [devario-development/gradle](devario-development/gradle/PKGBUILD) | — |
| `gradle-src` | [devario-development/gradle](devario-development/gradle/PKGBUILD) | — |
| `ldb` | [devario-utilities/samba](devario-utilities/samba/PKGBUILD) | Cycle G650 — seed packages required |
| `lib32-libxinerama` | [devario-libs/lib32-libxinerama](devario-libs/lib32-libxinerama/PKGBUILD) | — |
| `lib32-libxrandr` | [devario-libs/lib32-libxrandr](devario-libs/lib32-libxrandr/PKGBUILD) | — |
| `lib32-libxss` | [devario-libs/lib32-libxss](devario-libs/lib32-libxss/PKGBUILD) | — |
| `lib32-libxxf86vm` | [devario-libs/lib32-libxxf86vm](devario-libs/lib32-libxxf86vm/PKGBUILD) | — |
| `lib32-nss` | [devario-libs/lib32-nss](devario-libs/lib32-nss/PKGBUILD) | — |
| `libspectre` | [devario-libs/libspectre](devario-libs/libspectre/PKGBUILD) | — |
| `libtraceevent` | [devario-libs/libtraceevent](devario-libs/libtraceevent/PKGBUILD) | — |
| `libtraceevent-docs` | [devario-libs/libtraceevent](devario-libs/libtraceevent/PKGBUILD) | — |
| `libwbclient` | [devario-utilities/samba](devario-utilities/samba/PKGBUILD) | Cycle G650 — seed packages required |
| `nanobind` | [devario-libs/nanobind](devario-libs/nanobind/PKGBUILD) | — |
| `nasm` | [devario-development/nasm](devario-development/nasm/PKGBUILD) | — |
| `ocaml-ctypes` | [devario-libs/ocaml-ctypes](devario-libs/ocaml-ctypes/PKGBUILD) | — |
| `paraview-catalyst` | [devario-libs/paraview-catalyst](devario-libs/paraview-catalyst/PKGBUILD) | — |
| `pastebinit` | [devario-utilities/pastebinit](devario-utilities/pastebinit/PKGBUILD) | — |
| `patool` | [devario-utilities/patool](devario-utilities/patool/PKGBUILD) | — |
| `python-babel` | [devario-libs/python-babel](devario-libs/python-babel/PKGBUILD) | — |
| `python-beniget` | [devario-libs/python-beniget](devario-libs/python-beniget/PKGBUILD) | — |
| `python-booleanoperations` | [devario-libs/python-booleanoperations](devario-libs/python-booleanoperations/PKGBUILD) | — |
| `python-cffi` | [devario-libs/python-cffi](devario-libs/python-cffi/PKGBUILD) | — |
| `python-dateutil` | [devario-libs/python-dateutil](devario-libs/python-dateutil/PKGBUILD) | — |
| `python-fontmath` | [devario-libs/python-fontmath](devario-libs/python-fontmath/PKGBUILD) | — |
| `python-fontpens` | [devario-libs/python-fontpens](devario-libs/python-fontpens/PKGBUILD) | — |
| `python-fs` | [devario-libs/python-fs](devario-libs/python-fs/PKGBUILD) | — |
| `python-html5lib` | [devario-libs/python-html5lib](devario-libs/python-html5lib/PKGBUILD) | — |
| `python-jinja` | [devario-libs/python-jinja](devario-libs/python-jinja/PKGBUILD) | — |
| `python-kiwisolver` | [devario-libs/python-kiwisolver](devario-libs/python-kiwisolver/PKGBUILD) | — |
| `python-mako` | [devario-libs/python-mako](devario-libs/python-mako/PKGBUILD) | — |
| `python-mpmath` | [devario-libs/python-mpmath](devario-libs/python-mpmath/PKGBUILD) | — |
| `python-pytest` | [devario-development/python-pytest](devario-development/python-pytest/PKGBUILD) | — |
| `python-python-discovery` | [devario-libs/python-python-discovery](devario-libs/python-python-discovery/PKGBUILD) | — |
| `python-setuptools-rust` | [devario-development/python-setuptools-rust](devario-development/python-setuptools-rust/PKGBUILD) | — |
| `python-slugify` | [devario-libs/python-slugify](devario-libs/python-slugify/PKGBUILD) | — |
| `python-sphinx-theme-builder` | [devario-development/python-sphinx-theme-builder](devario-development/python-sphinx-theme-builder/PKGBUILD) | — |
| `python-tensile` | [devario-libs/python-tensile](devario-libs/python-tensile/PKGBUILD) | — |
| `python-typogrify` | [devario-libs/python-typogrify](devario-libs/python-typogrify/PKGBUILD) | — |
| `python-wsproto` | [devario-libs/python-wsproto](devario-libs/python-wsproto/PKGBUILD) | — |
| `python-xlib` | [devario-libs/python-xlib](devario-libs/python-xlib/PKGBUILD) | — |
| `rebuild-detector` | [devario-development/rebuild-detector](devario-development/rebuild-detector/PKGBUILD) | — |
| `samba` | [devario-utilities/samba](devario-utilities/samba/PKGBUILD) | Cycle G650 — seed packages required |
| `serf` | [devario-libs/serf](devario-libs/serf/PKGBUILD) | — |
| `smbclient` | [devario-utilities/samba](devario-utilities/samba/PKGBUILD) | Cycle G650 — seed packages required |
| `strip-nondeterminism` | [devario-development/strip-nondeterminism](devario-development/strip-nondeterminism/PKGBUILD) | — |

### Stage 07

48 packages from 26 recipes.

| Package | Build recipe | Bootstrap requirement |
| --- | --- | --- |
| `adios2` | [devario-development/adios2](devario-development/adios2/PKGBUILD) | — |
| `aws-crt-cpp` | [devario-libs/aws-crt-cpp](devario-libs/aws-crt-cpp/PKGBUILD) | — |
| `bootconfig` | [devario-utilities/linux-tools](devario-utilities/linux-tools/PKGBUILD) | — |
| `bpf` | [devario-utilities/linux-tools](devario-utilities/linux-tools/PKGBUILD) | — |
| `brltty` | [devario-utilities/brltty](devario-utilities/brltty/PKGBUILD) | — |
| `brltty-udev-generic` | [devario-utilities/brltty](devario-utilities/brltty/PKGBUILD) | — |
| `bun` | [devario-development/bun](devario-development/bun/PKGBUILD) | — |
| `cpupower` | [devario-utilities/linux-tools](devario-utilities/linux-tools/PKGBUILD) | — |
| `dracut-brltty` | [devario-utilities/brltty](devario-utilities/brltty/PKGBUILD) | — |
| `edk2-aarch64` | [devario-utilities/edk2](devario-utilities/edk2/PKGBUILD) | — |
| `edk2-ovmf` | [devario-utilities/edk2](devario-utilities/edk2/PKGBUILD) | — |
| `edk2-riscv64` | [devario-utilities/edk2](devario-utilities/edk2/PKGBUILD) | — |
| `edk2-shell` | [devario-utilities/edk2](devario-utilities/edk2/PKGBUILD) | — |
| `gi-docgen` | [devario-libs/gi-docgen](devario-libs/gi-docgen/PKGBUILD) | — |
| `gjs` | [devario-libs/gjs](devario-libs/gjs/PKGBUILD) | — |
| `hyperv` | [devario-utilities/linux-tools](devario-utilities/linux-tools/PKGBUILD) | — |
| `intel-speed-select` | [devario-utilities/linux-tools](devario-utilities/linux-tools/PKGBUILD) | — |
| `java-brltty` | [devario-utilities/brltty](devario-utilities/brltty/PKGBUILD) | — |
| `java-hamcrest` | [devario-libs/java-hamcrest](devario-libs/java-hamcrest/PKGBUILD) | — |
| `kcpuid` | [devario-utilities/linux-tools](devario-utilities/linux-tools/PKGBUILD) | — |
| `lib32-flac` | [devario-libs/lib32-flac](devario-libs/lib32-flac/PKGBUILD) | — |
| `libavif` | [devario-libs/libavif](devario-libs/libavif/PKGBUILD) | — |
| `libtracefs` | [devario-libs/libtracefs](devario-libs/libtracefs/PKGBUILD) | — |
| `libtracefs-docs` | [devario-libs/libtracefs](devario-libs/libtracefs/PKGBUILD) | — |
| `linux-tools-meta` | [devario-utilities/linux-tools](devario-utilities/linux-tools/PKGBUILD) | — |
| `maturin` | [devario-core/maturin](devario-core/maturin/PKGBUILD) | — |
| `ocaml-brltty` | [devario-utilities/brltty](devario-utilities/brltty/PKGBUILD) | — |
| `openh264` | [devario-libs/openh264](devario-libs/openh264/PKGBUILD) | — |
| `openvdb` | [devario-libs/openvdb](devario-libs/openvdb/PKGBUILD) | — |
| `perf` | [devario-utilities/linux-tools](devario-utilities/linux-tools/PKGBUILD) | — |
| `pybind11` | [devario-libs/pybind11](devario-libs/pybind11/PKGBUILD) | — |
| `python-brltty` | [devario-utilities/brltty](devario-utilities/brltty/PKGBUILD) | — |
| `python-cbor2` | [devario-libs/python-cbor2](devario-libs/python-cbor2/PKGBUILD) | — |
| `python-defcon` | [devario-libs/python-defcon](devario-libs/python-defcon/PKGBUILD) | — |
| `python-gevent` | [devario-libs/python-gevent](devario-libs/python-gevent/PKGBUILD) | — |
| `python-libcst` | [devario-libs/python-libcst](devario-libs/python-libcst/PKGBUILD) | — |
| `python-maturin` | [devario-core/maturin](devario-core/maturin/PKGBUILD) | — |
| `python-pandas` | [devario-libs/python-pandas](devario-libs/python-pandas/PKGBUILD) | — |
| `python-pytest-playwright` | [devario-development/python-pytest-playwright](devario-development/python-pytest-playwright/PKGBUILD) | — |
| `python-pythran` | [devario-libs/python-pythran](devario-libs/python-pythran/PKGBUILD) | — |
| `python-sympy` | [devario-libs/python-sympy](devario-libs/python-sympy/PKGBUILD) | — |
| `subversion` | [devario-development/subversion](devario-development/subversion/PKGBUILD) | — |
| `tcl-brltty` | [devario-utilities/brltty](devario-utilities/brltty/PKGBUILD) | — |
| `tmon` | [devario-utilities/linux-tools](devario-utilities/linux-tools/PKGBUILD) | — |
| `towncrier` | [devario-development/towncrier](devario-development/towncrier/PKGBUILD) | — |
| `turbostat` | [devario-utilities/linux-tools](devario-utilities/linux-tools/PKGBUILD) | — |
| `usbip` | [devario-utilities/linux-tools](devario-utilities/linux-tools/PKGBUILD) | — |
| `x86_energy_perf_policy` | [devario-utilities/linux-tools](devario-utilities/linux-tools/PKGBUILD) | — |

### Stage 08

29 packages from 19 recipes.

| Package | Build recipe | Bootstrap requirement |
| --- | --- | --- |
| `aws-sdk-cpp` | [devario-libs/aws-sdk-cpp](devario-libs/aws-sdk-cpp/PKGBUILD) | — |
| `aws-sdk-cpp-core` | [devario-libs/aws-sdk-cpp](devario-libs/aws-sdk-cpp/PKGBUILD) | — |
| `aws-sdk-cpp-ec2` | [devario-libs/aws-sdk-cpp](devario-libs/aws-sdk-cpp/PKGBUILD) | — |
| `aws-sdk-cpp-firehose` | [devario-libs/aws-sdk-cpp](devario-libs/aws-sdk-cpp/PKGBUILD) | — |
| `aws-sdk-cpp-iam` | [devario-libs/aws-sdk-cpp](devario-libs/aws-sdk-cpp/PKGBUILD) | — |
| `aws-sdk-cpp-kinesis` | [devario-libs/aws-sdk-cpp](devario-libs/aws-sdk-cpp/PKGBUILD) | — |
| `aws-sdk-cpp-s3` | [devario-libs/aws-sdk-cpp](devario-libs/aws-sdk-cpp/PKGBUILD) | — |
| `cudnn-frontend` | [devario-libs/cudnn-frontend](devario-libs/cudnn-frontend/PKGBUILD) | — |
| `junit` | [devario-libs/junit](devario-libs/junit/PKGBUILD) | — |
| `lib32-libsndfile` | [devario-libs/lib32-libsndfile](devario-libs/lib32-libsndfile/PKGBUILD) | — |
| `libheif` | [devario-libs/libheif](devario-libs/libheif/PKGBUILD) | — |
| `libxdp` | [devario-utilities/xdp-tools](devario-utilities/xdp-tools/PKGBUILD) | — |
| `ndctl` | [devario-libs/ndctl](devario-libs/ndctl/PKGBUILD) | — |
| `netpbm` | [devario-utilities/netpbm](devario-utilities/netpbm/PKGBUILD) | — |
| `opencode` | [devario-development/opencode](devario-development/opencode/PKGBUILD) | — |
| `openvkl` | [devario-libs/openvkl](devario-libs/openvkl/PKGBUILD) | — |
| `powertop` | [devario-utilities/powertop](devario-utilities/powertop/PKGBUILD) | — |
| `python-ast-serialize` | [devario-libs/python-ast-serialize](devario-libs/python-ast-serialize/PKGBUILD) | — |
| `python-contourpy` | [devario-libs/python-contourpy](devario-libs/python-contourpy/PKGBUILD) | — |
| `python-cryptography` | [devario-libs/python-cryptography](devario-libs/python-cryptography/PKGBUILD) | — |
| `python-cudnn-frontend` | [devario-libs/cudnn-frontend](devario-libs/cudnn-frontend/PKGBUILD) | — |
| `python-mutatormath` | [devario-libs/python-mutatormath](devario-libs/python-mutatormath/PKGBUILD) | — |
| `python-orjson` | [devario-libs/python-orjson](devario-libs/python-orjson/PKGBUILD) | — |
| `python-uv` | [devario-development/uv](devario-development/uv/PKGBUILD) | — |
| `python-uv-build` | [devario-development/uv](devario-development/uv/PKGBUILD) | — |
| `qt6-webengine` | [devario-libs/qt6-webengine](devario-libs/qt6-webengine/PKGBUILD) | — |
| `sdl2_image` | [devario-libs/sdl2_image](devario-libs/sdl2_image/PKGBUILD) | — |
| `uv` | [devario-development/uv](devario-development/uv/PKGBUILD) | — |
| `xdp-tools` | [devario-utilities/xdp-tools](devario-utilities/xdp-tools/PKGBUILD) | — |

### Stage 09

11 packages from 9 recipes.

| Package | Build recipe | Bootstrap requirement |
| --- | --- | --- |
| `ant` | [devario-development/ant](devario-development/ant/PKGBUILD) | — |
| `ant-doc` | [devario-development/ant](devario-development/ant/PKGBUILD) | — |
| `fig2dev` | [devario-development/fig2dev](devario-development/fig2dev/PKGBUILD) | — |
| `gd` | [devario-libs/gd](devario-libs/gd/PKGBUILD) | — |
| `hspell` | [devario-development/hspell](devario-development/hspell/PKGBUILD) | — |
| `hunspell-he` | [devario-development/hspell](devario-development/hspell/PKGBUILD) | — |
| `imlib2` | [devario-libs/imlib2](devario-libs/imlib2/PKGBUILD) | — |
| `lib32-libsamplerate` | [devario-libs/lib32-libsamplerate](devario-libs/lib32-libsamplerate/PKGBUILD) | — |
| `mypy` | [devario-development/mypy](devario-development/mypy/PKGBUILD) | — |
| `ospray` | [devario-development/ospray](devario-development/ospray/PKGBUILD) | — |
| `qt6-webview` | [devario-libs/qt6-webview](devario-libs/qt6-webview/PKGBUILD) | — |

### Stage 10

40 packages from 7 recipes.

| Package | Build recipe | Bootstrap requirement |
| --- | --- | --- |
| `libcaca` | [devario-libs/libcaca](devario-libs/libcaca/PKGBUILD) | — |
| `libgphoto2` | [devario-libs/libgphoto2](devario-libs/libgphoto2/PKGBUILD) | — |
| `libgphoto2-docs` | [devario-libs/libgphoto2](devario-libs/libgphoto2/PKGBUILD) | — |
| `libsynctex` | [devario-utilities/texlive-bin](devario-utilities/texlive-bin/PKGBUILD) | — |
| `php` | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `php-apache` | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `php-cgi` | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `php-dblib` | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `php-embed` | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `php-enchant` | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `php-fpm` | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `php-gd` | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `php-legacy` | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-apache` | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-cgi` | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-dblib` | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-embed` | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-enchant` | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-fpm` | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-gd` | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-odbc` | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-pgsql` | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-phpdbg` | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-pspell` | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-snmp` | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-sodium` | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-sqlite` | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-tidy` | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-legacy-xsl` | [devario-development/php-legacy](devario-development/php-legacy/PKGBUILD) | — |
| `php-odbc` | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `php-pgsql` | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `php-phpdbg` | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `php-snmp` | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `php-sodium` | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `php-sqlite` | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `php-tidy` | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `php-xsl` | [devario-development/php](devario-development/php/PKGBUILD) | — |
| `python-charset-normalizer` | [devario-libs/python-charset-normalizer](devario-libs/python-charset-normalizer/PKGBUILD) | — |
| `sonnet` | [devario-libs/sonnet](devario-libs/sonnet/PKGBUILD) | — |
| `texlive-bin` | [devario-utilities/texlive-bin](devario-utilities/texlive-bin/PKGBUILD) | — |

### Stage 11

56 packages from 7 recipes.

| Package | Build recipe | Bootstrap requirement |
| --- | --- | --- |
| `check` | [devario-libs/check](devario-libs/check/PKGBUILD) | — |
| `check-docs` | [devario-libs/check](devario-libs/check/PKGBUILD) | — |
| `dvisvgm` | [devario-utilities/dvisvgm](devario-utilities/dvisvgm/PKGBUILD) | Cycle G101 — seed packages required |
| `grpc` | [devario-libs/grpc](devario-libs/grpc/PKGBUILD) | — |
| `grpc-cli` | [devario-libs/grpc](devario-libs/grpc/PKGBUILD) | — |
| `openai-codex` | [devario-development/openai-codex](devario-development/openai-codex/PKGBUILD) | — |
| `openai-codex-voice` | [devario-development/openai-codex](devario-development/openai-codex/PKGBUILD) | — |
| `php-grpc` | [devario-libs/grpc](devario-libs/grpc/PKGBUILD) | — |
| `php-legacy-grpc` | [devario-libs/grpc](devario-libs/grpc/PKGBUILD) | — |
| `python-grpcio` | [devario-libs/grpc](devario-libs/grpc/PKGBUILD) | — |
| `python-grpcio-tools` | [devario-libs/grpc](devario-libs/grpc/PKGBUILD) | — |
| `python-requests` | [devario-libs/python-requests](devario-libs/python-requests/PKGBUILD) | — |
| `qt6-multimedia` | [devario-libs/qt6-multimedia](devario-libs/qt6-multimedia/PKGBUILD) | — |
| `qt6-multimedia-ffmpeg` | [devario-libs/qt6-multimedia](devario-libs/qt6-multimedia/PKGBUILD) | — |
| `qt6-multimedia-gstreamer` | [devario-libs/qt6-multimedia](devario-libs/qt6-multimedia/PKGBUILD) | — |
| `texlive-basic` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-bibtexextra` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-binextra` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-context` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-doc` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-fontsextra` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-fontsrecommended` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-fontutils` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-formatsextra` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-games` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-humanities` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langarabic` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langchinese` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langcjk` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langcyrillic` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langczechslovak` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langenglish` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langeuropean` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langfrench` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langgerman` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langgreek` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langitalian` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langjapanese` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langkorean` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langother` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langpolish` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langportuguese` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-langspanish` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-latex` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-latexextra` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-latexrecommended` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-luatex` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-mathscience` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-meta` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-metapost` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-music` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-pictures` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-plaingeneric` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-pstricks` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-publishers` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |
| `texlive-xetex` | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) | Cycle G101 — seed packages required |

### Stage 12

22 packages from 22 recipes.

| Package | Build recipe | Bootstrap requirement |
| --- | --- | --- |
| `arrow` | [devario-libs/arrow](devario-libs/arrow/PKGBUILD) | — |
| `bind` | [devario-utilities/bind](devario-utilities/bind/PKGBUILD) | — |
| `contour` | [devario-utilities/contour](devario-utilities/contour/PKGBUILD) | — |
| `dblatex` | [devario-development/dblatex](devario-development/dblatex/PKGBUILD) | — |
| `define` | [devario-productivity/define](devario-productivity/define/PKGBUILD) | — |
| `electron43` | [devario-libs/electron43](devario-libs/electron43/PKGBUILD) | — |
| `fontforge` | [devario-libs/fontforge](devario-libs/fontforge/PKGBUILD) | — |
| `gl2ps` | [devario-libs/gl2ps](devario-libs/gl2ps/PKGBUILD) | — |
| `python-distro` | [devario-libs/python-distro](devario-libs/python-distro/PKGBUILD) | — |
| `python-pooch` | [devario-libs/python-pooch](devario-libs/python-pooch/PKGBUILD) | — |
| `python-pyudev` | [devario-libs/python-pyudev](devario-libs/python-pyudev/PKGBUILD) | — |
| `python-sphinx-argparse` | [devario-development/python-sphinx-argparse](devario-development/python-sphinx-argparse/PKGBUILD) | — |
| `python-sphinx-autodoc-typehints` | [devario-development/python-sphinx-autodoc-typehints](devario-development/python-sphinx-autodoc-typehints/PKGBUILD) | — |
| `python-sphinx-basic-ng` | [devario-development/python-sphinx-basic-ng](devario-development/python-sphinx-basic-ng/PKGBUILD) | — |
| `python-sphinx-copybutton` | [devario-development/python-sphinx-copybutton](devario-development/python-sphinx-copybutton/PKGBUILD) | — |
| `python-sphinx-inline-tabs` | [devario-development/python-sphinx-inline-tabs](devario-development/python-sphinx-inline-tabs/PKGBUILD) | — |
| `python-sphinx-issues` | [devario-development/python-sphinx-issues](devario-development/python-sphinx-issues/PKGBUILD) | — |
| `python-sphinxcontrib-jquery` | [devario-development/python-sphinxcontrib-jquery](devario-development/python-sphinxcontrib-jquery/PKGBUILD) | — |
| `python-sphinxcontrib-mermaid` | [devario-development/python-sphinxcontrib-mermaid](devario-development/python-sphinxcontrib-mermaid/PKGBUILD) | — |
| `python-sphinxcontrib-towncrier` | [devario-development/python-sphinxcontrib-towncrier](devario-development/python-sphinxcontrib-towncrier/PKGBUILD) | — |
| `qt6-speech` | [devario-libs/qt6-speech](devario-libs/qt6-speech/PKGBUILD) | — |
| `virglrenderer` | [devario-libs/virglrenderer](devario-libs/virglrenderer/PKGBUILD) | — |

### Stage 13

16 packages from 13 recipes.

| Package | Build recipe | Bootstrap requirement |
| --- | --- | --- |
| `podman-desktop` | [devario-development/podman-desktop](devario-development/podman-desktop/PKGBUILD) | — |
| `pyside6` | [devario-libs/pyside6](devario-libs/pyside6/PKGBUILD) | — |
| `pyside6-tools` | [devario-libs/pyside6](devario-libs/pyside6/PKGBUILD) | — |
| `python-pip` | [devario-libs/python-pip](devario-libs/python-pip/PKGBUILD) | — |
| `python-pyarrow` | [devario-libs/python-pyarrow](devario-libs/python-pyarrow/PKGBUILD) | — |
| `python-scipy` | [devario-libs/python-scipy](devario-libs/python-scipy/PKGBUILD) | — |
| `python-sphinx-furo` | [devario-development/python-sphinx-furo](devario-development/python-sphinx-furo/PKGBUILD) | — |
| `python-sphinx_rtd_theme` | [devario-development/python-sphinx_rtd_theme](devario-development/python-sphinx_rtd_theme/PKGBUILD) | — |
| `python-userpath` | [devario-libs/python-userpath](devario-libs/python-userpath/PKGBUILD) | — |
| `python-virtualenv` | [devario-libs/python-virtualenv](devario-libs/python-virtualenv/PKGBUILD) | — |
| `ragel` | [devario-development/ragel](devario-development/ragel/PKGBUILD) | — |
| `rutabaga-ffi` | [devario-libs/rutabaga-ffi](devario-libs/rutabaga-ffi/PKGBUILD) | — |
| `shiboken6` | [devario-libs/pyside6](devario-libs/pyside6/PKGBUILD) | — |
| `shiboken6-generator` | [devario-libs/pyside6](devario-libs/pyside6/PKGBUILD) | — |
| `solaar` | [devario-utilities/solaar](devario-utilities/solaar/PKGBUILD) | — |
| `ttf-liberation` | [devario-libs/ttf-liberation](devario-libs/ttf-liberation/PKGBUILD) | — |

### Stage 14

7 packages from 6 recipes.

| Package | Build recipe | Bootstrap requirement |
| --- | --- | --- |
| `blueprint-compiler` | [devario-development/blueprint-compiler](devario-development/blueprint-compiler/PKGBUILD) | — |
| `chromium` | [devario-browser/chromium](devario-browser/chromium/PKGBUILD) | — |
| `kguiaddons` | [devario-libs/kguiaddons](devario-libs/kguiaddons/PKGBUILD) | — |
| `python-lxml` | [devario-libs/python-lxml](devario-libs/python-lxml/PKGBUILD) | — |
| `python-lxml-docs` | [devario-libs/python-lxml](devario-libs/python-lxml/PKGBUILD) | — |
| `python-pipx` | [devario-development/python-pipx](devario-development/python-pipx/PKGBUILD) | — |
| `rocblas` | [devario-libs/rocblas](devario-libs/rocblas/PKGBUILD) | — |

### Stage 15

7 packages from 7 recipes.

| Package | Build recipe | Bootstrap requirement |
| --- | --- | --- |
| `breeze-icons` | [devario-libs/breeze-icons](devario-libs/breeze-icons/PKGBUILD) | — |
| `kcolorscheme` | [devario-libs/kcolorscheme](devario-libs/kcolorscheme/PKGBUILD) | — |
| `lib32-vulkan-icd-loader` | [devario-libs/lib32-vulkan-icd-loader](devario-libs/lib32-vulkan-icd-loader/PKGBUILD) | — |
| `python-fontparts` | [devario-libs/python-fontparts](devario-libs/python-fontparts/PKGBUILD) | — |
| `python-steam` | [devario-libs/python-steam](devario-libs/python-steam/PKGBUILD) | — |
| `rocsparse` | [devario-libs/rocsparse](devario-libs/rocsparse/PKGBUILD) | — |
| `yelp-tools` | [devario-development/yelp-tools](devario-development/yelp-tools/PKGBUILD) | — |

### Stage 16

9 packages from 9 recipes.

| Package | Build recipe | Bootstrap requirement |
| --- | --- | --- |
| `gtk-doc` | [devario-libs/gtk-doc](devario-libs/gtk-doc/PKGBUILD) | — |
| `hipsparse` | [devario-libs/hipsparse](devario-libs/hipsparse/PKGBUILD) | — |
| `kconfigwidgets` | [devario-libs/kconfigwidgets](devario-libs/kconfigwidgets/PKGBUILD) | — |
| `kiconthemes` | [devario-libs/kiconthemes](devario-libs/kiconthemes/PKGBUILD) | — |
| `ksvg` | [devario-libs/ksvg](devario-libs/ksvg/PKGBUILD) | — |
| `protonup-qt` | [devario-gaming/protonup-qt](devario-gaming/protonup-qt/PKGBUILD) | — |
| `python-ufoprocessor` | [devario-libs/python-ufoprocessor](devario-libs/python-ufoprocessor/PKGBUILD) | — |
| `rocsolver` | [devario-libs/rocsolver](devario-libs/rocsolver/PKGBUILD) | — |
| `zenity` | [devario-utilities/zenity](devario-utilities/zenity/PKGBUILD) | — |

### Stage 17

26 packages from 19 recipes.

| Package | Build recipe | Bootstrap requirement |
| --- | --- | --- |
| `afdko` | [devario-libs/afdko](devario-libs/afdko/PKGBUILD) | — |
| `dbus-glib` | [devario-libs/dbus-glib](devario-libs/dbus-glib/PKGBUILD) | — |
| `gnome-desktop` | [devario-libs/gnome-desktop](devario-libs/gnome-desktop/PKGBUILD) | — |
| `gnome-desktop-4` | [devario-libs/gnome-desktop](devario-libs/gnome-desktop/PKGBUILD) | — |
| `gnome-desktop-common` | [devario-libs/gnome-desktop](devario-libs/gnome-desktop/PKGBUILD) | — |
| `gnome-desktop-docs` | [devario-libs/gnome-desktop](devario-libs/gnome-desktop/PKGBUILD) | — |
| `hipblas` | [devario-libs/hipblas](devario-libs/hipblas/PKGBUILD) | — |
| `hipsolver` | [devario-libs/hipsolver](devario-libs/hipsolver/PKGBUILD) | — |
| `kirigami-addons` | [devario-libs/kirigami-addons](devario-libs/kirigami-addons/PKGBUILD) | — |
| `lib32-libidn2` | [devario-libs/lib32-libidn2](devario-libs/lib32-libidn2/PKGBUILD) | — |
| `libcanberra` | [devario-libs/libcanberra](devario-libs/libcanberra/PKGBUILD) | — |
| `libgsf` | [devario-libs/libgsf](devario-libs/libgsf/PKGBUILD) | — |
| `libgsf-docs` | [devario-libs/libgsf](devario-libs/libgsf/PKGBUILD) | — |
| `libgxps` | [devario-libs/libgxps](devario-libs/libgxps/PKGBUILD) | — |
| `libiptcdata` | [devario-libs/libiptcdata](devario-libs/libiptcdata/PKGBUILD) | — |
| `libraqm` | [devario-libs/libraqm](devario-libs/libraqm/PKGBUILD) | — |
| `phodav` | [devario-libs/phodav](devario-libs/phodav/PKGBUILD) | — |
| `poppler` | [devario-libs/poppler](devario-libs/poppler/PKGBUILD) | — |
| `poppler-glib` | [devario-libs/poppler](devario-libs/poppler/PKGBUILD) | — |
| `poppler-qt5` | [devario-libs/poppler](devario-libs/poppler/PKGBUILD) | — |
| `poppler-qt6` | [devario-libs/poppler](devario-libs/poppler/PKGBUILD) | — |
| `qqc2-desktop-style` | [devario-libs/qqc2-desktop-style](devario-libs/qqc2-desktop-style/PKGBUILD) | — |
| `raptor` | [devario-libs/raptor](devario-libs/raptor/PKGBUILD) | — |
| `rocalution` | [devario-libs/rocalution](devario-libs/rocalution/PKGBUILD) | — |
| `totem-pl-parser` | [devario-libs/totem-pl-parser](devario-libs/totem-pl-parser/PKGBUILD) | — |
| `vala` | [devario-development/vala](devario-development/vala/PKGBUILD) | Seed: `vala` |

### Stage 18

50 packages from 25 recipes.

| Package | Build recipe | Bootstrap requirement |
| --- | --- | --- |
| `easyeffects` | [devario-entertainment/easyeffects](devario-entertainment/easyeffects/PKGBUILD) | — |
| `gdal` | [devario-libs/gdal](devario-libs/gdal/PKGBUILD) | — |
| `gexiv2` | [devario-libs/gexiv2](devario-libs/gexiv2/PKGBUILD) | — |
| `gexiv2-common` | [devario-libs/gexiv2](devario-libs/gexiv2/PKGBUILD) | — |
| `gexiv2-docs` | [devario-libs/gexiv2](devario-libs/gexiv2/PKGBUILD) | — |
| `gnome-autoar` | [devario-libs/gnome-autoar](devario-libs/gnome-autoar/PKGBUILD) | — |
| `gnome-autoar-docs` | [devario-libs/gnome-autoar](devario-libs/gnome-autoar/PKGBUILD) | — |
| `gtk-vnc` | [devario-libs/gtk-vnc](devario-libs/gtk-vnc/PKGBUILD) | — |
| `gtk-vnc-docs` | [devario-libs/gtk-vnc](devario-libs/gtk-vnc/PKGBUILD) | — |
| `gupnp-dlna` | [devario-libs/gupnp-dlna](devario-libs/gupnp-dlna/PKGBUILD) | — |
| `gvim` | [devario-development/vim](devario-development/vim/PKGBUILD) | — |
| `hipblaslt` | [devario-libs/hipblaslt](devario-libs/hipblaslt/PKGBUILD) | — |
| `ibus` | [devario-utilities/ibus](devario-utilities/ibus/PKGBUILD) | — |
| `imagemagick` | [devario-entertainment/imagemagick](devario-entertainment/imagemagick/PKGBUILD) | — |
| `lib32-gnutls` | [devario-libs/lib32-gnutls](devario-libs/lib32-gnutls/PKGBUILD) | — |
| `lib32-libpsl` | [devario-libs/lib32-libpsl](devario-libs/lib32-libpsl/PKGBUILD) | — |
| `libappindicator` | [devario-core/libappindicator](devario-core/libappindicator/PKGBUILD) | — |
| `libibus` | [devario-utilities/ibus](devario-utilities/ibus/PKGBUILD) | — |
| `liblrdf` | [devario-libs/liblrdf](devario-libs/liblrdf/PKGBUILD) | — |
| `libmanette` | [devario-libs/libmanette](devario-libs/libmanette/PKGBUILD) | — |
| `libmanette-docs` | [devario-libs/libmanette](devario-libs/libmanette/PKGBUILD) | — |
| `libnma` | [devario-core/libnma](devario-core/libnma/PKGBUILD) | — |
| `libnma-common` | [devario-core/libnma](devario-core/libnma/PKGBUILD) | — |
| `libnma-gtk4` | [devario-core/libnma](devario-core/libnma/PKGBUILD) | — |
| `libosinfo` | [devario-libs/libosinfo](devario-libs/libosinfo/PKGBUILD) | — |
| `libportal` | [devario-libs/libportal](devario-libs/libportal/PKGBUILD) | — |
| `libportal-docs` | [devario-libs/libportal](devario-libs/libportal/PKGBUILD) | — |
| `libportal-gtk3` | [devario-libs/libportal](devario-libs/libportal/PKGBUILD) | — |
| `libportal-gtk4` | [devario-libs/libportal](devario-libs/libportal/PKGBUILD) | — |
| `libportal-qt5` | [devario-libs/libportal](devario-libs/libportal/PKGBUILD) | — |
| `libportal-qt6` | [devario-libs/libportal](devario-libs/libportal/PKGBUILD) | — |
| `libvirt-glib` | [devario-libs/libvirt-glib](devario-libs/libvirt-glib/PKGBUILD) | — |
| `ollama` | [devario-development/ollama](devario-development/ollama/PKGBUILD) | — |
| `ollama-cuda` | [devario-development/ollama](devario-development/ollama/PKGBUILD) | — |
| `ollama-docs` | [devario-development/ollama](devario-development/ollama/PKGBUILD) | — |
| `ollama-rocm` | [devario-development/ollama](devario-development/ollama/PKGBUILD) | — |
| `ollama-vulkan` | [devario-development/ollama](devario-development/ollama/PKGBUILD) | — |
| `pavucontrol` | [devario-utilities/pavucontrol](devario-utilities/pavucontrol/PKGBUILD) | — |
| `python-gdal` | [devario-libs/gdal](devario-libs/gdal/PKGBUILD) | — |
| `python-pillow` | [devario-libs/python-pillow](devario-libs/python-pillow/PKGBUILD) | — |
| `sane` | [devario-development/sane](devario-development/sane/PKGBUILD) | — |
| `spice-gtk` | [devario-libs/spice-gtk](devario-libs/spice-gtk/PKGBUILD) | — |
| `vim` | [devario-development/vim](devario-development/vim/PKGBUILD) | — |
| `vim-runtime` | [devario-development/vim](devario-development/vim/PKGBUILD) | — |
| `vte-common` | [devario-libs/vte3](devario-libs/vte3/PKGBUILD) | — |
| `vte-docs` | [devario-libs/vte3](devario-libs/vte3/PKGBUILD) | — |
| `vte3` | [devario-libs/vte3](devario-libs/vte3/PKGBUILD) | — |
| `vte3-utils` | [devario-libs/vte3](devario-libs/vte3/PKGBUILD) | — |
| `vte4` | [devario-libs/vte3](devario-libs/vte3/PKGBUILD) | — |
| `vte4-utils` | [devario-libs/vte3](devario-libs/vte3/PKGBUILD) | — |

### Stage 19

98 packages from 13 recipes.

| Package | Build recipe | Bootstrap requirement |
| --- | --- | --- |
| `lib32-libngtcp2` | [devario-libs/lib32-libngtcp2](devario-libs/lib32-libngtcp2/PKGBUILD) | — |
| `liblas` | [devario-libs/liblas](devario-libs/liblas/PKGBUILD) | — |
| `localsearch` | [devario-utilities/localsearch](devario-utilities/localsearch/PKGBUILD) | — |
| `localsearch-testutils` | [devario-utilities/localsearch](devario-utilities/localsearch/PKGBUILD) | — |
| `miopen-hip` | [devario-libs/miopen-hip](devario-libs/miopen-hip/PKGBUILD) | — |
| `network-manager-applet` | [devario-core/network-manager-applet](devario-core/network-manager-applet/PKGBUILD) | — |
| `nm-connection-editor` | [devario-core/network-manager-applet](devario-core/network-manager-applet/PKGBUILD) | — |
| `pdal` | [devario-libs/pdal](devario-libs/pdal/PKGBUILD) | — |
| `proton-cachyos-native` | [devario-gaming/proton-cachyos-native](devario-gaming/proton-cachyos-native/PKGBUILD) | — |
| `python-matplotlib` | [devario-libs/python-matplotlib](devario-libs/python-matplotlib/PKGBUILD) | — |
| `python-pywal` | [devario-development/python-pywal](devario-development/python-pywal/PKGBUILD) | — |
| `qemu-audio-alsa` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-audio-dbus` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-audio-jack` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-audio-oss` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-audio-pa` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-audio-pipewire` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-audio-sdl` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-audio-spice` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-base` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-block-curl` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-block-dmg` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-block-iscsi` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-block-nfs` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-block-ssh` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-chardev-baum` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-chardev-spice` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-common` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-desktop` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-docs` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-emulators-full` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-full` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-guest-agent` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-hw-display-qxl` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-hw-display-virtio-gpu` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-hw-display-virtio-gpu-gl` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-hw-display-virtio-gpu-pci` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-hw-display-virtio-gpu-pci-gl` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-hw-display-virtio-gpu-pci-rutabaga` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-hw-display-virtio-gpu-rutabaga` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-hw-display-virtio-vga` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-hw-display-virtio-vga-gl` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-hw-display-virtio-vga-rutabaga` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-hw-s390x-virtio-gpu-ccw` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-hw-uefi-vars` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-hw-usb-host` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-hw-usb-redirect` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-hw-usb-smartcard` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-img` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-pr-helper` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-aarch64` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-alpha` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-alpha-firmware` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-arm` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-arm-firmware` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-avr` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-hexagon` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-hppa` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-hppa-firmware` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-loongarch64` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-m68k` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-microblaze` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-microblaze-firmware` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-mips` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-or1k` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-ppc` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-ppc-firmware` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-riscv` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-riscv-firmware` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-rx` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-s390x` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-s390x-firmware` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-sh4` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-sparc` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-sparc-firmware` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-tricore` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-x86` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-x86-firmware` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-system-xtensa` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-tests` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-tools` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-ui-curses` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-ui-dbus` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-ui-egl-headless` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-ui-gtk` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-ui-opengl` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-ui-sdl` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-ui-spice-app` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-ui-spice-core` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-user` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-user-binfmt` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-user-static` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-user-static-binfmt` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-vhost-user-gpu` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `qemu-vmsr-helper` | [devario-utilities/qemu](devario-utilities/qemu/PKGBUILD) | — |
| `wine` | [devario-gaming/wine](devario-gaming/wine/PKGBUILD) | — |
| `wine-cachyos-opt` | [devario-gaming/wine-cachyos-opt](devario-gaming/wine-cachyos-opt/PKGBUILD) | — |
| `zbar` | [devario-libs/zbar](devario-libs/zbar/PKGBUILD) | — |

### Stage 20

16 packages from 6 recipes.

| Package | Build recipe | Bootstrap requirement |
| --- | --- | --- |
| `goverlay` | [devario-gaming/goverlay](devario-gaming/goverlay/PKGBUILD) | — |
| `lib32-curl` | [devario-libs/lib32-curl](devario-libs/lib32-curl/PKGBUILD) | — |
| `lib32-libcurl-compat` | [devario-libs/lib32-curl](devario-libs/lib32-curl/PKGBUILD) | — |
| `lib32-libcurl-gnutls` | [devario-libs/lib32-curl](devario-libs/lib32-curl/PKGBUILD) | — |
| `libnautilus-extension` | [devario-utilities/nautilus](devario-utilities/nautilus/PKGBUILD) | — |
| `libnautilus-extension-docs` | [devario-utilities/nautilus](devario-utilities/nautilus/PKGBUILD) | — |
| `migraphx` | [devario-libs/migraphx](devario-libs/migraphx/PKGBUILD) | — |
| `nautilus` | [devario-utilities/nautilus](devario-utilities/nautilus/PKGBUILD) | — |
| `rocm-hip-libraries` | [devario-development/rocm-hip-sdk](devario-development/rocm-hip-sdk/PKGBUILD) | — |
| `rocm-hip-runtime` | [devario-development/rocm-hip-sdk](devario-development/rocm-hip-sdk/PKGBUILD) | — |
| `rocm-hip-sdk` | [devario-development/rocm-hip-sdk](devario-development/rocm-hip-sdk/PKGBUILD) | — |
| `rocm-language-runtime` | [devario-development/rocm-hip-sdk](devario-development/rocm-hip-sdk/PKGBUILD) | — |
| `rocm-ml-libraries` | [devario-development/rocm-hip-sdk](devario-development/rocm-hip-sdk/PKGBUILD) | — |
| `rocm-ml-sdk` | [devario-development/rocm-hip-sdk](devario-development/rocm-hip-sdk/PKGBUILD) | — |
| `rocm-opencl-sdk` | [devario-development/rocm-hip-sdk](devario-development/rocm-hip-sdk/PKGBUILD) | — |
| `winetricks` | [devario-gaming/winetricks](devario-gaming/winetricks/PKGBUILD) | — |

### Stage 21

13 packages from 4 recipes.

| Package | Build recipe | Bootstrap requirement |
| --- | --- | --- |
| `file-roller` | [devario-utilities/file-roller](devario-utilities/file-roller/PKGBUILD) | — |
| `lib32-libelf` | [devario-libs/lib32-libelf](devario-libs/lib32-libelf/PKGBUILD) | — |
| `onnxruntime-cpu` | [devario-development/onnxruntime](devario-development/onnxruntime/PKGBUILD) | — |
| `onnxruntime-cuda` | [devario-development/onnxruntime](devario-development/onnxruntime/PKGBUILD) | — |
| `onnxruntime-opt-cuda` | [devario-development/onnxruntime](devario-development/onnxruntime/PKGBUILD) | — |
| `onnxruntime-opt-rocm` | [devario-development/onnxruntime](devario-development/onnxruntime/PKGBUILD) | — |
| `onnxruntime-rocm` | [devario-development/onnxruntime](devario-development/onnxruntime/PKGBUILD) | — |
| `protontricks` | [devario-gaming/protontricks](devario-gaming/protontricks/PKGBUILD) | — |
| `python-onnxruntime-cpu` | [devario-development/onnxruntime](devario-development/onnxruntime/PKGBUILD) | — |
| `python-onnxruntime-cuda` | [devario-development/onnxruntime](devario-development/onnxruntime/PKGBUILD) | — |
| `python-onnxruntime-opt-cuda` | [devario-development/onnxruntime](devario-development/onnxruntime/PKGBUILD) | — |
| `python-onnxruntime-opt-rocm` | [devario-development/onnxruntime](devario-development/onnxruntime/PKGBUILD) | — |
| `python-onnxruntime-rocm` | [devario-development/onnxruntime](devario-development/onnxruntime/PKGBUILD) | — |

### Stage 22

5 packages from 5 recipes.

| Package | Build recipe | Bootstrap requirement |
| --- | --- | --- |
| `lib32-dbus` | [devario-libs/lib32-dbus](devario-libs/lib32-dbus/PKGBUILD) | Cycle G688 — seed packages required |
| `lib32-glib2` | [devario-libs/lib32-glib2](devario-libs/lib32-glib2/PKGBUILD) | Cycle G688 — seed packages required |
| `lib32-systemd` | [devario-libs/lib32-systemd](devario-libs/lib32-systemd/PKGBUILD) | Cycle G688 — seed packages required |
| `opencascade` | [devario-development/opencascade](devario-development/opencascade/PKGBUILD) | Cycle G364 — seed packages required |
| `vtk` | [devario-libs/vtk](devario-libs/vtk/PKGBUILD) | Cycle G364 — seed packages required |

### Stage 23

36 packages from 11 recipes.

| Package | Build recipe | Bootstrap requirement |
| --- | --- | --- |
| `lib32-cairo` | [devario-libs/lib32-cairo](devario-libs/lib32-cairo/PKGBUILD) | Cycle G714 — seed packages required |
| `lib32-fontconfig` | [devario-libs/lib32-fontconfig](devario-libs/lib32-fontconfig/PKGBUILD) | Cycle G714 — seed packages required |
| `lib32-freetype2` | [devario-libs/lib32-freetype2](devario-libs/lib32-freetype2/PKGBUILD) | Cycle G714 — seed packages required |
| `lib32-harfbuzz` | [devario-libs/lib32-harfbuzz](devario-libs/lib32-harfbuzz/PKGBUILD) | Cycle G714 — seed packages required |
| `lib32-harfbuzz-cairo` | [devario-libs/lib32-harfbuzz](devario-libs/lib32-harfbuzz/PKGBUILD) | Cycle G714 — seed packages required |
| `lib32-harfbuzz-icu` | [devario-libs/lib32-harfbuzz](devario-libs/lib32-harfbuzz/PKGBUILD) | Cycle G714 — seed packages required |
| `lib32-libglvnd` | [devario-libs/lib32-libglvnd](devario-libs/lib32-libglvnd/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-libnm` | [devario-libs/lib32-libnm](devario-libs/lib32-libnm/PKGBUILD) | — |
| `lib32-libpipewire` | [devario-libs/lib32-pipewire](devario-libs/lib32-pipewire/PKGBUILD) | — |
| `lib32-libpulse` | [devario-libs/lib32-libpulse](devario-libs/lib32-libpulse/PKGBUILD) | — |
| `lib32-libva` | [devario-libs/lib32-libva](devario-libs/lib32-libva/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-mesa` | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-opencl-mesa` | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-pipewire` | [devario-libs/lib32-pipewire](devario-libs/lib32-pipewire/PKGBUILD) | — |
| `lib32-pipewire-jack` | [devario-libs/lib32-pipewire](devario-libs/lib32-pipewire/PKGBUILD) | — |
| `lib32-pipewire-netjack2` | [devario-libs/lib32-pipewire](devario-libs/lib32-pipewire/PKGBUILD) | — |
| `lib32-pipewire-v4l2` | [devario-libs/lib32-pipewire](devario-libs/lib32-pipewire/PKGBUILD) | — |
| `lib32-vulkan-asahi` | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-vulkan-broadcom` | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-vulkan-dzn` | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-vulkan-freedreno` | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-vulkan-gfxstream` | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-vulkan-intel` | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-vulkan-mesa-implicit-layers` | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-vulkan-mesa-layers` | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-vulkan-nouveau` | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-vulkan-panfrost` | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-vulkan-powervr` | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-vulkan-radeon` | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-vulkan-swrast` | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `lib32-vulkan-virtio` | [devario-libs/lib32-mesa](devario-libs/lib32-mesa/PKGBUILD) | Cycle G734 — seed packages required |
| `opencv` | [devario-libs/opencv](devario-libs/opencv/PKGBUILD) | — |
| `opencv-cuda` | [devario-libs/opencv](devario-libs/opencv/PKGBUILD) | — |
| `opencv-samples` | [devario-libs/opencv](devario-libs/opencv/PKGBUILD) | — |
| `python-opencv` | [devario-libs/opencv](devario-libs/opencv/PKGBUILD) | — |
| `python-opencv-cuda` | [devario-libs/opencv](devario-libs/opencv/PKGBUILD) | — |

### Stage 24

2 packages from 2 recipes.

| Package | Build recipe | Bootstrap requirement |
| --- | --- | --- |
| `lib32-alsa-plugins` | [devario-libs/lib32-alsa-plugins](devario-libs/lib32-alsa-plugins/PKGBUILD) | — |
| `zxing-cpp` | [devario-libs/zxing-cpp](devario-libs/zxing-cpp/PKGBUILD) | — |

### Stage 25

6 packages from 4 recipes.

| Package | Build recipe | Bootstrap requirement |
| --- | --- | --- |
| `proton-cachyos-slr` | [devario-gaming/proton-cachyos-slr](devario-gaming/proton-cachyos-slr/PKGBUILD) | — |
| `umu-launcher` | [devario-gaming/umu-launcher](devario-gaming/umu-launcher/PKGBUILD) | — |
| `webkit2gtk-4.1` | [devario-development/webkit2gtk-4.1](devario-development/webkit2gtk-4.1/PKGBUILD) | — |
| `webkit2gtk-4.1-docs` | [devario-development/webkit2gtk-4.1](devario-development/webkit2gtk-4.1/PKGBUILD) | — |
| `webkitgtk-6.0` | [devario-libs/webkitgtk-6.0](devario-libs/webkitgtk-6.0/PKGBUILD) | — |
| `webkitgtk-6.0-docs` | [devario-libs/webkitgtk-6.0](devario-libs/webkitgtk-6.0/PKGBUILD) | — |

### Stage 26

2 packages from 2 recipes.

| Package | Build recipe | Bootstrap requirement |
| --- | --- | --- |
| `font-manager` | [devario-utilities/font-manager](devario-utilities/font-manager/PKGBUILD) | — |
| `glade` | [devario-development/glade](devario-development/glade/PKGBUILD) | — |

### Stage 27

3 packages from 2 recipes.

| Package | Build recipe | Bootstrap requirement |
| --- | --- | --- |
| `gtksourceview4` | [devario-libs/gtksourceview4](devario-libs/gtksourceview4/PKGBUILD) | — |
| `libhandy` | [devario-core/libhandy](devario-core/libhandy/PKGBUILD) | — |
| `libhandy-docs` | [devario-core/libhandy](devario-core/libhandy/PKGBUILD) | — |

### Stage 28

5 packages from 4 recipes.

| Package | Build recipe | Bootstrap requirement |
| --- | --- | --- |
| `meld` | [devario-development/meld](devario-development/meld/PKGBUILD) | — |
| `seahorse` | [devario-core/seahorse](devario-core/seahorse/PKGBUILD) | — |
| `virt-install` | [devario-development/virt-manager](devario-development/virt-manager/PKGBUILD) | — |
| `virt-manager` | [devario-development/virt-manager](devario-development/virt-manager/PKGBUILD) | — |
| `xpad` | [devario-gaming/xpad](devario-gaming/xpad/PKGBUILD) | — |

## Bootstrap requirements

There are **25 groups requiring seed packages**: 15 multi-recipe cycles and 10 additional self-hosted groups. The earlier cycle report covered only the multi-recipe cycles. The expanded plan now also identifies tools needed to build themselves, including through runtime dependencies of a published build tool.

The additional single-recipe seed groups are:

| Stage / group | Recipe | Existing tool required |
| --- | --- | --- |
| 01 / G431 | `fpc` | `fpc` |
| 02 / G168 | `java8-openjdk` | `java-environment=8` |
| 03 / G008 | `jdk-openjdk` | `java-environment>=22` |
| 03 / G165 | `java11-openjdk` | `java-environment=11` |
| 03 / G166 | `java17-openjdk` | `java-environment=17` |
| 03 / G167 | `java25-openjdk` | `java-environment=25` |
| 03 / G435 | `yarn` | `yarn` |
| 03 / G452 | `java21-openjdk` | `java-environment=21` |
| 04 / G479 | `pnpm` | `pnpm` |
| 17 / G111 | `vala` | `vala` |

[bootstrap-order.txt](audits/application-expansion-2026-10-08/bootstrap-order.txt) lists all 25 groups, their member recipes, and exact internal dependency constraints. Those seeds must come from a working, compatible bootstrap set or separately prepared bootstrap recipes. This plan identifies the prerequisites; it does not supply or build the seed binaries.

## Files to use

- [Full readable queue](audits/application-expansion-2026-10-08/build-stages.txt): every recipe, grouped by stage.
- [Package TSV](audits/application-expansion-2026-10-08/package-build-stages.tsv): one row per package, with its stage and build recipe.
- [Builder TSV](audits/application-expansion-2026-10-08/build-stages.tsv): stages, predecessor groups, bootstrap blockers, and requested outputs.
- [Application index](audits/application-expansion-2026-10-08/application-build-stages.tsv): the stage and source directory for each of the 114 requested packages.
- [Bootstrap queue](audits/application-expansion-2026-10-08/bootstrap-order.txt): seed requirements in stage order.
- [Alternative packages](audits/application-expansion-2026-10-08/package-alternatives.json): JDK/JRE, Node.js, Vim/GVim, Lazarus and OpenCV installation choices.

The separate Neovim and isolation-builder Texinfo hook repairs are outside the 908-recipe application manifest. Texinfo uses dependencies present in the saved repository snapshot; Neovim requires its own dependency plan. TeX Live’s hook correction is included in the main queue. See [the hook guide](HOOK-BUILDS.md).

All 3,730 recorded dependency edges were checked: every dependency outside its own group is in an earlier stage. Current PKGBUILD hashes match the audited manifest. The plan remains tied to the saved repository/provider snapshot; re-resolve it if dependency metadata, available providers, or recipes change. Full builds were not run to create this order.

To regenerate the stage files from the same audited graph:

```sh
python audits/application-expansion-2026-10-08/write-build-stages.py
```
