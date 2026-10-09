# Maintainer: judd <jvinet@zeroflux.org>

_pkgbasename=libgpg-error
pkgname=lib32-$_pkgbasename
pkgver=1.61
pkgrel=1
pkgdesc="Support library for libgcrypt (32-bit)"
arch=(x86_64)
url="https://www.gnupg.org"
license=(LGPL-2.1-or-later
         'BSD-3-Clause OR LGPL-2.1-or-later'
         FSFULLR
         GPL-2.0-or-later)
depends=('lib32-glibc' $_pkgbasename)
source=(https://www.gnupg.org/ftp/gcrypt/libgpg-error/${_pkgbasename}-${pkgver}.tar.bz2{,.sig})
sha256sums=('7a85413f2bc354f4f8aa832b718af122e48965e9e0eb9012ee659c13c6385c93'
            'SKIP')
validpgpkeys=('D8692123C4065DEA5E0F3AB5249B39D24F25E3B6'  # Werner Koch
              'AC8E115BF73E2D8D47FA9908E98E9B2D19C6C8BD'  # NIIBE Yutaka (GnuPG Release Key) <gniibe@fsij.org>
              '6DAA6E64A76D2840571B4902528897B826403ADA') # "Werner Koch (dist signing 2020)"

prepare() {
  cd ${_pkgbasename}-${pkgver}
  sed -e 's|/var/example-target||' -i src/gpg-error-config-test.sh.in # Fix pkgconfig test with pkgconf 1.8
}

build() {
  export CC="gcc -m32"
  export CXX="g++ -m32"
  export PKG_CONFIG_PATH="/usr/lib32/pkgconfig"

  cd "${srcdir}"/${_pkgbasename}-${pkgver}
  ./configure --prefix=/usr --libdir=/usr/lib32
  make
}

check() {
  cd "${srcdir}"/${_pkgbasename}-${pkgver}
  make check
}

package() {
  cd "${srcdir}"/${_pkgbasename}-${pkgver}
  make DESTDIR="${pkgdir}/" install

  rm -rf "${pkgdir}"/usr/{include,share,bin}
}
