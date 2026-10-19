# Maintainer: Orhun Parmaksız <orhun@archlinux.org>
# Contributor: Eric Long <i@hack3r.moe>

pkgname=bpf-linker
pkgver=0.11.0
pkgrel=2
pkgdesc="Simple BPF static linker"
arch=('x86_64')
url="https://github.com/aya-rs/bpf-linker"
license=('Apache-2.0' 'MIT')
depends=('glibc' 'libgcc' 'llvm-libs' 'clang')
makedepends=('cargo' 'llvm' 'lld')
source=("$pkgname-$pkgver.tar.gz::https://github.com/aya-rs/$pkgname/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('e32948056bd2604cdcc7fb384155feaf52f05512e02f4e8a7368af48e22f30f2')

prepare() {
  cd "$pkgname-$pkgver"
  cargo fetch --locked --target "$(rustc --print host-tuple)"
}

build() {
  cd "$pkgname-$pkgver"
  RUSTFLAGS+=" -C link-arg=-fuse-ld=lld" \
    cargo build --release --frozen
}

check() {
  cd "$pkgname-$pkgver"

  # skipping compile_test:
  # failed to build sysroot: "/usr/lib/rustlib/src/rust/library" does not seem to be a rust library
  # source folder: `src/Cargo.toml` not found
  RUSTFLAGS+=" -C link-arg=-fuse-ld=lld" \
    CARGO_MANIFEST_DIR="$PWD" cargo test --frozen \
    -- --skip compile_test --skip test_link_ir_files
}

package() {
  cd "$pkgname-$pkgver"
  install -Dm0755 -t "$pkgdir/usr/bin/" "target/release/$pkgname"
  install -Dm 644 README.md -t "$pkgdir/usr/share/doc/$pkgname"
  install -Dm 644 LICENSE-{APACHE,MIT} -t "$pkgdir/usr/share/licenses/$pkgname"
}

# vim: ts=2 sw=2 et:
