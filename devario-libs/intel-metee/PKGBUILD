# Maintainer: Bruno Pagani <archange@archlinux.org>
# Maintainer: Daniel Bermond <dbermond@archlinux.org>

pkgbase=intel-metee
pkgname=(
    'intel-metee'
    'intel-metee-doc')
pkgver=6.2.6
pkgrel=1
pkgdesc='Access library for Intel CSME HECI interface'
arch=('x86_64')
url='https://github.com/intel/metee/'
license=('Apache-2.0')
makedepends=(
    'cmake'
    'doxygen'
    'graphviz')
source=("https://github.com/intel/metee/archive/${pkgver}/${pkgname}-${pkgver}.tar.gz")
sha256sums=('adb5e2b4f3129616b7d3b095c8838a2041dc5240bfbdc67cd02aeeae807defc9')

build() {
    # fix error: "_FORTIFY_SOURCE" redefined [-Werror]
    # note: upstream forces _FORTIFY_SOURCE=2
    export CFLAGS="${CFLAGS/-Wp,-D_FORTIFY_SOURCE=?/}"
    export CXXFLAGS="${CXXFLAGS/-Wp,-D_FORTIFY_SOURCE=?/}"
    
    cmake -B build -S "metee-${pkgver}" \
        -G 'Unix Makefiles' \
        -DCMAKE_BUILD_TYPE='None' \
        -DCMAKE_INSTALL_PREFIX='/usr' \
        -DBUILD_DOCS='ON' \
        -DBUILD_SHARED_LIBS='ON' \
        -Wno-author
    cmake --build build
}

package_intel-metee() {
    depends=('glibc')
    
    DESTDIR="$pkgdir" cmake --install build
    mv "${pkgdir}/usr/share/doc" .
}

package_intel-metee-doc() {
    pkgdesc+=' (documentation)'
    
    install -d -m755 "${pkgdir}/usr/share"
    mv doc "${pkgdir}/usr/share"
}
