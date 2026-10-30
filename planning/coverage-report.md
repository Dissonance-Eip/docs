---
title: Coverage report, 2026-10-29
status: draft
owner: Luca Martinet
created: 2026-10-29
updated: 2026-10-30
milestone: L
tags: [planning, testing, coverage]
---

# Coverage report, 2026-10-29

## Summary

First coverage measurement for both repositories, taken on 2026-10-29. `core`
reaches 78.32% line coverage over the files linked into its test binary, which
meets the 70% target. `ui` reaches 8.92% line coverage against a 50% target,
which is not met. The gap in `ui` is almost entirely untested controllers, views
and main-process code. The CI jobs show coverage in the job summary, with no
threshold and no badge.

Targets are defined in [`test-strategy.md`](test-strategy.md). On 2026-10-30
the target was raised to 85% line coverage for both repositories ([docs#80](https://github.com/Dissonance-Eip/docs/issues/80)). The
measurements below are from 2026-10-29 and are kept as taken. Their Target
column shows the new target, with the one in force on the day in brackets.

## Status on 2026-10-30

| Repository | Command | Lines | Target | Result |
| --- | --- | --- | --- | --- |
| `core` | `npm run coverage` (`src/` lines, gcov) | about 92% | 85% | Met |
| `ui` | `npm run test:coverage` (Vitest V8), after [ui#128](https://github.com/Dissonance-Eip/ui/pull/128) | about 71% | 85% | Not met. Tracked in [ui#129](https://github.com/Dissonance-Eip/ui/issues/129) |

These are approximate figures from `dev` on 2026-10-30, not a full measurement
with a method section like the ones below. SonarQube Cloud shows 66.7% for
`core` and 67.6% for `ui` on `dev`. Those are not the figures the target is
checked against. See
[Why SonarQube shows lower coverage](sonarqube-setup.md#why-sonarqube-shows-lower-coverage).

## core

Method: `npm run coverage` in `core`, one run, macOS, AppleClang with `llvm-cov
gcov`, on 2026-10-29. Line coverage over the 12 source files linked into the
test binary.

| Measure | Value | Target | Result |
| --- | --- | --- | --- |
| Lines | 78.32% (744 of 950) | 85% (70% on the day) | Not met at 85%. Met the 70% target in force on the day |

- The command line interface and addon entry-point files are not linked into
  the test binary, so they are not measured yet. The figure does not describe
  them.
- The weakest area is the WAV file input and output utilities.
- Per-file figures are not published here, to keep the engine's structure out of
  public documentation.

## ui

Method: `npm run test:coverage` in `ui` (Vitest 4.1.12 with the V8 provider),
one run, macOS, Node v26.4.0, 2026-10-29. `ui` at commit `5a0c399` plus the
uncommitted working-tree changes of that day, including the addon integration
test. 6 test files, 55 tests passed and 3 expected failures.

| Measure | Value | Target | Result |
| --- | --- | --- | --- |
| Lines | 8.92% (89 of 997) | 85% (50% on the day) | Not met |
| Statements | 8.82% (98 of 1110) | none | n/a |
| Branches | 12.25% (63 of 514) | none | n/a |
| Functions | 9.12% (24 of 263) | none | n/a |

### Per file

Columns are statement, branch, function and line percentages. The last column
is covered lines over total lines.

| File | Stmts % | Branch % | Funcs % | Lines % | Lines covered |
| --- | --- | --- | --- | --- | --- |
| `main.js` | 0 | 100 | 100 | 0 | 0/2 |
| `preload.js` | 0 | 100 | 0 | 0 | 0/24 |
| `ipcHandlers/FileDialogHandlers.js` | 0 | 0 | 0 | 0 | 0/7 |
| `ipcHandlers/UiLogForwarder.js` | 0 | 0 | 0 | 0 | 0/9 |
| `ipcHandlers/fileHandlers.js` | 0 | 100 | 0 | 0 | 0/9 |
| `ipcHandlers/themeHandlers.js` | 0 | 0 | 0 | 0 | 0/17 |
| `ipcHandlers/core/CoreAddonLoader.js` | 64.15 | 50 | 80 | 64.7 | 33/51 |
| `ipcHandlers/core/CoreIpcHandlers.js` | 0 | 0 | 0 | 0 | 0/79 |
| `ipcHandlers/core/TempFileManager.js` | 0 | 0 | 0 | 0 | 0/36 |
| `ipcHandlers/core/coreSetup.js` | 0 | 100 | 0 | 0 | 0/9 |
| `main/MainApplication.js` | 0 | 0 | 0 | 0 | 0/70 |
| `main/MainWindowManager.js` | 0 | 0 | 0 | 0 | 0/18 |
| `renderer/index.js` | 0 | 100 | 0 | 0 | 0/2 |
| `renderer/app/bootstrap.js` | 0 | 0 | 0 | 0 | 0/19 |
| `renderer/base/BaseApi.js` | 0 | 0 | 0 | 0 | 0/8 |
| `renderer/base/BaseComponent.js` | 0 | 0 | 0 | 0 | 0/12 |
| `renderer/base/BaseController.js` | 0 | 100 | 0 | 0 | 0/6 |
| `renderer/base/Disposable.js` | 0 | 0 | 0 | 0 | 0/17 |
| `renderer/base/Logger.js` | 100 | 0 | 0 | 100 | 0/0 |
| `renderer/components/DropZone.js` | 0 | 0 | 0 | 0 | 0/48 |
| `renderer/components/WaveformPreview.js` | 0 | 0 | 0 | 0 | 0/128 |
| `renderer/controllers/AppController.js` | 0 | 0 | 0 | 0 | 0/206 |
| `renderer/infrastructure/DissonanceApi.js` | 0 | 100 | 0 | 0 | 0/10 |
| `renderer/infrastructure/SystemThemeWatcher.js` | 0 | 0 | 0 | 0 | 0/20 |
| `renderer/infrastructure/TerminalLogger.js` | 0 | 0 | 0 | 0 | 0/12 |
| `renderer/infrastructure/ViewRouter.js` | 0 | 0 | 0 | 0 | 0/7 |
| `renderer/services/TagWriteQueue.js` | 100 | 100 | 90 | 100 | 29/29 |
| `renderer/services/WavMetadataService.js` | 100 | 100 | 100 | 100 | 8/8 |
| `renderer/state/AppState.js` | 100 | 100 | 100 | 100 | 9/9 |
| `renderer/utils/pathUtils.js` | 100 | 100 | 100 | 100 | 2/2 |
| `renderer/utils/wavInfoFormatters.js` | 100 | 100 | 100 | 100 | 8/8 |
| `renderer/views/AnalyzeView.js` | 0 | 0 | 0 | 0 | 0/75 |
| `renderer/views/CompareView.js` | 0 | 0 | 0 | 0 | 0/34 |
| `renderer/views/UploadView.js` | 0 | 100 | 0 | 0 | 0/6 |

### The gap to the target

The files with coverage are the pure logic modules (state, formatting, path
handling, the metadata service and the tag write queue), all at 100% lines, and
part of the addon loader at 64.7%. The files with none are the controllers,
views, components, IPC handlers and the main process. Reaching 85% lines means
covering a large share of those files, and the Electron-dependent ones need
either test doubles or end-to-end tests.

Existing `ui` issues that would raise coverage:

- [ui#74](https://github.com/Dissonance-Eip/ui/issues/74): UI tests for
  perturbation mode controls
- [ui#97](https://github.com/Dissonance-Eip/ui/issues/97): end-to-end tests that
  drive the app (Playwright)
- [ui#89](https://github.com/Dissonance-Eip/ui/issues/89): handle an
  unavailable engine and validate external inputs

All three are open on 2026-10-29. End-to-end tests driven by Playwright may not
be counted by the Vitest V8 report. TODO(team): confirm how that coverage will
be measured. Reaching and enforcing 85% is tracked in [ui#129](https://github.com/Dissonance-Eip/ui/issues/129).

## Coverage in CI

- `core`: a `coverage` job in `core/.github/workflows/ci.yml` writes the total
  line coverage to the job summary. It is not enforced. Its GCC path has not run
  yet, and the first CI run will confirm it.
- `ui`: a "Report test coverage" step in
  `ui/.github/workflows/ui-quality-checks.yml` writes the total line coverage to
  the job summary. It is not enforced. This step is an uncommitted change in the
  `ui` working tree on 2026-10-29.
- Neither repository shows a badge.

On 2026-10-30 the team decided CI fails below 85%. In `core`,
`scripts/coverage.js` will exit non-zero below 85% ([core#151](https://github.com/Dissonance-Eip/core/issues/151)). In `ui`,
`vitest.config.mjs` will set `coverage.thresholds.lines: 85` once `ui` reaches
85% ([ui#129](https://github.com/Dissonance-Eip/ui/issues/129)). Both issues are open on 2026-10-30.

## Related

- [`test-strategy.md`](test-strategy.md)
- [`static-analysis-report.md`](static-analysis-report.md)
- [`sonarqube-setup.md`](sonarqube-setup.md)
- Issue [docs#61](https://github.com/Dissonance-Eip/docs/issues/61)
- Issue [docs#80](https://github.com/Dissonance-Eip/docs/issues/80)
