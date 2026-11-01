# Maintainer: Antonio Rojas <arojas@archlinux.org>
# Contributor: Aloxaf <aloxafx@gmail.com>
# Contributor: Alex Hirzel <alex@hirzel.us>

_name=playwright-python
pkgname=python-playwright
pkgver=1.64.1
pkgrel=1
pkgdesc='A Python library to automate Chromium, Firefox and WebKit browsers with a single API'
arch=(any)
url='https://github.com/microsoft/playwright-python'
license=(Apache-2.0)
depends=(nodejs
         python
         python-greenlet
         python-pyee
         sh)
makedepends=(git
             npm
             python-auditwheel
             python-build
             python-installer
             python-setuptools-scm
             python-wheel
             zip)
checkdepends=(python-autobahn
              python-flaky
              python-objgraph
              python-pixelmatch
              python-pyopenssl
              python-pytest chromium
              python-pytest-playwright
              python-requests)
source=(git+https://github.com/microsoft/$_name#tag=v$pkgver
        https://registry.npmjs.org/playwright-core/-/playwright-core-$pkgver.tgz)
sha256sums=('a375c7e33314a432bafd63c3efb59a51823d6587fcb233036bb5eaa646ced6c0'
            '3af03703c967c95037454f2283f709d53ce804a4776d4219d319f5bbcc2a0185')

prepare() {
  zip -qr playwright-$pkgver-linux.zip package

  cd $_name
  sed -e 's|==.*\"|"|' -i pyproject.toml # Drop dependency version constraints
  sed -e "s|driver_version = \".*\"|driver_version = \"$pkgver\"|" -i setup.py
  install -Dm644 "$srcdir"/playwright-$pkgver-linux.zip -t driver
}

build() {
  cd $_name
  SETUPTOOLS_SCM_PRETEND_VERSION="$pkgver" \
  python -m build --wheel --no-isolation
}

# Testing is utterly broken
#check() {
#  cd $_name
#  PYTHONPATH=$PWD \
#  pytest -v
#}

package() {
  cd $_name
  python -m installer --destdir="$pkgdir" dist/*.whl

# Replace bundled node with system one
  rm "$pkgdir"/usr/lib/python*/site-packages/playwright/driver/node
  ln -s /usr/bin/node -t "$pkgdir"/usr/lib/python*/site-packages/playwright/driver/
}
