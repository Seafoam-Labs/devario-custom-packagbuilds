# Maintainer: Torsten Keßler <tpkessler at archlinux dot org>
# Maintainer: Christian Heusel <gromit@archlinux.org>
# Contributor: acxz <akashpatel2008 at yahoo dot com>

pkgbase=rocm-llvm
pkgname=(rocm-llvm rocm-llvm-libs rocm-mlir-libs rocm-llvm-tools rocm-llvm-headers
         rocm-llvm-static rocm-flang rocm-device-libs comgr)
epoch=2
pkgver=7.2.4
pkgrel=3
arch=('x86_64')
url='https://rocm.docs.amd.com/en/latest/reference/rocmcc.html'
makedepends=('git' 'cmake' 'python' 'ninja' 'rocm-core' 'rocm-cmake' 'perl'
             'gcc-libs' 'zlib' 'zstd' 'libffi' 'libedit' 'ncurses' 'libxml2' 'patchelf')
source=("$pkgbase::git+https://github.com/ROCm/llvm-project#tag=rocm-$pkgver"
        '0001-compiler-rt-sanitizer-Remove-linux-scc.h.patch')
sha256sums=('cda215d04dfb6ede38c542d4604711d4a4623267df0f3d678491cd9fbcc32fd9'
            '3592a157f9c8c748a5f75d79c9e328f1c359ec6609d260a58d4b68ba97f7fe9b')
options=(staticlibs !lto)

prepare() {
    # linux/scc.h is gone from linux-api-headers >= 7.1
    patch -Np1 -d "$pkgbase" -i "$srcdir/0001-compiler-rt-sanitizer-Remove-linux-scc.h.patch"
}

build() {
    # Build only minimal debug info to reduce size
    CFLAGS+=' -g1'
    CXXFLAGS+=' -g1'

    # flang-rt compiles the Fortran modules with the just-built flang, which
    # errors out on the C-only flags makepkg exports in FFLAGS (see
    # /usr/share/makepkg/buildenv/fortran.sh) instead of ignoring them. Drop
    # exactly those and keep the rest, so -march, -O2, -g and
    # -fno-omit-frame-pointer still apply. If Arch ever adds another C-only flag
    # this fails loudly rather than silently dropping hardening.
    local _unsupported='-(pipe|fno-plt|fexceptions|fstack-clash-protection)\b'
    _unsupported+='|-(mno-omit-leaf-frame-pointer|Wformat|Werror=format-security)\b'
    _unsupported+='|-fcf-protection(=[^ ]*)?|-ffile-prefix-map=[^ ]*|-Wp,[^ ]*'
    FFLAGS=$(sed -E "s@($_unsupported)@@g" <<<"$FFLAGS")
    FCFLAGS=$(sed -E "s@($_unsupported)@@g" <<<"$FCFLAGS")
    export FFLAGS FCFLAGS

    local _rocm_exe_rpath='\$ORIGIN/../lib:\$ORIGIN/../../../lib'
    local _rocm_lib_rpath='\$ORIGIN'
    # comgr sits in /opt/rocm/lib, libLLVM.so in /opt/rocm/lib/llvm/lib
    local _rocm_comgr_rpath='\$ORIGIN/llvm/lib'
    # Flags according to
    # https://github.com/ROCm/ROCm/blob/87bc26e672e06294bd2a6a1b507ad5c9ae4cffba/tools/rocm-build/build_lightning.sh#L302
    local cmake_args=(
        -G Ninja
        -B build
        -S "$pkgbase/llvm"
        -D CMAKE_BUILD_TYPE=Release
        -D CMAKE_INSTALL_PREFIX="/opt/rocm/lib/llvm"
        -D LLVM_HOST_TRIPLE=$CHOST
        # mlir is a hard dependency of flang. flang provides the `flang` driver
        # that `amdflang` dispatches to; without it CLANG_ENABLE_AMDCLANG still
        # installs `amdflang`, leaving it pointing at a non-existent binary.
        # clang-tools-extra is not built: clangd, clang-tidy and friends add
        # ~1.1 GB, nothing in the ROCm stack uses them, and Arch already ships
        # them in the system clang package.
        -D LLVM_ENABLE_PROJECTS='clang;lld;mlir;flang'
        -D CLANG_ENABLE_AMDCLANG=ON
        -D PACKAGE_VENDOR="AMD"
        # flang-rt is the Fortran runtime; without it flang cannot link anything.
        # The OpenMP host runtime and the AMDGPU offload plugin are built by the
        # separate rocm-openmp package, because the plugin needs the HSA headers
        # from hsa-rocr, which in turn makedepends on this package.
        -D LLVM_ENABLE_RUNTIMES='compiler-rt;libunwind;libcxx;libcxxabi;flang-rt'
        # libc++ is built static only and not installed; it is a build-time dependency of the runtimes
        -D LIBCXX_ENABLE_SHARED=OFF
        -D LIBCXX_ENABLE_STATIC=ON
        -D LIBCXX_INSTALL_LIBRARY=OFF
        -D LIBCXX_INSTALL_HEADERS=OFF
        -D LIBCXXABI_ENABLE_SHARED=OFF
        -D LIBCXXABI_ENABLE_STATIC=ON
        -D LIBCXXABI_INSTALL_STATIC_LIBRARY=OFF
        -D LLVM_TARGETS_TO_BUILD='AMDGPU;NVPTX;Native'
        -D CLANG_DEFAULT_LINKER=lld
        -D ENABLE_LINKER_BUILD_ID=ON
        -D CLANG_DEFAULT_RTLIB=compiler-rt
        -D CLANG_DEFAULT_UNWINDLIB=libgcc
        -D LLVM_INSTALL_UTILS=ON
        -D LLVM_ENABLE_BINDINGS=OFF
        # Link the tools against a single libLLVM.so instead of statically
        -D LLVM_LINK_LLVM_DYLIB=ON
        -D LLVM_BUILD_LLVM_DYLIB=ON
        # Same for clang: without this comgr links the static clangBasic,
        # clangDriver, ... instead of libclang-cpp.so. AOMP sets it too.
        -D CLANG_LINK_CLANG_DYLIB=ON
        -D OCAMLFIND=NO
        -D LLVM_ENABLE_OCAMLDOC=OFF
        -D LLVM_INCLUDE_BENCHMARKS=OFF
        -D LLVM_BUILD_TESTS=OFF
        -D LLVM_INCLUDE_TESTS=OFF
        -D CLANG_INCLUDE_TESTS=OFF
        -D LLVM_BINUTILS_INCDIR=/usr/include
        -D CMAKE_SKIP_BUILD_RPATH=TRUE
        -D CMAKE_SKIP_INSTALL_RPATH=TRUE
        -D CMAKE_EXE_LINKER_FLAGS="-Wl,--enable-new-dtags,--build-id=sha1,--rpath,$_rocm_exe_rpath"
        -D CMAKE_SHARED_LINKER_FLAGS="-Wl,--enable-new-dtags,--build-id=sha1,--rpath,$_rocm_lib_rpath"
        -D CMAKE_CXX_STANDARD=17
        # Fortran driver and runtime. FLANG_RT_INCLUDE_AMD additionally builds
        # libflang_rt.amd.a, the part of the Fortran runtime that rocm-openmp
        # needs to make Fortran callable from inside OpenMP target regions.
        -D FLANG_RT_INCLUDE_AMD=ON
        -D FLANG_INCLUDE_DOCS=OFF
        -D FLANG_INCLUDE_TESTS=OFF
    )
    cmake "${cmake_args[@]}"

    local cmake_device_libs_args=(
        -Wno-dev
        -S "$pkgbase/amd/device-libs"
        -B build-device-libs
        -D CMAKE_BUILD_TYPE=None
        -D CMAKE_INSTALL_PREFIX=/opt/rocm
        -D CMAKE_PREFIX_PATH="$srcdir/build"
    )

    # The ROCm fork adds FIR/HLFIR includes to flang/Support/OpenMP-utils.h that
    # upstream does not have. Building the dialects first generates the header it needs
    cmake --build build -- HLFIRDialect CUFDialect

    # Bootstrapping libcxx, see
    # https://github.com/ROCm/ROCm/blob/87bc26e672e06294bd2a6a1b507ad5c9ae4cffba/tools/rocm-build/build_lightning.sh#L352-L359
    # llvm-link and opt are pulled in early because device-libs needs them.
    cmake --build build -- clang lld compiler-rt llvm-link opt
    cmake --build build -- runtimes cxx
    cmake --build build

    cmake "${cmake_device_libs_args[@]}"
    cmake --build build-device-libs

    local cmake_comgr_args=(
        -Wno-dev
        -S "$pkgbase/amd/comgr"
        -B build-comgr
        -D CMAKE_BUILD_TYPE=None
        -D CMAKE_INSTALL_PREFIX=/opt/rocm
        -D BUILD_TESTING=OFF
        -D CMAKE_PREFIX_PATH="$srcdir/build;$srcdir/build-device-libs"
        # comgr is installed in /opt/rocm/lib but links libLLVM.so from
        # /opt/rocm/lib/llvm/lib, which ld.so does not search: rocm.conf only
        # lists /opt/rocm/lib.
        -D CMAKE_SKIP_BUILD_RPATH=TRUE
        -D CMAKE_SKIP_INSTALL_RPATH=TRUE
        -D CMAKE_SHARED_LINKER_FLAGS="-Wl,--enable-new-dtags,--build-id=sha1,--rpath,$_rocm_comgr_rpath"
    )
    cmake "${cmake_comgr_args[@]}"
    cmake --build build-comgr
}

# Binaries that make up the usable compiler, taken from the rocm-llvm-core
# package definition in ROCm's build_lightning.sh. Everything else in bin/ is
# development tooling and goes to rocm-llvm-tools.
_core_bin=(amd-llvm-spirv amdgpu-arch amdgpu-offload-arch amdlld amdllvm
           amdclang amdclang++ amdclang-cl amdclang-cpp
           clang clang++ clang-cl clang-cpp clang-build-select-link
           clang-offload-bundler clang-offload-packager clang-offload-wrapper
           clang-linker-wrapper clang-nvlink-wrapper clang-sycl-linker
           ld64.lld ld.lld lld lld-link wasm-ld
           llc opt llvm-ar llvm-bitcode-strip llvm-dwarfdump llvm-install-name-tool
           llvm-link llvm-mc llvm-objcopy llvm-objdump llvm-otool llvm-ranlib
           llvm-readelf llvm-readobj llvm-strip llvm-symbolizer
           nvidia-arch nvptx-arch offload-arch)

package_rocm-llvm() {
    pkgdesc='Radeon Open Compute - LLVM toolchain (clang, lld)'
    license=('Apache-2.0 WITH LLVM-exception')
    depends=('rocm-llvm-libs' 'rocm-core' 'perl' 'glibc' 'libgcc' 'libstdc++' 'zlib' 'zstd'
             'libffi' 'libedit' 'ncurses' 'libxml2')
    optdepends=('rocm-flang: Fortran compiler'
                'rocm-llvm-headers: LLVM headers'
                'rocm-llvm-static: LLVM static libraries and CMake config'
                'rocm-llvm-tools: LLVM development tools'
                'rocm-openmp: OpenMP host runtime and GPU offloading')

    DESTDIR="$pkgdir" cmake --install build

    # Install everything here, then move each subset to $_split/<pkg>; what stays is rocm-llvm
    local _llvm="$pkgdir/opt/rocm/lib/llvm" _split="$srcdir/split"
    # The versioned binaries are named after the LLVM major version (clang-22),
    # which is unrelated to pkgver. Read it back from the resource directory.
    local _major
    _major=$(find "$_llvm/lib/clang" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | head -1)

    rm -rf "$_split"
    install -d "$_split"/{libs/lib,mlir/lib,tools/bin,tools/lib,headers,static/lib,flang/bin,flang/resource}

    # Only the two libraries actually loaded at runtime go to rocm-llvm-libs:
    # libLLVM.so and libclang-cpp.so are what the compiler binaries and comgr
    # link against.
    find "$_llvm/lib" -maxdepth 1 \( -name 'libLLVM.so*' -o -name 'libclang-cpp.so*' \) \
        -exec mv -t "$_split/libs/lib/" {} +

    # libMLIR.so is needed by flang and by the mlir-* tools, but by nothing in
    # the core compiler, so it gets its own package instead of being pulled in
    # by every rocm-llvm install.
    find "$_llvm/lib" -maxdepth 1 \( -name 'libMLIR*.so*' -o -name 'libmlir_*.so*' \) \
        -exec mv -t "$_split/mlir/lib/" {} +

    # libclang.so is the C API for tooling, libLTO.so and LLVMgold.so are the
    # binutils LTO plugins; nothing in the ROCm stack loads those.
    find "$_llvm/lib" -maxdepth 1 -name '*.so*' -exec mv -t "$_split/tools/lib/" {} +

    find "$_llvm/bin" -maxdepth 1 \( -name 'flang*' -o -name 'amdflang*' -o -name bbc \
        -o -name fir-opt -o -name tco \) -exec mv -t "$_split/flang/bin/" {} +
    mv "$_llvm/include/flang" "$_split/flang/"
    # --parents keeps the lib/clang/<major>/lib/<triple>/ path below resource/
    cd "$_llvm"
    find lib/clang -name 'libflang_rt.*' -exec cp -a --parents -t "$_split/flang/resource/" {} +
    find lib/clang -name 'libflang_rt.*' -delete
    cd "$srcdir"

    # Headers -> rocm-llvm-headers
    mv "$_llvm"/include "$_split/headers/"

    # Static libraries and CMake config -> rocm-llvm-static. The CMake files
    # reference *.a files, so they ship together.
    mv "$_llvm"/lib/cmake "$_split/static/lib/"
    find "$_llvm/lib" -maxdepth 1 -name '*.a' -exec mv -t "$_split/static/lib/" {} +

    # Remaining binaries (llvm-*, mlir-*, tblgen, FileCheck, ...) -> rocm-llvm-tools
    # A binary missing from _core_bin moves to rocm-llvm-tools.
    local _b _keep=()
    for _b in "${_core_bin[@]}" "clang-$_major" "amdclang-$_major"; do
        _keep+=(! -name "$_b")
    done
    find "$_llvm/bin" -mindepth 1 -maxdepth 1 "${_keep[@]}" -exec mv -t "$_split/tools/bin/" {} +

    # Some packages require amdclang to be found in /opt/rocm/bin
    mkdir -p "$pkgdir/opt/rocm/bin"
    local _compiler
    for _compiler in amdclang amdclang++ amdclang-cl amdclang-cpp amdlld; do
        ln -s /opt/rocm/lib/llvm/bin/$_compiler "$pkgdir/opt/rocm/bin/$_compiler"
    done

    cd "$pkgbase"
    install -Dm644 llvm/LICENSE.TXT "$pkgdir/usr/share/licenses/$pkgname/llvm-LICENSE"
    install -Dm644 clang/LICENSE.TXT "$pkgdir/usr/share/licenses/$pkgname/clang-LICENSE"
    install -Dm644 compiler-rt/LICENSE.TXT "$pkgdir/usr/share/licenses/$pkgname/compiler-rt-LICENSE"
    install -Dm644 lld/LICENSE.TXT "$pkgdir/usr/share/licenses/$pkgname/lld-LICENSE"
}

package_rocm-llvm-libs() {
    pkgdesc='Radeon Open Compute - LLVM runtime libraries'
    license=('Apache-2.0 WITH LLVM-exception')
    depends=('glibc' 'libgcc' 'libstdc++' 'zlib' 'zstd' 'libffi' 'libedit' 'ncurses' 'libxml2')

    install -d "$pkgdir/opt/rocm/lib/llvm/lib"
    cp -P "$srcdir"/split/libs/lib/* "$pkgdir/opt/rocm/lib/llvm/lib/"

    install -Dm644 "$srcdir/$pkgbase/llvm/LICENSE.TXT" \
        "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}

package_rocm-mlir-libs() {
    pkgdesc='Radeon Open Compute - MLIR runtime libraries'
    license=('Apache-2.0 WITH LLVM-exception')
    depends=('rocm-llvm-libs' 'glibc' 'libgcc' 'libstdc++')

    install -d "$pkgdir/opt/rocm/lib/llvm/lib"
    cp -P "$srcdir"/split/mlir/lib/* "$pkgdir/opt/rocm/lib/llvm/lib/"

    install -Dm644 "$srcdir/$pkgbase/mlir/LICENSE.TXT" \
        "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}

package_rocm-llvm-tools() {
    pkgdesc='Radeon Open Compute - LLVM development tools'
    license=('Apache-2.0 WITH LLVM-exception')
    depends=("rocm-llvm=$epoch:$pkgver-$pkgrel" 'rocm-llvm-libs' 'rocm-mlir-libs')

    install -d "$pkgdir/opt/rocm/lib/llvm"
    cp -a "$srcdir"/split/tools/bin "$pkgdir/opt/rocm/lib/llvm/"
    cp -a "$srcdir"/split/tools/lib "$pkgdir/opt/rocm/lib/llvm/"

    # https://bugs.archlinux.org/task/28479
    install -d "$pkgdir/opt/rocm/lib/llvm/lib/bfd-plugins"
    ln -s /opt/rocm/lib/llvm/lib/LLVMgold.so \
        "$pkgdir/opt/rocm/lib/llvm/lib/bfd-plugins/LLVMgold.so"

    install -Dm644 "$srcdir/$pkgbase/llvm/LICENSE.TXT" \
        "$pkgdir/usr/share/licenses/$pkgname/llvm-LICENSE"
    install -Dm644 "$srcdir/$pkgbase/mlir/LICENSE.TXT" \
        "$pkgdir/usr/share/licenses/$pkgname/mlir-LICENSE"
}

package_rocm-llvm-headers() {
    pkgdesc='Radeon Open Compute - LLVM headers'
    license=('Apache-2.0 WITH LLVM-exception')
    depends=("rocm-llvm=$epoch:$pkgver-$pkgrel")

    install -d "$pkgdir/opt/rocm/lib/llvm"
    cp -a "$srcdir"/split/headers/include "$pkgdir/opt/rocm/lib/llvm/"

    install -Dm644 "$srcdir/$pkgbase/llvm/LICENSE.TXT" \
        "$pkgdir/usr/share/licenses/$pkgname/llvm-LICENSE"
    install -Dm644 "$srcdir/$pkgbase/mlir/LICENSE.TXT" \
        "$pkgdir/usr/share/licenses/$pkgname/mlir-LICENSE"
}

package_rocm-llvm-static() {
    pkgdesc='Radeon Open Compute - LLVM static libraries and CMake configuration'
    license=('Apache-2.0 WITH LLVM-exception')
    # The CMake export files also check for include/ and the tools (llvm-tblgen, ...)
    depends=("rocm-llvm-headers=$epoch:$pkgver-$pkgrel" "rocm-llvm-tools=$epoch:$pkgver-$pkgrel")
    # FlangTargets-release.cmake checks for files from rocm-flang
    optdepends=('rocm-flang: find_package(Flang)')

    install -d "$pkgdir/opt/rocm/lib/llvm"
    cp -a "$srcdir"/split/static/lib "$pkgdir/opt/rocm/lib/llvm/"

    install -Dm644 "$srcdir/$pkgbase/llvm/LICENSE.TXT" \
        "$pkgdir/usr/share/licenses/$pkgname/llvm-LICENSE"
    install -Dm644 "$srcdir/$pkgbase/mlir/LICENSE.TXT" \
        "$pkgdir/usr/share/licenses/$pkgname/mlir-LICENSE"
}

package_rocm-flang() {
    pkgdesc='Radeon Open Compute - Fortran compiler'
    license=('Apache-2.0 WITH LLVM-exception')
    # flang links libMLIR.so, hence rocm-mlir-libs. gcc-libs provides
    # libquadmath, which flang needs for REAL(16).
    depends=("rocm-llvm=$epoch:$pkgver-$pkgrel" 'rocm-llvm-libs' 'rocm-mlir-libs'
             'gcc-libs' 'glibc' 'libgcc' 'libstdc++')
    optdepends=('rocm-openmp: OpenMP GPU offloading from Fortran')

    install -d "$pkgdir/opt/rocm/lib/llvm/include"
    cp -a "$srcdir"/split/flang/bin "$pkgdir/opt/rocm/lib/llvm/"
    cp -a "$srcdir/split/flang/flang" "$pkgdir/opt/rocm/lib/llvm/include/flang"
    cp -a "$srcdir"/split/flang/resource/. "$pkgdir/opt/rocm/lib/llvm/"

    # amdflang is dispatched through amdllvm, which lives in rocm-llvm
    install -d "$pkgdir/opt/rocm/bin"
    ln -s /opt/rocm/lib/llvm/bin/amdflang "$pkgdir/opt/rocm/bin/amdflang"

    install -Dm644 "$srcdir/$pkgbase/flang/LICENSE.TXT" \
        "$pkgdir/usr/share/licenses/$pkgname/flang-LICENSE"
    install -Dm644 "$srcdir/$pkgbase/flang-rt/LICENSE.TXT" \
        "$pkgdir/usr/share/licenses/$pkgname/flang-rt-LICENSE"
}

package_rocm-device-libs() {
    pkgdesc='AMD specific device-side language runtime libraries'
    license=('NCSA')
    depends=('rocm-core')

    DESTDIR="$pkgdir" cmake --install build-device-libs
    cd "$pkgbase/amd/device-libs"
    install -Dm644 LICENSE.TXT "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}

package_comgr() {
    pkgdesc='AMDGPU GPU Code Object Manager'
    license=('NCSA')
    depends=('glibc' 'libgcc' 'libstdc++' 'zstd' 'zlib' 'ncurses'
             'rocm-core' 'rocm-llvm' 'rocm-llvm-libs' 'rocm-device-libs')

    DESTDIR="$pkgdir" cmake --install build-comgr
    cd "$pkgbase/amd/comgr"
    install -Dm644 LICENSE.txt "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}
