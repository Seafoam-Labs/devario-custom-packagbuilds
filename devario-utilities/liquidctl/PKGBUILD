# Maintainer: Filipe Laíns (FFY00) <lains@archlinux.org>

pkgname=liquidctl
pkgver=1.16.0
pkgrel=1
arch=('any')
url='https://github.com/liquidctl/liquidctl'
license=('GPL3')
pkgdesc='Cross-platform CLI and Python drivers for AIO liquid coolers and other devices'
depends=('python' 'python-docopt' 'python-pyusb' 'python-hidapi' 'python-colorlog' 'i2c-tools' 'python-pillow' 'python-crcmod')
makedepends=('git' 'python-setuptools-scm' 'python-build' 'python-installer' 'python-wheel')
checkdepends=('python-pytest')
source=("git+$url.git?signed#tag=v$pkgver")
validpgpkeys=('23F335ED4E829797734B22F65841AF7406AF7AD0') # Jonas Tadeu Silva Malaco Filho <jonas@jonasmalaco.com>
sha512sums=('ae8ce2898be0aa13a403180730a95d313efd4341630fa7ef0667176e050de4097ed12d744e1baaeccd52bd7ca2774fa3168d37974b436f98cde8dfb0e57bb874')

build() {
  cd "${pkgname}"

  export DIST_NAME='Arch Linux'
  export DIST_PACKAGE="$pkgver-$pkgrel"
  export SETUPTOOLS_SCM_PRETEND_VERSION="$pkgver"

  python -m build --wheel --no-isolation
}

check() {
  cd "${pkgname}"

  mkdir runtime
  XDG_RUNTIME_DIR=runtime python -m pytest
}

package() {
  cd "${pkgname}"

  python -m installer --destdir="${pkgdir}" dist/*.whl

  install -Dm 644 extra/linux/71-liquidctl.rules "${pkgdir}"/usr/lib/udev/rules.d/71-liquidctl.rules

  # Install documentation
  install -dm 755 "${pkgdir}"/usr/share/doc/"${pkgname}"
  cp -r -a --no-preserve=ownership docs/* "${pkgdir}"/usr/share/doc/"${pkgname}"
  install -Dm 644 liquidctl.8 "${pkgdir}"/usr/share/man/man8/liquidctl.8
}
