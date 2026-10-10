# CppUTest for Devario

Builds `cpputest` 4.0-6, the C/C++ unit-testing and mocking framework required
by `roc-toolkit`. The package name is `cpputest`, not `cputest` or `cppunit`.
The recipe is adapted from the upstream Arch package recorded in
`DEVARIO-UPSTREAM.json`, with the source pinned by SHA-512 and BLAKE2 checksums.

The only declared build dependency is `cmake`, in addition to the worker's
standard C/C++ build toolchain. Static libraries are intentionally retained:
the package installs `libCppUTest.a`, `libCppUTestExt.a`, headers, CMake
configuration, and `cpputest.pc` for consumers such as ROC Toolkit.

```sh
shelly build --isolated ./devario-development/cpputest/PKGBUILD
```

Publish the resulting package and refresh worker repository metadata before
retrying `roc-toolkit`.

Validation: both source checksums, Bash syntax, and makepkg/Shelly metadata
agreement passed. The recipe's build, check, and package functions completed
with CMake 4.4.4; all 79 CTest entries passed. Libraries, headers, pkg-config
metadata, and the license were staged under a temporary package root. No host
packages were installed. Final package archive creation and a full isolated
worker build have not been run.
