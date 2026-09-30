#!/usr/bin/env python3
"""Read-only inventory audit of saved repository metadata and local OS inputs."""
import csv
import ctypes
import ctypes.util
from collections import defaultdict
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import re
import tarfile

HERE = Path(__file__).resolve().parent
OS = Path('/home/zoey/Devario/devario-os')
lib = ctypes.CDLL(ctypes.util.find_library('alpm'))
cmp = lib.alpm_pkg_vercmp
cmp.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
cmp.restype = ctypes.c_int


def read_db(name):
    result = []
    with tarfile.open(HERE / (name + '.db')) as archive:
        for member in archive:
            if not member.name.endswith('/desc'):
                continue
            fields = {}
            for block in archive.extractfile(member).read().decode().strip().split('\n\n'):
                lines = block.splitlines()
                fields[lines[0].strip('%')] = lines[1:]
            result.append(dict(name=fields['NAME'][0], version=fields['VERSION'][0],
                               repository=name, fields=fields))
    return result


def split_req(req):
    return re.fullmatch(r'([^<>=]+)(>=|<=|=|>|<)?(.*)', req).groups()


def satisfies(req, name, version):
    n, op, v = split_req(req)
    if n != name:
        return False
    if not op:
        return True
    if not version:
        return False
    c = cmp(version.encode(), v.encode())
    return {'=': c == 0, '>=': c >= 0, '<=': c <= 0, '>': c > 0, '<': c < 0}[op]


core, seafoam = read_db('devario-core'), read_db('seafoam-labs')


@lru_cache(None)
def candidates(req, combined=False):
    found = []
    for repo in ([core, seafoam] if combined else [core]):
        exact, virtual = [], []
        for p in repo:
            if satisfies(req, p['name'], p['version']):
                exact.append(p)
            elif any(satisfies(req, *provide.partition('=')[::2])
                     for provide in p['fields'].get('PROVIDES', [])):
                virtual.append(p)
        found.extend(exact + virtual)
    return found


def closure(seeds, combined=False, rebuild=False):
    pending = list(seeds)
    seen, missing, selected = set(), defaultdict(set), {}
    while pending:
        req, parent = pending.pop()
        if (req, parent) in seen:
            continue
        seen.add((req, parent))
        available = candidates(req, combined)
        if not available:
            missing[req].add(parent)
            continue
        p = next((p for p in available if p['name'] in selected), available[0])
        if p['name'] in selected:
            continue
        selected[p['name']] = p
        keys = ['DEPENDS'] + (['MAKEDEPENDS', 'CHECKDEPENDS'] if rebuild else [])
        for key in keys:
            pending.extend((d, p['name'] + ':' + key.lower()) for d in p['fields'].get(key, []))
    return {'selected': sorted(selected),
            'missing': {k: sorted(v) for k, v in sorted(missing.items())}}


def manifest(file):
    snapshot = 'iso-packages.x86_64' if file.startswith('iso/') else file
    return [line.strip() for line in (HERE / snapshot).read_text().splitlines()
            if line.strip() and not line.lstrip().startswith('#')]


iso = manifest('iso/packages.x86_64')
checklist = manifest('repository-packages.x86_64')
local = json.loads((HERE / 'local-srcinfo.json').read_text())
recipe_seeds = defaultdict(list)
for recipe, entry in local.items():
    assert entry['returncode'] == 0, recipe
    for line in entry['srcinfo'].splitlines():
        key, sep, value = line.strip().partition(' = ')
        if key in ('depends', 'makedepends', 'checkdepends'):
            recipe_seeds[key].append((value, recipe + ':' + key))

sections = {
    'iso_runtime_core': closure([(r, 'ISO package list') for r in iso]),
    'iso_runtime_configured_repos': closure([(r, 'ISO package list') for r in iso], True),
    'repository_checklist_core': closure([(r, 'repository checklist') for r in checklist]),
    'local_recipe_runtime_core': closure(recipe_seeds['depends']),
    'local_recipe_build_core': closure(recipe_seeds['makedepends']),
    'local_recipe_checks_core': closure(recipe_seeds['checkdepends']),
    'builder_bootstrap_core': closure([(r, 'build-packages-nspawn.sh bootstrap')
                                     for r in ['base-devel', 'git', 'sudo', 'python-jsonschema']]),
    'all_published_core_runtime': closure([(p['name'], 'published package') for p in core]),
    'source_rebuild_checklist_core': closure([(r, 'repository checklist') for r in checklist], rebuild=True),
}

rows = []
for section, data in sections.items():
    for req, parents in data['missing'].items():
        base = split_req(req)[0]
        same_name = candidates(base)
        kind = 'version/provision mismatch' if same_name else ('missing provision' if '.so' in base else 'missing package/provider')
        other = candidates(req, True)
        rows.append(dict(section=section, requirement=req, reason=kind, required_by='; '.join(parents),
                         core_versions='; '.join(p['name'] + '=' + p['version'] +
                                                (' [provides: ' + ', '.join(p['fields'].get('PROVIDES', [])) + ']'
                                                 if p['name'] != base else '') for p in same_name),
                         available_in_configured_repos='; '.join(p['repository'] + '/' + p['name'] + '=' + p['version'] for p in other)))

metadata = {
    'generated_utc': datetime.now(timezone.utc).isoformat(),
    'database_urls': {'devario-core': 'https://repo.seafoam-labs.org/devario-core/x86_64/devario-core.db',
                      'seafoam-labs': 'https://repo.seafoam-labs.org/x86_64/seafoam-labs.db'},
    'database_sha256': {n: hashlib.sha256((HERE / (n + '.db')).read_bytes()).hexdigest()
                        for n in ['devario-core', 'seafoam-labs']},
    'package_counts': {'devario-core': len(core), 'seafoam-labs': len(seafoam)},
    'iso_requested': iso, 'repository_checklist': checklist,
    'local_recipe_direct_requirements': dict(recipe_seeds),
    'sections': sections,
}
(HERE / 'results.json').write_text(json.dumps(metadata, indent=2) + '\n')
with (HERE / 'missing-requirements.csv').open('w') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)

lines = ['DEVARIO-CORE PACKAGE AVAILABILITY AUDIT', metadata['generated_utc'], '',
         f'Live database snapshot: {len(core)} core packages; {len(seafoam)} seafoam-labs packages.',
         f'Community ISO: {len(iso)} explicit packages; repository checklist: {len(checklist)} packages.',
         'Sources: ' + '; '.join(metadata['database_urls'].values()), '',
         'Scope: Community ISO, local default OS package recipes, builder bootstrap, and repository checklist.',
         'Version constraints and virtual provides checked using libalpm version comparison.',
         'Runtime traversal stops at unavailable packages; their unknown dependencies cannot be inferred.',
         'Local recipe requirements are audited separately, without pretending those packages are published.',
         'Build/check sections include runtime dependencies of the requested build/check tools.',
         'The source-rebuild section recursively includes MAKEDEPENDS and CHECKDEPENDS recorded in the DB.',
         'It is a broader source-rebuild inventory, not a list of packages to install in the ISO.',
         'Optional dependencies and Managed edition are excluded. Database declarations are not proof of',
         'archive availability, signature validity, ABI compatibility, or an installable transaction.',
         'Provider alternatives and conflicts are not solved as a package-manager transaction.',
         'No packages were installed or built.', '',
         'Important: packages/linux-cachyos-lts is absent locally although build-packages.sh names it.',
         'A packages/linux-devario recipe exists; it was excluded because the current ISO/build list uses CachyOS LTS.',
         'The kernel packages are published, but their intended local source recipe cannot be audited here.', '',
         'Important: spandsp is published, but advertises no libspandsp.so provision required by pipewire-audio.',
         'Verify the library ABI, add the correct provision, rebuild, and republish its metadata.',
         'seafoam-labs supplies Shelly, Noctalia, and Noctalia Greeter by name; this does not establish',
         'compatibility with the local pinned Devario recipes. Published Shelly requires pacman, currently',
         'unresolved in both repositories. The local devario-alpm-runtime recipe intends to provide it.', '']
titles = {
    'iso_runtime_core': '1. Unresolved ISO requirements in devario-core (direct plus recursive runtime)',
    'iso_runtime_configured_repos': '2. Unresolved ISO requirements using both configured repositories',
    'repository_checklist_core': '3. Unresolved repository checklist requirements in devario-core',
    'local_recipe_runtime_core': '4. Local OS recipe runtime requirements unresolved in devario-core',
    'local_recipe_build_core': '5. Local OS recipe build requirements unresolved in devario-core',
    'local_recipe_checks_core': '6. Local OS recipe test requirements unresolved in devario-core',
    'builder_bootstrap_core': '7. Builder bootstrap requirements unresolved in devario-core',
    'all_published_core_runtime': '8. Runtime gaps across ALL published core packages (broader than OS)',
    'source_rebuild_checklist_core': '9. Recursive source rebuild/check inventory (broader than ISO assembly)',
}
for section, data in sections.items():
    lines.extend([titles[section], f"{len(data['missing'])} distinct unresolved requirements", ''])
    for row in (r for r in rows if r['section'] == section):
        lines.append(row['requirement'] + ' | required by: ' + row['required_by'])
        if row['core_versions']:
            lines.append('  Published core version: ' + row['core_versions'])
        if row['available_in_configured_repos']:
            lines.append('  Available candidate: ' + row['available_in_configured_repos'])
    lines.append('')
lines += ['Reproduce: python audit.py (requires Python and libalpm, reads saved DBs and saved local manifests).',
          'The saved local-srcinfo.json was generated with makepkg --printsrcinfo for 14 default OS recipes.',
          'results.json preserves manifest inputs, selected names, dependency parents, hashes, and source URLs.',
          'missing-requirements.csv is the filterable list; section counts overlap and must not be added together.']
(HERE / 'report.txt').write_text('\n'.join(lines) + '\n')
for key, data in sections.items():
    print(key, len(data['missing']))
