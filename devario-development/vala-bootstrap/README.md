# vala-bootstrap

Seed for `../vala`, which is self-hosting: it builds from a signed git tag, so its `makedepends` name
`vala` and the worker plan fails with `vala (not_in_repositories)` until some repository already
publishes that name. This recipe packages upstream's dist tarball, which ships the valac-generated C
and a ready `configure`, as `vala 0.56.19-1`; the real recipe then builds over it as `vala 0.56.19-2`.

Source verification: GNOME publishes neither a detached signature nor a checksum file for vala
tarballs, so the source is pinned only by the sums recorded in the PKGBUILD and in `provenance.json`.
There is no key to import.

Retirement: this recipe publishes under the ALPM name `vala` itself, and worker removals evict every
repository entry recorded on the removed row, so a Remove against this recipe after the real vala has
published would unpublish the real package. A Remove enqueued while the real vala build is in flight is
safe: removals cancel only jobs keyed to the removed row's own name, the eviction lands within the poll
interval, and the build's later publish re-adds the name; a removal that lands after that final publish
evicts it again. Removing the seed before queueing the real build only re-breaks the plan. Retire the
directory instead, which is just a commit removing it; published packages outlive their recipes.
