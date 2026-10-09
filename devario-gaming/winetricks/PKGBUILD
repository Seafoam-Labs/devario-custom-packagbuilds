# Maintainer: Lukas Fleischer <lfleischer@archlinux.org>
# Maintainer: Felix Yan <felixonmars@archlinux.org>
# Contributor: Laurent Carlier <lordheavym@gmail.com>
# Contributor: DsTr <dstr@gmail.com>
# Contributor: Allan McRae <allan@archlinux.org>

pkgname=winetricks
pkgver=20260125
pkgrel=2
pkgdesc='Script to install various redistributable runtime libraries in Wine.'
url='https://wiki.winehq.org/winetricks'
license=('LGPL-2.1-or-later')
arch=('any')
depends=('bash' 'cabextract' 'perl' 'unzip')
optdepends=('zenity: GUI for GNOME desktop'
            'kdialog: GUI for KDE desktop')
source=("$pkgname-$pkgver.tar.gz::https://github.com/Winetricks/winetricks/archive/$pkgver.tar.gz")
sha512sums=('ab29191c8032ba70ee8e807c7910916d47cbbdab658cdb5a1c1daa11f0eb7e219a8cd5555e4e681a154913237e4600a8c5056e8bdd9c1f44dac92f27ec875fcb')

package() {
  depends+=('wine')

  cd winetricks-$pkgver
  make DESTDIR="$pkgdir" install
}
