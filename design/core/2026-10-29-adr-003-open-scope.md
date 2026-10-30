---
title: "ADR 003: open scope, open front and closed engine"
status: review
owner: Noé Kurata
created: 2026-10-29
updated: 2026-10-29
milestone: K
tags: [adr, licensing, open-source, governance]
---

# ADR 003: open scope, open front and closed engine

## Summary

The desktop app (`ui`) and the documentation (`docs`) are public and open
source under Apache 2.0. The perturbation engine (`core`) stays closed: its
source is not published, and only the compiled addon is distributed, inside the
app. The reason is that the engine is the part that protects audio, and
publishing how it works would let anyone build a countermeasure. This record is
proposed (front matter `status: review`) until the study supervisor (chargé
d'étude) approves it in writing.

## Context

The 2026-09-15 mentor session asked the team to formalise and justify the
openness scope, and to have it validated in writing by the study supervisor
([meeting notes](../../meeting-notes/2026-09-15-meeting-mentor-follow-up.md)).
Facts at the date of writing, 2026-10-29:

- `ui` and `docs` are public GitHub repositories (checked with the GitHub API on
  2026-10-29).
- `core` could not be queried with the same credentials on 2026-10-29 (the API
  answered "not found"), so its visibility is not verified here.
  TODO(team): confirm that `core` is private.
- The compiled addon is built by `core` CI and committed into the public `ui`
  repository under `ui/Build/Release/` (`dissonance_core-darwin-arm64.node`,
  `dissonance_core-linux-x64.node`, `dissonance_core-win32-x64.node`) by the
  workflow `ui/.github/workflows/sync-core-addon.yml`. The app release bundles
  the same binaries.
- The core CLI (`dissonance.core`) is built from source with CMake
  ([core/README.md](https://github.com/Dissonance-Eip/core/blob/dev/README.md)).
  The core release workflow `core/.github/workflows/release-addon.yml` publishes
  only `*.node` files, and the ui release workflow publishes only app installers.
  No CLI binary is distributed by either workflow.
- A first outside contribution has already landed in `ui`: PR #101 by an
  external contributor, merged 2026-10-09, resolved ui#94.

## Options considered

### Option A: everything public

- **How it works:** publish `ui`, `docs` and `core` under one open licence.
- **For:** simplest message, maximum contribution surface, no licence split.
- **Against:** the protection method becomes readable by anyone, including the
  parties it is meant to resist. Any weakness found in it is public at once.
- **Evidence:** none, argument only.

### Option B: open front, closed engine

- **How it works:** `ui` and `docs` public under Apache 2.0. `core` source
  private, all rights reserved. The compiled addon is distributed inside the
  app under the app's terms.
- **For:** contributors can work on everything users see and on the documented
  addon contract without access to the engine. The protection method is not
  published.
- **Against:** contributions to the engine are limited to the team. A compiled
  binary can still be inspected. Users cannot audit the engine source.
- **Evidence:** the outside contribution in `ui` (PR #101) touched only the UI.

### Option C: everything closed

- **How it works:** no public repository.
- **For:** maximum control.
- **Against:** contradicts the objective of the mentor session (open source
  release, contributors after the EIP) and removes the public research
  documentation the jury praised.
- **Evidence:** none.

## Decision

We will adopt Option B.

| Part | Status | Licence |
| --- | --- | --- |
| `ui` (Electron app) | Public, open source | Apache 2.0 |
| `docs` | Public, open source | Apache 2.0 |
| `core` source (perturbation engine, addon glue) | Closed | Proprietary, all rights reserved |
| Compiled addon (`*.node`) | Distributed inside the app and committed in `ui/Build/Release/` | Not covered by Apache 2.0, see the notice in the `ui` repository |
| `core` CLI | TODO(team): decide. Today it is only buildable from the closed source and is not distributed | Follows `core` unless decided otherwise |

The licence choice is justified in
[ADR 005](2026-10-29-adr-005-apache-2-licence.md). How the engine is deployed is
decided in [ADR 004](2026-10-29-adr-004-deployment-architecture.md).

The boundary between the two sides is the documented addon contract
(`process`, `readMetadata`, `writeTags`). Open contributors work against that
contract and never need the engine source.

## Consequences

**Accepted costs**

- No outside contribution to the engine. `CONTRIBUTING.md` says so for `core`.
- The proprietary binaries sit in the git history of a public repository, so
  they can be downloaded and inspected by anyone. TODO(team): decide whether to
  keep committing them to `ui` or to fetch them only at build time.
- Users and reviewers cannot audit the engine. Behaviour is documented through
  measurement (see the research folder), not source.

**Follow-up work this creates**

- LICENSE files in `ui`, `docs` and `core` (in progress, tracked with
  [docs#56](https://github.com/Dissonance-Eip/docs/issues/56)).
- Third-party notices for components compiled into the addon, listed in the
  [dependency inventory](../../planning/dependency-inventory.md).
- Update the sentence in `CONTRIBUTING.md` that says the engine "may become
  closed source" once this record is approved.

**What would make us revisit this**

- The study supervisor or the mentor rejects the scope.
- A decision to move the engine behind a server-side API, which changes what is
  distributed (see ADR 004).
- A request to open the CLI or parts of the engine.

## Validation

This record stays `status: review` (proposed) until the study supervisor approves it in writing.

| Item | Value |
| --- | --- |
| Approver | TODO(team): name of the chargé d'étude |
| Date requested | TODO(team) |
| Date answered | TODO(team) |
| Link to the written answer | TODO(team): add the link here |

When the link is filled in, set `status` to `final` and bump `updated`.

## Related

- [ADR 005: Apache 2.0 licence](2026-10-29-adr-005-apache-2-licence.md)
- [ADR 004: deployment architecture](2026-10-29-adr-004-deployment-architecture.md)
- [Dependency and licence inventory](../../planning/dependency-inventory.md)
- [Governance](../../GOVERNANCE.md)
- [Mentor follow-up meeting, 2026-09-15](../../meeting-notes/2026-09-15-meeting-mentor-follow-up.md)
- Issue [docs#55](https://github.com/Dissonance-Eip/docs/issues/55)
