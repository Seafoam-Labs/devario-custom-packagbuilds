# jq for Shelly

Based on [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/jq/-/blob/main/PKGBUILD),
this recipe builds `1.8.2-2` from the upstream release Git tag with source
checksum verification enabled. It explicitly provides `libjq.so=1-64` and
checks the installed library's ELF class and SONAME before packaging.

From this repository's root:

```sh
shelly build --review-only --json ./jq/PKGBUILD
shelly build --isolated --check ./jq/PKGBUILD
```

Bash syntax, generated metadata, and Shelly review passed. A native unprivileged
Shelly build produced the package successfully. All nine upstream test groups passed.
See [the dependency build guide](../DEPENDENCY-BUILDS.md) for build ordering,
repository publication, and the limits of local isolated-build validation.

