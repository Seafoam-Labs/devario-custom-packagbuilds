# TPM 2 tools for Devario

Builds `tpm2-tools` version `5.8-2`, based on
[Arch packaging commit 1dbf6098bd482f24fbe0697d42605894e18ef201](https://gitlab.archlinux.org/archlinux/packaging/packages/tpm2-tools/-/commit/1dbf6098bd482f24fbe0697d42605894e18ef201).
This supplies the TPM tools required by Devario's dracut package.

The recipe retains Arch's signed upstream tag, SHA-512 and BLAKE2 checksums,
public keys under `keys/pgp/`, disabled LTO, and removal of the two integration
tests affected by upstream issue 3606. Runtime library dependencies use
explicit Shelly-compatible ABI requirements. Publish the existing
`tpm2-tss` 4.2.0-3 recipe before building; the inspected repository's older
package lacks those versioned provisions.

`cmocka` is a build dependency because `--enable-unit` requires it even if the
worker skips `check()`. The repository databases inspected on 2026-10-02
also lack `autoconf-archive`; checks additionally require missing `expect`,
`swtpm`, and `tpm2-abrmd`. Keep the checks enabled on a worker with those
dependencies and simulator support.

Validation: Bash syntax, makepkg and Shelly metadata, Shelly review, source
checksums, and upstream Git-tag signature passed. Compilation and the TPM
unit/integration tests have not been run. See the
[dependency build guide](../../DEPENDENCY-BUILDS.md) for commands and key import.
