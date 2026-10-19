# Maintainer:  Sergej Pupykin <arch+pub@sergej.pp.ru>
# Maintainer:  Eli Schwartz <eschwartz@archlinux.org>
# Contributor: Jens Staal <staal1978@gmail.com>

pkgname=kernel-headers-musl
pkgver=6.12.77
pkgrel=1
pkgdesc="Linux kernel headers sanitized for use with musl libc"
arch=('x86_64')
url="https://github.com/sabotage-linux/kernel-headers"
license=('LGPL')
depends=('musl')
source=("$pkgname-$pkgver.tar.gz::https://github.com/sabotage-linux/kernel-headers/archive/v${pkgver/_/-}.tar.gz")
sha512sums=('10a5281c6535705171a2d8a7619f13d19a2dbdd15af28ee470bb436fbf9b954502bf9770da8f63e6b2b9f873b50c9ef2d7d77142d40598b8c6cf23f7bc4b1b69')

_CARCH=$CARCH
[[ $CARCH = i?86 ]] && _CARCH=x86

build() {
  cd "$srcdir"/kernel-headers-${pkgver/_/-}
  make ARCH=${_CARCH} prefix=/usr/lib/musl
}

package() {
  cd "$srcdir"/kernel-headers-${pkgver/_/-}
  make ARCH=${_CARCH} prefix=/usr/lib/musl DESTDIR="$pkgdir" install
}
