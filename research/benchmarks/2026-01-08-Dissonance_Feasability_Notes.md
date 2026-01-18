# Dissonance Project
External Video Study  
(Benn Jordan – "The Art Of Poison-Pilling Music Files")

**Author:** Noé Kurata  
**Date:** 2026-01-08

---

## 1. Video Overview

**Title:** The Art Of Poison-Pilling Music Files  
**Creator:** Benn Jordan  
**Publication date:** 2025-04-13  
**Length:** 27:10  
**Platform:** YouTube (https://www.youtube.com/watch?v=xMYm2d9bmEA)

### 1.1. Narrative Summary

In the video, Jordan presents a tool and workflow for "poison-pilling" music files so that they remain perceptually unchanged for human listeners but become harmful or unusable for certain AI systems:

- Demonstrates a tool ("Poisonify") that injects AI-breaking noise into music files.  
- References academic work such as HarmonyCloak (University of Tennessee) to justify the approach to melody scrambling and adversarial audio.  
- Tests poisoned audio against real-world systems (Amazon Echo, Meta AI, Suno/MusicGen) at several timestamps (~5:20, 8:00, 9:15).  
- Uses spectrograms to illustrate how AI models "see" music and how the perturbations alter that representation (~7:36).

### 1.2. Key Mathematical Segments

Relevant timestamps where mathematical or signal-processing concepts are highlighted include:

- Spectrogram basics and how models view audio as time–frequency images (~7:36–7:48).  
- Noise injection and the concept of adversarial perturbations (~7:51–8:33).  
- Training failure graphs showing divergence between clean and poisoned data (~6:58–7:15).


## 2. Mathematical Backbone

### 2.1. Discrete-Time Audio and Spectrograms (STFT)

The starting point is a discrete-time audio signal $x[n]$ sampled at rate $f_s$ (e.g. 44.1 kHz), with time $t = n / f_s$. To analyse how energy is distributed over time and frequency, Jordan uses a spectrogram, which corresponds to the short-time Fourier transform (STFT):

1. The signal is divided into overlapping frames of length $M$ and multiplied by a window $w[m]$ (e.g. Hann window).  
2. For each frame index $s$ and frequency bin $k$, the STFT is

     $$X(s, k) = \sum_{m=0}^{M-1} x[sR + m] \, w[m] \, e^{-j 2\pi k m / N},$$

     where $R$ is the hop size and $N$ is the DFT size.  
3. The spectrogram is the squared magnitude $|X(s, k)|^2$, displayed as an image.

At around ~7:36, Jordan explicitly uses this representation to show how different musical elements (drums, vocals, etc.) appear as distinctive patterns in the time–frequency plane. This is conceptually the same as the STFT-based visualisation planned in Dissonance.

### 2.2. Adversarial Noise in the Spectral Domain

The core adversarial idea is to add a carefully chosen perturbation $\delta$ to the original signal so that:

- The **perturbed audio** remains close to the original for human listeners.  
- The **model’s internal representation** (spectrogram/image) changes enough to break recognition or training.

In the time–frequency domain this can be written as:

- Clean spectrogram: $x(s, k)$  
- Perturbed spectrogram: $x'(s, k) = x(s, k) + \delta(s, k)$

After adding $\delta(s, k)$, the signal is reconstructed by an inverse STFT (ISTFT) to obtain a time-domain waveform $x'[n]$.

Around ~7:51, Jordan explains that the perturbation is optimised against specific models (via an API), with many GPU iterations on relatively short clips (e.g. 15k iterations on an 18-second example). HarmonyCloak is mentioned as an algorithm that pushes perturbations close to the human hearing threshold (~6:13), linking the approach to formal psychoacoustic limits.

### 2.3. Energy and Loudness Matching

To produce fair listening comparisons (A/B tests), the clean and perturbed signals should have similar overall level. This is often approximated using energy or RMS level:

- For a frame of $N$ samples, the energy is  
    $$E = \sum_{n=0}^{N-1} |x[n]|^2.$$

- The root mean square (RMS) level is  
    $$\text{RMS} = \sqrt{\frac{1}{N} \sum_{n=0}^{N-1} x[n]^2}.$$

In practice, the video keeps the perceived loudness comparable when switching between versions (~6:50), which aligns with Dissonance’s use of LUFS-based normalisation for A/B listening.

### 2.4. Training Curves and Model Failure

To demonstrate that the perturbations are effective against learning systems, Jordan shows training curves (e.g. in TensorBoard) around ~6:58:

- For **clean data**, the loss decreases over epochs (red curve), indicating successful learning.  
- For **poisoned data**, the loss remains nearly flat (blue curve), indicating that the model fails to learn meaningful patterns.

While not derived as formal equations in the video, these plots are good empirical evidence that adversarial perturbations can significantly degrade training performance.


## 3. Feasibility Argument for Dissonance

The video provides several independent arguments that Dissonance’s planned architecture and research direction are realistic in practice.

### 3.1. Workflow Parallels

Jordan’s workflow closely matches the offline pipeline envisioned for Dissonance:

- **Jordan:** load audio → compute spectrogram → design/optimise perturbation → listen to A/B examples → export poisoned files.  
- **Dissonance:** load audio → compute STFT in C++ core → apply perturbation in time/frequency domain → listen and compare in Electron UI → export perturbed files.

This shows that a file-based, non-real-time workflow with advanced DSP and adversarial methods is entirely practical on standard hardware.

### 3.2. Shared Mathematical Toolkit

The mathematical tools in the video are exactly those planned for Dissonance:

- STFT/ISTFT for time–frequency analysis and reconstruction.  
- Spectrograms as a bridge between audio and image-based model representations.  
- Carefully constrained perturbations that remain near perceptual thresholds.  
- Level normalisation to ensure fair A/B listening tests.

This overlap strengthens the claim that Dissonance is based on established, well-understood DSP methods rather than speculative techniques.

### 3.3. Real-World Impact on AI Systems

The tests performed on commercial or widely used AI systems (e.g. Suno/MusicGen at ~9:51) demonstrate that:

- Perturbed audio can significantly degrade model outputs or recognition quality.  
- The effect is robust enough to matter in real-world scenarios, not only in toy examples.

For Dissonance, this serves as external validation that adversarial audio research is both technically feasible and practically relevant.

## 4. Limitations and Citation

### 4.1. Scope Limitations

The video, while highly relevant, does not demonstrate several aspects that remain specific to Dissonance:

- The exact perturbation families and constraints designed for our research questions (e.g. time-domain vs. frequency-domain hybrids).  
- Our planned end-to-end robustness evaluation pipeline for ML models.  
- Formal human perception studies; the video mostly relies on informal A/B listening.

These differences preserve the originality of Dissonance while still allowing the video to serve as a strong feasibility benchmark.

### 4.2. Suggested Citation

For use in reports or the thesis, the video can be cited as:

> Jordan, B. (2025, April 13). *The art of poison-pilling music files* [Video]. YouTube.  
> https://www.youtube.com/watch?v=xMYm2d9bmEA

