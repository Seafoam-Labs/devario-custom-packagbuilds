# Maintainer: Andreas Radke <andyrtr@archlinux.org>

_pkgbasename=libcups
pkgname=lib32-$_pkgbasename
pkgver=2.4.20
pkgrel=1
pkgdesc="The CUPS Printing System - client libraries (32-bit)"
arch=('x86_64')
license=('Apache-2.0 WITH LLVM-exception AND BSD-3-Clause AND Zlib AND BSD-2-Clause')
url="https://www.cups.org/"
depends=(lib32-zlib lib32-gnutls $_pkgbasename lib32-gcc-libs lib32-glibc)
source=(https://github.com/OpenPrinting/cups/releases/download/v${pkgver}/cups-${pkgver}-source.tar.gz{,.sig}
        cups-freebind.patch
        guid.patch
        fix-getdata-cups.2.4.20.patch
)
sha256sums=('ab4d9cd7f3e58060091d2b24972223d6401675f11c49b65abf4f6ef31dea22ff'
            'SKIP'
            '3385047b9ac8a7b13aeb8f0ca55d15f793ce7283516db0155fe28a67923c592d'
            '8becc2ad17787ef755fb77f83a87cf52f1a38154c5dde0f4a0051e06a0583fb9'
            '5d8952dbd2b0f89f28c095091827a0a64cebac2078fbe7fa39391f5472715493')
#validpgpkeys=('7ADB58203CA5F046F28025B215AA6A7F4D4227D7') # "Zdenek Dohnal (Associate Software Engineer) <zdohnal@redhat.com>"
validpgpkeys=('7082A0A50A2E92640F3880E0E4522DCC9B246FF7') # Zdenek Dohnal (The old 4D4227D7 key revoked) <zdohnal@redhat.com>
# validpgpkeys+=('9086C3CDC66C3F563CF8F405BE67C75EC81F3244') #  "Michael R Sweet <msweet@msweet.org>"

prepare(){
  cd cups-${pkgver} 
  # https://github.com/OpenPrinting/cups/issues/1739
  patch -Np1 -i ../fix-getdata-cups.2.4.20.patch

  patch -Np1 -i ../cups-freebind.patch
  patch -Np1 -i ../guid.patch
}


build() {
  export CC="gcc -m32"
  export CXX="g++ -m32"
  export PKG_CONFIG_PATH="/usr/lib32/pkgconfig"

  cd cups-${pkgver}

  aclocal -I config-scripts
  autoconf -I config-scripts

  # The build system uses only DSOFLAGS but not LDFLAGS to build some libraries.
  export DSOFLAGS=${LDFLAGS}

  ./configure --prefix=/usr \
     --sysconfdir=/etc \
     --localstatedir=/var \
     --libdir=/usr/lib32 \
     --enable-raw-printing \
     --disable-dbus \
     --with-tls=gnutls \
     --enable-libusb=no \
     --with-dnssd=no \
     --enable-relro \
     --with-optim="$CFLAGS" #--help
  make libs
}

package() {
  cd cups-${pkgver}
  make BUILDROOT="${pkgdir}" install-libs
  rm -rf "$pkgdir/usr/lib"

# add license + exception
  install -m644 -Dt "${pkgdir}/usr/share/licenses/${pkgname}" {LICENSE,NOTICE}
}
