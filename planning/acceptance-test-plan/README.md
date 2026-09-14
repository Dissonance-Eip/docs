---
title: Acceptance test plan — beta
status: active
owner: Luca Martinet
created: 2026-09-14
updated: 2026-09-14
tags: [planning, testing, acceptance, beta]
---

# Acceptance test plan — beta

## Summary

[`atp_661_Dissonance.xlsx`](atp_661_Dissonance.xlsx) is the acceptance test plan
for the Dissonance beta: 56 scenarios run by testers against the released
installer of UI v0.1.1 with bundled core v0.0.5. F1–F48 are testable this cycle;
F49–F56 describe the in-app protection verification planned for a later build
and are listed for planning only. At the document date, 2026-09-03, the
development status column counts 42 scenarios done and 14 in progress, and the
Feedback column is empty — no test cycle has been recorded yet.

## What the spreadsheet contains

| Sheet | Contents |
| --- | --- |
| `Info & Access` | Versions under test, download links, test audio files, test environment, acceptance criteria, anomaly handling |
| `Test Plan` | One row per scenario: ID, name, category, objective, prerequisites, steps, expected results, development status, feedback |

| Category | Scenarios |
| --- | ---: |
| Critical feature | 27 |
| Secondary function | 14 |
| User interface | 10 |
| Compatibility | 5 |

## Running a test cycle

- Install from the [UI releases page](https://github.com/Dissonance-Eip/ui/releases/latest):
  macOS `.dmg` (Apple Silicon only), Windows `.exe`, or Linux `.AppImage`.
  Nothing else needs building.
- Use headphones — several scenarios are listening tests.
- No account is needed: the app is fully offline.
- For each scenario, set the Feedback cell to **MEETS REQUIREMENTS** or
  **NON-COMPLIANT**, then add a one-line note with your OS and app version.
  Write `N/A — <reason>` when a prerequisite cannot be met, and leave F49–F56 as
  N/A.

Every non-compliant row becomes an issue on the matching repository, titled with
its Feature ID. The plan is re-run in full each cycle, and a fixed scenario must
pass twice before its issue is closed.

## Anomaly severity

| Severity | Definition | Outcome |
| --- | --- | --- |
| Blocking | The scenario cannot be completed: crash, freeze, missing feature, app won't start | Non-compliant; fixed before the next cycle |
| Major | The scenario completes with a wrong result: bad metadata, audible artefact, original file altered, unplayable output | Non-compliant; triaged in the current cycle |
| Minor | Cosmetic or wording issue that does not change the outcome | Meets requirements; noted in Feedback |

## Test audio

The nine test files ship in the appendix ZIP, which is distributed alongside the
plan and is not stored in this repository.

| File | Purpose |
| --- | --- |
| `atp_stereo_44k.wav` | 30 s, 44.1 kHz, 16-bit stereo, all seven tags filled — main file for the UI scenarios |
| `atp_mono_48k.wav` | 30 s, 48 kHz, 16-bit mono, no tags |
| `atp_fulltrack.wav` | 3:06, 44.1 kHz stereo — processing time and A/B listening (F32, F35) |
| `atp_track_c.wav` | 90 s, quiet and sparse, peak −0.6 dBFS — least masking headroom (F35) |
| `atp_track_d.wav` | 90 s, loud dense master, peak 0.0 dBFS (F35) |
| `atp_24bit.wav` | 30 s, 44.1 kHz, 24-bit stereo, plain PCM header (F48) |
| `atp_24bit_ext.wav` | The same audio written as `WAVE_FORMAT_EXTENSIBLE` (F48) |
| `atp_corrupt.wav` | Truncated file with a `.wav` extension — error handling (F10, F30) |
| `atp_sample.mp3` | 30 s MP3 — a format the core does not parse yet (F9) |

F48 exercises the `WAVE_FORMAT_EXTENSIBLE` limitation documented in the
[C++ WAV parser audit](../../design/core/2026-09-04-cpp-wav-parser-audit.md).

## Related

- [Issue #52](https://github.com/Dissonance-Eip/docs/issues/52) — the EIP Pool task this plan delivers, with the Epitech template and example
- [`../milestones.md`](../milestones.md) — project status by milestone
- [`../testing-policy-core.md`](../testing-policy-core.md) — automated testing for the C++ core
- [`../../design/core/2026-09-04-cpp-wav-parser-audit.md`](../../design/core/2026-09-04-cpp-wav-parser-audit.md) — the parser limitation F48 checks
