# Maintainer: Carl Smedstad <carsme@archlinux.org>
# Maintainer: Levente Polyak <anthraxx[at]archlinux[dot]org>
# Contributor: Sven-Hendrik Haase <svenstaro@archlinux.org>
# Contributor: Carl George < arch at cgtx dot us >

pkgname=python-click
pkgver=8.5.0
pkgrel=1
pkgdesc="Simple wrapper around optparse for powerful command line utilities"
arch=('any')
url='https://click.palletsprojects.com/'
license=('BSD-3-Clause')
depends=('python')
makedepends=(
  'python-build'
  'python-flit-core'
  'python-installer'
)
checkdepends=(
  'less'
  'python-pytest'
)
source=("https://github.com/pallets/click/archive/$pkgver/$pkgname-$pkgver.tar.gz")
b2sums=('0e4ed5d703b3da63717edcc7e54e9cd9629a95635af1c54ee5d544a514be8ffc4e74d42cc7fbcd132669ba12265874e1707e2ae0dcfbe7de5b87f84ee0a4d8b8')

build() {
  cd ${pkgname#python-}-$pkgver
  python -m build --wheel --no-isolation --skip-dependency-check
}

check() {
  cd ${pkgname#python-}-$pkgver
  python -m venv --system-site-packages test-env
  test-env/bin/python -m installer dist/*.whl
  test-env/bin/python -m pytest
}

package() {
  cd ${pkgname#python-}-$pkgver
  python -m installer --destdir="$pkgdir" dist/*.whl
  install -vDm644 -t "$pkgdir/usr/share/licenses/$pkgname" LICENSE.txt
}
