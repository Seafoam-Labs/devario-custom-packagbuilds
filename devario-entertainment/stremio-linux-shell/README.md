# stremio-linux-shell

`stremio-linux-shell` packages the GTK4/WebKitGTK Stremio client. The recipe is
adapted from the AUR `stremio-linux-shell` recipe, with the schema, man page,
translation and dependency handling from the AUR `stremio-linux-shell-git`
recipe; see `DEVARIO-UPSTREAM.json` for the pinned AUR revisions.

## What the package installs

```
/usr/bin/stremio                                      launcher
/usr/lib/stremio/stremio                              private GTK4 binary
/usr/lib/stremio/server.js                            upstream streaming server
/usr/share/applications/com.stremio.Stremio.desktop
/usr/share/dbus-1/services/com.stremio.Stremio.service
/usr/share/glib-2.0/schemas/com.stremio.Stremio.gschema.xml
/usr/share/icons/hicolor/scalable/apps/com.stremio.Stremio.svg
/usr/share/metainfo/com.stremio.Stremio.metainfo.xml
/usr/share/man/man1/stremio.1
/usr/share/locale/{es,fr}/LC_MESSAGES/stremio.mo
/usr/share/licenses/stremio-linux-shell/
```

The launcher sets `SERVER_PATH` for the streaming server, `ANV_DEBUG` for Intel
Vulkan video acceleration, and prepends `/usr/bin` to `PATH` so D-Bus activation
always finds the packaged `node`. The 1.3.0 binary already selects the GL GSK
renderer and sets `LC_NUMERIC=C` before creating mpv, so the AUR's
`glxinfo`/`GSK_RENDERER` workaround and `mesa-utils` dependency are not needed.

The desktop entry keeps `DBusActivatable=true`; the packaged D-Bus service
points it at `/usr/bin/stremio --gapplication-service`, which the binary
forwards through clap's trailing arguments. This preserves single-instance and
URI handling without a service file missing.

## Licensing of `server.js`

The Rust shell is GPL-3.0-only. `data/server.js` is proprietary, closed-source
software of Stremio. Upstream ships it inside the official Stremio
applications and does not publish a license text for it: the file's header
refers to a `server.js.LICENSE.txt` that is not in the release tarball.
Redistribution terms remain unresolved as of 2026-11-27
([upstream issue](https://github.com/Stremio/stremio-linux-shell/issues/100)).
The package declares `LicenseRef-Stremio` and installs the notice
`LicenseRef-Stremio` beside the GPL license.

## Build and install

From this directory:

```sh
shelly build --reviewed ./PKGBUILD
shelly install standard ./stremio-linux-shell-*.pkg.tar.zst
```

`prepare()` runs `cargo fetch --locked`, so the Cargo registry and the pinned
`libmpv2` git dependency must be reachable. The build then runs frozen with
Cargo state under `$srcdir`.

## Updating

1. Set `pkgver` to the upstream tag without its `v`, and reset `pkgrel`. If a
   prerelease tag contains a hyphen, pkgver uses an underscore
   (`1.4.0-beta.1` -> `1.4.0_beta.1`); `_tag` maps it back for the URL.
2. Refresh the checksums and `.SRCINFO`:
   `printf 'y\n' | shelly build --updpkgsums PKGBUILD`. Shelly refreshes the
   remote tarball checksum but leaves the local source entries as they are, so
   run `sha256sum stremio.sh LicenseRef-Stremio` and update those two entries
   by hand if either file changed.
3. Re-run the check phase and review the package before publishing.
