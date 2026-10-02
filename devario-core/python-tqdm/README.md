# Python tqdm for Devario

Builds `python-tqdm` 4.70.1-1 as an architecture-independent package. It
contains the Python module, `tqdm` command, Bash completion, man page, and
license. The local Meson recipe requires this package.

Adapted from [Arch packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/python-tqdm/-/blob/main/PKGBUILD),
using the [PyPI source release](https://pypi.org/project/tqdm/4.70.1/#files)
and its published SHA-256 checksum. Wheel builds use the declared build
dependencies with `--no-isolation`, without downloading build tools.

From this repository's root:

```sh
shelly build --review-only --json ./devario-core/python-tqdm/PKGBUILD
shelly build --isolated --check ./devario-core/python-tqdm/PKGBUILD
```

Publish the resulting package and refresh the worker's repository before
building Meson or other consumers. Build dependencies are `python-build`,
`python-installer`, `python-setuptools`, and `python-setuptools-scm`.
Checks additionally require pytest, pytest-asyncio, and pytest-timeout.

The check function tests the installed wheel using upstream's core, CLI,
asyncio, concurrency, logging, iterator, synchronization, utility, and
version tests. It runs modules in separate processes to avoid global lock
state leaking between them. GUI, notebook, data-science integration suites,
and performance benchmarks are outside this package's checks.

Validation: source checksum, Bash syntax, makepkg/Shelly metadata, wheel
build, all 164 selected upstream tests, and staged installation passed
with Python 3.14. The staged module and CLI both report 4.70.1; completion,
man page, and license files are present. Build/test tools were installed
only into a temporary environment, without changing host packages.
Shelly review reports one warning for the Python site-packages path lookup
in `check()`; that command only reads Python's installation paths.
An isolated worker build and package archive generation remain unverified.
