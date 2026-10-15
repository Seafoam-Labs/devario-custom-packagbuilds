# Maintainer : Daniel Bermond <dbermond@archlinux.org>
# Maintainer : Santiago Torres-Arias <santiago@archlinux.org>
# Contributor: Simon Boulay <simon.boulay@alkeona.net>

pkgname=python-breathe
pkgver=5.1.0
pkgrel=1
pkgdesc='An extension to reStructuredText and Sphinx to be able to read and render Doxygen xml output'
arch=('any')
url='https://breathe.readthedocs.org/en/latest/'
license=('BSD-3-Clause')
depends=(
    'python'
    'python-docutils'
    'python-pygments'
    'python-sphinx')
makedepends=(
    'python-build'
    'python-flit-core'
    'python-installer'
    'python-setuptools'
    'python-wheel'
    'ruff')
checkdepends=(
    'doxygen'
    'python-pytest')
source=(
  "https://github.com/michaeljones/breathe/archive/v${pkgver}/${pkgname}-${pkgver}.tar.gz"
  "$pkgname-fix-tests-boolean-attr-compare.patch"
)
sha512sums=('d5c6a94b6a9b6071192ba0a31478245a96ea9f0bfbeeac4ae43817425f31ab1874bf106768d1ebb48911fb9ea3ce00b8a492ae3150159a12889a0486a91c1024'
            '093e1ff8544dfcf97fed12e0d8ae44645922dbdcfef630212543ece8718d4eb9501e9b14f92d6818d8f8091da68a3f36e6f5aeaee7407a6b27bf22903a869577')

prepare() {
  cd "breathe-${pkgver}"
  patch -Np1 < ../${pkgname}-fix-tests-boolean-attr-compare.patch
}

build() {
  cd "breathe-${pkgver}"
  make parser
  make format-parser
  python -m build --wheel --no-isolation
}

check() {
  cd "breathe-${pkgver}"
  
  # https://github.com/breathe-doc/breathe/issues/1036#issuecomment-3054012476
  PYTHONPATH="$PWD" pytest \
    --deselect 'tests/test_examples.py::test_example[class]' \
    --deselect 'tests/test_examples.py::test_example[cpp_function]' \
    --deselect 'tests/test_examples.py::test_example[group]' \
    --deselect 'tests/test_examples.py::test_example[headings]'
}

package_python-breathe() {
  python -m installer --destdir="$pkgdir" "breathe-${pkgver}/dist"/*.whl
  
  local _pyver
  _pyver="$(python -c 'import sys; print("%s.%s" %sys.version_info[:2])')"
  install -d -m755 "${pkgdir}/usr/share/licenses/${pkgname}"
  ln -s "../../../lib/python${_pyver}/site-packages/breathe-${pkgver}.dist-info/licenses/LICENSE" \
    "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
}
