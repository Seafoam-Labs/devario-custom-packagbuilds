# riscv64-linux-gnu-gcc-bootstrap

Seed for `../riscv64-linux-gnu-gcc`, which is one side of a cycle: the cross GCC depends on
`riscv64-linux-gnu-glibc`, and the cross glibc depends on the cross GCC, so the worker plan cannot
provision either while none is published. This recipe builds the stage-1 cross compiler and
publishes it as `riscv64-linux-gnu-gcc 16.2.1-0.1`; `riscv64-linux-gnu-glibc` then builds over it,
and the real recipe follows at `16.2.1-1`.

Stage 1 builds only `all-gcc` and `all-target-libgcc` with `--without-headers --with-newlib`,
`--disable-shared` and `--disable-threads`. It provides the C and C++ frontends but only libgcc
for the target, so it is compile-only for target code; glibc is the only intended consumer.
Nothing else should build against it, and it must not stay published after the real compiler
builds.

Order: `setconf`, `riscv64-linux-gnu-linux-api-headers`, `riscv64-linux-gnu-binutils`, this seed,
`riscv64-linux-gnu-glibc`, the real `riscv64-linux-gnu-gcc`, then `edk2`, `seabios`,
`virtiofsd` and `virtme-ng`. `setconf` is an existing unpublished recipe, not a seed; the last
three are the qemu runtime closure, not part of this cycle.

The version is deliberately below the real `16.2.1-1`, so the real package replaces the seed on
publish. The source is the same pinned commit and checksums as the real recipe.

Validation: `.SRCINFO` regenerates identically and `shelly build --review-only` exits 0. No
isolated or worker build has run.

Retirement: this recipe publishes under the ALPM name `riscv64-linux-gnu-gcc` itself, and worker
removals evict every repository entry recorded on the removed row, so a Remove against this recipe
after the real GCC has published would unpublish the real package. Retire the directory instead.