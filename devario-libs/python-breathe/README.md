# python-breathe for Shelly

Arch's packaging, imported unchanged at `5.1.0-1`. Copy the whole directory to
the worker, including the patch file and `keys/pgp/`.

Closes the `python-breathe` makedepend of the `wireplumber` documentation
build, which had resolved from the worker's Arch-side repositories. Its
`ruff` makedepend, the last build dependency without a local recipe, now
also has one in `devario-development/ruff`.

From the repository root:

```sh
shelly build --review-only --json ./devario-libs/python-breathe/PKGBUILD
shelly build --isolated --no-check ./devario-libs/python-breathe/PKGBUILD
```

`makepkg --printsrcinfo` matches the committed `.SRCINFO`, and the review gate
returned no findings. No full build has run.
