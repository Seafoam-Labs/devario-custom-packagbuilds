# Maintainer: Caleb Maclennan <caleb@alerque.com>

pkgname=bzip3
pkgver=1.5.4
pkgrel=1
pkgdesc='A better and stronger spiritual successor to BZip2'
arch=(x86_64)
license=(LGPL3 Apache)
url="https://github.com/kspalaiologos/$pkgname"
depends=(glibc
         sh)
makedepends=(clang)
provides=("lib$pkgname.so")
_archive="$pkgname-$pkgver"
source=("$url/releases/download/$pkgver/$_archive.tar.xz")
sha256sums=('fac65d7f39ae73c1c9221a97075eebeb27696299b02ad1e01ec039ab0eca9fca')

build() {
	cd "$_archive"
	./configure --prefix /usr CC=clang
	make all
}

check() {
	cd "$_archive"
	make check
}

package() {
	cd "$_archive"
	make DESTDIR="$pkgdir" install
	install -Dm0644 -t "$pkgdir/usr/share/licenses/$pkgname/" *LICENSE
}
