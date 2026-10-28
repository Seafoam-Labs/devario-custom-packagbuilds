# zls-0.16

Builds [ZLS 0.16.1](https://github.com/zigtools/zls/releases/tag/0.16.1) from
source for Zig 0.16.0. Build and publish [zig-0.16](../zig-0.16/PKGBUILD)
first; this recipe requires `zig-0.16=0.16.0` at build time and runtime.

The package installs `/usr/bin/zls`, `/usr/share/zls/schema.json`, and the MIT
license. It conflicts with `zls` because both packages use the same
editor-facing executable and schema paths. Use the ZLS package matching the
installed Zig compiler. `zls-0.16` also provides `zls=0.16.1`.

All source archives, including the three pinned Zig dependencies, have
SHA-256 checksums. `prepare()` extracts the dependencies into directories
named after the hashes in upstream `build.zig.zon`. Build and test hooks use
Zig's `--system` mode to resolve those local dependencies without downloads.
Optional Tracy profiling remains disabled. Caches and build outputs stay
inside the build directory.

Builds use baseline x86_64, position-independent executables, and ReleaseSafe
optimization. The check hook runs the upstream tests and checks the built
server's version.

```sh
shelly build --review-only --json ./devario-core/zls-0.16/PKGBUILD
shelly build --isolated --check ./devario-core/zls-0.16/PKGBUILD
```

See [the Zig build guide](../../ZIG-BUILDS.md) and the matching compiler's
README for prerequisites and worker setup.

## Validation

Bash syntax, generated Shelly metadata, all source checksums, and Shelly
review passed with no findings. The recipe's prepare, build, check, and
package hooks ran successfully with the matching Zig compiler. Upstream
tests passed, and the staged executable reports the expected version. The
staged license and schema were checked. Builds used temporary directories;
no packages were installed or published. An isolated Shelly package build
remains a worker check.
