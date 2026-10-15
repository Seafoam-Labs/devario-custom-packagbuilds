# Maintainer: Jan de Groot <jgc@archlinux.org>

_pkgbasename=libxcomposite
pkgname=lib32-$_pkgbasename
pkgver=0.4.7
pkgrel=1
pkgdesc="X11 Composite extension library (32-bit)"
arch=(x86_64)
url="https://xorg.freedesktop.org/"
license=('MIT' 'HPND-sell-variant')
depends=('lib32-libxfixes' $_pkgbasename 'lib32-libx11' 'lib32-glibc')
makedepends=('xorg-util-macros' gcc-multilib)
source=(${url}/releases/individual/lib/libXcomposite-${pkgver}.tar.xz)
sha512sums=('24a03e3242f22b113aa6a3f9341858c072730f0f0073a1a7b9d36b982cd5b77223151aad32b61d1a38bbcb9f8ffedaf67b882dcb95f197d80ece9dbc99332c36')

build() {
  export CC="gcc -m32"
  export CXX="g++ -m32"
  export PKG_CONFIG_PATH="/usr/lib32/pkgconfig"

  cd "${srcdir}/libXcomposite-${pkgver}"
  ./configure --prefix=/usr --sysconfdir=/etc --disable-static --libdir=/usr/lib32
  make
}

package() {
  cd "${srcdir}/libXcomposite-${pkgver}"

  make DESTDIR="${pkgdir}" install

  rm -rf "${pkgdir}"/usr/{include,share,bin}
  mkdir -p "$pkgdir/usr/share/licenses"
  ln -s $_pkgbasename "$pkgdir/usr/share/licenses/$pkgname"
}
