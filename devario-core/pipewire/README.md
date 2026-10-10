# PipeWire package setup in isolated roots

## Build prerequisites

The full split build requires dependencies for every enabled backend, even
when the immediate consumer only needs PipeWire's core libraries. Repeated
entries in a worker's `IncompleteDependencyPlan` can refer to the same missing
package across split outputs; they are not additional distinct dependencies.
Review success does not mean these dependencies are published.

For the reported missing packages, build and publish the following recipes
with their declared prerequisites available:

| Required package | Recipe | Notes |
| --- | --- | --- |
| `cdparanoia` | [devario-utilities/cdparanoia](../../devario-utilities/cdparanoia/PKGBUILD) | Publish first to satisfy the installed `gst-plugins-base` package's runtime dependency. |
| `libcanberra` | [devario-libs/libcanberra](../../devario-libs/libcanberra/PKGBUILD) | Existing recipe; publish its output. |
| `libcamera` | [devario-libs/libcamera](../../devario-libs/libcamera/PKGBUILD) | New recipe, 0.7.2-4; publish the `libcamera-ipa` split with the library. |
| `libffado` | [devario-libs/libffado](../../devario-libs/libffado/PKGBUILD) | New recipe, 2.5.0-2; can build before JACK2. |
| `onnxruntime` | [devario-development/onnxruntime](../../devario-development/onnxruntime/PKGBUILD) | Publish `onnxruntime-cpu`, which provides `onnxruntime`. Select one runtime provider, not all mutually conflicting variants. |
| `roc-toolkit` | [devario-libs/roc-toolkit](../../devario-libs/roc-toolkit/PKGBUILD) | New recipe, 0.4.0-3. |
| `rtkit` | [devario-core/rtkit](../rtkit/PKGBUILD) | New recipe, 0.14-2; uses `tinyxxd` for the build-time `xxd` utility. |

The four new recipes retain upstream patches, signatures/keys where present,
and archive provenance in `DEVARIO-UPSTREAM.json`. The FFADO recipe removes
the optional JACK build dependency to avoid `jack2 -> libffado -> jack2`.
FFADO's source only probes JACK's version for API selection; it does not link
to JACK. The recipe selects the set-buffer-size API supported by JACK2 1.9.22
and declares `which` for that optional probe.

These are full-feature recipes. For example, libcamera also builds its Qt 6
tools and documentation, and the existing ONNX Runtime recipe builds CPU and
GPU variants. Their own declared dependencies must be provisioned too; this
list addresses the worker's reported missing packages, not a complete source
bootstrap of an empty repository.

Refresh the worker's repository metadata after publication, resolve PipeWire
again, then build/publish the matching PipeWire splits and retry Pearl. Local
recipes alone do not satisfy `not_in_repositories`.

New-recipe validation: Bash syntax, makepkg/Shelly metadata agreement, bundled
patch checksums, and FFADO source archive checksums were checked. Full builds
and dependency resolution against the remote worker catalog have not run.

## Isolated-root scriptlets

The `pipewire` recipe produces the PipeWire split packages at `1:1.6.9-2`.
The `pipewire` and `pipewire-pulse` install scriptlets enable their user
sockets by default when `systemctl` is available. They do not start services.

Neither package requires the full systemd tools at runtime; the client
library depends on `systemd-libs`. An isolated build root can therefore lack
`systemctl`. Previously the unconditional command could return 127, which
Shelly treats as `ScriptletFailed` and aborts provisioning, even when the
installed PipeWire files are sufficient to build the consuming package.

Confirmed against the published `pipewire-1:1.6.9-1` archive, whose `.INSTALL`
line 3 is the unguarded `systemctl --global enable pipewire.socket`. A worker
build of `devario-libs/qt6-multimedia` installed PipeWire as package 331 of
354, before `systemd` itself, and aborted with
`.INSTALL: line 3: systemctl: command not found`, reported as
`BootstrapPackageSetupFailed` inside `IsolatedBootstrapFailed`. The build root
never reached `prepare()`, so no consumer-specific error exists.

Socket setup is now best-effort: missing tools and unsuccessful enable/disable
commands produce diagnostics without failing package installation or removal.
Existing unit masks are respected. Obsolete pre-Devario upgrade migrations
using `vercmp` were removed; upgrades leave the administrator's socket state
unchanged.

Rebuild this recipe and publish the matching split outputs together, including
`libpipewire`, `pipewire`, `pipewire-audio`, and `pipewire-pulse` when used.
Their exact-version dependencies must all resolve to release 2. Refresh the
worker repository metadata, then retry the blocked consumers in a fresh
isolated build root. Editing these source files does not repair the scriptlets
in the release 1 binary packages already in the repository or worker cache.

If socket setup was skipped on a desktop installation, inspect the diagnostic
and enable the desired sockets after systemd tools are installed:

```sh
systemctl --global enable pipewire.socket
systemctl --global enable pipewire-pulse.socket
```

Only enable the PulseAudio replacement when `pipewire-pulse` is installed.
Administrator masks are intentional overrides and should be reviewed first.

## Validation

Run `python tests/test-pipewire-scriptlets.py -v` from the repository root.
The five tests cover absent systemctl, failed commands with visible warnings,
upgrade behavior without vercmp, real offline systemctl enable/disable in
temporary roots, and preservation of masks. No host service state is changed.
Shell syntax and generated package metadata are also checked. A complete
PipeWire build and provisioning of the remote Pearl worker have not been run.
