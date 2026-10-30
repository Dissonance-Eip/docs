---
title: "ADR 005: Apache 2.0 for the open parts"
status: draft
owner: Noé Kurata
created: 2026-10-29
updated: 2026-10-29
milestone: K
tags: [adr, licensing, open-source]
---

# ADR 005: Apache 2.0 for the open parts

## Summary

`ui` and `docs` are licensed under Apache 2.0, not MIT. Apache 2.0 adds an
explicit patent grant and patent-retaliation clause, is compatible with every
dependency licence found in the [inventory](../../planning/dependency-inventory.md),
and says clearly that it covers only the files it is attached to, which lets a
proprietary compiled addon ship inside an Apache 2.0 app. The engine (`core`)
is proprietary, as set by [ADR 003](2026-10-29-adr-003-open-scope.md).

## Context

The mentor suggested MIT or Apache 2.0 for the open part. `ui/package.json`
declared MIT before this decision and no repository had a LICENSE file. The
project ships a compiled proprietary addon inside an open-source app, and uses
third-party code that needs its notices kept.

This is a project decision and not legal advice. TODO(team): confirm with the
study supervisor or a legal contact if the school offers one.

## Options considered

### Option A: MIT

- **How it works:** short permissive licence, requires keeping the copyright and
  licence notice.
- **For:** shortest text, most widely recognised, already declared in
  `ui/package.json`.
- **Against:** no express patent grant, so users and contributors rely on an
  implied licence for patents. No explicit statement about trademarks and about
  contributions.
- **Evidence:** licence texts.

### Option B: Apache 2.0

- **How it works:** permissive licence with an express patent licence from each
  contributor, a clause that ends the patent licence of anyone who sues over
  the work, a contribution clause (section 5) that licenses contributions under
  the same terms, and a rule that modified files carry a change notice.
- **For:** the patent grant protects users of the app and contributors. The
  contribution clause removes the need for a separate contributor agreement for
  a small team. It states that trademarks are not licensed.
- **Against:** longer text, and a NOTICE file to maintain. It is not compatible
  with GPLv2-only code (not relevant here, none found).
- **Evidence:** the inventory found no GPL-family dependency.

### Option C: copyleft (GPL or AGPL)

- **How it works:** derivative works must be released under the same licence.
- **For:** keeps improvements open.
- **Against:** the app loads a proprietary addon, which a copyleft licence would
  make hard to justify. Rejected without further analysis.
- **Evidence:** none.

## Decision

We will use Apache 2.0 for `ui` and `docs`, with the copyright line
"Copyright 2025-2026 Noé Kurata and Luca Martinet", and a proprietary
"all rights reserved" notice for `core`.

- **Patent grant:** chosen over MIT for the express patent licence and
  retaliation clause.
- **Compatibility with dependencies:** all direct and runtime dependencies of
  `ui` are MIT. The other licences found are permissive (ISC, BSD, Apache 2.0,
  BlueOak, 0BSD, CC0, Python-2.0, WTFPL) or MPL-2.0 (file-level copyleft, dev
  tooling only, not shipped). No GPL, LGPL or AGPL package is present. The
  C++ library compiled into the addon is BSD-3-Clause, which is compatible with
  both Apache 2.0 and a proprietary licence. Details and versions are in the
  [inventory](../../planning/dependency-inventory.md).
- **Coexistence with the closed engine:** Apache 2.0 applies to the files that
  carry it. The addon binary is a separate work, and the `NOTICE` file in `ui`
  says it is not covered by Apache 2.0. Apache 2.0 does not require the addon to
  be open, and does not forbid distributing it next to open code.
- **BSD-3-Clause obligation:** distributing the addon in binary form requires
  reproducing the library's copyright notice and licence text in the
  documentation or other materials shipped with it.
  TODO(team): confirm where this notice is shipped with the app.

## Consequences

**Accepted costs**

- A NOTICE file to keep accurate in `ui`.
- Contributors to `ui` and `docs` license their work under Apache 2.0 by
  contributing (section 5 of the licence).
- `ui/package.json` must say `Apache-2.0` (it said `MIT`). Tracked in the `ui`
  repository.

**Follow-up work this creates**

- Keep the [inventory](../../planning/dependency-inventory.md) current before
  each release.

**What would make us revisit this**

- A dependency under a licence that conflicts with Apache 2.0.
- A decision to open the engine, or to move it server-side (ADR 004).

## Related

- [ADR 003: open scope](2026-10-29-adr-003-open-scope.md)
- [ADR 004: deployment architecture](2026-10-29-adr-004-deployment-architecture.md)
- [Dependency and licence inventory](../../planning/dependency-inventory.md)
- [LICENSE](../../LICENSE)
- Issue [docs#56](https://github.com/Dissonance-Eip/docs/issues/56)
