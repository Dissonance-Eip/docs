---
title: Initial static analysis report
status: draft
owner: Luca Martinet
created: 2026-10-29
updated: 2026-10-29
milestone: L
tags: [planning, testing, quality, static-analysis]
---

# Initial static analysis report

## Summary

ESLint reports 0 problems across the 40 linted files of `ui`. `npm audit` in
`ui` reports 4 vulnerable packages (3 high, 1 moderate) in the full dependency
tree and 0 in production dependencies. Cppcheck on `core` reports 0 findings at
the level CI enforces, and 17 style and portability findings in an extended run.
clang-tidy has not been run. No decision on fixes is recorded yet.

## ui

Method, 2026-10-29, Node v26.4.0, ESLint 10.12.0, macOS, `ui` at commit
`5a0c399` plus uncommitted working-tree changes made the same day (coverage
script, `coverage/**` added to the ESLint ignore list, licence field). One run
each.

| Check | Command | Result |
| --- | --- | --- |
| ESLint | `npm run lint` | Exit 0, no output |
| ESLint, full report | `npx eslint . -f json` | 40 files, 0 errors, 0 warnings, 0 findings for any rule |
| Audit, all dependencies | `npm audit` | 4 vulnerable packages: 3 high, 1 moderate |
| Audit, production only | `npm audit --omit=dev` | 0 vulnerabilities |

Findings by rule: none, so there is nothing to count by rule.

### npm audit detail

| Package | Severity | Direct | Pulled in by | Ships in the app |
| --- | --- | --- | --- | --- |
| `electron` | High | Yes | `ui` devDependency | Yes (runtime). Advisory: mitigation for compromised intermediate certificates, `GHSA-jr5w-w6x2-84p9`. Affects 44.0.0-alpha.1 to 44.9.0 |
| `undici` | High | No | `electron` (through `@electron/get`) and `node-gyp` (through `electron-builder`) | Build time downloads only |
| `brace-expansion` | High | No | Development tooling | No |
| `fast-uri` | Moderate | No | Development tooling | No |

`npm audit` states a fix is available for all four. The Electron advisory
concerns the runtime that users receive, so it is the one to weigh first.

## core

Method: Cppcheck 2.21.0, run by the core maintainers on `core/src`.

| Run | Categories | Findings |
| --- | --- | --- |
| CI level (`warning`, `style`, `performance`, `portability`) | all | 0, the CI gate passes |
| Extended (`--enable=all --inconclusive`) | error | 0 |
| | warning | 0 |
| | performance | 0 |
| | style | 15 |
| | portability | 2 |

The 15 style findings split into 11 unused-function reports, 3 functions that
could be `const`, and 1 parameter-name mismatch. The 11 unused-function reports
are most likely false positives because `tests/` was not part of the analysis.
The 2 portability findings concern pointer casts in binary file input and
output code.

clang-tidy: not run, because it is not installed on the machine used.
TODO(team): install it and add its counts by category.

## What will be fixed and what is accepted

| Item | Proposal | Decision |
| --- | --- | --- |
| ui: Electron advisory | Update Electron to a fixed version | TODO(team) |
| ui: `undici`, `brace-expansion`, `fast-uri` (dev tooling) | Update with `npm audit fix` or accept until the tool updates | TODO(team) |
| core: style findings (15) | Review later, not release blockers | TODO(team) |
| core: portability findings (2) | Review later, not release blockers | TODO(team) |
| core: unused-function reports (11) | Re-run with `tests/` included, expected to clear most | TODO(team) |
| clang-tidy | Run once installed | TODO(team) |

## Related

- [`test-strategy.md`](test-strategy.md)
- [`dependency-inventory.md`](dependency-inventory.md)
- Issue [docs#64](https://github.com/Dissonance-Eip/docs/issues/64)
