# Maintainer: Alexander F. Rødseth <xyproto@archlinux.org>
# Contributor: David Runge <dave@sleepmap.de>
# Contributor: Ray Rashif <schiv@archlinux.org>

pkgname=calf
pkgver=0.90.9
pkgrel=2
pkgdesc='LV2 plug-in suite'
arch=(x86_64)
url='http://calf-studio-gear.org' # http only
_url="https://github.com/calf-studio-gear/calf"
groups=(lv2-plugins pro-audio)
license=(GPL-2.0-or-later LGPL-2.0-or-later)
depends=(expat fluidsynth glibc hicolor-icon-theme libgcc libstdc++)
makedepends=(cmake git lv2)
source=("git+$_url#tag=$pkgver")
b2sums=('a62f3617959a73a0b0f23ef4976944f31d9c3bc37d14cf316eee428aa197cfda4e9ebccce12a17d733567523480c3c48d99ada05a0501c709f4f8ab6d2f22a77')

build() {
  cmake \
    -B build \
    -D CMAKE_BUILD_TYPE=None \
    -D CMAKE_INSTALL_PREFIX=/usr \
    -D WANT_EXPERIMENTAL=ON \
    -D WANT_GUI=OFF \
    -S $pkgname \
    -W no-dev
  make -C build
}

package() {
  DESTDIR="$pkgdir" cmake --install build
  install -Dm644 $pkgname/{AUTHORS,ChangeLog,README.md} -t "$pkgdir/usr/share/doc/$pkgname"
}
