# ROC Toolkit dependencies

`IncompleteDependencyPlan` for `gengetopt`, `openfec`, `ragel`, and `sox`
means those packages are absent from the worker's enabled repositories and
build environment. Both diagnostic entries describe the same missing package.
Keep these dependencies in `roc-toolkit`; adding recipes alone does not make
their binary packages available to an isolated build.

New recipes supply `gengetopt`, `openfec`, and `sox`, plus SoX's missing
dependencies `libmad`, `opusfile`, and `time`. Ragel already has a recipe.
Each new directory includes generated `.SRCINFO`, packaging provenance in
`DEVARIO-UPSTREAM.json`, and any required patches and signing keys.

## Build and publish order

The public Devario package catalog checked on 2026-10-10 also lacked several
prerequisites with existing recipes. Build and publish the following stages,
refreshing worker repository metadata between stages:

| Stage | Recipe directories |
| --- | --- |
| 1 | `devario-development/gperf`, `devario-utilities/netpbm`, `devario-development/gengetopt`, `devario-libs/openfec`, `devario-libs/libmad`, `devario-libs/opusfile`, `devario-libs/twolame`, `devario-libs/wavpack`, `devario-utilities/time` |
| 2 | `devario-development/fig2dev` (after netpbm), `devario-libs/libid3tag` (after gperf) |
| 3 | `devario-development/ragel` (after fig2dev), `devario-utilities/sox` (after its audio libraries and time) |
| 4 | `devario-libs/roc-toolkit` |

For each directory, use `shelly build --isolated --check path/to/PKGBUILD`.
Copy complete recipe directories to the worker, including `keys/pgp` where
present. Import the public keys matching `validpgpkeys` into the build account's
keyring. Existing published packages, including `colm`, satisfy the other
declared prerequisites in this catalog snapshot.

Once stages 1–3 are published and visible to the worker, retry:

```sh
shelly build --isolated --check ./devario-libs/roc-toolkit/PKGBUILD
```

## Recipe adaptations

- Gengetopt uses GNU's signed release archive, which includes generated code
  and gnulib. This avoids the Git recipe's dependency on itself and `gengen`.
  Two bundled gnulib declarations are parenthesized to avoid expansion of
  glibc's type-generic `bsearch` and `memchr` macros with current compilers.
  The bundled public key includes the release signing subkey from GNU's keyring.
- SoX uses a checksum-pinned sox_ng tag archive and identifies the distribution
  as Devario. `--enable-replace` retains the `sox`, `sox.h`, and `libsox.so`
  compatibility names needed by ROC Toolkit.
- OpenFEC uses ROC Streaming's maintained fork, as in the upstream recipe.
- Libmad retains the upstream packaging's compatibility and security patches.

## Validation

- All six new recipes passed Bash syntax checks, source checksum verification,
  and makepkg/Shelly metadata comparison. Shelly review reports no findings
  except warnings about Makefile expressions in libmad's upstream patch.
- Gengetopt, libmad, and GNU time source signatures verified. GnuPG reports
  gengetopt's signing key as expired; its signature is cryptographically valid.
  The recipe retains signature verification and its pinned primary fingerprint.
- All six recipes completed native builds and package staging under `/tmp`.
  Gengetopt passed 50 tests, OpenFEC passed 265, GNU time passed 10, and SoX's
  `installcheck` completed. Libmad and opusfile have no recipe `check()` function.
- The native SoX check used the host's available features; ID3-tag and Opus
  support were disabled there. The isolated recipe retains the dependencies
  that enable those features, which still need validation in the worker.
- The unpublished dependency chain above has a local recipe for every name;
  remaining declared dependency names/providers exist in the catalog snapshot.

No host packages were installed. Isolated worker builds, signed publication,
and the final ROC Toolkit build have not been performed.
