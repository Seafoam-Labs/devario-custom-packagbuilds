# Fastfetch for Devario

`2.69.0-4` combines native Shelly package detection with Devario's PNG fish
logo and bordered Fastfetch layout. The three ASCII fish designs remain
available as alternatives. The recipe is based on upstream `2.69.0-1`.

ImageMagick, Chafa, and zlib are runtime dependencies. Ghostty can display the
PNG through the Kitty graphics protocol; terminals without image support can
use Chafa's text rendering. The build enables image support and `check()`
rejects binaries missing ImageMagick 7, Chafa, or zlib support.

The source patch queries `shelly list standard --show-hidden --json` and
counts installed package records. Shelly resolves its own configuration and
database paths. Fastfetch exposes the count as `{shelly}`, labels it `Shelly`
in normal output, and includes it in JSON results and totals. Pacman
detection is disabled by default in this build, and Shelly is a runtime
dependency. The bundled configuration uses `{shelly} (Shelly)`.

The query runs directly without a shell. Failed commands, malformed JSON,
and invalid package records report a detection error; they do not fall back
to Pacman or display a fabricated count. Other subprocess detectors retain
their upstream exit-status behavior. The `test-shelly.py` fixtures cover
counting, totals, output formats, empty and changing inventories, failure
handling, and disabled detection using a PATH without Pacman.

The package installs the configuration and logos in
`/usr/share/devario/fastfetch/`, matching the Devario OS image. The default
logo is `devario-logo.png`; the legacy `devario-fish.txt` remains a copy of
`fish-bold.txt`. The system configuration at
`/etc/xdg/fastfetch/config.jsonc` links to the shared configuration, so plain
`fastfetch` uses the same branding as the Devario terminal welcome display.
The ISO supplies the Bash/Fish startup hooks; this package supplies their
configuration and artwork without editing users' shell startup files.

Try the other designs with:

```sh
fastfetch --logo-type file --logo /usr/share/devario/fastfetch/fish-striped.txt
fastfetch --logo-type file --logo /usr/share/devario/fastfetch/fish-compact.txt
```

For a persistent personal selection, copy the system configuration to
`~/.config/fastfetch/config.jsonc` and change `logo.source` to the desired
logo's full path. Personal configuration takes precedence. Files under
`/usr/share/devario/fastfetch/` are package-owned defaults and should not be
edited directly.

Build and check with the normal Devario package worker:

```sh
shelly build --review-only --json ./devario-core/fastfetch/PKGBUILD
shelly build --isolated --check ./devario-core/fastfetch/PKGBUILD
```

Shelly's static review may flag the backticks in the striped and compact
ASCII art as dynamic commands. These files are installed as non-executable
text and read by Fastfetch's `file` logo renderer; they are never sourced by
a shell. `check()` runs the upstream tests, Shelly regression fixtures,
checks image features, and renders all three text logos with the bundled
configuration.

Older ISO installations can already contain these paths as unowned overlay
files. Before the first package upgrade, reconcile those specific files with
the package through the deployment workflow; an unowned-file conflict must
not be handled with a blanket overwrite. Subsequent upgrades use normal
package ownership. This source update does not publish a signed repository
artifact.

When changing the branding, keep the matching files in
`devario-os/iso/late-airootfs/usr/share/devario/fastfetch/` synchronized and
regenerate source checksums and `.SRCINFO`.
