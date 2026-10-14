# Maintainer: Caleb Maclennan <caleb@alerque.com>
# Maintainer: Orhun Parmaksız <orhun@archlinux.org>
# Contributor: Carl Smedstad <carl.smedstad at protonmail dot com>
# Contributor: George Rawlinson <grawlinson@archlinux.org>
# Contributor: Thomas <thomas at 6f dot io>

pkgname=jujutsu
_pkgname=jj
pkgver=0.46.0
pkgrel=1
pkgdesc='Git-compatible VCS that is both simple and powerful'
arch=(x86_64)
url="https://github.com/jj-vcs/$_pkgname"
license=(Apache-2.0)
depends=(glibc # libc.so libm.so ld-linux-x86-64.so
         git
         libgcc libgcc_s.so)
optdepends=('git: for push/clone/fetch actions when using git.subprocess = true')
makedepends=(cargo
             cargo-edit
             cmake) # builds vendored libz-ng
checkdepends=(git)
_archive="$_pkgname-$pkgver"
source=("$url/archive/refs/tags/v$pkgver/$_archive.tar.gz")
sha256sums=('6489f79d59dc4f9c11230c51d309dc9c6ec392921772b738546966c494b6d72c')

_srcenv() {
	cd "$_archive"
	export CARGO_HOME="$srcdir"
	export CARGO_PROFILE_RELEASE_DEBUG=2
	export CARGO_PROFILE_RELEASE_STRIP=false
	export CARGO_PROFILE_RELEASE_LTO=thin
	export CARGO_PROFILE_RELEASE_CODEGEN_UNITS=1
	export CARGO_PROFILE_RELEASE_OPT_LEVEL=3
	CFLAGS+=' -ffat-lto-objects'
}

prepare() {
	_srcenv
	cargo fetch --locked --target host-tuple
	mkdir -p completions manpages
}

build() {
	_srcenv
	cargo build --frozen --release --all-features --package jj-cli
	local jj=target/release/jj
	$jj util completion bash > completions/jj
	$jj util completion elvish > completions/jj.elv
	# https://gitlab.archlinux.org/archlinux/packaging/packages/jujutsu/-/issues/2
	# $jj util completion fish > completions/jj.fish
	$jj util completion zsh > completions/_jj
	$jj util install-man-pages manpages
}

check() {
	cd "$_archive"
	export useNextest=false
	local skipped=(
		test_diff_command # relies on config of external command
		test_acls::test_diff # relies on assumptions about tty
		test_converge_command::test_converge_description_changed_inconsistently::dont_invoke_text_editor
	)
	cargo test --frozen --all-features --package jj-cli -- ${skipped[@]/#/--skip }
}

package() {
	cd "$_archive"
	install -Dm0755 -t "$pkgdir/usr/bin" target/release/jj
	install -Dm0644 -t "$pkgdir/usr/share/bash-completion/completions/" completions/jj
	install -Dm0644 -t "$pkgdir/usr/share/elvish/lib/" completions/jj.elv
	# https://gitlab.archlinux.org/archlinux/packaging/packages/jujutsu/-/issues/2
	# install -Dm0644 -t "$pkgdir/usr/share/fish/vendor_completions.d/" completions/jj.fish
	install -Dm0644 -t "$pkgdir/usr/share/zsh/site-functions/" completions/_jj
	install -Dm0644 -t "$pkgdir/usr/share/man/man1/" manpages/man1/*
	install -Dm0644 -t "$pkgdir/usr/share/doc/$pkgname" ./*.md
	cp -at "$pkgdir/usr/share/doc/$pkgname" docs
	# Avoid namcap warning for dead symlink
	rm "$pkgdir/usr/share/doc/jujutsu/docs/cli-reference.md"
}
