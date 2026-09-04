# Contributing to Dissonance docs

## Before you write

Start from a skeleton in [`templates/`](templates/) rather than copying a
previous document, and read
[`DOCUMENTATION_STANDARD.md`](DOCUMENTATION_STANDARD.md) once. It covers front
matter, filenames, headings and where each kind of document belongs.

| You are writing | Use |
| --- | --- |
| A technical decision, with alternatives and consequences | [`templates/adr.md`](templates/adr.md) |
| A description of how something that already exists works | [`templates/technical-note.md`](templates/technical-note.md) |
| A measured comparison | [`templates/benchmark-report.md`](templates/benchmark-report.md) |
| Notes from a meeting | [`templates/meeting-notes.md`](templates/meeting-notes.md) |

## Style

- English throughout, including meeting notes.
- Write what was measured or decided, not what was intended.
- Every number carries its unit and its method — repetitions, machine, date. A
  figure with no method is not evidence.
- Claims about code name the file and the repository:
  `core/src/utils/WavParser.cpp`, not "the parser".
- Cite sources as relative Markdown links. Square brackets around a filename are
  not a link.
- Dates are ISO 8601: `2026-09-04`.

## Before opening a pull request

```bash
python3 scripts/check-docs.py
```

It checks front matter, headings, filenames, bullets and code fences, and exits
non-zero on any violation.

Three things it cannot check, which a reviewer should:

- Does the Summary state the conclusion, or only the topic?
- Does every number say how it was measured?
- Are `status:` and `updated:` honest?

## Pull requests

- Small edits: open a PR with a short description of what changed and why.
- Larger additions: open a draft PR early and request a reviewer — the UI lead
  for UI documents, the core lead for DSP and C++ documents.
- Use the checklist in [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md).
- Put images in the folder of the document that uses them, or in `assets/` when
  they are shared, and give every image alt text that says what it shows.
