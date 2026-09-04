#!/usr/bin/env python3
"""Print the headline decode comparison as a plain console table.

Usage:
    python3 summary.py <cpp.json> <node.json>
"""

import json
import sys

ORDER = ["pcm16_05s.wav", "pcm16_30s.wav", "pcm16_180s.wav", "pcm16_600s.wav",
         "real_sound_186s.wav", "pcm08_30s.wav", "pcm24_30s.wav",
         "pcm32_30s.wav", "flt32_30s.wav"]


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 1

    cpp = {f["file"]: f for f in json.load(open(sys.argv[1]))["files"]}
    node = {f["file"]: f for f in json.load(open(sys.argv[2]))["files"]}
    names = [n for n in ORDER if n in cpp and n in node]
    names += sorted(set(cpp) & set(node) - set(names))

    print(f"{'file':<22} {'C++ decode':>11} {'Node decode':>12} {'ratio':>7}")
    print("-" * 56)
    for name in names:
        c = cpp[name]["decode"]["median"]
        n = node[name]["decode"]["median"]
        print(f"{name:<22} {c:>8.2f} ms {n:>9.2f} ms {n / c:>6.2f}x")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
