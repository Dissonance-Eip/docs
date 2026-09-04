# Dissonance — documentation

Research, planning and technical documentation for Dissonance, an adversarial
audio protection tool. The code lives in two sibling repositories:

| Repository | What it holds |
| --- | --- |
| [`core`](https://github.com/Dissonance-Eip/core) | C++ DSP engine, exposed to the app as a Node native addon, plus a CLI |
| [`ui`](https://github.com/Dissonance-Eip/ui) | Electron desktop application |
| [`Tester`](https://github.com/Dissonance-Eip/Tester) | Perturbation testing harness |

## Where things are

```text
planning/          roadmap, milestones, onboarding, policies, documentation audits
design/
  core/            architecture decision records and C++ technical notes
  ui/              UI flows and mockups
research/
  benchmarks/      measured comparisons and POCs — one folder per study
  personas/        user personas
  surveys/         survey exports and analyses
  interviews/      expert interview notes
  veille/          ongoing tech watch
meeting-notes/     one file per meeting, YYYY-MM-DD-topic.md
templates/         document skeletons — start here, not from a previous file
scripts/           check-docs.py, the documentation linter
assets/            images, audio samples, slide decks
```

## Where to start

- **What is the project doing right now?** [`planning/milestones.md`](planning/milestones.md)
- **Why does it work the way it does?** [`design/core/`](design/core/) — the ADRs
- **New to the team?** [`planning/onboarding.md`](planning/onboarding.md)
- **How the pieces fit together:** [`architecture.md`](architecture.md)

## Adding a document

1. Start from a skeleton in [`templates/`](templates/) — not from a previous
   document.
2. Put it in the folder that matches its content, per the map above.
3. Follow [`DOCUMENTATION_STANDARD.md`](DOCUMENTATION_STANDARD.md): YAML front
   matter, one `#` heading, lowercase `kebab-case` filename, ISO dates.
4. Check it before opening a pull request:

   ```bash
   python3 scripts/check-docs.py
   ```

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the review workflow.
