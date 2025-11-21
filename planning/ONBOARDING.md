Dissonance — New teammate onboarding

Purpose

This central onboarding guide helps new teammates get productive quickly. It lists access requirements, the minimum local setup to run the UI and Core prototypes, where to find key documentation and templates, development conventions, and a first-week checklist.

Quick start (5-minute view)

1. Get access
   - Request GitHub org + repo access from the project lead.
   - Ask for any required CI/hosting credentials (if needed) from the project lead.
2. Clone the repos you need:

```bash
# clone the three main repos (replace origin with your fork if you plan to contribute)
git clone git@github.com:your-org/dissonance-core.git
git clone git@github.com:your-org/dissonance-ui.git
git clone git@github.com:your-org/dissonance-docs.git
```

3. Run a smoke build (UI + Core): see the "Local dev" section below.
4. Read `docs/planning/milestones.md` and `docs/planning/roadmap.md` to understand priorities.
5. Pick an onboarding task from `docs/planning/milestones.md` or ask the project lead.

Repo map and purpose
- `dissonance-core` — C++ DSP prototype, WAV parser, algorithms, tests.
- `dissonance-ui` — Electron + React UI, assets, packaging configs.
- `dissonance-docs` — research, benchmarks, personas, templates, roadmap.

Required accounts & access
- GitHub account with org access (ask a lead for invite)
- For macOS packaging: Apple Developer account (if involved in packaging)
- For Windows packaging: appropriate code-signing certs (if required)
- CI/CD: ensure your GitHub user has the required repo permissions for PRs and actions (read on the first PR)

Local development environment (recommended baseline)
- macOS or Linux; development is supported on both.
- Install developer tools:
  - Git (2.34+ recommended)
  - Node.js (18.x or 20.x — check `ui/package.json`) and npm or pnpm
  - CMake (3.20+ recommended), clang/gcc toolchain
  - Python 3.10+ (optional — used for benchmark scripts)
  - Docker (optional — recommended for reproducible benchmarks)

UI: quick dev setup

1) Enter the UI repo and install dependencies:

```bash
cd dissonance-ui
# using npm
npm install
# or using pnpm if you prefer
# pnpm install
```

2) Run the dev electron app (if project has a script):

```bash
# local development (dev server + electron)
npm run dev
# or if the script is `start`:
# npm start
```

3) Build production (packaging stub):

```bash
npm run build
# then package with electron-builder if configured
# npm run package
```

Core: quick dev setup (C++)

1) Create a build directory and configure with CMake:

```bash
cd dissonance-core
mkdir -p build && cd build
cmake ..
# on macOS you might specify generator or toolchain
# cmake -G "Unix Makefiles" ..
```

2) Build and run unit tests (googletest):

```bash
cmake --build . --config Debug -- -j
# run tests (ctest or the test binary)
ctest --output-on-failure
# or run the test executable directly from build/tests/ or similar
```

Running the docs locally
- `dissonance-docs` is primarily Markdown. If a docs site is scaffolded (MkDocs or Docusaurus), follow the repo README to serve the site locally.

Contribution workflow (PRs, issues)
- Fork-and-branch or work directly on feature branches in the main org depending on permissions.
- Branch naming convention: `feature/<short-description>`, `fix/<short-description>`, `docs/<short-description>`.
- Create a concise PR title and a descriptive body: explain the why, list the key files changed, and link related issues.
- Use the PR template in `.github/PULL_REQUEST_TEMPLATE.md`.
- Assign a reviewer (UI lead for UI changes, Core lead for DSP/Core changes, Docs lead for documentation changes).
- Include tests or update docs where relevant.

Code style and linters
- UI: ESLint + Prettier configured — run linters before committing:

```bash
cd dissonance-ui
npm run lint
npm run format
```

- Core: follow existing C++ style (clang-format may be present). If `clang-format` is used, run it before committing.
- Add tests for new behavior and aim to follow current test structure.

Testing & benchmarks
- Unit tests: run `ctest` (core) and `npm test` (ui) where available.
- Benchmarks: look in `docs/research/benchmarks/` for harness scripts and study folders. When running benchmarks, use the Docker image if provided to ensure reproducibility.

Documentation and templates
- Use templates in `docs/templates/` for meeting notes, study writeups, and ABX protocol.
- Add new docs under the appropriate folder (research, planning, surveys, personas).
- Keep `docs/README.md` and `docs/planning/milestones.md` up to date when you complete work.

Security and secrets
- Do not commit secrets or API keys. Use GitHub Secrets for CI or local environment variables for development.
- If you need signing keys or secrets, request them from the project lead and follow the secure transfer process.

Branching, releases, and tagging
- Main branches: `main` (stable), `develop` (ongoing work) — if you prefer a different model, align with the team.
- Tag releases using semantic versioning when packaging (v0.1.0, v0.2.0...).

First-week checklist (recommended tasks)
- [ ] Receive and confirm GitHub access
- [ ] Clone the three repos
- [ ] Run `npm install` and `npm run dev` for the UI
- [ ] Run CMake configure & run core unit tests
- [ ] Read `docs/planning/milestones.md` and `docs/planning/roadmap.md`
- [ ] Introduce yourself on the team channel and schedule a quick sync with your lead
- [ ] Pick a small starter task (docs edit, template population, small bug) and open your first PR

Starter tasks suitable for first PRs
- Add missing metadata to a comparative study
- Flesh out a persona entry in `docs/personas/`
- Fix a small lint issue in `dissonance-ui`
- Add a test or small README in `dissonance-core`

Onboarding checklist for leads (what to set up for new teammates)
- [ ] Grant GitHub org + repo access
- [ ] Provide build machine details and any necessary credentials
- [ ] Assign a buddy or mentor for initial week
- [ ] Add the new teammate to the communications channels
- [ ] Create a first-week task in the milestone board and assign


