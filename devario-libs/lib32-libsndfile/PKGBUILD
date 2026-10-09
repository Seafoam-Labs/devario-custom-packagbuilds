# Maintainer: Jan Alexander Steffens (heftig) <jan.steffens@gmail.com>
# Maintainer: David Runge <dvzrv@archlinux.org>

_name=libsndfile
pkgname=lib32-$_name
pkgver=1.2.2
pkgrel=3
pkgdesc="A C library for reading and writing files containing sampled audio data (32-bit)"
arch=(x86_64)
url="https://libsndfile.github.io/libsndfile/"
license=(LGPL-2.1-or-later)
depends=(
  lib32-glibc
  lib32-opus
  $_name=$pkgver
)
makedepends=(
  cmake
  lib32-alsa-lib
  lib32-flac
  lib32-libogg
  lib32-libvorbis
  lib32-sqlite
  python
)
provides=(libsndfile.so)
source=(https://github.com/$_name/$_name/releases/download/$pkgver/$_name-$pkgver.tar.xz{,.asc})
sha512sums=('a6e3ea3ac5d91befaa99f6a31a3fac44e7b7c11f1de4698167317a461d5a19a2651d47486a920b34400f18367b4f6173bf0c1c9ba80eb682cece1b5beee352a0'
            'SKIP')
b2sums=('bc8e49983d9ad9dfd98984e2ffef501c6f576480e556e9f9ef91c7d597524cc1bb8baed15dfef8e239f72c42136c524117029eb8271f3a2c9d607fee490279b5'
        'SKIP')
validpgpkeys=(
  '6A91A5CF22C24C99A35E013FCFDCF91FB242ACED'  # Erik de Castro Lopo <erikd@mega-nerd.com>
  '9B1CFD2E92239C4B288E025F9D0D1F1CCB35FF8C'  # evpobr evpobr@gmail.com
  '31D95CAB6D80D262244A1750A47620E801E47E95'  # David Seifert soap@gentoo.org
)

build() {
  export CFLAGS+=" -m32"
  export CXXFLAGS+=" -m32"
  export LDFLAGS+=" -m32"
  export PKG_CONFIG_PATH='/usr/lib32/pkgconfig'

  local cmake_options=(
    -B build
    -D BUILD_SHARED_LIBS=ON
    -D CMAKE_BUILD_TYPE=None
    -D CMAKE_INSTALL_LIBDIR=lib32
    -D CMAKE_INSTALL_PREFIX=/usr
    -D ENABLE_MPEG=OFF
    -S $_name-$pkgver
    -W no-dev
  )
  local cmake_test_options=(
    -B build-test
    -D CMAKE_BUILD_TYPE=None
    -D CMAKE_INSTALL_LIBDIR=lib32
    -D CMAKE_INSTALL_PREFIX=/usr
    -D ENABLE_MPEG=OFF
    -S $_name-$pkgver
    -W no-dev
  )

  cmake "${cmake_test_options[@]}"
  cmake --build build-test --verbose
  cmake "${cmake_options[@]}"
  cmake --build build --verbose
}

check() {
  ctest --test-dir build-test --output-on-failure
}

package() {
  depends+=(
    lib32-flac libFLAC.so
    lib32-libogg libogg.so
    lib32-libvorbis libvorbis.so libvorbisenc.so
  )

  DESTDIR="$pkgdir" cmake --install build
  install -vDm 644 $_name-$pkgver/{AUTHORS,ChangeLog,README} -t "$pkgdir/usr/share/doc/$pkgname"

  # remove everything that is provided by libsndfile
  rm -rf "$pkgdir/usr/"{bin,include,share/{man,doc/$_name}}
}
