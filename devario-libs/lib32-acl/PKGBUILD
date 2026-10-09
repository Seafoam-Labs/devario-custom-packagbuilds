# Maintainer: Thomas Bächler <thomas@archlinux.org>

pkgname=lib32-acl
pkgver=2.4.0
pkgrel=1
pkgdesc='Access control list libraries (32-bit)'
arch=('x86_64')
url='https://savannah.nongnu.org/projects/acl'
license=('LGPL-2.1-or-later AND GPL-2.0-or-later')
depends=('acl')
makedepends=('git' 'gcc-multilib' 'lib32-attr')
provides=('libacl.so')
validpgpkeys=('600CD204FBCEA418BD2CA74F154343260542DF34'  # Brandon Philips <brandon@ifup.co>
              'B902B5271325F892AC251AD441633B9FE837F581'  # Frysinger <vapier@gentoo.org>
              '259B3792B3D6D319212CC4DCD5BF9FEB0313653A') # Andreas Gruenbacher <andreas.gruenbacher@gmail.com>
source=("git+https://git.savannah.nongnu.org/git/acl.git?signed#tag=v${pkgver}")
sha256sums=('0637d58b5a2c1c595f679f297bd521f2b730a7315c6bc42ab30e2601c0fd2ba7')

prepare() {
  cd "${srcdir}"/acl

  ./autogen.sh
}

build() {
  cd "${srcdir}"/acl

  export CC="gcc -m32"
  export PKG_CONFIG_PATH="/usr/lib32/pkgconfig"

  ./configure \
    --prefix=/usr \
    --libdir=/usr/lib32 \
    --libexecdir=/usr/lib32
  sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0/g' libtool
  make 
}

package() {
  cd "${srcdir}"/acl

  make DESTDIR="${pkgdir}" install

  rm -rf "${pkgdir}"/usr/{bin,include,share}
}
