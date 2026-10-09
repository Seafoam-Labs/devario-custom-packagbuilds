# Maintainer: Alexander F. Rødseth <xyproto@archlinux.org>
# Contributor: Vincent B. <vb@luminar.eu.org>

pkgname=opam
pkgver=2.6.1
pkgrel=1
pkgdesc='OCaml package manager'
arch=(x86_64)
url='https://opam.ocaml.org/'
license=(LGPL-2.1-only)
depends=(bubblewrap libgcc libstdc++ glibc ocaml-compiler-libs unzip)
makedepends=(git)
optdepends=('darcs: For downloading packages with darcs'
            'git: For downloading packages with git'
            'mercurial: For downloading packages with mercurial'
            'rsync: For downloading packages with rsync')
source=("https://github.com/ocaml/opam/releases/download/${pkgver%_*}/opam-full-${pkgver/_/-}.tar.gz")
b2sums=('27a33f25322fcf326b36921840744dbf4d63b3b4b4943d6198e43afa34a7b7f28e78207de40d6c4bd38fcd7135c453430b3f96c6afdac958e694a3d4dd627231')

build() {
  cd opam-full-${pkgver%_*}
  ./configure --prefix=/usr --with-mccs --with-vendored-deps
  make all -j1
}

package() {
  make -C opam-full-${pkgver%_*} DESTDIR="$pkgdir" install
}
