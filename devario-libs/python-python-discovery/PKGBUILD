# Maintainer: George Rawlinson <grawlinson@archlinux.org>

pkgname=python-python-discovery
pkgver=1.6.1
pkgrel=1
pkgdesc='Python interpreter discovery'
arch=(any)
url='https://python-discovery.readthedocs.io'
license=(MIT)
depends=(
  python
  python-filelock
)
makedepends=(
  git
  python-build
  python-installer
  python-hatchling
  python-hatch-vcs
)
checkdepends=(
  python-pytest
  python-pytest-mock
  python-setuptools
)
source=(
  "$pkgname::git+https://github.com/tox-dev/python-discovery#tag=$pkgver"
  no-vermin.patch
)
sha512sums=('e1a81d245455a6d54cc7d87ae9d1a88b8062495a9efd3d0e676cd239ff35a703b801568fe0025baf803f2a144ee9b936b0171793f86a48af2ea2f2eb812982ef'
            'c9057e2e74dde6819b2f43cf6f29c6f0903da9f12784fc1e84fc24b972a8d114fb55c60630f65106cee1e2c02e043ddfff08f5729c98d3e35a32c0b83ec184cd')
b2sums=('8f708cfd4204aaa3cff0c0089e5acf4496bab456c88204f223365fff4d1ae69251a0f4ebef81366c2acdc62962210a0219c2eb9fb0106ae47076c4876b2ec131'
        'e23fac44ff0fe6dc0eb4f19da9bef5410c0e4d03b2992d2f79eba45a4b69c81173c11feb13e84d8d440938b67aa65f3ada6fe6583f627f828a83fa70863ec507')

prepare() {
  cd "$pkgname"

  # we don't want to detect old python versions
  patch -p1 -i "$srcdir/no-vermin.patch"
}

build() {
  cd "$pkgname"

  SETUPTOOLS_SCM_PRETEND_VERSION="$pkgver" python -m build --wheel --no-isolation
}

check() {
  cd "$pkgname"

  # temporary install
  python -m installer --destdir="$(pwd)/tmp" dist/*.whl
  local site_packages=$(python -c "import site; print(site.getsitepackages()[0])")
  export PYTHONPATH="$(pwd)/tmp/$site_packages"

  pytest -v
}

package() {
  cd "$pkgname"

  python -m installer --destdir="$pkgdir" dist/*.whl

  # license
  install -vDm644 -t "$pkgdir/usr/share/licenses/$pkgname" LICENSE
}
