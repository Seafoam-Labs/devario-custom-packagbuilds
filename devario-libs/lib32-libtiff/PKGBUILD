# Maintainer: Levente Polyak <anthraxx[at]archlinux[dot]org>
# Contributor: Eric Bélanger <eric@archlinux.org>
# Contributor: dorphell <dorphell@archlinux.org>

_pkgname=libtiff
pkgname=lib32-${_pkgname}
pkgver=4.7.2
pkgrel=1
pkgdesc='Library for manipulation of TIFF images (32-bit)'
url='http://www.simplesystems.org/libtiff/'
arch=('x86_64')
license=('libtiff')
depends=(
  libtiff=$pkgver
  'lib32-glibc'
  'lib32-gcc-libs'
  'lib32-libjpeg-turbo'
  'lib32-xz'
  'lib32-zlib'
  'lib32-zstd'
)
makedepends=(
  'freeglut'
  'git'
  'glu'
  'mesa'
)
provides=('libtiff.so' 'libtiffxx.so')
source=("git+https://gitlab.com/libtiff/libtiff.git?signed#tag=v${pkgver}")
sha512sums=('07e644950f6e693daa66aca84594b710c85e854175b14a358a1d9d27927b290935f9873e5c09257e0e5b71cfa0710336ec9d83afc29834332f8f01650c66b148')
b2sums=('1d5b034b62714984eabbc4fc503e06747884126bfd79cace67f29e0017c2b5067cd88f50e53a716f23f0e6d1244939b37a94e86d20118abe1af798a0692c57fa')
validpgpkeys=(
  'EBDFDB21B020EE8FD151A88DE301047DE1198975' # Bob Friesenhahn <bfriesen@simple.dallas.tx.us>
  'B1FA7D81EEB8E66399178B9733EBBFC47B3DD87D' # Even Rouault <even.rouault@spatialys.com>
)

prepare() {
  cd libtiff
  autoreconf -fiv
}

build() {
  local configure_options=(
    --prefix=/usr
    --sysconfdir=/etc
    --enable-ld-version-script
    --mandir=/usr/share/man
    --with-docdir=/usr/share/doc/${pkgname}
    --libdir=/usr/lib32
    --includedir=/usr/include/libtiff32
  )

  export CC="gcc -m32"
  export CXX="g++ -m32"
  export PKG_CONFIG_PATH="/usr/lib32/pkgconfig"

  cd libtiff
  ./configure "${configure_options[@]}"
  sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0/g' libtool
  make
}

check() {
  cd libtiff
  make check
}

package() {
  depends+=('libjpeg.so')
  cd libtiff
  make DESTDIR="${pkgdir}" install

  rm -rf "${pkgdir}"/usr/{share,bin}
  install -Dm 644 LICENSE.md -t "${pkgdir}/usr/share/licenses/${pkgname}/"
}

# vim: ts=2 sw=2 et:
