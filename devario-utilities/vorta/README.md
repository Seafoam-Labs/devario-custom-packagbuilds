# Vorta

Builds [Vorta 0.11.6](https://github.com/borgbase/vorta/releases/tag/v0.11.6)
from its checksum-pinned release archive. Includes Qt translations, desktop
launcher, application icons, and AppStream metadata.

From this directory, build with Shelly:

```sh
shelly build --sync-deps --no-check
```

Use `shelly build --sync-deps --check` to also run upstream unit tests with
Qt's offscreen platform and a temporary D-Bus session.

First build and publish the dependency recipes in
[VORTA-BUILDS.md](../../VORTA-BUILDS.md), refreshing the worker's repository
databases between stages. This checkout includes the four missing direct
dependencies and their three missing supporting dependencies. Vorta cannot
build until their package outputs are available in the worker's repositories.

The default build plan excludes test-only and optional dependencies. Running
`--check` also requires the declared `checkdepends`, including `python-pytest-qt`.

Install `openssh` for remote backups and SSH key generation, and
`python-pyfuse3` for mounting Borg archives. GNOME Keyring or KWallet can store
repository passwords; NetworkManager enables Wi-Fi and metered-network checks.
