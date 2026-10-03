# shadow for unprivileged Shelly builds

Upload all files in this directory together into Remora, including the public
key `.asc` files beside `PKGBUILD`. No subdirectories are required. The package is
`shadow 4.20.0.arch1-3`, based on Arch's packaging commit
`b9fd1505550d16a29861b4a0f6ac2de9a6d51a5a`:
https://gitlab.archlinux.org/archlinux/packaging/packages/shadow/-/tree/b9fd1505550d16a29861b4a0f6ac2de9a6d51a5a

The small local patch removes the two `setcap` commands from upstream's install
rule. `--with-fcaps` stays enabled, so `newuidmap` and `newgidmap` are packaged
with mode 0755 rather than setuid permissions. `shadow.install` applies and
verifies `cap_setuid=ep` and `cap_setgid=ep` after installation and every upgrade.
`libcap` is an explicit runtime dependency. Capability failures are reported and
return a nonzero scriptlet status; there is no setuid fallback. The package
manager may already have installed files when a scriptlet fails, so resolve the
error and reinstall before relying on the mapping helpers.

Arch's distribution patch, PAM files, service/timer, upstream source
checksums, and PGP verification are retained. The recipe does not require any
setcap support in Shelly. The mapping helpers intentionally have no capabilities
in the staging directory or archive: running the install scriptlets is required.
Do not use `--noscriptlet` when installing this package.

Release 3 sets `SHELL=/usr/bin/fish` in the packaged `/etc/default/useradd`.
Devario's base package requires Fish and this Shadow release so newly created
users receive an installed shell. Explicit `useradd -s` choices take precedence.
Existing account shells are not migrated. The defaults file
remains a backed-up configuration file, preserving administrator changes.

## Source keys and building

Import the bundled public keys as the account that runs the builder, after
checking their fingerprints against `validpgpkeys` in the PKGBUILD:

```sh
gpg --import ./*.asc
shelly build --review-only --json ./PKGBUILD
shelly build --isolated ./PKGBUILD
```

The included Alejandro Colomar key contains signing subkey
`4BB26DF6EF466E6956003022EB89995CC290C2A9`, needed by the 4.20.0 release tag.
Its primary fingerprint is still
`A9348594CE31283A826FBDD8D57633D441E25BB5`. The original Arch packaging snapshot
had an older copy of this key. No signature checks have been disabled.

When building natively, install the declared build dependencies first. In
particular, `itstool` is needed to generate the translated manual pages.
Regenerate `.SRCINFO` with `makepkg --printsrcinfo > .SRCINFO` after recipe edits.

After installing into a disposable test system, check:

```sh
getcap /usr/bin/newuidmap /usr/bin/newgidmap
stat -c '%a %n' /usr/bin/newuidmap /usr/bin/newgidmap
```

Expect `cap_setuid=ep`, `cap_setgid=ep`, and mode `755` for both programs.
The install script requires a privileged installer with `CAP_SETFCAP` and a
target filesystem that supports file capabilities.

## Validation

Release 3 passed Bash syntax checks, metadata regeneration, all 12 bundled-file
checksum checks, and Shelly review. `useradd -D -P` against a disposable prefix
read `SHELL=/usr/bin/fish` from the new defaults. Shelly still flags the two
removed `setcap` commands in the existing patch as dynamic-command warnings.
The updated package has not been rebuilt or published.

Release 2 was built successfully with Shelly's native unprivileged builder after reverting
all of the proposed setcap implementation changes. Source checksums and source
signatures were verified. The build used the declared dependencies, with a
private copy of itstool for the test environment; no host packages were installed.
The upstream test suite was not requested (`--no-check`).

The archive's actual install script and mapping-helper binaries were tested in
a disposable user-namespace root: post-install and post-upgrade both set the
exact capability bytes and mode 0755. Removing CAP_SETFCAP from the installer
caused a reported failure without a setuid fallback. These checks do not replace
a worker-specific nspawn build and functional subordinate-ID mapping test.
