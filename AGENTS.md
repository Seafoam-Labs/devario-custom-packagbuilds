# AGENTS.md

## Shelly: .SRCINFO and source checksums

Run from the package directory (the one holding `PKGBUILD`).

- `shelly build --updpkgsums PKGBUILD` — rewrites source checksums in `PKGBUILD`
  **and** the adjacent `.SRCINFO` in place. Use after editing any `source=()` file.
- `shelly build --makesrcinfo PKGBUILD` — prints SRCINFO to **stdout only**; it does
  not write the adjacent `.SRCINFO`. To update the file, redirect:
  `shelly build --makesrcinfo PKGBUILD >.SRCINFO`. Use after metadata-only edits
  (depends/makedepends/pkgver/…) with no source change.

Both prompt for confirmation and default to No; `--no-confirm` answers No and
cancels, so pipe `y`:
`printf 'y\n' | shelly build --makesrcinfo PKGBUILD >.SRCINFO`
