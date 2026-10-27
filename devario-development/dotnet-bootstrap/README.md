# dotnet-bootstrap

Seed for `../dotnet`, which builds .NET from source. Since .NET 10 a source build produces the
shared components (runtime, aspnetcore) only on the 1xx feature band: `Directory.Build.props` sets
`DotNetBuildSharedComponents=true` when `VersionSDKMinor` is 1. A checkout from any later band does
not build them and `eng/init-source-only.proj` aborts with
`Shared components must be provided as input to a build which does not produce shared components.`
unless it is handed the 1xx output first. `prep-source-build.sh` on the `release/10.0.4xx` tags does
no such download, so this seed carries that input: it repackages upstream's previously source-built
1xx archive as `dotnet-bootstrap 10.0.114-1` and `../dotnet` links it into the build.

Coexistence is deliberate. The seed keeps its own ALPM name, so it holds its own repository row and a
worker Remove run cannot evict the real dotnet packages. It ships one archive under
`/opt/dotnet-bootstrap` and nothing in `/usr/bin`, while the dotnet splits own `/usr/share/dotnet`
and `/usr/bin/dotnet`; no path is shared and the recipe declares no `provides`, `conflicts` or
`replaces`, so the seed can never satisfy a dependency meant for `dotnet-sdk`.

## How the version is chosen

The archive name is *not* this recipe's `pkgver`, it is the version the dotnet checkout demands:
`MicrosoftNETSdkPackageVersion` from that tree's `eng/Version.Details.props`
(`10.0.114-servicing.26522.126` for tag `v10.0.403`). `pkgver` carries only the band version because
ALPM reserves `-` for the `pkgver`-`pkgrel` separator, so `_sbver` holds the full string and the two
must be bumped together. `../dotnet`'s `prepare()` globs the exact `_sbver` out of the checkout and
stops with a named error when no installed seed matches, which is the signal to publish a newer seed.

Upstream names this asset `Private.SourceBuilt.Artifacts.*`, the same base name the band's own
bootstrap download uses, so it is stored under the `Private.SourceBuilt.SharedComponents` prefix that
`eng/VmrLayout.props` points `ExternalTarballsDir` at. That rename is upstream's own trick: their
`vmr-build.yml` and main's `prep-source-build.sh` fetch the 1xx artifacts archive and hand it over
under this prefix. Keeping the archive packed (`noextract`) is intentional; `init-source-only.proj`
untars it itself.

That untar is where the `release/10.0.4xx` tags fail: `eng/init-source-only.proj` repeats the
`SharedComponentsPrereqsArchivePathItem` glob that `eng/VmrLayout.props` already declares, so
`@(SharedComponentsPrereqsArchivePathItem)` expands to `"<archive>;<archive>"` and the unquoted `tar`
in `UnpackSharedComponentsPrereqsArchive` runs the archive as a command (exit 126). main removed the
duplicate declaration, and `../dotnet` backports that removal plus main's multi-match guard as
`dotnet-init-source-only-shared-components-glob.patch`, so the seed reaches the target as one path.
The archive is the input that target expects: listed over the full 1387301805-byte download, it is a
flat feed of 363 nupkgs with `PackageVersions.props` and `VerticalManifest.xml` at the root, which the
`--exclude='assets'` unpack puts in `prereqs/packages/shared-components`, plus
`assets/Release/dotnet-symbols-all-10.0.114-servicing.26522.126-centos.10-x64.tar.gz` for the symbols
step that follows it.

## Provenance

The sha512 is taken from the feed's own `.sha512` sidecar and recorded in `provenance.json`, and was
recomputed over the full 1387301805-byte download on 2026-10-27. Microsoft publishes no detached
signature for `source-build` assets, so there is no `validpgpkeys` to add here, unlike
`../jdk-bootstrap`. The archive is a flat NuGet feed plus `PackageVersions.props` and an `assets`
tree; it carries no license file, so the MIT term comes from the source-build repository, as it does
for `../dotnet`.

## Maintenance

`../dotnet` needs this package present for every band rebuild, so it stays published rather than
being retired. Bump it whenever a dotnet bump moves `MicrosoftNETSdkPackageVersion`: set `_sbver` to
that value, raise `pkgver` to its band version or `pkgrel` when only the servicing build id moved,
refresh `sha512sums` from the new sidecar, and publish this seed **before** queueing `../dotnet`,
because makedepends resolve from published repositories rather than from this directory tree.
