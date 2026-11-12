# liquidctl key material

Arch's `keys/pgp` export of `23F335ED4E829797734B22F65841AF7406AF7AD0`
(Jonas Tadeu Silva Malaco Filho) ships the primary key only. The `v1.16.0`
tag is signed with his signing subkey
`E85FE39F6A144827869F9A7745F0AD783D788A6D`, so a keyring built from Arch's
export alone fails `git verify-tag` with "No public key". The `.asc` here,
and the identical copy in `python-pyusb`, is a full export of the same
primary key refreshed from keyserver.ubuntu.com on 2026-11-12. The primary
fingerprint still matches `validpgpkeys`, gpg checks the subkey binding on
import, and both the `v1.16.0` and pyusb `v1.3.1` tags verify against the
shipped material alone.

The key export is the only file changed here. Everything else matches the
Arch packaging archive recorded in `DEVARIO-UPSTREAM.json`.

## Publication

Build after the five dependency recipes publish (`python-colorlog`,
`python-crcmod`, `python-docopt`, `python-hidapi`, `python-pyusb`);
`python-crcmod 1.7-9` satisfies the `python-crcmod=1.7` pin the worker's
plan reports. `check()` needs `python-pytest`, which is already published.