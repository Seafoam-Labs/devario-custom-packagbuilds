# Maintainer: Levente Polyak <anthraxx[at]archlinux[dot]org>
# Contributor: Chris Severance aur.severach aATt spamgourmet dott com
# Contributor: speps <speps at aur dot archlinux dot org>
# Contributor: Bastien Dejean <baskerville@lavabit.com>
# Contributor: Emmanuel Gil Peyrot <linkmauve@linkmauve.fr>

pkgname=lhasa
pkgver=0.5.0
pkgrel=1
pkgdesc='Free LZH/LHA archive tool'
url='https://github.com/fragglet/lhasa'
arch=(x86_64)
license=(ISC)
depends=(
  glibc
)
conflicts=(lha)
provides=(lha)
source=(https://github.com/fragglet/lhasa/releases/download/v${pkgver}/${pkgname}-${pkgver}.tar.gz{,.asc})
sha512sums=('26de1e454230e6ed33919ce0071d1f6aa8d35d2a534ce17956d32b9a73a162db8627bea58db6fef3f359ab88ca8331f991a04d7a6d696e949dd9e189b4835038'
            'SKIP')
validpgpkeys=('6D2C117E0310664497AA9546F6C2EE9C23354344') # Simon Howard <fraggle@soulsphere.org>

build() {
  cd ${pkgname}-${pkgver}
  ./configure --prefix=/usr
  make
}

check() {
  cd ${pkgname}-${pkgver}
  make check
}

package() {
  cd ${pkgname}-${pkgver}
  make DESTDIR="${pkgdir}" install
  install -Dm 644 COPYING.md -t "${pkgdir}/usr/share/licenses/${pkgname}"
}

# vim: ts=2 sw=2 et:
