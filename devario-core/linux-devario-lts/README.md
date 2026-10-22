# linux-devario-lts — Devario kernel (6.18 LTS)

The long-term-support kernel package. This track follows the 6.18 LTS series and is intended for systems that prefer a longer-lived kernel branch.

This directory contains the `PKGBUILD` and a versioned `config`. Devario builds
its own kernel packages from [Seafoam Labs' Linux source tree](https://github.com/Seafoam-Labs/linux).
The release source archives use the `devario-<version>-<N>` naming scheme.
Devario distributes and signs its own packages.

## Packages

The recipe produces:

- `linux-devario-lts` — kernel image and modules;
- `linux-devario-lts-headers` — headers and build files for external modules;
- `linux-devario-lts-dbg` — optional, unstripped `vmlinux` when `_build_debug=yes`.

## Default configuration

Official Devario builds target **x86-64-v3** (`_processor_opt=generic_v3`).
A compatible CPU is required to run the distributed kernel; `native` is only
appropriate for an individual local build, not a public package.

The defaults below come from `_release_opts` in `PKGBUILD`:

| Option | Default | Purpose |
| --- | --- | --- |
| `_processor_opt` | `generic_v3` | CPU ISA target (`generic_v1`, `generic_v2`, `generic_v3`, `native`). |
| `_HZ_ticks` | `1000` | Timer frequency; accepted values: 100, 250, 300, 500, 1000. |
| `_tickrate` | `full` | `periodic`, `idle`, or `full` tick configuration. |
| `_preempt` | `full` | Preemption mode: full, lazy, voluntary, none. |
| `_hugepage` | `always` | Default transparent hugepage policy (`always`, `madvise`). |
| `_cc_harder` | `yes` | Enable kernel `-O3` optimization. |
| `_per_gov` | `no` | Do not select `performance` in place of `schedutil` as the default governor. |
| `_localmodcfg` | `no` | Do not restrict the module set using `modprobed-db`. |
| `_use_current` | `no` | Start from the shipped `config`, not `/proc/config.gz`. |
| `_makenconfig` / `_makexconfig` | `no` / `no` | Disable interactive configuration frontends. |
| `_build_debug` | `no` | Do not produce the optional debug package. |
| `_rebuild` | `1` | Initial Devario rebuild number for a source tag. |

The definitive supported options and values are those in the checked-out
`PKGBUILD`, particularly if this README has not yet been updated for a newer
kernel release.

## Local builds

Build from this directory using `makepkg`:

```bash
makepkg -s
```

For a custom local kernel, override options through the environment:

```bash
_processor_opt=generic_v2 _preempt=voluntary makepkg -s
```

For example, `_localmodcfg=yes` uses the module database at
`$HOME/.config/modprobed.db` unless `_localmodcfg_path` specifies another file.
`_use_current=yes` requires `/proc/config.gz` and applies the recipe's selected
options on top of the running kernel's configuration. These options are **not**
recommended for building packages meant to run across many systems.

## Official release builds

The release pipeline must explicitly set `_devario_release=yes`:

```bash
_devario_release=yes makepkg -s
```

In this mode, every option listed in `_release_opts` is pinned to its
`PKGBUILD` value. A conflicting environment override causes the build to fail
instead of being silently accepted. Matching values are allowed. Without
`_devario_release=yes`, the recipe uses local-build rules.

This check protects the selected package options; it does not by itself pin the
build toolchain or replace testing in a controlled build environment.

## Source tags and package versions

- `pkgver` follows the kernel version selected by `_major` and `_minor`.
- `_tagrel` is the release index `N` in `devario-<version>-<N>`.
- `pkgrel` is `<_tagrel>.<_rebuild>`. Increase `_rebuild` when rebuilding the
  same source tag, or reset it to `1` for a newly tagged source release.
- The source archive and the shipped `config` are inputs to the package build.

## Updating the recipe

1. Review the intended source changes and publish or select the corresponding
   `devario-<version>-<N>` release in
   [Seafoam-Labs/linux](https://github.com/Seafoam-Labs/linux).
2. Update `_major`, `_minor`, and `_tagrel` as needed; review the vendored
   `config` against the new source tree (`make olddefconfig` and a config diff).
3. Update the release archive and configuration checksums with `updpkgsums`.
4. Build in a clean environment with `_devario_release=yes`, then test kernel
   boot, external-module/header compatibility, and upgrades before publishing.

**Branch note:** The LTS recipe permits the `voluntary` and `none` preemption modes in addition to `full` and `lazy`. Unlike the 7.x recipes in this tree, it has no `_lru_marie` build toggle.

## Credits and provenance

**The Devario kernel packaging and baseline configuration are derived from
[CachyOS](https://github.com/CachyOS/linux-cachyos).** In particular, this
recipe traces back to CachyOS `linux-cachyos-lts` at commit
`972d31fe2cbfda19208501a9518152ab90cfa2cc`, recorded in `PKGBUILD`.

We acknowledge the work of the CachyOS kernel maintainers **Peter Jung
(ptr1337), Eric Naim, and Vasiliy Stelmachenok**, and the earlier Arch
Linux kernel packaging contributors **Jan Alexander Steffens, Tobias
Powalowski, and Thomas Baechler**.

The Devario-specific source releases, modifications, build policy, and
package distribution are maintained separately by the Devario team. Credit to
CachyOS reflects the origin of the packaging work; it does not imply that
CachyOS publishes or supports Devario binaries.

Linux kernel code remains subject to its applicable upstream licenses; the
kernel package is declared `GPL-2.0-only` in `PKGBUILD`.
