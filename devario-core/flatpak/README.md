# Flatpak for Devario

Builds `flatpak` and `flatpak-docs` version `1:1.18.4-3`, based on
[Arch packaging commit 22a6dfa94f4c91c266a61823a1558c9fbc6d88fa](https://gitlab.archlinux.org/archlinux/packaging/packages/flatpak/-/commit/22a6dfa94f4c91c266a61823a1558c9fbc6d88fa).
This supplies the runtime required by Shelly's Flatpak backend. The recipe
retains the profile script, Flathub remote definition, signed upstream tag,
source checksums, and all three upstream public keys under `keys/pgp/`.

Devario explicitly provides `libflatpak.so=0-64`, guarded by an ELF64/SONAME
check, and requests `libostree-1.so=1-64`. Publish the existing Devario ostree
recipe with that provision before building. The bare `libflatpak.so` provision
is retained for consumers that use an unversioned requirement.

On 2026-10-02, repository metadata still lacked runtime packages
`libmalcontent` and `xdg-dbus-proxy`, plus build tools `gtk-doc`,
`python-pyparsing`, and `xmlto`. See the repository's
[dependency build guide](../../DEPENDENCY-BUILDS.md) for worker commands.

Validation: Bash syntax, makepkg and Shelly metadata, Shelly review, all source
checksums, and the upstream Git-tag signature passed. A full build has not
been run. Arch skips running integration tests because they hang in containers.
Release 3 also explicitly sets Meson's `tests=false` and
`installed_tests=false`. Omitting `check()` alone left test compilation enabled
and made `socat` mandatory during configuration, causing the isolated build
failure in release 2. The test-only dependencies are no longer required with
these options.
Verify Flatpak installation and sandbox execution on the built Devario system.
