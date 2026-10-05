# Maintainer: George Rawlinson <grawlinson@archlinux.org>
# Contributor: Kyle Keen <keenerd@gmail.com>
# Contributor: wenLiangcan <boxeed at gmail dot com>

pkgname=python-wcwidth
pkgver=0.9.2
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
sha512sums=('5b940f9c3b6cf82c61d745713a775e6e16cc1a7220be22cbea7be54d79d873c6b09239ab1e1c3af0b782fcefd8266661e8a506a5929d028ca783f4752d278c95')
b2sums=('2d6989683d5303d98f4254142db3e9289e90b2061f486cc8f90e19c1d31cf5e77175aea4253fafe1c0797ec2142780e5ea332f76429c93e6b510c4ff26d4a388')

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
