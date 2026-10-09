# Maintainer: Alexander F. Rødseth <xyproto@archlinux.org>
# Contributor: Brad Fanella <cesura@archlinux.org>
# Contributor: Musikolo <musikolo@hotmail.com>
# Contributor: Ruben Fonseca <fonseka@gmail.com>
# Contributor: Andreas W. Hauser <andy-aur@splashground.de>
# Contributor: YongMing Zhang

pkgname=groovy
pkgver=6.0.0
pkgrel=1
pkgdesc='Programming language for the Java platform, inspired by Python, Ruby and Smalltalk'
arch=(any)
url='https://groovy-lang.org/'
license=(Apache-2.0)
depends=(java-environment)
makedepends=(gendesk)
optdepends=('groovy-docs: html and pdf documentation for Groovy')
validpgpkeys=('34441E504A937F43EB0DAEF96A65176A0FB1CD0B') # Paul King <paulk@apache.org>
source=("https://groovy.jfrog.io/artifactory/dist-release-local/groovy-zips/apache-$pkgname-binary-$pkgver.zip"
        "https://downloads.apache.org/groovy/$pkgver/distribution/apache-$pkgname-binary-$pkgver.zip.asc")
sha256sums=('54ab1a877f01da2ed16ed43c1ed7a8d6c36b122714c6959712700e89e6efde7c'
            'SKIP')
b2sums=('aa41dc71b15b0384d209d705a06eb397122df0f9e13a32c7c607e8dfbabb56674ddb1c1093341448a15f87879427ed36f6f83d0bdef43e50bdc32129b5ecf513'
        'SKIP')

prepare() {
  gendesk -f -n \
    --pkgname $pkgname \
    --pkgdesc 'Groovy programming language' \
    --exec groovyConsole \
    --name 'Groovy Console'

  # Modify environment variables in the included scripts
  for f in $pkgname-$pkgver/bin/*; do
    sed 's:bin/env\ sh:bin/env\ sh\nGROOVY_HOME=/usr/share/groovy\nexport _JAVA_OPTIONS="-Dawt.useSystemAAFontSettings=gasp $_JAVA_OPTIONS":' -i "$f"
  done
}

package() {
  cd $pkgname-$pkgver

  install -d "$pkgdir/usr/"{bin,share/groovy}
  cp bin/* "$pkgdir/usr/bin"
  cp -r lib conf "$pkgdir/usr/share/groovy"
  rm -v "$pkgdir"/usr/bin/*completion
  install -Dm644 "$srcdir/$pkgname.desktop" -t "$pkgdir"/usr/share/applications
  install -Dm644 bin/*completion -t "$pkgdir"/usr/share/bash-completion/completions
  install -Dm644 LICENSE -t "$pkgdir"/usr/share/licenses/$pkgname
  find "$pkgdir" -name '*.bat' -type f -exec rm -v {} \;
}
