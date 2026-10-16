# Maintainer: Jakub Klinkovský <lahwaacz@archlinux.org>

pkgname=cccl
pkgver=3.5.0
pkgrel=1
pkgdesc="CUDA Core Compute Libraries"
arch=(any)
url="https://github.com/NVIDIA/cccl"
license=(Apache-2.0)
makedepends=(cmake)
source=($pkgname-$pkgver.tar.gz::$url/archive/refs/tags/v$pkgver.tar.gz)
b2sums=('0e0c8eca00caef4094c1274dd6e95d33034daf8b1141e6e5c487bf1e46c90a68720d828e0397aa33c258d6c5dbaf04eed1d822da55f7aafa4b48639305f4cd68')

build() {
  local cmake_options=(
    -B build
    -S $pkgname-$pkgver
    -W no-dev
    -DCMAKE_BUILD_TYPE=None
    -DCMAKE_INSTALL_PREFIX=/usr
    -DCMAKE_INSTALL_INCLUDEDIR=include/$pkgname
    -DCCCL_ENABLE_EXAMPLES=OFF
    -DCCCL_ENABLE_TESTING=OFF
    -DTHRUST_ENABLE_EXAMPLES=OFF
    -DTHRUST_ENABLE_HEADER_TESTING=OFF
    -DTHRUST_ENABLE_TESTING=OFF
    -DCUB_ENABLE_EXAMPLES=OFF
    -DCUB_ENABLE_HEADER_TESTING=OFF
    -DCUB_ENABLE_TESTING=OFF
    -DLIBCUDACXX_ENABLE_LIBCUDACXX_TESTS=OFF
    # controls only enable_language(CUDA) in CMake, but we don't build anything
    -DLIBCUDACXX_ENABLE_CUDA=OFF
  )
  cmake "${cmake_options[@]}"
  cmake --build build
}

package() {
  DESTDIR="$pkgdir" cmake --install build
  install -vDm 644 $pkgname-$pkgver/LICENSE -t "$pkgdir"/usr/share/licenses/$pkgname/
}
