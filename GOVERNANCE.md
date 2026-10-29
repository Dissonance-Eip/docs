# Governance of Dissonance

This page says who decides what across the Dissonance repositories
([ui](https://github.com/Dissonance-Eip/ui),
[core](https://github.com/Dissonance-Eip/core) and
[docs](https://github.com/Dissonance-Eip/docs)), how a disagreement is settled,
what triggers a release, how versions are numbered, and where the project goes
after the EIP. Contribution steps are in [`CONTRIBUTING.md`](CONTRIBUTING.md).

Facts below were checked on 2026-10-29 against the workflow files and GitHub
settings. Where a rule is not enforced by tooling, it says so.

## Maintainers

The project is run by two maintainers: Noé Kurata and Luca Martinet.

TODO(team): state who owns which repository for review purposes, if split.

## Who validates a pull request

A pull request is merged when:

1. CI passes: `ui/.github/workflows/ui-quality-checks.yml` (lint, format check,
   tests, build) and `core/.github/workflows/ci.yml` (cppcheck, clang-format
   check, CMake build and tests).
2. At least one maintainer other than the author has reviewed and approved it.
3. It is merged with a merge commit into `dev` (`main` in docs).

What is enforced by GitHub today:

- `ui`: a ruleset on `main` requires a pull request with one approving review,
  dismisses stale approvals on new pushes, and blocks deletion and force pushes.
  It does not list required status checks. `dev` is not covered by it.
- `docs`: no ruleset is configured.
- `core`: not readable with the credentials used for this check.

So the CI requirement and the review requirement on `dev` rest on team practice
and on `CONTRIBUTING.md`, not on a GitHub rule. TODO(team): enable required
status checks and required review on `dev` in `ui` and `core`, and on `main` in
`docs`, and record the result here.

`main` in `ui` and `core` only receives releases.

## How a disagreement is settled

1. Discuss it in the pull request or issue first.
2. If it is still blocked, write it up as an ADR (see
   [`templates/adr.md`](templates/adr.md)) with the options and their costs.
3. The mentor or the chargé d'étude decides, and the ADR records the decision.

TODO(team): name the person who takes the decision when neither the mentor nor
the chargé d'étude is available.

## What triggers a release

| Repository | Trigger | What runs | Result |
| --- | --- | --- | --- |
| `core` | Pushing a tag matching `v[0-9]*` | `core/.github/workflows/release-addon.yml`: checks, then builds the addon on Windows (x64), Linux (x64) and macOS (arm64) | A GitHub release with the `*.node` files, and a dispatch that makes `ui` sync the binaries |
| `ui` | Pushing a tag matching `v[0-9]*` | `ui/.github/workflows/release-app.yml`: builds installers on each platform | A GitHub release with `.dmg`, `.zip`, `.exe` and `.AppImage` |

Notes:

- The `core` workflow also runs its checks on every push to `dev`, and a manual
  run (`workflow_dispatch`) publishes a `dev-<run id>` release.
- `ui` copies the addon binaries from the latest `core` release into
  `ui/Build/Release/` with `ui/.github/workflows/sync-core-addon.yml`, so the
  order is: tag `core`, wait for the sync, then tag `ui`.
- A manual run of `release-app.yml` builds installers but does not publish.
- `docs` has no release process.

## Versioning

Versions follow [Semantic Versioning 2.0.0](https://semver.org): `MAJOR.MINOR.PATCH`.
Tags are `vMAJOR.MINOR.PATCH`.

State on 2026-10-29: `ui` is at `v0.1.1`, `core` has tags up to `v0.0.5`
while `core/package.json` says `0.0.2`. TODO(team): align the `core` package
version with its tags. While the major number is 0, anything may change in a
minor release, as SemVer allows. TODO(team): decide when to declare `1.0.0`.

### Addon API

The public API of the engine is the addon contract in
[`core/README.md`](https://github.com/Dissonance-Eip/core/blob/dev/README.md):
`process`, `readMetadata` and `writeTags`, their arguments, their returned
objects and their failure behaviour. The rules below apply SemVer to that
contract and are proposed, pending the team's confirmation.

| Bump | What counts |
| --- | --- |
| Major | Removing or renaming a function. Removing or renaming an option, or changing what a value means. Removing a field from a returned object or changing its type. Making an optional argument required. Changing how failures are reported. |
| Minor | Adding a function, an optional option, or a new field in a returned object. |
| Patch | A fix that leaves the contract unchanged. |

TODO(team): decide whether a change in protection behaviour (for example a new
default strength) is a minor or a patch, since the contract itself does not
change.

### The app

| Bump | What counts |
| --- | --- |
| Major | A change that breaks a user's existing workflow or files, removal of a supported platform, or a required `core` major version change. |
| Minor | A new user-visible feature, or a new supported platform. |
| Patch | A bug fix, a text or layout fix, a dependency update with no visible change. |

An app release states which addon version it bundles. An addon major version
needs an app release that adapts to it, so the two repositories change together
in that case.

## Roadmap after the EIP

The planned work is in [`planning/roadmap.md`](planning/roadmap.md) and is
tracked in [`planning/milestones.md`](planning/milestones.md): adversarial
perturbation v1 and v2, then optimisation, packaging and final documentation,
with the last milestone ending 2027-04-30.

The architecture direction after that is to move the engine behind a
server-side API, with no date decided
([ADR 004](design/core/2026-10-29-adr-004-deployment-architecture.md)).

TODO(team): everything else about the period after the EIP (who maintains the
project, what is built, how it is funded or hosted) is not decided and is not
written here.

## How contributors are recruited

- Small, self-contained issues carry the
  [`good first issue`](https://github.com/Dissonance-Eip/ui/issues?q=label%3A%22good+first+issue%22)
  label. Newcomers start there.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) explains the workflow, and each
  repository README has a welcome and install section.
- The first outside contribution has landed: `ui` pull request #101 by an
  external contributor (merged 2026-10-09), which resolved the `good first
  issue` ui#94. It was reviewed by a maintainer under the rule above.
- The engine is closed (see
  [ADR 003](design/core/2026-10-29-adr-003-open-scope.md)), so outside
  contributions go to `ui` and `docs`.

TODO(team): where else to announce the project (channels, schools, communities).

## Related

- [`CONTRIBUTING.md`](CONTRIBUTING.md)
- [`planning/roadmap.md`](planning/roadmap.md)
- [`design/core/2026-10-29-adr-003-open-scope.md`](design/core/2026-10-29-adr-003-open-scope.md)
- [`design/core/2026-10-29-adr-004-deployment-architecture.md`](design/core/2026-10-29-adr-004-deployment-architecture.md)
- Issue [docs#63](https://github.com/Dissonance-Eip/docs/issues/63)
