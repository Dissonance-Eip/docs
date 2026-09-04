/**
 * wav_parse_bench.mjs — times the JavaScript parser in wav_parser.mjs on the
 * same corpus as wav_parse_bench.cpp and prints one JSON object to stdout.
 *
 * Two operations are timed per file, matching the addon's two entry points:
 *   header — incremental fd reads, never touches the data chunk (readMetadata)
 *   decode — whole file into a Buffer, full sample conversion  (process)
 *
 * Usage: node wav_parse_bench.mjs <reps> <file> [file...]
 */

import { parseHeader, parseFull } from "./wav_parser.mjs";

function summarise(runs) {
  const sorted = [...runs].sort((a, b) => a - b);
  return {
    min: sorted[0],
    median: sorted[sorted.length >> 1],
    mean: sorted.reduce((a, b) => a + b, 0) / sorted.length,
  };
}

function time(fn, path, reps) {
  const runs = [];
  let last;
  for (let i = 0; i < reps; i++) {
    const t0 = process.hrtime.bigint();
    last = fn(path);
    const t1 = process.hrtime.bigint();
    runs.push(Number(t1 - t0) / 1e6);
  }
  return { stats: summarise(runs), last };
}

const [repsArg, ...files] = process.argv.slice(2);
const reps = Number(repsArg);
if (!reps || files.length === 0) {
  console.error("usage: node wav_parse_bench.mjs <reps> <file> [file...]");
  process.exit(2);
}

const out = { runner: "node", nodeVersion: process.version, reps, files: [] };
for (const path of files) {
  parseFull(path); // warm the page cache and let V8 tier up
  const header = time(parseHeader, path, reps);
  const decode = time(parseFull, path, reps);
  out.files.push({
    file: path,
    samples: decode.last.audioData.length,
    header: header.stats,
    decode: decode.stats,
  });
}
out.peakRssKb = Math.round(process.memoryUsage().rss / 1024);
console.log(JSON.stringify(out, null, 2));
