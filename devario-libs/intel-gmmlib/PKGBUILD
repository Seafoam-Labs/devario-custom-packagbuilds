# Maintainer: Bruno Pagani <archange@archlinux.org>
# Maintainer: Daniel Bermond <dbermond@archlinux.org>

pkgname=intel-gmmlib
pkgver=22.10.0
pkgrel=1
pkgdesc='Intel Graphics Memory Management Library'
arch=('x86_64')
url='https://github.com/intel/gmmlib/'
license=('MIT')
depends=(
    'glibc'
    'libgcc'
    'libstdc++')
makedepends=(
    'cmake')
provides=('gmmlib')
conflicts=('gmmlib')
replaces=('gmmlib')
options=('!emptydirs')
source=("https://github.com/intel/gmmlib/archive/intel-gmmlib-${pkgver}/${pkgname}-${pkgver}.tar.gz")
sha256sums=('893e3c5a24b408ac312a0318b70f38f427f297646e323f31e79d3a06a92c1543')

build() {
    cmake -B build -S "gmmlib-${pkgname}-${pkgver}" \
        -G 'Unix Makefiles' \
        -DCMAKE_BUILD_TYPE='Release' \
        -DCMAKE_INSTALL_PREFIX='/usr' \
        -DRUN_TEST_SUITE='ON' \
        -Wno-dev
    cmake --build build
}

package() {
    DESTDIR="$pkgdir" cmake --install build
    install -D -m644 "gmmlib-${pkgname}-${pkgver}/LICENSE.md" -t "${pkgdir}/usr/share/licenses/${pkgname}"
}
