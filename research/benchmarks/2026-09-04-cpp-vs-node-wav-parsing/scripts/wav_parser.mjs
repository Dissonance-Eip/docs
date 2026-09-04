/**
 * wav_parser.mjs — pure-JavaScript port of core/src/utils/WavParser.cpp.
 *
 * Behavioural parity with the C++ `Parser`:
 *   - validates RIFF/WAVE
 *   - walks chunks, honours odd-size padding, keeps unknown chunks verbatim
 *   - requires `fmt ` before `data`, stops after `data`
 *   - supports PCM 8/16/24/32 and IEEE float 32/64
 *   - normalises every sample to [-1, 1] in a Float32Array
 *
 * Exports two entry points mirroring the addon's:
 *   parseHeader(path) — incremental fd reads, never touches the data chunk (readMetadata)
 *   parseFull(path)   — whole file into a Buffer, full sample conversion  (process)
 */

import fs from "node:fs";

export class WavFormatError extends Error {}

/** Header-only parse: reads just enough of the file to describe it. */
export function parseHeader(path) {
  const fd = fs.openSync(path, "r");
  try {
    const head = Buffer.allocUnsafe(12);
    if (fs.readSync(fd, head, 0, 12, 0) !== 12) {
      throw new WavFormatError("Failed to read string field");
    }
    if (head.toString("latin1", 0, 4) !== "RIFF" || head.toString("latin1", 8, 12) !== "WAVE") {
      throw new WavFormatError("Not a valid RIFF/WAVE file");
    }

    const meta = { otherChunks: new Map() };
    const hdr = Buffer.allocUnsafe(8);
    let offset = 12;
    let sawFmt = false;

    for (;;) {
      if (fs.readSync(fd, hdr, 0, 8, offset) !== 8) {
        throw new WavFormatError("Failed to read string field");
      }
      const chunkId = hdr.toString("latin1", 0, 4);
      const chunkSize = hdr.readUInt32LE(4);
      const body = offset + 8;
      const advance = chunkSize + (chunkSize % 2);

      if (chunkId === "fmt ") {
        const fmt = Buffer.allocUnsafe(16);
        fs.readSync(fd, fmt, 0, 16, body);
        meta.audioFormat = fmt.readUInt16LE(0);
        meta.numChannels = fmt.readUInt16LE(2);
        meta.sampleRate = fmt.readUInt32LE(4);
        meta.byteRate = fmt.readUInt32LE(8);
        meta.blockAlign = fmt.readUInt16LE(12);
        meta.bitsPerSample = fmt.readUInt16LE(14);
        sawFmt = true;
      } else if (chunkId === "data") {
        if (!sawFmt) throw new WavFormatError("WAV missing fmt chunk before data");
        meta.subchunk2Size = chunkSize;
        return meta; // stop here — the point of a header-only read
      } else {
        const chunk = Buffer.allocUnsafe(chunkSize);
        fs.readSync(fd, chunk, 0, chunkSize, body);
        meta.otherChunks.set(chunkId, chunk);
      }
      offset = body + advance;
    }
  } finally {
    fs.closeSync(fd);
  }
}

/** Full parse: header plus every sample decoded into a Float32Array. */
export function parseFull(path) {
  const buf = fs.readFileSync(path);
  if (buf.length < 12) throw new WavFormatError("Failed to read string field");
  if (buf.toString("latin1", 0, 4) !== "RIFF" || buf.toString("latin1", 8, 12) !== "WAVE") {
    throw new WavFormatError("Not a valid RIFF/WAVE file");
  }

  const meta = { otherChunks: new Map() };
  let offset = 12;
  let sawFmt = false;

  for (;;) {
    if (offset + 8 > buf.length) throw new WavFormatError("Failed to read string field");
    const chunkId = buf.toString("latin1", offset, offset + 4);
    const chunkSize = buf.readUInt32LE(offset + 4);
    const body = offset + 8;

    if (chunkId === "fmt ") {
      meta.audioFormat = buf.readUInt16LE(body);
      meta.numChannels = buf.readUInt16LE(body + 2);
      meta.sampleRate = buf.readUInt32LE(body + 4);
      meta.byteRate = buf.readUInt32LE(body + 8);
      meta.blockAlign = buf.readUInt16LE(body + 12);
      meta.bitsPerSample = buf.readUInt16LE(body + 14);
      sawFmt = true;
    } else if (chunkId === "data") {
      if (!sawFmt) throw new WavFormatError("WAV missing fmt chunk before data");
      meta.subchunk2Size = chunkSize;
      meta.audioData = decodeSamples(buf, body, chunkSize, meta);
      return meta;
    } else {
      meta.otherChunks.set(chunkId, buf.subarray(body, body + chunkSize));
    }
    offset = body + chunkSize + (chunkSize % 2);
  }
}

function decodeSamples(buf, start, byteLength, meta) {
  const bytesPerSample = meta.bitsPerSample >>> 3;
  if (bytesPerSample === 0) throw new WavFormatError("Invalid bitsPerSample in WAV header");
  if (byteLength % bytesPerSample !== 0) throw new WavFormatError("Corrupt WAV data chunk size");

  const count = byteLength / bytesPerSample;
  const out = new Float32Array(count);

  if (meta.audioFormat === 1) {
    switch (meta.bitsPerSample) {
      case 8:
        for (let i = 0; i < count; i++) out[i] = (buf[start + i] - 128) / 128;
        return out;
      case 16:
        for (let i = 0, o = start; i < count; i++, o += 2) out[i] = buf.readInt16LE(o) / 32768;
        return out;
      case 24:
        for (let i = 0, o = start; i < count; i++, o += 3) {
          let v = buf[o] | (buf[o + 1] << 8) | (buf[o + 2] << 16);
          if (v & 0x800000) v |= ~0x00ffffff;
          out[i] = v / 8388608;
        }
        return out;
      case 32:
        for (let i = 0, o = start; i < count; i++, o += 4) out[i] = buf.readInt32LE(o) / 2147483648;
        return out;
      default:
        throw new WavFormatError(`Unsupported PCM bitsPerSample: ${meta.bitsPerSample}`);
    }
  }

  if (meta.audioFormat === 3) {
    if (meta.bitsPerSample === 32) {
      for (let i = 0, o = start; i < count; i++, o += 4) {
        const v = buf.readFloatLE(o);
        out[i] = v < -1 ? -1 : v > 1 ? 1 : v;
      }
      return out;
    }
    if (meta.bitsPerSample === 64) {
      for (let i = 0, o = start; i < count; i++, o += 8) {
        const v = buf.readDoubleLE(o);
        out[i] = v < -1 ? -1 : v > 1 ? 1 : v;
      }
      return out;
    }
    throw new WavFormatError(`Unsupported float bitsPerSample: ${meta.bitsPerSample}`);
  }

  throw new WavFormatError(`Unsupported WAV audioFormat: ${meta.audioFormat}`);
}
