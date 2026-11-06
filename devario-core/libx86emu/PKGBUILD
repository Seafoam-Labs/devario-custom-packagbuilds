# Maintainer: Alexander F. Rødseth <xyproto@archlinux.org>
# Contributor: Kaiting Chen <kaitocracy@gmail.com>
# Contributor: Gergely Imreh <imrehgATgmailDOTcom>

pkgname=libx86emu
pkgver=3.7
pkgrel=2
pkgdesc='x86 emulation library'
arch=(x86_64)
url='https://github.com/wfeldt/libx86emu'
license=(MIT)
depends=(glibc)
makedepends=(git setconf)
source=("git+$url#tag=$pkgver")
b2sums=('21931051ab2d1270f77248067cd3e645d3cd2c385320310f5a0f9ad367d1eb54e7130958a3431f45ead6d2257524e6d1f49fd11223fa9ebac1d8c6a41b35e94a')

prepare() {
  sed -i 's/-shared -Wl/-shared '"$LDFLAGS"'/g' $pkgname/Makefile
  setconf $pkgname/Makefile CFLAGS="$CFLAGS -shared -fPIC -fvisibility=hidden -fomit-frame-pointer -w"
}

build() {
  make -C $pkgname LIBDIR=/usr/lib
}

package() {
  make -C $pkgname LIBDIR=/usr/lib DESTDIR="$pkgdir" install
  install -Dm644 $pkgname/LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}
