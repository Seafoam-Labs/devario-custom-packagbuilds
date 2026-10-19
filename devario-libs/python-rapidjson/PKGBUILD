# Maintainer: Felix Yan <felixonmars@archlinux.org>

pkgname=python-rapidjson
pkgver=1.25
pkgrel=1
pkgdesc="Python wrapper around rapidjson"
arch=('x86_64')
url="https://pypi.python.org/pypi/python-rapidjson"
license=('MIT')
depends=('python')
makedepends=('python-setuptools' 'python-build' 'python-installer' 'python-wheel')
checkdepends=('python-pytest' 'python-pytz')
# The sdist includes the upstream-pinned RapidJSON headers.
source=("https://pypi.io/packages/source/p/python-rapidjson/python_rapidjson-$pkgver.tar.gz")
sha512sums=('54696fcff78e4f70e4abca75b1156971628ecc5dca134cd621cd6a537ed595182824d3fe3286378f138b0b10a2ce000e6f3edcfd960a69a1f95b5cdbc0461219')

build() {
  cd python_rapidjson-$pkgver
  python -m build --wheel --no-isolation
}

check() {
  cd python_rapidjson-$pkgver
  local python_version=$(python -c 'import sys; print("".join(map(str, sys.version_info[:2])))')
  # Benchmarks compare optional JSON implementations and are not correctness tests.
  PYTHONPATH="$PWD/build/lib.linux-$CARCH-cpython-$python_version" pytest --ignore benchmarks/
}

package() {
  cd python_rapidjson-$pkgver
  python -m installer --destdir="$pkgdir" dist/*.whl
  install -Dm644 LICENSE -t "$pkgdir"/usr/share/licenses/$pkgname/
}
