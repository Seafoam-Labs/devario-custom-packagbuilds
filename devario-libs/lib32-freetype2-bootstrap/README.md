# lib32-freetype2-bootstrap

Seed for `../lib32-freetype2`, one side of a four-package cycle: `lib32-freetype2` makedepends on
`lib32-harfbuzz`, `lib32-harfbuzz` makedepends on `lib32-freetype2` and `lib32-cairo`, and
`lib32-cairo` depends on `lib32-fontconfig` and `lib32-freetype2`, so the worker plan cannot
provision any of the four while none is published. This recipe builds the real source with
harfbuzz support disabled and publishes it as `lib32-freetype2 2.14.3-1.1`; `lib32-fontconfig`,
`lib32-cairo` and `lib32-harfbuzz` then build over it, and the real recipe follows at `2.14.3-2`.

Deviations from the mirrored recipe, limited to the cycle leg: `lib32-harfbuzz` is dropped from
`makedepends` and `-D harfbuzz=dynamic` becomes `-D harfbuzz=disabled`, losing only the
optdepend-level improved autohinting, and `lib32-gcc-libs` joins `makedepends` because Shelly
isolated roots carry no 32-bit libgcc. Nothing outside the cycle should build against this seed.

Source verification: `freetype-$pkgver.tar.xz.sig`, key Werner Lemberg
E30674707856409FF1948010BE6C3AAC63AD8E3F. Import it as the account that invokes Shelly before
the first build.

Retirement: this recipe publishes under the ALPM name `lib32-freetype2` itself, and worker
removals evict every repository entry recorded on the removed row, so a Remove against this
recipe after the real freetype2 has published would unpublish the real package. A Remove
enqueued while the real build is in flight is safe: removals cancel only jobs keyed to the
removed row's own name, the eviction lands within the poll interval, and the build's later
publish re-adds the name; a removal that lands after that final publish evicts it again.
Removing the seed before fontconfig, cairo and harfbuzz have built only re-breaks the cycle.
Retire the directory instead, which is just a commit removing it; published packages outlive
their recipes.
