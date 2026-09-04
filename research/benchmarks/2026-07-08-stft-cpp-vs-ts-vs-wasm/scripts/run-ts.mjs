// Harness for the pure TypeScript worker implementation
import { Worker } from 'node:worker_threads';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const dir = dirname(fileURLToPath(import.meta.url));
const worker = new Worker(join(dir, 'stft-worker.ts'));
worker.on('message', ({ frames, results }) => {
  console.log(`impl=ts-worker frames_per_channel=${frames} channels=2 fft=2048 hop=512`);
  results.forEach((r, i) =>
    console.log(`iter=${i} ms=${r.ms.toFixed(1)} checksum=${r.checksum.toFixed(6)}`));
});
worker.on('error', (e) => { console.error(e); process.exit(1); });
