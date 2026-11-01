rocMLIR packaging notes (2026-11-01)

This package supplies the static rockCompiler used by MIGraphX. It is pinned
to the rocMLIR source tree that MIGraphX 7.2.3 selects from AMDMIGraphX's
requirements.txt: tags rocm-7.2.2 and rocm-7.2.3 both point at commit
6671a1ee31d44e1f2f7743a26a71ffc4ce9169bf, so MIOpen 7.2.4 builds the same
tree and can adopt this package without a version split.

The recipe builds with BUILD_FAT_LIBROCKCOMPILER=ON and BUILD_SHARED_LIBS=OFF,
the configuration the inline MIGraphX stage used, and installs under /opt/rocm:

    /opt/rocm/lib/librockCompiler.a
    /opt/rocm/include/rocMLIR/...
    /opt/rocm/lib/cmake/rocmlir/rocmlir-config.cmake

Consumers find rocMLIR::rockCompiler through rocMLIR_DIR. The archive is
linked into the consumer, so rocmlir is a makedepend rather than a runtime
dependency; hsa-rocr stays a dependency because the exported target links
hsa-runtime64.

The package has no DEVARIO-UPSTREAM.json because Arch packages rocMLIR only
inside MIGraphX and MIOpen. It also has no .nvchecker.toml: the revision is
chosen by its consumers, not by the newest rocMLIR tag. Update the pin when
AMDMIGraphX or MIOpen changes its rocMLIR tree, and bump rocmlir's pkgrel
once for that change.

Validation status: the installed CMake package and static archive can only be
confirmed by a worker build. Build and publish rocmlir first, then refresh the
worker's repository database so migraphx and miopen-hip resolve the new
makedepend. Check that MIGraphX configures with
`rocMLIR_DIR=/opt/rocm/lib/cmake/rocmlir`, links `librockCompiler.a` into
`libmigraphx_gpu.so`, and no longer compiles LLVM/MLIR itself.

The first worker attempt failed at configure because Shelly's build shell does
not source `/etc/profile.d/rocm.sh`, so `amdclang` was not on PATH. Both stages
now export `/opt/rocm/bin`, which also puts `/opt/rocm` into CMake's prefix
search: the Rock dialect calls `find_package(hsa-runtime64 REQUIRED)` without a
hint, and the tool and device-library stages require `hip`, `hiprtc` and
`AMDDeviceLibs`. The recipe therefore lists hip-runtime-amd and
rocm-device-libs as makedepends, plus python because the vendored LLVM and the
test tree require a Python 3 interpreter at configure time.
