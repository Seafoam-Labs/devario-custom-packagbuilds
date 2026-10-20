# dart-bootstrap

Seed for `../dart`, which is self-hosting: its `makedepends` names `dart` and `build()` runs the
Dart SDK, so the worker plan fails with `dart (not_in_repositories)` until some repository already
publishes that name. This recipe packages upstream's prebuilt stable SDK zip as `dart 3.13.5-1`;
the real recipe then builds over it as `dart 3.13.5-2`.

The archive's sha256 is taken from the bucket's own `dartsdk-linux-x64-release.zip.sha256sum` and
recorded in `provenance.json`; Dart publishes an in-toto attestation for the asset but no detached
GPG signature.

Retirement: this recipe publishes under the ALPM name `dart` itself, and worker removals evict
every repository entry recorded on the removed row, so a Remove run after the real dart has
published would unpublish the real package too. Retire the directory only while the real build is
in flight, or after confirming the removal rule has changed.