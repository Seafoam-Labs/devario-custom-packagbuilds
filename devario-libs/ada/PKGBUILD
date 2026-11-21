# Maintainer: Sven-Hendrik Haase <svenstaro@archlinux.org>
pkgname=ada
pkgver=4.1.1
pkgrel=1
pkgdesc='WHATWG-compliant and fast URL parser written in modern C++'
arch=('x86_64')
url="https://github.com/ada-url/ada"
license=('Apache-2.0')
depends=('glibc' 'libgcc' 'libstdc++')
makedepends=('cmake')
source=("$pkgname-$pkgver.tar.gz::$url/archive/refs/tags/v$pkgver.tar.gz")
b2sums=('06e46a31a0f68ab3cfdd6e9f0f80ee6b12f36f95dd11f5f6b3eced4638d1deebe92d98a486e617ffcf949a4766b5eb80e8bb6ac4887a0d09e87a84256fc59a63')

build() {
  cmake -B build -S $pkgname-$pkgver \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX='/usr' \
    -DBUILD_SHARED_LIBS=ON
  cmake --build build
}

package() {
  DESTDIR="$pkgdir" cmake --install build
  install -Dm644 $pkgname-$pkgver/LICENSE* -t "$pkgdir/usr/share/licenses/$pkgname/"
}
