# Maintainer: Antonio Rojas <arojas@archlinux.org>

pkgname=qt6-graphs
_pkgver=6.12.1
pkgver=${_pkgver/-/}
pkgrel=1
arch=(x86_64)
url='https://www.qt.io'
license=(GPL-3.0-only
         LGPL-3.0-only
         LicenseRef-Qt-Commercial
         Qt-GPL-exception-1.0)
pkgdesc='Qt Graphs for data visualization'
depends=(glibc
         libstdc++
         qt6-base
         qt6-declarative
         qt6-quick3d)
makedepends=(cmake
             git
             ninja
             qt6-shadertools)
groups=(qt6)
_pkgfn=${pkgname/6-/}
source=(git+https://code.qt.io/qt/$_pkgfn#tag=v$_pkgver)
sha256sums=('fa1aa0e8b8b936df7c1cc6c914c19d8d00b47e1a57b0207b7bc829a63cff1bf9')

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
