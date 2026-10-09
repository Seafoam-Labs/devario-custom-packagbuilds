# Application package expansion — 2026-10-08

The follow-up [native compatibility audit](NATIVE-COMPATIBILITY.md) corrects
remaining distribution assumptions and documents mutually exclusive outputs.

The 114 packages in the edited `suggested-devario-repositories.txt` are covered
by 112 application recipe bases. Together with missing runtime and build
dependencies, the expansion uses **908 recipe directories: 896 new and 12
existing**. Each directory contains its PKGBUILD, generated `.SRCINFO`, and
upstream supporting files. Split packages share their upstream recipe directory.

Start with these manifests:

- [Builder order in 28 stages](BUILDER-ORDER.md), including cycle and self-hosted seed requirements
- [Requested packages and their directories](audits/application-expansion-2026-10-08/requested-packages.tsv)
- [All selected recipes and placement reasons](audits/application-expansion-2026-10-08/dependency-recipes.tsv)
- [Dependency-first build groups](audits/application-expansion-2026-10-08/build-order.tsv)
- [Bootstrap cycles](audits/application-expansion-2026-10-08/build-cycles.json)
- [Machine-readable summary](audits/application-expansion-2026-10-08/summary.json)

## Repository placement and coverage

Requested applications retain the repository assignments in the user's edited
list. Shared libraries, language modules, and runtime resources go in
`devario-libs`; compiler and build tools go in `devario-development`; supporting
system programs go in `devario-utilities`. Required core runtime chains stay in
`devario-core`. Existing recipes retain their established locations.

| Repository | Selected recipe directories |
| --- | ---: |
| devario-browser | 1 |
| devario-core | 21 |
| devario-development | 173 |
| devario-entertainment | 6 |
| devario-gaming | 16 |
| devario-libs | 604 |
| devario-productivity | 2 |
| devario-utilities | 85 |

Availability was checked against all ten published Devario repository databases
in the retrieved catalog, including `devario-scx-dev`. The
[snapshot](audits/application-expansion-2026-10-08/repository-snapshot.json)
records versions, providers, runtime dependencies, and database hashes. The
[resolution report](audits/application-expansion-2026-10-08/dependency-resolution.json)
records selected source dependencies and published providers. It has no
unresolved required runtime or build dependencies for that snapshot.

Resolution includes `depends`, `makedepends`, runtime dependencies of sibling
split outputs, and runtime chains through already-published packages. This
accounts for the large source set: Java, QEMU, Wine/Proton, NVIDIA settings,
scientific Python, and LLVM introduce substantial build toolchains.

Test-only and optional dependencies are recorded in
[test-dependencies.tsv](audits/application-expansion-2026-10-08/test-dependencies.tsv)
and [optional-dependencies.tsv](audits/application-expansion-2026-10-08/optional-dependencies.tsv).
They are **not recursively added** solely for tests or optional features.
Upstream `checkdepends` and `check()` declarations are retained. Use `--no-check`
for this build plan; enabling checks can require additional recipes.

## Building

Upload or copy each **complete recipe directory**, including patches, install
scripts, configuration files, icons, and `keys/pgp` where supplied. Build each
split recipe once and publish its matching outputs together. For example,
`ollama` also produces `ollama-cuda`, and `virt-manager` produces `virt-install`.
The requested-package manifest maps output names to their source directories.

From this repository, review and then build a selected recipe with Shelly:

```sh
shelly build --review-only --json devario-utilities/7zip/PKGBUILD
shelly build --isolated --no-check devario-utilities/7zip/PKGBUILD
```

Process `build-order.tsv` in increasing group order, making built dependencies
available to the isolated builder before their consumers. The **15 groups
marked `cyclic_group=yes` require bootstrap packages or staged builds**; their
members cannot simply be built sequentially from an empty repository. The cycle
report identifies each group, including MinGW, RISC-V GCC/glibc, Qt 5, OCaml,
and several 32-bit library groups. This is a dependency ordering report, not an
automated bootstrap implementation.

The [stage plan](BUILDER-ORDER.md) also flags 10 additional single-recipe
bootstrap groups, such as Java and Free Pascal, that require an existing tool
to build themselves. Use that plan for the complete queue and seed requirements.

## Devario adaptations

The [adaptation log](audits/application-expansion-2026-10-08/adaptations.json)
records changes beyond importing upstream recipes. These include RLPM hook
paths, removal of obsolete upstream migration notices, explicit dependency
metadata for split packages, and dependency-array syntax supported by Shelly.
`rebuild-detector` uses a private read-only Shelly metadata adapter. The existing
native `maturin` recipe now also supplies its matching `python-maturin` wheel.
Missing support files were restored for the unchanged existing JDK recipe.

Imported recipes carry `DEVARIO-UPSTREAM.json` with available source archive
hashes and Git revision information. The aggregate
[recipe manifest](audits/application-expansion-2026-10-08/recipes.json) records
provenance, outputs, and PKGBUILD hashes. VCS recipes retain upstream VCS source
tracking, so their future builds can use newer source revisions.

## Validation and limits

All 908 recipes passed Bash syntax checks, fresh `.SRCINFO` comparison, and
Shelly review parsing. All 564 checked bundled-source checksums matched.
The rebuild-detector adapter passed nine fixture tests. Repeat these checks:

```sh
python audits/application-expansion-2026-10-08/validate-recipes.py
python tests/test-rebuild-detector.py
```

[validation.json](audits/application-expansion-2026-10-08/validation.json)
retains Shelly's static findings; successful parsing does not mean zero
warnings. Findings include upstream dynamic commands, Makefile and configure
macros inside patches, a PNG icon, and printed service-enablement instructions.
These still need the normal recipe review when building.

Full isolated compilation, remote source checksum/signature verification,
installation, and repository publication have **not** been performed. Required
dependency resolution is a metadata check against the recorded snapshot;
compilation and ABI compatibility still need verification during builds.
