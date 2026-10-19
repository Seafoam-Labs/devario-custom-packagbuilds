# binutils for Shelly

Based on [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/binutils/-/blob/main/PKGBUILD), pinned to `2.47-4`. Copy the entire directory, including supporting files and keys.

Provides the native assembler and linker with x86 multilib support. Retains upstream configuration and patches. The upstream test hook does not fail on test failures; inspect the test results.

Release `2.47-8` explicitly enables `--as-needed` so the unused `-lfl` from
configure's lexer detection does not become a runtime dependency. Packaging
rejects `ar` or `ranlib` with a `DT_NEEDED` entry for `libfl.so`, including when
the upstream test hook is skipped. Rebuild and publish this release to fix
systems affected by `2.47-7`.

From the repository root:

```sh
shelly build --review-only --json ./binutils/PKGBUILD
shelly build --isolated --check ./binutils/PKGBUILD
```

Bash syntax, generated metadata, and bundled source checksums were validated.
Remote source checksums/signatures, full builds, and upstream tests have not been
run. See [the multilib guide](../MULTILIB-BUILDS.md) for bootstrap requirements,
build order, signing-key handling, and the isolated-root toolchain probe.
