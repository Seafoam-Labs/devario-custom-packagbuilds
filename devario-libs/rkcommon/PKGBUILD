# Maintainer: Daniel Bermond <dbermond@archlinux.org>
# Maintainer: Bruno Pagani <archange@archlinux.org>

pkgname=rkcommon
pkgver=1.15.4
pkgrel=1
pkgdesc='Intel RenderKit common C++/CMake infrastructure'
arch=('x86_64')
url='https://github.com/ospray/rkcommon/'
license=('Apache-2.0')
depends=(
    'glibc'
    'libgcc'
    'libstdc++'
    'onetbb')
makedepends=(
    'cmake'
    'git')
source=("https://github.com/ospray/rkcommon/archive/v${pkgver}/${pkgname}-${pkgver}.tar.gz")
sha256sums=('d584cc3620e56f12f07b84358b33a14de8aed29149693a1fe6eeed64ef74ae9b')

build() {
    cmake -B build -S "${pkgname}-${pkgver}" \
        -G 'Unix Makefiles' \
        -DCMAKE_BUILD_TYPE:STRING='None' \
        -DCMAKE_INSTALL_PREFIX:PATH='/usr' \
        -Wno-author
    cmake --build build
}

check() {
    ctest --test-dir build --output-on-failure
}

package() {
    DESTDIR="$pkgdir" cmake --install build
}
