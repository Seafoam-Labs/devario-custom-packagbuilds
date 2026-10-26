# dart-bootstrap

Seed for `../dart`, which is self-hosting: its `build()` runs the Dart SDK, so the worker plan
fails with `dart (not_in_repositories)` until a repository already publishes a compiler. This
recipe packages upstream's prebuilt stable SDK zip as `dart-bootstrap 3.13.5-1`, and the real
recipe builds over it as `dart 3.13.5-2`.

Coexistence is deliberate. The seed keeps its own ALPM name, so it holds its own repository row
and a worker Remove run can no longer evict the real dart, which is what publishing under the name
`dart` used to risk. It installs the SDK tree into `/opt/dart-bootstrap-sdk` and ships nothing in
`/usr/bin`, while the real package owns `/opt/dart-sdk` and `/usr/bin/{dart,dartaotruntime}`; no
path is shared, and neither recipe declares `provides`, `conflicts` or `replaces`, so both install
side by side. `../dart` names `dart-bootstrap` in `makedepends` and prepends
`/opt/dart-bootstrap-sdk/bin` to `PATH` in `prepare()` and `build()` to reach the seed.

Keeping the seed out of `provides` is what makes `dart` unambiguous downstream: every package that
depends on `dart` resolves to the source-built SDK, never to this seed.

The archive's sha256 is taken from the bucket's own `dartsdk-linux-x64-release.zip.sha256sum` and
recorded in `provenance.json`; Dart publishes an in-toto attestation for the asset but no detached
GPG signature.

Maintenance: `../dart` needs this package present for every rebuild, so it stays published rather
than being retired. Bump it alongside `../dart`'s `pkgver`, pinning the seed to the preceding
stable release so the seed is always older than what it bootstraps.