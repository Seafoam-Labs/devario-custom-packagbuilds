# Maintainer: Lukas Fleischer <lfleischer@archlinux.org>
# Contributor: Eric Belanger <eric@archlinux.org>
# Contributor: tardo <tardo@nagi-fanboi.net>
# Contributor: Thayer Williams <thayer@archlinux.org>

pkgname=libx86
pkgver=1.1.1
pkgrel=1
pkgdesc='A library for real-mode x86 calls with an emulated x86 processor'
arch=(x86_64)
url='https://gitlab.archlinux.org/grawlinson/libx86'
license=(MIT)
depends=(glibc)
makedepends=(git)
source=("$pkgname::git+$url#tag=v$pkgver")
sha512sums=('115d0a458dbc78dc7ada8a88f7766f63aa83663efee77c00869be1d6fc788d3a4f132ce7319b4a0e8e895650d1a3c0b3f3fa4d4a967acada4dcc6247d4933590')
b2sums=('56b3d66fb96d14e9a1c08b7e4543a44a9b3179d410ed46921ec36ddaf5e284173686789b994ec36554308528ff67b5d048bd3735cca77167cebdfb1316cd05ee')

build() {
  cd "$pkgname"

  # compensate for x86_64
  if [ "$CARCH" = "x86_64" ]; then
    make BACKEND=x86emu LIBRARY=shared
  else
    make LIBRARY=shared
  fi
}

package() {
  cd "$pkgname"

  make DESTDIR="${pkgdir}" install

  # license
  install -vDm644 -t "$pkgdir/usr/share/licenses/$pkgname" COPYRIGHT
}
