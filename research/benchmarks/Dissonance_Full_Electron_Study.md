# Dissonance Project
Full Comparative Study  
(Electron + TypeScript Architecture)

![img.png](img.png)

**Authors:** Luca Martinet, Noé Kurata  
**Date:** 2025

---

Dissonance Project — Full Academic Comparative Study (Electron + TypeScript Architecture)

This document provides a comprehensive academic comparative study analyzing the transition from a JUCE/C++ architecture to an Electron + TypeScript architecture for the Dissonance project. The goal is to deliver an in-depth technical justification for the final architectural decision, taking into account performance factors, scalability, UI/UX requirements, maintainability, developer workflow, cross-platform deployment, and long-term evolution over Dissonance’s two-year roadmap.

This study is intended to serve as an comparative reference and includes:
- Architectural analysis
- Performance considerations
- Detailed UI/UX comparison
- Maintainability and scalability analysis
- Code examples in JUCE and Electron
- Design system methodology
- IPC analysis
- Benchmark graphs and comparison tables
- A formal ADR-style conclusion


## 1. JUCE/C++ Architecture Analysis

JUCE is a mature C++ framework widely used in the audio software industry, primarily for plugin development (VST/AU) and native applications with real-time DSP constraints. Its architecture is optimized for deterministic, ultra-low-latency processing and provides direct access to audio drivers, buffers, and native system APIs.

However, JUCE exhibits several structural limitations for projects requiring highly flexible, 
dynamic, customizable, and visually rich user interfaces. These limitations stem from the 
imperative nature of its UI model, limited component ecosystem, and the high engineering overhead associated with UI changes.

Example: JUCE Imperative UI

```cpp
void MainComponent::resized() {
    auto area = getLocalBounds().reduced(10);
    auto header = area.removeFromTop(50);

    gainSlider.setBounds(header.removeFromLeft(200));
    muteButton.setBounds(header.removeFromLeft(150));

    statusLabel.setBounds(area.removeFromTop(30));
    waveformDisplay.setBounds(area);
}
```


## 2. Electron + TypeScript Architecture Analysis

Electron provides a hybrid application architecture combining:
- Chromium (UI rendering engine)
- Node.js (backend runtime)
- A secure IPC layer between them

This architecture allows the us to build a desktop application using modern Web technologies - React, TypeScript, CSS, Tailwind, Radix, shadcn/ui - while retaining the ability to execute high-performance DSP code through WebAssembly or native Node modules compiled from C++.

Example: Electron React UI

```tsx
export function ControlPanel() {
  return (
    <div className="p-4 space-y-4">
      <GainSlider density="normal" />
      <MuteButton />
    </div>
  );
}
```


## 3. UI Customization Requirements

Dissonance requires a deeply customizable UI, enabling users to adjust:
- Button sizes
- Slider density
- Layout scaling
- Themes and color palettes
- Typography sizes
- Spacing and padding

Electron + React is uniquely suited for this because styling is declarative and dynamic. JUCE 
cannot provide runtime theming without substantial C++ boilerplate and reimplementation of basic UI primitives.

Example: Customizable Slider

```tsx
export function GainSlider({ density = 'normal' }) {
  const sizes = { compact: 'h-1', normal: 'h-2', comfortable: 'h-3' };
  return <input type="range" className={sizes[density] + " w-full"} />;
}
```


## 4. Electron Architecture (Main / Renderer / Preload / Workers)

Electron uses a multi-process architecture that maps perfectly to the needs of the Dissonance project:
- Main Process -- window management, OS integration, file handles
- Preload Script -- secure bridging of Node APIs
- Renderer Process -- React UI, no Node access (sandboxed)
- Worker Threads -- heavy DSP operations
- WASM Modules -- compiled C++ DSP engine

This structure isolates heavy computation away from the UI thread while still delivering rich visual interaction through React.

Secure IPC Example

```js
contextBridge.exposeInMainWorld('engine', {
    processFile: (filePath) => ipcRenderer.invoke('process-file', filePath),
    runSTFT: (buffer) => ipcRenderer.invoke('run-stft', buffer)
});
```


## 5. Design System Architecture

A formal design system is necessary to support UI customizability. In Electron+React, this system is built using TypeScript design tokens, CSS variables, and reusable components.

Pipeline:
Design Tokens → Primitive Components → Compound Views → Screens

This pipeline cannot be replicated efficiently in JUCE due to its lack of styling abstractions.

```ts
export const tokens = {
  spacing: { sm: 4, md: 8, lg: 16 },
  radius: { sm: 2, md: 6, lg: 10 },
  controlSize: {
    compact: "h-7 text-xs",
    normal: "h-9 text-sm",
    comfortable: "h-11 text-base"
  }
};
```


## 6. Comparison Tables


## 7. Benchmark Discussion

Tests on 5-minute stereo audio files show that:
- JUCE/C++ is fastest, as expected.
- WASM STFT implementation is ~12% slower.
- Pure TypeScript worker implementation is ~1.8× slower but still acceptable.

Given that Dissonance runs file-based processing, not real-time streaming, this performance figures are well within acceptable bounds.


## 8. Final ADR Decision Summary

Decision: Use Electron + TypeScript as the UI framework and integrate DSP code via WebAssembly or native Node modules compiled from C++.

Rationale:
Electron allows rapid development of a deeply customizable user interface, essential for 
Dissonance’s UX goals. While C++ provides faster DSP, this performance difference does not 
impact Dissonance’s offline processing model. The web ecosystem, Electron packaging, and 
React-based design system together provide a more sustainable long-term architecture.

Consequences:
- Slightly lower raw DSP performance (offset by WASM speed)
- Major gains in UI flexibility, maintainability, and developer productivity
- Stable cross-platform distribution for Windows/macOS/Linux


> **Side note on WASM:**
>
> Although WebAssembly (WASM) offers demonstrably higher computational performance for numerical and signal-processing workloads, its integration imposes a level of architectural and operational complexity that is disproportionate to the current needs and development capacity of the project. Implementing WASM typically requires parallel maintenance of a secondary language environment (e.g., C++ or Rust), dedicated compilation pipelines, memory-management considerations, and additional bindings to interface with JavaScript and Electron. These requirements significantly increase the cognitive and technical overhead for our current small team, especially in an early-stage research context where rapid iteration, clarity of implementation, and maintainability are prioritised. Furthermore, contemporary JavaScript and TypeScript runtimes, provide sufficient performance for the scale and latency constraints of the project’s initial DSP and adversarial processing tasks. Therefore, while WASM remains a potential avenue for future optimisation, the current phase of the project is better served by a unified, TypeScript-only architecture that maximises development efficiency, cross-platform simplicity, and accessibility for future contributors.
