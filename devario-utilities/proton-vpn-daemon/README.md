# proton-vpn-daemon service scriptlet

Arch runs `systemctl` unconditionally in all three actions of
`proton-vpn-daemon.install`. A Shelly isolated build root can hit that twice
over: `systemd` installs late in alpm's own dependency order, so an earlier
package in the transaction has no `systemctl` on `PATH` yet and the call exits
127; and even with the binary present a root has no running init, so
`enable --now`, `restart` and `daemon-reload` fail on the bus. A failing
scriptlet aborts provisioning as `ScriptletFailed` before the recipe's
`prepare()` runs, and the log names only the package being installed, not this
recipe. The same unguarded pattern previously blocked consumers of the
`wireplumber` and `pipewire` records.

Every call now goes through one helper that reports to stderr and returns 0.
On a real system `systemctl` is present and the service is still enabled and
started by `post_install`, so nothing changes for an installed host; only the
build root behavior differs. `post_upgrade` additionally treats a missing
`systemctl` as "not enabled", so it asks for the enable rather than failing.

The scriptlet is the only file changed here. Everything else matches the Arch
packaging archive recorded in `DEVARIO-UPSTREAM.json`, including
`split-tunneling.patch` and Arch's own unreferenced `kernel-7.0.patch`, which
that recipe ships in the directory but never names in `source=`, so it is
carried along untouched. The `dbus.conf`, `dbus.service` and `systemd.service`
files are fetched from Proton's `stable` branch at build time, not vendored.
`tests/test-proton-vpn-daemon-scriptlets.py` exercises all three actions with
and without a failing `systemctl`.

## Publication

Nothing publishes under this name yet, so `pkgrel` stays at 1 and no revision
disambiguation is needed. Build after `python-proton-vpn-api-core`, which the
recipe's `depends` requires, and before `proton-vpn-gtk-app`, which requires
this one.
