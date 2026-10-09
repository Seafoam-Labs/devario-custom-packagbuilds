# Maintainer: Maxime Gauduin <alucryd@archlinux.org>
# Contributor: Thomas Jost <schnouki@schnouki.net>
# Contributor: Andrey Mikhaylenko <neithere@gmail.com>

pkgname=python-slugify
pkgver=9.1.2
pkgrel=1
pkgdesc='A Python slugify application that handles unicode'
arch=(any)
url=https://github.com/un33k/python-slugify
license=(MIT)
depends=(
  python
  python-text-unidecode
)
makedepends=(
  git
  python-build
  python-installer
  python-setuptools
  python-wheel
)
optdepends=('python-unidecode: Unidecode support')
source=(git+https://github.com/un33k/python-slugify.git#tag=v${pkgver})
b2sums=('6235d13106f2a5296800c7f1c55a70b31c11fcf8ae120ca9cfcd576397be337df6fd6bf8a48781a47dcf1f98a47897e8af8bb69b8810c7e77607ab708f44e441')

build() {
  cd python-slugify
  python -m build --wheel --no-isolation
}

package() {
  cd python-slugify
  python -m installer --destdir="${pkgdir}" dist/*.whl
  install -Dm 644 LICENSE -t "${pkgdir}"/usr/share/licenses/python-slugify/
}
