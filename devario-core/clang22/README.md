# Clang 22 for Zig 0.17

Build `clang22 22.1.8-1` after publishing `llvm22` and `llvm22-libs`
`22.1.8-3`. Both dependencies are pinned to that release. This recipe uses
upstream LLVM monorepo sources and the versioned installation layout from
the existing Clang 21 recipe.

Tools and headers install under `/usr/lib/llvm22`. Versioned shared libraries
are exposed under `/usr/lib`, allowing Zig to load them alongside other LLVM
releases. Packaging starts the staged tool with eager symbol binding. The
`check()` hook runs upstream tests using the source tree's matching lit runner.

The distro stack-protector default patch is adapted to LLVM 22’s split
safe-stack test. The existing ArmPL driver revert is retained. Copy the
whole recipe directory, including patches and public signing keys.

The LLVM archive signature was verified against Douglas Yung's key,
`FFB3368980F3E6BB5737145A316C56D064CACBA5`. Import the supplied public keys
into the worker build account's keyring before building.

```sh
gpg --import devario-core/clang22/keys/pgp/*.asc
shelly build --review-only --json ./devario-core/clang22/PKGBUILD
shelly build --isolated --check ./devario-core/clang22/PKGBUILD
```

Bash syntax, metadata generation, source checksums, signature verification,
and source preparation passed. Shelly review flags the inherited dynamic distribution-component
calculation; it has been inspected. CMake configuration,
compilation, and tests still require worker validation.

See [the Zig 0.17 guide](../zig/README.md) for the complete build order.
