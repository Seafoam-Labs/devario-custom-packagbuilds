# gtksourceview5 for Shelly

Based on [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/gtksourceview5/-/blob/main/PKGBUILD),
this recipe builds `5.20.0-2` from the upstream release Git tag with source
checksum verification enabled. It explicitly provides `libgtksourceview-5.so=0-64` and
checks the installed library's ELF class and SONAME before packaging.

The same build also produces `gtksourceview5-docs`. Documentation, introspection,
and Vala support are preserved. Build and publish GLib's `glib2-devel` output
first; it supplies the development tools required in the isolated root.

From this repository's root:

```sh
shelly build --review-only --json ./gtksourceview5/PKGBUILD
shelly build --isolated --check ./gtksourceview5/PKGBUILD
```

Bash syntax, generated metadata, and Shelly review passed. A native unprivileged
Shelly build produced the package successfully. All 26 upstream tests passed using Xvfb and a temporary D-Bus session.
See [the dependency build guide](../DEPENDENCY-BUILDS.md) for build ordering,
repository publication, and the limits of local isolated-build validation.

