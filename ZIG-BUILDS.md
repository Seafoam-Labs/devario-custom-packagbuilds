# Zig 0.16 prerequisite builds

The 18 new recipe directories below, together with the existing GCC recipe,
cover all 34 missing package names identified in the Devario Core audit.
Packages are built from upstream source. Each directory includes generated
`.SRCINFO`, packaging license information, and any required patches and public
signing keys. Copy whole directories to the worker.

| Recipe | Version | Outputs relevant to this build |
| --- | --- | --- |
| [gcc](gcc/PKGBUILD) (existing) | `16.2.1+r23+gd564253eb6c8-2` | GCC compiler/runtime set, `libgccjit`, and `lib32-gcc-libs` |
| [rhash](rhash/PKGBUILD) | `1.4.6-2` | `rhash`, providing `librhash.so=1-64` |
| [jsoncpp](jsoncpp/PKGBUILD) | `1.9.8-2` | `jsoncpp`, providing `libjsoncpp.so=27-64`; also `jsoncpp-doc` |
| [libuv](libuv/PKGBUILD) | `1.53.0-1` | `libuv` |
| [cppdap](cppdap/PKGBUILD) | `1.58.0-3` | `cppdap` |
| [emacs](emacs/PKGBUILD) | `31.1-2` | `emacs`, `emacs-nox`, `emacs-wayland` |
| [cmake](cmake/PKGBUILD) | `4.4.3-2` | `cmake` |
| [ninja](ninja/PKGBUILD) | `1.13.2-3` | `ninja` |
| [python-build](python-build/PKGBUILD) | `1.6.0-1` | `python-build` |
| [python-installer](python-installer/PKGBUILD) | `1.0.1-1` | `python-installer` |
| [python-wheel](python-wheel/PKGBUILD) | `0.48.0-1` | `python-wheel` |
| [python-setuptools](python-setuptools/PKGBUILD) | `1:84.0.0-3` | `python-setuptools` |
| [python-psutil](python-psutil/PKGBUILD) | `7.2.2-1` | `python-psutil` |
| [python-sphinx](python-sphinx/PKGBUILD) | `9.1.0-1` | `python-sphinx` |
| [python-myst-parser](python-myst-parser/PKGBUILD) | `5.1.0-1` | `python-myst-parser` |
| [llvm21](llvm21/PKGBUILD) | `21.1.8-1` | `llvm21`, `llvm21-libs` |
| [compiler-rt21](compiler-rt21/PKGBUILD) | `21.1.8-1` | `compiler-rt21`, including 32-bit runtimes |
| [clang21](clang21/PKGBUILD) | `21.1.8-1` | `clang21` |
| [lld21](lld21/PKGBUILD) | `21.1.8-1` | `lld21` |
| [zig](zig/PKGBUILD) (existing) | `0.16.0-1` | `zig` |

The existing GCC build supplies `gcc`, `gcc-libs`, `libgcc`, `libstdc++`,
`libasan`, `libatomic`, `libgfortran`, `libgomp`, `libhwasan`, `liblsan`,
`libobjc`, `libquadmath`, `libtsan`, `libubsan`, and `lib32-gcc-libs` from the
audit. Do not create separate competing recipes for these outputs. Publish
the complete GCC set together because compiler packages depend on exact
versions of their runtimes. Install just one of the three Emacs alternatives.

## Bootstrap requirements

These are distribution rebuild recipes. The worker needs a working base-devel
environment and a bootstrap package repository, as described in
[DEPENDENCY-BUILDS.md](DEPENDENCY-BUILDS.md). Creating these recipes does not
make a Devario-Core-only build root complete.

There is no single linear build order from an empty root: `cppdap` needs CMake
while CMake depends on `cppdap`, and Python build tools require existing
versions of themselves. Seed the worker with CMake, `python-build`,
`python-installer`, `python-setuptools`, `python-wheel`, and `python-flit-core`
from the bootstrap repository. See [gcc/README.md](gcc/README.md) for GCC's
additional compiler bootstrap requirements, including Ada, D, Rust, and
matching multilib packages. The Python recipes retain the regular rebuild
path and omit the unused alternative interpreter-bootstrap branch.

The deeper dependency check also found prerequisites outside the original
34-package list. Supply them from the bootstrap repository. In particular:

| Used by | Additional runtime/build requirements absent from the audited Core index |
| --- | --- |
| Emacs | `libotf`, `tree-sitter` |
| JsonCpp documentation/build | `doxygen`, `graphviz`, `meson` |
| libuv documentation | `python-sphinx-copybutton` |
| Ninja | `re2c` |
| Python build tools | `python-flit-core`, `python-packaging`, `python-pyproject-hooks` |
| Setuptools runtime | `python-jaraco.collections`, `python-jaraco.functools`, `python-jaraco.text`, `python-more-itertools`, `python-platformdirs` |
| Sphinx runtime | `python-babel`, `python-docutils`, `python-imagesize`, `python-jinja`, `python-packaging`, `python-pygments`, `python-requests`, `python-roman-numerals-py`, `python-snowballstemmer`, `python-sphinx-alabaster-theme`, and its six `python-sphinxcontrib-*` packages |
| MyST runtime | `python-docutils`, `python-jinja`, `python-markdown-it-py`, `python-mdit_py_plugins`, `python-pygments`, `python-yaml` |

Checks introduce further dependencies, including pytest and its plugins,
network utilities, and TeX packages for Sphinx. The generated `.SRCINFO` files
contain the exact `depends`, `makedepends`, and `checkdepends` for each recipe;
the bootstrap repository must resolve their dependency chains. This set
covers the previously named packages, not every recursive test/documentation
dependency of the entire toolchain.

## Build and publish

With the bootstrap packages available, use this order and publish each stage
before starting its dependents:

1. Build and publish the complete existing GCC set, including `libgccjit` and
   `lib32-gcc-libs`. The installed `lib32-glibc` must match the build root's glibc.
2. Rebuild `python-installer`, `python-build`, `python-wheel`, and
   `python-setuptools` using the seeded Python tools. Then build `python-psutil`,
   `python-sphinx`, and `python-myst-parser` with their runtime dependencies.
3. Build `rhash`, `jsoncpp`, `libuv`, `cppdap`, and `emacs`. Use the seeded CMake
   for `cppdap`. Then build `cmake`, followed by `ninja`.
4. Build `llvm21` and publish both `llvm21` and `llvm21-libs`.
5. Build `compiler-rt21`, then `clang21` and `lld21`.
6. Build `zig` with checks enabled. Its `lib32-glibc` check dependency was
   already published in the audited Core index.

LLVM 21 installs alongside newer LLVM releases. Devario Core's LLVM 23 is not
a replacement for Zig 0.16's LLVM 21 development and runtime dependencies.

Import the supplied public keys **as the build account**, after checking the
fingerprints listed in each recipe's README:

```sh
for recipe in cmake llvm21 compiler-rt21 clang21 lld21 emacs libuv rhash; do
  gpg --import "$recipe"/keys/pgp/*.asc
done
```

Review and build one recipe at a time from the repository root:

```sh
shelly build --review-only --json ./llvm21/PKGBUILD
shelly build --isolated --check ./llvm21/PKGBUILD
```

Publish the resulting archives and refresh the repository database before
building the next stage. Recipe creation does not install or publish packages.

## Source integrity and validation

All 18 new recipes passed Bash syntax checks, source checksum verification,
applicable upstream signature verification, and source extraction/preparation.
Their generated makepkg and Shelly metadata agree, including split-package
outputs and architecture-specific dependencies. No source archive or Git
snapshot checksum is skipped; `SKIP` entries apply only to detached signature
files that are verified against their corresponding sources.

The Setuptools recipe downloaded from Arch had an incorrect Git checksum.
The corrected recipe pins the archive checksum previously verified against
Jason R. Coombs' signed `v84.0.0` tag. Python recipes do not require a PGP key
at build time. See
[python-setuptools/README.md](python-setuptools/README.md) for the fingerprint
and resolved commit. JsonCpp and RHash have explicit Shelly ABI provisions
with ELF64/SONAME checks, following this repository's existing conventions.

Shelly review completed for every recipe. Its warnings flag upstream command
substitutions used for component lists, CPU count, documentation tools, and
Python installation paths. Emacs warnings also match the word `node` and
backticks in patch text; those are C/Texinfo content, not Node.js commands.
These inputs were inspected; review warnings are not test failures.

Native local builds succeeded for `rhash`, `cppdap`, `ninja`, and both JsonCpp
packages. The RHash, Ninja, and JsonCpp check hooks passed, including all 127
JsonCpp unit tests. The cppdap recipe has no check hook. The generated archives
contain the expected `librhash.so=1-64` and `libjsoncpp.so=27-64` provisions.
JsonCpp's documentation copy leaves ownership assignment to the package
builder, avoiding a source-owner preservation failure under fakeroot. These
builds used temporary directories without installing host packages. Full LLVM,
Clang, compiler-rt, Emacs, CMake, Python, GCC, and Zig builds have not been run
as part of this prerequisite work. Isolated worker validation is still needed.

Arch's `clang21` and `lld21` check hooks remain disabled for their documented
upstream failures. CMake, cppdap, compiler-rt, and Emacs have no check hook;
passing `--check` does not add a test suite to those recipes.
