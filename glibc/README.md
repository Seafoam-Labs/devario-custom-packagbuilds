# glibc for Shelly

Based on [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/glibc/-/blob/main/PKGBUILD), pinned to `2.44+r50+g1848099f063e-1`. Copy the entire directory, including supporting files and keys.

Builds `glibc`, `lib32-glibc`, and `glibc-locales` together. Install the native and 32-bit libc packages at matching versions. Requires existing multilib GCC libraries to bootstrap.

From the repository root:

```sh
shelly build --review-only --json ./glibc/PKGBUILD
shelly build --isolated --check ./glibc/PKGBUILD
```

Bash syntax, generated metadata, and bundled source checksums were validated.
Remote source checksums/signatures, full builds, and upstream tests have not been
run. See [the multilib guide](../MULTILIB-BUILDS.md) for bootstrap requirements,
build order, signing-key handling, and the isolated-root toolchain probe.
