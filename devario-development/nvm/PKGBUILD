# Maintainer: Carl Smedstad <carsme@archlinux.org>
# Contributor: Tom Wadley <tom@tomwadley.net>

pkgname=nvm
pkgver=0.40.8
pkgrel=1
pkgdesc="Node Version Manager - Simple bash script to manage multiple active node.js versions"
arch=('any')
url="https://github.com/nvm-sh/nvm"
license=('MIT')
makedepends=('git')
checkdepends=(
  'bash'
  'npm'
)
install="$pkgname.install"
source=(
  "git+$url.git#tag=v$pkgver"
  "init-nvm.sh"
)
b2sums=('fb103dc889b255eb8a03479eff93ed44c9498abb32ede657c219cd75d2a297de8b4fb96a1dcc3cfadf3c55971bf6e3335b3e8607432feca58de0dd71deb81249'
        'd541d4a3411b665ad19e80fce02bc44e19b389a67959944451da4fb3e0a3e10bee0052f0f2ece2a67e4908333a26d23664bef995ef929bdcf44ffa77eff052aa')

prepare() {
  cd $pkgname
  # Requires sudo and/or Docker, skip.
  rm -v "test/fast/Running 'nvm uninstall' with incorrect file permissions fails nicely"
  rm -v "test/fast/Unit tests/nvm_download"
  rm -v "test/fast/Unit tests/nvm_get_arch"
  rm -v "test/fast/Unit tests/nvm_get_arch_unofficial"
  # Requires submodule, skip.
  rm -v "test/fast/Unit tests/nvm_process_nvmrc"
  # Fails in a chroot for some reason.
  rm -v "test/fast/Listing versions/Running 'nvm ls' should not show a trailing slash"
  rm -v "test/fast/Set Colors/nvm_print_versions calls nvm_get_colors"
  rm -v "test/fast/Unit tests/nvm ls-remote"
}

check() {
  cd $pkgname
  npm install
  node_modules/.bin/urchin  -f -s bash test/fast
}

package() {
  cd $pkgname
  install -vDm644 -t "$pkgdir/usr/share/$pkgname" nvm.sh
  install -vDm755 -t "$pkgdir/usr/share/$pkgname" nvm-exec
  install -vDm644 -t "$pkgdir/usr/share/$pkgname" bash_completion
  install -vDm644 -t "$pkgdir/usr/share/licenses/$pkgname" LICENSE.md

  # Convenience script
  install -vDm644 -t "$pkgdir/usr/share/$pkgname" "$srcdir/init-nvm.sh"
}
