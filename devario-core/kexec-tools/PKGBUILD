# Maintainer: Tobias Powalowski <tpowa@archlinux.org>
# Contributor: Camille Moncelier <pix@devlife.org>, simo <simo@archlinux.org>

pkgname=kexec-tools
pkgver=2.0.32
pkgrel=1
pkgdesc="Load another kernel from the currently executing Linux kernel"
arch=('x86_64')
url="https://kernel.org/pub/linux/utils/kernel/kexec/"
source=("git+https://git.kernel.org/pub/scm/utils/kernel/kexec/kexec-tools.git?signed#tag=v${pkgver}")
makedepends=('git')
validpgpkeys=('E27CD9A1F5ACC2FF4BFE7285D7CF64696A374FBE') # Simon Horman <horms@debian.org>
depends=(
  xz
  zlib
  zstd
)
license=('GPL-2.0-or-later')
b2sums=('d0633ece7e8309aa88992675cda1f6ebba9027e49831e78e27b61cc6ee668a63bc158f56311b728ca09b76366b8d3c554c3a991092bed379e440f0b86c7b4d00')

prepare() {
  cd "${pkgname}"
  ./bootstrap
}

build() {
  cd "${pkgname}"
  ./configure --prefix=/usr --sbindir=/usr/bin --without-lzma
  make
}

package() {
  cd "${pkgname}"
  make DESTDIR="${pkgdir}" install
  install -D -m644 kexec/kexec.8 "$pkgdir"/usr/share/man/man8/kexec.8
}

