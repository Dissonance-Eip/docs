---
title: C++ WAV parser — audit and reference
status: final
owner: Luca Martinet
created: 2026-09-04
updated: 2026-09-04
milestone: E1
tags: [core, wav, audit]
---

# C++ WAV parser — audit and reference

## Summary

`Parser` in `core/src/utils/WavParser.cpp` reads RIFF/WAVE files and decodes PCM
8/16/24/32-bit and IEEE float 32/64-bit into normalised `float` samples in
[-1, 1]. It is correct on well-formed input from the formats it claims, and it
is fast — roughly 1,000 million samples per second on 16-bit stereo. Two of its
behaviours are worth knowing before Milestone F builds on it: the
`readAudioData = false` path is not actually header-only for 8-, 24- and 32-bit
PCM, and `WAVE_FORMAT_EXTENSIBLE` — the format many DAWs write for 24-bit and
multichannel exports — is rejected outright.

Six limitations are documented below, each with a reproduction. None of them
block Milestone E; three should be fixed before the DSP kernel in Milestone F
starts depending on this parser's guarantees.

## Where it lives

Audited at `dev` / `13bac85` (2026-09-02).

| File | Role |
| --- | --- |
| `core/include/utils/WavParser.hpp` | `Parser` class, all accessors |
| `core/src/utils/WavParser.cpp` | Chunk walk and sample decoding (194 lines) |
| `core/include/core/Errors.hpp` | `dissonance::WavFormatError` |
| `core/src/utils/WavUtils.cpp` | LIST/INFO tag parsing and in-place rewrite |
| `core/tests/wav_roundtrip_test.cpp` | Round-trip coverage |

Callers: `WavProcessor.cpp` (the `process` pipeline), `addon/addon.cpp`
(`readMetadata`), `cli/Commands.cpp` (the `info` and `process` commands).

## Public interface

```cpp
class Parser {
  public:
    static Parser fromFile(std::ifstream &file, bool readAudioData = true);
    void readFromFile(std::ifstream &file, bool readAudioData = true);

    const std::string &getRiff() const;          // "RIFF"
    uint32_t           getChunkSize() const;     // RIFF size field, unvalidated
    const std::string &getWave() const;          // "WAVE"
    uint16_t           getAudioFormat() const;   // 1 = PCM, 3 = IEEE float
    uint16_t           getNumChannels() const;
    uint32_t           getSampleRate() const;
    uint32_t           getByteRate() const;
    uint16_t           getBlockAlign() const;
    uint16_t           getBitsPerSample() const;
    uint32_t           getSubchunk2Size() const; // data chunk size in bytes
    const std::vector<float> &getAudioData() const;              // [-1, 1]
    const std::unordered_map<std::string, std::vector<char>> &
                       getOtherChunks() const;   // non-fmt, non-data chunks
};
```

`fromFile` returns by value; `Parser` is copyable and the audio buffer is copied
with it. For a ten-minute stereo file that buffer is 212 MB, so callers pass the
result around by reference.

Every failure path throws `dissonance::WavFormatError` (a `std::runtime_error`).
There are no error returns and no partial-success states: either the object is
fully populated or the constructor threw.

## How it works

1. Read and validate the 12-byte RIFF header. `riff != "RIFF"` or
   `wave != "WAVE"` throws immediately.
2. Loop over chunks. Each iteration reads a 4-byte ID and a 4-byte little-endian
   size, then dispatches:
   - **`fmt `** — read the 16 standard bytes, seek past any extension, continue.
   - **`data`** — require that `fmt ` was already seen, decode (or skip) the
     samples, then **break out of the loop**.
   - **anything else** — read the whole chunk into `otherChunks[chunkId]` and
     continue.
3. Odd-sized chunks are followed by one padding byte, which is skipped.

The loop ends only at the `data` chunk. A file with no `data` chunk runs off the
end of the stream and throws.

## What it supports

| `audioFormat` | Bits | Supported | Conversion applied |
| --- | ---: | --- | --- |
| 1 (PCM) | 8 | yes | `(u8 - 128) / 128` |
| 1 (PCM) | 16 | yes | `i16 / 32768` |
| 1 (PCM) | 24 | yes | sign-extended `i24 / 8388608` |
| 1 (PCM) | 32 | yes | `i32 / 2147483648` |
| 3 (IEEE float) | 32 | yes | read directly, clamped to [-1, 1] |
| 3 (IEEE float) | 64 | yes | clamped, narrowed to `float` |
| 65534 (`EXTENSIBLE`) | any | **no** | throws |
| 6 / 7 (A-law / µ-law) | 8 | no | throws |

Note the asymmetry in the 16-bit conversion: the divisor is 32768 while the
positive maximum of an `int16_t` is 32767, so full-scale positive peaks decode to
0.99997 rather than 1.0. This is the conventional choice — it keeps 0 at 0 and
guarantees the result stays inside [-1, 1] — and it matches what the JavaScript
reference implementation in
[`../../research/benchmarks/2026-09-04-cpp-vs-node-wav-parsing/scripts/wav_parser.mjs`](../../research/benchmarks/2026-09-04-cpp-vs-node-wav-parsing/scripts/wav_parser.mjs)
does. It is recorded here because a future FLAC or WAV writer must use the same
convention or round-trips will drift.

## Error handling

| Message | Raised when |
| --- | --- |
| `Failed to read string field` | A 4-byte ID or string could not be read — in practice, end of file |
| `Failed to read data field` | A fixed-width numeric field could not be read |
| `Not a valid RIFF/WAVE file` | Magic bytes wrong |
| `WAV missing fmt chunk before data` | `data` reached before `fmt ` |
| `Invalid bitsPerSample in WAV header` | `bitsPerSample / 8 == 0` |
| `Corrupt WAV data chunk size` | `dataSize % bytesPerSample != 0` |
| `Failed to read audio data` | The data chunk is shorter than its size field claims |
| `Unsupported PCM bitsPerSample: N` | PCM at a depth other than 8/16/24/32 |
| `Unsupported float bitsPerSample: N` | Format 3 at a depth other than 32/64 |
| `Unsupported WAV audioFormat: N` | Any format other than 1 or 3 |

## Known limitations

Each was reproduced against `dev` / `13bac85` with a purpose-built file. The
generator and the probe are in
[`../../research/benchmarks/2026-09-04-cpp-vs-node-wav-parsing/scripts/`](../../research/benchmarks/2026-09-04-cpp-vs-node-wav-parsing/scripts/).

### 1. `readAudioData = false` is not header-only for 8-, 24- and 32-bit PCM

The flag is what `readMetadata()` uses to avoid decoding a whole file just to
show its duration. It works for 16-bit PCM and 32-bit float, which `seekg` past
the data chunk. The 8-, 24- and 32-bit PCM branches read the entire data chunk
into a buffer first and only then check the flag before converting
(`WavParser.cpp:107–142`). The read is the expensive part.

Measured on a 30-second file: 0.003 ms for 16-bit, 0.254 ms for 8-bit, 0.814 ms
for 24-bit, 1.160 ms for 32-bit — a 400× spread for an operation that should
touch a few hundred bytes. It scales with file size, so a ten-minute 24-bit file
costs proportionally more.

**Impact:** the UI calls `readMetadata` on every dropped file to populate the
metadata form. For a 24-bit import this reads the whole file off disk.
**Fix:** hoist the `if (readAudioData)` check above the `file.read`, and `seekg`
in the else branch, as the 16-bit and float32 branches already do. Roughly ten
lines.

### 2. `WAVE_FORMAT_EXTENSIBLE` is rejected

```text
extensible.wav  THROW Unsupported WAV audioFormat: 65534
```

Format `0xFFFE` puts the real format in a `SubFormat` GUID inside the `fmt `
extension. Pro Tools, Reaper and Audacity all write it for 24-bit and for
anything above two channels. A user exporting a 24-bit stereo master from a DAW
is reasonably likely to hit this, and the message they would see names a number,
not a cause.

**Fix:** when `audioFormat == 0xFFFE` and `subchunk1Size >= 40`, read the
`SubFormat` GUID and map its first two bytes onto 1 or 3. About twenty lines,
and it makes the parser accept a large class of real-world files.

### 3. A second chunk with the same ID silently overwrites the first

`otherChunks` is an `unordered_map<std::string, vector<char>>`. A file with two
`LIST` chunks keeps only the last:

```text
twolist.wav  OK  samples=50 otherChunks=1
```

Chunk **order** is lost too, since a hash map has none. The class comment says
"Unknown chunks are preserved verbatim", which is true of the bytes of the
surviving chunk and not of the file's chunk structure.

**Impact:** low today — nothing writes files back through this map. It matters
the moment Milestone F adds a WAV writer that claims to preserve unknown chunks.
**Fix:** `std::vector<std::pair<std::string, std::vector<char>>>`, or correct the
comment to say what is actually guaranteed.

### 4. Chunk sizes are trusted before allocation

`std::vector<char> chunkData(currentChunkSize)` at `WavParser.cpp:182` allocates
whatever the file's size field says, before any read confirms the bytes exist. A
44-byte file declaring a 4 GB chunk:

```text
hugechunk.wav  THROW std::bad_alloc
```

The same pattern applies to the sample buffers. The throw is caught by
`addon.cpp` and surfaces as a rejected promise, so the app does not crash — but
on a memory-constrained machine the allocation attempt itself is the problem,
and this is reachable from any file a user drags in.

**Fix:** stat the stream once and reject any chunk size larger than the bytes
remaining, before allocating. Five lines, and it turns a class of malformed
files into a clean error.

### 5. A truncated final frame is accepted

The size check is `dataSize % bytesPerSample`, per **sample**. It should be per
**frame** — `dataSize % blockAlign`. A 6-byte data chunk on a 16-bit stereo file
is one and a half frames, and the parser accepts it:

```text
truncframe.wav  OK  ch=2 samples=3
```

Three samples for a stereo stream leaves a dangling left channel. Every
downstream stage that does `for (i = 0; i < n; i += channels)` reads one sample
past its own last frame.

**Fix:** add `if (currentChunkSize % blockAlign != 0)` alongside the existing
check.

### 6. NaN survives into the sample buffer

For 32-bit float input, `std::clamp` is applied per sample. `std::clamp(NaN,
-1, 1)` returns NaN — the comparisons are all false, so the value passes through.
`±Inf` clamps correctly.

```text
nan.wav  OK  samples=4 nan=1 inf=0 oob=0
```

A single NaN entering the FFT poisons an entire windowed block, and the masking
stage's thresholds go with it. The failure is silent: the output file is written,
and it is full of silence or noise.

**Fix:** `std::isfinite(s) ? std::clamp(s, -1.0f, 1.0f) : 0.0f`.

### 7. A missing `data` chunk reports the wrong error

```text
nodata.wav  THROW Failed to read string field
```

The loop has no explicit end-of-stream branch, so a valid RIFF file with no
`data` chunk fails while trying to read the next chunk ID. The message describes
the mechanism, not the problem.

**Fix:** check `file.eof()` at the top of the loop and throw
`"WAV has no data chunk"`.

## Performance

Full numbers, method and figures are in
[`../../research/benchmarks/2026-09-04-cpp-vs-node-wav-parsing/`](../../research/benchmarks/2026-09-04-cpp-vs-node-wav-parsing/).
In short, on the reference machine:

| Operation | 30 s, 16-bit stereo | 10 min, 16-bit stereo |
| --- | ---: | ---: |
| Header only | 0.003 ms | 0.003 ms |
| Full decode | 2.65 ms | 191.9 ms |

Decode throughput is 275–1,120 Msample/s depending on file size, falling as the
output buffer stops fitting in cache. The parser is memory-bandwidth bound, not
compute bound: the per-sample work is one integer divide-by-constant, which the
compiler turns into a multiply.

## Usage

```cpp
#include <fstream>
#include "utils/WavParser.hpp"

std::ifstream file("input.wav", std::ios::binary);
if (!file) throw std::runtime_error("cannot open input.wav");

try {
    // Header only — for a metadata display.
    const Parser meta = Parser::fromFile(file, /* readAudioData */ false);
    const double seconds =
        static_cast<double>(meta.getSubchunk2Size()) / meta.getByteRate();

    // Full decode — for the processing pipeline.
    file.clear();
    file.seekg(0);
    const Parser full = Parser::fromFile(file, true);
    const std::vector<float> &samples = full.getAudioData();  // interleaved
} catch (const dissonance::WavFormatError &e) {
    // Every malformed-input path arrives here.
}
```

Samples are **interleaved**, not planar: for stereo, index `2n` is left and
`2n + 1` is right. Nothing in the accessor names says so.

## Recommended follow-up

| # | Limitation | Effort | Priority |
| --- | --- | --- | --- |
| 1 | `readAudioData` reads the data chunk for 8/24/32-bit | ~10 lines | Before F — it is on the UI's hot path today |
| 6 | NaN reaches the DSP | 1 line | Before F — silent corruption |
| 5 | Truncated frame accepted | 3 lines | Before F — out-of-frame reads downstream |
| 2 | `WAVE_FORMAT_EXTENSIBLE` unsupported | ~20 lines | Before beta — real DAW exports fail |
| 4 | Unvalidated allocation size | ~5 lines | Before beta |
| 3 | Duplicate chunk IDs collapse | ~10 lines | With the F8 WAV writer |
| 7 | Misleading missing-`data` error | ~3 lines | Opportunistic |

## Related

- [`2026-09-04-cpp-electron-integration-complexity.md`](2026-09-04-cpp-electron-integration-complexity.md) — E3, what it costs to ship this from Electron
- [`../../research/benchmarks/2026-09-04-cpp-vs-node-wav-parsing/`](../../research/benchmarks/2026-09-04-cpp-vs-node-wav-parsing/) — E2, the measurements cited here
- [`../../planning/milestones.md`](../../planning/milestones.md) — Milestone E and F task lists
- `core/tests/wav_roundtrip_test.cpp` — existing round-trip coverage
