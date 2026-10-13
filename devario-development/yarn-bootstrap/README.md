# yarn-bootstrap

Seed for `../yarn`, which is self-hosting: its `build()` runs yarn, so its `makedepends` name
`yarn` and the worker plan fails with `yarn (not_in_repositories)` until some repository already
publishes that name. This recipe packages upstream's prebuilt release tarball as
`yarn 1.22.22-1`; the real recipe then builds over it as `yarn 1.22.22-2`.

Source signature: `yarn-v1.22.22.tar.gz.asc` from Yarn Packaging <yarn@dan.cx>, fingerprint
72ECF46A56B4AD39C907BBB71646B01B86E50310 (served by dl.yarnpkg.com). Import it as the account
that invokes Shelly before the first build.

Retirement: this recipe publishes under the ALPM name `yarn` itself, and worker removals evict
every repository entry recorded on the removed row, so a Remove run after the real yarn has
published would unpublish the real package too; the first seed removal on 2026-10-13 did exactly
that. A Remove enqueued while the real yarn build is in flight is safe: removals cancel only
jobs keyed to the removed row's own name, the eviction lands within the poll interval, and the
build's later publish re-adds the name; a removal that lands after that final publish evicts it
again. Closed 2026-10-13 this way, with `yarn 1.22.22-2` surviving the seed deletion. Retiring this directory from the tree is just a commit removing it;
published packages outlive their recipes.
