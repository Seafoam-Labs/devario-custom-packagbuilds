# Maintainer: David Runge <dvzrv@archlinux.org>

pkgname=python-zopfli
_name="${pkgname/thon/}"
pkgver=0.4.3
pkgrel=1
pkgdesc="Python bindings to zopfli"
arch=(x86_64)
url="https://github.com/fonttools/py-zopfli"
license=(Apache-2.0)
depends=(
  glibc
  python
)
makedepends=(
  python-build
  python-installer
  python-setuptools
  python-setuptools-scm
  python-wheel
  zopfli
)
checkdepends=(python-pytest)
source=($_name-$pkgver.tar.gz::$url/archive/refs/tags/v$pkgver.tar.gz)
sha512sums=('b61204b769df4bb67cbc9993fee7b0a135559a01154ff68e82294b2aa66bff433bb388f230b68ab762f59ea19fc6dfaa110acb04a10cab6c325c01f367060274')
b2sums=('dc1c8c476f1a0cf8655703b102d843707c3800b2f9490975d81697c91d39b1393658842cbaee11bc552f814f35632d97e8fa27f86175e0bee96fc06325aca763')

build() {
  cd $_name-$pkgver
  SETUPTOOLS_SCM_PRETEND_VERSION=$pkgver USE_SYSTEM_ZOPFLI=true python -m build --wheel --no-isolation
}

check() {
  local _site_packages=$(python -c "import site; print(site.getsitepackages()[0])")

  cd $_name-$pkgver
  python -m installer --destdir=test_dir dist/*.whl
  export PYTHONPATH="test_dir/$_site_packages:$PYTHONPATH"
  pytest -vv
}

package() {
  depends+=(
    zopfli libzopfli.so libzopflipng.so
  )

  cd $_name-$pkgver
  python -m installer --destdir="$pkgdir" dist/*.whl
  install -vDm 644 README.rst -t "$pkgdir/usr/share/doc/$pkgname/"
}
