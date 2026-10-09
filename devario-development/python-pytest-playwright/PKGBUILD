# Maintainer: Antonio Rojas <arojas@archlinux.org>

_name=playwright-pytest
pkgname=python-pytest-playwright
pkgver=0.9.0
pkgrel=1
pkgdesc='Pytest plugin to write end-to-end browser tests with Playwright'
arch=(any)
url='https://github.com/microsoft/playwright-pytest'
license=(Apache-2.0)
depends=(python
         python-pytest
         python-slugify)
makedepends=(git
             python-build
             python-installer
             python-setuptools-scm
             python-wheel)
source=(git+https://github.com/microsoft/$_name#tag=v$pkgver)
sha256sums=('cfc94203ac69920dbb0cb2db1b788a048f82e5ca648c0be0f2a54e4c6457a69d')

build() {
  cd $_name/pytest-playwright
  python -m build --wheel --no-isolation --skip-dependency-check
}

check() {
  cd $_name/pytest-playwright
#  pytest -v
}

package() {
  cd $_name/pytest-playwright
  python -m installer --destdir="$pkgdir" dist/*.whl
}
