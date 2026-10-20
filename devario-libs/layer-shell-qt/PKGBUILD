# Maintainer: Antonio Rojas <arojas@archlinux.org>

pkgname=layer-shell-qt
pkgver=6.8.0
_dirver=$(echo $pkgver | cut -d. -f1-3)
pkgrel=1
pkgdesc='Qt component to allow applications to make use of the Wayland wl-layer-shell protocol'
arch=(x86_64)
url='https://kde.org/plasma-desktop/'
license=(GPL-2.0-or-later LGPL-2.0-or-later)
depends=(glibc
         qt6-base
         libstdc++
         wayland)
makedepends=(extra-cmake-modules
             qt6-declarative
             wayland-protocols)
optdepends=('qt6-declarative: QML bindings')
groups=(plasma)
source=(https://download.kde.org/stable/plasma/$_dirver/$pkgname-$pkgver.tar.xz{,.sig})
sha256sums=('91ced561862f0d84836ad4ae5c34914bb532576c88607baf4ec2c957b895b41d'
            'SKIP')
validpgpkeys=('E0A3EB202F8E57528E13E72FD7574483BB57B18D'  # Jonathan Esk-Riddell <jr@jriddell.org>
              '0AAC775BB6437A8D9AF7A3ACFE0784117FBCE11D'  # Bhushan Shah <bshah@kde.org>
              'D07BD8662C56CB291B316EB2F5675605C74E02CF'  # David Edmundson <davidedmundson@kde.org>
              '1FA881591C26B276D7A5518EEAAF29B42A678C20') # Marco Martin <notmart@gmail.com>

build() {
  cmake -B build  -S $pkgname-$pkgver
  cmake --build build
}

package() {
  DESTDIR="$pkgdir" cmake --install build
}
