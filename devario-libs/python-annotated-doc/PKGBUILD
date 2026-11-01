# Maintainer: Robin Candau <antiz@archlinux.org>

pkgname=python-annotated-doc
_pkgname=${pkgname#python-}
pkgver=0.0.5
pkgrel=1
pkgdesc="Document parameters, class attributes, return types, and variables inline, with Annotated"
arch=('any')
url="https://github.com/fastapi/annotated-doc"
license=('MIT')
depends=('python')
makedepends=('python-build' 'python-installer' 'python-wheel' 'python-pdm-backend')
checkdepends=('python-pytest' 'python-typing_extensions' 'python-typer')
source=("${_pkgname}-${pkgver}.tar.gz::${url}/archive/${pkgver}.tar.gz")
sha256sums=('b1df640b7d5658b8d3807b42d51291ed3f24e43d4a059092c11495a3f7714fc9')

build() {
	cd "${_pkgname}-${pkgver}"
	python -m build --wheel --no-isolation
}

check() {
	cd "${_pkgname}-${pkgver}"
	python -m venv --system-site-packages test-env
	test-env/bin/python -m installer dist/*.whl
	PATH="${PWD}/test-env/bin:${PATH}" test-env/bin/python -m pytest
}

package() {
	cd "${_pkgname}-${pkgver}"
	python -m installer --destdir="${pkgdir}" dist/*.whl
	
	install -Dm 644 README.md "${pkgdir}/usr/share/doc/${pkgname}/README.md"
	install -Dm 644 LICENSE "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
}
