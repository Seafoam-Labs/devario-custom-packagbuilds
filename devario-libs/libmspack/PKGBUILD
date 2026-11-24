# Maintainer: Jan Alexander Steffens (heftig) <heftig@archlinux.org>
# Contributor: AndyRTR <andyrtr@archlinux.org>

pkgname=libmspack
epoch=1
pkgver=1.12
pkgrel=1
pkgdesc='A library for Microsoft compression formats'
url='https://www.cabextract.org.uk/libmspack/'
arch=('x86_64')
license=('LGPL-2.1-only')
depends=('glibc')
makedepends=('git')
provides=('libmspack.so')
source=("git+https://github.com/kyz/libmspack#tag=v${pkgver}")
sha256sums=('4c2c02daf1ab18d4fb9a7e0d5500113395969e213d292fef25c411004d79f004')

pkgver() {
  cd "${pkgname}"
  git describe --tags | sed 's/^v//;s/[^-]*-g/r&/;s/-/+/g'
}

prepare() {
  cd "${pkgname}/${pkgname}"
  autoreconf -vfi
}

build() {
  cd "${pkgname}/${pkgname}"
  ./configure \
    --prefix=/usr \
    --sysconfdir=/etc \
    --localstatedir=/var \
    --disable-static
  sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0/g' libtool
  make
}

check() {
  cd "${pkgname}/${pkgname}"
  make check
}

package() {
  cd "${pkgname}/${pkgname}"
  make DESTDIR="${pkgdir}" install
}
