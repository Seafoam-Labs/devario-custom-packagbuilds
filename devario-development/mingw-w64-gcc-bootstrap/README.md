# mingw-w64-gcc-bootstrap

Seed for `../mingw-w64-gcc`, which is one side of a cycle: it depends on `mingw-w64-crt` and
`mingw-w64-winpthreads`, and both of those name `mingw-w64-gcc` in `makedepends`, so the worker plan
cannot provision any of the three while none is published. This recipe builds the stage-1 cross
compiler and publishes it as `mingw-w64-gcc 16.2.0-1`; crt and winpthreads then build over it, and
the real recipe follows at `16.2.0-2`.

Stage 1 follows the documented mingw-w64 bootstrap order: build `all-gcc` and `all-target-libgcc`
only, then crt, then winpthreads, then the full compiler. `mingw-w64-crt`'s configure runs
`AC_NO_EXECUTABLES`, so a compiler that cannot yet link executables is enough to build it; the
installed libgcc covers the winpthreads DLL link once crt is in place.

The stage-1 compiler is compile-only for target code. Nothing outside this cycle should build
against it, and it must not stay published.

Source verification: GNU's `gcc-16.2.0.tar.xz.sig`, keys in `keys/pgp/` (Jakub Jelinek
D3A93CAD751C2AF4F8C7AD516C35B99309B5FA62, Richard Guenther
13975A70E63C361C73AE69EF6EEB81F8981C74C7). Import them as the account that invokes Shelly before
the first build.

Retirement: this recipe publishes under the ALPM name `mingw-w64-gcc` itself, and worker removals
evict every repository entry recorded on the removed row, so a Remove against this recipe after the
real gcc has published would unpublish the real package. A Remove enqueued while the real build is
in flight is safe: removals cancel only jobs keyed to the removed row's own name, the eviction lands
within the poll interval, and the build's later publish re-adds the name; a removal that lands after
that final publish evicts it again. Removing the seed before crt and winpthreads have built only
re-breaks the cycle. Retire the directory instead, which is just a commit removing it; published
packages outlive their recipes.
