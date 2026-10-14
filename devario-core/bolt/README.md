# Bolt and boltctl

This split PKGBUILD builds Bolt 0.9.10 once and produces:

- `bolt`: `boltd`, the systemd/D-Bus service, upstream udev activation rules,
  Polkit policy, D-Bus interfaces, and daemon manual.
- `boltctl`: the command-line client and its manual, depending on the matching
  daemon package.

Build through the repository's normal package builder with the dependencies
declared in `PKGBUILD`. Both output archives must be published together.
The source archive is pinned by SHA-256. `check()` runs the upstream Meson
suite; its declared check dependencies enable the mock-device tests.

The daemon's static service is started by udev or D-Bus. Keep upstream
authorization policy: list devices with `boltctl list`, authorize one with
`boltctl authorize UUID`, or remember a trusted enclosure with
`boltctl enroll --policy auto UUID`. Do not enable every connected device with
an unconditional udev authorization rule.
