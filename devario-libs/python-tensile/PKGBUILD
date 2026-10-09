# Maintainer: Torsten Keßler <tpkessler at archlinux dot org>
# Maintainer: Christian Heusel <gromit@archlinux.org>

pkgname=python-tensile
pkgver=10.0
pkgrel=1
pkgdesc="benchmark-driven backend libraries for general matrix-matrix multiplications"
arch=('any')
url='https://rocm.docs.amd.com/projects/Tensile/en/latest/'
license=('MIT')
depends=('python' 'python-msgpack' 'python-pyaml' 'python-joblib')
makedepends=('git' 'cmake' 'python-build' 'python-installer' 'python-wheel' 'python-setuptools')
_git='https://github.com/ROCm/rocm-libraries'
source=("rocm-libraries::git+$_git.git#tag=therock-$pkgver")
sha256sums=('bc3cc5a8f4bba70d2f7f9cb6582210a16244bfbf353cebc667db05bb756b5b20')
_dirname="rocm-libraries/shared/tensile"

prepare() {
	cd ${_dirname}

	# https://src.fedoraproject.org/rpms/python-tensile/blob/rawhide/f/python-tensile.spec#_85
	sed -i -e 's@${Tensile_PREFIX}/bin/TensileGetPath@TensileGetPath@g' Tensile/cmake/TensileConfig.cmake
	sed -i -e 's@opt/rocm@usr@g' Tensile/Common.py
	sed -i -e 's@opt/rocm@usr@g' Tensile/Tests/yaml_only/test_config.py
	sed -i -e 's@globalParameters["IgnoreAsmCapCache"] = False@globalParameters["IgnoreAsmCapCache"] = True@' Tensile/Common.py
	sed -i -e 's@arguments["IgnoreAsmCapCache"] = args.IgnoreAsmCapCache@arguments["IgnoreAsmCapCache"] = True@' Tensile/TensileCreateLibrary.py
	sed -i -e 's@if not ignoreCacheCheck and derivedAsmCaps@if False and derivedAsmCaps@' Tensile/Common.py
}

build() {
	cd ${_dirname}
	python -m build --wheel --no-isolation
}

package() {
	cd ${_dirname}
	python -m installer --destdir="$pkgdir" dist/*.whl
	# cmake files are installed to the wrong location, /usr/cmake.
	# Move them to the right directory.
	mkdir -p "$pkgdir"/usr/lib/cmake/Tensile
	mv "$pkgdir"/usr/cmake/* "$pkgdir"/usr/lib/cmake/Tensile
	rm -rf "$pkgdir"/usr/cmake
	install -vDm644 LICENSE.md "$pkgdir"/usr/share/licenses/"$pkgname"/LICENSE
}
