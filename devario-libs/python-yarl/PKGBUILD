# Maintainer: Levente Polyak <anthraxx[at]archlinux[dot]org>
# Maintainer: Carl Smedstad <carsme@archlinux.org>

pkgname=python-yarl
pkgver=1.25.1
pkgrel=1
pkgdesc='Yet another URL library'
arch=('x86_64')
url='https://github.com/aio-libs/yarl/'
license=('Apache-2.0')
depends=(
  'glibc'
  'python'
  'python-idna'
  'python-multidict'
  'python-propcache'
)
makedepends=(
  'cython'
  'python-setuptools'
  'python-build'
  'python-installer'
  'python-wheel'
  'python-expandvars'
)
checkdepends=(
  'python-hypothesis'
  'python-pytest'
)
source=("$url/archive/v$pkgver/$pkgname-$pkgver.tar.gz")
sha512sums=('0fac24fd47acab64951bfe5e3854d90338b8bb5a64324638e7831a0c76b36d06775a44460ab39e93163dd2d669acb649e9ffece63bea96d815d8a660317342b7')
b2sums=('b8d5fee02f4888290d979194b510783314ca8b148cb21e79663ac0a4327f21cffc41e9979778da0bcfc9aa482738b732cddf030f8f5bdc626f46fe60731b37fa')

build() {
  cd ${pkgname#python-}-$pkgver
  python -m build --wheel --no-isolation
}

check() {
  cd ${pkgname#python-}-$pkgver
  python -m venv --system-site-packages test-env
  test-env/bin/python -m installer dist/*.whl
  test-env/bin/python -Pm pytest -v --override-ini="addopts="
}

package() {
  cd ${pkgname#python-}-$pkgver
  python -m installer --destdir="$pkgdir" dist/*.whl
}
