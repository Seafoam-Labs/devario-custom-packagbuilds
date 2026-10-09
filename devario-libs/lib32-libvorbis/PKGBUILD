# Maintainer: Maxime Gauduin <alucryd@archlinux.org>
# Contributor: Bartłomiej Piotrowski <bpiotrowski@archlinux.org>
# Contributor: Tobias Kieslich <tobias@archlinux.org>
# Contributor: dorphell <dorphell@archlinux.org>
# Contributor: John Proctor <jproctor@prium.net>

pkgbase=lib32-libvorbis
pkgname=(
  lib32-libvorbis
)
pkgver=1.3.7
pkgrel=4
pkgdesc='Reference implementation of the Ogg Vorbis audio format (32-bit)'
arch=(x86_64)
url=https://www.xiph.org/vorbis/
license=(BSD-3-Clause)
depends=(
  lib32-gcc-libs
  lib32-glibc
  lib32-libogg
  libvorbis
)
makedepends=(git)
_tag=0c55fa38933fd4bdb7db7c298b27e7bf2f2c5e98
source=(git+https://github.com/xiph/vorbis.git?signed#tag=${_tag})
sha256sums=('f58777e598c5ef1c9f21698e581f6e62729f3d343ec4aa270051fb304a56fe26')
validpgpkeys=(
  B7B00AEE1F960EEA0FED66FB9259A8F2D2D44C84 # Ralph Giles <giles@thaumas.net>
)

pkgver() {
  cd vorbis

  git describe --tags | sed 's/^v//'
}

prepare() {
  cd vorbis

  ./autogen.sh
}

build() {
  cd vorbis

  export CC="gcc -m32"
  export CXX="g++ -m32"
  export PKG_CONFIG="i686-pc-linux-gnu-pkg-config"

  ./configure \
    --prefix=/usr \
    --libdir=/usr/lib32 \
    --disable-static \
    --enable-shared
  sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0/g' libtool
  make
}

check() {
  make -C vorbis check -j1
}

package_lib32-libvorbis() {
  depends+=(libogg.so)
  provides=(
    libvorbis.so
    libvorbisenc.so
    libvorbisfile.so
  )

  make DESTDIR="${pkgdir}" -C vorbis install

  rm -r "${pkgdir}"/usr/{include,share}

  install -Dm 644 vorbis/COPYING -t "${pkgdir}/usr/share/licenses/${pkgname}"
}

# vim:set sw=2 sts=-1 et:
