# Contributing to Dissonance

Dissonance is split across three repositories, and this guide covers all of
them:

| Repository | What it is | Pull requests go to |
| --- | --- | --- |
| [ui](https://github.com/Dissonance-Eip/ui) | The Electron desktop app | `dev` |
| [core](https://github.com/Dissonance-Eip/core) | The C++ audio engine, used by the app as a Node addon and as a CLI | `dev` |
| [docs](https://github.com/Dissonance-Eip/docs) | Research, planning and documentation | `main` |

New here? Issues labelled
[`good first issue`](https://github.com/Dissonance-Eip/ui/issues?q=is%3Aopen+label%3A%22good+first+issue%22)
are small and self-contained. Found a security problem? Do not open a public
issue; follow the [security policy](.github/SECURITY.md) instead.

## Workflow

The same steps apply in every repository.

1. **Start from an issue.** Every change has an issue, so pick an existing one
   or open a new one first. Comment on it to say you are taking it.
2. **Branch from the issue.** Maintainers use "Create a branch" in the issue
   sidebar, or `gh issue develop <number> --base dev --checkout`. Outside
   contributors fork the repository and branch from `dev` (from `main` in
   docs). Name the branch `<issue-number>-short-description`.
3. **Commit in the team format** ([Conventional Commits](https://www.conventionalcommits.org)):
   `type(scope): summary (#issue)`, for example
   `fix(core): stop processing from lowering the level and cutting high frequencies (#107)`.
   Types: `feat`, `fix`, `test`, `docs`, `refactor`, `style`, `chore`, `ci`,
   `build`.
4. **Open a pull request** against `dev` (`main` in docs) and link the issue in
   the description. `main` in ui and core only receives releases, so a pull
   request against it will be asked to move.
5. **Get it reviewed.** CI has to pass, and the other maintainer reviews every
   pull request before it is merged with a merge commit. Merging into `dev`
   does not close the issue automatically; the maintainer closes it.

## App (ui)

Needs Node.js 20 and npm.

```bash
npm install
npm run dev
```

The app loads a prebuilt engine from `Build/Release/`, synced from the latest
core release, so you do not need to build core to work on the app. To run it
against your own core build instead, keep `core` next to `ui` and run
`npm run dev:with-core`.

Before opening a pull request, run the same checks as CI:

```bash
npm run lint
npm run format:check
npm test
npm run build
```

`npm run format` fixes formatting, and `npm run lint:fix` fixes what ESLint can.

## Audio engine (core)

Needs CMake 3.11 or later, a C++17 compiler, GoogleTest, Node.js 20, and
clang-format and cppcheck for the checks (`brew install cmake googletest
clang-format cppcheck` on macOS, or
`apt install cmake g++ libgtest-dev clang-format cppcheck` on Debian and
Ubuntu).

Build the engine and the CLI, then run the tests from the repository root, so
the tests that read files from `test_files/` find them:

```bash
cmake -S . -B build -DBUILD_CLI=ON -DBUILD_NODE_ADDON=OFF
cmake --build build
./build/runTests
```

The Node addon the app uses builds with `npm install` then `npm run build`,
into `build/Release/dissonance_core.node`.

Before opening a pull request:

```bash
npm run format:cpp    # CI fails on unformatted C++
npm run cppcheck
```

The perturbation engine may become closed source (see
[ADR 003, issue #55](https://github.com/Dissonance-Eip/docs/issues/55)); if it
does, this section will say how contributions to it work.

## Documentation (docs)

### Before you write

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

### Style

- English throughout, including meeting notes.
- Write what was measured or decided, not what was intended.
- Every number carries its unit and its method — repetitions, machine, date. A
  figure with no method is not evidence.
- Claims about code name the file and the repository:
  `core/src/utils/WavParser.cpp`, not "the parser".
- Cite sources as relative Markdown links. Square brackets around a filename are
  not a link.
- Dates are ISO 8601: `2026-09-04`.

### Before opening a pull request

```bash
python3 scripts/check-docs.py
```

It checks front matter, headings, filenames, bullets and code fences, and exits
non-zero on any violation.

Three things it cannot check, which a reviewer should:

- Does the Summary state the conclusion, or only the topic?
- Does every number say how it was measured?
- Are `status:` and `updated:` honest?

### Pull requests

- Small edits: open a PR with a short description of what changed and why.
- Larger additions: open a draft PR early and request a reviewer — the UI lead
  for UI documents, the core lead for DSP and C++ documents.
- Use the checklist in [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md).
- Put images in the folder of the document that uses them, or in `assets/` when
  they are shared, and give every image alt text that says what it shows.
