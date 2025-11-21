This roadmap expands the short roadmap and maps the project milestones (A–I) to concrete objectives, deliverables, owners, success criteria, dependencies, and risks. Use this file to plan work, assign issues, and track progress across repos: `dissonance-docs`, `dissonance-ui`, and `dissonance-core`.

How to use
- Each milestone below lists: timeline, primary repo(s), objectives, deliverables, owners (recommended), acceptance criteria, dependencies, and key risks.
- For each milestone open issue(s) referenced by the milestone ID (for example, "A1", "B3") and link them here.
- Keep this file lightweight — link to deep-dive docs in `docs/research/`, `docs/design/`, and `docs/research/comparative-studies/` when needed.

Legend
- AC: Acceptance criteria — how we know the milestone is complete
- Risks: things to watch and mitigation suggestions

Milestone A — User Research & Personas
- Timeline: Start Sep 2025 — End 2025-11-30
- Primary repo: `dissonance-docs`
- Objectives:
  - Collect and centralize raw survey data
  - Produce summarized user needs and personas
  - Create slide deck + presentation artifacts
- Deliverables:
  - Raw survey exports (CSV/Google Forms) in `surveys/raw/` (A1)
  - Survey summary report in `surveys/summaries/` (A2)
  - Personas in `personas/` with short bios and needs mapping (A3)
  - Slide deck PDF and presentation video in `assets/slides/` and `assets/` (A4, A5)
  - User stories and workflow diagram (A6)
- AC: Survey + personas uploaded; at least 3 personas with user needs; slide deck available; summary document with recommended user stories.
- Dependencies: access to raw survey exports; volunteers for interviews
- Risks: incomplete survey metadata — mitigate by annotating raw exports; low response clarity — use follow-up interviews.

Milestone B — Veille & Technical Benchmarking
- Timeline: 2025-11-01 — 2026-01-23
- Primary repo: `dissonance-docs` (research)
- Objectives:
  - Create living veille notes covering relevant literature, tools, and threats
  - Benchmark parsing and FFT approaches (C++ vs WASM vs Node vs Python)
  - Produce POCs: Electron audio loader and WASM FFT test (B5, B6)
- Deliverables:
  - `research/veille/` notes with sources and short abstracts (B1)
  - Export of bookmarks / RSS list and newsletter summary (B2)
  - Benchmark reports (B3, B4) with scripts and raw outputs in `research/benchmarks/`
  - POC #1: Electron audio loader project in `dissonance-ui` repo (B5)
  - POC #2: WASM FFT microbenchmark showing baseline performance (B6)
  - Expert interview notes (B7)
  - Decision justification document synthesizing benchmark outcomes (B8)
- AC: Benchmarks reproducible via scripts; clear recommendation for preferred technology stack or tradeoffs documented.
- Dependencies: test audio files, minimal harnesses, CI for running microbenchmarks
- Risks: environment-dependent results — run benchmarks on at least two platforms and include versions.

Milestone C — Repo Architecture & CI/CD
- Timeline: 2025-11-15 — 2025-12-20
- Primary repo: `dissonance-ui`, `dissonance-core`, `dissonance-docs`
- Objectives:
  - Standardize repository READMEs, contributing guidelines, issue/PR templates
  - Set up basic CI for UI (lint/build/test) and Core (CMake build + unit tests)
  - Document tech environment and dev setup
- Deliverables:
  - `README.md`, `CONTRIBUTING.md`, issue and PR templates in each repo (C1–C4)
  - GitHub Actions workflows: `ci-ui.yml`, `ci-core.yml` (C5)
  - ESLint + Prettier configs and a style guide (C6)
  - Architecture diagram and docs in `docs/design/core` and `docs/design/ui` (C7–C8)
- AC: CI runs on main branch; linters and basic build/tests pass in CI; contributing guide available.
- Dependencies: GitHub workflows access, minimal unit tests
- Risks: native build differences (Linux vs macOS) — use matrix runners and document host requirements.

Milestone D — Electron UI Skeleton
- Timeline: 2025-12-01 — 2026-03-13
- Primary repo: `dissonance-ui`
- Objectives:
  - Implement Electron + React + Vite skeleton and base styles
  - Implement core flows: file drag/drop, WAV metadata display, playback, mock processing
  - Add settings placeholders, theme support, and IPC bridge
- Deliverables:
  - Working Electron skeleton with the following features:
    - File drag & drop (D1)
    - Display WAV metadata (D2)
    - Playback "Before" audio (D3)
    - Mock processing UI + processed file placeholder (D4–D6)
    - Settings panel placeholders + light/dark theme (D7–D8)
    - Tailwind base styles (D10)
    - IPC bridge stub for talking to native/core (D11)
  - Documentation pages describing UI flow and components (D9)
- AC: App builds and runs locally; users can load a WAV, see metadata, and play audio.
- Dependencies: decisions about audio backend (Web Audio vs native Dav1d), sample assets
- Risks: platform packaging differences — define packaging plan early.

Milestone E — C++ Evaluation & Technology Strategy
- Timeline: 2026-03-01 — 2026-06-12
- Primary repo: `dissonance-docs`, `dissonance-core`
- Objectives:
  - Audit and document the existing C++ WAV parser and editing prototype (E1)
  - Benchmark parsing performance across implementations (E2)
  - Evaluate integration complexity and make a migration decision (E3–E4)
  - Produce a Year 2 technology strategy (E5)
- Deliverables:
  - C++ parser audit report and usage examples (E1)
  - Benchmark results and scripts comparing C++/Node/WASM/Python (E2)
  - Integration evaluation matrix and recommendation (E3–E4)
  - Strategy doc for Year 2 (E5)
- AC: Clear recommendation with pros/cons and migration plan if needed.
- Dependencies: C++ prototype codebase, test audio corpus
- Risks: hidden integration costs — run small end-to-end POCs to quantify.

=== YEAR 2 (DSP and perturbations) ===

Milestone F — DSP Kernel (STFT/ISTFT)
- Timeline: 2026-07-01 — 2026-10-09
- Primary repo: `dissonance-core`
- Objectives:
  - Implement STFT and ISTFT reference implementations with configurable window functions and overlap
  - Provide worker-based DSP kernels suitable for use in UI (WASM/TS fallback) and native (C++)
  - Add WAV writer/reader support and reconstruction tests
- Deliverables:
  - STFT/ISTFT library (F3–F4)
  - Window functions collection and tests (F5)
  - Worker-based DSP harness and examples (F6)
  - Reconstruction tests with fidelity/PSNR metrics (F7)
  - WAV writer utility (F8)
  - DSP kernel documentation (F9)
- AC: Round-trip reconstruction error within acceptable threshold (define target, e.g., SNR > 80 dB or perceptual indistinguishability tests pass), documented API.
- Dependencies: audio test corpus, chosen numeric precision, CI with build matrix
- Risks: numerical boundary issues and reconstruction artifacts — add automated regression tests.

Milestone G — Adversarial Perturbation v1
- Timeline: 2026-11-01 — 2027-01-22
- Primary repo: `dissonance-core`
- Objectives:
  - Implement initial perceptual masking and spectral perturbation approaches
  - Build LUFS safety rails and config schema
  - Provide ABX testing helper for human evaluation (G5)
- Deliverables:
  - Masking threshold estimator (G1)
  - Spectral perturbation module (G2)
  - LUFS safety module for limiting overall loudness (G3)
  - Config schema and examples (G4)
  - ABX testing helper scripts and instructions (G5)
  - Documentation for v1 (G6)
- AC: Perturbation demonstrator that reduces transcription accuracy for selected baseline models (document models and test harness), while remaining below masking thresholds or LUFS targets.
- Dependencies: model testing harness (e.g., Whisper), evaluation metrics
- Risks: adversarial attacks may transfer differently across models — ensure evaluations on multiple models and document limits.

Milestone H — Adversarial Perturbation v2
- Timeline: 2027-02-01 — 2027-03-15
- Primary repo: `dissonance-core`
- Objectives:
  - Implement advanced perturbation techniques (temporal jitter, phase distortion, hybrid approaches)
  - Build model testing harness and improve reproducibility
- Deliverables:
  - Temporal jitter engine (H1)
  - Phase distortion engine (H2)
  - Hybrid perturbation engine (H3)
  - Model testing harness for multiple ASR/music models (H4)
  - v2 documentation and evaluations (H5)
- AC: Demonstrated stronger or more transferable perturbations across a broader set of models with controlled perceptual quality.
- Dependencies: access to target models, compute resources for testing
- Risks: increased perceptual artifacts — include human listening tests to validate imperceptibility.

Milestone I — Optimization, Packaging & Final Docs
- Timeline: 2027-03-15 — 2027-04-30
- Primary repos: `dissonance-core`, `dissonance-ui`, `dissonance-docs`
- Objectives:
  - Profile and optimize DSP and perturbation implementations
  - Prepare Electron packaging and auto-update configuration
  - Produce final documentation, reproducibility artifacts, and final project report
- Deliverables:
  - Performance profiling reports and optimization patches (I1–I2)
  - Electron Builder configuration and build scripts (I3–I4)
  - Auto-update setup and packaging documentation (I5–I6)
  - Final wiki and project report (I7–I8)
- AC: Production-ready packaging (installer for at least one OS), performance within target bounds, final report complete.
- Dependencies: packaging keys, platform-specific testing machines
- Risks: packaging edge cases, auto-update complexity — start early and test incremental releases.

Quarterly plan and immediate next steps (Nov 2025 → Mar 2026)
- Nov 2025 (now)
  - Finalize Milestone A deliverables (personas, survey summaries)
  - Begin Milestone B benchmark planning and set up benchmark harnesses
  - Close out repo hygiene tasks for Milestone C (README, CONTRIBUTING already drafted)
- Dec 2025 — Jan 2026
  - Run comparative benchmarks (B3) and produce POC results (B5, B6)
  - Finalize CI basics for UI and Core (C5)
  - Start skeleton of Electron app (D)
- Feb — Mar 2026
  - Continue Electron skeleton (D1–D11)
  - Prepare C++ evaluation tasks for Milestone E (E1–E3)

KPIs and success indicators
- Documentation coverage: key docs present for each milestone (README, plan, templates)
- Reproducible benchmarks: benchmark scripts can be run with documented commands
- CI coverage: builds and unit tests pass on main + PRs
- DSP fidelity: round-trip reconstruction metrics within threshold (set numeric targets during F)
- User validation: at least 3 artist/tester ABX sessions for perceptual checks during G and H

Risks and mitigations (summary)
- Risk: Platform variability affects benchmarks and packaging. Mitigation: run on Linux and macOS, document environment, use Docker for reproducibility where possible.
- Risk: Integration complexity between C++ core and Electron UI. Mitigation: evaluate WASM and Node native bridges early in Milestone B/E and choose minimal viable integration.
- Risk: Adversarial methods produce perceptible artifacts. Mitigation: use LUFS and masking thresholds as hard constraints; run human ABX tests early.

Artifacts and repo mapping
- `dissonance-docs` — research, survey data, personas, benchmarks, comparative studies, final reports
- `dissonance-ui` — Electron UI skeleton, POC loader, packaging configs
- `dissonance-core` — C++ prototype, DSP kernel, perturbation engines, tests

