# numactl for Shelly

Based on [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/numactl/-/blob/main/PKGBUILD),
this recipe builds `2.0.19-2` from the upstream release archive with source
checksum verification enabled. It explicitly provides `libnuma.so=1-64` and
checks the installed library's ELF class and SONAME before packaging.

From this repository's root:

```sh
shelly build --review-only --json ./numactl/PKGBUILD
shelly build --isolated --check ./numactl/PKGBUILD
```

Bash syntax, generated metadata, and Shelly review passed. A native unprivileged
Shelly build produced the package successfully. Six tests passed and three were skipped by the upstream suite.
See [the dependency build guide](../DEPENDENCY-BUILDS.md) for build ordering,
repository publication, and the limits of local isolated-build validation.

