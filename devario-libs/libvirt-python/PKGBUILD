# Maintainer: Robin Broda <robin@broda.me>
# Contributor: Christian Rebischke <chris.rebischke@archlinux.org>
# Contributor: Sergej Pupykin <pupykin.s+arch@gmail.com>
# Contributor: Jonathan Wiersma <archaur at jonw dot org>

pkgname='libvirt-python'
epoch=1
pkgver=12.8.0
pkgrel=1
pkgdesc="libvirt python binding"
arch=('x86_64')
url="https://pypi.python.org/pypi/libvirt-python"
license=('LGPL-2.1-or-later')
makedepends=(
  git
  libvirt
  python
  python-setuptools
  python-build
  python-installer
  python-wheel
)
depends=(
  python
  libvirt
)
options=('emptydirs')
source=(
  "git+https://gitlab.com/libvirt/libvirt-python.git#tag=v${pkgver}"
)
sha512sums=('bd29adffde6853bc4329d8c851f3abf4b0af5d87d87868d06f5e1f4571302bf4d7b47b03fe27395744e0817ebaa0751f5a75e32017ca0eb86bd1e56c66a7e0b1')

build() {
  cd ${pkgbase}
  python -m build --wheel --no-isolation
}

package() {
  cd ${pkgbase}
  python -m installer --destdir="$pkgdir" dist/*.whl
}
