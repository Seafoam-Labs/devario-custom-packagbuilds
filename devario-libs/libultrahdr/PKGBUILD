# Maintainer: Antonio Rojas <arojas@archlinux.org>
# Maintainer: Daniel Bermond <dbermond@archlinux.org>

pkgname=libultrahdr
pkgver=2.0.2
pkgrel=1
pkgdesc='The reference codec for the Ultra HDR format'
arch=(x86_64)
url='https://github.com/google/libultrahdr'
license=(Apache-2.0)
depends=(glibc
         libgcc
         libjpeg-turbo
         libstdc++)
# TODO: libheif support requires unmerged https://github.com/strukturag/libheif/pull/1503
makedepends=(cmake
             git
             gtest)
source=(git+https://github.com/google/libultrahdr#tag=v$pkgver
        unbundle-gtest.patch)
sha256sums=('ae22b616a77ea0fd35dc98acccecf983c6ebd7f68ad82e0f57e77755133566b2'
            'bc32ce7083a0eca06ec2c9423442e044e9dd914ad6d83cc02be8f49043b7a2c8')

prepare() {
  patch -d libultrahdr -p1 < unbundle-gtest.patch
}

build() {
  cmake -B build -S $pkgname \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DCMAKE_BUILD_TYPE=None \
    -DUHDR_BUILD_TESTS=ON \
    -Wno-author
  cmake --build build
}

check() {
    ctest --test-dir build --output-on-failure
}

package() {
  DESTDIR="$pkgdir" cmake --install build
}
