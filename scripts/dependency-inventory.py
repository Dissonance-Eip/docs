#!/usr/bin/env python3
"""Regenerate the dependency and licence tables for planning/dependency-inventory.md.

Reads, from sibling checkouts of the ui and core repositories:

- ui/package.json and ui/package-lock.json (direct and transitive npm packages)
- ui/node_modules/<pkg>/package.json (licence, when installed)
- core/package.json and core/package-lock.json (build tooling)
- core/vendor/*/ (vendored C and C++ libraries, licence read from SPDX headers)

It prints Markdown to standard output. Paste the output into the "Generated
tables" section of planning/dependency-inventory.md and update the date there.

Usage:
    python3 scripts/dependency-inventory.py [--ui ../ui] [--core ../core]

Run `npm ci` in ui first so licences are read from node_modules. Without it the
script falls back to the licence recorded in package-lock.json.

Exits 1 when a GPL-family licence is found in any npm package, so it can be
used as a gate.
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re
import sys

# Strong copyleft: flagged. Weak (file-level) copyleft: listed separately.
STRONG = re.compile(r"\b(A|L)?GPL|SSPL|EUPL|CC-BY-SA", re.I)
WEAK = re.compile(r"\b(MPL|EPL|CDDL|CPL)\b|^(MPL|EPL|CDDL)", re.I)

# Direct dependencies that end up inside the packaged app even though npm
# lists them under devDependencies. Judgement, kept here so it is reviewable.
SHIPS_NOTE = {
    "electron": "yes (the Electron runtime is the app shell)",
    "tailwindcss": "no (its generated CSS file ships, the package does not)",
    "@tailwindcss/cli": "no (its generated CSS file ships, the package does not)",
}


def load_json(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def licence_of(pkg_dir: pathlib.Path, lock_entry: dict) -> str:
    manifest = pkg_dir / "package.json"
    if manifest.exists():
        value = load_json(manifest).get("license")
        if isinstance(value, dict):
            value = value.get("type")
        if value:
            return str(value)
    return str(lock_entry.get("license") or "UNKNOWN")


def classify(licence: str) -> str:
    if STRONG.search(licence):
        return "STRONG COPYLEFT"
    if WEAK.search(licence):
        return "weak copyleft"
    return ""


def ui_tables(ui: pathlib.Path) -> tuple[list[str], int]:
    manifest = load_json(ui / "package.json")
    lock = load_json(ui / "package-lock.json")["packages"]
    out: list[str] = []
    strong_found = 0

    out.append(f"ui package: `{manifest['name']}` {manifest['version']}, "
               f"declared licence `{manifest.get('license', 'none')}`.")
    out.append("")
    out.append("### ui direct dependencies")
    out.append("")
    out.append("| Package | Range | Resolved | Licence | Kind | Ships in the app | Copyleft |")
    out.append("| --- | --- | --- | --- | --- | --- | --- |")
    for kind, key in (("runtime", "dependencies"), ("dev", "devDependencies")):
        for name, spec in sorted(manifest.get(key, {}).items()):
            entry = lock.get(f"node_modules/{name}", {})
            licence = licence_of(ui / "node_modules" / name, entry)
            ships = "yes" if kind == "runtime" else SHIPS_NOTE.get(name, "no")
            flag = classify(licence)
            strong_found += flag == "STRONG COPYLEFT"
            out.append(f"| `{name}` | `{spec}` | {entry.get('version', '?')} | {licence} "
                       f"| {kind} | {ships} | {flag or 'none'} |")

    prod = {k: v for k, v in lock.items() if k and not v.get("dev")}
    out.append("")
    out.append("### ui transitive runtime dependencies")
    out.append("")
    out.append("Every package in `package-lock.json` not marked `dev`, which is the set "
               "`electron-builder` bundles from `node_modules`.")
    out.append("")
    out.append("| Package | Resolved | Licence | Copyleft |")
    out.append("| --- | --- | --- | --- |")
    for path, entry in sorted(prod.items()):
        name = path.split("node_modules/")[-1]
        licence = licence_of(ui / path, entry)
        flag = classify(licence)
        strong_found += flag == "STRONG COPYLEFT"
        out.append(f"| `{name}` | {entry.get('version', '?')} | {licence} | {flag or 'none'} |")

    out.append("")
    out.append("### ui licence summary, all installed packages")
    out.append("")
    counts: collections.Counter[str] = collections.Counter()
    weak: list[str] = []
    unknown: list[str] = []
    for path, entry in lock.items():
        if not path:
            continue
        name = path.split("node_modules/")[-1]
        licence = licence_of(ui / path, entry)
        counts[licence] += 1
        flag = classify(licence)
        if flag == "STRONG COPYLEFT":
            strong_found += 1
        elif flag:
            weak.append(f"{name} ({'dev' if entry.get('dev') else 'RUNTIME'})")
        if licence == "UNKNOWN":
            unknown.append(f"{name} ({'dev' if entry.get('dev') else 'RUNTIME'})")
    out.append(f"Total packages in the lockfile: {sum(counts.values())}.")
    out.append("")
    out.append("| Licence | Packages |")
    out.append("| --- | --- |")
    for licence, n in counts.most_common():
        out.append(f"| {licence} | {n} |")
    out.append("")
    out.append("Strong copyleft (GPL, AGPL, LGPL, SSPL, EUPL, CC-BY-SA) found: "
               f"{'yes, see the Copyleft column above' if strong_found else 'none'}.")
    out.append("")
    base_weak = sorted({re.sub(r'-(android|darwin|freebsd|linux|win32)[a-z0-9-]*', '', w.split(' ')[0])
                        for w in weak})
    runtime_weak = [w for w in weak if "RUNTIME" in w]
    out.append(f"Weak (file-level) copyleft, MPL family: {len(weak)} packages "
               f"({', '.join(base_weak) or 'none'}), "
               f"{'of which runtime: ' + ', '.join(runtime_weak) if runtime_weak else 'none at runtime'}.")
    out.append("")
    out.append(f"Packages declaring no licence: {', '.join(unknown) or 'none'}.")
    return out, strong_found


def core_tables(core: pathlib.Path) -> list[str]:
    manifest = load_json(core / "package.json")
    lock_path = core / "package-lock.json"
    lock = load_json(lock_path)["packages"] if lock_path.exists() else {}
    out: list[str] = []
    out.append("### core build and vendored dependencies")
    out.append("")
    out.append(f"core package: `{manifest['name']}` {manifest['version']}.")
    out.append("")
    out.append("| Component | Range or source | Resolved | Licence | Kind | Ships in the app | Copyleft |")
    out.append("| --- | --- | --- | --- | --- | --- | --- |")

    for kind, key, ships in (("build (compiled in)", "dependencies", "yes, compiled into the addon"),
                             ("build tool", "devDependencies", "no")):
        for name, spec in sorted(manifest.get(key, {}).items()):
            entry = lock.get(f"node_modules/{name}", {})
            licence = licence_of(core / "node_modules" / name, entry)
            out.append(f"| `{name}` | `{spec}` (npm) | {entry.get('version', '?')} | {licence} "
                       f"| {kind} | {ships} | {classify(licence) or 'none'} |")

    vendor = core / "vendor"
    for lib in sorted(p for p in vendor.iterdir() if p.is_dir()) if vendor.exists() else []:
        licence = "UNKNOWN"
        for src in sorted(lib.glob("*.[ch]")):
            match = re.search(r"SPDX-License-Identifier:\s*([^\s*]+)",
                              src.read_text(encoding="utf-8", errors="replace")[:2000])
            if match:
                licence = match.group(1)
                break
        out.append(f"| `{lib.name}` | `core/vendor/{lib.name}/` (vendored source) | "
                   f"not recorded in the copy | {licence} | build (compiled in) "
                   f"| yes, compiled into the addon | {classify(licence) or 'none'} |")

    cmake = (core / "CMakeLists.txt").read_text(encoding="utf-8")
    if re.search(r"find_package\(\s*GTest", cmake):
        out.append("| `googletest` | `find_package(GTest)` (system package) | "
                   "set by the machine, not by the repo | BSD-3-Clause (upstream licence, "
                   "not read from this checkout) | test | no | none |")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    here = pathlib.Path(__file__).resolve().parent.parent
    parser.add_argument("--ui", default=str(here.parent / "ui"))
    parser.add_argument("--core", default=str(here.parent / "core"))
    args = parser.parse_args()

    ui, core = pathlib.Path(args.ui), pathlib.Path(args.core)
    lines, strong = ui_tables(ui)
    lines.append("")
    lines += core_tables(core)
    print("\n".join(lines))
    return 1 if strong else 0


if __name__ == "__main__":
    sys.exit(main())
