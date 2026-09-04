/**
 * wav_parity_check.mjs — prints the same fingerprint as wav_parity_check.cpp
 * for the JavaScript parser, so the two implementations can be proven
 * equivalent before any timing is trusted.
 *
 * Usage: node wav_parity_check.mjs <file>
 */

import { parseFull } from "./wav_parser.mjs";

const path = process.argv[2];
if (!path) {
  console.error("usage: node wav_parity_check.mjs <file>");
  process.exit(2);
}

const p = parseFull(path);

// FNV-1a over the raw float bits, byte-for-byte identical to the C++ version.
const view = new DataView(p.audioData.buffer, p.audioData.byteOffset, p.audioData.byteLength);
let hash = 14695981039346656037n;
const MASK = (1n << 64n) - 1n;
const PRIME = 1099511628211n;
for (let i = 0; i < p.audioData.length; i++) {
  const bits = view.getUint32(i * 4, true);
  for (let b = 0; b < 4; b++) {
    hash = ((hash ^ BigInt((bits >>> (b * 8)) & 0xff)) * PRIME) & MASK;
  }
}

console.log(
  JSON.stringify({
    audioFormat: p.audioFormat,
    numChannels: p.numChannels,
    sampleRate: p.sampleRate,
    byteRate: p.byteRate,
    blockAlign: p.blockAlign,
    bitsPerSample: p.bitsPerSample,
    dataSize: p.subchunk2Size,
    samples: p.audioData.length,
    otherChunks: p.otherChunks.size,
    hash: hash.toString(16).padStart(16, "0"),
  }),
);
