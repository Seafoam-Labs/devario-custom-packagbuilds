# Maintainer: Juergen Hoetzel <juergen@archlinux.org>
# Maintainer: George Rawlinson <grawlinson@archlinux.org>
# Maintainer: Carl Smedstad <carsme@archlinux.org>

pkgname=clisp
pkgver=2.49.95
pkgrel=3
pkgdesc="ANSI Common Lisp interpreter, compiler and debugger"
arch=('x86_64')
url="https://clisp.sourceforge.io/"
license=('GPL-2.0-only')
depends=(
  'ffcall'
  'glibc'
  'libsigsegv'
  'libunistring'
  'ncurses'
  'readline'
)
makedepends=('git')
provides=('common-lisp')
options=(
  '!emptydirs'
  '!makeflags'
)
_rev=afa64df1c2bd92175159e8065117ec7286c65522
source=(
  "$pkgname::git+https://gitlab.com/gnu-clisp/clisp#commit=$_rev"
  "$pkgname-fix-build-with-gcc-15.1.patch"
)
sha512sums=('c93e403b768e5d6e842a86835da8ccd905cc2d5461671b7b0a47def0d0a96c91cffc9c0344eef75a999f4cbddf12f191f1c42f410ebf09277d7e338dc8ffa3d6'
            '4d97d2c9d19dcf1ec58fb924e1751814ffed8231bc28a859e1bd01edc9907a5264ee6d2e37f8460db7af1b216db7b8fe4fd349aa941dd9e3a0decc127d70cecd')
b2sums=('5a9ed2744db2efebbc63218b6f51ddff7087c985a97f8720d8ec66ba771e86e4c887a9955ce20b9226706ce73b12b45cd3e9d184b33fb282e8ba04e0dab76957'
        '81241db406cf00b5c219ded3067b3734d8dc2a3e13c2604f3b87e34fd863bd5fefe3e2b3aac77f1a400a3ca58d529e8e9ac08a815d22794dd37c05f5a3fc7365')

prepare() {
  cd $pkgname
  # Fix build with GCC 15.1
  patch -Np1 -i ../$pkgname-fix-build-with-gcc-15.1.patch
}

build() {
  cd $pkgname
  CFLAGS+=" -ffat-lto-objects" \
  ./configure --prefix=/usr --with-readline --with-ffcall --with-threads=POSIX_THREADS src

  cd src
  ./makemake --prefix=/usr --with-readline --with-ffcall --with-dynamic-ffi > Makefile
  make
}

check() {
  cd $pkgname
  make check
}

package() {
  cd $pkgname/src
  make DESTDIR="$pkgdir" install
}
