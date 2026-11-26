# Maintainer: Campbell Jones <serebit at archlinux dot org>
# Contributor: Sandy Carter <bwrsandman at gmail dot com>
# Contributor: Hans-Kristian Arntzen <post at arntzen-software dot no>
# Contributor: Joshua Ashton <joshua at froggi dot es>

pkgname=renderdoc
pkgver=1.47
pkgrel=1
pkgdesc="OpenGL and Vulkan debugging tool"
arch=(x86_64)
url="https://github.com/baldurk/renderdoc"
license=("MIT")
makedepends=("cmake" "git" "ninja" "pcre")
depends=("harfbuzz" "hicolor-icon-theme" "libgl" "libx11" "libxcb" "mesa" "python" "qt5-base" "qt5-svg" "qt5-x11extras" "xcb-util-keysyms")
options=("!lto")
source=("${pkgname}::git+https://github.com/baldurk/${pkgname}.git#tag=v${pkgver}?signed"
        "https://github.com/baldurk/swig/archive/${pkgname}-modified-7.zip")
validpgpkeys=('1B039DB9A4718A2D699DE031AC612C3120C34695')
b2sums=('72540ca0fae7c554989c2d4c3594855f71e455ef9fc9d286731723c846813bab64ba6a4875b5368c6a996af6c6789bae1cd393b075f79b24d80f8b5a2214c9b8'
        '136b0b48d5bddb2dfe6fffd54220a5b62bb9a725b800f1f7846d03469f0c859d0585a61118f64b2def81ad94ff650bdf82d1db7aeb7608a190792ce8033597dc')

build() {
    cd "$pkgname"

    cmake -G Ninja \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=/usr \
        -DBUILD_VERSION_STABLE=ON \
        -DBUILD_VERSION_DIST_CONTACT="https://archlinux.org/packages/$pkgname" \
        -DBUILD_VERSION_DIST_NAME="Arch" \
        -DBUILD_VERSION_DIST_VER="$pkgver" \
        -DRENDERDOC_SWIG_PACKAGE="$srcdir/${pkgname}-modified-7.zip" \
        -DVULKAN_LAYER_FOLDER="/etc/vulkan/implicit_layer.d" \
        -B build

    cmake --build build
}

package() {
    cd "$pkgname"

    DESTDIR="$pkgdir" cmake --install build
    install -Dm 0644 "LICENSE.md" "$pkgdir/usr/share/licenses/${pkgname}/LICENSE"
}
