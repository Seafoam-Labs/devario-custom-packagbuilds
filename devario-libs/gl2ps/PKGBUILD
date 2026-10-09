# Maintainer: Felix Yan <felixonmars@archlinux.org>
# Contributor: hauptmech, figo.zhang, chubtuff, lubosz
#
# Matlab bindings are not built by default to reduce dependencies.

pkgname=gl2ps
pkgver=1.4.3
pkgrel=1
pkgdesc="an OpenGL to PostScript printing library"
arch=('x86_64')
url='https://geuz.org/gl2ps/'
license=('LGPL-2.0-or-later')
depends=('libpng' 'libgl')
makedepends=('git' 'cmake' 'texlive-latex' 'texlive-latexrecommended')
source=("git+https://gitlab.onelab.info/gl2ps/gl2ps.git#tag=gl2ps_${pkgver//./_}")
sha512sums=('686efbe1ac252adda811bcd06c7629e3737e18c2f8e910d9c212127f092912988c47fb0f51e5c6215fe1bce80ecac6c78e46b4b33d5b84755daba684170ffa8c')

prepare() {
  mkdir build
}

build() {
  cd build
  export FORCE_SOURCE_DATE=1 # make pdftex adhere to SOURCE_DATE_EPOCH
  cmake ../gl2ps \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/usr
  make
}

package() {
  cd build
  make DESTDIR="$pkgdir/" install
}
