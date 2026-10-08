# Maintainer: Levente Polyak <anthraxx[at]archlinux[dot]org>
# Maintainer: Caleb Maclennan <caleb@alerque.com>
# Contributor: Fredy García <frealgagu at gmail dot com>
# Contributor: fuero <fuerob@gmail.com>

pkgname=lazygit
pkgver=0.66.0
pkgrel=1
pkgdesc='Simple terminal UI for git commands'
url='https://github.com/jesseduffield/lazygit'
arch=('x86_64')
license=('MIT')
depends=('git' 'glibc')
makedepends=('go')
source=("${url}/archive/v${pkgver}/${pkgname}-${pkgver}.tar.gz")
sha256sums=('704b14509dae4c0212754d60d1c00181aea79c0734aafa2c83c89301dba1aefd')
b2sums=('cec7c065d858ad1aa5ad2103898f8f43728f6f05bb550a3e3cf3254c0b6ebb72d1981ec86cab3b95c5ba9ef5a6e9a0c591de3c7f493110549a0db82c8c40c3a4')

build() {
  cd ${pkgname}-${pkgver}

  export CGO_CPPFLAGS="${CPPFLAGS}"
  export CGO_CFLAGS="${CFLAGS}"
  export CGO_CXXFLAGS="${CXXFLAGS}"
  export GOFLAGS="-buildmode=pie -trimpath -mod=readonly -modcacherw -x -v"

  go build \
    -ldflags "\
      -linkmode external \
      -extldflags '${LDFLAGS}' \
      -X main.date=$(date --date=@${SOURCE_DATE_EPOCH} -u +%Y-%m-%dT%H:%M:%SZ) \
      -X main.buildSource=binaryRelease \
      -X main.version=${pkgver} \
      -X main.commit=v${pkgver} \
    "
}

package() {
  cd ${pkgname}-${pkgver}
  install -Dm 755 lazygit -t "${pkgdir}/usr/bin"
  install -Dm 644 README*.md -t "${pkgdir}/usr/share/doc/${pkgname}"
  cp -r docs/* -t "${pkgdir}/usr/share/doc/${pkgname}"
  install -Dm 644 LICENSE -t "${pkgdir}/usr/share/licenses/${pkgname}"
}

# vim: ts=2 sw=2 et:
