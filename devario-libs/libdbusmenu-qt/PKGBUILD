# Maintainer: Antonio Rojas <arojas@archlinux.org>
# Contributor: Andrea Scarpino <andrea@archlinux.org>

pkgbase=libdbusmenu-qt
pkgname=(libdbusmenu-qt5)
pkgver=0.9.3+16.04.20160218
pkgrel=8
pkgdesc='A library that provides a Qt implementation of the DBusMenu spec'
arch=(x86_64)
url='https://github.com/desktop-app/libdbusmenu-qt'
license=(GPL)
depends=(glibc
         libgcc
         libstdc++
         qt5-base)
makedepends=(cmake)
source=(http://archive.ubuntu.com/ubuntu/pool/main/libd/$pkgbase/${pkgbase}_$pkgver.orig.tar.gz)
sha256sums=('a8e6358a31c44ccdf1bfc46c95a77a6bfc7fc1f536aadb913ed4f4405c570cf6')

build() {
  cmake -B build $pkgbase-$pkgver \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DUSE_QT5=ON \
    -DWITH_DOC=OFF \
    -DCMAKE_POLICY_VERSION_MINIMUM=3.5
  cmake --build build
}

package_libdbusmenu-qt5() {
  DESTDIR="$pkgdir" cmake --install build
}
