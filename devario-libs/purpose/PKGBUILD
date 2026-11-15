# Maintainer:Antonio Rojas <arojas@archlinux.org>

pkgname=purpose
pkgver=6.31.0
pkgrel=1
pkgdesc='Framework for providing abstractions to get the developers purposes fulfilled'
arch=(x86_64)
url='https://develop.kde.org/products/frameworks/'
license=(LGPL-2.0-only LGPL-3.0-only)
depends=(glibc
         hicolor-icon-theme
         kaccounts-integration
         kcmutils
         kconfig
         kcoreaddons
         ki18n
         kio
         kirigami
         kitemmodels
         knotifications
         kservice
         libaccounts-qt
         libstdc++
         qt6-base
         qt6-declarative)
makedepends=(extra-cmake-modules
             intltool
             prison
             qt6-tools)
optdepends=('bluedevil: sharing via Bluetooth'
            'kdeclarative: Nextcloud and YouTube plugins'
            'kdeconnect: sharing to smartphone via KDE Connect'
            'prison: QR code plugin'
            'telegram-desktop: sharing via Telegram')
conflicts=('purpose5<5.114.0-2')
groups=(kf6)
source=(https://download.kde.org/stable/frameworks/${pkgver%.*}/$pkgname-$pkgver.tar.xz{,.sig})
sha256sums=('665b579a6b4c4d6f9f19a83fe802da70a65d38d9b23193471b5b64e65b7a55c3'
            'SKIP')
validpgpkeys=(53E6B47B45CEA3E0D5B7457758D0EE648A48B3BB # David Faure <faure@kde.org>
              90A968ACA84537CC27B99EAF2C8DF587A6D4AAC1 # Nicolas Fella <nicolas.fella@kde.org>
              )

build() {
  cmake -B build -S $pkgname-$pkgver \
    -DCMAKE_INSTALL_LIBEXECDIR=lib \
    -DBUILD_TESTING=OFF
  cmake --build build
}

package() {
  DESTDIR="$pkgdir" cmake --install build
}
