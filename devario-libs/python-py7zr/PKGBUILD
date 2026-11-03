# Maintainer: Caleb Maclennan <caleb@alerque.com>
# Contributor: Eli Schwartz <eschwartz@archlinux.org>

pkgname=python-py7zr
pkgver=1.1.4
pkgrel=1
pkgdesc='Pure Python 7-zip library'
arch=(any)
url='https://github.com/miurahr/py7zr'
license=(LGPL-2.1-or-later)
depends=(
  python
  python-brotli
  python-brotlicffi
  python-psutil
  python-multivolumefile
  python-pybcj
  python-pycryptodomex
  python-pyppmd
  python-texttable
  python-inflate64
)
makedepends=(
  git
  python-build
  python-installer
  python-setuptools
  python-setuptools-scm
  python-wheel
)
checkdepends=(
  p7zip
  python-requests
  python-py-cpuinfo
  python-pytest
  python-pytest-benchmark
  python-pytest-httpserver
  python-pytest-timeout
)
optdepends=()
options=(!lto)
source=("$pkgname::git+$url#tag=v$pkgver")
sha512sums=('8dbd9c94e30159ebc29a6436d7fd2467452f0ff3f188b3cfa7065301cc5f90ea60a0549df117fb11240e97c8368882d7f6d409bc6d4670d1c9eb6b204f7635b1')
b2sums=('fe65cdb1fb84e52b2d3676b83095b226476a5befda5efe464a824f4da398b947a0260f787f0bc157848f4b35372ad0df0a8683e791232ce3a6ba9a06a3af3b07')

build() {
  cd "$pkgname"

  python -m build --wheel --no-isolation
}

check() {
  cd "$pkgname"

  local pytest_options=(
    -vv
    -rsx
		--deselect tests/test_concurrent.py
		--deselect tests/test_extra_codecs.py
		-m 'not benchmark and not remote_data'
  )
  
  pytest "${pytest_options[@]}"
}

package() {
  cd "$pkgname"

  python -m installer --destdir="$pkgdir" dist/*.whl
}
