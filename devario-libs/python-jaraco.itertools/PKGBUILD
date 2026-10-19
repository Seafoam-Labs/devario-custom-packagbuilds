# Maintainer: David Runge <dvzrv@archlinux.org>

_name=jaraco.itertools
pkgname=python-jaraco.itertools
pkgver=6.4.2
pkgrel=2
pkgdesc="Itertools for Python"
arch=(any)
url="https://github.com/jaraco/jaraco.itertools"
license=(MIT)
depends=(
  python
  python-inflect
  python-more-itertools
)
makedepends=(
  python-build
  python-installer
  python-setuptools
  python-setuptools-scm
  python-toml
  python-wheel
)
checkdepends=(
  python-pytest
  python-pytest-enabler
)
conflicts=(python-jaraco)
replaces=(python-jaraco)
source=($_name-$pkgver.tar.gz::$url/archive/refs/tags/v$pkgver.tar.gz)
sha256sums=('c7c4616cfaeeb02b62cb27477df75f8327dc532003394d12b89df26b53fc6f00')
b2sums=('7ea8d920e31cf46d24ee68989a30adfdfcdfcfd4cbb15853de1d2960a505cf54b8d41689e8ea36bcc850b5c718522afbffc763daceb4b0a16110049fa6a31063')

build() {
  cd $_name-$pkgver
  export SETUPTOOLS_SCM_PRETEND_VERSION=$pkgver
  python -m build --wheel --no-isolation
}

check() {
  cd $_name-$pkgver
  pytest -vv
}

package() {
  cd $_name-$pkgver
  python -m installer --destdir="$pkgdir" dist/*.whl
  install -vDm 644 LICENSE -t "$pkgdir/usr/share/licenses/$pkgname/"
}
