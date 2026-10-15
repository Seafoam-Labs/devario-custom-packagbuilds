# WirePlumber package setup in isolated roots

`wireplumber` first reached `devario-core` as a seed record at release 1, whose
`.INSTALL` runs `systemctl --global enable wireplumber.service` unconditionally.
An isolated build root installs `systemd` near the end of the transaction, so a
package that early in the set has no `systemctl` on `PATH` yet. Shelly treats the
resulting exit 127 as `ScriptletFailed` and aborts provisioning as
`IsolatedBootstrapFailed` before the consumer's `prepare()` ever runs.

Confirmed in a worker build of `devario-libs/lib32-alsa-plugins`, where
`wireplumber` was package 234 of 253 and `systemd` 250. The same root installed
the guarded PipeWire scriptlet cleanly two hundred packages earlier, so only this
one record blocked the job.

Enable and disable are now best-effort: absent tools and unsuccessful commands
produce diagnostics without failing package setup. No service is started from a
scriptlet. The pre-0.4.4-2 reenable migration was dropped because no Devario
install can be that old and it needed the `vercmp` utility; upgrades leave the
administrator's service state, including masks, untouched.

## Publication

Release 2 replaces the seed record in place, in the same repository. The four
splits pin each other by exact version, so publish `wireplumber`,
`libwireplumber`, `wireplumber-docs` and `wireplumber-system-services` together
and refresh the worker's repository database before retrying a blocked consumer.
Nothing outside this pkgbase needs a bump: `pipewire-session-manager` depends on
an unpinned `wireplumber`, so it resolves to release 2 on its own. Editing these
files does not repair the release 1 archive already in the repository or cache.

`libwireplumber` advertises `libwireplumber-0.5.so=0-64` beside the bare
provision and checks the real SONAME during `package()`, because Shelly's
packager keeps only the bare form.

## Validation

`python3 tests/test-wireplumber-scriptlets.py` from the repository root covers
absent `systemctl`, failed commands with visible warnings, the no-op upgrade
path, offline enable and disable in a temporary root, and mask preservation.
`bash -n`, `makepkg --printsrcinfo` agreement with the committed `.SRCINFO`, and
`shelly build --review-only` (no findings) also pass. No full build has run, so
the compile and the `meson test` suite are unverified here; at validation time
the root pulled `python-breathe` from the worker's Arch-side repositories,
which now also has a local recipe in `devario-libs/python-breathe`.
