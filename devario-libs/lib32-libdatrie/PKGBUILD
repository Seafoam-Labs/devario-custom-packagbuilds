# Maintainer: Maxime Gauduin <alucryd@archlinux.org>
# Contributor: Jan de Groot <jgc@archlinux.org>
# Contributor: Chaiwat Suttipongsakul <cwt114@gmail.com>

pkgname=lib32-libdatrie
pkgver=0.2.14
pkgrel=1
pkgdesc='Implementation of double-array structure for representing trie, as proposed by Junichi Aoe.'
url='https://linux.thai.net/projects/datrie'
license=('LGPL')
arch=('x86_64')
depends=('lib32-glibc' 'libdatrie')
provides=('libdatrie.so')
source=("https://linux.thai.net/pub/thailinux/software/libthai/libdatrie-${pkgver}.tar.xz")
sha256sums=('f04095010518635b51c2313efa4f290b7db828d6273e39b2b8858f859dfe81d5')

build() {
  cd libdatrie-${pkgver}

  export CC='gcc -m32'
  export CXX='g++ -m32'
  export PKG_CONFIG="i686-pc-linux-gnu-pkg-config"

  ./configure \
    --prefix='/usr' \
    --libdir='/usr/lib32' \
    --disable-static
  make
}

package() {
  cd libdatrie-${pkgver}

  make DESTDIR="${pkgdir}" install -j1
  rm -rf "${pkgdir}"/usr/{bin,include,share}
}

# vim:set sw=2 sts=-1 et:
