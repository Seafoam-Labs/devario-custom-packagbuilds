# Optional Python JSON Schema repository build chain

The 15 recipe directories (`python-*` plus `maturin`) under `devario-core/` stay
as the optional repository-managed chain for users who want these packages from
the repository. They are not required for ISO construction or the Remora upload
list; the stage order is readable from each recipe's `.SRCINFO` depends.
