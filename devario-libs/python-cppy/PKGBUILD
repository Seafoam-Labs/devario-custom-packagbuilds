# Maintainer: Felix Yan <felixonmars@archlinux.org>

pkgname=python-cppy
pkgver=1.3.1
pkgrel=1
pkgdesc="A collection of C++ headers which make it easier to write Python C extension modules"
url="https://github.com/nucleic/cppy"
license=('BSD-3-Clause')
arch=('any')
# cppy/__init__.py uses setuptools
depends=('python-setuptools')
makedepends=('git' 'python-build' 'python-installer' 'python-setuptools-scm' 'python-wheel')
checkdepends=('python-pytest')
source=("git+https://github.com/nucleic/cppy.git#tag=${pkgver}")
sha512sums=('89a0b11953637a3d7490219da7a3798c8a5e6c0fd84224f0793f92b7a6251c9bd116cdcbd23fa6cdd63111cc26028981965ef0599dfefa1b24e620e0f37b15f5')

build() {
  cd cppy
  python -m build -wn
}

check() {
  cd cppy
  python -m pytest
}

package() {
  cd cppy
  python -m installer -d "$pkgdir" dist/*.whl
  install -Dm644 LICENSE -t "$pkgdir"/usr/share/licenses/$pkgname/
}
