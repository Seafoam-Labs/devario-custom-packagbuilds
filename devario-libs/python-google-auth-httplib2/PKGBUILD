# Maintainer: Felix Yan <felixonmars@archlinux.org>

pkgname=python-google-auth-httplib2
pkgver=0.4.4
pkgrel=1
pkgdesc="Google Authentication Library: httplib2 transport"
url="https://github.com/googleapis/google-cloud-python/tree/main/packages/google-auth-httplib2"
license=('Apache-2.0')
arch=('any')
depends=('python-google-auth' 'python-httplib2')
makedepends=('git' 'python-build' 'python-installer' 'python-setuptools' 'python-wheel')
checkdepends=('python-pytest' 'python-flask' 'python-pytest-localserver')
source=("git+https://github.com/googleapis/google-cloud-python.git#tag=google-auth-httplib2-v$pkgver")
sha512sums=('d337b494dfb3696a56fdbf47b0983c5060b51140cea103ce32c77b928c08c1ec9e7ce450842b72dcb0ba3b7f9e6850b6764834e7a12d0db460b42c48466270e0')

build() {
  cd google-cloud-python/packages/google-auth-httplib2
  python -m build --wheel --no-isolation
}

check() {
  cd google-cloud-python/packages/google-auth-httplib2
  pytest
}

package() {
  cd google-cloud-python/packages/google-auth-httplib2
  python -m installer --destdir="$pkgdir" dist/*.whl
  install -Dm644 LICENSE -t "$pkgdir"/usr/share/licenses/$pkgname/
}
