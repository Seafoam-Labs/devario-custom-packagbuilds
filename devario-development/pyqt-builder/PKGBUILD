# Maintainer: Antonio Rojas <arojas@archlinux.org>

pkgname=pyqt-builder
pkgver=1.20.0
pkgrel=1
pkgdesc='The PEP 517 compliant PyQt build system'
arch=(any)
url='https://pypi.org/project/PyQt-builder/'
license=(BSD-2-Clause)
depends=(python
         python-packaging
         sip)
makedepends=(git
             python-build
             python-installer
             python-setuptools-scm
             python-wheel)
source=(git+https://github.com/Python-PyQt/PyQt-builder#tag=$pkgver)
sha256sums=('35ff003a0012d49205c4c7f141755f67190e58e15122b115afb78401885607ab')

build() {
  cd PyQt-builder
  SETUPTOOLS_SCM_PRETEND_VERSION=$pkgver \
  python -m build --wheel --no-isolation
}

package() {
  cd PyQt-builder
  python -m installer --destdir="$pkgdir" dist/*.whl
  install -Dm644 LICENSE -t "$pkgdir"/usr/share/licenses/$pkgname
}
