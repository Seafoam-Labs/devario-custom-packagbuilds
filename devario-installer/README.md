# Devario live USB and installer packages

This folder contains the eight OS-owned recipes and their supporting files:

`devario-base` 3-20 requires `pam>=1.7.3-4`. Build and publish
[`devario-core/pam`](../devario-core/pam/PKGBUILD) 1.7.3-4 first, then base, and
rebuild the ISO with both packages staged. PAM ships `deny = 0` in its own
`/etc/security/faillock.conf`, disabling failed-password account lockout.
Existing installations receive the default through `sudo shelly upgrade standard`.
Locally edited configurations retain normal backup handling; merge the `.pacnew`
or set `deny = 0` manually to adopt the default. No reboot is needed.

`devario-base` 3-18 requires `sof-firmware` and `alsa-ucm-conf` to deliver Intel
onboard audio firmware and ALSA use-case configuration to existing installations.
Build and publish this release with both dependencies available in the repository,
then rebuild the ISO. Existing users receive them through
`sudo shelly upgrade standard` and should reboot afterward. Installing both
packages and rebooting resolved missing onboard audio on the ASUS V16 V3607VH.

The current ISO uses the repository's `devario-desktop` and stable
`pearl-greeter`. Desktop recipes are maintained in Aqueous; OS login and GPU
configuration is delivered by `devario-system-integration`. `seafoam-keyring` is retained
for older configurations and is not part of the default ISO build.
Rebuild `devario-base` 3-13, `devario-boot` 1-7, and `devario-keyring`
20260923-3 for the Shelly Devario path profile, RLPM hooks, and all six signed
runtime repositories: core, browser, development, entertainment, gaming, and
utilities. OS login and GPU defaults are owned by the integration package.

Publish `fish` 4.9.3-1 and `shadow` 4.20.0.arch1-3 from `devario-core/`
before rebuilding base. Fish is the default shell for new user accounts;
Shadow supplies the `useradd` default, and the ISO profile configures the
live user and Calamares-created accounts.

| Recipe | Build order |
| --- | --- |
| [devario-filesystem](devario-filesystem/PKGBUILD) | Before devario-base |
| [devario-keyring](devario-keyring/PKGBUILD) | Before devario-base |
| [seafoam-keyring](seafoam-keyring/PKGBUILD) | Legacy; excluded from the default ISO |
| [devario-boot](devario-boot/PKGBUILD) | After devario-dracut; before devario-base |
| [devario-system-integration](devario-system-integration/PKGBUILD) | Publish before Aqueous devario-desktop 1.0.5-2 |
| [devario-base](devario-base/PKGBUILD) | After filesystem, boot, devario-keyring, Fish, and Shadow |
| [ckbcomp](ckbcomp/PKGBUILD) | Before Calamares |
| [calamares](calamares/PKGBUILD) | After ckbcomp and inter-font |

`devario-filesystem` 1-3 is synchronized with the current OS checkout,
including the Devario display name. The integration package supplies eGPU files. Bolt and boltctl are built together by
[`devario-core/bolt`](../devario-core/bolt/PKGBUILD).

The active `devario-desktop` comes from Aqueous's
`packaging/devario/aqueous-desktop/PKGBUILD`; publish all six `1.0.5-2` outputs
after `devario-system-integration` 1-3, with [`rtkit`](../devario-core/rtkit/PKGBUILD) available to deliver
realtime audio support to current desktops. After the one-time integration
adoption described below, existing users can run `sudo shelly upgrade standard` after publication, then reboot. For an
immediate repair, run `sudo shelly install standard rtkit` and reboot.
The [OS recovery instructions](https://github.com/Seafoam-Labs/devario-os#realtime-audio-and-existing-installations)
describe runtime verification. Rebuild the ISO after publication for new installs.

Filesystem release 1-3 supplies `append_path` while loading `/etc/profile.d`
scripts, restoring Perl and Flatpak executable directories to login-session
PATH. Rebuild and publish this package for existing installations and future
ISOs. After upgrading, merge any configuration update for a locally modified
`/etc/profile` and start a fresh login session.

Copy complete recipe directories to a worker. From this repository's root,
review and build a recipe with:

```sh
shelly build --review-only --json ./devario-installer/ckbcomp/PKGBUILD
shelly build --isolated --check ./devario-installer/ckbcomp/PKGBUILD
```

General runtime dependencies remain in `../devario-core/`. The source folder
name does not change the ISO's binary repository: completed signed packages
must still be included in its staged `devario-core` repository with their
dependencies and matching signed metadata.

These recipes are copies of the OS repository's recipes with local packaging
adjustments. The OS repository can also build its own copies using
`scripts/build-packages.sh` or `scripts/build-packages-nspawn.sh`. Its ISO
assembler consumes completed packages. The two sets of recipes do not
automatically synchronize.

See [dependency build notes](../DEPENDENCY-BUILDS.md) for prerequisites and
validation limitations. Shared [provenance](../devario-core/iso-packages-upstream.json)
and [validation records](../devario-core/iso-packages-validation.json) cover both
the runtime recipes and these OS packages.

`devario-boot` 1-7 deploys systemd-boot for installed systems. Calamares now
requires 64-bit UEFI; the live ISO retains BIOS Syslinux support. Build boot
before base, whose 3-12 recipe requires the new boot lifecycle.

Papirus icon defaults are delivered by `papirus-icon-theme` 20260801-2
through GSettings. The ISO overlays supply matching GTK defaults.
Build and publish Papirus before rebuilding the ISO. The existing GLib transaction hook
compiles the new schema override during upgrades. These packages update
existing installations without writing user settings; log out and back in to
refresh running applications. Rebuild the ISO with these packages for new
installations.

`devario-system-integration` 1-3 declares Shelly migrations for the unowned
GPU helpers and desktop configuration left by older ISOs. Deploy Shelly CLI
3.1.9 or later with migration support and RLPM first, then publish integration
before Aqueous's six 1.0.5-2 outputs and rebuild the ISO. Existing installations
follow the [one-time adoption instructions](devario-system-integration/README.md#existing-installations-one-time-adoption):
normal installation adopts unowned files in place without running the old
manual helper. Files owned by another package require a separate ownership
migration. Later updates use normal Shelly upgrades.
