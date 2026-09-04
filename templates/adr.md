---
title: "ADR NNN — <the decision, as a short noun phrase>"
status: draft
owner: <name>
created: YYYY-MM-DD
updated: YYYY-MM-DD
milestone: <letter or task ID>
tags: [adr]
---

# ADR NNN — <the decision, as a short noun phrase>

<!--
Copy to design/core/ or design/ui/ as YYYY-MM-DD-adr-NNN-short-title.md.
Number sequentially from 001 across the whole repo.
Delete these comments once filled in.
An ADR is never edited after status: final — supersede it with a new one.
-->

## Summary

<!-- Two to four sentences: what was decided, and the one reason that decided
it. A reader who stops here knows the outcome. -->

## Context

<!-- What forced a decision now. Constraints that were real at the time:
deadlines, team size, existing code, the milestone this sits in. Include the
numbers that mattered — link the benchmark or study that produced them. -->

## Options considered

### Option A — <name>

- **How it works:** <one or two sentences>
- **For:** <concrete advantages>
- **Against:** <concrete costs>
- **Evidence:** <link to the measurement, or "none — estimated">

### Option B — <name>

- **How it works:**
- **For:**
- **Against:**
- **Evidence:**

<!-- Options that were rejected quickly still get a line. "We did not consider
X" is a question a reviewer will ask. -->

## Decision

<!-- The chosen option, stated as a decision: "We will ...". Then the reason,
tied to the criteria in Context. -->

## Consequences

**Accepted costs**

- <what becomes harder or slower>

**Follow-up work this creates**

- <issue or task, linked>

**What would make us revisit this**

- <the concrete signal — a measurement crossing a threshold, a platform
  dropping support, a dependency going unmaintained>

## Related

- <links to the benchmark, study, or issue behind this decision>
- <the ADR this supersedes, if any>
