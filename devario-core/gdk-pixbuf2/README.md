# gdk-pixbuf image loading in build roots

This recipe builds `gdk-pixbuf2` and `gdk-pixbuf2-docs` 2.44.8-3. It keeps
Arch's option set, imported from
[packaging commit ed98c931](https://gitlab.archlinux.org/archlinux/packaging/packages/gdk-pixbuf2/-/commit/ed98c931304355645634f4a67d5289e9881a8289),
including `-D png=disabled`, `-D jpeg=disabled`, `-D gif=disabled`,
`-D tiff=disabled` and `-D glycin=enabled`. The only local additions are the
`glycin>=2.2.1` version floor (see [../glycin/README.md](../glycin/README.md)),
the `/usr/share/rlpm` hook paths, and the compiled MIME database that `build()`
seeds for itself.

## The package ships no in-process image decoder

Under that option set gdk-pixbuf decodes nothing inside `libgdk_pixbuf-2.0.so`.
Every image format is delegated to glycin, which runs the real decoder in a
separate process. On a gdk-pixbuf2 2.44.8-3 install:

```sh
objdump -p /usr/lib/libgdk_pixbuf-2.0.so.0 | grep NEEDED   # libglycin-2.so.0, no libpng
gdk-pixbuf-query-loaders                                    # header only, zero loader entries
```

`/usr/lib/gdk-pixbuf-2.0/` does not exist at all, because no loader module is
built. The formats come from glycin's registry instead, read from
`/usr/share/glycin-loaders/2+/conf.d/*.conf`, where each entry is keyed by
MIME type and carries its own magic signature, for example
`[loader:image/png]` with `Identifiers=0:\x89PNG\r\n\x1a\n`. The legacy
`loaders.cache` that the shipped hooks maintain therefore has no bearing on
whether images decode.

## Why this matters to recipes

A recipe that decodes an image while compiling depends on that registry being
reachable. `glib-compile-resources` does exactly this: it re-encodes any PNG
or JPEG listed in a `.gresource.xml`, so a build that embeds image resources
fails when the registry comes back empty. gdk-pixbuf reports that case as
`GDK_PIXBUF_ERROR_UNKNOWN_TYPE`, which surfaces as:

```text
failed to load ".../gnome-fs-directory.png": Couldn't recognize the image file format for file ".../gnome-fs-directory.png"
```

The first worker build of [../gtkmm3](../gtkmm3/PKGBUILD) hit this on
`demos/gtk-demo/demo-resources.c` on 2026-10-27, and that recipe now drops the
demo subtree rather than depend on build-time decoding. Expect the same failure
in any recipe that compiles gresources containing images.

## What was ruled out on a host install

Checked on a working Devario host, where the same stack decodes PNG correctly:

- The MIME database. Isolated roots do not run `30-update-mime-database.hook`,
  and `mime.cache` is generated rather than owned by a package. Rebinding
  `/usr/share/mime` to a tree that holds only `packages/freedesktop.org.xml`
  still decoded the PNG, because glycin's own `Identifiers` magic does the
  format sniffing.
- A blocked nested sandbox. Running the compile under
  `bwrap --unshare-user --disable-userns` still decoded the PNG.
- A bad source blob. `gnome-fs-directory.png` at gtkmm tag `3.24.11` is a
  valid 2044-byte 48x48 RGBA PNG.

The failure reproduces on demand by hiding glycin's registry from the data
dirs, which is the closest known analogue to the worker's environment:

```sh
XDG_DATA_DIRS=/build/work/only python3 -c '
import gi; gi.require_version("GdkPixbuf", "2.0")
from gi.repository import GdkPixbuf
GdkPixbuf.Pixbuf.new_from_file("/usr/share/icons/Adwaita/16x16/mimetypes/font-x-generic.png")'
```

This raises the same `Couldn't recognize the image file format` message. The
worker's exact trigger is still unconfirmed: `/etc/shellybuild.conf` carries no
`XDG_DATA_DIRS`, and the gtkmm3 job log prints no environment dump, so nothing
yet proves the isolated root sets it.

## If build-time decoding has to work

Two options, both needing a fresh isolated root to prove out:

1. Rebuild gdk-pixbuf2 with `-D png=enabled` and `-D jpeg=enabled` so the
   legacy loaders are compiled in and no child process is involved. This
   deviates from Arch's option set for a core library, so it needs a
   comment naming the mechanism.
2. Give the build root a reachable glycin registry, by confirming what the
   worker exports over `XDG_DATA_DIRS` and either clearing it or including
   `/usr/share`.

Before either one, re-check the registry from inside the root:

```sh
gdk-pixbuf-query-loaders | wc -l
ls /usr/share/glycin-loaders/2+/conf.d/
echo "$XDG_DATA_DIRS"
```

## Validation

Metadata and hooks follow the pinned Arch revision; nothing here was verified
by an isolated build on the worker. The decoder findings above come from host
inspection of the published `gdk-pixbuf2-2.44.8-3` and `glycin-2.2.1-1`, plus
the reproduction commands in this file.
