---
title: Meeting — pedagogical follow-up, BTP evidence and experiment tooling
status: final
owner: Noé Kurata
created: 2026-04-12
updated: 2026-09-04
tags: [meeting, pedago]
---

# Meeting — pedagogical follow-up, BTP evidence and experiment tooling

**Date:** 2026-04-12
**Attendees:** Noé Kurata, Luca Martinet, Théo Pawalec

## Summary

Two priorities were set. For the BTP evaluation, the priority is being able to
*prove* the solution works — measurable, reproducible evidence — rather than
describe it. For the UI, the priority is something presentable on desktop, judged
on clarity and credibility. A supporting decision: build a small tool that sends
requests to GPT-Audio so hypotheses can be tested against a real model quickly.

## Agenda

- Next follow-up: BTP evaluation.
- Next green lights (validation checkpoints).
- An audio experimentation tool built on GPT-Audio.
- Approach: formulate several hypotheses, then test them with that tool.
- Deliverable targets: BTP (proof), UI (presentable on desktop).

## Discussion

**BTP evaluation**

- Clarify the validation criteria and prepare the supporting evidence.

**Green lights**

- *Blanc (UI):* validate a simple, neutral visual direction.
- A second green light, covering the steps after the UI checkpoint, was left to
  be defined.

**Experimentation tool**

- Build a tool that sends requests to GPT-Audio —
  <https://developers.openai.com/api/docs/models/gpt-audio>
- Goal: speed up the hypothesis → test → result loop on audio files.
- Write several hypotheses, then test them through the tool.

## Decisions

- **BTP:** the priority is proving the solution works, with measurable and
  reproducible evidence — Noé
- **UI:** present something credible on desktop; clarity over completeness — Luca

## Action items

- [ ] Define the BTP validation criteria and how each will be demonstrated — examples, metrics, test cases — Noé
- [ ] Specify v1 of the testing tool: inputs, outputs, workflow, where results are stored — Théo
- [ ] Write 3–5 concrete hypotheses plus a minimal test protocol — Luca
- [ ] Stabilise a presentable desktop UI: structure, copy, main flow — Luca
- [ ] Define the second green light — *unresolved at the time of the meeting*

## Original notes (French)

> Agenda:
> - Prochain follow-up : évaluation BTP
> - Prochains « green lights » (jalons de validation)
> - Outil d'expérimentation audio basé sur GPT-Audio
> - Approche : formuler plusieurs hypothèses puis les tester avec un outil
> - Objectifs de livrables : BTP (preuve), UI (présentable desktop)
>
> Notes:
> - Prochain follow-up / évaluation BTP : clarifier les critères de validation et préparer les éléments de preuve.
> - Prochains « green lights » :
>   - Blanc (UI) : valider une direction visuelle simple / neutre.
>   - (autre green light à préciser) : valider la suite des étapes après le jalon UI.
> - Créer un outil qui envoie des requêtes vers GPT-Audio :
>   - Référence : https://developers.openai.com/api/docs/models/gpt-audio
>   - Objectif : accélérer l'exploration (hypothèses → tests → résultats) sur des fichiers audio.
> - Développer plusieurs hypothèses puis les tester via l'outil (approche expérimentale).
>
> Décisions / Alignement:
> - BTP : la priorité est de pouvoir prouver que la solution fonctionne (preuves mesurables, reproductibles).
> - UI : présenter quelque chose de présentable sur desktop (priorité à la clarté et la crédibilité).

## Related

- [`2026-05-28-presentation-feedback.md`](2026-05-28-presentation-feedback.md) — the presentation these deliverables fed into
