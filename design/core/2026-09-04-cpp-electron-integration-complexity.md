---
title: C++ into Electron — integration complexity
status: final
owner: Luca Martinet
created: 2026-09-04
updated: 2026-09-04
milestone: E3
tags: [core, ui, electron, build, packaging]
---

# C++ into Electron — integration complexity

## Summary

The C++ core reaches the Electron app as a Node native addon, and the machinery
that makes that happen — N-API bindings, a three-platform CI matrix, a
cross-repo release-and-commit pipeline, a five-strategy runtime loader — already
exists and works. The integration is done. The cost is not in building it again;
it is in the six failure modes it carries, four of which are silent.

The two that matter most: **the UI has no version relationship with the core it
ships**, so a stale or mismatched binary produces wrong audio rather than an
error; and **the CI gate that is supposed to test the addon runs `echo`**, so a
broken addon can reach a release. Both are cheap to fix and neither depends on
the E4 migration decision.

Three platforms a user might plausibly be on — Intel Mac, ARM Windows, ARM Linux
— have no binary at all, and on those the app starts and every operation fails.

**Recommendation for E4:** the integration cost is real but it is largely
*already paid*. Migrating away from C++ to avoid it would be paying a second
cost to recover the first. The decision should turn on whether the DSP pipeline
needs native performance (not yet measured — see E2), not on integration
difficulty.

## What the integration is made of

Audited at `core` `dev` / `13bac85` and `ui` `dev` / `a9b099c`, both 2026-09-02.

```text
   core repo                      GitHub                      ui repo
┌──────────────┐          ┌────────────────────┐        ┌──────────────────┐
│ C++ sources  │          │                    │        │ Build/Release/   │
│ binding.gyp  │─ CI ────▶│ Release assets     │─ CI ──▶│  *-darwin-arm64  │
│ addon.cpp    │  build   │  3 × .node         │  sync  │  *-linux-x64     │
└──────────────┘  matrix  │                    │ commit │  *-win32-x64     │
                          └────────────────────┘        └────────┬─────────┘
                                                                 │ require()
                                                        ┌────────▼─────────┐
                                                        │ CoreAddonLoader  │
                                                        │  → ipcMain       │
                                                        │  → preload       │
                                                        │  → renderer      │
                                                        └──────────────────┘
```

| Layer | Where | Lines / size |
| --- | --- | --- |
| N-API bindings | `core/src/addon/addon.cpp` | 3 async workers, ~250 lines |
| Addon build | `core/binding.gyp` + `scripts/build-addon.js` | 14 sources listed by hand |
| CLI/test build | `core/CMakeLists.txt` | the same 13 sources, listed again |
| Release matrix | `core/.github/workflows/release-addon.yml` | 3 runners |
| Binary sync | `ui/.github/workflows/sync-core-addon.yml` | commits binaries into `ui` |
| Runtime loader | `ui/ipcHandlers/core/CoreAddonLoader.js` | 5 resolution strategies, 113 lines |
| IPC surface | `ui/ipcHandlers/core/CoreIpcHandlers.js` | 4 `core:*` channels |

## What it costs

### Build

Compiling the 13 core `.cpp` files at `-O2` takes **8.0 s** on 2 vCPU
(Xeon 2.80 GHz); the linked addon is 232 KB on darwin-arm64, 259 KB on
linux-x64, 427 KB on win32-x64. That is not a meaningful cost.

The costs that are real:

- **`node-gyp` needs the network at build time.** It fetches Node headers from
  `nodejs.org` unless `~/.cache/node-gyp` is already warm. On a machine with
  restricted egress `npm install` in `core` fails outright — reproduced while
  writing this document. Any contributor behind a corporate proxy hits it.
- **Toolchain per platform.** Xcode command-line tools, Visual Studio Build
  Tools, or GCC. A new contributor cannot run the UI against a locally built
  core without one.
- **A pinned Windows runner.** `release-addon.yml` is pinned to `windows-2022`
  with a comment explaining that `windows-latest` moved to VS 18, which
  `node-gyp` 10.x cannot detect. This is a live maintenance obligation: the pin
  works until GitHub retires the image, and the fix is a `node-gyp` upgrade
  someone has to do.

### Source lists in two places

`binding.gyp` lists 14 sources; `CMakeLists.txt` lists the same 13 plus kissfft
through `FetchContent`. Adding a `.cpp` file means editing both. Forget the
`binding.gyp` entry and the CLI and tests build while the addon fails to link;
forget the CMake entry and the addon works while CI's tests do not compile.
Nothing checks that the lists agree.

Worth noting the two builds do not even source kissfft the same way: CMake
fetches it from GitHub at configure time, `binding.gyp` compiles the vendored
copy at `vendor/kissfft/kiss_fft.c`. They can drift.

### Distribution

`sync-core-addon.yml` downloads `*.node` from the **latest** GitHub release of
`Dissonance-Eip/core` and commits ~918 KB of binaries into the `ui` repo on
`dev`. That is a deliberate and defensible choice — it makes `git clone && npm
install && npm run dev` work with no C++ toolchain, which matters for a
four-person team. The costs it accepts:

- Binaries in git history, growing with every core release.
- `electron-builder` has no `files` filter, so **every installer ships all three
  platforms' binaries** — the Linux AppImage carries a Windows `.node` it can
  never load.
- Nothing ties a UI commit to the core commit its binary came from.

## Failure modes

Ranked by how quietly they fail.

### 1. No version relationship between UI and core — silent

The loader `require()`s whatever `.node` is present. There is no version field
in the addon, no check at load, and no record in the `ui` repo of which core
commit produced the committed binaries — the sync commit message is
`chore(ui): sync core addon binaries [skip ci]` and names no version.

`sync-core-addon.yml` pulls from the **latest** release, and
`release-addon.yml` publishes dev builds tagged `dev-<run-id>` on
`workflow_dispatch` alongside real `v*` tags. A manual dispatch can therefore
make an unreviewed dev build the "latest" one the UI syncs.

The failure is not a crash. It is the app running a superseded DSP pipeline and
writing plausible-looking audio. Nobody would notice.

**Fix:** export a `version` from the addon, assert it at load, and put the core
tag in the sync commit message. An afternoon.

### 2. The CI test gate is a no-op — silent

`core/package.json`:

```json
"test": "echo \"JS tests removed — DSP covered by CTest\""
```

`release-addon.yml` has a step named **"Run addon JS tests"** that runs
`npm test`, and a step before it that *fails the build if the `test` script is
missing*. So the pipeline carefully verifies that a script exists, runs it, and
the script prints a sentence and exits 0.

The smoke test beside it is real but thin — it checks that `process` is a
function, and does not check `readMetadata` or `writeTags`, both of which the UI
depends on:

```js
const required = ['process'];
```

The DSP genuinely is covered by CTest in `ci.yml`. What is not covered anywhere
is the addon boundary: that the built `.node` exposes the contract
`core/README.md` documents.

**Fix:** make the smoke test require all three exports and call `readMetadata`
on `test_files/sound.wav`, asserting the header fields. Twenty lines, and it
would catch a genuinely broken release.

### 3. Three plausible platforms have no binary — loud, but unhelpful

Shipped: `darwin-arm64`, `linux-x64`, `win32-x64`. Missing: `darwin-x64` (Intel
Macs, still widely used in studios), `win32-arm64`, `linux-arm64`.

On those, the loader exhausts every candidate, falls through to the
`dissonance-core` package and to `bindings`, and returns `null`. The app opens,
the user drops a file, and processing fails. `release-app.yml` already documents
the macOS side: "the macOS build is Apple Silicon (arm64) only — matches the
single darwin-arm64 addon the core repo ships."

**Fix:** add `macos-13` (Intel) to the release matrix — one line, and it covers
the platform most likely to be a paying user. ARM Windows and ARM Linux can
wait. Separately, when the addon is missing, the UI should say so on startup
rather than at the first Process click.

### 4. `.gitignore` says `build/`, the binaries live in `Build/` — a trap

`ui/.gitignore` ignores `build/`. The committed addons are in `Build/Release/`.
Gitignore patterns are case-sensitive, so the capital-B path is tracked, which
is what the design intends — but the loader's candidate list contains **both**
`Build/Release/` and `build/Release/`. A developer who builds locally into
`build/Release/` gets a binary that is correctly ignored and silently takes
priority over the synced one on a case-sensitive filesystem, and collides with
it on macOS or Windows where the two paths are the same directory.

**Fix:** pick one spelling. `Build/` is already committed, so make the loader
look only there plus the `DISSONANCE_CORE_ADDON_PATH` override, and ignore
`build/` everywhere.

### 5. Five loading strategies, one of which cannot succeed

The loader tries, in order: the env override, a platform-named `.node` in
`Build/Release/`, generic names in `Build/Release/` and `build/Release/`, the
`dissonance-core` npm package, and `bindings()`.

`dissonance-core` is not a dependency of `ui/package.json` and is not published,
so strategy 4 can never succeed. `bindings` *is* a dependency and would look in
`build/Release/`, which strategies 3 and 4 already covered. Every path is
wrapped in try/catch and the loader never throws, which is right for a main
process — but it also means a misconfiguration produces `console.log` output and
a `null`, and nothing surfaces to the user.

**Fix:** drop strategies 4 and 5; surface `null` as a startup-time error.

### 6. N-API is doing the hard part, and it is worth saying so

The addon builds against Node 20 in CI and is loaded by Electron 40, which
embeds a different V8 and a different Node. That works because `binding.gyp`
uses `node-addon-api` over N-API, which is ABI-stable across Node and Electron
versions: an addon built against N-API 8 keeps loading on later runtimes without
recompilation.

Had the addon used raw V8 or NAN, every Electron upgrade would require a rebuild
of all three binaries. This is the single largest integration cost the project
already avoided, and it should be recorded as a constraint: **anything that
replaces the addon must stay on N-API**.

## Cost matrix for E4

Effort is calendar time for one person already familiar with the code.

| Dimension | Keep the C++ addon | Move audio path to TypeScript | Move to WebAssembly |
| --- | --- | --- | --- |
| Build toolchain | Xcode / VS / GCC per platform | none | Emscripten, one toolchain |
| CI runners needed | 3 native | 1 | 1 |
| Binaries in the UI repo | 3, ~918 KB | 0 | 1 `.wasm`, portable |
| Platform coverage | 3 of 6 today | all | all |
| ABI risk | none (N-API) | none | none |
| Parsing speed | baseline | 2.2–3.5× slower ([E2](../../research/benchmarks/2026-09-04-cpp-vs-node-wav-parsing/)) | not measured |
| DSP speed | baseline | **not measured** | **not measured** |
| Debugging | two toolchains, two debuggers | one | awkward — no source-level debugging in practice |
| Work already done | **all of it** | rewrite parser + DSP | rewrite build, keep C++ sources |
| Work to remove it | — | delete the addon, the sync pipeline, the loader | replace the build, keep the rest |

The row that decides this is "DSP speed", and it is empty. E2 measured parsing,
where C++ wins by a factor that does not justify the machinery. The FFT, masking
and perturbation stages are a different shape of work — compute-bound, not
memory-bound — and that is where a 10× would actually change the product.

## Recommendation

1. **Do not migrate away from C++ on integration grounds.** The integration
   exists, works, and is on the ABI-stable path. Its costs are maintenance, not
   construction, and construction is the expensive half.
2. **Benchmark the DSP pipeline before writing E4**, with the same method as E2:
   an equivalence check first, then C++ against a TypeScript and a WASM build of
   the same algorithm. That is the measurement E4 actually needs.
3. **Fix the two silent failures now**, independent of E4 — the version check
   (#1) and the real smoke test (#2). Together, about a day.
4. **Add `macos-13` to the release matrix**, one line, covering Intel Macs.
5. **If E4 chooses WebAssembly**, note that it keeps the C++ sources and replaces
   only the build and loading layers. It is the cheapest way out of the
   three-platform matrix without discarding the DSP work — and it removes the
   `node-gyp` network dependency at the same time.

## Follow-up issues

| # | Issue | Effort | Blocks |
| --- | --- | --- | --- |
| 1 | Addon exports a version; loader asserts it; sync commit names the core tag | ~4 h | — |
| 2 | Smoke test requires all three exports and calls `readMetadata` | ~2 h | — |
| 3 | Add `macos-13` (Intel) to the release matrix | ~15 min | — |
| 4 | Settle on `Build/` and drop `build/` from the loader and `.gitignore` | ~1 h | — |
| 5 | Drop the two unreachable loader strategies; surface a missing addon at startup | ~2 h | — |
| 6 | Generate the source list once, shared by `binding.gyp` and `CMakeLists.txt` | ~3 h | — |
| 7 | `files` filter in `electron-builder` so each installer ships only its own `.node` | ~1 h | — |
| 8 | Benchmark the DSP pipeline (C++ / TS / WASM) | ~3 d | **E4** |

## Related

- [`2026-09-04-cpp-wav-parser-audit.md`](2026-09-04-cpp-wav-parser-audit.md) — E1, what the C++ parser does
- [`../../research/benchmarks/2026-09-04-cpp-vs-node-wav-parsing/`](../../research/benchmarks/2026-09-04-cpp-vs-node-wav-parsing/) — E2, measured parsing performance
- [`../../research/benchmarks/2026-05-31-poc-electron-audio-loader.md`](../../research/benchmarks/2026-05-31-poc-electron-audio-loader.md) — the addon loader, in detail
- [`../../research/benchmarks/2025-11-21-electron-comparative-study.md`](../../research/benchmarks/2025-11-21-electron-comparative-study.md) — the original JUCE vs Electron decision
- [`../../architecture.md`](../../architecture.md) — IPC channels and data flow
- [`../../planning/milestones.md`](../../planning/milestones.md) — Milestone E task list
