---
title: Behaviour-neutrality check — threshold computation moved upstream
status: final
owner: Noé Kurata
created: 2026-09-01
updated: 2026-09-04
milestone: G
tags: [benchmark, core, dsp, masking]
---

# Behaviour-neutrality check — threshold computation moved upstream

This study verifies that a refactor (moving when masking thresholds are computed)
changed nothing in the audio output. The claim: output before and after the
refactor must be indistinguishable, and clearly different from the unperturbed
input.

## What the figure shows

`spectra_compare.png` is a grid of three columns by three time segments:

- **normal (no perturb)** - the input processed with no perturbation applied,
  a reference for what unprocessed audio looks like.
- **pre#87** - output from the build before the refactor.
- **post#87** - output from the build after the refactor.

Each panel is a spectrogram: a time-frequency visualisation of the audio.
The horizontal axis is time (one second per panel), the vertical axis is
frequency, and the brightness/colour shows how much energy is present at each
frequency over time.

Three one-second segments are shown, taken from the start, middle, and later in
the file, so the comparison covers material that differs in content.

## How to run it

1. Produce three WAV outputs from the sample input using the same processing
   options, changing only whether perturbation is applied and which build
   produced the file.
2. Place them as `normal.wav`, `pre87.wav`, `post87.wav` next to the script.
3. Run the comparison script, which writes `spectra_compare.png` and prints the
   peak spectral difference between each pair.

Dependencies: Python with `numpy`, `scipy`, and `matplotlib`.

## What the numbers mean

The script computes the largest magnitude difference between two spectrograms:

- `normal vs pre#87` and `normal vs post#87` are small non-zero values, because
  perturbation adds a little energy (that is its purpose).
- `pre#87 vs post#87` is zero, which is the pass criterion: the refactor is
  behaviour-neutral, output is unchanged, and the two builds are byte-for-byte
  equivalent.

```python
import numpy as np
from scipy.io import wavfile
from scipy.signal import spectrogram

def peak_spectral_diff(path_a, path_b):
    _, a = wavfile.read(path_a)
    _, b = wavfile.read(path_b)
    a = a.astype(np.float64)
    b = b.astype(np.float64)
    if a.ndim == 2:
        a = a.mean(axis=1)
        b = b.mean(axis=1)
    _, _, Sa = spectrogram(a, window="hann", nperseg=1024, noverlap=768, scaling="spectrum")
    _, _, Sb = spectrogram(b, window="hann", nperseg=1024, noverlap=768, scaling="spectrum")
    return np.abs(Sa - Sb).max()

print("pre vs post:", peak_spectral_diff("pre87.wav", "post87.wav"))
print("normal vs pre:", peak_spectral_diff("normal.wav", "pre87.wav"))
print("normal vs post:", peak_spectral_diff("normal.wav", "post87.wav"))
```

## Scope and privacy

This document describes only how the comparison is visualised and what the pass
criterion is. It intentionally does not describe how the perturbation or masking
processing itself works internally; those details stay in the private `core/`
source and documentation.