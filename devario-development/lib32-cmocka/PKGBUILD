# Maintainer: David Runge <dvzrv@archlinux.org>

_name=cmocka
pkgname=lib32-cmocka
pkgver=2.0.2
pkgrel=1
pkgdesc='Elegant unit testing framework for C with support for mock objects'
url='https://cmocka.org/'
arch=(x86_64)
license=(Apache-2.0)
depends=(
  cmocka
  lib32-glibc
)
makedepends=(cmake)
provides=(libcmocka.so)
options=(!lto)
source=(https://cmocka.org/files/2.0/$_name-$pkgver.tar.xz{,.asc})
sha512sums=('d02d65f0881f18f30b9e46c325acfa349261339daa2c1bf3a4e6360976f13b31588e997415197220f6def156f77d9864994d4e3cfd09c8f16a8594d0a4789a16'
            'SKIP')
b2sums=('03bb0558c5bdb0d7ea222ae0e6a710106e63d3eb62333c91864488a33745120ab82f395388a984a9bd95ed1aedf228ee1ea42671ca6ae0112d33b7b06bf385c2'
        'SKIP')
validpgpkeys=('8DFF53E18F2ABC8D8F3C92237EE0FC4DCC014E3D') # Andreas Schneider <asn@cryptomilk.org>

build() {
  local cmake_options=(
    -B build
    -D CMAKE_BUILD_TYPE=Release
    -D CMAKE_INSTALL_LIBDIR=lib32
    -D CMAKE_INSTALL_PREFIX=/usr
    -D UNIT_TESTING=ON
    -S $_name-$pkgver
    -W no-dev
  )

  export CC='gcc -m32'
  export PKG_CONFIG_PATH='/usr/lib32/pkgconfig'

  cmake "${cmake_options[@]}"
  cmake --build build --verbose
}

check() {
  ctest --test-dir build --output-on-failure
}

package() {
  DESTDIR="$pkgdir" cmake --install build
  rm -rvf "$pkgdir/usr/include"
}
# vim: ts=2 sw=2 et:
