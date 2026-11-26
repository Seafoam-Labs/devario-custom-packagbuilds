# Maintainer: Antonio Rojas <arojas@archlinux.org>
# Maintainer: Felix Yan <felixonmars@archlinux.org>

pkgname=qt6-positioning
_pkgver=6.12.1
pkgver=${_pkgver/-/}
pkgrel=1
arch=(x86_64)
url='https://www.qt.io'
license=(GPL-3.0-only
         LGPL-3.0-only
         LicenseRef-Qt-Commercial
         Qt-GPL-exception-1.0)
pkgdesc='Provides access to position, satellite and area monitoring classes'
depends=(glibc
         libgcc
         libstdc++
         qt6-base)
makedepends=(cmake
             git
             ninja
             qt6-declarative
             qt6-serialport)
optdepends=('geoclue: geoclue2 plugin'
            'qt6-declarative: QML bindings'
            'qt6-serialport: NMEA plugin')
groups=(qt6)
_pkgfn=${pkgname/6-/}
source=(git+https://code.qt.io/qt/$_pkgfn#tag=v$_pkgver)
sha256sums=('61c86b41d1f55c000c5fe3a91e180822a4bf91d733e70dec40e28fd9d2932c77')

build() {
  cmake -B build -S $_pkgfn -G Ninja \
    -DCMAKE_MESSAGE_LOG_LEVEL=STATUS
  cmake --build build
}

package() {
  DESTDIR="$pkgdir" cmake --install build

  install -d "$pkgdir"/usr/share/licenses
  ln -s /usr/share/licenses/qt6-base "$pkgdir"/usr/share/licenses/$pkgname
}
