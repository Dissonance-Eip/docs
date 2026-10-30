---
title: Outside reproducibility test
status: draft
owner: Luca Martinet
created: 2026-10-29
updated: 2026-10-29
milestone: K
tags: [planning, testing, onboarding, open-source]
---

# Outside reproducibility test

## Summary

This test has not been run. It checks that a person outside the team can go from
a clean machine to a processed audio file by following only the READMEs. This
document holds the protocol and an empty results record for the team to fill in.

## Protocol

1. Pick a person who has never worked on Dissonance and who is not a team
   member. Record who they are only by role (for example "student, JavaScript
   developer").
2. Use a clean machine or a fresh user account with no Dissonance tooling. Note
   the operating system and version, and the CPU architecture.
3. Give them the link to the repository READMEs and nothing else. Do not
   answer questions, except to note them.
4. Ask them to go from clone to a processed file by following the READMEs. Two
   routes are in scope: installing a release of the app, and running the app
   from source with `npm install` and `npm run dev` in `ui`.
5. Start a timer at the first README. Stop it when a processed `.wav` file
   exists and opens.
6. Record every moment they are blocked, what blocked them and the fix. A
   blocker is anything that stops them for more than a minute or makes them
   leave the README.
7. Fix the READMEs for each blocker and list the changes.

The engine is closed, so building `core` is out of scope for an outside person.

## Results record

| Field | Value |
| --- | --- |
| Who (role only) | TODO(team) |
| Machine (OS, version, architecture) | TODO(team) |
| Date | TODO(team) |
| Route tested | TODO(team) |
| Total time, clone to processed file | TODO(team) |
| Outcome (file produced: yes or no) | TODO(team) |

### Blockers

| Step | What blocked them | Fix made | Pull request |
| --- | --- | --- | --- |
| TODO(team) | TODO(team) | TODO(team) | TODO(team) |

### README changes made

TODO(team): list each README change, with the repository and the pull request.

## Related

- [`CONTRIBUTING.md`](../CONTRIBUTING.md)
- [`onboarding.md`](onboarding.md)
- [`GOVERNANCE.md`](../GOVERNANCE.md)
- Issue [docs#62](https://github.com/Dissonance-Eip/docs/issues/62)
