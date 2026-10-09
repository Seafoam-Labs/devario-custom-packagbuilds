# Maintainer: David Runge <dvzrv@archlinux.org>
# Contributor: Jan Alexander Steffens (heftig) <jan.steffens@gmail.com>

_name=alsa-plugins
pkgname=lib32-alsa-plugins
pkgver=1.2.12
pkgrel=1
pkgdesc="Additional ALSA plugins (32-bit)"
arch=(x86_64)
url="https://www.alsa-project.org"
license=(
  GPL-2.0-or-later
  LGPL-2.1-or-later
)
depends=(
  "alsa-plugins=1:$pkgver"
  lib32-glibc
)
makedepends=(
  lib32-alsa-lib
  lib32-dbus
  lib32-jack
  lib32-libavtp
  lib32-libpulse
  lib32-libsamplerate
  lib32-speexdsp
)
optdepends=(
  'lib32-dbus: for maemo plugin'
  'lib32-jack: for pcm_jack plugin'
  'lib32-libavtp: for pcm_aaf plugin'
  'lib32-libsamplerate: for rate_samplerate plugin'
  'lib32-libpulse: for conf_pulse, ctl_pulse and pcm_pulse plugins'
  'lib32-speexdsp: for pcm_speex and rate_speexrate plugins'
)
source=(https://www.alsa-project.org/files/pub/plugins/$_name-$pkgver.tar.bz2{,.sig})
sha512sums=('b2064eb32662662f422f6e7c71f503d82c68d7a7059c8197bdd61ee08735b3ee104c6a5f9e3451e81124634514b91fc89d05d33041d9c2bb0f55b3c2ac3271b1'
            'SKIP')
b2sums=('ee9514d7cd73881840b17d86d52d3557936ce666ae5027b423903f2dedc74b112a8592d66dd2514744057e4bcebaf5c689f39fcc9027e05106cc0a0090470f34'
        'SKIP')
validpgpkeys=('F04DF50737AC1A884C4B3D718380596DA6E59C91') # ALSA Release Team (Package Signing Key v1) <release@alsa-project.org>

prepare() {
  cd $_name-$pkgver
  autoreconf -fiv
}

build() {
  local configure_options=(
    --prefix=/usr
    --libdir=/usr/lib32
    --sysconfdir=/etc
    --enable-maemo-plugin
  )

  cd $_name-$pkgver

  export CC='gcc -m32'
  export PKG_CONFIG=i686-pc-linux-gnu-pkg-config

  ./configure "${configure_options[@]}"
  make
}

package() {
  depends+=(
    lib32-alsa-lib libasound.so
  )

  make DESTDIR="$pkgdir" install -C $_name-$pkgver
  rm -rv "$pkgdir"/{etc,usr/share}
}
# vim:set sw=2 et:
