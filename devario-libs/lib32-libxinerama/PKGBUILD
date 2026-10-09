# Maintainer: Jan de Groot <jgc@archlinux.org>
# Contributor: Alexander Baldeck <alexander@archlinux.org>

_pkgbasename=libxinerama
pkgname=lib32-$_pkgbasename
pkgver=1.1.6
pkgrel=1
pkgdesc="X11 Xinerama extension library (32-bit)"
arch=(x86_64)
url="https://xorg.freedesktop.org/"
license=('MIT')
depends=('lib32-libxext' $_pkgbasename 'lib32-libx11' 'lib32-glibc')
makedepends=('xorg-util-macros' gcc-multilib)
source=(${url}/releases/individual/lib/libXinerama-${pkgver}.tar.xz)
sha512sums=('64bff837941625120da43b8876db4204bc5740bcf3147997fc4df1475f90d6d9e3f9caa8748c7ebbf69d681be8e5ab4bc40f82c56c367dddcec3ab27d1c71573')

build() {
  export CC="gcc -m32"
  export CXX="g++ -m32"
  export PKG_CONFIG_PATH="/usr/lib32/pkgconfig"

  cd "${srcdir}/libXinerama-${pkgver}"
  ./configure --prefix=/usr --libdir=/usr/lib32
  make
}

package() {
  cd "${srcdir}/libXinerama-${pkgver}"

  make DESTDIR="${pkgdir}" install

  rm -rf "${pkgdir}"/usr/{include,share,bin}
  mkdir -p "$pkgdir/usr/share/licenses"
  ln -s $_pkgbasename "$pkgdir/usr/share/licenses/$pkgname"
}
