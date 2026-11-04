# Mesa 26.3.0-rc3

Bleeding-edge Mesa, based on `devario-core/mesa`, with the same split package
names and epoch. Packaged version: `1:26.3.0rc3-2`.

The upstream release contains `.EXT_image_drm_format_modifier = true` in
`src/amd/vulkan/radv_physical_device.c`, removing the GFX9 gate that excluded
the RX 590. No local RADV patch is needed. Aqueous buffer import and presentation
on the RX 590 still require runtime testing.

Build from this directory with Shelly:

```sh
shelly build PKGBUILD --isolated --sync-deps
```

For RX 590 testing, publish/install the matching `mesa`, `vulkan-radeon`, and
`vulkan-mesa-implicit-layers` outputs (plus any other installed Mesa splits).
The RADV change is delivered by `vulkan-radeon`. This recipe builds the 64-bit
stack; 32-bit Mesa is packaged separately.

Source: <https://archive.mesa3d.org/mesa-26.3.0-rc3.tar.xz> and its detached
signature. SHA-256 and BLAKE2 checksums are pinned in the PKGBUILD, including
the new `mach2` Rust subproject.
