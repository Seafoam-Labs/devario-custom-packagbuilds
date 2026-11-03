# Maintainer: Felix Yan <felixonmars@archlinux.org>
# Contributor: Simon Sapin <simon dot sapin at exyr dot org>
# Contributor: Kyle Keen <keenerd@gmail.com>

pkgname=python-cjkwrap
pkgver=2.2
pkgrel=14
pkgdesc="A library for wrapping and filling CJK text."
url="https://github.com/fgallaire/cjkwrap"
license=('LGPL-3.0-or-later')
arch=('any')
depends=('python')
makedepends=('git' 'python-build' 'python-installer' 'python-setuptools' 'python-wheel')
source=("git+https://github.com/fgallaire/cjkwrap.git#tag=v$pkgver")
sha512sums=('a4d3e26e0a8401f8b157bdd682c01ec286c6a0e3f7a16cea97ad27abf6dfc73a3c255164ce8da8afb42fec5db83603a464a6757946c1f72fbfc489ebd145b2fc')

build() {
  cd cjkwrap
  python -m build --wheel --no-isolation
}

package() {
  cd cjkwrap
  python -m installer --destdir="$pkgdir" dist/*.whl
}
