# ruff for Shelly

Arch's packaging, imported unchanged at `0.17.0-1`. Copy the whole directory to
the worker.

Builds both splits, the `ruff` binary and `python-ruff`. Closes the `ruff`
makedepend of `devario-libs/python-breathe`, which had resolved from the
worker's Arch-side repositories. Its own `cargo` makedepend has no Devario
recipe and still resolves Arch-side.

From the repository root:

```sh
shelly build --review-only --json ./devario-development/ruff/PKGBUILD
shelly build --isolated --no-check ./devario-development/ruff/PKGBUILD
```

`makepkg --printsrcinfo` matches the committed `.SRCINFO`. The review returns
four warnings, all upstream shape: `cargo fetch` in `prepare()` and the
`rustc --print host-tuple` substitution in `build()`. No full build has run.
