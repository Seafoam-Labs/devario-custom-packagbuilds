# hunspell for Shelly

Based on [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/hunspell/-/blob/main/PKGBUILD),
this recipe builds `1.7.3-2` from the upstream release tarball with source
checksum verification enabled. It explicitly provides `libhunspell-1.7.so=0-64` and
checks the installed library's ELF class and SONAME before packaging.

From this repository's root:

```sh
shelly build --review-only --json ./hunspell/PKGBUILD
shelly build --isolated --check ./hunspell/PKGBUILD
```

Bash syntax, generated metadata, and Shelly review passed. A native unprivileged
Shelly build produced the package successfully. All 145 upstream tests passed.
See [the dependency build guide](../DEPENDENCY-BUILDS.md) for build ordering,
repository publication, and the limits of local isolated-build validation.

