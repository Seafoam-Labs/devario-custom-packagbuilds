# Maintainer: George Hu <integral@archlinux.org>
# Maintainer: DeepChirp <deepchirp@archlinux.org>
# Contributor: dalto <dalto at fastmail.com>

pkgname=btrfs-assistant
pkgver=2.3.1
pkgrel=1
pkgdesc="An application for managing BTRFS subvolumes and Snapper snapshots"
arch=('x86_64')
url="https://gitlab.com/${pkgname}/${pkgname}"
license=('GPL-3.0-or-later')
depends=(
	'bash'
	'btrfs-progs'
	'diffutils'
	'glibc'
	'hicolor-icon-theme'
	'libgcc'
	'libstdc++'
	'polkit'
	'qt6-base'
	'util-linux'
)
optdepends=('snapper: Snapper support'
            'btrfsmaintenance: Btrfs maintenance support')
makedepends=('cmake' 'qt6-declarative' 'qt6-tools')
backup=("etc/${pkgname}.conf")
source=("${url}/-/archive/${pkgver}/${pkgname}-${pkgver}.tar.gz")
sha256sums=('1dcf140132b88e82d2d3c189464978af0a0c28dd5b8a82f23f4311b5b0211e15')

build() {
	cmake -B build -S "${pkgname}-${pkgver}" -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=None
	cmake --build build
}

package() {
	DESTDIR="${pkgdir}" cmake --install build
}
