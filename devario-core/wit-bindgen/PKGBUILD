# Maintainer: Frederik Schwan <freswa at archlinux.org>
# Maintainer: Quentin Michaud <mh4ckt3mh4ckt1c4s@archlinux.org>

pkgname=wit-bindgen
pkgver=0.62.0
pkgrel=1
pkgdesc="A language binding generator for WebAssembly interface types "
url="https://github.com/bytecodealliance/wit-bindgen"
arch=('x86_64')
license=('Apache-2.0' 'MIT')
depends=(
  cargo
  glibc
  libgcc
)
makedepends=(
  git
)
options=(!lto)
source=("git+https://github.com/bytecodealliance/wit-bindgen.git#tag=v${pkgver}")
sha256sums=('a8edfcf134053c7d718ad6cb264d82dd533fc6702bb2f755ad022074c94daea4')
b2sums=('9780c2736c60c9a3c6e710481e2b42c4d64b9bf7d9b11bb1d8e4d1c05370bfb6aec0ee76c9f357b1ea7eeafea58b161a0274eb93bbf06ad07b8f1f6b237e2b75')

prepare() {
  cd ${pkgname}
  cargo fetch --locked --target "$(rustc --print host-tuple)"
}

build() {
  cd ${pkgname}
  cargo build --release --locked
}

check() {
  cd ${pkgname}
  cargo test --release --locked
}

package() {
  cd ${pkgname}
  install -Dm755 target/release/${pkgname} -t "${pkgdir}"/usr/bin
  install -Dm644 LICENSE-MIT -t "${pkgdir}"/usr/share/licenses/${pkgname}
}
