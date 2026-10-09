# Maintainer: Caleb Maclennan <caleb@alerque.com>
# Contributor: Luis Aleman Vazquez <luisv@tuta.io>

pkgname=cliphist
pkgver=0.7.0
pkgrel=2
epoch=1
pkgdesc='wayland clipboard manager'
arch=(i686 x86_64)
url="https://github.com/sentriz/$pkgname"
license=(GPL3)
depends=(glibc
         wl-clipboard)
makedepends=(go)
optdepends=('xdg-utils: image and mime inferance')
_archive="$pkgname-$pkgver"
source=("$url/archive/v$pkgver/$_archive.tar.gz")
sha256sums=('8d7dc7b4495e5812b5613274c250ba5d3900933d78888ce7921c01247f191cc8')

build() {
	cd "$_archive"
	export CGO_CPPFLAGS="$CPPFLAGS"
	export CGO_CFLAGS="$CFLAGS"
	export CGO_CXXFLAGS="$CXXFLAGS"
	export GOFLAGS="-buildmode=pie -trimpath -mod=readonly -modcacherw"
	go build \
		-ldflags "-linkmode external -extldflags '$LDFLAGS'" \
		-o $pkgname
}

package() {
	cd "$_archive"
	install -Dm0755 -t "$pkgdir/usr/bin/" $pkgname
	install -Dm644 "contrib/$pkgname.service" "$pkgdir/usr/lib/systemd/user/$pkgname.service"
}
