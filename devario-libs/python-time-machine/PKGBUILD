# Maintainer: George Rawlinson <grawlinson@archlinux.org>
# Maintainer: Daniel M. Capella <polyzen@archlinux.org>

pkgname=python-time-machine
pkgver=3.5.1
pkgrel=1
pkgdesc='Travel through time in your tests'
arch=(x86_64)
url='https://github.com/adamchainz/time-machine'
license=(MIT)
depends=(
  glibc
  python
  python-dateutil
)
makedepends=(
  git
  python-build
  python-installer
  python-setuptools
  python-wheel
)
checkdepends=(
  python-pytest
  python-pytest-randomly
  python-tokenize-rt
  python-freezegun
  python-hypothesis
)
optdepends=(
  'python-pytest: for pytest plugin'
  'python-tokenize-rt: for the migration tool'
)
source=("$pkgname::git+$url#tag=$pkgver")
sha512sums=('e947eb6a0eef7b6d5176ee87579e4cfe344ceb04e6f926e340dae5b4494f61bba0efce43e8d501db81bbe527f25b403b72f2bbbae8c925fb78a72a07c11a0554')
b2sums=('97d71b30a69b680824c76da8c641f749a8f104004d7f58a7c86d73be50e988d5d768543433895e97066e11d8ca61c9ab7e1e22a645bb94ae70621b11586a60d9')

build() {
  cd "$pkgname"

  python -m build --wheel --no-isolation
}

check() {
  cd "$pkgname"

  local pytest_options=(
    -vv
    --deselect tests/test_fuzz.py::test_travel_to_aware_datetime
  )

  python -m venv --system-site-packages test-env
  test-env/bin/python -m installer dist/*.whl
  test-env/bin/python -m pytest "${pytest_options[@]}"
}

package() {
  cd "$pkgname"

  python -m installer --destdir="$pkgdir" dist/*.whl

  # license
  install -vDm644 -t "$pkgdir/usr/share/licenses/$pkgname" LICENSE
}
