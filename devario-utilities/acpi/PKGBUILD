# Maintainer: Alexander F Rødseth <xyproto@archlinux.org>
# Contributor: Judd Vinet <jvinet@zeroflux.org>

pkgname=acpi
pkgver=1.8
pkgrel=2
pkgdesc='Client for battery, power, and thermal readings'
arch=('x86_64')
url='https://sourceforge.net/projects/acpiclient/files/acpiclient/'
license=('GPL-2.0-or-later')
depends=('glibc')
source=("https://downloads.sourceforge.net/acpiclient/$pkgname-$pkgver.tar.gz")
sha256sums=('e64c6e00b53cd797427ea32a160513425b03ed4f077733f71f1f09ff340f230b')

build() {
  cd "$pkgname-$pkgver"

  ./configure --prefix=/usr
  make
}

package() {
  make -C "$pkgname-$pkgver" DESTDIR"=$pkgdir" install
}

# vim:ts=2 sw=2 et:
