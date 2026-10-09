# Maintainer: Felix Yan <felixonmars@archlinux.org>
# Contributor: Anatol Pomozov <anatol.pomozov@gmail.com>

_target_arch=riscv
_target=riscv64-linux-gnu
pkgname=$_target-linux-api-headers
pkgver=7.2
pkgrel=1
pkgdesc="Kernel headers sanitized for use in userspace ($_target)"
arch=(any)
url='https://www.kernel.org'
license=(GPL-2.0-only)
makedepends=('rsync')
source=(https://www.kernel.org/pub/linux/kernel/v${pkgver:0:1}.x/linux-$pkgver.tar.{xz,sign})
sha256sums=('f9fef3d14c0df53819026f4be74459835c2a0b0dcbf5b5bbd9ea19f0829402b3'
            'SKIP')
b2sums=('cf5f3d87b96f223034c47c6e5fc972fe52c2556310eb2f064632537b8727231135a8540179fd5d51343738c8a51f51f09c7e8da374324b68551c84a4124bb71b'
        'SKIP')
validpgpkeys=(
  'ABAF11C65A2970B130ABE3C479BE3E4300411886'  # Linus Torvalds
  '647F28654894E3BD457199BE38DBBDC86092693E'  # Greg Kroah-Hartman
)

build() {
  cd linux-$pkgver
  make ARCH=$_target_arch mrproper
}

package() {
  cd linux-$pkgver
  make INSTALL_HDR_PATH="$pkgdir/usr/$_target/" ARCH=$_target_arch V=0 headers_install
}
