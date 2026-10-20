# dune-bootstrap

Seed for `../dune`. The dune release packages depend on `ocaml-csexp`, `ocaml-pp` and
`ocaml-re`, and all three build with dune, so the real recipe cannot be planned until some
repository publishes `dune`. This recipe builds only dune's vendored bootstrap (`boot/`, with
csexp, pp and re under `vendor/`) and packages `_boot/dune.exe` as `dune 3.24.2-1`; the real
recipe then builds over it as `dune 3.24.2-2`.

`depends` is reduced to `glibc` and `ocaml`: the bootstrap binary compiles projects with the
system OCaml and needs none of the libraries the release packages provide. It installs no
`dune-configurator` library, so it declares no `provides`.

Order: publish the `ocaml` pkgbase, then `ocaml-findlib`, then this seed, then `ocaml-result`,
`ocaml-csexp`, `ocaml-pp` and `ocaml-re`, then `dune`.

Retirement: this recipe publishes under the ALPM name `dune` itself, and worker removals evict
every repository entry recorded on the removed row, so a Remove run after the real dune has
published would unpublish the real package too. Retire the directory only while the real build
is in flight, or after confirming the removal rule has changed.