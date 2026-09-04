#!/usr/bin/env python3
"""Generate the malformed and unusual WAV files used in the parser audit.

Each file reproduces exactly one limitation documented in
design/core/2026-09-04-cpp-wav-parser-audit.md. Feed them to probe_parser.cpp.

Usage:
    python3 make_edge_cases.py <output-dir>
"""

import os
import struct
import sys


def chunk(cid: bytes, payload: bytes) -> bytes:
    """A RIFF chunk with its size field and the pad byte odd sizes require."""
    size = len(payload)
    if size % 2:
        payload += b"\x00"
    return cid + struct.pack("<I", size) + payload


def riff(fmt: bytes, data: bytes, extra: bytes = b"") -> bytes:
    body = b"WAVE" + chunk(b"fmt ", fmt) + extra + chunk(b"data", data)
    return b"RIFF" + struct.pack("<I", len(body)) + body


def pcm_fmt(channels: int, bits: int, rate: int = 44100) -> bytes:
    block = channels * bits // 8
    return struct.pack("<HHIIHH", 1, channels, rate, rate * block, block, bits)


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 1
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)

    def write(name, payload):
        with open(os.path.join(out, name), "wb") as fh:
            fh.write(payload)

    # (2) WAVE_FORMAT_EXTENSIBLE — what DAWs write for 24-bit and multichannel.
    # audioFormat 0xFFFE, cbSize 22, valid bits 16, channel mask, PCM SubFormat GUID.
    extensible = (
        struct.pack("<HHIIHH", 0xFFFE, 2, 44100, 176400, 4, 16)
        + struct.pack("<H", 22)
        + struct.pack("<H", 16)
        + struct.pack("<I", 0x3)
        + b"\x01\x00\x00\x00\x00\x00\x10\x00\x80\x00\x00\xaa\x00\x38\x9b\x71"
    )
    write("extensible.wav", riff(extensible, b"\x00\x00" * 100))

    # (3) Two LIST chunks — the second overwrites the first in otherChunks.
    two_lists = (
        chunk(b"LIST", b"INFO" + chunk(b"INAM", b"first\x00"))
        + chunk(b"LIST", b"INFO" + chunk(b"IART", b"second\x00"))
    )
    write("twolist.wav", riff(pcm_fmt(1, 16), b"\x00\x00" * 50, two_lists))

    # (4) A chunk declaring 4 GB in a file of a few dozen bytes.
    body = b"WAVE" + chunk(b"fmt ", pcm_fmt(1, 16)) + b"junk" + struct.pack("<I", 0xF0000000)
    write("hugechunk.wav", b"RIFF" + struct.pack("<I", len(body)) + body)

    # (5) 6 bytes of 16-bit stereo — one and a half frames.
    write("truncframe.wav", riff(pcm_fmt(2, 16), b"\x01\x00\x02\x00\x03\x00"))

    # (6) float32 carrying NaN, +Inf and an out-of-range value.
    floats = struct.pack("<ffff", float("nan"), float("inf"), -2.5, 0.5)
    write("nan.wav", riff(struct.pack("<HHIIHH", 3, 1, 44100, 176400, 4, 32), floats))

    # (7) A valid RIFF/WAVE header with no data chunk at all.
    body = b"WAVE" + chunk(b"fmt ", pcm_fmt(1, 16))
    write("nodata.wav", b"RIFF" + struct.pack("<I", len(body)) + body)

    for name in sorted(os.listdir(out)):
        print(f"{name:18s} {os.path.getsize(os.path.join(out, name)):>8} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
