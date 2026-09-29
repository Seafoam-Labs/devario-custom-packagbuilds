# lld21 for Shelly

Based on [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/lld21/-/blob/main/PKGBUILD), pinned to `21.1.8-1`. Copy the whole directory to the worker, including local patches and `keys/` where present.

Installs LLVM 21 linker libraries alongside newer LLVM versions. Arch disables `check()` because two tests fail; `--check` does not enable that suite.

The permitted upstream signing fingerprints are:

- `474E22316ABF4785A88C6E8EA2C794A986419D8A`
- `D574BD5D1D0E98895E3BF90044F2485E45D59042`
- `FFB3368980F3E6BB5737145A316C56D064CACBA5`
- `71046D1E9C6656BDD61171873E83BABF4A4F9E85`

Import the supplied public keys as the build account after checking these fingerprints:

```sh
gpg --import lld21/keys/pgp/*.asc
```

From the repository root:

```sh
shelly build --review-only --json ./lld21/PKGBUILD
shelly build --isolated --check ./lld21/PKGBUILD
```

Bash syntax, generated metadata, source checksums, applicable signatures, and source preparation were validated. makepkg and Shelly metadata agree. See [the Zig build guide](../ZIG-BUILDS.md) for build order, bootstrap dependencies, review findings, and the exact limits of local build validation.
