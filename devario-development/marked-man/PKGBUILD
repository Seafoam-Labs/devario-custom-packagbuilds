# Maintainer: Felix Yan <felixonmars@archlinux.org>

pkgname=marked-man
pkgver=2.1.1
pkgrel=1
pkgdesc="Wrapper adding manpage output to 'marked', inspired by 'ronn'"
arch=('any')
url='https://github.com/kapouer/marked-man'
license=('MIT')
depends=('marked' 'nodejs')
makedepends=('npm')
source=(https://registry.npmjs.org/$pkgname/-/$pkgname-$pkgver.tgz)
noextract=($pkgname-$pkgver.tgz)
sha512sums=('1a7032cb295c7b164b3c028239ac7c8bf609b40cad711126c78f3963e25805519dce4097cf1d680c8a92537bcfcd1712128c2cc6e1151ad0f24ff83682e552c8')

package() {
  npm install -g --prefix "$pkgdir"/usr "$srcdir"/$pkgname-$pkgver.tgz

  # Experimental dedup
  rm -r "$pkgdir"/usr/lib/node_modules/$pkgname/node_modules/{,.bin/}marked

  # Non-deterministic race in npm gives 777 permissions to random directories.
  # See https://github.com/npm/npm/issues/9359 for details.
  chmod -R u=rwX,go=rX "$pkgdir"

  # npm installs package.json owned by build user
  # https://bugs.archlinux.org/task/63396
  chown -R root:root "$pkgdir"

  install -d "$pkgdir"/usr/share/licenses/$pkgname
  ln -s ../../../lib/node_modules/marked-man/LICENSE "$pkgdir"/usr/share/licenses/$pkgname/LICENSE
}
