# Maintainer: Maxime Gauduin <alucryd@archlinux.org>
# Contributor: Jan de Groot <jgc@archlinux.org>
# Contributor: Chaiwat Suttipongsakul <cwt114@gmail.com>

pkgname=lib32-libthai
pkgver=0.1.30
pkgrel=1
pkgdesc='Thai language support routines'
url='https://linux.thai.net/projects/libthai'
arch=('x86_64')
license=('LGPL')
depends=('lib32-libdatrie')
makedepends=('autoconf-archive' 'git')
provides=('libthai.so')
source=("git+https://github.com/tlwg/libthai.git#tag=v${pkgver}")
sha256sums=('b949f005383400df249e7c925f4228db4ccc6cbe395d2ad7b893dfbc0c353615')

prepare() {
  cd libthai

  ./autogen.sh
}

build() {
  cd libthai

  export CC='gcc -m32'
  export CXX='g++ -m32'
  export PKG_CONFIG="i686-pc-linux-gnu-pkg-config"

  ./configure \
    --prefix='/usr' \
    --libdir='/usr/lib32' \
    --disable-static \
    --disable-doxygen-doc
  make
}

package() {
  make DESTDIR="${pkgdir}" -C libthai install
  rm -rf "${pkgdir}"/usr/{include,share}
}

# vim:set sw=2 sts=-1 et:
