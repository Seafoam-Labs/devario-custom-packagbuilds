# Maintainer: Caleb Maclennan <caleb@alerque.com>
# Maintainer: George Rawlinson <grawlinson@archlinux.org>
# Contributor: Kyle Keen <keenerd@gmail.com>
# Contributor: Angel Velasquez <angvp@archlinux.org>
# Contributor: Andrew Antle <andrew dot antle at gmail dot com>
# Contributor: Thomas Dziedzic < gostrc at gmail >
# Contributor: Chaiwat Suttipongsakul <cwt at bashell dot com>

pkgname=python-markdown
pkgver=3.11.0
pkgrel=1
pkgdesc="Python implementation of John Gruber's Markdown"
arch=(any)
url='https://python-markdown.github.io/'
license=(BSD-3-Clause)
depends=(python)
makedepends=(
  git
  python-build
  python-installer
  python-setuptools
  python-wheel
)
optdepends=(
  'python-yaml: parse Python in YAML metadata'
  'python-pygments: Code highlighting'
)
checkdepends=(python-yaml python-pygments)
source=("$pkgname::git+https://github.com/Python-Markdown/markdown#tag=$pkgver")
sha512sums=('1c7624147ff0d2844add5aa4be76374b1af028d3d28f80f4b472e2e5f0cc93f798d4498848afe33db3a919cbad372de451e7efc3eaef5f56b284187d28610b7b')
b2sums=('a7fb41fccb630e2378a3d0a929875704d7afd9608caeaf38407773d0a6c713db54bccb7cbbb0b3acfd62fc5807d9a484227cecc56893cc1894488013de0c4fec')

build() {
  cd "$pkgname"

  python -m build --wheel --no-isolation
}

check() {
  cd "$pkgname"

  python -m unittest discover tests
}

package() {
  cd "$pkgname"

  python -m installer --destdir="$pkgdir" dist/*.whl

  # license
  install -vDm644 -t "$pkgdir/usr/share/licenses/$pkgname" LICENSE.md
}
