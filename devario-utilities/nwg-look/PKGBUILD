# Maintainer: Robin Candau <antiz@archlinux.org>
# Contributor: kpcyrd <kpcyrd[at]archlinux[dot]org>
# Contributor: Piotr Miller <nwg.piotr@gmail.com>

pkgname=nwg-look
pkgver=1.2.1
pkgrel=1
pkgdesc="GTK settings editor adapted to work on wlroots-based compositors"
url="https://github.com/nwg-piotr/nwg-look"
arch=('x86_64')
license=('MIT')
depends=('glibc' 'gtk3' 'at-spi2-core' 'cairo' 'fontconfig' 'freetype2' 'gdk-pixbuf2' 'glib2' 'harfbuzz' 'pango' 'zlib' 'xcur2png')
makedepends=('go')
optdepends=("libcanberra: for GTK sound themes support")
source=("${url}/archive/v${pkgver}/${pkgname}-${pkgver}.tar.gz")
sha256sums=('1c66053f559f1756b18b615987a450433117c6b6c08759debdef94b6fd906480')

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
