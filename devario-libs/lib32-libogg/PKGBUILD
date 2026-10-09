# Maintainer: Jan Alexander Steffens (heftig) <heftig@archlinux.org>
# Contributor: Maxime Gauduin <alucryd@archlinux.org>

pkgname=lib32-libogg
pkgver=1.3.6
pkgrel=1
pkgdesc='Ogg bitstream and framing library (32-bit)'
arch=(x86_64)
url=https://www.xiph.org/ogg/
license=(BSD)
depends=(lib32-glibc libogg)
makedepends=(
  cmake
  git
  ninja
)
provides=(libogg.so)
source=(git+https://github.com/xiph/ogg.git?signed#tag=v${pkgver})
sha256sums=('2e83a0b16d3863e87f3d9372686b00fa0bf62a2641b458b929185103645fdf35')
validpgpkeys=(B7B00AEE1F960EEA0FED66FB9259A8F2D2D44C84) # Ralph Giles <giles@thaumas.net>

prepare() {
  cd ogg
}

build() {
  export CC="gcc -m32"
  export CXX="g++ -m32"
  export PKG_CONFIG=i686-pc-linux-gnu-pkg-config

  cmake -S ogg -B build -G Ninja \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DCMAKE_INSTALL_LIBDIR=/usr/lib32 \
    -DINSTALL_DOCS=OFF \
    -DBUILD_SHARED_LIBS=ON
  cmake --build build
}

package() {
  DESTDIR="${pkgdir}" cmake --install build
  rm -r "$pkgdir"/usr/include
  install -Dm 644 ogg/COPYING -t "${pkgdir}"/usr/share/licenses/${pkgname}/
}

# vim: ts=2 sw=2 et:
