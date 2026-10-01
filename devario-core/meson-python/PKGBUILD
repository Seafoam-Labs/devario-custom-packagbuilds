# Maintainer:

pkgname=meson-python
pkgver=0.22.0
pkgrel=1
pkgdesc='Meson PEP 517 Python build backend'
arch=(any)
url='https://github.com/mesonbuild/meson-python'
groups=(python-build-backend)
license=(MIT)
depends=(meson
         patchelf
         python
         python-packaging
         python-pyproject-metadata)
makedepends=(git
             ninja
             python-build
             python-installer)
optdepends=('python-colorama: colored output')
checkdepends=(cmake
              cython
              python-gitpython
              python-pytest
              python-pytest-mock
              python-wheel)
source=(git+https://github.com/mesonbuild/meson-python#tag=$pkgver)
sha256sums=('a1615dfaba3099526c1e2de2f2374a75c4d39a93cfc8ae436ab60b31d2c494e7')

prepare() {
  cd $pkgname
  sed -e '/ninja/d' -i pyproject.toml
}

build() {
  cd $pkgname
  python -m build --wheel --no-isolation
}

check() {
  cd $pkgname
  python -m venv --system-site-packages test-env
  test-env/bin/python -m installer dist/*.whl
  test-env/bin/python -m pytest -W ignore::DeprecationWarning
}

package() {
  cd $pkgname
  python -m installer --destdir="$pkgdir" dist/*.whl
  install -Dm644 LICENSE -t "$pkgdir"/usr/share/licenses/$pkgname
}
