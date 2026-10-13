# Devario Plymouth theme

Displays the supplied seafoam-and-blue fish with DEVARIO lettering, centered
on black, without a spinner, progress bar or animation. The PNG is copied
unchanged from the replacement image supplied on 2026-10-13. Plymouth scales
it at runtime, preserving its aspect ratio, to at most 420 logical pixels wide
and 40% of the display height.

White text appears only for password prompts, questions and boot messages.
Passwords are masked; an empty field shows an underscore. The script handles
both the traditional password/question callbacks and the unified prompt API.
Display changes trigger layout updates without animating the logo.

Code is GPL-3.0-or-later. The original Devario artwork is CC-BY-SA-4.0 under
the source repository's default artwork license, reproduced in
`ARTWORK-LICENSE.md`; attribution is to the Devario contributors. The original
trademark notice is preserved in `TRADEMARKS.md`. The PNG has not been edited.

## Build

Build and publish `devario-core/plymouth` first, then refresh the worker's
repository metadata. From the repository root:

```sh
shelly build --isolated --check ./devario-core/devario-plymouth-theme/PKGBUILD
```

The theme package installs only assets and licensing notices. It neither owns
`/etc/plymouth/plymouthd.conf` nor changes an administrator's selected theme.

Shelly's current text scanner reports the local PNG as a critical
`<local-binary>` finding and Markdown backticks in `ARTWORK-LICENSE.md` as
dynamic commands. These findings refer to data files: `package()` copies them
with `install -m644` and never executes or sources them. The PNG was visually
inspected and its SHA-256 matches the supplied replacement PNG exactly:
`21dcc8a853a546bdd989005c7bebdc2df2f39046e39f2d275d39d78f8f02c7b8`.
Review these files through the worker's normal package-review process before
its isolated build; they are intentionally retained unchanged.

## Enable in Devario OS

1. Add `plymouth` and `devario-plymouth-theme` to `iso/packages.x86_64` and the
   repository seed list. Publish both packages before building the ISO.
2. In the image overlay, set `/etc/plymouth/plymouthd.conf` to:

   ```ini
   [Daemon]
   Theme=devario
   ```

3. Append `add_dracutmodules+=" plymouth "` to both `live.conf` and
   `installed.conf` in `packages/devario-boot`, then update that package's
   checksums, metadata and release. Devario passes an empty `--confdir` to
   dracut, so `/etc/dracut.conf.d/` alone does not configure its image builder.
4. Add `splash` alongside `quiet` in the installed kernel-command-line
   generator. Add `quiet splash` to the live ISO GRUB kernel command line.
5. Rebuild the boot package and ISO. Check the greeter handoff and encrypted
   installation unlock on real hardware. Keep a boot entry without `splash`,
   with `plymouth.enable=0 rd.plymouth=0`, for affected devices; do not disable
   graphics modesetting just to bypass the splash.

On an installed Devario system with those boot changes deployed, select and
rebuild with:

```sh
sudo plymouth-set-default-theme devario
sudo /usr/lib/devario/boot-update
```

The modified Plymouth package also routes `plymouth-set-default-theme -R`
through the same Devario helper. No host boot settings are changed by building
either package.

## Validate without booting

`test-theme.sh` uses a compiled Plymouth source/build tree to execute the real
script engine and PNG/Pango renderers, without root, a display server or a GPU.
It redirects the label module lookup to that build tree and supplies synthetic
display dimensions; it does not simulate the DRM driver or systemd startup.

```sh
bash ./devario-core/devario-plymouth-theme/test-theme.sh \
  /path/to/plymouth/src/plymouth-26.134.222 \
  /path/to/plymouth/src/build \
  /tmp/devario-theme-validation
```

The harness checks the static logo across repeated refreshes, masked password
callbacks, questions, message hiding, and layouts at 640x480, 800x1280,
3840x2160 and 320x240. It renders `normal.png` and `password.png` in the output
directory. It requires the normal C toolchain and libpng, already used to
build Plymouth.

Validation: the native theme package build and scripting-engine checks passed.
Preview images were inspected. These checks do not establish compatibility
with the devices previously affected by Plymouth graphics issues.
