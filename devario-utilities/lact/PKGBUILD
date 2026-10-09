# Maintainer: Leonidas Spyropoulos <artafinde@archlinux.org>
# Contributor: Ilya Zlobintsev <ilya.zl@protonmail.com>

pkgname=('lact')
pkgbase=lact
pkgver=0.10.1
pkgrel=1
pkgdesc="Linux GPU Configuration Tool"
arch=('x86_64')
url="https://github.com/ilya-zlobintsev/LACT"
license=('MIT')
depends=(
  hwdata
  libdisplay-info
  libgcc
  libstdc++
  glibc
  gtk4
  libadwaita
  vulkan-tools
  ocl-icd
)
makedepends=(
  cargo
  clang
  git
)
checkdepends=(
  fuse3
)
install="$pkgbase.install"
source=("git+https://github.com/ilya-zlobintsev/LACT.git#tag=v$pkgver")
sha256sums=('0b46c49da3b54bc05992bbae0ef0c022da60485f411891b8d2f5e60c33ead07d')
b2sums=('05166815dfaf40c9cc170f6c431411454b65e94072520fb26a6953542bd3da1872907c8e341b017eb5d50702640d2411fd65b8224ab4c8cde2c46c1cbe0e6a86')

_backports=(
)

_reverts=(
)

prepare() {
  cd "LACT"
  local _c
  for _c in "${_backports[@]}"; do
    if [[ $_c == *..* ]]; then
      git log --oneline --reverse "${_c}"
    else
      git log --oneline -1 "${_c}"
    fi
    git cherry-pick -n -m1 "${_c}"
  done
  for _c in "${_reverts[@]}"; do
    git log --oneline -1 "${_c}"
    git revert -n "${_c}"
  done
  cargo fetch --locked --target "$(rustc --print host-tuple)"
}

build() {
  cd "LACT"
  CFLAGS+=' -ffat-lto-objects'

  cargo build -p "$pkgbase" --frozen --release
}

check() {
  cd "LACT"
  CFLAGS+=' -ffat-lto-objects'
  cargo test --frozen --workspace --verbose
}

package_lact() {
  provides=('lact-libadwaita')
  conflicts=('lact-libadwaita')
  replaces=('lact-libadwaita')

  cd "LACT"
  make PREFIX=/usr DESTDIR="$pkgdir/" install

  install -Dvm644 LICENSE -t "$pkgdir/usr/share/licenses/$pkgbase/"
}
