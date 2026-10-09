# Maintainer: Bruno Pagani <archange@archlinux.org>
# Contributor: Guillaume Horel <guillaume.horel@gmail.com>

_pkg=orc
pkgname=apache-${_pkg}
pkgver=2.3.1
pkgrel=4
pkgdesc="Columnar storage for Hadoop workloads."
arch=(x86_64)
url="https://orc.apache.org"
license=(Apache-2.0)
depends=(
  abseil-cpp
  glibc
  libgcc
  libstdc++
  lz4
  protobuf
  snappy
  zlib
  zstd
)
makedepends=(cmake git)
checkdepends=(gtest)
source=(
  ${pkgname}::git+https://github.com/apache/orc.git#tag=v${pkgver}
  fix-find-package-mode.patch
)
sha256sums=('ff3d1b6719318da33d540b3a7df02dfcbd2a9fea7b57d98d0ab1647346078eeb'
            '458ec83da45446442a32dd5bd21b8569a2f20c4cef07fd03ec0044f5604260ea')
validpgpkeys=(F28C9C925C188C35E345614DEDA00CE834F0FC5C  # Dongjoon Hyun (CODE SIGNING KEY) <dongjoon@apache.org>
              AA94E2A8F0A0B7167305C5232D9F6201DECDFA29) # William Hyun (CODE SIGNING KEY) <william@apache.org>

prepare(){
  cd ${pkgname}
  sed -i 's/orc STATIC/orc SHARED/' c++/src/CMakeLists.txt

  # Our zlib package does not provide files for the config-mode of find_package.
  # Also when "NAMES" is given, find_package cannot find zlib.
  patch -p1 < ../fix-find-package-mode.patch
}

build(){
  # Fix build with protobuf - avoid errors like
  # /usr/bin/ld: /usr/lib/libabsl_log_internal_check_op.so.2508.0.0: error adding symbols: DSO missing from command line
  # Apparently protobuf's cmake targets don't specify all dependencies properly.
  # Solution from https://github.com/protocolbuffers/protobuf/issues/14500#issuecomment-1781292098
  LDFLAGS+=" -Wl,--copy-dt-needed-entries"

  local cmake_options=(
    -B build
    -S ${pkgname}
    -DCMAKE_BUILD_TYPE=None
    -DCMAKE_INSTALL_PREFIX=/usr
    -DSTOP_BUILD_ON_WARNING=OFF
    -DLZ4_HOME=/usr  # needed to use orc's FindLZ4Alt.cmake
    -DORC_PREFER_STATIC_PROTOBUF=OFF
    -DORC_PREFER_STATIC_SNAPPY=OFF
    -DORC_PREFER_STATIC_LZ4=OFF
    -DORC_PREFER_STATIC_ZSTD=OFF
    -DORC_PREFER_STATIC_ZLIB=OFF
    -DBUILD_LIBHDFSPP=OFF
    -DBUILD_JAVA=OFF
    -DINSTALL_VENDORED_LIBS=OFF
    -Wno-dev
  )
  cmake "${cmake_options[@]}"
  cmake --build build
}

check(){
  ctest --test-dir build --output-on-failure
}

package(){
  DESTDIR="${pkgdir}" cmake --install build
}
