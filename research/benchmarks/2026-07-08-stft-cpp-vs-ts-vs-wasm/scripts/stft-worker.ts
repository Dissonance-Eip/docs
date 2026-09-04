// Dissonance STFT benchmark - pure TypeScript worker (worker_threads)
// Identical algorithm to stft.cpp and assembly/index.ts.
import { parentPort } from 'node:worker_threads';

const SR = 44100, SECONDS = 300, CHANNELS = 2;
const N = SR * SECONDS;
const FRAME = 2048, HOP = 512;

function fft(re: Float64Array, im: Float64Array, n: number, inverse: boolean): void {
  for (let i = 1, j = 0; i < n; i++) {
    let bit = n >> 1;
    for (; j & bit; bit >>= 1) j ^= bit;
    j ^= bit;
    if (i < j) {
      const tr = re[i]; re[i] = re[j]; re[j] = tr;
      const ti = im[i]; im[i] = im[j]; im[j] = ti;
    }
  }
  for (let len = 2; len <= n; len <<= 1) {
    const ang = (2 * Math.PI / len) * (inverse ? 1 : -1);
    const wr = Math.cos(ang), wi = Math.sin(ang);
    for (let i = 0; i < n; i += len) {
      let cr = 1.0, ci = 0.0;
      for (let j = 0; j < len / 2; j++) {
        const a = i + j, b = i + j + len / 2;
        const vr = re[b] * cr - im[b] * ci;
        const vi = re[b] * ci + im[b] * cr;
        re[b] = re[a] - vr; im[b] = im[a] - vi;
        re[a] += vr;        im[a] += vi;
        const ncr = cr * wr - ci * wi;
        ci = cr * wi + ci * wr; cr = ncr;
      }
    }
  }
  if (inverse) {
    const inv = 1.0 / n;
    for (let i = 0; i < n; i++) { re[i] *= inv; im[i] *= inv; }
  }
}

// deterministic pseudo-random "audio" (same LCG as the other impls)
const signal = new Float32Array(N * CHANNELS);
let x = 1234567 >>> 0;
for (let i = 0; i < signal.length; i++) {
  x = (Math.imul(x, 1664525) + 1013904223) >>> 0;
  signal[i] = ((x >>> 8) / 16777216) * 2 - 1;
}
const win = new Float64Array(FRAME);
for (let i = 0; i < FRAME; i++)
  win[i] = 0.5 * (1 - Math.cos(2 * Math.PI * i / (FRAME - 1)));

const re = new Float64Array(FRAME), im = new Float64Array(FRAME);
const frames = Math.floor((N - FRAME) / HOP) + 1;
const ITER = 5;
const results: { ms: number; checksum: number }[] = [];

for (let it = 0; it < ITER; it++) {
  let checksum = 0.0;
  const t0 = process.hrtime.bigint();
  for (let ch = 0; ch < CHANNELS; ch++) {
    const base = ch * N;
    for (let f = 0; f < frames; f++) {
      const off = base + f * HOP;
      for (let i = 0; i < FRAME; i++) { re[i] = signal[off + i] * win[i]; im[i] = 0.0; }
      fft(re, im, FRAME, false);
      fft(re, im, FRAME, true);
      checksum += re[0] + re[FRAME / 2];
    }
  }
  const t1 = process.hrtime.bigint();
  results.push({ ms: Number(t1 - t0) / 1e6, checksum });
}

parentPort!.postMessage({ frames, results });
