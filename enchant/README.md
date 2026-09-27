# enchant for Shelly

Based on [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/enchant/-/blob/main/PKGBUILD),
this recipe builds `2.8.21-2` from the upstream release tarball with source
checksum verification enabled. It explicitly provides `libenchant-2.so=2-64` and
checks the installed library's ELF class and SONAME before packaging.

The release archive includes bootstrapped gnulib, avoiding an unpinned gnulib
checkout and network fetches during `prepare()`. The tarball's SHA-256 was
checked against the digest published with the upstream GitHub release. All five
spellchecking backends remain enabled when their declared build dependencies
are present. Install dictionaries separately for the selected backend.

From this repository's root:

```sh
shelly build --review-only --json ./enchant/PKGBUILD
shelly build --isolated --check ./enchant/PKGBUILD
```

Bash syntax, generated metadata, and Shelly review passed. A native unprivileged
Shelly build produced the package successfully. Both library test groups and all four program test groups passed.
See [the dependency build guide](../DEPENDENCY-BUILDS.md) for build ordering,
repository publication, and the limits of local isolated-build validation.

