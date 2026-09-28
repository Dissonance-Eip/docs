---
title: "Meeting - mentor follow-up on open source and quality objectives"
status: final
owner: Noé Kurata
created: 2026-09-15
updated: 2026-09-15
tags: [meeting, mentor]
---

# Meeting - mentor follow-up on open source and quality objectives

**Date:** 2026-09-15, 15:00-15:37 (Google Meet)
**Attendees:** Noé Kurata, Luca Martinet

## Summary

Two mandatory objectives were reviewed ahead of the end-of-October 2026
deliverable deadline. Both are currently on track: objective 1 (open source
release and governance) has a public repository with research documentation and
a release version; objective 2 (test strategy and quality measurement) has
operational CI and automated tests. Four prerequisite decisions remain open and
must be settled by end of September 2026 before the deliverables are written.

## Discussion

**Progress review since last session**

- Slides shared in advance.
- General state: a green light was obtained at the June defence (score
  43/60).
- Jury feedback: the presentation was appreciated; the audio perturbation
  benchmark was judged unconvincing because the comparison bar was set too
  high; team roles were insufficiently explicit; the presentation lacked
  music/AI market statistics. The project continues.
- Licence reflections are ongoing: a public repository with a closed-source
  core (the perturbation engine).
- CI via GitHub Actions has been in place since the start of the project:
  tests on every push/PR, merge blocked on failure, lint, mandatory review
  before merging to main.

**Mandatory objective 1 - open source release and governance**

- Produced since the last session: a public repository with research
  documentation (language and technique comparisons, justification of the
  adversarial choices). A release version exists.
- Feedback given - strengths: research documentation already published;
  main-branch protection and cross-review are already active.
- Feedback given - improvement axes:
  - Formally justify in writing the openness scope (open front / closed
    engine).
  - Choose a licence (MIT or Apache 2 recommended for the open part) with
    written justification.
  - Inventory of dependencies and their licences (watch for contaminating
    licences such as GPL; the C++ dependency in BSD-3 is compatible).
  - A welcome and install README plus a CONTRIBUTING.md.
  - A reproducibility test by an external person: time, blockers, corrections
    made.
  - 5 open issues including 3 accessible to a newcomer.
  - Written governance (who validates, how a disagreement is settled, what
    triggers a release, post-EIP roadmap).
  - A SemVer presentation for the versioning strategy.
- Questioning: keeping the engine closed is consistent with keeping the
  project alive after the EIP but must be validated quickly with the study
  supervisor. A documented API with a mini SDK would be a plus (nice to have,
  not priority). Recruiting contributors is needed.

**Mandatory objective 2 - test strategy and quality measurement**

- Currently: GitHub Actions CI operational, automated tests, lint/formatting,
  review with comments on every PR, coverage measured on the C++ side (value
  unknown in session). Several regressions already caught by the tests.
- Feedback given - strengths: CI hygiene and code review already at the
  expected level; identified logs (managed / unmanaged) to improve.
- Feedback given - improvement axes:
  - Write a test strategy (which test type for which part, where the tests
    live, naming, when they are written).
  - Aim for high coverage on the engine, less critical on the front-end.
  - At least one integration test.
  - Document 3 regressions caught by the tests.
  - Validation of external inputs and front-end behaviour when the
    engine/backend is unavailable.
  - An initial static analysis report.
- Questioning: the "end of October" CI deadline is already satisfied; the
  effort must go to the written strategy and quality measurements.

**Blockers**

- None strictly speaking, the students are autonomous.
- Licence types were explained during the session; SemVer was presented.
- A VM made available by Epitech is needed. Out of mentorship scope,
  reported for information.

## Decisions

- None taken in session. The four pending decisions were deferred to the
  team.

## Action items

- [ ] Formalise the openness scope (open front / closed engine) and have it
  validated by the study supervisor - Noé - due 2026-09-30
- [ ] Choose and add the licence to the repository, with written justification
  - Noé - due 2026-09-30
- [ ] Extract the dependency list (front-end stack, C++) with their licences
  and check compatibility - Luca - due 2026-09-30
- [ ] Settle the architecture decision (hosted API / encrypted local /
  server-side engine) - Noé and Luca - due 2026-09-30

## Follow-up (end-of-October deliverables)

**Objective 1**

- [ ] Welcome + install README, CONTRIBUTING.md - due 2026-10-30
- [ ] Reproducibility test by an external person: time, blockers, corrections
  made - due 2026-10-30
- [ ] Open 5 GitHub issues including 3 "good first issue" - due 2026-10-30
- [ ] Write governance: validation, disagreements, SemVer versioning, post-EIP
  roadmap - due 2026-10-30

**Objective 2**

- [ ] Written test strategy + team convention - due 2026-10-30
- [ ] Coverage measurement + initial static analysis report - due 2026-10-30
- [ ] Document 3 regressions caught by the tests and at least one integration
  test - due 2026-10-30

**Next meeting:** 2026-10-16, 14:00

## Original notes (French)

> Séance du mardi 15 septembre 2026, 15h00-15h37 (visio Google Meet).
> Présents : Noé Kurata, Luca Martinet (équipe complète, 2 membres).
> Absents : aucun.
>
> Revue de l'avancement depuis le dernier RDV
>
> Slides transmises. État général : green light obtenu à la soutenance de
> juin (43/60). Retours du jury : présentation appréciée, mais benchmark
> des perturbations audio jugé peu convaincant car la barre de comparaison
> était placée trop haut ; rôles dans l'équipe insuffisamment explicités ;
> manque de statistiques sur le marché musique/IA. Le projet continue.
> Réflexions en cours sur la licence : dépôt public, cœur (algorithme de
> perturbation) en close source. CI GitHub Actions en place depuis le début
> du projet (tests à chaque push/PR, merge bloqué en cas d'échec, lint,
> revue obligatoire avant merge sur main).
>
> Objectif obligatoire 1 (traité en séance)
>
> Produit depuis la dernière séance : dépôt public avec documentation de
> recherche (comparatif de langages et de techniques, justification des
> choix côté adversarial). Une version release existe. Feedback donné :
> Points forts : documentation de recherche déjà publiée ; règle de
> protection de main et revue croisée déjà actives. Axes d'amélioration :
> périmètre d'ouverture (front open / moteur close) à formaliser et
> justifier par écrit ; licence à choisir (MIT ou Apache 2 recommandées pour
> la partie ouverte) avec justification ; inventaire des dépendances et de
> leurs licences (attention aux licences contaminantes type GPL ; la
> dépendance C++ en BSD-3 est compatible) ; README d'accueil et
> d'installation, CONTRIBUTING.md à produire ; test de reproductibilité par
> une personne extérieure (temps, blocages, corrections) ; 5 tickets ouverts
> dont 3 accessibles à un nouveau venu ; gouvernance écrite (qui valide,
> comment un désaccord se tranche, ce qui déclenche une version, feuille de
> route post-EIP) ; Présentation de Semver pour la stratégie de
> versionning. Questionnement : garder le moteur fermé est cohérent avec la
> volonté de faire vivre le projet après l'EIP, mais doit être validé
> rapidement avec le chargé d'étude. Une API documentée avec mini SDK serait
> un plus (nice to have, pas prioritaire). Recrutement de contributeurs
> nécessaires.
>
> Objectif obligatoire 2 (traité en séance)
>
> Actuellement : CI GitHub Actions opérationnelle, tests automatisés,
> lint/formatage, revue avec commentaires sur chaque PR, coverage mesuré
> côté C++ (valeur non connue en séance). Plusieurs régressions déjà
> attrapées par les tests. Feedback donné : Points forts : hygiène CI et
> revue de code déjà au niveau attendu ; logs identifiés (gérés / non gérés)
> à améliorer. Axes d'amélioration : rédiger la stratégie de tests (quel
> type de test pour quelle partie, où vivent les tests, nommage, quand on les
> écrit) ; viser une grosse couverture sur le moteur, moins critique sur le
> front ; au moins un test d'intégration ; documenter 3 régressions
> rattrapées par les tests ; validation des entrées externes et
> comportement du front si le moteur/back est indisponible ; rapport
> d'analyse statique initial. Questionnement : échéance CI fin octobre déjà
> satisfaite, l'effort doit aller sur la stratégie écrite et les mesures de
> qualité.
>
> Blocages : pas de blocage à proprement parlé, les étudiants sont
> autonomes. Explication des différents types de licence pendant la séance,
> présentation de SemVer. Besoin d'une VM mise à dispo par Epitech. Hors
> périmètre mentorat, signalé pour information.
>
> Actions pour la suite : discuté en séance, en cours de finalisation :
> 1. Formaliser le périmètre d'ouverture (front open / moteur close) et le
>    faire valider par le chargé d'étude.
> 2. Choisir et ajouter la licence au dépôt, avec justification écrite.
> 3. Extraire la liste des dépendances (React, C++) avec leurs licences et
>    vérifier la compatibilité.
> 4. Trancher l'architecture (API hébergée / local chiffré / moteur serveur).
>
> Objectif 1 (livrable fin octobre) :
> 5. README d'accueil + installation, CONTRIBUTING.md.
> 6. Test de reproductibilité par une personne extérieure : temps,
>    blocages, corrections apportées.
> 7. Ouvrir 5 tickets GitHub dont 3 good first issue.
> 8. Rédiger la gouvernance : validation, désaccords, versionning Semver,
>    feuille de route post-EIP.
>
> Objectif 2 (livrable fin octobre) :
> 9. Stratégie de tests écrite + convention d'équipe.
> 10. Mesure de couverture rapport d'analyse statique initial.
> 11. Documenter 3 régressions rattrapées par les tests et au moins un
>     test d'intégration.
>
> Date du prochain RDV : 16 octobre - 14h

## Related

- [Objectives - open source release and quality - H2 2026](../planning/objectives-2026-h2.md)
- [Milestones](../planning/milestones.md)
- [Roadmap](../planning/roadmap.md)
