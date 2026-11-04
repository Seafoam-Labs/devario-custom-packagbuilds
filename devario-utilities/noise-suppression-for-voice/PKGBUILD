# Maintainer: Antonio Rojas <arojas@archlinux.org>
# Contributor: WorMzy Tykashi <wormzy.tykashi@gmail.com>

pkgname=noise-suppression-for-voice
pkgver=1.22
pkgrel=1
pkgdesc='A real-time noise suppression plugin for voice'
arch=(x86_64)
url='https://github.com/werman/noise-suppression-for-voice'
license=(GPL-3.0-only)
depends=(freetype2
         glibc
         libatomic
         libgcc
         libstdc++)
makedepends=(cmake
             git
             libx11
             libxcursor
             libxinerama
             libxrandr)
source=(git+https://github.com/werman/noise-suppression-for-voice#tag=v$pkgver)
sha256sums=('ce52e88878930187234f9588f0c343bb7b35b0f9dbae4283d10f0cba5db41baf')

build() {
  cmake -B build -S $pkgname \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DCMAKE_BUILD_TYPE=None
  cmake --build build
}

package() {
  DESTDIR="$pkgdir" cmake --install build
}
