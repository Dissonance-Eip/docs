---
title: Onboarding
status: active
owner: Noé Kurata
created: 2025-12-15
updated: 2026-09-04
tags: [planning, onboarding]
---

# Onboarding

## Summary

How to get a working Dissonance development environment and make your first
contribution. Every command here has been run — if one fails, that is a bug in
this document, so fix it in the same pull request as your first change.

Expect an hour to a working app, most of it toolchain installation.

## The three repositories

| Repository | What it is | Default branch |
| --- | --- | --- |
| [`core`](https://github.com/Dissonance-Eip/core) | C++ DSP engine — a Node native addon plus a CLI | `dev` |
| [`ui`](https://github.com/Dissonance-Eip/ui) | Electron desktop application | `dev` |
| [`docs`](https://github.com/Dissonance-Eip/docs) | This repository — research, planning, decisions | `main` |

`dev` is where work lands; `main` is the released state. Ask the project lead
for organisation access before you start.

```bash
mkdir Dissonance && cd Dissonance
git clone git@github.com:Dissonance-Eip/core.git
git clone git@github.com:Dissonance-Eip/ui.git
git clone git@github.com:Dissonance-Eip/docs.git
```

Clone them as siblings. `ui`'s `dev:with-core` script expects `../core`.

## Prerequisites

| Tool | Version | Needed for |
| --- | --- | --- |
| Git | 2.34+ | everything |
| Node.js | 20.x | `ui` and the `core` addon build — CI uses 20 |
| A C++ toolchain | C++17 | building `core` |
| CMake | 3.11+ | the `core` CLI and unit tests |
| Python 3 | 3.10+ | documentation linter, benchmark scripts |

The C++ toolchain is Xcode Command Line Tools on macOS, Visual Studio 2022 Build
Tools on Windows, or GCC/Clang on Linux. `node-gyp` downloads Node headers from
`nodejs.org` on first build, so that first build needs network access.

## Running the app

The UI ships prebuilt addon binaries under `Build/Release/`, so you can run it
without a C++ toolchain at all:

```bash
cd ui
npm install
npm run dev
```

That is enough to open a WAV, see its metadata and play it back. Binaries are
committed for `darwin-arm64`, `linux-x64` and `win32-x64` only — on any other
platform the app opens but processing fails.

To run the UI against a `core` you have built yourself:

```bash
cd ui
npm run dev:with-core     # builds ../core, then launches with DISSONANCE_CORE_ADDON_PATH set
```

## Building core

```bash
cd core
npm install
npm run build             # the .node addon → build/Release/dissonance_core.node
npm run build:cli:debug   # the CLI → cmake-build/Debug/dissonance.core
```

Try the CLI on the bundled fixture:

```bash
cmake-build/Debug/dissonance.core info test_files/sound.wav
cmake-build/Debug/dissonance.core process test_files/sound.wav \
  --perturbation 0.5 --mode white_noise --output out-processed.wav
```

Run the C++ tests:

```bash
cmake -S . -B cmake-build -DBUILD_CLI=ON -DBUILD_NODE_ADDON=OFF
cmake --build cmake-build
ctest --test-dir cmake-build --output-on-failure
```

`core/README.md` documents the full addon contract and every CLI flag;
`core/DEVELOPMENT.md` is currently out of date and is being corrected.

## Running the checks

| Repository | Command | What it runs |
| --- | --- | --- |
| `ui` | `npm run lint` / `npm run format` | ESLint, Prettier |
| `ui` | `npm test` | Vitest |
| `core` | `ctest --test-dir cmake-build` | GoogleTest suite |
| `core` | `npm run format:cpp:check` / `npm run cppcheck` | clang-format, cppcheck |
| `docs` | `python3 scripts/check-docs.py` | documentation format linter |

## Contribution workflow

1. Branch from `dev` (`main` in `docs`):
   `feature/<short-description>`, `fix/<short-description>`, `docs/<short-description>`.
2. Keep the pull request focused. Explain *why* in the body, not just what.
3. Run the checks above before pushing — CI runs the same ones.
4. Use the PR template; assign a reviewer — UI lead for `ui`, core lead for
   `core` and DSP, docs lead for `docs`.
5. Add or update tests with behaviour changes, and update the documentation the
   change makes wrong.

## Writing documentation

Read [`../DOCUMENTATION_STANDARD.md`](../DOCUMENTATION_STANDARD.md) once, then
start from a skeleton in [`../templates/`](../templates/):

| Template | For |
| --- | --- |
| [`adr.md`](../templates/adr.md) | A technical decision, with alternatives and consequences |
| [`technical-note.md`](../templates/technical-note.md) | How something that exists actually works |
| [`benchmark-report.md`](../templates/benchmark-report.md) | A measured comparison |
| [`meeting-notes.md`](../templates/meeting-notes.md) | Any meeting |

Technical decisions get an ADR in [`../design/core/`](../design/core/) or
`../design/ui/`. This was asked for explicitly in the 2025-11-04 expert meeting:
record the reasoning, not only the outcome.

## Secrets

Never commit keys, tokens or signing certificates. CI uses GitHub Secrets; local
development uses environment variables. Ask the project lead for anything you
need and follow the secure transfer process.

## First week

- [ ] GitHub organisation access confirmed
- [ ] Three repositories cloned as siblings
- [ ] `npm run dev` opens the app and loads a WAV
- [ ] `core` builds and `ctest` passes
- [ ] Read [`milestones.md`](milestones.md) and [`roadmap.md`](roadmap.md)
- [ ] Read the ADRs in [`../design/core/`](../design/core/)
- [ ] Open a first pull request

Good first tasks: fix something this document got wrong; add front matter to a
document that lacks it; pick up a small issue from the current milestone in
[`milestones.md`](milestones.md).

## For leads, when someone joins

- [ ] GitHub organisation and repository access
- [ ] Add to the team channels
- [ ] Assign a buddy for the first week
- [ ] Assign a first issue in the current milestone

## Related

- [`milestones.md`](milestones.md) — where the project is now
- [`roadmap.md`](roadmap.md) — what each milestone is for
- [`../architecture.md`](../architecture.md) — how the pieces fit together
- [`../CONTRIBUTING.md`](../CONTRIBUTING.md) — documentation review workflow
