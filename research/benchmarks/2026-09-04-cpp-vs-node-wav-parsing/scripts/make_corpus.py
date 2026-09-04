#!/usr/bin/env python3
"""Generate the WAV benchmark corpus.

Writes deterministic RIFF/WAVE files covering the formats `Parser` supports,
so the C++ and Node harnesses read byte-identical inputs.

Usage:
    python3 make_corpus.py <output-dir>
"""

import math
import os
import struct
import sys

SAMPLE_RATE = 44100
CHANNELS = 2


def _riff(fmt_chunk: bytes, data: bytes, extra_list: bool = True) -> bytes:
    chunks = [b"fmt " + struct.pack("<I", len(fmt_chunk)) + fmt_chunk]
    if extra_list:
        # A LIST/INFO chunk, as produced by the Dissonance writeTags path.
        info = b"INFO"
        for cid, value in ((b"INAM", b"bench-corpus"), (b"IART", b"dissonance")):
            payload = value + b"\x00"
            if len(payload) % 2:
                payload += b"\x00"
            info += cid + struct.pack("<I", len(value) + 1) + payload
        chunks.append(b"LIST" + struct.pack("<I", len(info)) + info)
    chunks.append(b"data" + struct.pack("<I", len(data)) + data)
    body = b"WAVE" + b"".join(chunks)
    return b"RIFF" + struct.pack("<I", len(body)) + body


def _tone(frames: int):
    """Deterministic two-channel signal; avoids compressible all-zero data."""
    for i in range(frames):
        t = i / SAMPLE_RATE
        left = 0.6 * math.sin(2 * math.pi * 440.0 * t)
        right = 0.4 * math.sin(2 * math.pi * 660.0 * t + 0.5)
        yield left, right


def write_pcm(path: str, seconds: float, bits: int) -> None:
    frames = int(SAMPLE_RATE * seconds)
    fmt = struct.pack("<HHIIHH", 1, CHANNELS, SAMPLE_RATE,
                      SAMPLE_RATE * CHANNELS * bits // 8,
                      CHANNELS * bits // 8, bits)
    out = bytearray()
    for left, right in _tone(frames):
        for s in (left, right):
            if bits == 8:
                out += struct.pack("<B", max(0, min(255, int(s * 127) + 128)))
            elif bits == 16:
                out += struct.pack("<h", max(-32768, min(32767, int(s * 32767))))
            elif bits == 24:
                v = max(-8388608, min(8388607, int(s * 8388607)))
                out += struct.pack("<i", v)[:3]
            elif bits == 32:
                v = max(-2147483648, min(2147483647, int(s * 2147483647)))
                out += struct.pack("<i", v)
            else:
                raise ValueError(bits)
    with open(path, "wb") as fh:
        fh.write(_riff(fmt, bytes(out)))


def write_float32(path: str, seconds: float) -> None:
    frames = int(SAMPLE_RATE * seconds)
    fmt = struct.pack("<HHIIHH", 3, CHANNELS, SAMPLE_RATE,
                      SAMPLE_RATE * CHANNELS * 4, CHANNELS * 4, 32)
    out = bytearray()
    for left, right in _tone(frames):
        out += struct.pack("<ff", left, right)
    with open(path, "wb") as fh:
        fh.write(_riff(fmt, bytes(out)))


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 1
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)

    # Size sweep at the format the pipeline actually sees (16-bit stereo).
    for label, seconds in (("05s", 5), ("30s", 30), ("180s", 180), ("600s", 600)):
        write_pcm(os.path.join(out, f"pcm16_{label}.wav"), seconds, 16)

    # Format sweep at a fixed duration, to isolate decode cost per bit depth.
    write_pcm(os.path.join(out, "pcm08_30s.wav"), 30, 8)
    write_pcm(os.path.join(out, "pcm24_30s.wav"), 30, 24)
    write_pcm(os.path.join(out, "pcm32_30s.wav"), 30, 32)
    write_float32(os.path.join(out, "flt32_30s.wav"), 30)

    for name in sorted(os.listdir(out)):
        path = os.path.join(out, name)
        print(f"{name:20s} {os.path.getsize(path) / 1_000_000:8.2f} MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
