# Maintainer: Florian Pritz <flo@xssn.at>
# Contributor: Jan de Groot <jgc@archlinux.org>
# Contributor: Alexander Baldeck <alexander@archlinux.org>

_pkgbasename=libxss
pkgname=lib32-$_pkgbasename
pkgver=1.2.5
pkgrel=1
pkgdesc="X11 Screen Saver extension library (32-bit)"
arch=(x86_64)
license=('X11')
url="https://gitlab.freedesktop.org/xorg/lib/libxscrnsaver"
depends=('lib32-libxext' $_pkgbasename)
makedepends=('xorg-util-macros' gcc-multilib)
source=("https://xorg.freedesktop.org/releases/individual/lib/libXScrnSaver-${pkgver}.tar.xz"{,.sig})
sha512sums=('1c0be0d15c5e7b50a3eb4a239e2c833c44b693b111c7f64c409f9abf8051356572acadebc8b295555683ff6bd4895acdbe32b15a538c971f15d8aa4e6b7fd51b'
            'SKIP')
validpgpkeys=('3AB285232C46AE43D8E192F4DAB0F78EA6E7E2D2') # "Alan Coopersmith <alan.coopersmith@oracle.com>"

build() {
  export CC="gcc -m32"
  export CXX="g++ -m32"
  export PKG_CONFIG_PATH="/usr/lib32/pkgconfig"

  cd "${srcdir}/libXScrnSaver-${pkgver}"
  ./configure --prefix=/usr --sysconfdir=/etc \
    --libdir=/usr/lib32
  make
}

package() {
  cd "${srcdir}/libXScrnSaver-${pkgver}"

  make DESTDIR="${pkgdir}" install

  rm -rf "${pkgdir}"/usr/{include,share,bin}
  mkdir -p "$pkgdir/usr/share/licenses"
  ln -s $_pkgbasename "$pkgdir/usr/share/licenses/$pkgname"
}
