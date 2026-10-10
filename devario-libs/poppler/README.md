# poppler

## Qt build dependency cycle

This recipe builds the core library and GLib, Qt 5, and Qt 6 bindings together,
so both `qt5-base` and `qt6-base` are required build dependencies.
The cycle came from the Qt base recipes' unnecessary `cups` build dependency:

```text
poppler -> qt5-base / qt6-base -> cups -> cups-filters -> libcupsfilters -> poppler
```

The Qt recipes now use their existing `libcups` dependency and explicitly enable
CUPS support. `libcups` supplies `cups/cups.h`, `libcups.so`, and `cups-config`;
the daemon and filters are not needed to compile Qt. This preserves Poppler's
Qt bindings and Qt printing support.

With the other prerequisites available, build/publish `qt5-base` (release 2)
and `qt6-base` (release 3) using the updated recipes, then build Poppler,
`libcupsfilters`, `cups-filters`, and finally `cups`. Provision the client-only
`libcups` package before Qt. Use the updated Qt recipes on the worker; an older
recipe still pulls in the cycle.

The CUPS daemon dependency is declared by the external
[CUPS package](https://archlinux.org/packages/extra/x86_64/cups/).
Qt 5's [pinned CUPS probe](https://invent.kde.org/qt/qt/qtbase/-/blob/fbed962c3195ab3952fa54d40e012ad1a4fdc42b/src/printsupport/configure.json)
only compiles against `cups/cups.h` and links `-lcups`; Qt 6's
[PrintSupport configuration](https://code.qt.io/cgit/qt/qtbase.git/tree/src/printsupport/configure.cmake?h=v6.12.0)
uses CMake's `Cups::Cups` target.

Bash syntax and makepkg/Shelly metadata checks passed for both updated Qt
recipes. The pinned Qt 5 CUPS compile/link probe and a CMake `Cups::Cups`
compile/link probe passed on a host with `libcups` installed and no `cups`
daemon package. Full isolated Qt and Poppler builds have not been run.

## Soname bump on new upstream releases

New upstream releases include a soname bump in `libpoppler.so` (and sometimes in `libpoppler-cpp.so` and / or `libpoppler-glib.so` as well).  
You can run `sogrep` on the built `poppler` package, targeting `libpoppler.so` (same should be done targetting `libpoppler-cpp.so` or `libpoppler-glib.so` if it had a soname bump too), to identify the list of packages to rebuilb against it (e.g. `for repo in core extra; do for lib in $(find-libprovides poppler-24.12.0-1-x86_64.pkg.tar.zst | sed 's/=.*//g'); do sogrep -r $repo libpoppler.so; done; done | sort | uniq`).

Creating ToDos to track those rebuilds (in `staging`) is encouraged. For instance: <https://archlinux.org/todo/poppler-24120/>
