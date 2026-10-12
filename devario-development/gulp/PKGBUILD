# Maintainer: Felix Yan <felixonmars@archlinux.org>
# Contributor: Micha Alt <micha.tucker at gmail dot com>

pkgname=gulp
pkgver=5.0.1
pkgrel=1
pkgdesc="The streaming build system"
arch=('any')
url="https://gulpjs.com/"
license=('MIT')
depends=('nodejs' 'semver')
makedepends=('npm')
source=("https://registry.npmjs.org/$pkgname/-/$pkgname-$pkgver.tgz")
noextract=($pkgname-$pkgver.tgz)
sha512sums=('3c4ae89370d9480e5618c77a5d757721134ed26941fb05b73b384524b11e7358d21118368f56f127a7b9161e8de9f9f7147d93f403f851835bfe962500307db0')

package() {
  npm install -g --prefix "$pkgdir"/usr "$srcdir"/$pkgname-$pkgver.tgz

  mkdir -p "$pkgdir/usr/share/licenses/$pkgname"
  ln -s "../../../lib/node_modules/$pkgname/LICENSE" "$pkgdir/usr/share/licenses/$pkgname/"

  # Non-deterministic race in npm gives 777 permissions to random directories.
  # See https://github.com/npm/npm/issues/9359 for details.
  chmod -R u=rwX,go=rX "$pkgdir"

  # npm installs package.json owned by build user
  # https://bugs.archlinux.org/task/63396
  chown -R root:root "$pkgdir"

  # Experimental dedup
  cd "$pkgdir"/usr/lib/node_modules/$pkgname/node_modules
  for dep in semver; do
    rm -r $dep;
  done
}
