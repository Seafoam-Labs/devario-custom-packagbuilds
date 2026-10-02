# NFS utilities for Devario

Builds `nfs-utils` and `nfsidmap` version `3.1.1-2`, based on
[Arch packaging commit 5b87798048485436ceebc580fb698ba2f3747d92](https://gitlab.archlinux.org/archlinux/packaging/packages/nfs-utils/-/commit/5b87798048485436ceebc580fb698ba2f3747d92).
This supplies the live image's NFS client/server tools and ID-mapping library.

The recipe retains the kernel.org archive checksum and detached signature,
Steve Dickson's public key under `keys/pgp/`, exports configuration, sysusers
declaration, service files, ownership, and split-package layout. Publish both
outputs together: `nfs-utils` requires the matching `nfsidmap` version.
`nfsidmap` explicitly provides `libnfsidmap.so` and `libnfsidmap.so=1-64`,
guarded by an ELF64/SONAME check.

The repository databases inspected on 2026-10-02 lack runtime packages
`rpcbind` and `gssproxy`, and build dependency `rpcsvc-proto`. Supply those
before building. See the [dependency build guide](../../DEPENDENCY-BUILDS.md)
for worker commands and public-key import instructions.

Validation: Bash syntax, makepkg and Shelly metadata, Shelly review, source
checksums, and the upstream detached signature passed. The source's libtool
version confirms the declared SONAME. Compilation, `make check`, packaging,
and an actual NFS mount have not been run.
