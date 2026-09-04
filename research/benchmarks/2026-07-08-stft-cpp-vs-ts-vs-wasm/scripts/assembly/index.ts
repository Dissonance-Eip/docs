// Dissonance STFT benchmark - WASM build (AssemblyScript, -O3)
// Identical algorithm to stft.cpp and stft.ts.
const SR: i32 = 44100;
const SECONDS: i32 = 300;
const CHANNELS: i32 = 2;
const N: i32 = SR * SECONDS;
const FRAME: i32 = 2048;
const HOP: i32 = 512;

let signal: Float32Array = new Float32Array(0);
let win: Float64Array = new Float64Array(FRAME);
let re: Float64Array = new Float64Array(FRAME);
let im: Float64Array = new Float64Array(FRAME);

// unchecked() removes AS bounds checks, matching C++ raw-array semantics
function fft(re: Float64Array, im: Float64Array, n: i32, inverse: bool): void {
  for (let i: i32 = 1, j: i32 = 0; i < n; i++) {
    let bit: i32 = n >> 1;
    for (; j & bit; bit >>= 1) j ^= bit;
    j ^= bit;
    if (i < j) {
      const tr = unchecked(re[i]); unchecked(re[i] = re[j]); unchecked(re[j] = tr);
      const ti = unchecked(im[i]); unchecked(im[i] = im[j]); unchecked(im[j] = ti);
    }
  }
  for (let len: i32 = 2; len <= n; len <<= 1) {
    const ang: f64 = (2.0 * Math.PI / len) * (inverse ? 1.0 : -1.0);
    const wr: f64 = Math.cos(ang), wi: f64 = Math.sin(ang);
    for (let i: i32 = 0; i < n; i += len) {
      let cr: f64 = 1.0, ci: f64 = 0.0;
      for (let j: i32 = 0; j < len / 2; j++) {
        const a: i32 = i + j, b: i32 = i + j + len / 2;
        const vr: f64 = unchecked(re[b]) * cr - unchecked(im[b]) * ci;
        const vi: f64 = unchecked(re[b]) * ci + unchecked(im[b]) * cr;
        unchecked(re[b] = re[a] - vr); unchecked(im[b] = im[a] - vi);
        unchecked(re[a] = re[a] + vr); unchecked(im[a] = im[a] + vi);
        const ncr: f64 = cr * wr - ci * wi;
        ci = cr * wi + ci * wr; cr = ncr;
      }
    }
  }
  if (inverse) {
    const inv: f64 = 1.0 / n;
    for (let i: i32 = 0; i < n; i++) {
      unchecked(re[i] = re[i] * inv); unchecked(im[i] = im[i] * inv);
    }
  }
}

export function setup(): void {
  signal = new Float32Array(N * CHANNELS);
  let x: u32 = 1234567;
  for (let i: i32 = 0; i < N * CHANNELS; i++) {
    x = x * 1664525 + 1013904223;
    signal[i] = <f32>((<f64>(x >> 8) / 16777216.0) * 2.0 - 1.0);
  }
  for (let i: i32 = 0; i < FRAME; i++)
    win[i] = 0.5 * (1.0 - Math.cos(2.0 * Math.PI * i / (FRAME - 1)));
}

export function frames(): i32 {
  return (N - FRAME) / HOP + 1;
}

export function process(): f64 {
  const nFrames: i32 = frames();
  let checksum: f64 = 0.0;
  for (let ch: i32 = 0; ch < CHANNELS; ch++) {
    const base: i32 = ch * N;
    for (let f: i32 = 0; f < nFrames; f++) {
      const off: i32 = base + f * HOP;
      for (let i: i32 = 0; i < FRAME; i++) {
        unchecked(re[i] = <f64>unchecked(signal[off + i]) * unchecked(win[i]));
        unchecked(im[i] = 0.0);
      }
      fft(re, im, FRAME, false);
      fft(re, im, FRAME, true);
      checksum += unchecked(re[0]) + unchecked(re[FRAME / 2]);
    }
  }
  return checksum;
}
