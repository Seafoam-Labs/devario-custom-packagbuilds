# Maintainer: Carl Smedstad <carsme@archlinux.org>

pkgname=python-propcache
pkgver=0.5.4
pkgrel=1
pkgdesc='Fast property caching'
arch=(x86_64)
url='https://github.com/aio-libs/propcache'
license=(Apache-2.0)
depends=(
  glibc
  python
)
makedepends=(
  cython
  python-build
  python-expandvars
  python-installer
  python-setuptools
  python-wheel
)
checkdepends=(python-pytest)
source=("$url/archive/v$pkgver/${pkgname#python-}-$pkgver.tar.gz")
sha512sums=('2256bbbc926d72a27839393f0d2c8a0513f705057a85f7496fcb7dc4850e9daa2891dfee4512548174f84efad00f23fe2fbc0d4d82b1e00348ea43d7341cccee')

prepare() {
  cd ${pkgname#python-}-$pkgver
  # Drop Cython versioned requirement
  sed -i 's/ ~= 3.1.0//' packaging/pep517_backend/_backend.py
}

build() {
  cd ${pkgname#python-}-$pkgver
  python -m build --wheel --no-isolation
}

check() {
  cd ${pkgname#python-}-$pkgver
  python -m venv --system-site-packages test-env
  test-env/bin/python -m installer dist/*.whl
  test-env/bin/python -m pytest --override-ini="addopts="
}

package() {
  cd ${pkgname#python-}-$pkgver
  python -m installer --destdir="$pkgdir" dist/*.whl
}
