# Maintainer: David Runge <dvzrv@archlinux.org>
# Maintainer: Caleb Maclennan <caleb@alerque.com>

pkgname=python-cbor2
_name=${pkgname#python-}
pkgver=6.1.5
pkgrel=1
pkgdesc="Pure Python CBOR (de)serializer with extensive tag support"
arch=(x86_64)
url="https://github.com/agronholm/cbor2"
license=(MIT)
depends=(
  glibc
  libgcc
  python
)
makedepends=(
  python-build
  python-installer
  python-setuptools
  python-setuptools-rust
  python-setuptools-scm
  python-toml
  python-wheel
)
checkdepends=(
  python-hypothesis
  python-pytest
)
source=($url/archive/refs/tags/$pkgver/$_name-$pkgver.tar.gz)
sha512sums=('37b103521be8729765c42fc8b3c58d6d6102e2323f3364e40ce7852f7ad0b6ad3c5c87ffe75e80aa751d16c55b50c8d824b699adbe8021d85afcf21df1f1c8e3')
b2sums=('2b2582918f86d8ce821c977b95a06a1fd9379a1cb03deaf20c8525676395d7279d77905737ce49863ee89c94110c9a0305df4f03900efd10fc450ea8474bb232')

build() {
  cd $_name-$pkgver
  SETUPTOOLS_SCM_PRETEND_VERSION=$pkgver python -m build -wn
}

check() {
  local python_version=$(python -c 'import sys; print("".join(map(str, sys.version_info[:2])))')

  cd $_name-$pkgver
  PYTHONPATH="$PWD/build/lib.linux-$CARCH-cpython-$python_version:${PYTHONPATH}" pytest -vvv -c /dev/null tests
}

package() {
  cd $_name-$pkgver
  python -m installer -d "$pkgdir" dist/*.whl
  install -vDm 644 README.rst -t "$pkgdir/usr/share/doc/$pkgname/"
  install -vDm 644 LICENSE.txt -t "$pkgdir/usr/share/licenses/$pkgname/"
}
