#Maintainer: Jan de Groot <jgc@archlinux.org>

_pkgbasename=libxfixes
pkgname=lib32-$_pkgbasename
pkgver=6.0.2
pkgrel=1
pkgdesc="X11 miscellaneous 'fixes' extension library (32-bit)"
arch=('x86_64')
url="https://xorg.freedesktop.org/"
license=('custom')
depends=('lib32-libx11' $_pkgbasename)
makedepends=('pkg-config' gcc-multilib )
source=(${url}/releases/individual/lib/libXfixes-${pkgver}.tar.xz{,.sig})
sha256sums=('39f115d72d9c5f8111e4684164d3d68cc1fd21f9b27ff2401b08fddfc0f409ba'
            'SKIP')
validpgpkeys=('3AB285232C46AE43D8E192F4DAB0F78EA6E7E2D2') # "Alan Coopersmith <alan.coopersmith@oracle.com>"

build() {
  export CC="gcc -m32"
  export CXX="g++ -m32"
  export PKG_CONFIG="i686-pc-linux-gnu-pkg-config"

  cd libXfixes-${pkgver}
  ./configure --prefix=/usr --sysconfdir=/etc --disable-static --libdir=/usr/lib32
  make
}

package() {
  cd libXfixes-${pkgver}
  make DESTDIR="${pkgdir}" install
 
  rm -rf "${pkgdir}"/usr/{include,share,bin}
  mkdir -p "$pkgdir/usr/share/licenses"
  ln -s $_pkgbasename "$pkgdir/usr/share/licenses/$pkgname"
}
