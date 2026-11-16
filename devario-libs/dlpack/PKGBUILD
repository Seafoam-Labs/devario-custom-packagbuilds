# Maintainer: Torsten Keßler <tpkessler at archlinux dot org>
pkgname=dlpack
pkgver=1.4
pkgrel=1
pkgdesc='Open in-memory tensor structure for sharing tensors among frameworks'
arch=('any')
url='https://dmlc.github.io/dlpack/latest/'
license=('Apache-2.0')
# header-only library
# depends=()
makedepends=('cmake')
_git='https://github.com/dmlc/dlpack'
source=("$pkgname-$pkgver.tar.gz::$_git/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('5886003d8558ebe94d94b2f72a191f9843164412ee1d06f2e410d042ea2bb88e')


build() {
	local cmake_args=(
		-Wno-dev
		-D CMAKE_POLICY_VERSION_MINIMUM=3.5
		-B build
		-S "$pkgname-$pkgver"
		-D CMAKE_BUILD_TYPE=None
		-D CMAKE_INSTALL_PREFIX=/usr
	)
	cmake "${cmake_args[@]}"
	cmake --build build
}

# check() {
# 	./build/mock
# }

package() {
	DESTDIR="$pkgdir" cmake --install build
}
