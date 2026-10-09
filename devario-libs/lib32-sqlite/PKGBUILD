# Maintainer: Laurent Carlier <lordheavym@archlinux.org>
# Contributor: Andreas Radke <andyrtr@archlinux.org>
# Contributor: Tom Newsom <Jeepster@gmx.co.uk>
# Contributor: Biru Ionut <ionut@archlinux.ro>
# Contributor: Mikko Seppälä <t-r-a-y@mbnet.fi>
# Contributor: Kaos < gianlucaatlas dot gmail dot com >

pkgname=('lib32-sqlite')
pkgver=3.53.4
_srcver=$(echo "$pkgver" | awk -F. '{ printf "%d%02d%02d00", $1, $2, $3 }')
pkgrel=1
pkgdesc="A C library that implements an SQL database engine (32-bit)"
arch=('x86_64')
license=('LicenseRef-Sqlite')
url="https://www.sqlite.org/"
makedepends=('tcl' 'lib32-readline' 'sqlite')
options=('!emptydirs')
source=(https://www.sqlite.org/2026/sqlite-src-${_srcver}.zip
        license.txt)
# upstream now switched to sha3sums - currently not supported by makepkg
sha256sums=('d18fa15aec74d8c17e1463f861095adc01b5ad190256acb4f91d22f0368d232b'
            '4e57d9ac979f1c9872e69799c2597eeef4c6ce7224f3ede0bf9dc8d217b1e65d')

prepare() {
  cd sqlite-src-$_srcver

  #autoreconf -vfi
}

build() {
  # this uses malloc_usable_size, which is incompatible with fortification level 3
  export CFLAGS="${CFLAGS/_FORTIFY_SOURCE=3/_FORTIFY_SOURCE=2}"
  export CXXFLAGS="${CXXFLAGS/_FORTIFY_SOURCE=3/_FORTIFY_SOURCE=2}"

  export CPPFLAGS="$CPPFLAGS \
        -DSQLITE_ENABLE_COLUMN_METADATA=1 \
        -DSQLITE_ENABLE_UNLOCK_NOTIFY \
        -DSQLITE_ENABLE_DBSTAT_VTAB=1 \
        -DSQLITE_ENABLE_FTS3_PARENTHESIS \
        -DSQLITE_SECURE_DELETE \
        -DSQLITE_ENABLE_STMTVTAB \
        -DSQLITE_ENABLE_STAT4 \
        -DSQLITE_MAX_VARIABLE_NUMBER=250000 \
        -DSQLITE_MAX_EXPR_DEPTH=10000 \
        -DSQLITE_ENABLE_MATH_FUNCTIONS"
        
  # build sqlite
  cd sqlite-src-$_srcver

  export CC="gcc -m32"
  export CXX="g++ -m32"
  export PKG_CONFIG="i686-pc-linux-gnu-pkg-config"

  ./configure --prefix=/usr \
	--libdir=/usr/lib32 \
	--disable-static \
    --enable-session \
    --enable-fts3 \
	--fts4 \
	--fts5 \
	--rtree \
	--disable-tcl \
	--soname=legacy
	TCLLIBDIR=/usr/lib/sqlite$pkgver
  sed -i -e 's/$(LDFLAGS.libsqlite3)/ -Wl,-O1,--as-needed \0/g' main.mk
  make
}

package_lib32-sqlite() {

 pkgdesc="A C library that implements an SQL database engine (32-bit)"
 depends=('lib32-glibc' 'lib32-gcc-libs' 'sqlite')
 provides=('libsqlite3.so')

  cd sqlite-src-$_srcver
  make DESTDIR="${pkgdir}" install

  rm -r "${pkgdir}"/usr/{bin,include,share/man}

  # license
  install -D -m644 "${srcdir}"/license.txt "${pkgdir}"/usr/share/licenses/${pkgname}/license.txt
}
