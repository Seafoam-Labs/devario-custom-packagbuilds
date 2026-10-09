# Maintainer: Felix Yan <felixonmars@archlinux.org>
# Maintainer: Peter Jung <ptr1337@archlinux.org>

pkgname=mingw-w64-binutils
pkgver=2.47
pkgrel=1
pkgdesc="Cross binutils for the MinGW-w64 cross-compiler"
arch=('x86_64')
url="http://www.gnu.org/software/binutils"
license=(GPL-2.0-or-later GPL-3.0-or-later LGPL-2.0-or-later LGPL-3.0-or-later GFDL-1.3-only FSFAP)
groups=('mingw-w64-toolchain' 'mingw-w64')
depends=(
  glibc
  zlib
  zstd
)
options=('!libtool' '!emptydirs')
validpgpkeys=('3A24BC1E8FB409FA9F14371813FCEF89DD9E3C4F' # Nick Clifton (Chief Binutils Maintainer) <nickc@redhat.com>
              '5EF3A41171BB77E6110ED2D01F3D03348DB1A3E2') # Sam James <sam@cmpct.info>
source=("https://ftp.gnu.org/gnu/binutils/binutils-${pkgver}.tar.gz"{,.sig})
sha512sums=('0e86bcf998e4fa8fcdd1a4461899dd8efebfb57f6c15e31f6518a9b037d5e8c6b9a6be3fe28b4b1589c8c82e8611e01241dfef4b54543006a07a855cd8754a67'
            'SKIP')

_targets="i686-w64-mingw32 x86_64-w64-mingw32"

prepare() {
  cd "$srcdir"/binutils-${pkgver}
  #do not install libiberty
  sed -i 's/install_to_$(INSTALL_DEST) //' libiberty/Makefile.in
}

build() {
  for _target in $_targets; do
    echo "Building ${_target} cross binutils"
    mkdir -p "$srcdir"/binutils-${_target} && cd "${srcdir}/binutils-${_target}"
    "$srcdir"/binutils-${pkgver}/configure --prefix=/usr \
        --target=${_target} \
        --infodir=/usr/share/info/${_target} \
        --enable-lto --enable-plugins \
        --enable-deterministic-archives \
        --disable-multilib --disable-nls \
        --disable-werror
     make -O
  done
}

package() {
  for _target in ${_targets}; do
    echo "Installing ${_target} cross binutils"
    cd "$srcdir"/binutils-${_target}
    make DESTDIR="$pkgdir" install

    rm "$pkgdir"/usr/lib/bfd-plugins/libdep.so
  done
}
