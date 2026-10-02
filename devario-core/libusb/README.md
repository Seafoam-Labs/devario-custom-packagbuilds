# Libusb for Shelly

Builds libusb 1.0.30-2 with the explicit `libusb-1.0.so=0-64` provision
required by libgusb. This resolves the missing provider at the start of
the reported `libgusb -> colord -> weston` dependency failure while
provisioning libadwaita's isolated build root.

Adapted from [Arch packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/libusb/-/blob/main/PKGBUILD),
retaining its pinned release tag and both source checksums. The package
release is incremented for the corrected metadata. Packaging checks that
the built library is ELF64 with SONAME `libusb-1.0.so.0`. Udev support
remains enabled, with `systemd-libs` and `libudev.so=1-64` dependencies.

From the repository root:

```sh
shelly build --review-only --json ./devario-core/libusb/PKGBUILD
shelly build --isolated --check ./devario-core/libusb/PKGBUILD
```

Publish the resulting `libusb-1.0.30-2-x86_64.pkg.tar.zst`, refresh the
repository database used by the worker, and retry libadwaita in a fresh
isolated root. The published binary package and repository database must
contain the corrected provision; changing only `.SRCINFO` or the host's
installed library does not update the worker's repository metadata.

Check the built archive before publishing:

```sh
bsdtar -xOf /path/to/libusb-1.0.30-2-x86_64.pkg.tar.zst .PKGINFO | grep '^provides = '
```

Expected output: `provides = libusb-1.0.so=0-64`.

## Validation

Both source checksums, Bash syntax, makepkg/Shelly metadata generation,
and Shelly review passed with no findings. A native makepkg build passed
all four upstream test programs and produced the package archive. Its
`.PKGINFO` contains the exact required provision, and the ELF64 library's
SONAME is `libusb-1.0.so.0`.

Tests were run outside the local execution sandbox because it blocked
udev initialization. No host packages were installed. The isolated worker
build and repository publication remain outstanding.
