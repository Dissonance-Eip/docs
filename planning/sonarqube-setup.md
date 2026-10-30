---
title: SonarQube Cloud setup
status: draft
owner: Luca Martinet
created: 2026-10-30
updated: 2026-10-30
milestone: L
tags: [planning, testing, quality, static-analysis, coverage]
---

# SonarQube Cloud setup

## Summary

`core` and `ui` are analysed by SonarQube Cloud on the Free plan, at no cost.
The scans run inside the existing CI jobs and reuse their coverage reports. They
stay skipped until the `SONAR_TOKEN` secret is added to each repository. The
quality gate is the built-in Sonar way, which is **proposed — to agree as a
team**. Tracked in [docs#78](https://github.com/Dissonance-Eip/docs/issues/78).

## Hosting decision

| Option | Cost | C/C++ analysis | Decision |
| --- | --- | --- | --- |
| SonarQube Cloud, Free plan | €0 | Yes | **Chosen** |
| SonarQube Cloud, Team plan | Paid | Yes | Not needed at our size |
| Self-hosted SonarQube Community Build | €0 plus a server to run | No, the official C/C++ analyser needs a paid edition | Rejected |

The issue assumed SonarQube Cloud is paid for private repositories. That is out of
date: the Free plan analyses private projects up to 50k lines of code per
organisation.

- `ui` is public. Public projects have no line limit.
- `core` is private. It has about 7.5k lines of code without the vendored
  kissfft, which is excluded from analysis. That leaves about 42k lines of headroom
  under the 50k limit.

Free plan limits that shape the setup:

| Limit | Effect on us |
| --- | --- |
| Only the main branch is analysed | Each project's main branch must be `dev`, where the team merges, not `main` |
| Pull requests are analysed only if they target the main branch | PRs into `dev` are analysed. Other PRs are not |
| No custom quality gates | We use the built-in Sonar way gate. See below |
| At most 5 organisation members | Enough for the team. Readers of public `ui` results need no account |

## How the analysis runs

| | `core` | `ui` |
| --- | --- | --- |
| Configuration | `sonar-project.properties` | `sonar-project.properties` |
| Organisation | `dissonance-eip` | `dissonance-eip` |
| Project key | `Dissonance-Eip_core` | `Dissonance-Eip_ui` |
| CI job | `coverage` in `ci.yml` | `quality-checks` in `ui-quality-checks.yml` |
| Language | C/C++, from the coverage build's `compile_commands.json` | JavaScript, HTML |
| Coverage | gcovr, SonarQube generic XML (`COVERAGE_SONARQUBE`) | Vitest V8, `coverage/lcov.info` |
| Runs on | Pull requests, and manual runs on `dev` (`workflow_dispatch`) | Pull requests, and pushes to `dev` |
| Excluded | `vendor/`, FetchContent `_deps/`, build directories | `dist/`, `node_modules/`, `coverage/`, `Build/`, `tailwind.css`, `*.min.js` |

The scan action is `SonarSource/sonarqube-scan-action`, pinned by commit to
v8.3.0. Both workflows skip the scan when `SONAR_TOKEN` is missing, on
`merge_group` runs, and on fork pull requests, which receive no secrets.

Known gap in `core`: `src/cli/main.cpp` and `src/addon/addon.cpp` are not part
of the coverage build, so they are not in its compilation database and Sonar runs
no C/C++ rules on them.

## CI minutes

`core` is private, so its GitHub Actions minutes count against the
organisation's quota. `ui` is public and its minutes are free.

| Change in `core` | Cost per pull request run |
| --- | --- |
| No new job and no second build. The scan reuses the instrumented coverage build | 0 |
| `gcovr` installed with apt, report written | A few seconds. The coverage job took 99 s on the first run, against 86 to 100 s before |
| Scan step, once the token exists | Estimated 1 to 2 minutes: scanner download and C++ analysis of about 45 files |
| Full clone (`fetch-depth: 0`), once the token exists | Estimated 10 to 20 s. The repository's history is about 130 MiB |

Measure the real figures on the first scanned pull request and update this
table. The `dev` analysis in `core` only runs when someone starts it by hand, so
it costs nothing until then.

## Setup steps

The `dissonance-eip` organisation already exists on SonarQube Cloud. `core`, `ui`
and `docs` have been imported with Automatic Analysis on, and it already comments
on pull requests. Automatic Analysis cannot read our coverage reports, so we switch
`core` and `ui` to CI-based analysis. Organisation and project admins do the
following steps.

1. Check the project keys are `Dissonance-Eip_core` and `Dissonance-Eip_ui`. If a
   key differs, update `sonar-project.properties` in that repository.
2. Leave `docs` on Automatic Analysis or remove it. It holds no code to analyse.
   It is public, so it does not count towards the 50k line limit.
3. In `core` and `ui`, go to **Administration > Analysis Method** and turn off
   **Automatic Analysis**. CI-based analysis fails while it is on.
4. In `core` and `ui`, go to **Administration > Branches and Pull Requests** and
   rename the main branch from `main` to `dev`.
5. Create a token under **My Account > Security**. It is personal, so use the
   account of a team member who will stay on the project.
6. In GitHub, add it as a repository secret named `SONAR_TOKEN` in both `core`
   and `ui`, under **Settings > Secrets and variables > Actions**. Never commit it.
7. Record the first `dev` analysis:
   - `ui`: merge any pull request into `dev`.
   - `core`: run **Core Quality Checks** from the Actions tab on `dev`.
8. Link the first report from the static analysis report
   ([docs#64](https://github.com/Dissonance-Eip/docs/issues/64)).

## Quality gate

**Proposed — to agree as a team.** The Free plan cannot create custom gates, so
the proposal is the built-in Sonar way. On new code, it requires:

| Condition | Threshold |
| --- | --- |
| New bugs | None (reliability rating A) |
| New vulnerabilities | None (security rating A) |
| Technical debt | Maintainability rating A |
| New security hotspots | All reviewed |
| Coverage on new code | At least 80% |
| Duplication on new code | At most 3% |

Coverage and duplication are only checked once a change has at least 20 new lines.

The 80% applies to new code only, and still applies to pull requests. It does
not replace the overall target in [`test-strategy.md`](test-strategy.md): 85%
line coverage for both `core` and `ui`, raised from 70% and 50% on 2026-10-30
([docs#80](https://github.com/Dissonance-Eip/docs/issues/80)). The Free plan
cannot hold a custom gate with that 85%, so it is enforced in CI, not in Sonar.

### Why SonarQube shows lower coverage

On `dev` on 2026-10-30, SonarQube Cloud shows 66.7% coverage for `core` and
67.6% for `ui`. The repositories' own commands give about 92% (`core`, `npm run
coverage`) and about 71% (`ui`, `npm run test:coverage`).

The numbers differ because they count different lines. In `core`, the coverage
report sent to Sonar only lists `src/` files, so Sonar counts every line of
header-only code in `include/` as uncovered, even when tests run it (for
example `include/utils/SampleCodec.hpp` shows 0%). `src/cli/main.cpp` and
`src/addon/addon.cpp` get no coverage figure in Sonar and do not lower it.
core#151 adds `include/` to both the Sonar report and the 85% check so the two
numbers agree. Until then, the repositories' own commands are the reference for
the 85% target. Sonar's numbers are for trends and for the new-code condition
above.

The gate is shown on each pull request. It is not a required status check yet.
Making it blocking is part of the team decision.

TODO(team): agree the gate and decide whether it blocks merging.

## Related

- [`static-analysis-report.md`](static-analysis-report.md), which should link the first report (docs#64)
- [`coverage-report.md`](coverage-report.md) (docs#61)
- [`test-strategy.md`](test-strategy.md)
- Issue [docs#80](https://github.com/Dissonance-Eip/docs/issues/80), which raised the coverage target to 85%
- core: `sonar-project.properties`, `.github/workflows/ci.yml`, `scripts/coverage.js`
- ui: `sonar-project.properties`, `.github/workflows/ui-quality-checks.yml`, `vitest.config.mjs`
