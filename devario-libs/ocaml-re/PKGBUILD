# Maintainer: Jürgen Hötzel <juergen@archlinux.org>

_pkgname=re
pkgname=ocaml-${_pkgname}
pkgver=1.14.0
pkgrel=3
pkgdesc="A regular expression library for OCaml"
arch=('x86_64')
url="https://github.com/ocaml/ocaml-re"
license=('LGPL2.1')
depends=('ocaml')
makedepends=('dune')
options=('!strip')
source=("${url}/archive/${pkgver}/${_pkgname}-${pkgver}.tar.gz")
sha256sums=('e32eb4c6f319ff74241da9e1b00032f990241347271baf3adb468faaaa616147')

build() {
  cd ${pkgname}-$pkgver
  dune build --profile release -p $_pkgname
}

package() {
  cd ${pkgname}-$pkgver

  DESTDIR="${pkgdir}" dune install --prefix '/usr' --libdir '/usr/lib/ocaml' '--docdir' '/usr/share/doc' --release
}
