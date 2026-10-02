# clang21 for Shelly

Devario package `21.1.8-1`, adapted from [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/clang21/-/blob/main/PKGBUILD). Copy the whole directory to the worker, including local patches and `keys/` where present.

Build and runtime dependencies require Devario's `llvm21` / `llvm21-libs`
published release `21.1.8-1.1`. Packaging
always runs the staged `clang --version` with eager symbol binding to catch
unresolved runtime symbols, including when the full test suite is disabled.

Keeps the upstream stack-protector and ArmPL patches and the LLVM 21 installation prefix. Arch disables `check()` because its Clang tests are incompatible with the newer lit runner; `--check` does not enable those tests. Requires `compiler-rt21` and the GCC compiler package.

The permitted upstream signing fingerprints are:

- `474E22316ABF4785A88C6E8EA2C794A986419D8A`
- `D574BD5D1D0E98895E3BF90044F2485E45D59042`
- `FFB3368980F3E6BB5737145A316C56D064CACBA5`
- `71046D1E9C6656BDD61171873E83BABF4A4F9E85`

Import the supplied public keys as the build account after checking these fingerprints:

```sh
gpg --import devario-core/clang21/keys/pgp/*.asc
```

From the repository root:

```sh
shelly build --review-only --json ./devario-core/clang21/PKGBUILD
shelly build --isolated --check ./devario-core/clang21/PKGBUILD
```

Bash syntax, generated metadata, source checksums, applicable signatures, and source preparation were validated. makepkg and Shelly metadata agree. See [the Zig build guide](../../ZIG-BUILDS.md) for build order, bootstrap dependencies, review findings, and the exact limits of local build validation.
