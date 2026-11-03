# Maintainer: Felix Yan <felixonmars@archlinux.org>
# Contributor: Yen Chi Hsuan <yan12125 at gmail.com>
# Contributor: rich_o <rich_o@lavabit.com>
# Contributor: Jason St. John <jstjohn .. purdue . edu>
# Contributor: Daniel YC Lin <dlin.tw at gmail>

pkgname=python-texttable
pkgver=1.7.2
pkgrel=1
pkgdesc="Generate a formatted text table using ASCII characters"
arch=('any')
url="https://pypi.python.org/pypi/texttable/"
license=('MIT')
depends=('python')
optdepends=('python-cjkwrap: for better CJK support')
makedepends=('git' 'python-build' 'python-cjkwrap' 'python-installer' 'python-setuptools' 'python-wheel')
checkdepends=('python-pytest')
source=("git+https://github.com/foutaise/texttable.git#tag=v$pkgver")
sha512sums=('86692e95d7c7440449f8b5324f111ee2ebd28dda117a8dd79fa33fd61835cb739cde31ab5a056da0ba1744385776c00ab258f0c032695d2be9e66bc74e1bb509')

build() {
  cd texttable
  python -m build --wheel --no-isolation
}

check() {
  cd texttable
  pytest tests.py
}

package() {
  cd texttable
  python -m installer --destdir="$pkgdir" dist/*.whl
  install -Dm644 LICENSE -t "$pkgdir"/usr/share/licenses/$pkgname/
}
