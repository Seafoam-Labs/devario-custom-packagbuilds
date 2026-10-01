libassuan 3.0.2-2: compatibility for existing GnuPG binaries

The isolated Clang build failed before source key import because GPG required
LIBASSUAN_1.0 from libassuan.so.9, while upstream libassuan 3.0.2 exports
LIBASSUAN_2.0. Upstream changed only the version-node name in release 3.0.1:
https://github.com/gpg/libassuan/commit/c9e902705a50abaf532c9d24347dfd1f3b5779fb

This recipe keeps LIBASSUAN_2.0 as the default for newly linked programs and
adds LIBASSUAN_1.0 compatibility aliases for the same 98 functions. Existing
consumers of either version can use the library. The SONAME remains
libassuan.so.9. The package step checks ELF64, SONAME, and both versions of
every function before producing an archive. The explicit libassuan.so=9-64
provision supports Shelly's dependency metadata handling.

The small patch adds the old version node and includes a generated assembler
alias header only while compiling the library. The header is generated from
upstream's export list. Distinct assembler aliases preserve both versions;
the version script keeps intermediate compat_* symbols private. This was
tested with GCC and link-time optimization enabled.

The signed Git source URL uses ?signed before #tag, as expected by
makepkg. The upstream tag and its SHA-256 checksum are unchanged. The pinned
Werner Koch public key is included under keys/pgp/.

Recovery on the worker

1. Build this recipe on a builder with working GPG and source-key import.
   Resolve the isolated keyboxd startup/configuration issue before using that
   root. Keep source checksums and signature verification enabled.
2. Publish/sign libassuan 3.0.2-2 and refresh the repository database through
   the normal repository workflow.
3. Ensure the worker's isolated root/bootstrap cache selects the rebuilt
   package. Refresh any cached root that retains an older release.
4. Check /usr/bin/gpg --version inside that root. Before retrying Clang, also
   repair the isolated GPG keyboxd startup/configuration; that is a separate
   issue from libassuan's ABI compatibility.

Example build from this repository's root, using a working isolated root:
  shelly build --review-only --json ./devario-core/libassuan/PKGBUILD
  shelly build --isolated --check ./devario-core/libassuan/PKGBUILD

Validation on 2026-09-30

- Source checksum and signed upstream tag verified.
- Native package build succeeded; all four upstream tests passed. The socket
  test required running outside this session's socket-restricted sandbox.
- dlvsym resolved all 98 functions under both LIBASSUAN_1.0 and LIBASSUAN_2.0
  to identical addresses. No compat_* implementation aliases were exported.
- GPG 2.4.9 started with the rebuilt library and imported all four bundled
  Clang public keys into a temporary keyring, returning exit status zero.
- No host packages were installed. This task did not publish the package or
  update the user's worker. A full isolated Clang build has not been rerun.
