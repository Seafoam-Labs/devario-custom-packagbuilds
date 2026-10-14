# Maintainer: Lukas Fleischer <lfleischer@archlinux.org>
# Contributor: Fabio 'Lolix' Loli <fabio.loli@disroot.org> -> https://github.com/FabioLolix

pkgname=unordered_dense
pkgver=5.3.2
pkgrel=1
pkgdesc="A fast and densely stored hashmap and hashset"
arch=(any)
url="https://github.com/martinus/unordered_dense"
license=(MIT)
makedepends=(cmake git)
source=("git+https://github.com/martinus/unordered_dense.git#tag=v${pkgver}")
sha256sums=('ab107b6a90cb699afac0abfe2cf275ba345534f9b8c83fd9bca40589ff6b82ba')

build() {
	cmake \
		-B build \
		-S unordered_dense \
		-W no-author \
		-D CMAKE_BUILD_TYPE=None \
		-D CMAKE_INSTALL_PREFIX=/usr
	cmake --build build
}

package() {
	DESTDIR="${pkgdir}" cmake --install build
	install -Dm644 unordered_dense/LICENSE -t "${pkgdir}/usr/share/licenses/${pkgname}/"
}
