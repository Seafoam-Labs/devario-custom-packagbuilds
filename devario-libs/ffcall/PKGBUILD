# Maintainer: Jürgen Hötzel <juergen@archlinux.org>
# Maintainer: Carl Smedstad <carsme@archlinux.org>
# Contributor: Vesa Kaihlavirta <vegai@iki.fi>
# Contributor: Michael Baehr <usemike@spamblocked.com>

pkgname=ffcall
pkgver=2.5
pkgrel=1
pkgdesc="C library for implementing foreign function calls in embedded interpreters"
arch=('x86_64')
url="https://www.gnu.org/software/libffcall/"
license=('GPL-2.0-or-later')
depends=('glibc')
options=('!makeflags')
source=("https://ftp.gnu.org/gnu/libffcall/libffcall-${pkgver}.tar.gz"{,.sig})
sha256sums=('7f422096b40498b1389093955825f141bb67ed6014249d884009463dc7846879'
            'SKIP')
validpgpkeys=("9001B85AF9E1B83DF1BDA942F5BE8B267C6A406D") # Bruno Haible (Open Source Development) <bruno@clisp.org>

build() {
  cd "lib${pkgname}-${pkgver}"
  CFLAGS+=" -ffat-lto-objects" \
    ./configure \
    --prefix=/usr \
    --mandir=/usr/share/man \
    --with-pic \
    --disable-static
  make
}

check() {
  cd "lib${pkgname}-${pkgver}"
  make check
}

package() {
  cd "lib${pkgname}-${pkgver}"
  make DESTDIR="${pkgdir}" htmldir=/usr/share/doc/ffcall install
}
