---
title: Milestones
status: active
owner: Noé Kurata
created: 2025-09-15
updated: 2026-09-04
tags: [planning, milestones]
---

# Milestones

## Summary

Where the project stands, per milestone, across the three repositories. This
file mirrors the GitHub milestones — it is not a second plan. When the two
disagree, GitHub is right and this file is stale.

As of 2026-09-04 the project is working through **Milestone G — Adversarial
Perturbation v1** in `core` and `ui`, with **Milestone E** open in `docs` and
**Milestone I — Packaging & Release** queued in `ui`.

## Status, 2026-09-04

Issue counts are from the GitHub milestone API on 2026-09-04.

### `docs` — [Dissonance-Eip/docs](https://github.com/Dissonance-Eip/docs/milestones)

| Milestone | Open | Closed | State |
| --- | ---: | ---: | --- |
| 0 — Project Planning & Documentation Architecture | 0 | 10 | Closed |
| A — User Research & Personas | 0 | 5 | Closed |
| B — Veille & Technical Benchmarking | 1 | 6 | Closed — [#12](https://github.com/Dissonance-Eip/docs/issues/12) still open |
| E — C++ Evaluation & Technology Strategy | 3 | 0 | **Open** |
| EIP Pool | 3 | 0 | **Open** |

### `core` — [Dissonance-Eip/core](https://github.com/Dissonance-Eip/core/milestones)

| Milestone | Open | Closed | State |
| --- | ---: | ---: | --- |
| 1 — MVP | 0 | 15 | Closed |
| E — C++ Native Add-on Architecture Decision | 0 | 1 | Closed |
| F — C++ DSP Kernel as Node Add-on (STFT/ISTFT, Audio I/O) | 1 | 9 | **Open** — only [#40](https://github.com/Dissonance-Eip/core/issues/40), the kernel documentation, remains |
| G — Adversarial Perturbation v1 (Proof of Concept, C++ Add-on) | 7 | 8 | **Open — active** |
| H — Adversarial Perturbation v2 (Model Coverage + Imperceptibility) | 0 | 0 | Open, not started |

### `ui` — [Dissonance-Eip/ui](https://github.com/Dissonance-Eip/ui/milestones)

| Milestone | Open | Closed | State |
| --- | ---: | ---: | --- |
| 1 — MVP | 0 | 13 | Closed |
| C — Repo Architecture & CI/CD (UI) | 0 | 7 | Closed |
| D — Electron UI Skeleton | 0 | 10 | Closed |
| G — Adversarial Perturbation v1 (Proof of Concept, C++ Add-on) | 2 | 2 | **Open — active** |
| I — Packaging & Release | 5 | 0 | Open, not started |

## What is open right now

### `docs` — Milestone E, C++ Evaluation & Technology Strategy

| Issue | Deliverable | State |
| --- | --- | --- |
| [#23](https://github.com/Dissonance-Eip/docs/issues/23) | Document the existing C++ WAV parser | Written — [parser audit](../design/core/2026-09-04-cpp-wav-parser-audit.md) |
| [#24](https://github.com/Dissonance-Eip/docs/issues/24) | Benchmark C++ vs Node | Written — [benchmark](../research/benchmarks/2026-09-04-cpp-vs-node-wav-parsing/) |
| [#25](https://github.com/Dissonance-Eip/docs/issues/25) | Document integration complexity of C++ into Electron | Written — [integration analysis](../design/core/2026-09-04-cpp-electron-integration-complexity.md) |

Two further deliverables have no issue yet and follow from those three:

- **The migration decision itself.** ADR 002 recording why the project ships a
  C++ native addon rather than the TypeScript/WASM architecture chosen in
  [ADR 001](../design/core/2025-11-21-adr-001-ui-framework-and-dsp-integration.md).
- **The DSP benchmark it should rest on.** The parsing benchmark concluded that
  parsing is not the argument for C++;
  [the STFT benchmark](../research/benchmarks/2026-07-08-stft-cpp-vs-ts-vs-wasm/)
  exists in source form and has never been run to a recorded result.

### `docs` — Milestone B

- [#12](https://github.com/Dissonance-Eip/docs/issues/12) — Contact DSP/audio
  experts & document discussion. Notes go in
  [`../research/interviews/`](../research/interviews/), which is currently empty.

### `docs` — EIP Pool

Three school deliverables, none of which has a document yet:

| Issue | Deliverable |
| --- | --- |
| [#52](https://github.com/Dissonance-Eip/docs/issues/52) | Acceptance Test Plan |
| [#53](https://github.com/Dissonance-Eip/docs/issues/53) | Poster for Dissonance |
| [#54](https://github.com/Dissonance-Eip/docs/issues/54) | Warm Up Presentation |

### `core` — Milestones F and G

F is one issue from closing: [#40](https://github.com/Dissonance-Eip/core/issues/40),
the DSP kernel documentation. G is the active work — the open issues are the
limiter, the LUFS safeguard, the ABX export helper, mask-aware shaping for the
remaining perturbation modes, and the v1 write-up.

### `ui` — Milestones G and I

G: perturbation mode in the Compare view and export filename, plus UI tests for
the mode controls. I (Packaging & Release) has five issues and has not started.

## The original two-year plan

The A–I lettering comes from the original plan agreed at the start of the
project. The GitHub milestones have since diverged from it — names differ,
granularity differs, and some letters mean different things in different repos
(`E` is "C++ Evaluation & Technology Strategy" in `docs` and "C++ Native Add-on
Architecture Decision" in `core`). Treat the tables above as authoritative and
[`roadmap.md`](roadmap.md) as the narrative intent behind them.

| Letter | Original scope | Window |
| --- | --- | --- |
| 0 | Project planning & documentation architecture | 2025-09 → 2025-11 |
| A | User research & personas | 2025-09 → 2025-11 |
| B | Veille & technical benchmarking | 2025-11 → 2026-01 |
| C | Repo architecture & CI/CD | 2025-11 → 2025-12 |
| D | Electron UI skeleton | 2025-12 → 2026-03 |
| E | C++ evaluation & technology strategy | 2026-03 → 2026-06 |
| F | DSP kernel (STFT/ISTFT) | 2026-07 → 2026-10 |
| G | Adversarial perturbation v1 | 2026-11 → 2027-01 |
| H | Adversarial perturbation v2 | 2027-02 → 2027-03 |
| I | Optimisation, packaging & final documentation | 2027-03 → 2027-04 |

Note that G is running ahead of the original window and E behind it.

## Keeping this current

Update at each milestone open or close, not continuously. The counts come from:

```bash
for r in docs core ui; do
  curl -s "https://api.github.com/repos/Dissonance-Eip/$r/milestones?state=all&per_page=100" \
    | python3 -c "import json,sys; [print(f\"{m['title']:<62} open={m['open_issues']:>2} closed={m['closed_issues']:>2}\") for m in json.load(sys.stdin)]"
done
```

## Related

- [`roadmap.md`](roadmap.md) — objectives, deliverables and risks per milestone
- [`../README.md`](../README.md) — repository map
