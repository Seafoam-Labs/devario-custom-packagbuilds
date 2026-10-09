# Maintainer: Jürgen Hötzel <juergen@archlinux.org>

pkgname=ocaml-integers
pkgver=0.8.0
pkgrel=1
pkgdesc='Various signed and unsigned integer types for OCaml'
arch=('x86_64')
url=https://github.com/ocamllabs/ocaml-integers
license=('custom')
options=('!strip' '!debug')
depends=('ocaml-stdlib-shims')
makedepends=('dune' 'ocaml-topkg' 'ocaml-findlib' 'ocaml-compiler-libs' 'ocamlbuild' 'opam')
source=("$pkgname-$pkgver.tar.gz::https://github.com/ocamllabs/$pkgname/archive/$pkgver.tar.gz")
sha256sums=('04a1a6d5cc1ecfd3f354a83caed27e59995bb26adec64d88193ccc36268929fa')


build() {
  cd ${pkgname}-$pkgver
  dune build --profile release
}

package() {
  cd ${pkgname}-$pkgver

  opam-installer --prefix="${pkgdir}/usr" \
		 --libdir="${pkgdir}$(ocamlc -where)" \
		 --docdir="${pkgdir}/usr/share/doc" \
		 --stubsdir="${pkgdir}$(ocamlc -where)/stublibs" \
		 ./_build/default/integers.install
  install -Dm644 LICENSE.md "${pkgdir}/usr/share/licenses/${pkgname}"/LICENSE.md
}
