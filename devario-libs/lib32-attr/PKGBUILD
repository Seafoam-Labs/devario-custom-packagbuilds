# Maintainer: Thomas Bächler <thomas@archlinux.org>

_pkgbasename=attr
pkgname=lib32-$_pkgbasename
pkgver=2.6.0
pkgrel=1
pkgdesc='Extended attribute support library for ACL support (32-bit)'
arch=(x86_64)
url='https://savannah.nongnu.org/projects/attr'
license=('LGPL-2.1-or-later AND GPL-2.0-or-later')
depends=('lib32-glibc' $_pkgbasename)
makedepends=('git' 'gcc-multilib' 'gettext')
provides=('libattr.so')
validpgpkeys=('600CD204FBCEA418BD2CA74F154343260542DF34'  # Brandon Philips <brandon@ifup.co>
              'B902B5271325F892AC251AD441633B9FE837F581'  # Frysinger <vapier@gentoo.org>
              '259B3792B3D6D319212CC4DCD5BF9FEB0313653A') # Andreas Gruenbacher <andreas.gruenbacher@gmail.com>
source=("git+https://git.savannah.nongnu.org/git/attr.git?signed#tag=v${pkgver}")
sha256sums=('ccd84181352d72d01efd1eb72ec99c539f23eb483406100a10747509477cf644')

prepare() {
  cd "${srcdir}"/attr

  ./autogen.sh
}

build() {
  cd "${srcdir}"/attr

  export CC="gcc -m32"
  export PKG_CONFIG_PATH="/usr/lib32/pkgconfig"

  ./configure \
    --prefix=/usr \
    --libdir=/usr/lib32 \
    --libexecdir=/usr/lib32 \
    --sysconfdir=/etc
  make
}

package() {
  cd "${srcdir}"/attr

  make DESTDIR="${pkgdir}" install

  rm -rf "${pkgdir}"/{etc,usr/{bin,include,share}}
}
