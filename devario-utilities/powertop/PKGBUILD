# Maintainer: Jaroslav Lichtblau <svetlemodry@archlinux.org>
# Maintainer: Hyacinthe Cartiaux <hyacinthe@archlinux.org>
# Contributor: Alexander Fehr <pizzapunk gmail com>
# Contributor: Xilon <xilonmu@gmail.com>

pkgname=powertop
pkgver=2.16
pkgrel=1
pkgdesc='A tool to diagnose issues with power consumption and power management'
arch=('x86_64')
url='https://github.com/fenrus75/powertop/'
license=('GPL-2.0-only')
depends=(
  'libgcc'
  'libstdc++'
  'libnl'
  'ncurses'
  'libtracefs'
  'libtraceevent'
  'pciutils'
)
makedepends=(
  'meson'
  'ninja'
)
optdepends=(
  'xorg-xset: for the --calibrate function'
)
changelog="${pkgname}.changelog"
source=("${pkgname}-${pkgver}.tar.gz::https://github.com/fenrus75/powertop/archive/v${pkgver}.tar.gz")
sha256sums=('cf37e565b958a64f1e3086daeab82d7959566a372d01d40d3904cbca95cdf3d2')

check() {
  cd "${srcdir}/${pkgname}-${pkgver}"

  meson setup -Denable-tests=true build_test
  ninja -C build_test test
}

build() {
  cd "${srcdir}/${pkgname}-${pkgver}"

  meson setup build --prefix=/usr
  ninja -C build
}

package() {
  cd "${srcdir}/${pkgname}-${pkgver}"

  DESTDIR="${pkgdir}" ninja -C build install
}
