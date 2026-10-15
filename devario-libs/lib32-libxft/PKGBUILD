# Maintainer: Ionut Biru <ibiru@archlinux.org>

_pkgbasename=libxft
pkgname=lib32-$_pkgbasename
pkgver=2.3.9
pkgrel=1
pkgdesc="FreeType-based font drawing library for X (32-bit)"
arch=('x86_64')
license=('HPND-sell-variant')
url="https://xorg.freedesktop.org/"
depends=('lib32-fontconfig' 'lib32-libxrender')
makedepends=('gcc-multilib')
source=(${url}/releases/individual/lib/libXft-${pkgver}.tar.xz{,.sig})
sha512sums=('493e4475c0eeab04a510819446eaa871ba9e1695e42d05bb7791d2ed59f7faff31e910dae95efa4b0ac4a7a2da38614b5740a4ca9388134bea80d348e9ad57e5'
            'SKIP')
validpgpkeys=('19882D92DDA4C400C22C0D56CC2AF4472167BE03') # Thomas E. Dickey (use for email) <dickey@his.com>
validpgpkeys+=('3BB639E56F861FA2E86505690FDD682D974CA72A') # Matt Turner <mattst88@gmail.com>

build() {
  export CC="gcc -m32"
  export CXX="g++ -m32"
  export PKG_CONFIG_PATH="/usr/lib32/pkgconfig"

  cd libXft-${pkgver}
  ./configure --prefix=/usr \
    --libdir=/usr/lib32 --disable-static
  make
}

package() {
  cd libXft-${pkgver}
  make DESTDIR="${pkgdir}" install

  rm -rf "${pkgdir}"/usr/{bin,include,share}
  mkdir -p "$pkgdir/usr/share/licenses"
  ln -s $_pkgbasename "$pkgdir/usr/share/licenses/$pkgname"
}
