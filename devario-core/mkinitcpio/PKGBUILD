# Maintainer: Giancarlo Razzolini <grazzolini@archlinux.org>
# Maintainer: Lukas Fleischer <lfleischer@archlinux.org>
# Contributor: Morten Linderud <foxboron@archlinux.org>
# Contributor: Dave Reisner <dreisner@archlinux.org>
# Contributor: Thomas Bächler <thomas@archlinux.org>

pkgname=mkinitcpio
pkgver=42.2
pkgrel=1
pkgdesc="Modular initramfs image creation utility"
arch=('any')
url='https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio'
license=('GPL-2.0-only')
depends=('awk' 'mkinitcpio-busybox' 'kmod' 'util-linux' 'libarchive' 'coreutils'
         'bash' 'binutils' 'diffutils' 'findutils' 'grep' 'gzip' 'filesystem' 'zstd' 'systemd')
checkdepends=('bats' 'bats-assert' 'lzop')
makedepends=('asciidoctor' 'git' 'meson')
optdepends=('xz: Use lzma or xz compression for the initramfs image'
            'bzip2: Use bzip2 compression for the initramfs image'
            'lzop: Use lzo compression for the initramfs image'
            'lz4: Use lz4 compression for the initramfs image'
            'mkinitcpio-nfs-utils: Support for root filesystem on NFS'
            'systemd-ukify: alternative UKI generator')
provides=('initramfs')
backup=('etc/mkinitcpio.conf')
source=("git+$url.git#tag=v${pkgver}?signed")
sha512sums=('ddc6cb65586ea690ebdcf04f12eb0b441306efc900fb3045816512ec43b25cdec484d72cb1cbb928911a14ffd8637b14a2b7d0706232dd58797a3a07b0d40fc2')
b2sums=('b2fb0987878f13a26ebae0c2b4a75b15f52d3f1f8d5eb46ba7e8114629889070472232a4cb5cb259a3fae0c1658ac2d049f17933bbaa6bab9fdd31cd8af18640')
validpgpkeys=('ECCAC84C1BA08A6CC8E63FBBF22FB1D78A77AEAB'    # Giancarlo Razzolini
              'BB8E6F1B81CF0BB301D74D1CBF425A01E68B38EF')   # nl6720

build(){
	arch-meson -Dsystemd_hooks=true "$pkgname" build
	meson compile -C build
}

check() {
	meson test -C build
}

package() {
	meson install -C build --destdir "$pkgdir"
}
