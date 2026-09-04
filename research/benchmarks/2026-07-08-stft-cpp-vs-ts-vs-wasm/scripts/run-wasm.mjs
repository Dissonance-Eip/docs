// Harness for the AssemblyScript/WASM build
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const dir = dirname(fileURLToPath(import.meta.url));
const wasm = readFileSync(join(dir, 'build', 'stft.wasm'));
const { instance } = await WebAssembly.instantiate(wasm, {
  env: { abort() { throw new Error('wasm abort'); } },
});
const { setup, process: proc, frames } = instance.exports;

setup();
console.log(`impl=wasm frames_per_channel=${frames()} channels=2 fft=2048 hop=512`);
const ITER = 5;
for (let it = 0; it < ITER; it++) {
  const t0 = process.hrtime.bigint();
  const checksum = proc();
  const t1 = process.hrtime.bigint();
  console.log(`iter=${it} ms=${(Number(t1 - t0) / 1e6).toFixed(1)} checksum=${checksum.toFixed(6)}`);
}
