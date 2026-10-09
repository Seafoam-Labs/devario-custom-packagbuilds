# Flit Core 3 compatibility backend

This recipe packages Flit Core 3.12.0 for Python projects whose build requirements
include `flit_core<4`. It provides `python-flit-core=3.12.0` and conflicts with
`python-flit-core`, since both own the same Python module and distribution metadata.
Select the appropriate backend for each isolated build root.

Build from the repository root:

```sh
shelly build --isolated --no-check devario-core/python-flit-core3/PKGBUILD
```

Package tests and test-only dependencies are omitted. The wheel build uses the backend in the source tree and does not require an installed Flit
backend or `python-build`.

Publish the resulting package and refresh the worker repository metadata. In a
dependent PKGBUILD, replace its unversioned `python-flit-core` build dependency
with `'python-flit-core<4'` or `python-flit-core3`, then regenerate its `.SRCINFO`.
An unversioned dependency can still select Flit Core 4.x. The project's Python
build requirement should remain `flit_core<4`.
