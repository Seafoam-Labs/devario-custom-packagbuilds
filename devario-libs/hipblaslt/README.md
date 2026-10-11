hipBLASLt packaging notes (2026-10-11)

The native recipe is currently ROCm 7.2.4, package release 5. The attempted
builds failed in rocRoller when HIP's `__noinline__` macro collided with
`[[__gnu__::__noinline__]]` in GCC 16's `<format>`, reached through `<chrono>`.
The fmt deprecation messages in the logs were warnings; the macro collision
was the fatal error.

`rocroller-gcc16-noinline.patch` saves, undefines, and restores that macro
around the standard library includes in both `Timer.hpp` and `HIPTimer.hpp`.
Patching only `Timer.hpp` allowed GPUArchitectureGenerator to build, but
`CommandSolution.cpp` then failed through `HIPTimer.hpp`, which includes
`<chrono>` first. Both headers are now covered. The existing dependency-fetch
patches and `<cstdint>` include patch are also retained and applied.

To reduce the native build workload, the recipe now sets
`HIPBLASLT_ENABLE_ROCROLLER=OFF` and retains only these six GPU targets:

- `gfx1100`, `gfx1101`, `gfx1102`: RX 7000 discrete GPUs.
- `gfx1151`: Strix Halo.
- `gfx1200`, `gfx1201`: RX 9000 discrete GPUs.

The original twelve-target configuration also included `gfx908`, `gfx90a`,
`gfx942`, `gfx950`, `gfx1103`, and `gfx1150`; these were removed. RX 6000 and
Strix Point are outside the requested coverage. Client builds remain disabled.
The rocRoller patches remain available if that backend is revisited later.
There is no confirmed successful full native build for this revised recipe
in the recorded work. Earlier compilation-time estimates for the Ryzen 7
3800X with 96 GB RAM were estimates, not measurements.

The temporary distribution workaround is
[`scripts/import-arch-hipblaslt.fish`](../../scripts/import-arch-hipblaslt.fish).
It downloads the Arch `hipblaslt-7.2.4-1-x86_64.pkg.tar.zst` binary, checks its
package name/version/architecture, signs it with the Devario key, and updates
the existing repository database while preserving other package entries.
This imports the Arch build unchanged: the six-target selection and disabled
rocRoller setting above apply only to the native recipe.

The configured binary repository root is `/srv/repositories/devario-libs`;
its x86_64 database is under `x86_64/devario-libs.db.tar.*`. Run the importer
as `remora-worker`, with `HOME=/var/lib/remora`,
`GNUPGHOME=/var/lib/remora/.gnupg`, and
`XDG_CONFIG_HOME=/var/lib/remora/.config`. The signing fingerprint is
`BB62CD2725FD8E25558F900A84F94F672976872C`. Stop `remora.service` before the
import, restart it after success, and request the normal mirror sync.
The importer does not update Remora's build records or perform that sync.

Arch signature verification failed on the builder with an invalid-packet
keyring error. For this stopgap, setting `SKIP_ARCH_SIGNATURE=1` bypasses the
Arch keyring check, signature download, and verification. Devario package
and repository signing still run. Without that environment setting, Arch
verification remains required. Re-signing does not establish Arch provenance
when its verification was skipped.

Future native rebuilds need the compilation broken apart into independently
reusable stages. The current single `cmake --build build` invocation still
combines the host library and all selected GPU kernel generation/compilation.
Reducing targets is an immediate workload reduction, not an implemented
incremental rebuild strategy.

The follow-up work should:

1. Separate common host-library work from device-library generation and
   compilation, identifying the supported upstream build targets first.
2. Build and retain device artifacts per GPU target, or per compatible group
   where upstream generation requires it, so a failed target can be retried
   without rebuilding every other target.
3. Key reusable artifacts by source revision, patches, toolchain, target, and
   build options. Reuse must not mix incompatible ROCm builds.
4. Assemble the final package with all required target artifacts and shared
   metadata, checking installation paths, library loading, and dispatch for
   each retained architecture before replacing the stopgap binary.
5. Record wall time, peak memory, and disk use per stage on the builder to
   choose concurrency and establish measured rebuild expectations.

This restructuring is not implemented yet. Merely splitting package outputs
after the existing monolithic build would not avoid repeated compilation;
the build stages and their artifact dependencies must be separated as well.
