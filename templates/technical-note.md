---
title: "<Component> — <what this note covers>"
status: draft
owner: <name>
created: YYYY-MM-DD
updated: YYYY-MM-DD
milestone: <letter or task ID>
tags: [core]
---

# <Component> — <what this note covers>

<!--
For documenting how something that already exists actually works: a parser, a
loader, a pipeline stage, an IPC surface. Not for proposing something new —
that is an ADR.

Write it from the source, and name the source files. A note that describes what
the code was meant to do rather than what it does is worse than no note.
Delete these comments once filled in.
-->

## Summary

<!-- What this component is, where it lives, and the two or three things a
reader most needs to know before touching it. -->

## Where it lives

| File | Role |
| --- | --- |
| `repo/path/to/File.hpp` | <public interface> |
| `repo/path/to/File.cpp` | <implementation> |

<!-- Say which repo and which branch these paths are on, and at which commit
this note was written. Code moves. -->

## Public interface

<!-- The API as a caller sees it. Signatures, ownership, threading, what can
throw. Types and units, not prose approximations. -->

## How it works

<!-- The control flow, in the order the code executes it. A short diagram or
step list beats paragraphs. Keep implementation detail that a caller cannot
observe out of this section — put it under Implementation notes. -->

## What it supports

<!-- The concrete matrix: formats, sizes, encodings, platforms. A table with a
row per case and an explicit "not supported" where that is the answer. -->

## Error handling

<!-- Which exceptions or error values, thrown from where, and what a caller is
expected to do about each. -->

## Known limitations

<!-- Behaviour that is surprising, wrong, or merely absent, with the evidence
for each and a linked issue where one exists. This is the section that makes
the note worth writing — do not soften it. -->

## Usage

```cpp
// The smallest thing that works.
```

## Related

- <tests covering this component>
- <benchmarks that measured it>
- <the ADR that chose this design>
