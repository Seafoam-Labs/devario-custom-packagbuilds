# Paseo with native Zig editing

This recipe builds Paseo 0.15.0 from its checksummed upstream source archive
and packages the desktop app, daemon, and CLI as `paseo 0.15.0-3`.

`0001-native-zig-editor-support.patch` registers `.zig` and `.zon` in the shared
language registry. The editor and static source/diff previews gain syntax
highlighting, with delimiter indentation and line-comment metadata in the editor.
Highlighting works without Zig or ZLS installed.

`0002-native-zls-integration.patch` connects the built-in web/desktop source
editor to ZLS through Paseo's daemon protocol. It adds:

- Completion, including snippets and additional text edits; use Ctrl+Space.
- Inline diagnostics, gutter markers, and a Problems panel.
- Hover documentation.
- Go to definition with F12 or Ctrl/Cmd-click.
- Find references with Shift+F12 and a clickable results list.
- Status, error reporting, and a Restart ZLS button.

Install compatible Zig and ZLS packages with Shelly on the **daemon host**.
The integration requires matching major/minor release series and rejects mixing
stable and development builds; nightly versions must also be mutually compatible.
By default it uses `zig` and `zls` from the daemon's PATH. Set `PASEO_ZIG_PATH`
and `PASEO_ZLS_PATH` in the daemon environment to select other executables, then
restart the daemon. Remote hosts must run this patched daemon too. No Editor Plus
plugin is required. These language features apply to the web/desktop editor;
the native mobile editor only retains highlighting.

ZLS uses the nearest `build.zig` or `build.zig.zon` within the opened workspace.
Its usual configuration and the project's `check` step control compiler/build
diagnostics; syntax diagnostics also work in standalone files. Navigation can
open imported files and the standard library. Cross-file jumps select the target
line, while same-file jumps select the precise range.

Each open buffer gets an isolated ZLS process, so different clients' unsaved
changes cannot overwrite each other. Edits are synchronized before queries,
stale results are discarded, and processes close on editor/connection shutdown
or idle expiry. Imported files' unsaved changes in another buffer become visible
after saving. ZLS operations require the daemon's workspace-write permission,
as analyzing project builds can execute build scripts. Rename and formatting
commands are not part of this patch.

Build with Shelly:

```sh
shelly build --isolated --check ./devario-development/paseo/PKGBUILD
```

The build needs network access for the upstream lockfile's JavaScript
dependencies and pinned Electron runtime. Paseo itself is compiled from source;
Electron and upstream native dependency prebuilds remain bundled. Caches stay
inside `srcdir`. Dependency setup skips mobile downloads and Git hooks, runs
selected desktop native setup scripts, and applies upstream dependency patches.
The installed paths remain `/opt/Paseo`, `/usr/bin/paseo-desktop`, and
`/usr/bin/paseo`. Shelly manages updates.

The recipe's `check()` runs highlighting, protocol, document synchronization,
UTF-16 position, LSP transport, authorization, real-ZLS, and daemon round-trip
tests. It requires Zig and ZLS, including a working Zig `check` build step.
Browser tests additionally cover completion acceptance, diagnostics display,
navigation, restart/reconnect, and editor cleanup; they run separately with
Playwright Chromium. A full isolated Shelly package build and graphical Electron
smoke test have not been run.

Validation completed locally: both patches apply to a fresh source archive and
`npm ci` accepts the patched lockfile; app/server typechecks, all 146 recipe tests,
and three browser tests pass. The renderer, server, CLI, and Electron main
process compile, Electron Builder produces the Linux bundle, and `package()`
stages it successfully. The staged CLI reports `0.15.0`; its archive includes the
ZLS service and protocol, and its renderer includes the ZLS controls. Checksums,
shell syntax, desktop metadata, and Shelly-generated `.SRCINFO` are verified.
Shelly review reports the npm build commands and misidentifies TypeScript
template strings inside patches as dynamic shell commands.
