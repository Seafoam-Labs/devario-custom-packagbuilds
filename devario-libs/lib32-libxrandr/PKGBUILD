# Maintainer: Alexander Baldeck <alexander@archlinux.org>
# Contributor: Jan de Groot <jgc@archlinux.org>
_pkgbasename=libxrandr
pkgname=lib32-$_pkgbasename
pkgver=1.5.5
pkgrel=1
pkgdesc="X11 RandR extension library (32-bit)"
arch=('x86_64')
license=('HPND-sell-variant')
url="https://xorg.freedesktop.org/"
depends=('lib32-libxext' 'lib32-libxrender' $_pkgbasename 'lib32-libx11' 'lib32-glibc')
makedepends=('xorg-util-macros')
source=(${url}/releases/individual/lib/libXrandr-${pkgver}.tar.xz{,.sig})
sha256sums=('72b922c2e765434e9e9f0960148070bd4504b288263e2868a4ccce1b7cf2767a'
            'SKIP')
validpgpkeys=('10A6D91DA1B05BD29F6DEBAC0C74F35979C486BE'  # Dave Airlie <airlied@redhat.com>
              'C41C985FDCF1E5364576638B687393EE37D128F8'  # Matthieu Herrb <matthieu.herrb@laas.fr>
              '3AB285232C46AE43D8E192F4DAB0F78EA6E7E2D2') # Alan Coopersmith <alan.coopersmith@oracle.com>

build() {
  export CC="gcc -m32"
  export CXX="g++ -m32"
  export PKG_CONFIG="i686-pc-linux-gnu-pkg-config"

  cd "${srcdir}/libXrandr-${pkgver}"
  ./configure --prefix=/usr --sysconfdir=/etc --libdir=/usr/lib32
  make
}

package() {
  cd "${srcdir}/libXrandr-${pkgver}"

  make DESTDIR="${pkgdir}" install

  rm -rf "${pkgdir}"/usr/{include,share,bin}
  mkdir -p "$pkgdir/usr/share/licenses"
  ln -s $_pkgbasename "$pkgdir/usr/share/licenses/$pkgname"
}
