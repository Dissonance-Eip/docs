---
title: "ADR 004: deployment architecture for the engine"
status: draft
owner: Noé Kurata
created: 2026-10-29
updated: 2026-10-29
milestone: K
tags: [adr, architecture, privacy, licensing]
---

# ADR 004: deployment architecture for the engine

## Summary

Today the engine runs on the user's machine, as a compiled Node native addon
loaded by the Electron app. Audio never leaves the machine and the app works
offline. We keep this for now. The intended direction is to eventually move the
engine behind a server-side API. No date is decided.

## Context

Mentor action 4 asks for a comparison of a hosted API, a local encrypted engine
and an engine on a server, with consequences for licensing, privacy and offline
use. It depends on [ADR 003](2026-10-29-adr-003-open-scope.md), which keeps the
engine closed.

Current state (2026-10-29): the UI calls the addon over IPC (`core:process`,
`core:readMetadata`, `core:writeTags`), see [architecture](../../architecture.md)
and [ADR 002](2026-09-04-adr-002-cpp-native-addon-for-dsp.md). The compiled
addon is shipped to users in the app installers.

## Options considered

### Option A: local native addon (current)

- **How it works:** the engine is compiled to a `.node` file bundled in the app.
- **For:** audio stays on the machine. Works offline. No server to run or pay
  for.
- **Against:** the compiled engine is in the hands of every user and can be
  inspected. The binaries are also committed in the public `ui` repository.
  Updates need an app release.
- **Evidence:** in production since the first app release (v0.1.0).

### Option B: local encrypted engine

- **How it works:** the engine is still shipped to the user, but in an encrypted
  form that the app decrypts at run time.
- **For:** raises the effort needed to extract the engine. Keeps the local and
  offline properties.
- **Against:** the decryption key must live on the user's machine, so it only
  slows down extraction. Adds key management and build complexity.
- **Evidence:** none, not prototyped. TODO(team): confirm this reading of the
  option, which is not further documented in the meeting notes.

### Option C: hosted API or engine on a server

- **How it works:** the app uploads the audio, a server runs the engine and
  returns the processed file. The two names in the issue (hosted API, engine on a
  server) describe the same shape for this comparison. TODO(team): confirm
  whether they were meant to differ (for example a third-party hosted service
  versus a server operated by the team).
- **For:** the engine binary is never distributed. Engine updates need no app
  release. The open app and the closed engine are separated by a network API.
- **Against:** audio leaves the user's machine. Needs internet. The team has to
  run and secure a service, and pay for it. Large files raise bandwidth and
  latency costs.
- **Evidence:** none, not prototyped.

| Criterion | A: local addon | B: local encrypted | C: server |
| --- | --- | --- | --- |
| Audio leaves the machine | No | No | Yes |
| Works offline | Yes | Yes | No |
| Engine binary in users' hands | Yes | Yes (encrypted) | No |
| Infrastructure to operate | None | None | Yes |
| Fits the open front / closed engine split | Yes | Yes | Yes, and cleaner |

## Decision

We will keep Option A for now. The intended direction is Option C, to be taken
when the team decides to operate a service. No date is decided.
TODO(team): record the trigger and the date if one is set.

## Consequences

**Licensing**

- With A, a proprietary binary ships inside an Apache 2.0 app (see
  [ADR 005](2026-10-29-adr-005-apache-2-licence.md)). With C, no engine binary
  ships at all, and the app only holds a client of the API.

**Privacy**

- With A, audio never leaves the machine, which is a property the project can
  state to users today.
- Moving to C means audio is uploaded once per processing. That requires a
  privacy notice, a retention rule, transport security and a decision on whether
  files are stored. TODO(team): define these before any server work starts.

**Offline use**

- A works offline. C does not. TODO(team): decide whether to keep a local mode
  alongside the server mode.

**Follow-up work this creates**

- A new ADR that supersedes this one when the server move is decided, including
  the API definition.
- The addon contract (`process`, `readMetadata`, `writeTags`) is the natural
  seam to carry over to a network API. Versioning rules are in
  [GOVERNANCE.md](../../GOVERNANCE.md).

**What would make us revisit this**

- A decision to operate a server.
- Evidence that the shipped binaries are being extracted or abused.
- Users asking for processing on devices that cannot run the addon.

## Related

- [ADR 003: open scope](2026-10-29-adr-003-open-scope.md)
- [ADR 005: Apache 2.0 licence](2026-10-29-adr-005-apache-2-licence.md)
- [ADR 002: C++ native addon](2026-09-04-adr-002-cpp-native-addon-for-dsp.md)
- [Architecture](../../architecture.md)
- Issue [docs#60](https://github.com/Dissonance-Eip/docs/issues/60)
