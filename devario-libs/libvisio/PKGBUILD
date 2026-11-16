# Maintainer: AndyRTR <andyrtr@archlinux.org>
# Contributor: Bartłomiej Piotrowski <bpiotrowski@archlinux.org>
# Contributor: ponsfoot <cabezon dot hashimoto at gmail dot com>
# Contributor: philacs

pkgname=libvisio
pkgver=0.1.12
pkgrel=1
pkgdesc='Library providing ability to interpret and import visio diagrams'
arch=('x86_64')
url="https://wiki.documentfoundation.org/DLP/Libraries/libvisio"
license=('MPL-2.0')
depends=('libxml2' 'icu' 'librevenge'
         'glibc' 'libstdc++' 'libgcc')
makedepends=('boost' 'gperf' 'doxygen' 'cppunit')
source=(https://dev-www.libreoffice.org/src/$pkgname/$pkgname-$pkgver.tar.xz)
sha256sums=('f59fa2e3baf95475256fe84ea0aa1214f43940bae94424f4026b2d633933df01')

prepare() {
  cd $pkgname-$pkgver
  autoreconf -fiv
}

build() {
  cd $pkgname-$pkgver
  ./configure --prefix=/usr
  sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0/g' libtool
  make
}

check() {
  cd $pkgname-$pkgver
  make check
}

package() {
  cd $pkgname-$pkgver
  make DESTDIR="$pkgdir" install
}
