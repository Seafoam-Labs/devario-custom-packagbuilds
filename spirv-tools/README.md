# SPIR-V build pair

Build `../spirv-headers` first, publish its package, and refresh the repository
database used by the isolated worker. Then build `spirv-tools`:

```sh
shelly build --isolated ./spirv-headers/PKGBUILD
# Publish spirv-headers and refresh the worker repository before continuing.
shelly build --isolated ./spirv-tools/PKGBUILD
```

Run these commands from the repository root. Updating the host headers alone
does not update the isolated build root.

These recipes pair SPIRV-Tools `2026.4.rc2` at commit
`ef96ed763b43b59b33b31b362f09a02b729fa1c9` with SPIRV-Headers
`1.4.363.0` at commit `496543121ce6419f23d6fa5d7194ba66c36212d2`.
The headers commit is the upstream `vulkan-sdk-1.4.363.0` tag and the exact
revision specified in the tools release's
[DEPS file](https://github.com/KhronosGroup/SPIRV-Tools/blob/ef96ed763b43b59b33b31b362f09a02b729fa1c9/DEPS).
Both archives have SHA-256 checksums.

The tools recipe requires that exact headers package version and uses its
installed headers and JSON grammars from `/usr`. This prevents an isolated
build from silently selecting older headers that lack
`OpCooperativeMatrixPerElementOpEXT` and `OpCooperativeMatrixReduceEXT`.
When updating either recipe, check upstream DEPS and update the pair together.

SPIRV-Tools installs shared libraries, command-line tools, public API headers,
and CMake/pkg-config metadata. Upstream tests are disabled; they require
additional third-party test dependencies not included in these recipes.

## Validation

Both recipes pass Bash syntax checks, source checksum verification, `.SRCINFO`
generation, and Shelly review with no findings. Both build and installation
functions completed locally with GCC 16.2.1. For the tools build, only the
headers prefix was redirected from `/usr` to the staged headers package under
`/tmp`; no host packages were installed. All 383 build steps succeeded.

The staged tools successfully assembled, validated, optimized, revalidated,
and disassembled a minimal Vulkan 1.3 compute shader. Full upstream tests and
isolated worker builds have not been run.
