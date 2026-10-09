# Maintainer: Johannes Löthberg <johannes@kyriasis.com>
# Maintainer: George Rawlinson <grawlinson@archlinux.org>
# Contributor: Sergej Pupykin <pupykin.s+arch@gmail.com>
# Contributor:  hydro <hydro@freenet.de>

pkgname=libmediainfo
pkgver=26.10
pkgrel=1
pkgdesc='Shared library for MediaInfo'
arch=(x86_64)
url='https://mediaarea.net'
license=(BSD-2-Clause)
depends=(
  glibc
  curl
  glib2
  libmms
  libzen
  libgcc
  libstdc++
  tinyxml2
  graphviz
  zlib
)
source=("$pkgname-$pkgver.tar.xz::https://mediaarea.net/download/source/libmediainfo/$pkgver/libmediainfo_$pkgver.tar.xz")
sha512sums=('5b155195d92c098c05ea7e9bd5af884350186367297535a3d533a6657bb7a1f0a307d585a10e92caaca0a0d16815c90525b9bb9de9bfc373d44f89cad7ee8c6a')
b2sums=('5f1d92f4fe4de60bf3e0eb21f2b3bc73ecd4e75856ece7df0b864df3779c9e5301730794d849a603799b69a1e486ecf343d8670505529e0c35507a78dda40983')

build() {
  cd MediaInfoLib/Project/GNU/Library

  ./autogen.sh

  ./configure \
    --prefix=/usr \
    --enable-shared \
    --disable-static \
    --with-libcurl \
    --with-libmms \
    --with-libtinyxml2 \
    --with-graphviz

  make
}

package() {
  cd MediaInfoLib/Project/GNU/Library

  make DESTDIR="$pkgdir" install

  # license
  install -vDm644 -t "$pkgdir/usr/share/licenses/$pkgname" "$srcdir/MediaInfoLib/LICENSE"
}
