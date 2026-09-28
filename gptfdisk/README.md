# gptfdisk for Shelly

This recipe builds `gptfdisk 1.0.10-3`, based on
[Arch's packaging](https://gitlab.archlinux.org/archlinux/packaging/packages/gptfdisk/-/blob/main/PKGBUILD).

Shelly's function-body parser misinterprets the first brace in the valid Bash
word `{{,c,s}gdisk,fixparts}.8` as a structural opening brace. It then includes
the function's closing brace in the extracted body. Wrapping that body in
`__shelly_step()` produces an extra closing brace and the reported
`shelly-step: syntax error near unexpected token '}'` during packaging.
The reported line number belongs to the generated script, not the PKGBUILD.

The workaround lists `gdisk.8 cgdisk.8 sgdisk.8 fixparts.8` explicitly. This
installs exactly the same files while avoiding the parser bug. Upstream source,
checksum, dependencies, compilation, and tests are unchanged; the package
release is bumped from 2 to 3.

From the repository root:

```sh
shelly build --review-only --json ./gptfdisk/PKGBUILD
shelly build --isolated --check ./gptfdisk/PKGBUILD
```

Validation: reproduced the syntax error with the original packaging commands
and dummy input files using local Shelly `3.1.6r4747.g8d61a9e-1`. Replacing
only the nested man-page expansion produced a package successfully. This
tests packaging syntax, not gptfdisk compilation. The full gptfdisk build and
isolated worker run have not been performed.
