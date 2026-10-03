# Python JSON Schema build chain

Upload the complete recipe directories below to Remora and publish them to
`devario-core` in this order. Refresh the worker database between stages.

| Stage | Recipe directories under `devario-core/` |
| --- | --- |
| 1 | `python-pyproject-hooks`, `python-more-itertools`, `python-platformdirs`, `python-jaraco.context`, `python-autocommand` |
| 2 | `python-jaraco.functools` |
| 3 | `python-jaraco.text` |
| 4 | `python-jaraco.collections` |
| 5 | `python-hatch-fancy-pypi-readme`, `maturin` |
| 6 | `python-attrs`, `python-rpds-py` |
| 7 | `python-referencing` |
| 8 | `python-jsonschema-specifications` |
| 9 | `python-jsonschema` |

Stages 1–4 provide runtime dependencies missing from the already published
`python-build` and `python-setuptools` packages. They install upstream
pure-Python wheels with pinned SHA-256 checksums using `python-installer`.
This avoids requiring setuptools to build its own missing dependencies.
They target Python 3.12 or newer, including the repository's Python 3.14.
`python-jaraco.text` uses 4.0.0, compatible with setuptools, to keep this
bootstrap independent of newer optional CLI tooling.

Stages 5–9 build from pinned source distributions. Rust recipes fetch locked
Cargo dependencies during preparation and build with `--frozen`. `maturin`
packages the standalone build executable; `python-rpds-py` invokes it directly.
The jsonschema check runs its upstream validator unit tests without requiring
the optional format-validation extras.

All recipes include generated `.SRCINFO`. Source/wheel checksum verification,
local package builds, and 303 jsonschema validator tests passed. These local
builds used temporary Python build tools and skipped the installed-package
dependency check; full isolated Remora builds remain to be run after publication.

After building and publishing, install `python-jsonschema` on the ISO builder
and on the host running the nspawn wrappers. Building an archive alone does not
install the Python module on those machines.

The ISO integration also requires the updated installer recipes
`devario-installer/devario-base` (3-10), `devario-installer/devario-boot` (1-6),
and `devario-installer/devario-keyring` (20260923-2).
They use the patched Shelly Devario profile paths, RLPM hooks, and Shelly public
key bundles. See [the full rebuild list](DEPENDENCY-BUILDS.md) for the five
additional core recipes that install hooks and helper scripts.
The current core-only audit also needs `devario-core/nbd` published to core.
