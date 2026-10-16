# python-sphinx-hawkmoth for Shelly

Arch's packaging, imported unchanged at `0.22.0-3`. Copy the whole directory to
the worker, including `keys/pgp/`.

Closes the `python-sphinx-hawkmoth` makedepend of the `mesa` pkgbase, which
needs it for the `mesa-docs` split (`-D html-docs=enabled`). It is a makedepend
and not a runtime dep, so publishing this closes a parity gap rather than
unblocking a build: the published `mesa-1:26.2.4-1` already built with
`python-sphinx-hawkmoth-0.22.0-3.1-x86_64_v3` in its root, which is an Arch-side
package, not a Devario output. There is no local `mesa` recipe yet either.

`depends` names `clang` because `hawkmoth/parser.py` does
`from clang.cindex import ...`, and Arch's clang ships those Python bindings
into site-packages rather than a separate package. That binding is not on PyPI,
so a host import probe needs `clang`, `python-docutils` and `python-sphinx`
present, not just the wheel.

Two build-log entries that are not defects:

- The pinned key `3FE6F7606966ED87707760B6A14C59DFEDB4CE88` (Jani Nikula)
  expired in May 2026. Arch ships it as is, the tag signature itself is valid,
  and Shelly downgrades an expired key to a warning and continues.
- `checkdepends` lists `python-strictyaml`, which has no recipe in this tree.
  The worker builds with `--no-check`, so `check()` never runs.

From the repository root:

```sh
shelly build --review-only --json ./devario-development/python-sphinx-hawkmoth/PKGBUILD
shelly build --isolated --no-check ./devario-development/python-sphinx-hawkmoth/PKGBUILD
```

`makepkg --printsrcinfo` matches the committed `.SRCINFO`, `makepkg
--verifysource` passes b2sums and the tag signature, and a host run of the
recipe's own `build()` and `package()` produced
`hawkmoth-0.22.0-py3-none-any.whl` and installed it under
`/usr/lib/python3.14/site-packages`. The Sphinx entry point is `hawkmoth.setup`,
so `conf.py` lists `hawkmoth`, not `hawkmoth.extension`. The review gate
returned no findings. No isolated worker build has run.
