# sudo for Shelly isolated builds

This recipe builds `sudo 1.9.17.p2-7`, based on
[Arch's sudo packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/sudo/-/blob/main/PKGBUILD).
It retains Arch's configuration options, PAM configuration, log-server service,
source checksums, release-signature verification, and configuration backup list.

The packaging change is `make DESTDIR="$pkgdir" INSTALL_OWNER= install`.
Upstream's empty `INSTALL_OWNER` option omits root ownership changes during
staging, allowing Shelly's unprivileged build user to install into `$pkgdir`.
Shelly records root ownership in the package archive. Sudo's mode remains
`4755`, `/etc/sudoers` remains `0440`, and `/etc/sudoers.d` remains `0750`.
No build-time root access or changes to the host's installed sudo are needed.

Upload these three build inputs together into Remora:

- `PKGBUILD`
- `sudo.pam`
- `sudo_logsrvd.service`

Import the bundled public release key as the builder account after checking
its fingerprint against `validpgpkeys`, then build:

```sh
cd sudo
gpg --import 59D1E9CCBA2B376704FDD35BA9F4C021CEA470FB.asc
shelly build --review-only --json ./PKGBUILD
shelly build --isolated --check ./PKGBUILD
```

Validation:

- Source checksums and the upstream release signature verified successfully.
- Shell syntax, `.SRCINFO` generation, and Shelly review passed (no findings).
- Shelly's native unprivileged builder produced the package; upstream reported
  1,536 tests run with zero errors.
- Verified root ownership of all archive entries and the security-sensitive
  modes in both the tar archive and `.MTREE` metadata. Also checked PAM,
  systemd service, tmpfiles configuration, and all four backup declarations.
- `/run/sudo` and the duplicate `sudoers.dist` are omitted as in Arch's recipe.

Full isolated nspawn verification remains unavailable locally because Shelly's
privileged coordinator requires an interactive sudo password. Installed
privilege elevation has not been tested; the checks above cover the build,
upstream regression suite, and package metadata. No host packages were installed.
