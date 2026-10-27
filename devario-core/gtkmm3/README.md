# gtkmm3

Builds `gtkmm3` and `gtkmm3-docs` 3.24.11-2 from the tagged Git sources, and
pins the GTK3-era ABI that the bare `gtkmm3` name carries in `devario-core`:
`libgtkmm-3.0.so=1-64` and `libgdkmm-3.0.so=1-64`, checked in `package()`
against the real ELF64 SONAMEs so a future version refresh cannot advertise an
incompatible ABI under this name. The depends list matches the published
`3.24.11-1` `.PKGINFO` verbatim.

It exists because `gparted` needs `pangomm` plus `libpangomm-1.4.so`, and the
bare `pangomm` name was refreshed to the 2.48 ABI on 2026-10-27.
[../pangomm/PKGBUILD](../pangomm/PKGBUILD) carries the `epoch=1` supersede that
restores `1:2.46.5-1` under the bare name, and the repository now publishes
`pangomm 1:2.46.5-1` with `pangomm-docs 1:2.46.5-1`.

## Local deviation: the demo subtree is not built

`prepare()` deletes `subdir('demos/gtk-demo')` from `meson.build`. The reason is
the worker log for attempt 1 on 2026-10-27: after all dependencies resolved and
294 packages installed, the build reached target 278 and died in
`glib-compile-resources`, which could not decode a demo PNG:

```text
FAILED: [code=1] demos/gtk-demo/demo-resources.c
failed to load ".../demos/gtk-demo/gnome-fs-directory.png": Couldn't recognize the image file format for file "..."
```

That is a gdk-pixbuf problem, not a gtkmm one: gdk-pixbuf2 2.44 has no
in-process image decoder and delegates all decoding to glycin's registry, which
is not reachable from an isolated build root. The canonical writeup, including
what was ruled out and how to re-check it from inside a root, is in
[../gdk-pixbuf2/README.md](../gdk-pixbuf2/README.md).

Two notes for whoever revisits this:

- `-D build-demos=false` does not avoid the failure. In
  `demos/gtk-demo/meson.build` that option only gates `build_by_default` on the
  executable; `gnome.compile_resources()` is guarded solely by
  `epoxy_dep.found()`, so meson still generates and compiles
  `demo-resources.c`. Verified with meson 1.12.1, matching the worker's version.
- Dropping the subtree changes no package content. Both demo targets are
  declared `install: false`, and the published `gtkmm3 3.24.11-1` file list
  contains no demo or example paths. The `docs/reference` subtree does not read
  the demos directory.

`prepare()` greps for the exact anchor before deleting it and returns non-zero
if it is missing, so a version refresh that moves or drops that line fails here
instead of silently rebuilding the demos.

## Validation

The recipe change is static: no package was built on the worker after the edit.
The `pkgrel=2` revision has not been published yet (the repository still serves
`3.24.11-1`), so this fix rides into that same revision without another bump.
`.SRCINFO` is unchanged, since only the `prepare()` body moved.
