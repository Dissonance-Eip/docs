---
title: Dependency and licence inventory
status: draft
owner: Luca Martinet
created: 2026-10-29
updated: 2026-10-29
milestone: K
tags: [planning, licensing, dependencies]
---

# Dependency and licence inventory

## Summary

No GPL-family package (GPL, AGPL, LGPL) was found in `ui` or `core`. The `ui`
runtime ships three npm packages, all MIT. The C++ library compiled into the
engine (KISS FFT) is BSD-3-Clause, which is compatible with Apache 2.0 and with a
proprietary engine, provided its notice is reproduced with the binary. The only
copyleft found is MPL-2.0 (file-level) in a development-only tool that is not
shipped. Regenerate the tables with `python3 scripts/dependency-inventory.py`.

## Method

- Date: 2026-10-29. Machine: the maintainer's macOS workstation.
- `ui`: `ui/package.json` and `ui/package-lock.json` at commit `5a0c399` plus
  the uncommitted working-tree changes present on 2026-10-29 (adds
  `@vitest/coverage-v8`, switches the declared licence to `Apache-2.0`).
  Licences read from `ui/node_modules/<package>/package.json`, falling back to
  the lockfile.
- Runtime transitive set: `npm ls --omit=dev --all` in `ui`, cross-checked with
  the packages not marked `dev` in the lockfile. Both give the same three
  packages.
- `core`: `core/package.json`, `core/package-lock.json`, `core/CMakeLists.txt`
  and the SPDX header of the vendored sources. `core/node_modules` was not
  installed, so licences come from the lockfile.
- Copyleft detection is a pattern match on the licence string (GPL, AGPL, LGPL,
  SSPL, EUPL, CC-BY-SA are strong; MPL, EPL, CDDL are weak). It trusts what each
  package declares.

## Regenerate

From `docs/`, with `ui` and `core` checked out next to it and `npm ci` run in `ui`:

```bash
python3 scripts/dependency-inventory.py > /tmp/inventory.md
```

The script exits 1 if a strong-copyleft licence is found in any npm package, so
it can serve as a gate. Use `--ui` and `--core` to point to other checkouts.

## Findings

- **GPL, AGPL, LGPL:** none in `ui` (565 packages in the lockfile) and none in
  `core` build tooling.
- **BSD-3 C++ dependency:** KISS FFT (`core/vendor/kissfft/`, SPDX
  `BSD-3-Clause`) is compatible with Apache 2.0 for the open part and with a
  proprietary engine. Condition: the binary distribution must reproduce the
  copyright notice and licence text. TODO(team): confirm where the notice ships
  with the app.
- **Version of the vendored library is not recorded** in the copy.
  `core/CMakeLists.txt` also fetches the library from its upstream `master`
  branch for CLI and test builds, which is not pinned. TODO(team): record the
  version of the vendored copy and pin the fetch.
- **MPL-2.0:** 24 packages, all `lightningcss` and its platform builds, pulled
  in by Tailwind. Dev only. Not shipped.
- **No declared licence:** `callsite` (dev only, via `depcheck`). Not shipped.
  TODO(team): check its upstream licence if `depcheck` stays.
- **Electron** is a `devDependency` in npm terms but its runtime ships in every
  installer. It is MIT, and it bundles Chromium and Node.js with their own
  licence files. TODO(team): confirm the installers include those notices (not
  verified here).
- **Development tools outside npm** (not dependencies, not shipped):
  `cppcheck` is GPL-3.0 upstream and `clang-format` is Apache 2.0 with LLVM
  exceptions. Both are only run as checks. This is general knowledge and was not
  verified in this checkout.
- Runtime transitive dependencies of `ui` were checked with `npm ls --omit=dev
  --all`: three packages, all MIT, no GPL, AGPL or LGPL.

## Generated tables

Output of `python3 scripts/dependency-inventory.py` on 2026-10-29.

ui package: `Dissonance` 0.1.1, declared licence `Apache-2.0`.

### ui direct dependencies

| Package | Range | Resolved | Licence | Kind | Ships in the app | Copyleft |
| --- | --- | --- | --- | --- | --- | --- |
| `@arraypress/waveform-player` | `^1.5.2` | 1.5.2 | MIT | runtime | yes | none |
| `bindings` | `^1.5.0` | 1.5.0 | MIT | runtime | yes | none |
| `@eslint/js` | `^10.0.1` | 10.0.1 | MIT | dev | no | none |
| `@tailwindcss/cli` | `^4.3.3` | 4.3.3 | MIT | dev | no (its generated CSS file ships, the package does not) | none |
| `@vitest/coverage-v8` | `^4.1.12` | 4.1.12 | MIT | dev | no | none |
| `check-peer-dependencies` | `^5.0.0` | 5.0.0 | MIT | dev | no | none |
| `depcheck` | `^1.4.7` | 1.4.7 | MIT | dev | no | none |
| `electron` | `^44.7.0` | 44.7.0 | MIT | dev | yes (the Electron runtime is the app shell) | none |
| `electron-builder` | `^26.15.3` | 26.15.3 | MIT | dev | no | none |
| `eslint` | `^10.12.0` | 10.12.0 | MIT | dev | no | none |
| `globals` | `^17.13.0` | 17.13.0 | MIT | dev | no | none |
| `npm-check-updates` | `^23.1.0` | 23.1.0 | Apache-2.0 | dev | no | none |
| `prettier` | `^3.9.9` | 3.9.9 | MIT | dev | no | none |
| `tailwindcss` | `^4.3.3` | 4.3.3 | MIT | dev | no (its generated CSS file ships, the package does not) | none |
| `vitest` | `^4.1.7` | 4.1.12 | MIT | dev | no | none |

### ui transitive runtime dependencies

Every package in `package-lock.json` not marked `dev`, which is the set `electron-builder` bundles from `node_modules`.

| Package | Resolved | Licence | Copyleft |
| --- | --- | --- | --- |
| `@arraypress/waveform-player` | 1.5.2 | MIT | none |
| `bindings` | 1.5.0 | MIT | none |
| `file-uri-to-path` | 1.0.0 | MIT | none |

### ui licence summary, all installed packages

Total packages in the lockfile: 565.

| Licence | Packages |
| --- | --- |
| MIT | 424 |
| ISC | 49 |
| MPL-2.0 | 24 |
| Apache-2.0 | 22 |
| BSD-3-Clause | 15 |
| BSD-2-Clause | 14 |
| BlueOak-1.0.0 | 8 |
| Python-2.0 | 3 |
| UNKNOWN | 1 |
| WTFPL OR ISC | 1 |
| WTFPL | 1 |
| 0BSD | 1 |
| (MIT OR CC0-1.0) | 1 |
| (WTFPL OR MIT) | 1 |

Strong copyleft (GPL, AGPL, LGPL, SSPL, EUPL, CC-BY-SA) found: none.

Weak (file-level) copyleft, MPL family: 24 packages (lightningcss), none at runtime.

Packages declaring no licence: callsite (dev).

### core build and vendored dependencies

core package: `dissonance-core` 0.0.2.

| Component | Range or source | Resolved | Licence | Kind | Ships in the app | Copyleft |
| --- | --- | --- | --- | --- | --- | --- |
| `node-addon-api` | `^7.0.0` (npm) | 7.1.1 | MIT | build (compiled in) | yes, compiled into the addon | none |
| `node-gyp` | `^12.1.0` (npm) | 12.4.0 | MIT | build tool | no | none |
| `kissfft` | `core/vendor/kissfft/` (vendored source) | not recorded in the copy | BSD-3-Clause | build (compiled in) | yes, compiled into the addon | none |
| `googletest` | `find_package(GTest)` (system package) | set by the machine, not by the repo | BSD-3-Clause (upstream licence, not read from this checkout) | test | no | none |

## Related

- [ADR 003: open scope](../design/core/2026-10-29-adr-003-open-scope.md)
- [ADR 005: Apache 2.0 licence](../design/core/2026-10-29-adr-005-apache-2-licence.md)
- [Static analysis report](static-analysis-report.md) (`npm audit` results)
- [`scripts/dependency-inventory.py`](../scripts/dependency-inventory.py)
- Issue [docs#57](https://github.com/Dissonance-Eip/docs/issues/57)
