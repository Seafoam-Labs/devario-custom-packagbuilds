# Maintainer: Torsten Keßler <tpkessler at archlinux dot org>
pkgname=rocm-toolchain
pkgver=0.6.0
pkgrel=1
pkgdesc="Scripts for ROCm packaging"
arch=('any')
url="https://gitlab.archlinux.org/tpkessler/rocm-toolchain"
license=('GPL-3.0-or-later')
depends=('bash')
makedepends=('git')
source=("$pkgname::git+$url#tag=v$pkgver")
sha256sums=('0993c57c32bbc2e57e93db389b7c722f8a1d0a401699b869ad10727558255dc2')

package() {
	cd $pkgname
	install -Dm755 rocm-supported-gfx "$pkgdir"/usr/bin/rocm-supported-gfx
}
