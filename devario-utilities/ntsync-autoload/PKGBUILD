pkgname=ntsync-autoload
pkgver=1
pkgrel=1
pkgdesc='NTSync kernel module autoload'
url='https://www.archlinux.org'
arch=(any)
license=(0BSD)
depends=(
  NTSYNC-MODULE
)
source=(
  LICENSE
  ntsync.conf
)
sha512sums=('a33658d9271e5c537ccd41bf540b463ad2a5eca4a060c80486ff42a736f0aa042d10436e7177c34d792177cb11285243dee1f31c4df54fb0bfaabbc306406930'
            'ac2bd634838ffe6b90f2637e229013f0993fc1013271dbeefd216dc262a8bb79e4a5ce15a75cbfcb0c3b521d32f4ebe1ed25a6b066b99cc327b60bd6d7212e6f')

package() {
  install -Dm644 LICENSE -t "${pkgdir}/usr/share/licenses/${pkgname}"
  # Load NTSync module
  install -Dm644 ntsync.conf "${pkgdir}/usr/lib/modules-load.d/10-ntsync.conf"
}

# vim:set sw=2 sts=-1 et:
