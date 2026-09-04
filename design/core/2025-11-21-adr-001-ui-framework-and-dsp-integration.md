---
title: ADR 001 — UI framework and DSP integration
status: superseded
owner: Noé Kurata
created: 2025-11-21
updated: 2026-09-04
milestone: B
tags: [adr, architecture, ui, core]
---

# ADR 001 — UI framework and DSP integration

> **Superseded** by [ADR 002 — C++ native addon for DSP](2026-09-04-adr-002-cpp-native-addon-for-dsp.md).
> The decision recorded here was taken on 2025-11-21 and is preserved verbatim as
> the historical record. What the project actually built diverged from it; ADR 002
> records what was built and why.

## Context

Extracted on 2026-09-04 from § 8 of
[`../../research/benchmarks/2025-11-21-electron-comparative-study.md`](../../research/benchmarks/2025-11-21-electron-comparative-study.md),
where it had been written as the closing section of a comparative study rather
than as a standalone decision record.

The study compared a JUCE/C++ desktop architecture against Electron with
TypeScript, across UI customisation needs, the Electron process model, design
system architecture, and DSP performance.

## Decision

> Use Electron + TypeScript as the UI framework and integrate DSP code via
> WebAssembly or native Node modules compiled from C++.

## Rationale

> Electron allows rapid development of a deeply customizable user interface,
> essential for Dissonance's UX goals. While C++ provides faster DSP, this
> performance difference does not impact Dissonance's offline processing model.
> The web ecosystem, Electron packaging, and React-based design system together
> provide a more sustainable long-term architecture.

## Consequences

> - Slightly lower raw DSP performance (offset by WASM speed)
> - Major gains in UI flexibility, maintainability, and developer productivity
> - Stable cross-platform distribution for Windows/macOS/Linux

## Side note on WebAssembly

Recorded with the original decision:

> Although WebAssembly (WASM) offers demonstrably higher computational
> performance for numerical and signal-processing workloads, its integration
> imposes a level of architectural and operational complexity that is
> disproportionate to the current needs and development capacity of the project.
> Implementing WASM typically requires parallel maintenance of a secondary
> language environment (e.g., C++ or Rust), dedicated compilation pipelines,
> memory-management considerations, and additional bindings to interface with
> JavaScript and Electron. These requirements significantly increase the
> cognitive and technical overhead for our current small team, especially in an
> early-stage research context where rapid iteration, clarity of implementation,
> and maintainability are prioritised. Furthermore, contemporary JavaScript and
> TypeScript runtimes, provide sufficient performance for the scale and latency
> constraints of the project's initial DSP and adversarial processing tasks.
> Therefore, while WASM remains a potential avenue for future optimisation, the
> current phase of the project is better served by a unified, TypeScript-only
> architecture that maximises development efficiency, cross-platform simplicity,
> and accessibility for future contributors.

## Why this was superseded

The Electron decision held. The rest did not:

| This ADR chose | What was built |
| --- | --- |
| TypeScript | Vanilla JavaScript — no `tsconfig.json` in `ui` |
| A React-based design system | No React; hand-rolled MVC in `ui/renderer/` with Tailwind |
| DSP via WebAssembly, or a "TypeScript-only architecture" | DSP in C++, shipped as a Node native addon over N-API |

The divergence was never recorded at the time.
[ADR 002](2026-09-04-adr-002-cpp-native-addon-for-dsp.md) closes that gap.

## Related

- [`../../research/benchmarks/2025-11-21-electron-comparative-study.md`](../../research/benchmarks/2025-11-21-electron-comparative-study.md) — the study this came from
- [`2026-09-04-adr-002-cpp-native-addon-for-dsp.md`](2026-09-04-adr-002-cpp-native-addon-for-dsp.md) — supersedes this
