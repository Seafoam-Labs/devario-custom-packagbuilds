# Maintainer: Caleb Maclennan <caleb@alerque.com>
# Contributor: loathingkernel <username at gmail dot com>

pkgname=python-pybcj
_pyname=${pkgname#python-}
pkgver=1.0.8
pkgrel=1
pkgdesc='BCJ (Branch-Call-Jump) filter for python'
arch=(x86_64)
url="https://github.com/miurahr/$_pyname"
license=(LGPL-2.1-only)
depends=(python)
makedepends=(python-{build,installer,wheel}
             python-setuptools-scm)
checkdepends=(python-pytest
              python-hypothesis)
_archive="$_pyname-$pkgver"
# PyPi package >= 1.0.7 does not include tests
# source=("https://files.pythonhosted.org/packages/source/${_pyname::1}/$_pyname/$_archive.tar.gz")
source=("$url/archive/v$pkgver/$_archive.tar.gz")
sha256sums=('c5dcda1403301f6f70db40a8b7e89dab4d230a3b634a529b98820d351d874eeb')

build() {
	cd "$_archive"
	python -m build -wn
}

check() {
	cd "$_archive"
	local _pyver=$(python -c 'import sys; print("".join(map(str, sys.version_info[:2])))')
	export PYTHONPATH="$PWD/build/lib.linux-$CARCH-cpython-$_pyver"
	python -m pytest -rsx
}

package() {
	cd "$_archive"
	python -m installer -d "$pkgdir" dist/*.whl
}
