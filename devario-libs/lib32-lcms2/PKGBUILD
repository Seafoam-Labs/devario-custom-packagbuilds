# Maintainer: Laurent Carlier <lordheavym@archlinux.org>
# Contributor: Eric Bélanger <eric@archlinux.org>
# Contributor: Lukas Jirkovsky <l.jirkovsky@gmail.com>

pkgname=lib32-lcms2
pkgver=2.17
pkgrel=1
pkgdesc="Small-footprint color management engine, version 2 (32-bit)"
arch=('x86_64')
license=('MIT')
depends=('lib32-libtiff' 'lcms2')
provides=('liblcms2.so')
makedepends=('gcc-multilib')
url="https://www.littlecms.com"
source=("https://github.com/mm2/Little-CMS/releases/download/lcms${pkgver}/lcms2-${pkgver}.tar.gz")
sha512sums=('81885c70fb26a9b7d37a398f43ccb0d1d3ab8f43de7da8f760b26d053a0d7e0543e7d3b0cdcaf9b3b681a1b88f032134c5a3c1a6774a9abc66a8a3f10ba64398')

build() {
  export CC="gcc -m32"
  export CXX="g++ -m32"
  export PKG_CONFIG_PATH="/usr/lib32/pkgconfig"

  cd lcms2-${pkgver}

  ./configure --prefix=/usr \
    --libdir=/usr/lib32
  make
}

check() {
  cd lcms2-${pkgver}

  make check
}

package() {
  cd lcms2-${pkgver}

  make DESTDIR="${pkgdir}" install

  rm -rf "${pkgdir}"/usr/{include,share,bin}
  mkdir -p "${pkgdir}/usr/share/licenses"
  ln -s lcms2 "${pkgdir}/usr/share/licenses/${pkgname}"
}
