# Millennium dependency builds

## First batch (2026-10-14)

Build and publish the 29 recipe directories below before continuing the missing
Millennium/Steam dependency chain. The batch reuses 27 recipes already in this
tree and adds two complete, unchanged official Arch imports: `perl-test-pod`
and `perl-par-dist`. Copy each complete directory, including auxiliary files,
licenses and signing keys where present.

The batch was selected against the public Devario x86_64 sync repositories
on 2026-10-14. Its mandatory runtime, build and check dependency closure
resolves to published packages, assuming a compatible base-devel and multilib
toolchain. No recipe in this batch depends on another unpublished recipe, so
these builds can be queued independently. This is dependency-metadata
readiness; source availability, package code, ABI and file conflicts can still
cause individual builds to fail. The actual worker's enabled repositories and
refresh state must agree with the public repositories used for this audit.

| Recipe directory | Release | Source |
| --- | --- | --- |
| [devario-development/lib32-cmocka](devario-development/lib32-cmocka/PKGBUILD) | `2.0.2-1` | Existing recipe |
| [devario-development/lynx](devario-development/lynx/PKGBUILD) | `2.9.3-1` | Existing recipe |
| [devario-development/mercurial](devario-development/mercurial/PKGBUILD) | `7.2.4-2` | Existing recipe |
| [devario-development/publicsuffix-list](devario-development/publicsuffix-list/PKGBUILD) | `20260507.2070.ee780bcf-1` | Existing recipe |
| [devario-libs/lib32-acl](devario-libs/lib32-acl/PKGBUILD) | `2.4.0-1` | Existing recipe |
| [devario-libs/lib32-bzip2](devario-libs/lib32-bzip2/PKGBUILD) | `1.0.8-4` | Existing recipe |
| [devario-libs/lib32-directx-headers](devario-libs/lib32-directx-headers/PKGBUILD) | `1:1.619.5-1` | Existing recipe |
| [devario-libs/lib32-flac](devario-libs/lib32-flac/PKGBUILD) | `1.5.0-1` | Existing recipe |
| [devario-libs/lib32-libgcrypt](devario-libs/lib32-libgcrypt/PKGBUILD) | `1.12.4-1` | Existing recipe |
| [devario-libs/lib32-libidn2](devario-libs/lib32-libidn2/PKGBUILD) | `2.3.8-1` | Existing recipe |
| [devario-libs/lib32-libldap](devario-libs/lib32-libldap/PKGBUILD) | `2.7.1-1` | Existing recipe |
| [devario-libs/lib32-libpciaccess](devario-libs/lib32-libpciaccess/PKGBUILD) | `0.19-1` | Existing recipe |
| [devario-libs/lib32-libpng](devario-libs/lib32-libpng/PKGBUILD) | `1.6.59-1` | Existing recipe |
| [devario-libs/lib32-libssh2](devario-libs/lib32-libssh2/PKGBUILD) | `1.11.1-5` | Existing recipe |
| [devario-libs/lib32-libvorbis](devario-libs/lib32-libvorbis/PKGBUILD) | `1.3.7-4` | Existing recipe |
| [devario-libs/lib32-libxdmcp](devario-libs/lib32-libxdmcp/PKGBUILD) | `1.1.5-1` | Existing recipe |
| [devario-libs/lib32-libxshmfence](devario-libs/lib32-libxshmfence/PKGBUILD) | `1.3.3-1` | Existing recipe |
| [devario-libs/lib32-nettle](devario-libs/lib32-nettle/PKGBUILD) | `4.0-2` | Existing recipe |
| [devario-libs/lib32-nspr](devario-libs/lib32-nspr/PKGBUILD) | `4.40-1` | Existing recipe |
| [devario-libs/lib32-readline](devario-libs/lib32-readline/PKGBUILD) | `8.3.3-1` | Existing recipe |
| [devario-libs/lib32-util-linux](devario-libs/lib32-util-linux/PKGBUILD) | `2.42.4-1` | Existing recipe |
| [devario-libs/lib32-zstd](devario-libs/lib32-zstd/PKGBUILD) | `1.5.7-2` | Existing recipe |
| [devario-libs/libclc](devario-libs/libclc/PKGBUILD) | `23.1.1-2` | Existing recipe |
| [devario-libs/perl-par-dist](devario-libs/perl-par-dist/PKGBUILD) | `0.53-4` | New Arch import |
| [devario-libs/perl-test-pod](devario-libs/perl-test-pod/PKGBUILD) | `1.52-12` | New Arch import |
| [devario-libs/perl-text-wrapi18n](devario-libs/perl-text-wrapi18n/PKGBUILD) | `0.06-10` | Existing recipe |
| [devario-libs/xtrans](devario-libs/xtrans/PKGBUILD) | `1.6.0-1` | Existing recipe |
| [devario-utilities/lsb-release](devario-utilities/lsb-release/PKGBUILD) | `2.0.r55.a25a4fc-2` | Existing recipe |
| [devario-utilities/zenity](devario-utilities/zenity/PKGBUILD) | `4.2.2-1` | Existing recipe |

For each listed directory, review and build with checks enabled:

```sh
cd devario-libs/perl-test-pod
shelly build --review-only --json "$PWD/PKGBUILD"
shelly build --isolated --check "$PWD/PKGBUILD"
```

Publish the resulting package outputs and refresh the worker's repository
databases before scheduling consumers. Recipe imports alone do not satisfy
`not_in_repositories` failures. Do not rebuild existing split outputs as
separate source recipes.

## Why the two imports are needed

`perl-unicode-linebreak` checks require `perl-test-pod`, and
`perl-module-build` checks require `perl-par-dist`. Both consumers are needed
by `po4a`, which is a build dependency of `lib32-xz`. The imports depend only
on `perl`, which is already published, plus the normal build environment.

The imported recipe versions, source pins, checksums, packaging licenses,
upstream metadata and check functions are unchanged from Arch:

- [perl-test-pod](https://gitlab.archlinux.org/archlinux/packaging/packages/perl-test-pod/-/tree/de2a1c1750fe73d510f5fa552101cadbbc29b506), commit `de2a1c1750fe73d510f5fa552101cadbbc29b506`.
- [perl-par-dist](https://gitlab.archlinux.org/archlinux/packaging/packages/perl-par-dist/-/tree/5d2a8c0a66c4fd10b83e6e49472397f6447ce22c), commit `5d2a8c0a66c4fd10b83e6e49472397f6447ce22c`.

## Following this batch

Once the first batch is published, build the next dependency-ready stage,
including `perl-module-build` and `perl-unicode-linebreak`, then `po4a`,
then `lib32-xz`. Reevaluate repository availability between stages so already
published providers can be reused.

`lib32-fakeroot` is an optional addition for reproducing Arch's exact
`multilib-devel` baseline. It is not declared by Millennium and is not part
of this first batch: its `po4a` build requirement is not yet published.

The full remaining multilib chain has bootstrap cycles involving
GNUTLS/p11-kit, keyutils/Kerberos, D-Bus/GLib/systemd, Cairo/fontconfig/
FreeType/HarfBuzz and libglvnd/libva/Mesa. This first batch does not resolve
those cycles or guarantee a complete Millennium build.

## Validation

- All 29 recipes pass `bash -n`, and fresh `makepkg --printsrcinfo`
  agrees with the saved dependency metadata.
- Clean official Arch devtools chroot builds succeed with checks enabled for
  `perl-test-pod` (19 tests), `perl-par-dist` (7 tests) and the existing
  `perl-text-wrapi18n` recipe (2 tests). Source checksums pass.
- All three packages install inside their disposable chroots, have no missing
  package files and load their Perl modules successfully.
- The other 26 batch recipes were not compiled for this change. No package
  was published or built on the actual Devario worker during validation.
