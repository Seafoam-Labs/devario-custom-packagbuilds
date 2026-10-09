# Native Devario compatibility audit

The subsequent [hook audit](HOOK-BUILDS.md) checks the full recipe tree against
`devario-os`, fixes two older hook recipes, and aligns TeX Live's hook metadata
paths with Devario.

This follow-up audits the 908 recipes in the application expansion. It corrects
21 recipe bases that still inherited distribution integration from upstream
packaging. Devario uses compatible package formats while retaining its own
identity, repository configuration, and Shelly/RLPM integration.

## Corrections

- Java uses `devario-java` in native installation hooks. All six OpenJDK recipes
  require `java-runtime-common>=3-7`, which supplies that helper. An
  `archlinux-java` symlink remains for externally built compatible packages.
  Java builds identify their vendor as Devario.
- Vim installs `devario.vim`. Vim, cdrtools, SeaBIOS, TeX Live, and the 32-bit
  libtasn1 build identify Devario as their packager. The 32-bit systemd fallback
  hostname is `devario`; dpkg origin metadata and LSB identification use Devario.
  Flite's distribution voice configuration is named `devario`.
- gRPC reads protobuf's version through pkg-config. VTK reads fast_float's
  installed CMake version metadata. Neither invokes `pacman` during the build.
- Reflector is patched to consume the Devario repository catalog at
  `https://repo.seafoam-labs.org/api/v1/repositories`. It emits native
  `$repo/$arch` server paths, rates the Devario core database, and its service
  writes `/etc/shelly.d/mirrorlist`. It does not write Shelly's main configuration.
- The native and Steam Linux Runtime CachyOS Proton variants retain distinct
  installation directories without inheriting a `replaces=proton-cachyos`
  migration rule.

Reflector accepts only catalog roots advertising all listed Devario repositories
for its shared mirrorlist. Catalog indexing dates are used for age sorting;
they are not measured mirror synchronization or health statistics. Geographic,
IP, ISO, delay, and health filters are rejected because the catalog does not
provide those measurements. Rate sorting performs an actual database download.
To use the generated list, an administrator can add
`Include = /etc/shelly.d/mirrorlist` to the intended Devario repository sections.
Existing direct server settings are not changed by this package.

The [adaptation log](audits/application-expansion-2026-10-08/adaptations.json)
and [native audit report](audits/application-expansion-2026-10-08/native-compatibility-audit.json)
record the affected recipes. Changed recipes have updated release numbers,
bundled-source checksums, and `.SRCINFO` metadata.

## Conflicting alternatives

The source set contains **21 declared conflict pairs** whose current versions
are mutually exclusive. See
[package-alternatives.json](audits/application-expansion-2026-10-08/package-alternatives.json).
These are installation choices, including:

- JDK, JRE, and headless JRE outputs for the same Java version;
- Vim and GVim;
- current and LTS Node.js versions;
- Qt 5 and Qt 6 Lazarus variants;
- CPU and CUDA OpenCV variants.

Publish matching split outputs as appropriate, but install only one conflicting
alternative in an installation or build root. Removing their conflict entries
would hide overlapping files. Separate isolated build roots also allow
applications to use different build-time Node.js or Java versions.

## Retained references and validation

Upstream source URLs, public signing keys, copyright and author attribution,
patch history, and provenance are retained. Some preparation commands contain
old distribution paths as the text they replace. CachyOS product names remain
because those specific variants were requested. These references do not select
Arch repositories or require an Arch installation.

All 908 recipes pass metadata comparison, shell syntax, and Shelly review
parsing; all 564 bundled-source checksum checks pass. Required dependency
resolution remains complete against the saved Devario repository snapshot.
Seven native Java/Reflector fixture tests pass, and Reflector's actual
`prepare()`, wheel build, and `package()` were exercised in temporary staging
directories. No host configuration was changed.

To repeat the native fixtures with the checksum-pinned upstream archive:

```sh
DEVARIO_REFLECTOR_ARCHIVE=/path/to/reflector-2023.tar.xz \
  python tests/test-native-package-adaptations.py
```

This audit covers the expansion manifest, not unrelated existing recipes or
every file in remote upstream source trees. Full isolated compilation and
installation tests remain necessary to establish binary file ownership and
ABI compatibility. Static metadata alone cannot guarantee zero installation
conflicts.
