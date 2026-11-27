# zig-mcp

MCP server that serves Zig standard library and builtin-function documentation
to coding agents. Upstream: <https://github.com/zig-wasm/zig-mcp> (npm package
`zig-mcp`). Documentation is generated from the locally installed Zig via
`zig std`, so the `zig` runtime dependency must match the toolchain you want
docs for.

## Local patch: `wasm-instance-cache.patch`

Upstream 1.4.1 re-reads `main.wasm`, instantiates a **new** WASM module, and
re-unpacks the entire std `sources.tar` on *every* `search_std_lib` /
`get_std_lib_item` call (`dist/std.js`). Each instance retains a full parsed
copy of the standard library (~75–110 MB resident, plus a multi-GB virtual
guard reservation), and V8 does not reclaim them promptly. A handful of queries
grows the process by hundreds of MB.

The patch instantiates and unpacks once per process and reuses that instance
for all calls. Query execution after initialization is synchronous, so
concurrent requests safely share the single instance. Failed initialization is
not cached, so a later call can retry.

## Using the packaged server

The package installs `/usr/bin/zig-mcp`. Point the editor at it instead of
`npx -y zig-mcp@latest`; this also drops the ~115 MB `npm exec` wrapper process
per window. Example Zed `settings.json`:

```json
{
  "context_servers": {
    "zig-mcp": {
      "command": { "path": "zig-mcp", "args": [] }
    }
  }
}
```

Note that Zed spawns one server per window; the patch caps each at roughly
baseline + one WASM instance instead of growing per query.
