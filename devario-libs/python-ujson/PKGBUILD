# Maintainer: Levente Polyak <anthraxx[at]archlinux[dot]org>
# Maintainer: Massimiliano Torromeo <massimiliano.torromeo@gmail.com>

pkgname=python-ujson
_pkgname=ultrajson
pkgver=6.0.0
pkgrel=1
pkgdesc="Ultra fast JSON encoder and decoder for Python"
url="https://github.com/ultrajson/ultrajson"
arch=('x86_64')
license=('BSD')
depends=('python')
makedepends=(python-setuptools-scm python-wheel python-build python-installer)
checkdepends=('python-pytest')
source=(https://github.com/ultrajson/ultrajson/archive/$pkgver/$pkgname-$pkgver.tar.gz)
sha512sums=('79042cee1aba89e1f67db7d21ee2050aea346aa2a383b40ae3da170560a530b82aa0e42294f49f235ced51ac0c39808354448fae5500e23bdf9ea8ceb8949746')
b2sums=('d5dcf4837951c0167892573498ee33867cf296a22f8016c57292bb89901825c288c51c6aff3e01131398f9d296c3683b57e566312be1e5a8dab51f076753c0ff')

export SETUPTOOLS_SCM_PRETEND_VERSION=$pkgver

build() {
  cd ${_pkgname}-${pkgver}
  python -m build --wheel --no-isolation
}

check() {
  cd ${_pkgname}-${pkgver}
  local PYTHONVERSION="$(python -c 'import sys; print("{}{}".format(sys.version_info.major, sys.version_info.minor))')"
  PYTHONPATH="build/lib.linux-${CARCH}-cpython-${PYTHONVERSION}" pytest
}

package() {
  cd ${_pkgname}-${pkgver}
  python -m installer --destdir="$pkgdir" dist/*.whl
  install -Dm 644 LICENSE.txt -t "${pkgdir}/usr/share/licenses/${pkgname}"
  install -Dm 644 README.md -t "${pkgdir}/usr/share/doc/${pkgname}"
}

# vim: ts=2 sw=2 et:
