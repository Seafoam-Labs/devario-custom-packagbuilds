# Maintainer: Bruno Pagani <archange@archlinux.org>
# Maintainer: Jakub Klinkovský <lahwaacz at archlinux dot org>

pkgname=sz
pkgver=3.3.2
pkgrel=2
pkgdesc="Modular parametrizable lossy compressor framework for scientific data"
arch=(x86_64)
url="https://szcompressor.org/"
license=(LicenseRef-BSD-3-Clause-UChicago-Argonne)
depends=(
  glibc
  gsl  # not linked to, but required from cmake
  hdf5
  libgcc
  libgomp
  libstdc++
  zstd
)
makedepends=(
  cmake
  gtest
  ninja
)
source=($pkgname-$pkgver.tar.gz::https://github.com/szcompressor/SZ3/archive/refs/tags/v$pkgver.tar.gz)
b2sums=('c5234f58d196682ae02834df2738476740446e8ca6beea9435aafabf0d6fedd5799599e9f83ef4c0c769fca6b44ce5cdb941ec85113239c7e80467ab26edfcb7')

build() {
  local cmake_options=(
    -B build
    -S SZ3-$pkgver
    -G Ninja
    -W no-dev
    -DCMAKE_BUILD_TYPE=None
    -DCMAKE_INSTALL_PREFIX=/usr
    -DBUILD_TESTING=ON
    -DBUILD_H5Z_FILTER=ON
    -DBUILD_MDZ=ON
  )
  cmake "${cmake_options[@]}"
  cmake --build build
}

check() {
  ctest --test-dir build --output-on-failure
}

package() {
  DESTDIR="$pkgdir" cmake --install build
  install -vDm 644 SZ3-$pkgver/copyright-and-BSD-license.txt -t "$pkgdir"/usr/share/licenses/$pkgname/
}
