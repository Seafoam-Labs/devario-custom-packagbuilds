# Maintainer: Quentin Michaud <mh4ckt3mh4ckt1c4s@archlinux.org>

pkgname=wasm-tools
pkgver=1.258.0
pkgrel=1
pkgdesc="Low level tooling for WebAssembly in Rust"
arch=("x86_64")
url="https://github.com/bytecodealliance/wasm-tools"
license=("Apache-2.0")
depends=(
  "glibc"
  "libgcc"
)
# Update using ./retrieve-testsuite-commit.sh <pkgver>
_wasm_testsuite_commit=51279a9d02cbba193cb25142d115388d7b83299c
makedepends=("cargo")
source=(
	"$pkgname-$pkgver.tar.gz::https://github.com/bytecodealliance/$pkgname/archive/refs/tags/v$pkgver.tar.gz"
	"wasm-testsuite-$_wasm_testsuite_commit.tar.gz::https://github.com/WebAssembly/testsuite/archive/$_wasm_testsuite_commit.tar.gz"
)
sha256sums=('14a867a7f5ae233f27c6ad93c2ce6153afa43bf93b0a60450b8ba789d65f8ce4'
            '1b3caa3fab5259b1e1cda8c66d14ee8c81f5e0dc6322f518964c0c6f6590d945')

options_aarch64=(!lto)

prepare() {
    cd "$pkgname-$pkgver"
    rm -r tests/testsuite
    cp -r "$srcdir/testsuite-$_wasm_testsuite_commit" tests/testsuite
    cargo fetch --locked --target "$(rustc --print host-tuple)"
}

build() {
    cd "$pkgname-$pkgver"
    cargo build --frozen --release --all-features --bin wasm-tools
}

check() {
    cd "$pkgname-$pkgver"
    cargo test --frozen
}

package() {
    cd "$pkgname-$pkgver"
    install -Dm0755 -t "$pkgdir/usr/bin/" "target/release/$pkgname"
}
