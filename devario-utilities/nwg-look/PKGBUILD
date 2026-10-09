# Maintainer: Robin Candau <antiz@archlinux.org>
# Contributor: kpcyrd <kpcyrd[at]archlinux[dot]org>
# Contributor: Piotr Miller <nwg.piotr@gmail.com>

pkgname=nwg-look
pkgver=1.1.2
pkgrel=1
pkgdesc="GTK settings editor adapted to work on wlroots-based compositors"
url="https://github.com/nwg-piotr/nwg-look"
arch=('x86_64')
license=('MIT')
depends=('glibc' 'gtk3' 'at-spi2-core' 'cairo' 'fontconfig' 'freetype2' 'gdk-pixbuf2' 'glib2' 'harfbuzz' 'pango' 'zlib' 'xcur2png')
makedepends=('go')
source=("${url}/archive/v${pkgver}/${pkgname}-${pkgver}.tar.gz")
sha256sums=('2db9bf20042beec0e9e9bba5769c08e34197e3a0da595b743c39b384aa0e0af0')

build() {
	cd "${pkgname}-${pkgver}"
	go build \
		-trimpath \
		-buildmode=pie \
		-mod=readonly \
		-modcacherw \
		-ldflags "-linkmode external -extldflags \"${LDFLAGS}\"" \
		-o bin/nwg-look \
		.
}

package() {
	make DESTDIR="${pkgdir}" install -C "${pkgname}-${pkgver}"
}
