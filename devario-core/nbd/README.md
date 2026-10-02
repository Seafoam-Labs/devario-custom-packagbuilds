# NBD for Devario

Builds `nbd` version `3.27.1-4`, based on
[Arch packaging commit e71037c4ee8bd257a23d8774669e832376731890](https://gitlab.archlinux.org/archlinux/packaging/packages/nbd/-/commit/e71037c4ee8bd257a23d8774669e832376731890).
This supplies the client and server for live-image network block devices.

The recipe retains Arch's checksummed release tag and three upstream fixes,
server configuration, systemd service, sysusers declaration, and packaging
licenses. `glibc` is explicitly declared alongside GLib, GnuTLS, and libnl.
The upstream client template `nbd@.service` is also packaged. No service is
enabled automatically by this recipe.

The repository databases inspected on 2026-10-02 lack `autoconf-archive`,
`docbook-utils`, and `perl-sgmls`, all declared build dependencies. Supply them
before building; the SGML tools generate the manual pages.

Validation: source checksums, Bash syntax, makepkg and Shelly metadata, Shelly
review, and application of all three upstream fixes passed. Preparation on
this host then stops at the missing `autoconf-archive` macros. A complete build
has not been run. Arch's disabled test suite remains disabled; verify an NBD
client/server connection and live-image boot separately on a capable worker.
See the [dependency build guide](../../DEPENDENCY-BUILDS.md) for commands.
