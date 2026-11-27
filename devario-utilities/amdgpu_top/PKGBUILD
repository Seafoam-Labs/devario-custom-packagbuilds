# Maintainer: Sven-Hendrik Haase <svenstaro@archlinux.org>
# Contributor: Paul <pb.orzel@proton.me>
pkgname=amdgpu_top
pkgver=0.11.5
pkgrel=1
pkgdesc="Tool that shows AMD GPU utilization"
arch=('x86_64')
url="https://github.com/Umio-Yasuno/amdgpu_top"
license=("MIT")
depends=("glibc" "libgcc" "libdrm")
makedepends=("rust")
source=("$pkgname-$pkgver.tar.gz::https://github.com/Umio-Yasuno/amdgpu_top/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('e511ed15a6e0f3ea72321dfc97145ffb85999b37b6b304e9795978945f3f04cd')

prepare() {
	cd "$srcdir/$pkgname-$pkgver"
	export CARGO_TARGET_DIR=target
	cargo fetch --locked --target "$(rustc --print host-tuple)"
}

build() {
	cd "$srcdir/$pkgname-$pkgver"
	export CARGO_TARGET_DIR=target
	cargo build --frozen --release
}

package() {
	cd "$srcdir/$pkgname-$pkgver"
	install -Dm755 target/release/amdgpu_top "$pkgdir/usr/bin/amdgpu_top"
	install -Dm644 assets/amdgpu_top.desktop "$pkgdir/usr/share/applications/amdgpu_top.desktop"
  install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}
