# Maintainer: Jan Alexander Steffens (heftig) <heftig@archlinux.org>
# Contributor: Levente Polyak <anthraxx[at]archlinux[dot]org>
# Contributor: Eric Bélanger <eric@archlinux.org>

pkgbase=lib32-flac
pkgname=(
  'lib32-flac'
)
pkgver=1.5.0
pkgrel=1
pkgdesc='Free Lossless Audio Codec (32-bit)'
url='https://xiph.org/flac/'
arch=('x86_64')
license=(
  'BSD-3-Clause'     # library
  'GPL-2.0-or-later' # apps
)
depends=(
  'flac'
  'lib32-gcc-libs'
  'lib32-glibc'
  'lib32-libogg'
)
makedepends=(
  'cmake'
  'git'
  'nasm'
  'ninja'
)
source=("git+https://github.com/xiph/flac#tag=${pkgver}")
b2sums=('2df577ac40233cdbea3389b076b239b266cdb3cf04a7a57982ae16b9c6f99af245b15590c19954d34cd3c8617ed2ddec3346c13c3f4b6e495df127104a978d19')

prepare() {
  cd flac

  # Shorten tests
  sed -i 's/FLAC__TEST_LEVEL=1/FLAC__TEST_LEVEL=0/' test/CMakeLists.txt
}

build() {
  local cmake_options=(
    -D BUILD_DOCS=OFF
    -D BUILD_EXAMPLES=OFF
    -D BUILD_PROGRAMS=OFF
    -D BUILD_SHARED_LIBS=ON
    -D CMAKE_BUILD_TYPE=None
    -D CMAKE_INSTALL_LIBDIR=/usr/lib32
    -D CMAKE_INSTALL_PREFIX=/usr
    -D INSTALL_MANPAGES=OFF
    -D NDEBUG=ON

    # Handled by our CFLAGS
    -D WITH_FORTIFY_SOURCE=OFF
    -D WITH_STACK_PROTECTOR=OFF
  )

  export CC="gcc -m32"
  export CXX="g++ -m32"
  export PKG_CONFIG="i686-pc-linux-gnu-pkg-config"

  cmake -S flac -B build -G Ninja "${cmake_options[@]}"
  cmake --build build
}

check() {
  ctest --test-dir build --output-on-failure --stop-on-failure -j1
}

package_lib32-flac() {
  provides=(
    'libFLAC.so'
    'libFLAC++.so'
  )

  DESTDIR="${pkgdir}" cmake --install build

  rm -r "${pkgdir}/usr/include"

  install -Dm 644 flac/COPYING.Xiph -t "${pkgdir}/usr/share/licenses/${pkgname}"
}

# vim:set sw=2 sts=-1 et:
