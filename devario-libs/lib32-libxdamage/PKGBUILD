# Maintainer: Jan de Groot <jgc@archlinux.org>

_pkgbasename=libxdamage
pkgname=lib32-$_pkgbasename
pkgver=1.1.7
pkgrel=1
pkgdesc="X11 damaged region extension library (32-bit)"
arch=(x86_64)
url="https://xorg.freedesktop.org/"
license=('HPND-sell-variant')
depends=('lib32-libxfixes>=4.0.4' $_pkgbasename 'lib32-libx11' 'lib32-glibc')
makedepends=('xorgproto')
source=(${url}/releases/individual/lib/libXdamage-${pkgver}.tar.xz)
sha256sums=('127067f521d3ee467b97bcb145aeba1078e2454d448e8748eb984d5b397bde24')

build() {
  export CC="gcc -m32"
  export CXX="g++ -m32"
  export PKG_CONFIG="i686-pc-linux-gnu-pkg-config"

  cd "${srcdir}/libXdamage-${pkgver}"
  ./configure --prefix=/usr --sysconfdir=/etc --disable-static --libdir=/usr/lib32
  make
}

package() {
  cd "${srcdir}/libXdamage-${pkgver}"

  make DESTDIR="${pkgdir}" install || return 1
  rm -rf "${pkgdir}"/usr/{include,share,bin}
  mkdir -p "$pkgdir/usr/share/licenses"
  ln -s $_pkgbasename "$pkgdir/usr/share/licenses/$pkgname"
}
