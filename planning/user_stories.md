# User stories & workflows (from personas)

This document captures core user stories and end-to-end workflows derived from the Dissonance personas.

**References**
- Personas: `../research/personas/` (see also `../research/personas/2026-02-18-Dissonance_User_Needs_Personas.md`)
- Planning: `milestones.md` and `roadmap.md`

## Personas (source docs)

- Music Label Executive: ../research/personas/musiclabelexecutive.md
- Independent Musician: ../research/personas/independantmusician.md
- Audio Engineer / Studio Producer: ../research/personas/audioengineer.md
- Music Enthusiast / AI User: ../research/personas/music_enthusiast_ai_user.md
- Academic Researcher (AI & Audio): ../research/personas/academicresearcher.md

## Persona summary → primary goals

| Persona | Primary goals (with Dissonance) |
|---|---|
| Music Label Executive | Protect large catalogs from AI exploitation at scale, manage rights with minimal friction, and signal strong IP protection to artists and partners. |
| Independent Musician | Safeguard individual tracks from unauthorized AI remixes/piracy while keeping the creative output authentic and under personal control. |
| Audio Engineer / Studio Producer | Integrate imperceptible protection into professional workflows without sacrificing sound quality or slowing production. |
| Music Enthusiast / AI User | Use platforms that respect ethical AI + music practices, understand how audio is treated, and preserve authenticity. |
| Academic Researcher (AI & Audio) | Run transparent, controllable adversarial experiments on audio, with clear documentation and ethical framing. |

## User stories by persona

### Music Label Executive

- As a music label executive, I want to upload batches of catalog tracks and apply AI-resistant protection profiles so that our entire library becomes safer without manual per-track work.
- As a music label executive, I want visibility into which catalogs have been processed and are AI-safe so that I can report risk reduction to artists and internal stakeholders.
- As a music label executive, I want configurable policies (e.g., which artists or releases to prioritize) so that I can balance protection efforts with business priorities.
- As a music label executive, I want non-technical dashboards and clear documentation so that legal, A&R, and marketing teams can understand what Dissonance is doing to our audio.

### Independent Musician

- As an independent musician, I want to drag-and-drop my WAV/FLAC file into Dissonance and get back a protected version so that I can publish music without fear of AI exploitation.
- As an independent musician, I want assurance that the protection is inaudible to my listeners so that my artistic intent is preserved.
- As an independent musician, I want to see a simple explanation of how Dissonance safeguards my work so that I can communicate this to my audience and collaborators.
- As an independent musician, I want presets (e.g., “platform upload”, “promo snippet”) so that I can quickly choose appropriate protection levels without understanding every technical detail.

### Audio Engineer / Studio Producer

- As an audio engineer, I want Dissonance to run as a non-destructive step in my production or mastering pipeline so that I can add protection without rebuilding my workflow.
- As an audio engineer, I want the protection to be imperceptible and verifiable (ABX or similar) so that I can sign off on quality with confidence.
- As an audio engineer, I want automation-friendly interfaces (CLI, API, or plugin-style integration) so that I can batch-process stems or finals overnight.
- As an audio engineer, I want clear technical documentation about the perturbation limits and LUFS safety rails so that I can ensure no unexpected loudness or artifacts.

### Music Enthusiast / AI User

- As a music enthusiast who uses AI tools, I want clear information on whether a track is protected and how so that I can choose platforms that respect artists.
- As a music enthusiast, I want educational content inside or alongside Dissonance (or its partner platforms) so that I better understand ethical AI + music practices.
- As a music enthusiast, I want ways to verify that my personal collections are not secretly harvested for AI training so that my trust in platforms is preserved.

### Academic Researcher (AI & Audio)

- As an academic researcher, I want a transparent, well-documented perturbation pipeline so that I can reproduce and extend adversarial audio experiments.
- As an academic researcher, I want configurable parameters and access to raw STFT/ISTFT stages so that I can run controlled ablations in my studies.
- As an academic researcher, I want clear ethical guidance and usage examples so that my work using Dissonance aligns with AI safety best practices.
- As an academic researcher, I want a way to export experiment logs and metrics so that I can include them directly in papers and benchmarks.

## Core workflows

### 1) Independent musician: Protect and publish a new track (Milestone D)

1. Open the Dissonance desktop app and land on the “Protect a track” flow (see Milestone D in `milestones.md` / `roadmap.md`).
2. Drag an unprotected WAV/FLAC into the app; Dissonance reads metadata and shows a waveform preview.
3. Choose a simple preset (e.g., “Streaming release”) with default LUFS safety rails and perceptual masking settings.
4. Run processing; the app shows progress and a quick ABX-style before/after preview to verify audibility.
5. Export the protected file and an optional “proof” report (hash + settings summary).

**Outcome:** The musician has a protected, listener-transparent version ready for upload, plus documentation they can share if needed.

### 2) Audio engineer: Integrate Dissonance into studio workflow (Milestones F–G)

1. Finish mix/master in the DAW and export a final WAV (or stems) to a designated Dissonance folder.
2. Use a CLI/automation hook or UI batch mode to process all exports using a studio profile.
3. Run automated checks: reconstruction tests, LUFS verification, and optional ABX scripts to validate perceptual transparency.
4. Deliver both protected finals and a short technical note describing the protection used.

**Outcome:** Protection becomes a standard, low-friction post-processing step without compromising sound quality.

### 3) Music label executive: Catalog-level rollout (Milestones F–G + reporting)

1. Import catalog metadata (artists, albums, priority flags) and connect a storage location or export job from the label’s system.
2. Define label-wide policies: processing priority, default strengths, and reporting cadence.
3. Schedule batch jobs that process catalog segments with Dissonance’s perturbation engine.
4. Review dashboards summarizing coverage (percentage protected, recent jobs, risk indicators).
5. Export reports for internal IP committees and external partners.

**Outcome:** The label gains scalable protection over large catalogs with evidence of proactive AI risk mitigation.

### 4) Academic researcher: Run a controlled adversarial study (Milestones F–G)

1. Set up Dissonance in a research environment (core library + documentation).
2. Load a curated audio corpus and configure STFT/ISTFT parameters, masking thresholds, and perturbation types via config files.
3. Run experiments against a baseline transcription or classification harness, logging accuracy changes and audio quality metrics.
4. Export experiment metadata, configs, and results for papers and benchmarks.

**Outcome:** Researchers get a reproducible, ethically framed toolkit for adversarial audio experiments instead of ad-hoc scripts.

### 5) Music enthusiast / AI user: Understand and verify protection

1. Encounter a Dissonance-protected track on a partner platform (or via a lightweight verifier tool).
2. Open a verification UI or documentation page explaining what Dissonance is and what it claims.
3. Optionally verify a local audio file (e.g., purchased download) to confirm it carries Dissonance protection.

**Outcome:** Enthusiasts develop trust in platforms that deploy Dissonance and better understand ethical AI practices around music.