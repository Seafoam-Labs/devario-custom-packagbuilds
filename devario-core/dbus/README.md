# D-Bus for Shelly

Based on [Arch's dbus recipe](https://gitlab.archlinux.org/archlinux/packaging/packages/dbus/-/blob/main/PKGBUILD),
this builds `1.16.2-2` as `dbus`, `dbus-daemon-units`, and `dbus-docs`.
The main package explicitly provides `libdbus-1.so=3-64`, verified against the
installed ELF64 library's `libdbus-1.so.3` SONAME during packaging.

Keep the patch, hook, and public key with the recipe. The signed upstream Git
tag remains verified. The included Arch-packaged key has primary fingerprint:

```text
DA98F25C0871C49A59EAFF2C4DE8FF2A63C7CC90  Simon McVittie
```

As the Remora worker account, import the key before invoking Shelly:

```sh
gpg --import ./dbus/DA98F25C0871C49A59EAFF2C4DE8FF2A63C7CC90.asc
shelly build --isolated --check ./dbus/PKGBUILD
```

Source verification and a native Shelly build succeeded: 26 tests passed and
two were skipped. All three split archives were produced. See
[the dependency build guide](../DEPENDENCY-BUILDS.md) for isolated-build limits
and publishing the updated ABI provision.
