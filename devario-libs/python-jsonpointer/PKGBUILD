# Maintainer: George Rawlinson <grawlinson@archlinux.org>
# Contributor: Daniel Wallace <danielwallace at gtmanfred dot com>
# Contributor: Limao Luo <luolimao+AUR@gmail.com>

pkgname=python-jsonpointer
pkgver=3.4
pkgrel=1
pkgdesc='Identify specific nodes in a JSON document (RFC 6901)'
arch=(any)
url='https://python-json-pointer.readthedocs.org/'
license=(BSD-3-Clause)
depends=(python)
makedepends=(
  git
  python-build
  python-installer
  python-setuptools
  python-wheel
)
source=("$pkgname::git+https://github.com/stefankoegl/python-json-pointer#tag=v$pkgver")
sha512sums=('44b54d1a030a0cd17b703eb1b4ad5cdc6239d5ffbc13adf8711c903590734dadd4e9d1637d6f3b4414f7ae9effc5fec3225b76341cc5dcc935d3dc2a3752ddfe')
b2sums=('44099838fa4a42a39dcc26f881f5c215bf7294be7864d70fb99fa4c22eea4df524473cc0bffd88ec1ff1e6c0e1bde445a2aca327e10d0d8a919da6f1a18762dd')

build() {
  cd "$pkgname"

  python -m build --wheel --no-isolation
}

check() {
  cd "$pkgname"

  python -m unittest
}

package() {
  cd "$pkgname"

  python -m installer --destdir="$pkgdir" dist/*.whl

  # license
  install -vDm644 -t "$pkgdir/usr/share/licenses/$pkgname" LICENSE.txt
}
