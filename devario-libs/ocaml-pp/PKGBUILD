# Maintainer: Konstantin Gizdov <arch at kge dot pw>
_pkgname='pp'
pkgname="ocaml-${_pkgname}"
pkgver=2.0.0
pkgrel=6
pkgdesc="OCaml Pretty printing: a lean alternative to the Format module of the OCaml standard library."
arch=('x86_64')
url="https://github.com/ocaml-dune/pp"
license=('MIT')
makedepends=('dune' 'ocaml')
depends=('glibc')
options=('!strip' '!debug')
source=("${pkgname}-${pkgver}.tar.gz::${url}/archive/${pkgver}/${pkgname}-${pkgver}.tar.gz")
sha512sums=('0a407e2674e71050ba17b768e473e9e856c7a050c7e9d712e7649424b9207d272a0091f97452ae8939693c74d5007e2616398a2dc7e9de6c5880588510887d29')

build() {
    cd "${srcdir}/${_pkgname}-${pkgver}"
    dune build -p "${_pkgname}"
}

package() {
    cd "${srcdir}/${_pkgname}-${pkgver}"
    DESTDIR="${pkgdir}" dune install --prefix "/usr" --libdir="$(ocamlc -where)"

    install -dm755 "${pkgdir}/usr/share/"
    mv "${pkgdir}/usr/doc" "${pkgdir}/usr/share/"

    install -dm755 "${pkgdir}/usr/share/licenses/${pkgname}"
    ln -s /usr/share/doc/pp/LICENSE.md "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
}
