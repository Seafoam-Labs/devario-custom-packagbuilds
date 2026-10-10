# Libcamera build prerequisites

This recipe builds the library, IPA modules, tools, GStreamer plugin, Python
bindings, and documentation together. Python bindings require `pybind11`;
documentation requires `python-sphinx-book-theme` and
`python-sphinxcontrib-doxylink`. Repeated dependency-plan errors refer to these
same requirements across the split outputs.

For the reported missing packages, build and publish these recipes before
retrying libcamera, with their own declared prerequisites available:

| Package | Recipe | Notes |
| --- | --- | --- |
| `cdparanoia` | [devario-utilities/cdparanoia](../../devario-utilities/cdparanoia/PKGBUILD) | Existing recipe; satisfies `gst-plugins-base`'s missing runtime dependency. |
| `pybind11` | [devario-libs/pybind11](../pybind11/PKGBUILD) | Existing recipe, 3.1.0-2. |
| `python-sphinxcontrib-doxylink` | [devario-development/python-sphinxcontrib-doxylink](../../devario-development/python-sphinxcontrib-doxylink/PKGBUILD) | Added recipe, 1.13.0-2. |
| `python-sphinx-book-theme` | [devario-development/python-sphinx-book-theme](../../devario-development/python-sphinx-book-theme/PKGBUILD) | Added recipe, 1.4.0-2. Requires `python-pydata-sphinx-theme`. |

The book theme uses the packaged Node.js/npm, following the existing
`python-pydata-sphinx-theme` recipe. Its upstream exact PyData 0.20.0 wheel
requirement is relaxed to `>=0.20,<0.24`, in both the wheel and package
metadata, to support this repository's PyData 0.23.0. Its Python and Sphinx
minimum versions are also declared explicitly.

If needed, publish the existing
[PyData theme](../../devario-development/python-pydata-sphinx-theme/PKGBUILD)
and [theme builder](../../devario-development/python-sphinx-theme-builder/PKGBUILD)
before building the book theme. Refresh the worker repository metadata after
publishing the missing packages, then retry libcamera. A recipe on disk does
not satisfy `not_in_repositories`; the binary package must be available in a
repository enabled for the worker.

## Validation

The two new dependency source archives passed their upstream checksums. Both
recipes passed Bash syntax and matching makepkg/Shelly metadata checks. Their
build and package functions produced wheels and staged files in a temporary
environment. The book theme's locale conversion test passed.

A Sphinx 9.1.0 HTML build with warnings treated as errors passed using the
built book theme, PyData 0.23.0, and the built Doxylink extension. The rendered
Doxygen API link and compiled theme CSS/JavaScript were checked. `pip check`
reported no broken requirements. No host packages were installed; a full
libcamera build and remote worker dependency resolution have not been run.
