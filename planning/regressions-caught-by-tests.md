---
title: Regressions caught by tests
status: draft
owner: Luca Martinet
created: 2026-10-29
updated: 2026-10-29
milestone: L
tags: [planning, testing, quality]
---

# Regressions caught by tests

## Summary

No case could be documented as a regression caught by an automated test before
it shipped. The history that is still readable shows one regression fixed with
tests added afterwards, and several CI failures that were format checks or test
maintenance, not product regressions. This document lists what was found and
what evidence is missing, so the team can complete it. Nothing here is
inferred beyond what the history shows.

## Method

- `core`: local git history on 2026-10-29. CI run logs for `core` could not be
  read, because the GitHub API answered "not found" for that repository with
  the credentials used.
- `ui`: local git history, merged pull requests (`gh pr list`) and failed CI
  runs (`gh run list --status failure`, 2026-10-29). Run logs older than the
  retention window are gone (HTTP 410 for runs from May and June 2026).

A case qualifies when a test (not a lint or format check) failed on a change,
the failure was fixed before release, and the behaviour at stake is described.

## Cases found

| # | Repository and reference | What it is | Qualifies? |
| --- | --- | --- | --- |
| 1 | `core` issue #107, PR #108 (merge `83dadbd`, commit `77ca589`, 2026-10-08) | Default processing made every file quieter and removed content in the upper part of the spectrum. Found by measuring output, not by a test. The fix added end-to-end level tests on generated audio. | No as a catch. Yes as a regression now guarded by tests. |
| 2 | `core` commit `acdf03d` (2026-10-25) | A test that asserted the old default output level failed after an intended change to the default output level. It was updated to the new default. | No. The test caught an intended change. |
| 3 | `core` commit `eff5808` (2026-08-31) | Round-trip tests failed on Windows because temporary files were deleted while still open. The commit message quotes the failure. The defect was in the test teardown, not in the product. | No. Test defect, not a product regression. |
| 4 | `ui` PR #96 (merged 2026-10-05) | CI failed on 2026-10-01 and 2026-10-05 at the format check step. A newline was added in the next commit. | No. Format gate, not a test. |
| 5 | `ui` branches `feat/tests` and `feat/beta-finish` (2026-05-22) | First CI runs failed. The only readable failure shows the format check step. | No. Format gate, not a test. |

### Case 1 in detail

- **PR:** `core` PR #108, resolving issue #107.
- **Failing test:** none at the time. End-to-end level tests on generated audio
  were added with the fix. They require the output level and the high-frequency
  content to be preserved.
- **What shipped:** app releases before the fix produced output that was lower
  in level and had less high-frequency content than the input, with no setting
  to avoid it. TODO(team): add the measured level change and the release
  versions affected, from the issue.
- **Fix:** the default pipeline no longer changes the level or removes high
  frequencies, and the tests above now fail if it does again.

## What is missing

To reach three qualifying cases, the team needs to supply, for each:

1. A pull request where a test (not lint or format) failed in CI and the author
   fixed the code, not the test.
2. The name of the failing test, and a link or a saved log. Logs from `core`
   CI are not readable from this repository's tooling, and old `ui` logs have
   expired.
3. A one-line description of what users would have seen had it merged.

Places to look: failed `core` CI runs on pull requests (the `cmake-tests` job),
and review comments that mention a failing test. TODO(team): add the cases or
confirm that fewer exist.

## Related

- [`test-strategy.md`](test-strategy.md)
- [`static-analysis-report.md`](static-analysis-report.md)
- Issue [docs#65](https://github.com/Dissonance-Eip/docs/issues/65)
