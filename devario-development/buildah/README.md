# buildah

## Circular dependency on `containers-common` and bootstrapping

Due to a strict requirement in terms of version at runtime and related compatibility checks performed during build, our `buildah` package have a circular dependency on our `containers-common` package. This eventually requires a bootstrap dance with the `containers-common` package on version bump.

See the [`containers-common` README](https://gitlab.archlinux.org/archlinux/packaging/packages/containers-common/-/blob/main/README.md) for more details and the bootstrapping procedure.
