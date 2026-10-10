# Maintainer: Antonio Rojas <arojas@archlinux.org>

pkgname=python-pyqt5-sip
pkgver=12.20.0
pkgrel=1
arch=(x86_64)
pkgdesc='The sip module support for PyQt5'
url='https://riverbankcomputing.com/software/pyqt/intro'
license=(GPL)
depends=(glibc
         python)
makedepends=(python-build
             python-installer
             python-setuptools
             python-wheel)
source=(https://pypi.python.org/packages/source/P/PyQt5-sip/pyqt5_sip-$pkgver.tar.gz)
sha256sums=('93e0622791f8d22cd4a32a29edfdd2ef6d6680f4c47f59b03ebf1c5da3c3e896')

build() {
  cd pyqt5_sip-$pkgver
  python -m build --wheel --no-isolation
}

package()  {
  cd pyqt5_sip-$pkgver
  python -m installer --destdir="$pkgdir" dist/*.whl
}
