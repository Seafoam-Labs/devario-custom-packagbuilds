# cmake for Shelly

Based on [Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/cmake/-/blob/main/PKGBUILD), pinned to `4.4.3-2`. Copy the whole directory to the worker, including local patches and `keys/` where present.

Retains the upstream bootstrap build, GUI, HTML/man documentation, and byte-compiled Emacs integration. The worker needs the declared Qt, Sphinx, and Emacs build dependencies. Upstream packaging has no `check()` hook.

The permitted upstream signing fingerprints are:

- `CBA23971357C2E6590D9EFD3EC8FEF3A7BFB4EDA`

Import the supplied public keys as the build account after checking these fingerprints:

```sh
gpg --import cmake/keys/pgp/*.asc
```

From the repository root:

```sh
shelly build --review-only --json ./cmake/PKGBUILD
shelly build --isolated --check ./cmake/PKGBUILD
```

Bash syntax, generated metadata, source checksums, applicable signatures, and source preparation were validated. makepkg and Shelly metadata agree. See [the Zig build guide](../ZIG-BUILDS.md) for build order, bootstrap dependencies, review findings, and the exact limits of local build validation.
