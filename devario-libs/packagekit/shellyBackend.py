#!/usr/bin/python3 -I
# SPDX-License-Identifier: GPL-2.0-or-later
"""PackageKit spawn protocol adapter for Shelly's native repository commands."""
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import tempfile

SHELLY = "/usr/bin/shelly"
ARCH = platform.machine()
PAGE_SIZE = 1000
NAME = re.compile(r"[A-Za-z0-9@_+][A-Za-z0-9@._+-]*\Z")


class BackendError(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def emit(*fields):
    # PackageKit's helper protocol is line- and tab-delimited. Metadata and
    # subprocess diagnostics must never be interpreted as additional records.
    print("\t".join(re.sub(r"[\x00-\x1f\x7f]", " ", str(field)) for field in fields), flush=True)


def environment():
    env = {
        "PATH": "/usr/bin:/usr/sbin", "HOME": "/root", "USER": "root", "LOGNAME": "root",
        "LC_ALL": "C.UTF-8",
        "XDG_CONFIG_HOME": str(Path(__file__).resolve().parent / "config"),
        "XDG_CACHE_HOME": "/var/cache/PackageKit/shelly",
        "XDG_DATA_HOME": "/var/lib/PackageKit/shelly/data",
        "XDG_STATE_HOME": "/var/lib/PackageKit/shelly/state",
    }
    for name in ("http_proxy", "https_proxy", "ftp_proxy", "no_proxy"):
        if name in os.environ:
            env[name] = os.environ[name]
    return env


def run_shelly(*args, query=False):
    command = [SHELLY, *args, "--config", "/etc/shelly.conf", "--no-confirm"]
    if query:
        command.append("--json")
    # Keep Shelly's human output out of the PackageKit protocol and bound the
    # diagnostic copied back on error. Never time out/kill a package transaction.
    with tempfile.TemporaryFile(mode="w+", encoding="utf-8") as out, \
            tempfile.TemporaryFile(mode="w+", encoding="utf-8") as err:
        result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                                env=environment(), check=False)
        if result.returncode:
            diagnostics = []
            for stream in (out, err):
                stream.flush()
                stream.seek(max(0, os.fstat(stream.fileno()).st_size - 4096))
                diagnostics.append(stream.buffer.read().decode("utf-8", errors="replace"))
            raise BackendError("transaction-error", f"Shelly {args[0]} failed ({result.returncode}): " + " ".join(diagnostics))
        if query:
            out.seek(0)
            text = out.read()
            # Empty search results are represented by no output in Shelly.
            return json.loads(text) if text.strip() else []


def rows(value):
    if not isinstance(value, list) or any(not isinstance(p, dict) for p in value):
        raise BackendError("internal-error", "Shelly returned an invalid package list")
    return value


def catalog(installed):
    result = []
    page = 1
    seen = set()
    while True:
        batch = rows(run_shelly("search", "standard", "--installed" if installed else "--available",
                                 "--show-hidden", "--limit", str(PAGE_SIZE), "--page", str(page), query=True))
        for package in batch:
            identifier = package_id(package, installed)
            if identifier in seen:
                raise BackendError("internal-error", "Shelly returned duplicate or repeated search pages")
            seen.add(identifier)
        result.extend(batch)
        if len(batch) < PAGE_SIZE:
            return result
        page += 1


def package_id(package, installed=False):
    name = package.get("Name", "")
    version = package.get("NewVersion", package.get("Version", ""))
    repo = "installed" if installed else package.get("Repository", "")
    if not isinstance(name, str) or not NAME.fullmatch(name) or \
            not isinstance(repo, str) or not NAME.fullmatch(repo) or \
            not isinstance(version, str) or not version or re.search(r"[\s;&|\x00-\x1f]", version):
        raise BackendError("internal-error", "Shelly returned invalid package identity fields")
    return f"{name};{version};{ARCH};{repo}"


def parse_ids(value):
    result = []
    for identifier in value.split("&"):
        parts = identifier.split(";")
        if len(parts) != 4 or not NAME.fullmatch(parts[0]) or not NAME.fullmatch(parts[3]) or \
                not parts[1] or re.search(r"[\s&|\x00-\x1f]", parts[1]) or parts[2] != ARCH:
            raise BackendError("package-id-invalid", "Invalid Shelly package identifier")
        result.append(identifier)
    if len(set(result)) != len(result):
        raise BackendError("package-id-invalid", "Duplicate package identifiers")
    return result


def filters(value):
    selected = set(value.split(";")) - {"", "none"}
    if selected - {"installed", "~installed"} or selected == {"installed", "~installed"}:
        raise BackendError("not-supported", "Only the installed package filter is supported")
    return selected


def candidates(filter_text):
    selected = filters(filter_text)
    local = catalog(True)
    if "~installed" not in selected:
        for package in local:
            yield package, True
    if "installed" not in selected:
        local_versions = {(p["Name"], p["Version"]) for p in local}
        for package in catalog(False):
            if (package["Name"], package["Version"]) not in local_versions:
                yield package, False


def emit_package(package, installed=False, info=None):
    emit("package", info or ("installed" if installed else "available"),
         package_id(package, installed), package.get("Description", ""))


def find_ids(identifiers, installed):
    available = {package_id(p, installed): p for p in catalog(installed)}
    for identifier in identifiers:
        if identifier not in available:
            raise BackendError("package-not-found", f"Package is unavailable or its version changed: {identifier}. Refresh and retry.")
    return [available[identifier] for identifier in identifiers]


def transaction(command, flag_text, id_text, *options):
    flags = set(flag_text.split(";")) - {"", "none", "only-trusted"}
    if flags:
        raise BackendError("not-supported", "Shelly does not expose these PackageKit transaction flags: " + ", ".join(sorted(flags)))
    identifiers = parse_ids(id_text)
    if command == "update-packages":
        updates = rows(run_shelly("list-updates", "standard", query=True))
        expected = {package_id(p): p for p in updates}
        if set(identifiers) != set(expected):
            raise BackendError("not-supported", "Select all current standard updates; partial upgrades are not supported. Refresh the update list and retry.")
        emit("status", "update")
        run_shelly("upgrade", "standard")
        local = {p["Name"]: p["Version"] for p in catalog(True)}
        if any(local.get(p["Name"]) != p["NewVersion"] for p in updates):
            raise BackendError("transaction-error", "The installed versions do not match the requested update set; check Shelly's logs.")
        for package in updates:
            emit_package(package, True)
    elif command == "install-packages":
        packages = find_ids(identifiers, False)
        targets = [f'{p["Repository"]}/{p["Name"]}' for p in packages]
        emit("status", "install")
        run_shelly("install", "standard", "--needed", *targets)
        local = {p["Name"]: p["Version"] for p in catalog(True)}
        if any(local.get(p["Name"]) != p["Version"] for p in packages):
            raise BackendError("transaction-error", "Shelly did not install all requested versions")
        for package in packages:
            emit_package(package, True)
    elif command == "remove-packages":
        if len(options) != 2 or any(option not in ("true", "false") for option in options):
            raise BackendError("internal-error", "Invalid removal options")
        packages = find_ids(identifiers, True)
        arguments = ["--cascade" if options[1] == "true" else "--no-cascade"]
        if options[0] == "true":
            arguments.append("--ripple")
        emit("status", "remove")
        for package in packages:
            emit_package(package, True, "removing")
        run_shelly("remove", "standard", *arguments, *[p["Name"] for p in packages])
        remaining = {p["Name"] for p in catalog(True)}
        if any(p["Name"] in remaining for p in packages):
            raise BackendError("transaction-error", "Shelly did not remove all requested packages")


def dispatch(command, *args):
    emit("allow-cancel", "false")
    emit("status", "query")
    if command in ("get-packages", "resolve", "search-name", "search-details"):
        filter_text, terms = args
        wanted = terms.split("&") if terms else []
        if command != "get-packages" and not wanted:
            raise BackendError("package-id-invalid", "No package names or search terms provided")
        for package, installed in candidates(filter_text):
            name = package["Name"]
            haystack = name + (" " + (package.get("Description") or "") if command == "search-details" else "")
            if command == "resolve" and name not in wanted:
                continue
            if command.startswith("search-") and not all(term.casefold() in haystack.casefold() for term in wanted):
                continue
            emit_package(package, installed)
    elif command == "get-details":
        identifiers = parse_ids(args[0])
        for installed in (True, False):
            selected = [i for i in identifiers if (i.split(";")[3] == "installed") == installed]
            if not selected:
                continue
            for identifier, package in zip(selected, find_ids(selected, installed)):
                emit("details", identifier, package.get("Description", ""),
                     " and ".join(package.get("Licenses") or []) or "unknown", "other",
                     package.get("Description", ""), package.get("Url", ""),
                     max(0, package.get("InstalledSize", 0)), max(0, package.get("DownloadSize", 0)))
    elif command == "get-updates":
        filters(args[0])
        for package in rows(run_shelly("list-updates", "standard", query=True)):
            emit_package(package, info="normal")
    elif command == "get-repo-list":
        filters(args[0])
        repos = run_shelly("search", "standard", "--repos", query=True)
        if not isinstance(repos, list) or any(not isinstance(r, str) or not NAME.fullmatch(r) for r in repos):
            raise BackendError("internal-error", "Shelly returned an invalid repository list")
        for repo in repos:
            emit("repo-detail", repo, repo, "true")
    elif command == "refresh-cache":
        if args not in (("true",), ("false",)):
            raise BackendError("internal-error", "Invalid refresh options")
        emit("status", "refresh-cache")
        run_shelly("sync", "standard", *(["--force"] if args[0] == "true" else []))
    elif command in ("install-packages", "remove-packages", "update-packages"):
        transaction(command, *args)
    else:
        raise BackendError("not-supported", f"Unsupported Shelly operation: {command}")


def execute(args):
    try:
        dispatch(*args)
    except BackendError as error:
        emit("error", error.code, str(error))
    except (OSError, ValueError, TypeError, KeyError) as error:
        emit("error", "internal-error", str(error))
    finally:
        emit("finished")


def main():
    if len(sys.argv) > 1:
        execute(sys.argv[1:])
    # PackageKit reuses a helper by sending tab-separated arguments on stdin.
    for line in sys.stdin:
        line = line.rstrip("\n")
        if not line or line == "exit":
            break
        execute(line.split("\t"))


if __name__ == "__main__":
    main()
