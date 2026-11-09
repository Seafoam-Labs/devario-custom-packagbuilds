#!/usr/bin/env python3
"""Guard the versioned SONAME provisions of the fan-in ABI libraries in this tree.

Each recipe here publishes a shared object, so every bare `libfoo.so` provision it declares
must be paired with the `libfoo.so=N-64` form Shelly carries into `.PKGINFO`, and each pinned
form must be checked by the recipe's own ELF64/SONAME probe. The bare-only state is what let
the tree-sitter 0.27 break load an incompatible library, and a consumer that pins a provision
nothing published declares makes every isolated build root unresolvable.
"""

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

# Provisions read off the published archives with `readelf -d`, not derived from recipe text.
PINNED = {
    "acl": {"libacl.so": "libacl.so=1-64"},
    "attr": {"libattr.so": "libattr.so=1-64"},
    "audit": {"libaudit.so": "libaudit.so=1-64", "libauparse.so": "libauparse.so=0-64"},
    "gdbm": {
        "libgdbm.so": "libgdbm.so=6-64",
        "libgdbm_compat.so": "libgdbm_compat.so=4-64",
    },
    "libbpf": {"libbpf.so": "libbpf.so=1-64"},
    "libcap": {"libcap.so": "libcap.so=2-64", "libpsx.so": "libpsx.so=2-64"},
    "libcap-ng": {
        "libcap-ng.so": "libcap-ng.so=0-64",
        "libdrop_ambient.so": "libdrop_ambient.so=0-64",
    },
    "libdeflate": {"libdeflate.so": "libdeflate.so=0-64"},
    "libnsl": {"libnsl.so": "libnsl.so=3-64"},
    "libunistring": {"libunistring.so": "libunistring.so=5-64"},
    "libverto": {
        "libverto.so": "libverto.so=1-64",
        "libverto-libevent.so": "libverto-libevent.so=1-64",
    },
    "oniguruma": {"libonig.so": "libonig.so=5-64"},
    "p11-kit": {"libp11-kit.so": "libp11-kit.so=0-64"},
    # Compiler support, numeric libraries, and language runtimes. Every value here
    # is the SONAME the published archive carries, read with `readelf -d`.
    "duktape": {
        "libduktape.so": "libduktape.so=207-64",
        "libduktaped.so": "libduktaped.so=207-64",
    },
    "fftw": {
        "libfftw3.so": "libfftw3.so=3-64",
        "libfftw3_omp.so": "libfftw3_omp.so=3-64",
        "libfftw3_threads.so": "libfftw3_threads.so=3-64",
        "libfftw3f.so": "libfftw3f.so=3-64",
        "libfftw3f_omp.so": "libfftw3f_omp.so=3-64",
        "libfftw3f_threads.so": "libfftw3f_threads.so=3-64",
        "libfftw3l.so": "libfftw3l.so=3-64",
        "libfftw3l_omp.so": "libfftw3l_omp.so=3-64",
        "libfftw3l_threads.so": "libfftw3l_threads.so=3-64",
        "libfftw3q.so": "libfftw3q.so=3-64",
        "libfftw3q_omp.so": "libfftw3q_omp.so=3-64",
        "libfftw3q_threads.so": "libfftw3q_threads.so=3-64",
        "libfftw3_mpi.so": "libfftw3_mpi.so=3-64",
        "libfftw3f_mpi.so": "libfftw3f_mpi.so=3-64",
        "libfftw3l_mpi.so": "libfftw3l_mpi.so=3-64",
    },
    "gtest": {
        "libgmock.so": "libgmock.so=1.18.0-64",
        "libgmock_main.so": "libgmock_main.so=1.18.0-64",
        "libgtest.so": "libgtest.so=1.18.0-64",
        "libgtest_main.so": "libgtest_main.so=1.18.0-64",
    },
    "jemalloc": {"libjemalloc.so": "libjemalloc.so=2-64"},
    "libedit": {"libedit.so": "libedit.so=0-64"},
    "libisl": {"libisl.so": "libisl.so=23-64"},
    "pahole": {
        "libdwarves.so": "libdwarves.so=1-64",
        "libdwarves_emit.so": "libdwarves_emit.so=1-64",
        "libdwarves_reorganize.so": "libdwarves_reorganize.so=1-64",
    },
    "pcre": {
        "libpcre.so": "libpcre.so=1-64",
        "libpcre16.so": "libpcre16.so=0-64",
        "libpcre32.so": "libpcre32.so=0-64",
        "libpcreposix.so": "libpcreposix.so=0-64",
        "libpcrecpp.so": "libpcrecpp.so=0-64",
    },
    "shaderc": {"libshaderc_shared.so": "libshaderc_shared.so=1-64"},
    "tomlplusplus": {"libtomlplusplus.so": "libtomlplusplus.so=3-64"},
    "yaml-cpp": {"libyaml-cpp.so": "libyaml-cpp.so=0.9-64"},
    "yyjson": {"libyyjson.so": "libyyjson.so=0-64"},
    "zeromq": {"libzmq.so": "libzmq.so=5-64"},
    # Storage, boot, and installer path. libdevmapper is published under lvm2's
    # device-mapper output, libbd_* under the matching libblockdev output.
    "cryptsetup": {"libcryptsetup.so": "libcryptsetup.so=12-64"},
    "e2fsprogs": {
        "libcom_err.so": "libcom_err.so=2-64",
        "libe2p.so": "libe2p.so=2-64",
        "libext2fs.so": "libext2fs.so=2-64",
        "libss.so": "libss.so=2-64",
    },
    "efivar": {
        "libefiboot.so": "libefiboot.so=1-64",
        "libefisec.so": "libefisec.so=1-64",
        "libefivar.so": "libefivar.so=1-64",
    },
    "f2fs-tools": {
        "libf2fs.so": "libf2fs.so=11-64",
        "libf2fs_format.so": "libf2fs_format.so=10-64",
    },
    "libblockdev": {
        "libbd_utils.so": "libbd_utils.so=3-64",
        "libblockdev.so": "libblockdev.so=3-64",
        "libbd_btrfs.so": "libbd_btrfs.so=3-64",
        "libbd_crypto.so": "libbd_crypto.so=3-64",
        "libbd_dm.so": "libbd_dm.so=3-64",
        "libbd_fs.so": "libbd_fs.so=3-64",
        "libbd_loop.so": "libbd_loop.so=3-64",
        "libbd_lvm.so": "libbd_lvm.so=3-64",
        "libbd_lvm-dbus.so": "libbd_lvm-dbus.so=3-64",
        "libbd_mdraid.so": "libbd_mdraid.so=3-64",
        "libbd_mpath.so": "libbd_mpath.so=3-64",
        "libbd_nvdimm.so": "libbd_nvdimm.so=3-64",
        "libbd_nvme.so": "libbd_nvme.so=3-64",
        "libbd_part.so": "libbd_part.so=3-64",
        "libbd_smart.so": "libbd_smart.so=3-64",
        "libbd_smartmontools.so": "libbd_smartmontools.so=3-64",
        "libbd_swap.so": "libbd_swap.so=3-64",
    },
    "lvm2": {
        "libdevmapper.so": "libdevmapper.so=1.02-64",
        "libdevmapper-event.so": "libdevmapper-event.so=1.02-64",
    },
    "udisks2": {"libudisks2.so": "libudisks2.so=0-64"},
    # No provision of their own, but every .so they depend on is pinned above or
    # by a published provider, so their depends belong in this guard too.
    "efibootmgr": {},
    "parted": {},
    "squashfs-tools": {},
    "thin-provisioning-tools": {},
    # Network, PKI, and cryptography. libnm is published by networkmanager's libnm output and
    # libbluetooth.so by bluez's bluez-libs output; iptables declares its four libraries in both
    # of its outputs, so the probe runs in the _package() helper both of them call.
    "bluez": {"libbluetooth.so": "libbluetooth.so=3-64"},
    "iptables": {
        "libip4tc.so": "libip4tc.so=2-64",
        "libip6tc.so": "libip6tc.so=2-64",
        "libipq.so": "libipq.so=0-64",
        "libxtables.so": "libxtables.so=12-64",
    },
    "libnice": {"libnice.so": "libnice.so=10-64"},
    "libnl": {
        "libnl-3.so": "libnl-3.so=200-64",
        "libnl-cli-3.so": "libnl-cli-3.so=200-64",
        "libnl-genl-3.so": "libnl-genl-3.so=200-64",
        "libnl-idiag-3.so": "libnl-idiag-3.so=200-64",
        "libnl-nf-3.so": "libnl-nf-3.so=200-64",
        "libnl-route-3.so": "libnl-route-3.so=200-64",
        "libnl-xfrm-3.so": "libnl-xfrm-3.so=200-64",
    },
    "libpcap": {"libpcap.so": "libpcap.so=1-64"},
    "libsodium": {"libsodium.so": "libsodium.so=26-64"},
    "libssh": {"libssh.so": "libssh.so=4-64"},
    "libteam": {
        "libteam.so": "libteam.so=5-64",
        "libteamdctl.so": "libteamdctl.so=0-64",
    },
    "networkmanager": {"libnm.so": "libnm.so=0-64"},
    "npth": {"libnpth.so": "libnpth.so=0-64"},
    # No provision of their own here either, but every .so depend names a versioned
    # provision its provider publishes.
    "dbus-broker": {},
    "gnupg": {},
    "gnutls": {},
    "openldap": {},
    "pinentry": {},
    # Audio codecs and DSP libraries. `serd`, `zix` and `ncurses` carry the provisions
    # their consumers name, and `alsa-lib` already published both of its pins.
    # `rubberband` also ships `librubberband-jni.so`, whose own SONAME carries no
    # version, so it has no versioned form to declare.
    "alsa-lib": {
        "libasound.so": "libasound.so=2-64",
        "libatopology.so": "libatopology.so=2-64",
    },
    "flac": {"libFLAC.so": "libFLAC.so=14-64", "libFLAC++.so": "libFLAC++.so=11-64"},
    "lame": {"libmp3lame.so": "libmp3lame.so=0-64"},
    "libbs2b": {"libbs2b.so": "libbs2b.so=0-64"},
    "libexsid": {"libexsid.so": "libexsid.so=2-64"},
    "libfdk-aac": {"libfdk-aac.so": "libfdk-aac.so=2-64"},
    "libfreeaptx": {"libfreeaptx.so": "libfreeaptx.so=0-64"},
    "liblc3": {"liblc3.so": "liblc3.so=1-64"},
    "libldac": {
        "libldacBT_abr.so": "libldacBT_abr.so=2-64",
        "libldacBT_enc.so": "libldacBT_enc.so=2-64",
    },
    "libogg": {"libogg.so": "libogg.so=0-64"},
    "libopenmpt": {"libopenmpt.so": "libopenmpt.so=0-64"},
    "libresidfp": {"libresidfp.so": "libresidfp.so=0-64"},
    "libsamplerate": {"libsamplerate.so": "libsamplerate.so=0-64"},
    "libsidplayfp": {
        "libsidplayfp.so": "libsidplayfp.so=7-64",
        "libstilview.so": "libstilview.so=0-64",
    },
    "libvorbis": {
        "libvorbis.so": "libvorbis.so=0-64",
        "libvorbisenc.so": "libvorbisenc.so=2-64",
        "libvorbisfile.so": "libvorbisfile.so=3-64",
    },
    "mpg123": {
        "libmpg123.so": "libmpg123.so=0-64",
        "libout123.so": "libout123.so=0-64",
        "libsyn123.so": "libsyn123.so=0-64",
    },
    "ncurses": {
        "libncurses++w.so": "libncurses++w.so=6-64",
        "libformw.so": "libformw.so=6-64",
        "libmenuw.so": "libmenuw.so=6-64",
        "libpanelw.so": "libpanelw.so=6-64",
        "libncursesw.so": "libncursesw.so=6-64",
    },
    "opencore-amr": {
        "libopencore-amrnb.so": "libopencore-amrnb.so=0-64",
        "libopencore-amrwb.so": "libopencore-amrwb.so=0-64",
    },
    "opus": {"libopus.so": "libopus.so=0-64"},
    "orc": {
        "liborc-0.4.so": "liborc-0.4.so=0-64",
        "liborc-test-0.4.so": "liborc-test-0.4.so=0-64",
    },
    "rtaudio": {"librtaudio.so": "librtaudio.so=7-64"},
    "rubberband": {"librubberband.so": "librubberband.so=3-64"},
    "sbc": {"libsbc.so": "libsbc.so=1-64"},
    "sdl_image": {"libSDL_image-1.2.so": "libSDL_image-1.2.so=0-64"},
    "serd": {"libserd-0.so": "libserd-0.so=0-64"},
    "sndio": {"libsndio.so": "libsndio.so=7-64"},
    "speex": {"libspeex.so": "libspeex.so=1-64"},
    "sord": {"libsord-0.so": "libsord-0.so=0-64"},
    "sratom": {"libsratom-0.so": "libsratom-0.so=0-64"},
    "vamp-plugin-sdk": {
        "libvamp-hostsdk.so": "libvamp-hostsdk.so=3-64",
        "libvamp-sdk.so": "libvamp-sdk.so=2-64",
    },
    "zix": {"libzix-0.so": "libzix-0.so=0-64"},
    # No provision of their own, but every .so depend names a pinned provider.
    "alsa-utils": {},
    # Video, imaging, and graphics codecs. Here too every value is the SONAME the
    # published archive carries, except `libopenslide.so=1` and `libdicom.so=1`:
    # neither has published yet, so their pins come from the upstream meson ABI
    # version (`abi_version`/`soversion`), and Arch already publishes
    # libopenslide.so=1-64. add-determinism ships no library but pins its zlib
    # depend, and libass and libbluray pin the published freetype2 provision.
    # The librsvg pair is written literal because the guard reads recipe text.
    "add-determinism": {},
    "dav1d": {"libdav1d.so": "libdav1d.so=7-64"},
    "l-smash": {"liblsmash.so": "liblsmash.so=2-64"},
    "libass": {"libass.so": "libass.so=9-64"},
    "libbluray": {"libbluray.so": "libbluray.so=4-64"},
    "libdicom": {"libdicom.so": "libdicom.so=1-64"},
    "libdovi": {"libdovi.so": "libdovi.so=3-64"},
    "libexif": {"libexif.so": "libexif.so=12-64"},
    "libinih": {
        "libinih.so": "libinih.so=0-64",
        "libINIReader.so": "libINIReader.so=0-64",
    },
    "libjxl": {
        "libjxl.so": "libjxl.so=0.12-64",
        "libjxl_cms.so": "libjxl_cms.so=0.12-64",
        "libjxl_threads.so": "libjxl_threads.so=0.12-64",
    },
    "libplacebo": {"libplacebo.so": "libplacebo.so=387-64"},
    "librsvg": {"librsvg-2.so": "librsvg-2.so=2-64"},
    "libvips": {
        "libvips.so": "libvips.so=42-64",
        "libvips-cpp.so": "libvips-cpp.so=42-64",
    },
    "libvpl": {"libvpl.so": "libvpl.so=2-64"},
    "libvpx": {"libvpx.so": "libvpx.so=12-64"},
    "openslide": {"libopenslide.so": "libopenslide.so=1-64"},
    "rav1e": {"librav1e.so": "librav1e.so=0.8-64"},
    "vid.stab": {"libvidstab.so": "libvidstab.so=1.2-64"},
    "xvidcore": {"libxvidcore.so": "libxvidcore.so=4-64"},
    "graphicsmagick": {
        "libGraphicsMagick.so": "libGraphicsMagick.so=3-64",
        "libGraphicsMagickWand.so": "libGraphicsMagickWand.so=2-64",
        "libGraphicsMagick++.so": "libGraphicsMagick++.so=12-64",
    },
    # GObject, GTK, Qt, and KDE bindings. Every value is the SONAME the published
    # archive carries, read with readelf -d. glibmm pins the libsigc++ provision
    # this batch publishes, and the gupnp trio pins the gssdp, gupnp and libsoup3
    # provisions the same stage publishes, provider before consumer.
    "gcr": {
        "libgck-1.so": "libgck-1.so=0-64",
        "libgcr-base-3.so": "libgcr-base-3.so=1-64",
        "libgcr-ui-3.so": "libgcr-ui-3.so=1-64",
    },
    "gcr-4": {
        "libgck-2.so": "libgck-2.so=2-64",
        "libgcr-4.so": "libgcr-4.so=4-64",
    },
    "glibmm": {
        "libglibmm-2.4.so": "libglibmm-2.4.so=1-64",
        "libgiomm-2.4.so": "libgiomm-2.4.so=1-64",
    },
    "graphene": {"libgraphene-1.0.so": "libgraphene-1.0.so=0-64"},
    "gssdp": {"libgssdp-1.6.so": "libgssdp-1.6.so=0-64"},
    "gupnp": {"libgupnp-1.6.so": "libgupnp-1.6.so=0-64"},
    "gupnp-igd": {"libgupnp-igd-1.6.so": "libgupnp-igd-1.6.so=0-64"},
    "libadwaita": {"libadwaita-1.so": "libadwaita-1.so=0-64"},
    "libcloudproviders": {"libcloudproviders.so": "libcloudproviders.so=0-64"},
    "libgee": {"libgee-0.8.so": "libgee-0.8.so=2-64"},
    "libgnomekbd": {
        "libgnomekbd.so": "libgnomekbd.so=8-64",
        "libgnomekbdui.so": "libgnomekbdui.so=8-64",
    },
    "libpanel": {"libpanel-1.so": "libpanel-1.so=1-64"},
    "libproxy": {"libproxy.so": "libproxy.so=1-64"},
    "libsigc++": {"libsigc-2.0.so": "libsigc-2.0.so=0-64"},
    "libsoup3": {"libsoup-3.0.so": "libsoup-3.0.so=0-64"},
    "sdbus-cpp": {"libsdbus-c++.so": "libsdbus-c++.so=2-64"},
    "tinysparql": {"libtinysparql-3.0.so": "libtinysparql-3.0.so=0-64"},
    # Language bindings, the Perl cluster, and arch=any data. libstemmer is the only
    # unpinned provision in that batch: the published archive's SONAME is
    # libstemmer.so.0, and the three consumers that name libstemmer name the package,
    # not the provision.
    "snowball": {"libstemmer.so": "libstemmer.so=0-64"},
    # System utilities, HID, and console. Every value here is the SONAME the published
    # archive carries, read with `readelf -d`, paired beside the bare name upstream declares.
    "gpm": {"libgpm.so": "libgpm.so=2-64"},
    "hidapi": {
        "libhidapi-hidraw.so": "libhidapi-hidraw.so=0-64",
        "libhidapi-libusb.so": "libhidapi-libusb.so=0-64",
    },
    "lm_sensors": {"libsensors.so": "libsensors.so=5-64"},
    "pcsclite": {
        "libpcsclite.so": "libpcsclite.so=1-64",
        "libpcsclite_real.so": "libpcsclite_real.so=1-64",
        "libpcscspy.so": "libpcscspy.so=0-64",
    },
    # Application-layer imaging and document stacks. Every value here is the SONAME the
    # published archive carries, read with `readelf -d`, paired beside the bare name
    # upstream declares. gegl also ships libgegl-npd-0.4.so and libgegl-sc-0.4.so, whose
    # own SONAMEs carry no version, so they have no versioned form to declare. gexiv2 is
    # the pkgbase the gexiv2-common folder clones; its provision libgexiv2-0.16.so and
    # libgexiv2's libgexiv2.so belong to two different pkgbases and never cross-provide.
    "babl": {"libbabl-0.1.so": "libbabl-0.1.so=0-64"},
    "gegl": {"libgegl-0.4.so": "libgegl-0.4.so=0-64"},
    "gexiv2": {"libgexiv2-0.16.so": "libgexiv2-0.16.so=4-64"},
    "gmime3": {"libgmime-3.0.so": "libgmime-3.0.so=0-64"},
    "gspell": {"libgspell-1.so": "libgspell-1.so=3-64"},
    "libgexiv2": {"libgexiv2.so": "libgexiv2.so=2-64"},
    "xapian-core": {"libxapian.so": "libxapian.so=45-64"},
    # Small single-purpose libraries. nettle3 keeps nettle's 3.x SONAMEs, read off
    # the published archive: libnettle.so.8 and libhogweed.so.6, not the 9/7 pair
    # the owned nettle 4.0 declares beside it.
    "nettle3": {
        "libnettle.so": "libnettle.so=8-64",
        "libhogweed.so": "libhogweed.so=6-64",
    },
}

# rtaudio, sdl_image and the libsidplayfp trio live in devario-libs, and
# graphicsmagick lives in devario-entertainment; the guard follows the recipe, not the group.
GROUP = {
    "rtaudio": "devario-libs",
    "sdl_image": "devario-libs",
    "libexsid": "devario-libs",
    "libresidfp": "devario-libs",
    "libsidplayfp": "devario-libs",
    "graphicsmagick": "devario-entertainment",
    "libgee": "devario-libs",
    "babl": "devario-libs",
    "gegl": "devario-libs",
    "gexiv2": "devario-libs",
    "gmime3": "devario-libs",
    "gspell": "devario-libs",
    "libgexiv2": "devario-libs",
    "xapian-core": "devario-libs",
    "nettle3": "devario-libs",
}

# The gexiv2 row is served by the folder named after its row, gexiv2-common, because that
# split base's header output is what the repository database holds a row for.
FOLDER = {"gexiv2": "gexiv2-common"}

# A probe has to name a file the package really installs, which is not always the bare
# provision: SDL_image ships libSDL_image-1.2.so.0 and the libSDL_image.so linker name only.
PROBE_PATH = {"sdl_image": {"libSDL_image-1.2.so": "libSDL_image.so"}}

# Providers outside these recipes that publish only an unpinned provision, so a consumer here
# cannot name a versioned form of them without making itself uninstallable. util-linux-libs
# (libblkid, libmount, libfdisk), kmod (libkmod) and polkit (libpolkit-*) own recipe folders
# but no versioned provision, so their pins are a separate change with their own pkgrel bump.
# nettle3's SONAMEs are libnettle.so.8 and libhogweed.so.6, and its import lands
# the pair as 3.10.2-3. devario-utilities/sequoia-sqv names libnettle.so and
# libhogweed.so bare today: its binary needs libnettle.so.8, so it switches to
# the 8/6 provisions once the nettle3 stage publishes, and must never name nettle
# 4.0's libnettle.so=9-64 / libhogweed.so=7-64, which ship a library it cannot load.
# vulkan-icd-loader 1.4.364-1 publishes only bare libvulkan.so, so libplacebo names it bare.
# gtk4 1:4.24.1-2 publishes only bare libgtk-4.so, so libadwaita names it bare and pinning
# gtk4 itself is a separate change on that recipe with its own pkgrel bump.
# gtk3 1:3.24.52-3 likewise publishes only bare libgdk-3.so and libgtk-3.so, so gparted
# names both bare while its other eleven .so depends name the pinned forms their providers carry.
# exiv2 0.28.9-1 publishes only bare libexiv2.so, gdk-pixbuf2 2.44.8-3 only bare
# libgdk_pixbuf-2.0.so, jasper 4.2.9-2 only bare libjasper.so and poppler-glib 26.08.0-1
# only bare libpoppler-glib.so, so gexiv2, libgexiv2 and gegl name those four bare.
UNPINNED_PROVIDERS = {
    "libkrb5.so",
    "libvulkan.so",
    "libgtk-4.so",
    "libgdk-3.so",
    "libgtk-3.so",
    "libblkid.so",
    "libmount.so",
    "libfdisk.so",
    "libkmod.so",
    "libpolkit-agent-1.so",
    "libpolkit-gobject-1.so",
    "libexiv2.so",
    "libgdk_pixbuf-2.0.so",
    "libjasper.so",
    "libpoppler-glib.so",
}

ARRAY = re.compile(r"^(\s*)(\w+)(\+?)=\((.*?)\)", re.M | re.S)
ELEMENT = re.compile(r"'[^']*'|\"[^\"]*\"|[^\s'\"#]+")


def strip_comments(text):
    """Drop what bash would read as a comment, so an array's annotations are not elements."""
    cleaned = []
    for line in text.splitlines():
        kept, quote = [], None
        for ch in line:
            if quote:
                if ch == quote:
                    quote = None
            elif ch in "'\"":
                quote = ch
            elif ch == "#" and (not kept or kept[-1].isspace()):
                break
            kept.append(ch)
        cleaned.append("".join(kept))
    return "\n".join(cleaned)


def braces(word):
    """Expand the bash brace form a PKGBUILD array may hold, as bash would."""
    parts = []
    i = 0
    while i < len(word):
        if word[i] == "{" and "}" in word[i:]:
            end = word.index("}", i)
            parts.append(word[i + 1 : end].split(","))
            i = end + 1
        else:
            parts.append(word[i])
            i += 1
    out = [""]
    for part in parts:
        choices = part if isinstance(part, list) else (part,)
        out = [head + choice for head in out for choice in choices]
    return out


def arrays(recipe, key):
    """Every assignment to `key` in the recipe, top level or inside a package_* function."""
    text = strip_comments((recipe / "PKGBUILD").read_text())
    found = []
    for match in ARRAY.finditer(text):
        if match.group(2) != key:
            continue
        for element in ELEMENT.findall(match.group(4)):
            element = element.strip("'\"")
            if element:
                found.extend(braces(element))
    return found


class AbiSonamePins(unittest.TestCase):
    def recipes(self):
        for pkgbase in sorted(PINNED):
            group = GROUP.get(pkgbase, "devario-core")
            recipe = ROOT / group / FOLDER.get(pkgbase, pkgbase)
            name = "%s/%s" % (group, pkgbase)
            self.assertTrue(
                (recipe / "PKGBUILD").is_file(), f"{name}/PKGBUILD is missing"
            )
            self.assertTrue(
                (recipe / ".SRCINFO").is_file(), f"{name}/.SRCINFO is missing"
            )
            yield name, recipe

    def test_every_bare_provision_is_paired_with_its_versioned_form(self):
        for name, recipe in self.recipes():
            declared = arrays(recipe, "provides")
            for bare, pinned in PINNED[name.split("/")[1]].items():
                self.assertIn(bare, declared, f"{name} dropped the bare {bare} provide")
                self.assertIn(pinned, declared, f"{name} does not declare {pinned}")
            srcinfo = (recipe / ".SRCINFO").read_text()
            for pinned in PINNED[name.split("/")[1]].values():
                self.assertIn(
                    f"provides = {pinned}",
                    srcinfo,
                    f"{name}/.SRCINFO is stale: no {pinned}",
                )

    def test_every_pinned_provision_has_a_matching_probe(self):
        for name, recipe in self.recipes():
            pkgbase = name.split("/")[1]
            text = (recipe / "PKGBUILD").read_text()
            for bare, pinned in PINNED[pkgbase].items():
                soname = f"{bare}.{pinned.split('=')[1].split('-')[0]}"
                probed = PROBE_PATH.get(pkgbase, {}).get(bare, bare)
                probe = re.search(
                    r'_verify_soname\s+"?\$\{?pkgdir\}?[^"]*?/'
                    + re.escape(probed)
                    + r'"+\s+'
                    + re.escape(soname)
                    + r"\s*\|\|\s*return 1",
                    text,
                )
                self.assertIsNotNone(
                    probe, f"{name} declares {pinned} without probing {soname}"
                )

    def test_no_recipe_here_depends_on_an_unpinned_provision_it_can_pin(self):
        provided = {
            bare: pinned for pins in PINNED.values() for bare, pinned in pins.items()
        }
        for name, recipe in self.recipes():
            for dep in arrays(recipe, "depends"):
                base = re.split(r"[=<>]", dep)[0]
                if not base.endswith(".so"):
                    continue
                if base in provided:
                    self.assertEqual(
                        dep,
                        provided[base],
                        f"{name} depends on bare {base}, which is "
                        f"published as {provided[base]} in this recipe set",
                    )
                    continue
                if "=" in dep:
                    continue  # pinned against a provider that already declares the versioned form
                self.assertIn(
                    base,
                    UNPINNED_PROVIDERS,
                    f"{name} depends on bare {base} with no pinned provider "
                    "recorded for it",
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
