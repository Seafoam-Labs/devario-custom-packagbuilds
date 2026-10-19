# Maintainer: Robin Candau <antiz@archlinux.org>
# Contributor: David Runge <dvzrv@archlinux.org>
# Contributor: NicoHood <archlinux {cat} nicohood {dog} de>
# Contributor: Sven Klomp <mail@klomp.eu>

pkgname=python-gnupg
pkgver=0.5.7
pkgrel=1
pkgdesc="A wrapper for the Gnu Privacy Guard (GPG or GnuPG)"
url="https://docs.red-dove.com/python-gnupg"
arch=('any')
license=('BSD-3-Clause')
depends=('gnupg' 'python')
makedepends=('python-build' 'python-installer' 'python-setuptools' 'python-wheel')
checkdepends=('python-pytest')
source=("${pkgname}-${pkgver}.tar.gz::https://github.com/vsajip/python-gnupg/archive/refs/tags/${pkgver}.tar.gz"
        "${pkgname}-${pkgver}.tar.gz.asc::https://github.com/vsajip/python-gnupg/releases/download/${pkgver}/source-${pkgver}.tar.gz.asc"
        'drop-setuptools-version-upperbound.patch')
sha512sums=('6558359e060f3914a321f1161203d4441417e75247344cd527cf3337bbf57379e317fdefefc8457559f2a669c26fbb13eefaa0495abbef85e4303cd91a651f82'
            'SKIP'
            '63dd9b341f010bc8c9c659f76767e50e15cfdba708930136a401516efb171d9f1d59f467eea649a39fdc6f6bfe8c46d45c763bde52937c8dcbcc880f496c0e2a')
b2sums=('cf8360e2b116871d3c1f74c45d28315f221e09a3d189113db57755b695686fe60dde3ccae32a128c960e5872ee37598606362f63788261989e834741664bc25b'
        'SKIP'
        '412fdc33ced27adfeee14598717d1cd40f34689cb324762b0fee24d9d40873e90ccc4ff4f6f5452745e49383bbaa56d5f509714fbab1b0837e7cd1545a9cbcec')
validpgpkeys=('CA749061914EAC138E66EADB9147B477339A9B86') # Vinay Sajip (CODE SIGNING KEY) <vinay_sajip@yahoo.co.uk>

prepare() {
	cd "${pkgname}-${pkgver}"
	patch -Np1 -i "${srcdir}/drop-setuptools-version-upperbound.patch"
}

build() {
	cd "${pkgname}-${pkgver}"
	python -m build --wheel --no-isolation
}

check() {
	cd "${pkgname}-${pkgver}"
	export NO_EXTERNAL_TESTS='true'
	pytest
}

package() {
	cd "${pkgname}-${pkgver}"
	python -m installer --destdir="${pkgdir}" dist/*.whl
	install -Dm 644 LICENSE.txt "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE.txt"
	install -Dm 644 README.rst "${pkgdir}/usr/share/doc/${pkgname}/README.rst"
}
