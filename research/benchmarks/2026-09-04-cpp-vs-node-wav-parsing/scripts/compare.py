#!/usr/bin/env python3
"""Turn the two runner JSON files into the Markdown tables used in the report.

Usage:
    python3 compare.py <cpp.json> <node.json> > results.md
"""

import json
import os
import sys


def load(path):
    with open(path) as fh:
        data = json.load(fh)
    return data, {os.path.basename(f["file"]): f for f in data["files"]}


def fmt_ratio(r):
    return f"{r:.2f}×" if r < 10 else f"{r:.0f}×"


def row(name, cpp, node, key):
    c = cpp[key]["median"]
    n = node[key]["median"]
    ratio = n / c if c else float("inf")
    return (f"| `{name}` | {c:.3f} | {cpp[key]['min']:.3f} | {n:.3f} | "
            f"{node[key]['min']:.3f} | {fmt_ratio(ratio)} |")


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 1

    cpp_meta, cpp = load(sys.argv[1])
    node_meta, node = load(sys.argv[2])
    names = sorted(set(cpp) & set(node))

    print(f"Median of {cpp_meta['reps']} repetitions, milliseconds per call. "
          f"Node {node_meta.get('nodeVersion', '?')}.\n")

    for key, title in (("decode", "Full decode (`process` path)"),
                       ("header", "Header only (`readMetadata` path)")):
        print(f"### {title}\n")
        print("| File | C++ median | C++ min | Node median | Node min | Node / C++ (median) |")
        print("| --- | ---: | ---: | ---: | ---: | ---: |")
        for name in names:
            print(row(name, cpp[name], node[name], key))
        print()

    print("### Throughput, full decode\n")
    print("| File | Samples | C++ (Msample/s) | Node (Msample/s) |")
    print("| --- | ---: | ---: | ---: |")
    for name in names:
        s = cpp[name]["samples"]
        c = s / cpp[name]["decode"]["median"] / 1000
        n = s / node[name]["decode"]["median"] / 1000
        print(f"| `{name}` | {s:,} | {c:.1f} | {n:.1f} |")
    print()

    if "spread" in cpp[names[0]]["decode"]:
        print("### Run-to-run spread, full decode\n")
        print(f"Gap between the slowest and fastest replicate median, over "
              f"{cpp_meta.get('replicates', '?')} replicates. This is the error bar on "
              "the figures above — differences smaller than this are noise.\n")
        print("| File | C++ | Node |")
        print("| --- | ---: | ---: |")
        for name in names:
            print(f"| `{name}` | {cpp[name]['decode']['spread'] * 100:.1f}% "
                  f"| {node[name]['decode']['spread'] * 100:.1f}% |")
        print()

    print(f"Whole-run peak RSS: C++ {cpp_meta['peakRssKb'] / 1024:.0f} MB, "
          f"Node {node_meta['peakRssKb'] / 1024:.0f} MB.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
