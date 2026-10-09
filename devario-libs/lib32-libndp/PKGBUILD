# Maintainer: Maxime Gauduin <alucryd@archlinux.org>
# Contributor: oi_wtf <brainpower@gulli.com>
# Contributor: Jan Alexander Steffens (heftig) <heftig@archlinux.org>

pkgname=lib32-libndp
pkgver=1.9
pkgrel=1
pkgdesc="Library for Neighbor Discovery Protocol (32-bit)"
url="http://libndp.org/"
arch=(x86_64)
license=(LGPL-2.1-or-later)
depends=(
  lib32-glibc
  libndp
)
makedepends=(git)
source=("git+https://github.com/jpirko/libndp#tag=v$pkgver")
b2sums=('150f2bc4d0e67c44a694f6c6d0fb7f6927f7af2a8467b39fd77a41c0f5abb9df28d99432e444cff7328d0c8cd514516216d777cc416cfed3bb4cfa62007d6173')

prepare() {
  cd libndp
  ./autogen.sh
}

build() {
  local configure_options=(
    --prefix=/usr
    --libdir=/usr/lib32
    --sysconfdir=/etc
    --localstatedir=/var
    --libexecdir=/usr/lib
    --disable-static
  )

  cd libndp

  export CC="gcc -m32" CXX="g++ -m32"
  export PKG_CONFIG=i686-pc-linux-gnu-pkg-config

  ./configure "${configure_options[@]}"
  make
}

check() {
  cd libndp
  make check
}

package() {
  cd libndp
  make DESTDIR="$pkgdir" install
  rm -r "$pkgdir"/usr/{bin,include,share}
}

# vim:set sw=2 sts=-1 et:
