# llvm21 for Shelly

Devario package `21.1.8-1.1`, adapted from [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/llvm21/-/blob/main/PKGBUILD). Copy the whole directory to the worker, including local patches and `keys/` where present.

One build produces `llvm21` and `llvm21-libs`. Publish both together. The development package requires the exact runtime release from this build. Tools live under `/usr/lib/llvm21`; versioned command links such as `llvm-config-21` allow LLVM 21 to coexist with newer LLVM packages. The runtime package declares the current split GCC runtime dependencies. After compilation, `llc --version` runs with eager symbol binding against the newly built library.

The permitted upstream signing fingerprints are:

- `474E22316ABF4785A88C6E8EA2C794A986419D8A`
- `D574BD5D1D0E98895E3BF90044F2485E45D59042`
- `FFB3368980F3E6BB5737145A316C56D064CACBA5`
- `71046D1E9C6656BDD61171873E83BABF4A4F9E85`

Import the supplied public keys as the build account after checking these fingerprints:

```sh
gpg --import devario-core/llvm21/keys/pgp/*.asc
```

From the repository root:

```sh
shelly build --review-only --json ./devario-core/llvm21/PKGBUILD
shelly build --isolated --check ./devario-core/llvm21/PKGBUILD
```

Bash syntax, generated metadata, source checksums, applicable signatures, and source preparation were validated. makepkg and Shelly metadata agree. See [the Zig build guide](../../ZIG-BUILDS.md) for build order, bootstrap dependencies, review findings, and the exact limits of local build validation.
