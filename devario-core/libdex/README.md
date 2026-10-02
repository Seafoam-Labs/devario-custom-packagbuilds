# Libdex for Devario

Builds `libdex` and `libdex-docs` 1.2.0-1 for x86_64, adapted from
[Arch packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/libdex/-/blob/main/PKGBUILD).
The source is the [GNOME 1.2.0 release archive](https://download.gnome.org/sources/libdex/1.2/),
verified against its published SHA-256 checksum.

The runtime package includes headers, pkg-config metadata, GIR/typelib
files, Vala bindings, PyGObject overrides, and the GDBus code generator
extension. It explicitly provides `libdex-1.so=1-64`; packaging checks the
ELF64 library's `libdex-1.so.1` SONAME. API documentation is split into
`libdex-docs`.

From this repository's root:

```sh
shelly build --review-only --json ./devario-core/libdex/PKGBUILD
shelly build --isolated --check ./devario-core/libdex/PKGBUILD
```

Upstream requires GLib >= 2.87. Make compatible `glib2` and `glib2-devel`
packages available to the worker, along with the other declared dependencies.
The local GLib 2.90.0 recipe satisfies that requirement. Development tools
are needed for GDBus code generation; `gi-docgen` builds the documentation.
Tests run in a private D-Bus session. Publish both outputs and refresh the
worker repository before building dependent packages.

## Validation

Source checksum, Bash syntax, makepkg/Shelly metadata generation, and Shelly
review passed with no findings. A native build including documentation,
all 20 upstream tests, and staged installation of both packages passed.
The library SONAME, headers, bindings, code generator extension, and
`libdex-1.pc` version 1.2.0 were verified. Runtime and documentation packages
have no overlapping files.

Missing development/documentation tools were extracted into `/tmp`; no host
packages were installed. Full isolated worker builds and package archive
generation have not been performed here.
