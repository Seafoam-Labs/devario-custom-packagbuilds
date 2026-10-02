# LLVM 22 for Devario

This Devario recipe builds `llvm22` and `llvm22-libs` version `22.1.8-3` from
LLVM's signed source release. The recipe was adapted from [Arch packaging commit
1ecd452c461c3a65fa9041493aa68d2557c78ce7](https://gitlab.archlinux.org/archlinux/packaging/packages/llvm22/-/commit/1ecd452c461c3a65fa9041493aa68d2557c78ce7)
and retains its SelectionDAG backport, source checksums, split GCC runtime
dependencies, and LLVM test hook. Devario is an independent operating system;
the Arch reference records the adapted recipe's provenance.

The development package installs under `/usr/lib/llvm22` and supplies versioned
commands such as `llvm-config-22`. Consumers can use
`-DCMAKE_PREFIX_PATH=/usr/lib/llvm22` or
`-DLLVM_DIR=/usr/lib/llvm22/lib/cmake/llvm` to select this version. The runtime
package installs `libLLVM.so.22.1` in `/usr/lib` and declares
`libLLVM.so=22.1-64` explicitly for Shelly. Packaging verifies the ELF64 SONAME.
Publish both split packages together.

Copy this entire directory, including the patch and signing keys, to the
worker. The accepted LLVM release signing fingerprints are:

- `474E22316ABF4785A88C6E8EA2C794A986419D8A`
- `D574BD5D1D0E98895E3BF90044F2485E45D59042`
- `FFB3368980F3E6BB5737145A316C56D064CACBA5`
- `71046D1E9C6656BDD61171873E83BABF4A4F9E85`

From the repository root, import the supplied public keys as the build account,
then review and build:

```sh
gpg --import devario-core/llvm22/keys/pgp/*.asc
shelly build --review-only --json ./devario-core/llvm22/PKGBUILD
shelly build --isolated --check ./devario-core/llvm22/PKGBUILD
```

The worker must supply the dependencies listed in `.SRCINFO`, including CMake,
Ninja, the development libraries, and Python build/test helpers. Compiler and
CPU flags come from the worker configuration. LTO remains disabled because it
breaks an LLVM shared-library test.

## Validation

Bash syntax and makepkg/Shelly metadata checks passed. Source and patch
checksums, the LLVM release signature, and patch application passed. Both
CMake configuration passes and a Ninja dry-run succeeded with the recipe's
selected distribution components, including LLVM and LLVMgold.

Shelly review warns about the distribution-component command substitution
and backticks in the patch text; those inputs were inspected and retained.
Full compilation, LLVM tests, and an isolated package build have not been run.
