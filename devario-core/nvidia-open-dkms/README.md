# nvidia-open-dkms for Shelly

Builds `nvidia-open-dkms 615.78.08-1` as a standalone package matching
`devario-core/nvidia-utils` and `devario-libs/lib32-nvidia-utils`. It requires
`dkms` and exactly `nvidia-utils=615.78.08`; the utilities package's `pkgrel`
may differ. It does not require a new Linux kernel release.

## Sources and packaging

Adapted from the `nvidia-open-dkms` split output and DKMS preparation in
[Arch's nvidia-utils PKGBUILD](https://gitlab.archlinux.org/archlinux/packaging/packages/nvidia-utils/-/blob/main/PKGBUILD),
version `615.78.08-1`. The reference recipe's SHA-256 is
`77dde84094df5ef1caee8630d942508d532f8f40b0255355e8930998ab42be3e`.
The bundled `LICENSE` preserves the Arch packaging license.

The recipe downloads NVIDIA's official `NVIDIA-kernel-module-source` archive
and retains Arch's SHA-512 checksum. It packages the full source tree under
`/usr/src/nvidia-615.78.08`, completes the upstream DKMS template for all five
modules, and installs the upstream license. The README and GPU support table
remain in the source tree for Devario's installed-target validation.

DKMS builds modules for installed kernels using their matching headers when
the package is installed. This recipe does not build or install modules on
the packaging host. The matching `nvidia-utils` supplies firmware and
userspace libraries. No binary NVIDIA `.run` download is needed here.

## Build and publish

Copy this directory to the Remora worker. From this repository's root:

```sh
shelly build --review-only --json ./devario-core/nvidia-open-dkms/PKGBUILD
shelly build --isolated --check ./devario-core/nvidia-open-dkms/PKGBUILD
```

Shelly review reports dynamic-command warnings for the literal DKMS `nproc`
substitution and the module-index arithmetic. These are intentional: `nproc`
must run when DKMS reads its configuration, and the arithmetic indexes the
five module declarations. Review these findings before accepting the build.

After editing the recipe, regenerate `.SRCINFO` with Shelly:

```sh
shelly build --makesrcinfo ./devario-core/nvidia-open-dkms/PKGBUILD > ./devario-core/nvidia-open-dkms/.SRCINFO
```

Make matching `nvidia-utils` available to the isolated worker. Publish this
package with that version of `nvidia-utils` and, where used, matching
`lib32-nvidia-utils` and OpenCL packages. Upgrade the installed NVIDIA set in
one transaction. Keep the exact version dependency; do not relax it to allow
a mismatched driver. Remora's ordinary `pkgrel` rebuild cascade does not
change the NVIDIA source version.

For release monitoring, use `GitHubTags` with
`https://github.com/NVIDIA/open-gpu-kernel-modules`. Leave prefix, pattern,
replacement and published-version override empty; use the same optional
series policy as the utilities packages. Numeric tags alone do not identify
NVIDIA beta releases, so review a detected release before publishing.

## Validation

- Bash syntax and Shelly-generated `.SRCINFO`.
- Official source download verified against the retained SHA-512 checksum.
- Shelly review inspected; the two warnings above are understood.
- Successful unprivileged native Shelly build with `--check`, producing
  `nvidia-open-dkms-615.78.08-1-x86_64.pkg.tar.zst`.
- Archive dependency, conflict, provision, source layout and license checks.
- Generated DKMS configuration evaluated with a test kernel version; all five
  modules use the `kernel-open` build directory.
- Devario's actual `updated_support()` installer helper accepted the packaged
  README and extracted 834 PCI support entries for `615.78.08`.

There is no upstream `check()` suite in this packaging recipe. An isolated
build, actual DKMS compilation against target kernel headers, and GPU runtime
tests remain to be performed on the worker/test system. Before rollout,
verify DKMS success and, after reboot, `nvidia-smi`, graphics, suspend/resume,
and a 32-bit graphics application where multilib is installed. No host package
installation, module loading, or repository publication was performed during
the validation above.
