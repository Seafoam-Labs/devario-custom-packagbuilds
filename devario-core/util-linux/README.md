# util-linux for Shelly isolated builds

This recipe builds `util-linux` and `util-linux-libs` 2.42.4-3, based on
[Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/util-linux/-/blob/main/PKGBUILD).
It retains the signed release tag, original source checksums, build options,
PAM files, services, udev rules, and package split.

Arch's recipe sets `_python_stdlib` inside `package_util-linux()` and reuses it
inside `package_util-linux-libs()`. Shelly runs these functions in separate
shells, so the second function loses that value. The original code relies on
creating the Python directory to also create its parent `/usr/lib`; without
the variable, `mv` fails with the error from the build log.

This recipe computes the Python path independently in both functions and
explicitly creates `/usr/lib`, the Python directory, and `/usr/share/man` before
moving the library payload. Both functions explicitly start in `$srcdir`.
The staged files continue to pass between packages through the filesystem.
Build dependencies are also declared explicitly for the isolated root.

Upload all files in this directory together into Remora. Import the bundled
public release key as the account that invokes Shelly, after checking its
fingerprint against `validpgpkeys`:

```sh
cd util-linux
gpg --import B0C64D14301CC6EFAEDF60E4E4B71D5EEC39C284.asc
shelly build --review-only --json ./PKGBUILD
shelly build --isolated ./PKGBUILD
```

Release 3 adds `libuuid.so=1-64` to `util-linux-libs`, alongside its existing
bare provision. Shelly preserves this explicit ABI dependency for consumers
such as wget. Packaging verifies that the staged library is ELF64 with SONAME
`libuuid.so.1`, and fails if the declared ABI no longer matches the binary.
Rebuild and publish both split packages together, then refresh the worker
repository database before retrying dependent builds.

Release 3 validation: Bash syntax, makepkg and Shelly metadata, and Shelly review
passed. The ABI helper accepts the matching host library and rejects an
incorrect SONAME or an executable without a SONAME. This revision has not been
compiled or published.

Validation of release 2, before the ABI metadata change:

- Shell syntax, `.SRCINFO` generation, and Shelly review passed (no findings).
- The release-tag signature and all source checksums verified successfully.
- A separate-shell regression reproduced the exact missing-directory error
  with Arch's function and passed with the corrected function.
- Shelly's native unprivileged builder produced both package archives.
- Checked that the archives have no overlapping payload files and that shared
  libraries, headers, pkg-config files, Python bindings, and section 3 manuals
  reside in `util-linux-libs`.
- Imported the packaged Python libmount bindings and ran the packaged
  `findmnt` and `uuidgen` with the packaged libraries.
- Confirmed root ownership and mode `4755` for `newgrp`, `chsh`, and `chfn`
  in the package archive.

Native validation used `--no-check`; the full upstream regression suite was not
run. The recipe retains Arch's `check()` function. Missing documentation tools
were signature-verified and extracted under `/tmp` for validation; no host
packages were installed. Full nspawn verification remains unavailable locally
because Shelly's coordinator requires an interactive sudo password.
