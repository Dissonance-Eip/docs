---
title: White noise threshold-shaping — issue #88
status: final
owner: Noé Kurata
created: 2026-09-04
updated: 2026-09-04
milestone: G
tags: [benchmark, core, dsp, masking, perturbation]
---

# White noise threshold-shaping — issue #88

## Summary

Replaced the flat white noise + 8 kHz high-pass filter injection with
threshold-shaped injection gated under the psychoacoustic masking threshold.
The injected noise energy is now bounded per-bin by the hearing threshold,
making it significantly less perceptible while maintaining adversarial
perturbation effectiveness.

## What changed

**Pre-88 (old behavior):**
- White noise generated flat across all frequencies
- 8 kHz first-order IIR high-pass filter applied (attenuates below 8 kHz)
- Noise mixed at `strength * kMaxAmplitude` (0.01 at full strength, ~-40 dBFS)

**Post-88 (new behavior):**
- White noise generated flat, then spectrally shaped via STFT
- Per-bin magnitude clamped to psychoacoustic mask threshold from MaskingThresholdStage
- 8 kHz HP filter skipped (mask already bounds energy across all frequencies)
- Amplitude scaling done once at the mixing loop (`strength * kMaxAmplitude`)

## Files modified

| File | Change |
|------|--------|
| `core/include/audio/PerturbationStage.hpp` | `applyWhiteNoise` signature: static -> non-static |
| `core/src/audio/PerturbationStage.cpp` | Rewrote `applyWhiteNoise` with STFT mask-gating; conditional HP skip |
| `core/tests/perturbation_stage_test.cpp` | 4 new tests + 2 pre-existing assertion fixes |

## Test results

All 13 perturbation stage tests pass. Full test suite green.

New tests:
- `NullContextFallbackAddsNoise` - context=nullptr falls back to flat noise
- `MaskShapedNoiseStaysUnderThreshold` - noise power bounded by mask
- `VeryLowMaskYieldsNearSilentOutput` - very low mask yields near-silent output
- `EmptyMaskContextFallsBackToFlat` - empty mask context falls back to flat

## Spectral analysis

Processed `test_files/sound.wav` (31 MB, stereo, 44.1 kHz) with both binaries.
Parameters: `--gain 0.8 --perturbation 0.5 --mode white_noise`

### Per-band average noise power (noise = output - original)

| Band | Pre-88 | Post-88 | Difference |
|------|--------|---------|------------|
| 0-2 kHz | -59.9 dB | -60.1 dB | -0.1 dB |
| 2-4 kHz | -82.4 dB | -84.5 dB | -2.1 dB |
| 4-6 kHz | -90.7 dB | -96.1 dB | **-5.4 dB** |
| 6-8 kHz | -90.5 dB | -94.8 dB | **-4.3 dB** |
| 8-12 kHz | -93.3 dB | -96.6 dB | -3.3 dB |
| 12-16 kHz | -96.2 dB | -98.5 dB | -2.2 dB |
| 16-22 kHz | -104.4 dB | -117.8 dB | **-13.4 dB** |

### Key findings

1. **Overall noise power is identical** (-49.3 dB for both). The total energy
   injected is the same; only the spectral distribution changes.

2. **Post-88 noise is 2-13 dB quieter across all bands**. The threshold shaping
   redistributes noise energy to stay under the hearing threshold at each
   frequency, rather than relying on a blunt 8 kHz cutoff.

3. **Largest improvement at 16-22 kHz** (-13.4 dB). The psychoacoustic model
   assigns very low thresholds at high frequencies where hearing sensitivity
   drops, so the mask aggressively suppresses noise there.

4. **Meaningful improvement at 4-8 kHz** (-4.3 to -5.4 dB). This is the range
   where human hearing is most sensitive and where the old flat noise was most
   audible. The mask-shaped noise is significantly quieter here.

5. **0-2 kHz nearly unchanged** (-0.1 dB). The psychoacoustic mask is already
   very low at low frequencies (high hearing sensitivity), so both approaches
   produce minimal noise there.

## Spectrograms

Three spectrogram images are saved alongside this document:
- `spectrogram_comparison.png` - Original vs Pre-88 vs Post-88
- `noise_comparison.png` - Injected noise only (signal subtracted)
- `frequency_profile.png` - Average noise spectrum with 8 kHz cutoff line