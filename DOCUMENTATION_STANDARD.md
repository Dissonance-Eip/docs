---
title: Documentation standard
status: active
owner: Luca Martinet
created: 2026-09-04
updated: 2026-09-04
milestone: E
tags: [process, documentation]
---

# Documentation standard

Every Markdown file in `dissonance-docs` follows the rules below. They exist so a
reader can tell, in five seconds, what a document is, whether it is still true,
and who to ask about it — and so that files sort, link and search predictably.

New documents follow this from the start. Every existing document was migrated
to it on 2026-09-04, and `scripts/check-docs.py` reports the repository clean —
run it before opening a pull request to keep it that way.

## Summary of the rules

| Rule | Value |
| --- | --- |
| Front matter | YAML block, required on every `.md` file |
| Top heading | Exactly one ATX `#`, matching the front-matter `title` |
| Filenames | lowercase `kebab-case`, ASCII only |
| Dated artifacts | `YYYY-MM-DD-slug.md` |
| Dates in text | ISO 8601 — `2026-09-04`, never `04/09/2026` |
| Headings | ATX (`##`), no level skipped, sentence case |
| Bullets | `-`, no leading space |
| Code fences | Always tagged with a language |
| Links | Relative paths within the repo |

## 1. Front matter

Every file opens with a YAML block. Nothing precedes it.

```yaml
---
title: Benchmark — C++ vs Node WAV parsing
status: final
owner: Luca Martinet
created: 2026-09-04
updated: 2026-09-04
milestone: E
tags: [benchmark, core, performance]
---
```

| Field | Required | Notes |
| --- | --- | --- |
| `title` | yes | Sentence case. Repeated verbatim as the `#` heading. |
| `status` | yes | `draft`, `review`, `final`, `active`, or `superseded`. |
| `owner` | yes | The person who answers questions about it, not necessarily the author. |
| `created` | yes | ISO date the document was first committed. |
| `updated` | yes | ISO date of the last substantive edit. Bump it in the same commit. |
| `milestone` | when applicable | Milestone letter or task ID (`E`, `E2`). Omit for process docs. |
| `tags` | no | Lowercase, flat list. Use existing tags before inventing one. |
| `supersedes` | when applicable | Relative path to the document this replaces. |

`status` is the field that earns its keep. A document marked `final` is safe to
cite in a jury presentation; a `draft` is not. A document nobody has confirmed in
six months is `draft` again, whatever it says.

## 2. Filenames

Lowercase, ASCII, words separated by `-`. No spaces, no `&`, no `_`, no
uppercase, no accents. These names end up in URLs and in shell commands, and the
current mix of `2025_11_04-MeetingExpert.md`, `academic-researcher.md` and
`2026-01-18-Dissonance-User-Need&Pain.md` breaks tab-completion, sorting and
Markdown links in different ways each time.

**Dated artifacts** — anything that captures a moment: meeting notes, studies,
benchmark runs, survey exports. Prefix with the ISO date so the folder sorts
chronologically:

```text
meeting-notes/2026-05-28-presentation-feedback.md
research/benchmarks/2026-09-04-cpp-vs-node-wav-parsing/
```

**Living documents** — anything that is kept current: the roadmap, the testing
policy, a persona. No date prefix; `updated` in the front matter carries that
information:

```text
planning/testing-policy-core.md
research/personas/audio-engineer.md
```

A benchmark or study that ships scripts, data or images is a **folder**, not a
file. The folder is named as the artifact would be; the prose lives in its
`README.md`.

## 3. Structure

One `#` heading, first line after the front matter, identical to `title`. Never
a second `#`; never a document that opens at `##`.

Immediately after the heading, a **Summary**: two to four sentences answering
what this is, what was found, and what the reader should do about it. A reader
who stops there should still have the conclusion. Studies with a recommendation
put the recommendation here, not on the last page.

Then the body, in ATX headings, no level skipped. Numbered section headings
(`## 1. Goal`) are fine for long studies and should be left off short ones.

Every document ends with a **Related** section listing the documents, issues and
source files it depends on or supersedes, as relative links.

## 4. Prose

- English, throughout, including meeting notes. Mixed-language files cannot be
  searched consistently and cannot be handed to an external reader.
- Write what was measured or decided, not what was intended. "Node decodes
  16-bit PCM at 175 Msample/s" beats "Node performance is acceptable".
- Every number carries its unit and, where it came from a measurement, its
  method — repetitions, machine, date. A figure with no method is not evidence.
- Cite sources as relative links to files in this repo, or full URLs to external
  material. `[music-label-executive.md]` in square brackets is not a link and does
  not resolve.
- Claims about code name the file: `core/src/utils/WavParser.cpp`, not "the
  parser". Paths are relative to the repo root of whichever repo is named.

## 5. Formatting

- Bullets use `-` at column zero. Not `*`, not indented one space.
- Code fences always declare a language: ` ```bash `, ` ```cpp `, ` ```json `.
  An untagged fence loses syntax highlighting on GitHub.
- Tables get a header row and aligned pipes where practical.
- Horizontal rules (`---`) are not section separators. Headings are.
- Images live beside the document that uses them, or in `assets/images/` when
  shared. Every image has alt text.

## 6. Where a document goes

| Content | Location |
| --- | --- |
| Tech watch, veille notes | `research/veille/` |
| Measured comparisons, POCs | `research/benchmarks/` |
| Expert interviews | `research/interviews/` |
| Survey exports and analyses | `research/surveys/` |
| Personas | `research/personas/` |
| Architecture decisions (ADRs) | `design/core/` or `design/ui/` |
| UI flows and mockups | `design/ui/` |
| Roadmap, milestones, policies, onboarding | `planning/` |
| Meeting notes | `meeting-notes/` |
| Reusable document skeletons | `templates/` |

`README.md` lists the folders this repo actually has. When a new top-level
folder appears, it is added there in the same commit.

## 7. Templates

Start from a template rather than from a previous document — copying a previous
document is how two meeting notes ended up with "Meeting notes template" as
their first line.

| Template | Use for |
| --- | --- |
| [`templates/adr.md`](templates/adr.md) | A technical decision with alternatives and consequences |
| [`templates/technical-note.md`](templates/technical-note.md) | Documenting how an existing component works |
| [`templates/benchmark-report.md`](templates/benchmark-report.md) | A measured comparison with reproducible scripts |
| [`templates/meeting-notes.md`](templates/meeting-notes.md) | Any meeting |

Delete the instructional comments from a template once you have filled it in.

## 8. ADRs

The 2025-11-04 expert meeting asked the team to record the reasoning behind
technical choices, not only the outcome. That is what an ADR is: one file per
decision, in `design/core/` or `design/ui/`, named
`YYYY-MM-DD-adr-NNN-short-title.md`, numbered sequentially from `001`.

An ADR is written when a choice constrains future work: a language, a library, a
protocol, a file format, a build system. It is never edited after it reaches
`status: final` — a decision that changes gets a new ADR whose front matter
`supersedes` the old one, and the old one becomes `status: superseded`. The
history is the point.

## 9. Exemptions

GitHub owns the names and the front-matter schema of a few files, so these are
outside the rules above and the linter skips them:

- `README.md` and `CONTRIBUTING.md` — conventional uppercase, no front matter.
- `.github/**` — `PULL_REQUEST_TEMPLATE.md`, `ISSUE_TEMPLATE/*.md`. GitHub
  requires these exact names and parses its own `name:` / `about:` front matter.
- A benchmark's `results/` folder — generated data and generated tables, not
  documents. The benchmark's `README.md` is the document.
- `templates/` — placeholder front matter (`YYYY-MM-DD`) is checked for shape
  only, not for a real date.

Everything else in the repo follows this document.

## 10. Checking

`scripts/check-docs.py` enforces the mechanical rules — front matter and its
required fields, one ATX `#`, filename shape, ISO dates, bullet markers, tagged
code fences, leftover template headers. Run it before opening a pull request:

```bash
python3 scripts/check-docs.py
```

It exits non-zero on any violation and prints one line per problem, so it can be
wired into CI as a required check whenever the team decides to.

The three things it cannot check are the ones that matter most, so a reviewer
checks them by hand:

- Does the Summary state the conclusion, or only the topic?
- Does every number say how it was measured?
- Is `status` honest?

## Related

- [`CONTRIBUTING.md`](CONTRIBUTING.md) — contribution workflow and PR checklist
- [`README.md`](README.md) — repository map
