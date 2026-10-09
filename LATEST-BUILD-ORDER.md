# Build order — latest hook changes only

This queue covers the **three recipes changed in the 2026-10-08 Shelly/RLPM hook audit**, producing **43 packages**. Its scope comes from [the change manifest](audits/hook-layout-2026-10-08/changes.json).

## Prerequisites

Use a working Devario builder with the dependencies declared in each recipe available inside its isolated build root. This queue assumes those dependencies have already been built and made available through the builder repository.

Neovim's Lua, tree-sitter, and other dependencies must be available before its rebuild. TeX Live needs `texlive-bin` and `subversion`; its output dependencies also include `perl` and `dvisvgm`. If the TeX Live/`dvisvgm` cycle still needs bootstrapping, resolve it using the [existing bootstrap plan](audits/application-expansion-2026-10-08/bootstrap-order.txt) before using this queue. The [full application build order](BUILDER-ORDER.md) covers the earlier expansion; it does not include Neovim's dependency closure.

## Stage 01 — rebuild the changed recipes

There is no dependency between these three recipe bases, so they may build in parallel in separate roots once their prerequisites are satisfied. **Build each recipe once.** All 41 `texlive-*` packages below are outputs of the same `texlive-texmf` recipe.

| Package | Version | Build recipe |
| --- | --- | --- |
| `neovim` | 0.12.5-2 | [devario-development/neovim](devario-development/neovim/PKGBUILD) |
| `texinfo` | 7.3-2 | [isolation-builder/texinfo](isolation-builder/texinfo/PKGBUILD) |
| `texlive-basic` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-bibtexextra` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-binextra` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-context` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-doc` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-fontsextra` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-fontsrecommended` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-fontutils` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-formatsextra` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-games` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-humanities` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-langarabic` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-langchinese` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-langcjk` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-langcyrillic` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-langczechslovak` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-langenglish` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-langeuropean` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-langfrench` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-langgerman` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-langgreek` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-langitalian` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-langjapanese` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-langkorean` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-langother` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-langpolish` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-langportuguese` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-langspanish` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-latex` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-latexextra` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-latexrecommended` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-luatex` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-mathscience` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-meta` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-metapost` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-music` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-pictures` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-plaingeneric` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-pstricks` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-publishers` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |
| `texlive-xetex` | 2026.1-3 | [devario-utilities/texlive-texmf](devario-utilities/texlive-texmf/PKGBUILD) |

## Publish after the builds

Publish the rebuilt packages and refresh repository metadata before using them in new build roots or images. Publish all TeX Live collection outputs together so their hook targets and shared metadata path remain consistent.

Machine-readable queue: [package-build-stages.tsv](audits/hook-layout-2026-10-08/package-build-stages.tsv). This document specifies the rebuild order; it does not record completed builds or publication.
