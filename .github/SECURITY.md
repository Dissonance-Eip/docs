# Security policy

This policy covers every repository in the Dissonance-Eip organization: the
desktop app ([ui](https://github.com/Dissonance-Eip/ui)), the audio engine
([core](https://github.com/Dissonance-Eip/core)) and the documentation
([docs](https://github.com/Dissonance-Eip/docs)).

## Supported versions

Only the latest release gets security fixes.

| Component | Supported |
| --- | --- |
| Dissonance app | The [latest release](https://github.com/Dissonance-Eip/ui/releases/latest) |
| Audio engine | The version bundled with the latest app release |
| Older releases | No. Update to the latest release |

## Reporting a vulnerability

Please do not open a public issue, pull request or discussion for a security
problem.

Report it privately through GitHub instead, on the repository where the problem
is:

- App: [report a vulnerability in ui](https://github.com/Dissonance-Eip/ui/security/advisories/new)
- Audio engine: [report a vulnerability in core](https://github.com/Dissonance-Eip/core/security/advisories/new)
- Documentation: [report a vulnerability in docs](https://github.com/Dissonance-Eip/docs/security/advisories/new)

If you are not sure which one, use ui. Only the maintainers can see the report.

Please include:

- The component and version affected (app release, or commit)
- Your operating system
- Steps to reproduce, and a sample file if the problem comes from opening one
- What an attacker could do with it

## What to expect

Dissonance is maintained by a two-person student team, so these are targets,
not guarantees:

- We acknowledge your report within 7 days.
- We tell you whether we accept it, and our plan, within 14 days.
- Once it is fixed, we publish a GitHub security advisory and credit you,
  unless you prefer to stay anonymous.

Please give us 90 days to ship a fix before disclosing the problem publicly.

## Scope

In scope:

- The desktop app: the Electron main process, the preload bridge and the
  renderer
- The audio engine, especially reading untrusted audio files (malformed WAV
  headers or chunks)
- Our release builds and CI workflows

Out of scope:

- How well the audio protection works against a given AI model. That is a
  research question, not a vulnerability. Please open a normal issue in
  [core](https://github.com/Dissonance-Eip/core/issues).
- Vulnerabilities in third-party dependencies that do not affect Dissonance.
  Report those to the project concerned.
