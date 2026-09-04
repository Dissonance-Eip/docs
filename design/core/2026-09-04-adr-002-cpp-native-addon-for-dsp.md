---
title: ADR 002 — C++ native addon for DSP
status: draft
owner: Luca Martinet
created: 2026-09-04
updated: 2026-09-04
milestone: E
supersedes: design/core/2025-11-21-adr-001-ui-framework-and-dsp-integration.md
tags: [adr, architecture, core, dsp]
---

# ADR 002 — C++ native addon for DSP

> **Draft.** The recommendation below rests on parsing and integration evidence
> only. The DSP measurement it should also rest on —
> [the STFT benchmark](../../research/benchmarks/2026-07-08-stft-cpp-vs-ts-vs-wasm/) —
> has not been run to a recorded result. Do not mark this `final` until it has.

## Summary

Dissonance ships its DSP as a C++ engine loaded into Electron as a Node native
addon over N-API, not as the TypeScript or WebAssembly implementation
[ADR 001](2025-11-21-adr-001-ui-framework-and-dsp-integration.md) chose. This
record exists because that divergence happened without one.

The recommendation is to **keep the native addon**, on the grounds that its
integration cost is already paid and its ABI risk is nil — not on the grounds of
raw speed, which the measured evidence does not support as a deciding factor.

## Context

ADR 001, in November 2025, chose Electron with TypeScript and DSP via
WebAssembly, closing with an argument for "a unified, TypeScript-only
architecture". What was built over the following ten months is a vanilla
JavaScript Electron app calling a C++ N-API addon. No TypeScript, no WebAssembly,
no React.

Milestone E exists to settle whether that is the right architecture for year two,
with E4 as the migration decision. Three pieces of evidence were produced for it
in September 2026:

- [E1 — the C++ WAV parser audit](2026-09-04-cpp-wav-parser-audit.md)
- [E2 — C++ vs Node WAV parsing benchmark](../../research/benchmarks/2026-09-04-cpp-vs-node-wav-parsing/)
- [E3 — integration complexity of C++ into Electron](2026-09-04-cpp-electron-integration-complexity.md)

## Options considered

### Option A — Keep the C++ native addon

- **How it works:** C++ sources built by `node-gyp` against `node-addon-api`;
  three platform binaries produced by CI, published as release assets, and synced
  into the `ui` repository; loaded at main-process startup.
- **For:** it exists and works. N-API is ABI-stable across Node and Electron
  versions, so an Electron upgrade needs no rebuild — the single largest
  integration cost the project has already avoided. Fastest measured option for
  parsing.
- **Against:** three native toolchains, a pinned Windows CI runner, a build-time
  network dependency on `nodejs.org`, ~918 KB of binaries committed to `ui`, and
  three plausible platforms with no binary at all (Intel Mac, ARM Windows,
  ARM Linux).
- **Evidence:** [E3](2026-09-04-cpp-electron-integration-complexity.md)

### Option B — Move the audio path to TypeScript

- **How it works:** reimplement parsing and DSP in TypeScript, delete the addon,
  the CI matrix and the sync pipeline.
- **For:** one toolchain, one CI runner, no binaries, every platform covered, no
  ABI concerns, debugging in one language.
- **Against:** the parser and DSP would be rewritten; measured 2.2–3.5× slower on
  WAV parsing.
- **Evidence:** [E2](../../research/benchmarks/2026-09-04-cpp-vs-node-wav-parsing/).
  DSP performance **not measured**.

### Option C — Compile the existing C++ to WebAssembly

- **How it works:** keep the C++ sources, replace `node-gyp` with Emscripten,
  ship one portable `.wasm`.
- **For:** keeps the DSP work; removes the three-platform matrix and the
  `node-gyp` network dependency; covers every platform.
- **Against:** a new build toolchain; no practical source-level debugging;
  performance unmeasured.
- **Evidence:** none yet — this is what
  [the STFT benchmark](../../research/benchmarks/2026-07-08-stft-cpp-vs-ts-vs-wasm/)
  is for.

## Decision

**Keep the C++ native addon** for the remainder of year two, and revisit for
year three only if the STFT benchmark shows the DSP gap is small.

The reasoning is integration economics, not speed. E2 found C++ ahead by
2.5–2.8× on realistically-sized files — a gap worth a few hundred milliseconds
once per file, which does not by itself pay for a native addon. E3 found that the
addon's cost is largely *already paid*: the bindings, the CI matrix, the release
pipeline and the loader all exist and work, and N-API removes the ABI risk that
would otherwise make every Electron upgrade expensive. Migrating away would be
paying a second construction cost to recover the first.

Explicitly **not** decided here: whether year three's DSP work stays native. That
depends on the STFT numbers.

## Consequences

**Accepted costs**

- Three native toolchains and a CI matrix to maintain, including a `windows-2022`
  pin that survives only until GitHub retires the image.
- Contributors need a C++ toolchain to change the DSP, though not to run the app.
- Binaries continue to accumulate in the `ui` repository's history.
- Intel Mac, ARM Windows and ARM Linux users have no working build until the
  matrix is extended.

**Follow-up work this creates**

- Run [the STFT benchmark](../../research/benchmarks/2026-07-08-stft-cpp-vs-ts-vs-wasm/)
  to a recorded result, and update this ADR before marking it final.
- The eight integration issues in
  [E3](2026-09-04-cpp-electron-integration-complexity.md#follow-up-issues) —
  above all the missing UI↔core version check and the no-op CI test gate.
- The seven parser issues in [E1](2026-09-04-cpp-wav-parser-audit.md#recommended-follow-up).
- Add `macos-13` to the release matrix so Intel Macs have a binary.

**What would make us revisit this**

- The STFT benchmark showing WebAssembly within roughly 20% of native — at which
  point Option C buys platform coverage cheaply.
- N-API ceasing to be ABI-stable across Electron majors, which would restore the
  rebuild cost this decision assumes away.
- The team growing past the point where one person maintains three toolchains.

## Related

- [`2025-11-21-adr-001-ui-framework-and-dsp-integration.md`](2025-11-21-adr-001-ui-framework-and-dsp-integration.md) — the decision this supersedes
- [`2026-09-04-cpp-wav-parser-audit.md`](2026-09-04-cpp-wav-parser-audit.md) — E1
- [`../../research/benchmarks/2026-09-04-cpp-vs-node-wav-parsing/`](../../research/benchmarks/2026-09-04-cpp-vs-node-wav-parsing/) — E2
- [`2026-09-04-cpp-electron-integration-complexity.md`](2026-09-04-cpp-electron-integration-complexity.md) — E3
- [`../../research/benchmarks/2026-07-08-stft-cpp-vs-ts-vs-wasm/`](../../research/benchmarks/2026-07-08-stft-cpp-vs-ts-vs-wasm/) — the missing DSP measurement
