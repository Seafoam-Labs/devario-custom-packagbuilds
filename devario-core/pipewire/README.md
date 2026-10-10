# PipeWire package setup in isolated roots

The `pipewire` recipe produces the PipeWire split packages at `1:1.6.9-3`.
The `pipewire` and `pipewire-pulse` install scriptlets enable their user
sockets by default when `systemctl` is available. They do not start services.

Neither package requires the full systemd tools at runtime; the client
library depends on `systemd-libs`. An isolated build root can therefore lack
`systemctl`. Previously the unconditional command could return 127, which
Shelly treats as `ScriptletFailed` and aborts provisioning, even when the
installed PipeWire files are sufficient to build the consuming package.
The reported Pearl failure identifies this scriptlet, but does not include
the underlying command error; earlier worker output is needed to confirm
which `systemctl` failure occurred there.

Socket setup is now best-effort: missing tools and unsuccessful enable/disable
commands produce diagnostics without failing package installation or removal.
Existing unit masks are respected. Obsolete pre-Devario upgrade migrations
using `vercmp` were removed; upgrades leave the administrator's socket state
unchanged.

Rebuild this recipe and publish the matching split outputs together, including
`libpipewire`, `pipewire`, `pipewire-audio`, and `pipewire-pulse` when used.
Their exact-version dependencies must all resolve to release 3. Refresh the
worker repository metadata, then retry Pearl in a fresh isolated build root.
Editing these source files does not repair the scriptlets in release 2 binary
packages already in the repository or worker cache.

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
