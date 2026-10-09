# Maintainer: Daniel Bermond <dbermond@archlinux.org>

pkgname=mujs
pkgver=1.3.10
pkgrel=1
pkgdesc='An embeddable Javascript interpreter in C'
arch=('x86_64')
url='https://mujs.com/'
license=('ISC')
depends=(
    'glibc'
    'readline')
makedepends=('python')
source=("https://mujs.com/downloads/mujs-${pkgver}.tar.gz"
        '010-mujs-use-arch-flags.patch')
sha256sums=('6e36c15dbb84ff859320297c900852f241b131a7b6ddaea669ac9a65bd75571c'
            '711d596fb6f473acfec4a618990389a7911defbfec49018f12c97b3d35ed5491')

prepare() {
    patch -d "${pkgname}-${pkgver}" -Np1 -i "${srcdir}/010-mujs-use-arch-flags.patch"
}

build() {
    make -C "${pkgname}-${pkgver}" prefix='/usr' release
}

package() {
    make -C "${pkgname}-${pkgver}" DESTDIR="$pkgdir" prefix='/usr' install-shared
    install -d -m755 "${pkgdir}/usr/share/doc"
    install -D -m644 "${pkgname}-${pkgver}/COPYING" "${pkgdir}/usr/share/licenses/mujs/LICENSE"
    cp -dr --no-preserve='ownership' "${pkgname}-${pkgver}/docs" "${pkgdir}/usr/share/doc/${pkgname}"
}
