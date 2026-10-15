# Contributor: Jan de Groot <jgc@archlinux.org>

_pkgbasename=libxtst
pkgname=lib32-$_pkgbasename
pkgver=1.2.5
pkgrel=2
pkgdesc="X11 Testing -- Resource extension library (32-bit)"
arch=(x86_64)
url="https://xorg.freedesktop.org/"
license=('custom')
depends=('lib32-libxext' 'lib32-libxi' 'lib32-libxfixes' $_pkgbasename)
makedepends=('gcc-multilib' 'xorg-util-macros')
source=(${url}/releases/individual/lib/libXtst-${pkgver}.tar.xz{,.sig})
sha256sums=('b50d4c25b97009a744706c1039c598f4d8e64910c9fde381994e1cae235d9242'
            'SKIP')
validpgpkeys=('4A193C06D35E7C670FA4EF0BA2FB9E081F2D130E') # Alan Coopersmith <alan.coopersmith@oracle.com>

build() {
  cd "${srcdir}/libXtst-${pkgver}"

  export CC="gcc -m32"
  export PKG_CONFIG_PATH="/usr/lib32/pkgconfig"

  ./configure --prefix=/usr --disable-static \
    --libdir=/usr/lib32
  make
}

package() {
  cd "${srcdir}/libXtst-${pkgver}"

  make DESTDIR="${pkgdir}" install

  rm -rf "${pkgdir}"/usr/{include,share}

  mkdir -p "$pkgdir/usr/share/licenses"
  ln -s $_pkgbasename "$pkgdir/usr/share/licenses/$pkgname"
}
