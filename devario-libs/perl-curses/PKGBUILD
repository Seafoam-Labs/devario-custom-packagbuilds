# Maintainer: Sergej Pupykin <pupykin.s+arch@gmail.com>
# Maintainer: Charles Mauch <cmauch@gmail.com>
# Contributor: Francois Charette <firmicus@gmx.net>

pkgname=perl-curses
pkgver=1.46
pkgrel=2
pkgdesc="Character screen handling and windowing"
arch=('x86_64')
url="https://search.cpan.org/dist/Curses"
license=('GPL' 'PerlArtistic')
depends=('perl' 'ncurses')
options=('!emptydirs')
source=(https://search.cpan.org/CPAN/authors/id/G/GI/GIRAFFED/Curses-$pkgver.tar.gz)
sha512sums=('01d1ecde53838defea22725c2864d3afb236104da6eb98631b3342f86244f75b59a942163c2f2945dedea35f0c270435ee5054f489d0aa4ae75fe2fd8c6ed537')

build() {
  cd  "$srcdir"/Curses-$pkgver
  PERL_MM_USE_DEFAULT=1 perl Makefile.PL INSTALLDIRS=vendor
  make
}

package() {
  cd  "$srcdir"/Curses-$pkgver
  make pure_install doc_install DESTDIR="$pkgdir"
}
