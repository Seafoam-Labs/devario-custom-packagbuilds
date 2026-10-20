# Maintainer: Sergej Pupykin <pupykin.s+arch@gmail.com>
#Contributor: Pete Morris <pete dot morris at gmail dot com>
pkgname=perl-crypt-des
pkgver=2.09
pkgrel=2
pkgdesc="Perl DES encryption module"
arch=('x86_64')
url="https://search.cpan.org/~dparis/Crypt-DES"
license=("GPL" "PerlArtistic")
depends=('glibc')
source=("https://www.cpan.org/authors/id/T/TI/TIMLEGGE/Crypt-DES-$pkgver.tar.gz")
sha256sums=('149cdc0a14e944b4cc5eefb7560c78d8cb25254f9f9774547c880355a7e9f40c')

build() {
  cd "$srcdir"/Crypt-DES-$pkgver
  PERL_MM_USE_DEFAULT=1 perl Makefile.PL INSTALLDIRS=vendor
  sed -E 's|(^OPTIMIZE.*)|\1 -Wno-implicit-function-declaration|' -i Makefile
  make
}

package() {
  cd "$srcdir"/Crypt-DES-$pkgver
  make pure_install doc_install DESTDIR="$pkgdir"
}
