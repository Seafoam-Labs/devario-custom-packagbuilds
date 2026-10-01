# Maintainer: George Rawlinson <grawlinson@archlinux.org>
# Contributor: Kyle Keen <keenerd@gmail.com>
# Contributor: wenLiangcan <boxeed at gmail dot com>

pkgname=python-wcwidth
pkgver=0.9.1
pkgrel=1
pkgdesc='Python library that measures the width of unicode strings rendered to a terminal'
arch=(x86_64)
url='https://github.com/jquast/wcwidth'
license=(MIT)
depends=(glibc python)
makedepends=(
  git
  python-build
  python-installer
  python-setuptools
)
checkdepends=(python-pytest)
source=("$pkgname::git+$url#tag=$pkgver")
sha512sums=('560312b6a7cf8ad1736da6ec017dc0c575a4f30c9cee40d38346ac548457764927982c2e7b57055fdfad77b42823ca2fe38446e8dc0e0a47f99790fd591aeb36')
b2sums=('c3e63b6ac19a98142e84c04f9c12e9a57f4adac594047201c6dc04e49211126abf7d2677a9eb2528f50f09a1dee5a6b4ad3a49598a62058dcefb8f5c26fd553e')

build() {
  cd "$pkgname"

  CIBUILDWHEEL=1 python -m build --wheel --no-isolation
}

check() {
  cd "$pkgname"

  rm -v tox.ini

  # temporary install
  python -m installer --destdir="$(pwd)/tmp" dist/*.whl
  local site_packages=$(python -c "import site; print(site.getsitepackages()[0])")
  export PYTHONPATH="$(pwd)/tmp/$site_packages"

  WCWIDTH_PYTHON=1 pytest -v
}

package() {
  cd "$pkgname"

  python -m installer --destdir="$pkgdir" dist/*.whl

  # license
  install -vDm644 -t "$pkgdir/usr/share/licenses/$pkgname" LICENSE
}
