# Maintainer: David Runge <dvzrv@archlinux.org>
# Contributor: Ray Rashif <schiv@archlinux.org>
# Contributor: Limao Luo <luolimao+AUR@gmail.com>
# Contributor: Sebastien Luttringer <seblu+arch@seblu.net>
# Contributor: Jochen Immendœrfer <jochen.immendoerfer@gmail.com>

pkgname=alsa-tools
pkgver=1.2.15
pkgrel=3
pkgdesc="Advanced tools for certain sound cards"
arch=(x86_64)
url="https://alsa-project.org/"
license=(GPL-2.0-or-later)
depends=(
  glibc
  hicolor-icon-theme
  libgcc_s.so
  libstdc++.so
)
makedepends=(
  alsa-lib
  fltk1.3
  gtk3
  gtk4
)
optdepends=(
  'fltk1.3: for hdspconf, hdspmixer'
  'gtk3: for hdajackretask and hwmixvolume'
  'gtk4: for envy24control'
  'python-pyalsa: for hwmixvolume'
  'python-gobject: for hwmixvolume'
)
provides=($pkgname-emu10k1 $pkgname-ice1712 liblo10k1.so)
source=(
  $url/files/pub/tools/$pkgname-$pkgver.tar.bz2{,.sig}
  $pkgname-1.2.15-use-fltk1.3.patch
)
sha512sums=('b2354fcaccfa316df7847438ad6b4ca3702be4ca88c46878c198a52ca6c659263b61759d4898e7a73acf64dd0e3004c103fa67a1cbdb2e53212f13368173be23'
            'SKIP'
            'c757722e7d44999aa5d0f2cd6110e913acc5acecf512b0fc63decc7b7277bf49cc3f9696514a6a53ae0681eeac92ab29abd07eb6771d8391a8ecaf593aeec7e7')
b2sums=('c7790391233546fe6faf5e0bbb58d8067bb71137da25a9d3f02c07dc4abcdd78d361fd9b9a43e8d75a3328a364a4916b64c16d2972718b8bcf9c6d1a4b717882'
        'SKIP'
        '2fa8e7ef4dc34f241f1136becfdfe3bec7d19284b674c67481f9c51ba971cf6ba3ff78e4b3496564f3797a750ebff556911ef04d73ad01f37457ea43ac2e5380')
validpgpkeys=('F04DF50737AC1A884C4B3D718380596DA6E59C91') # ALSA Release Team (Package Signing Key v1) <release@alsa-project.org>

_tools=(
  as10k1
  envy24control
  hda-verb
  hdajackretask
  hdajacksensetest
  hdspconf
  hdsploader
  hdspmixer
  hwmixvolume
  ld10k1
  mixartloader
  pcxhrloader
  # qlo10k1  # disabled, because build is broken
  sb16_csp
  seq/sbiload
  sscape_ctl
  vxloader
  us428control
  usx2yloader
)

prepare() {
  # use fltk1.3, because at the very least the hdspmixer is broken with fltk 1.4
  # https://gitlab.archlinux.org/archlinux/packaging/packages/fltk/-/issues/7
  patch -Np1 -d $pkgname-$pkgver -i ../$pkgname-1.2.15-use-fltk1.3.patch

  for tool in "${_tools[@]}"; do
    (
      cd $pkgname-$pkgver/$tool
      autoreconf -vfi
    )
  done
}

build() {
  # not using upstream's global makefile as it's trying to be too clever
  for tool in "${_tools[@]}"; do
    (
      cd $pkgname-$pkgver/$tool
      ./configure --prefix=/usr --sbindir=/usr/bin
      make
    )
  done
}

package() {
  depends+=(
    alsa-lib libasound.so
  )

  for tool in "${_tools[@]}"; do
    make DESTDIR="$pkgdir" install -C $pkgname-$pkgver/$tool
  done
}

# vim:set ts=2 sw=2 et:
