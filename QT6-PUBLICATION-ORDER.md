# Qt6 publication order

Order to build and publish the `qt6-*` family on a new Qt release. Derived from the
`depends` plus `makedepends` of the 33 recipes in this tree (see
[AGENTS.md](AGENTS.md) for the `.SRCINFO` rules).

Qt dependencies in this family are `>=`, so a module needs its dependencies published
**at the new version** before it can build. Qt only promises backwards binary
compatibility within a major version, so a newer module against an older base is not
allowed. The graph is acyclic: `qt6-base` depends on no Qt package and publishes first,
and `qt6-translations` sits at the far end. The one `=` pin, `qt6-xcb-private-headers`
against the `qt6-base` pkgbase, is safe because both outputs ship from a single build.

## Tiers

Repo in parentheses: `c` is `devario-core`, `l` is `devario-libs`. Finish a tier (publish
plus metadata refresh) before starting the next. Names inside a tier are independent, so
they can publish in parallel in separate roots.

| Tier | Packages |
| --- | --- |
| 0 | `qt6-base` (c) |
| 1 | `qt6-connectivity` (l), `qt6-imageformats` (c), `qt6-languageserver` (c), `qt6-networkauth` (l), `qt6-serialport` (l), `qt6-shadertools` (c), `qt6-svg` (c) |
| 2 | `qt6-declarative` (c), `qt6-serialbus` (l) |
| 3 | `qt6-3d` (l), `qt6-5compat` (l), `qt6-canvaspainter` (l), `qt6-charts` (l), `qt6-datavis3d` (l), `qt6-positioning` (l), `qt6-quicktimeline` (l), `qt6-remoteobjects` (l), `qt6-scxml` (l), `qt6-sensors` (l), `qt6-tools` (c), `qt6-wayland` (l), `qt6-webchannel` (l), `qt6-websockets` (l) |
| 4 | `qt6-httpserver` (l), `qt6-location` (l), `qt6-quick3d` (l), `qt6-translations` (c), `qt6-webengine` (l) |
| 5 | `qt6-graphs` (l), `qt6-multimedia` (l), `qt6-webview` (l) |
| 6 | `qt6-speech` (l) |

## Critical chain

The long pole, and the order that matters most if you publish serially:

```
qt6-base -> qt6-shadertools, qt6-languageserver, qt6-svg -> qt6-declarative -> qt6-tools -> qt6-translations
```

Five of the seven tiers sit on this path. `qt6-translations` is last because it needs
`qt6-tools`, which needs `qt6-declarative`, which needs three tier 1 modules. Everything
else is off-chain and can lag behind.

## Notes

- `qt6-base` is a split recipe. Build it once and publish `qt6-base` plus
  `qt6-xcb-private-headers` together.
- `qt6-translations` is `arch=(any)`. Rebuilding it against a newer base is optional unless
  its own version changed; a same-version rebuild produces an identical filename, which the
  package comparison rejects.
- `qt6-webengine` is the slowest build in tier 4 and pulls in `qt6-tools` too, so it is
  worth starting as soon as tier 3 is published.
- Consumers outside the family (KF6 frameworks, `qt6ct`, `qt6pas`) use `>=` floors and are
  not in this order. They need rebuilds for ABI reasons, not dependency reasons.

## Regenerate after recipe edits

```sh
python3 - <<'EOF'
import re, glob, os
pkgs = {}
for path in glob.glob('*/qt6-*/PKGBUILD'):
    name = os.path.basename(os.path.dirname(path))
    text = open(path).read()
    deps = set()
    for arr in ('depends', 'makedepends'):
        for m in re.finditer(arr + r'=\((.*?)\)', text, re.S):
            deps |= set(re.findall(r'qt6-[a-z0-9-]+', m.group(1)))
    for m in re.finditer(r'depends\+=\((.*?)\)', text, re.S):
        deps |= set(re.findall(r'qt6-[a-z0-9-]+', m.group(1)))
    deps.discard(name)
    pkgs[name] = deps
tier, order = 0, []
while pkgs:
    ready = sorted(p for p, d in pkgs.items() if not (d & pkgs.keys()))
    if not ready:
        print('CYCLE among:', sorted(pkgs)); break
    order.append((tier, ready)); [pkgs.pop(p) for p in ready]; tier += 1
for t, ps in order:
    print(f'Tier {t}: ' + ', '.join(ps))
EOF
```
