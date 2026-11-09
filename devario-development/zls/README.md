# zls

Builds [ZLS 0.17.0](https://github.com/zigtools/zls/releases/tag/0.17.0) from
source for the Zig 0.17 series. Build and publish [zig](../../devario-core/zig/PKGBUILD)
first; this recipe requires `zig>=0.17.0` and `zig<0.18` at build time and
runtime, so it works with both 0.17.0 and the 0.17.1 bugfix release (either
the `zig` package or the pinned `zig-0.17` variant, which provides
`zig=0.17.0`).

The package installs `/usr/bin/zls`, `/usr/share/zls/schema.json`, and the MIT
license. It conflicts with `zls-0.16` because both packages use the same
editor-facing executable and schema paths. Use the ZLS package matching the
installed Zig compiler. `zls-0.16` also provides `zls=0.16.1`.

All source archives, including the three pinned Zig dependencies, have
SHA-256 checksums. `prepare()` extracts the dependencies into directories
named after the hashes in upstream `build.zig.zon`. Build and test hooks use
Zig's `--system` mode to resolve those local dependencies without downloads.
Do not replace `--system` resolution with `zig fetch`: Zig 0.17.0
recompresses GitHub tarball cache entries with an extra top-level directory,
so re-reading an entry from the global cache loses the dependency's
`build.zig.zon`, the package is treated as naked, and every later build fails
with `hash mismatch: ... but the fetched package has N-V-...`.
Optional Tracy profiling remains disabled. Caches and build outputs stay
inside the build directory.

Builds use baseline x86_64, position-independent executables, and ReleaseSafe
optimization. The check hook runs the upstream tests and checks the built
server's version.

```sh
shelly build --review-only --json ./devario-development/zls/PKGBUILD
shelly build --isolated --check ./devario-development/zls/PKGBUILD
```

See [the Zig build guide](../../ZIG-BUILDS.md) and the matching compiler's
README for prerequisites and worker setup.

## Validation

Bash syntax, generated Shelly metadata, all source checksums, and Shelly
review passed with no findings. The recipe's prepare, build, check, and
package hooks ran successfully with the matching Zig compiler, and dependency
resolution was additionally verified with no network access at all. Upstream
tests passed, and the staged executable reports the expected version. The
staged license and schema were checked. Builds used temporary directories;
no packages were installed or published. An isolated Shelly package build
remains a worker check.
