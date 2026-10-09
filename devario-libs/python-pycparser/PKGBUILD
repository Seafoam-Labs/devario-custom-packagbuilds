# Maintainer: Felix Yan <felixonmars@archlinux.org>
# Contributor: Justin Dray <justin@dray.be>
# Contributor: Alexander Rødseth <rodseth@gmail.com>
# Contributor: lang2 <wenzhi.liang@gmail.com>

pkgname=python-pycparser
pkgver=3.01
pkgrel=1
pkgdesc='C parser and AST generator written in Python'
url='https://github.com/eliben/pycparser'
depends=('python')
makedepends=('git' 'python-build' 'python-installer' 'python-setuptools')
arch=('any')
license=('BSD-3-Clause')
source=("git+https://github.com/eliben/pycparser.git#tag=release_v$pkgver")
sha512sums=('8e4d918f13ab22c41c5bddf4703eadddc63c0cbbb3ac1e65a52fe41a20387e6505f82c369fc36b408e5d5ec7e80788e78e33e28ecf2b89fc8c441096e5ae165f')

build() {
  cd pycparser
  python -m build --wheel --no-isolation
}

check() {
  cd pycparser
  python -m unittest discover
}

package() {
  cd pycparser

  python -m installer --destdir="$pkgdir" dist/*.whl
  install -Dm644 LICENSE -t "$pkgdir"/usr/share/licenses/$pkgname/
}
