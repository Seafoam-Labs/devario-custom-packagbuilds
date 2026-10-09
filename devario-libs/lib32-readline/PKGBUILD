# Maintainer: Giancarlo Razzolini <grazzolini@archlinux.org>
# Contributor: Allan McRae <allan@archlinux.org>
# Contributor: judd <jvinet@zeroflux.org>

_pkgbasename=readline
pkgname=lib32-$_pkgbasename
pkgver=8.3.3
_patchlevel=${pkgver#*.*.}
[[ $_patchlevel == "$pkgver" ]] && _patchlevel=0
_basever=${pkgver%"${_patchlevel:+.$_patchlevel}"}
pkgrel=1
pkgdesc="GNU readline library (32-bit)"
arch=(x86_64)
url="https://tiswww.case.edu/php/chet/readline/rltop.html"
license=('GPL-3.0-or-later')
depends=('lib32-glibc' 'lib32-ncurses' $_pkgbasename)
makedepends=('gcc-multilib')
source=(
  https://ftp.gnu.org/gnu/readline/readline-$_basever.tar.gz{,.sig}
  # INFO: point patches are extended automatically into the source array
)
b2sums=('45d6fe7e34c56d309102a94aa776a7f5284201e844450e14ff818df9fa84a72154bdca70f11828c94954b080cbbe4666fa0b00ffa8460118ec8f3ea551b73dad'
        'SKIP'
        'b0953458a18b8b06b0086567abd3c9ca3efceb5e4c38271e62137e126c106b938945d956394de0e955ecea5d48f8b261a4f2f3db2ee1d2cbc3b4cfdcf213ca46'
        'SKIP'
        'bb07c3e1663b36988e59721d8e8054022726f6adc2160cbb1fe30bcb5fe96d70fc38980a84c05a0518b9916975ffa1c4c97542fc9c82845736c6f6d03ca60229'
        'SKIP'
        '39f48eefef1840460aa418a070813dd284893e74dddad5fb44230498a7991148e9681be89b30e98fe805a67b3093360c883a16a26a7f103548f36c899f9359da'
        'SKIP')
validpgpkeys=('7C0135FB088AAF6C66C650B9BB5869F064EA74AB') # Chet Ramey

# extend patches to source array
if (( _patchlevel > 0 )); then
    for (( _p=1; _p <= $((10#${_patchlevel})); _p++ )); do
        source=(${source[@]} https://ftp.gnu.org/gnu/readline/readline-$_basever-patches/readline${_basever//.}-$(printf "%03d" $_p){,.sig})
    done
fi

prepare() {
  cd ${_pkgbasename}-$_basever
  for (( _p=1; _p <= $((10#${_patchlevel})); _p++ )); do
    msg2 "applying patch readline${_basever//.}-$(printf "%03d" $_p)"
    patch -p0 -i ../readline${_basever//.}-$(printf "%03d" $_p)
  done

  # remove RPATH from shared objects (FS#14366)
  sed -i 's|-Wl,-rpath,$(libdir) ||g' support/shobj-conf
}

build() {
  cd ${_pkgbasename}-$_basever

  export CC="gcc -m32"
  export CXX="g++ -m32"
  export PKG_CONFIG_PATH="/usr/lib32/pkgconfig"

  # build with -fPIC for x86_64 (FS#15634)
  [[ $CARCH == x86_64* ]] && CFLAGS="$CFLAGS -fPIC"

  ./configure --prefix=/usr --libdir=/usr/lib32
  make SHLIB_LIBS=-lncurses
}

package() {
  cd ${_pkgbasename}-$_basever

  make DESTDIR="${pkgdir}" install
  rm -rf "${pkgdir}"/usr/{include,share,bin}
}
