# Inxi for Devario

Builds `inxi` version `3.3.41.1-3`, based on
[Arch packaging commit 73f0a4d86fa7518e4b76dd4e7b9c075a15349cf6](https://gitlab.archlinux.org/archlinux/packaging/packages/inxi/-/commit/73f0a4d86fa7518e4b76dd4e7b9c075a15349cf6).
This supplies the system-information command required by `devario-base`.

The Codeberg archive for release `3.3.41-1` no longer matches the checksum
recorded by Arch. Its complete file tree was compared with upstream release
commit `d9941a4ed84fdc20737cc44e987a92d4cd0d8d5c` and found identical.
The recipe pins that commit and checksums its Git export instead of depending
on the changing generated archive. `git` is declared as a build dependency.
The CLI and manual are installed with the original permissions.

Validation: source checksum, Bash syntax, makepkg and Shelly metadata, Shelly
review, Perl syntax check, and a local makepkg package build passed. The staged
command runs with `--version`. An isolated worker build has not been run.
See the [dependency build guide](../../DEPENDENCY-BUILDS.md) for commands.
