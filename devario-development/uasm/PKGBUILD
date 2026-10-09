# Maintainer: George Rawlinson <grawlinson@archlinux.org>
# Contributor: Oleksandr Natalenko <oleksandr@natalenko.name>
# Contributor: Darren Ng <$(base64 --decode <<<VW4xR2ZuQGdtYWlsLmNvbQo=)>
# Contributor: Dan Bryant <$(base64 --decode <<<VanVzdGRhbjk2QGdtYWlsLmNvbQo=)>

pkgname=uasm
pkgver=2.57
pkgrel=3
pkgdesc='A MASM-compatible assembler'
arch=(x86_64)
url='http://www.terraspace.co.uk/uasm.html'
# Previous versions were licensed under the following licenses:
# - JWasm License
# - Sybase Open Watcom Public License 1.0
# Of which both are the same license with the following SPDX
# identifier: Watcom-1.0.
# The uasm-nocolor script uses code from stackoverflow, which
# is licensed under CC-BY-SA-3.0.
license=(
  Watcom-1.0
  CC-BY-SA-3.0
)
depends=(glibc sh sed)
makedepends=(git)
options=(!makeflags)
source=(
  "$pkgname::git+https://github.com/Terraspace/UASM#tag=v${pkgver}r"
  'uasm_extended_guide_v2.57.pdf::https://www.terraspace.co.uk/uasm257_ext.pdf'
  uasm-nocolor
  repro-date.patch
  add-missing-header.patch
  add-modern-ish-defines.patch
)
sha512sums=('8846942df358418217feb0941ef66de3064e5115fa5bbdaf70bac9ba2695606f910b58e9b5e3c933a530bda1e04d7cfd4d3616478b3d7ae12e74b6242d24a713'
            'e3b15a17d5ba753fe859fbff5cfda2c5c1d5209d9651e136d00989d41472e281023840b6dc2b0b96de554a659f5594f067c45d620f67296e60fd474a659b2c5d'
            '6099e122db071419e2158f37611726d6e2d9a73a0a6966320c8b7cd0621730df52078eaec70ab03358a40aece7b3312072370ba864cfd7f00f92c791ef98f0ca'
            '194f922ed137b679af2a4b86916cd0a9b613ad9c57617212b9dfe0900bd2f9726f59d4cde8e323de4ff573e5ff670ecb1321642fa69d61598e7266ae82579457'
            '9fd1fec9f37f8c5a28795789e9593f298930a1c86cc8376d43b33e81f5642bbe0d7912c44923e9c89f00675365e25eae6418352540ab7d2033639df602e8f9a8'
            'bab585595a223598bfa8703d83e5e4ac83d49d94acf68fdddb963021b47eec6ecce7ab30e3b0d1a498a010a3c9fbce38109aade1906083f5e9aa727bc2ed3573')
b2sums=('1be65d4e22a89f9a10e48ab24ac21eb4345ec96e68b9e002059a61572f02792ad80c87bbb4b3952ea7b5649b4e4cfb427b1723a48de82553c4c74b0e9ed78da3'
        'bf2e64b1bbddc6ba7f1cd2b88655168643f60e467f97eb28cd8b2083a7e623c9b801fc38bb7856f00b070057c024de8bf496cc2cf952f172ead20e44e66471d2'
        '29f03fede4f03363b106afe2a502c45b3ef8dcf5ae681f5e0f495908c83309f34b9f6fc663976814f03d3a73e4ca62762963caaa4c96a6c36b0c4ad806b1e1db'
        '385b460bed0ce2ba99bdbf545995bf30f43d993add687c27c58625d5bd18a2a1ef35f9076d8f0d79565b6702fca24f9247409b0df694e92bf76f84d55818de36'
        'f5ac24cb311109b43b0310e3ccbff0f3db8ac3965b0006ac6783e58c8f52f0ce5c54463f7d7014085aaad9a5c28cf45d043e61ee673f877da01680e1333be59f'
        '91bae50db6d95de62c87203df48ad373c75f3721e462e402584501c7faed3b6d70d8186d013e4e0d99007d38c2e28232cd1d17f71133e02f0d719d4051f78e69')

prepare() {
  cd "$pkgname"

  # build on newer GCC and Clang releases, silence compiler warnings
  # https://github.com/Terraspace/UASM/pull/216
  git cherry-pick --no-commit \
    ecb6d7c59755bd952e460c857b50c3155246898d \
    055e46a67298aa1b764dc8979e28cdddcb07cd15 \
    ecd4b944924d7d195194eb52b2cf6d127cda920d \
    16bf1d51b1fdc3a425e61f886140e151cb9b548f \
    e60a4a35ca03190638f6d091728ded1b3f741ffb \
    3946571dab2c4f0b596ff36abb230e4558498ae9 \
    98472b800a6733a565d530dd06f42576544827b4 \
    3dd005d7b4a26a8adce4980961661fd4196492ff \
    4057659ae7ab2f9db1f299b773476753db8a5c77 \
    33ae21341bd2c5d569b74813afa5cbf617f4eb5c \
    1b95cb75aa118f5af1b379e1d9f0eb152b0d7e0c

  # use git commit for date instead of __DATE__
  # note: if sed doesn't match, it fails silently,
  # hence the usage of patch
  patch -p1 -i "$srcdir/repro-date.patch"

  local COMMIT_DATE=$(git show --no-patch --format=%cd --date=format:"%b %d %Y")

  sed \
    -e "s/@COMMIT_DATE@/${COMMIT_DATE}/" \
    -i H/msgdef.h

  # ftbfs: missing header
  patch -p1 -i "$srcdir/add-missing-header.patch"

  # ftbfs: add correct-ish defines
  patch -p1 -i "$srcdir/add-modern-ish-defines.patch"
}

build() {
  cd "$pkgname"

  make -f Makefile-Linux.mak
}

package() {
  cd "$pkgname"

  # binary
  install -vDm755 -t "$pkgdir/usr/bin" GccUnixR/uasm "$srcdir/uasm-nocolor"

  # documentation
  install -vDm644 -t "$pkgdir/usr/share/doc/$pkgname" \
    {Readme,History}.txt \
    README.md \
    Doc/* \
    "$srcdir/uasm_extended_guide_v2.57.pdf"

  # license
  install -vDm644 -t "$pkgdir/usr/share/licenses/$pkgname" License.txt
}
