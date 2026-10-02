# Libmalcontent bootstrap for Devario

Builds `libmalcontent 0.14.0-5` from the checksummed upstream 0.14.0 tag.
The source checksum comes from Arch's malcontent recipe at commit
`b73007214057fbbb17c3fee61fe221ccca7e6645`.

Flatpak needs libmalcontent, but the full malcontent UI needs Flatpak. The small
Meson patch adds `library_only` and builds only the upstream public library,
headers, pkg-config metadata, GIR and typelib. It preserves the upstream library
implementation and public ABI. It avoids the UI, daemons, bundled subprojects,
documentation generators, and test helpers required by the full application.
It does not install the parental-control administration UI or service policies.

The recipe supplies `libmalcontent-0.so` and `libmalcontent-0.so=0-64`, with an
ELF64/SONAME guard. Publish it before provisioning Flatpak consumers. Build
dependencies include `glib2-devel` for `glib-mkenums`, introspection tools,
D-Bus and Polkit development metadata required by the upstream root build.

Validation: checksum and clean patch application, Bash syntax, metadata, Shelly
review, compilation and package creation passed. Local validation supplied
`glib-mkenums` from temporary GLib development tools without installing host
packages. The built library's GIR typelib loads through Python/PyGObject.
Upstream unit tests are not part of this bootstrap profile. Full isolated
worker validation remains pending. See [the build guide](../../DEPENDENCY-BUILDS.md).
