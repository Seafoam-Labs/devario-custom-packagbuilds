# Maintainer: Jakub Klinkovský <lahwaacz at archlinux dot org>

_name=ucc
pkgname=openucc
pkgver=1.9.0
pkgrel=1
pkgdesc="Unified Collective Communication Library"
arch=(x86_64)
url="https://github.com/openucx/ucc"
license=(BSD-3-Clause)
depends=(
  glibc
  libstdc++
  openucx
)
makedepends=(
  cuda
  hip-runtime-amd
  rocm-llvm
  nccl
  rccl
  rdma-core
)
checkdepends=(
  gtest
)
optdepends=(
  'cuda: for CUDA execution engine and transport layer'
  'hip-runtime-amd: for HIP execution engine'
  'nccl: for NCCL transport layer'
  'rccl: for RCCL transport layer'
  'rdma-core: for InfiniBand transport layer'
)
provides=(
  libucc.so
)
source=(
  "$pkgname-$pkgver.tar.gz::$url/archive/refs/tags/v$pkgver.tar.gz"
)
b2sums=('5459f1e64ea27bea8e89932eb90509fe39719bd4adc82ecf3172971da6d2f9510dc8e2e5160130ac31163f9ae383168952183107ac04d0d954c0b5923ae233e1')

prepare() {
  cd $_name-$pkgver
  # fix building with gcc 15 (yes ucx bundles its old version of gtest...)
  sed -i '1i\#include <cstdint>' test/gtest/common/gtest-all.cc
}

build() {
  local configure_options=(
    --prefix=/usr
    --with-ucx=/usr
    --with-cuda=/opt/cuda
    --with-rocm=/opt/rocm
    --with-rocm-arch=all-arch-no-native
    --enable-gtest
    CFLAGS="$CFLAGS"
    CXXFLAGS="$CXXFLAGS"
    LDFLAGS="$LDFLAGS"
    NVCC_CFLAGS="--threads 0"
    HIPCC="/opt/rocm/lib/llvm/bin/amdclang"
  )

  cd $_name-$pkgver
  ./autogen.sh
  ./configure "${configure_options[@]}"
  # prevent excessive overlinking due to libtool
  sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0/g' libtool
  make V=1
}

check() {
  # exclude test_mc_rocm.* - we cannot test ROCm without a GPU
  # exclude test_*reduce*:test_bcast_*:test_barrier.*:test_team.*:test_mc.*:test_active_set_2.*:test_scatter*:test_*gather*:*test_alltoall* - UCC ERROR no components supported memory type host available
  # exclude test_context.global due to https://github.com/openucx/ucc/issues/1090
  # exclude test_asymmetric_memory.* and test_asymmetric_memory_v.* and test_active_set.* due to https://github.com/openucx/ucc/issues/1132
  make gtest -C $_name-$pkgver GTEST_FILTER='-test_mc_rocm.*:test_*reduce*:test_bcast_*:test_barrier.*:test_team.*:test_mc.*:test_active_set_2.*:test_scatter*:test_*gather*:*test_alltoall*:test_context.global:test_asymmetric_memory.*:test_asymmetric_memory_v.*:test_active_set.*'
}

package() {
  make DESTDIR="$pkgdir" install -C $_name-$pkgver

  # install the license
  install -vDm 644 $_name-$pkgver/LICENSE -t "$pkgdir"/usr/share/licenses/$pkgname/

  # remove bundled gtest
  rm "$pkgdir"/usr/bin/gtest
}
