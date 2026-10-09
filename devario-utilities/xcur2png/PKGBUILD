# Maintainer: Christian Hesse <mail@eworm.de>
# Contributor: Jarred Leonardo <jarredleonardo at googlemail dot com>

pkgname=xcur2png
pkgver=0.7.1
pkgrel=9
pkgdesc='Convert X cursors to PNG images'
arch=('x86_64')
url='https://github.com/eworm-de/xcur2png'
license=('GPL-3.0-or-later')
depends=('libpng' 'libxcursor')
source=("https://github.com/eworm-de/${pkgname}/releases/download/${pkgver}/${pkgname}-${pkgver}.tar.gz"
        '0001-fix-wrong-math.patch'
        '0002-fix-gcc-14-build.patch')
sha256sums=('bc6a062fdb48615a7159ed56ef3d2011168cd8a9decaf1d8a4e316d3064132c9'
            '224cf894c53eeb647a696ff311054cecf1a3dfeb10f49d96293c8bfeba4b88e9'
            '05a9dde0023cfd984279ccb08094ecbbdb4618e0abfeb3761eba4f2afa10ba5b')

prepare() {
  cd "${srcdir}/${pkgname}-${pkgver}"

  patch -Np1 < ../0001-fix-wrong-math.patch
  patch -Np1 < ../0002-fix-gcc-14-build.patch
}

build() {
  cd "${srcdir}/${pkgname}-${pkgver}"

  ./configure \
    --prefix=/usr
  make
}

package() {
  cd "${srcdir}/${pkgname}-${pkgver}"

  make DESTDIR="${pkgdir}" install
}

