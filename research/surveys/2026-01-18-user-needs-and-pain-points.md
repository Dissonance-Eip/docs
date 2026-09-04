---
title: User needs and pain points
status: final
owner: Noé Kurata
created: 2026-01-18
updated: 2026-09-04
milestone: A
tags: [research, survey, personas, user-needs]
---

# User needs and pain points

## Summary

The needs and pain points Dissonance is built to address, combining the November
2025 survey with all five personas. This supersedes the two earlier partial
analyses — survey-only and personas-only — which were removed on 2026-09-04.

**Sources**

- [`2025-11-25-Dissonance_GF_Survey_Results.csv`](2025-11-25-Dissonance_GF_Survey_Results.csv) — raw survey export
- [`../personas/music-label-executive.md`](../personas/music-label-executive.md)
- [`../personas/music-enthusiast-ai-user.md`](../personas/music-enthusiast-ai-user.md)
- [`../personas/independent-musician.md`](../personas/independent-musician.md)
- [`../personas/audio-engineer.md`](../personas/audio-engineer.md)
- [`../personas/academic-researcher.md`](../personas/academic-researcher.md)

## Protection and control

- Assert consent over AI training — stop/hinder unauthorized use
- Catalog-wide repeatable workflows — process all releases systematically
- Visible guarantees — users want to understand how it works and what it promises

## Audio quality and UX

- Imperceptible but strong perturbations — no audible damage to releases
- Simple defaults + expert depth — one-click presets for beginners, advanced settings for pros
- A/B and QA tooling — side-by-side listening, spectrograms, loudness matching

## Integration and reach

- Fit existing tools — DAW plugins, mastering chain, desktop app, web flows
- Format robustness — survives MP3, YouTube, Spotify, SoundCloud compression
- Scalable operations — batch jobs, CLI/CI hooks, reporting for labels and researchers

## Trust, ethics and future-proofing

- Ethical alignment and transparency — defend artists, communicate tradeoffs
- Honest about arms-race limits — clear communication about what each version can/can't do
- Ecosystem recognition — industry legitimacy, academic credibility, platform endorsement

## Key pain points, cross-cutting

| Pain Point | Description |
|------------|-------------|
| Outpaced and outgunned | AI capabilities accelerate faster than legal/technical protections  *(survey)*, *(audio engineer)* |
| No credible defenses today | Existing options are too technical, opaque, or not music-focused  *(survey)*, *(independent musician)* |
| Platform retaliation fear | Worry that platforms might shadowban anti-AI content  *(survey)*, *(label executive)* |
| Arms race uncertainty | AI will adapt — protection feels temporary  *(survey)*, *(academic researcher)* |
| Invisible exploitation | No visibility into where/how work is being scraped  *(survey)*, *(independent musician)* |

## Quick reference — top user needs by persona

| Persona | #1 Need | #2 Need |
|---------|---------|---------|
| Audio Engineer | DAW-integrated, transparent processing | Technical metering and QA tools |
| Indie Musician | One-click simplicity | Clear non-technical explanations |
| Label Executive | Catalog-scale batch processing | Audit logs for legal/policy |
| Enthusiast/Ethical User | Transparency and explainability | Community and education features |
| Academic Researcher | Configurable pipelines with logs | Clear licensing for publication |

## Related

- [`../personas/`](../personas/) — the five personas this draws on
- [`../../planning/user-stories.md`](../../planning/user-stories.md) — user stories derived from these needs
- [`../../planning/milestones.md`](../../planning/milestones.md) — Milestone A
