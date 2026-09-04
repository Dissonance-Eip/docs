---
title: Benchmark — STFT in C++, TypeScript and WebAssembly
status: draft
owner: Noé Kurata
created: 2026-07-08
updated: 2026-09-04
milestone: E2
tags: [benchmark, core, dsp, stft, wasm]
---

# Benchmark — STFT in C++, TypeScript and WebAssembly

## Summary

Three implementations of the same STFT — C++, a TypeScript worker, and
AssemblyScript compiled to WebAssembly — built to compare DSP performance across
the three candidate stacks. Each harness prints a checksum alongside its timing
so the implementations can be proven equivalent before they are compared.

**This benchmark has never been run to a recorded result.** The sources were
committed on 2026-07-08 as an archive; the harnesses print to stdout and no
output was saved. The figures quoted in
[`../2025-11-21-electron-comparative-study.md`](../2025-11-21-electron-comparative-study.md)
§ 7 — "~12% slower" for WASM and "~1.8× slower" for the TypeScript worker —
appear to come from an unrecorded run of this code, but nothing links them and
no method was written down.

Completing it is a Milestone E deliverable, not cleanup:
[the WAV parsing benchmark](../2026-09-04-cpp-vs-node-wav-parsing/) concluded
that parsing is *not* where the C++ core earns its cost, and that the DSP stage
is where the E4 migration decision actually rests. This is that measurement.

## Question

Does the DSP pipeline need native C++, or is a TypeScript or WebAssembly
implementation fast enough for an offline, file-based workload?

## What is here

| Path | What it is |
| --- | --- |
| [`scripts/stft.cpp`](scripts/stft.cpp) | C++ reference implementation |
| [`scripts/stft-worker.ts`](scripts/stft-worker.ts) | TypeScript implementation, run in a worker thread |
| [`scripts/assembly/index.ts`](scripts/assembly/index.ts) | AssemblyScript source, compiled to `build/stft.wasm` |
| [`scripts/run-ts.mjs`](scripts/run-ts.mjs) | Harness for the TypeScript worker |
| [`scripts/run-wasm.mjs`](scripts/run-wasm.mjs) | Harness for the WebAssembly build |
| [`scripts/package.json`](scripts/package.json) | `assemblyscript` dependency |
| `results/` | Empty — see below |

Parameters, from the harnesses: FFT size 2048, hop 512, 2 channels, 5 iterations
per run.

The original archive also carried 174 `node_modules` entries, a compiled
`stft-cpp` binary, `.DS_Store` files and `__MACOSX/` metadata, which is what made
it 23 MB. Those are not source and have been dropped; `npm install` in `scripts/`
restores the dependency.

## What is missing

Four things stand between this and a citable result.

1. **No C++ harness.** `stft.cpp` has no `main` that prints the
   `impl= frames= ms= checksum=` lines the other two produce. Without it there is
   no C++ column.
2. **The TypeScript harness may not run as committed.**
   `run-ts.mjs` does `new Worker(join(dir, 'stft-worker.ts'))`. Node cannot load
   a `.ts` file into a worker without a loader — either compile it first, or run
   under `node --experimental-strip-types`. Untested either way.
3. **No equivalence check has been performed.** The checksum machinery is there;
   nobody has confirmed the three implementations agree. Until they do, any
   timing comparison is between three different algorithms.
4. **No recorded environment.** Machine, compiler, flags, Node version, date.

## To complete it

Follow the shape of
[`../2026-09-04-cpp-vs-node-wav-parsing/`](../2026-09-04-cpp-vs-node-wav-parsing/),
which is the same comparison done end to end for the WAV parser.

1. Write `scripts/run-cpp.cpp`, printing the same line format as the other two.
2. Make the TypeScript harness run — compile `stft-worker.ts` or use the
   strip-types flag — and document which.
3. Run all three on the same input and confirm the checksums match. Stop and fix
   the implementations if they do not.
4. Raise the iteration count above 5, take three independent replicates, and
   commit the raw output under `results/`.
5. Write the analysis into this file using
   [`../../../templates/benchmark-report.md`](../../../templates/benchmark-report.md),
   record the environment, and replace § 7 of the 2025-11-21 study with a link
   to it.

## Related

- [`../2026-09-04-cpp-vs-node-wav-parsing/`](../2026-09-04-cpp-vs-node-wav-parsing/) — the same comparison, completed, for WAV parsing
- [`../2025-11-21-electron-comparative-study.md`](../2025-11-21-electron-comparative-study.md) — quotes figures that appear to come from this code
- [`../../../design/core/2026-09-04-cpp-electron-integration-complexity.md`](../../../design/core/2026-09-04-cpp-electron-integration-complexity.md) — what the native path costs to ship
- [`../../../planning/milestones.md`](../../../planning/milestones.md) — Milestone E
