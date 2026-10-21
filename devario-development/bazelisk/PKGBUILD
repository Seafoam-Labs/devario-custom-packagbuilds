# Maintainer: Christian Heusel <gromit@archlinux.org>

pkgname=bazelisk
pkgver=1.30.0
pkgrel=1
pkgdesc='A user-friendly launcher for Bazel.'
arch=('x86_64')
url="https://github.com/bazelbuild/bazelisk"
license=('Apache-2.0')
makedepends=(
    'go'
    'git'
)
depends=(
    'glibc'
)
provides=('bazel')
conflicts=('bazel')
source=("git+https://github.com/bazelbuild/bazelisk#tag=v$pkgver")
sha256sums=('b29e109091b8c8e4a603726fb1e129ccbbea1ae070e73f42cb8afc278e5ed558')
options=(!lto)

prepare(){
  cd "$pkgname"

  mkdir -p build/
}

build() {
  cd "$pkgname"
  export CGO_CPPFLAGS="${CPPFLAGS}"
  export CGO_CFLAGS="${CFLAGS}"
  export CGO_CXXFLAGS="${CXXFLAGS}"
  export CGO_LDFLAGS="${LDFLAGS}"
  export GOFLAGS="-buildmode=pie -trimpath -ldflags=-linkmode=external -mod=readonly -modcacherw"
  go build -o build .
}

package() {
  cd "$pkgname"
  install -Dm755 build/$pkgname "$pkgdir"/usr/bin/$pkgname
  ln -s /usr/bin/bazelisk $pkgdir/usr/bin/bazel
}
