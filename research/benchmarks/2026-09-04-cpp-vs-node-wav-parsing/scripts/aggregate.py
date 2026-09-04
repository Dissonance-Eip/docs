#!/usr/bin/env python3
"""Merge replicate runs of one runner into a single canonical result file.

Each replicate already reports the median of N in-process repetitions. This
takes the median of those medians (and the min of the mins) across replicates,
so a single noisy replicate cannot move the published number.

Usage:
    python3 aggregate.py <out.json> <run1.json> <run2.json> [run3.json ...]
"""

import json
import os
import statistics
import sys


def main() -> int:
    if len(sys.argv) < 4:
        print(__doc__)
        return 1

    out_path, run_paths = sys.argv[1], sys.argv[2:]
    runs = [json.load(open(p)) for p in run_paths]

    merged = {
        "runner": runs[0]["runner"],
        "reps": runs[0]["reps"],
        "replicates": len(runs),
        "files": [],
    }
    if "nodeVersion" in runs[0]:
        merged["nodeVersion"] = runs[0]["nodeVersion"]

    by_name = [{os.path.basename(f["file"]): f for f in r["files"]} for r in runs]
    for name in sorted(by_name[0]):
        entry = {"file": name, "samples": by_name[0][name]["samples"]}
        for op in ("header", "decode"):
            medians = [r[name][op]["median"] for r in by_name]
            entry[op] = {
                "median": statistics.median(medians),
                "min": min(r[name][op]["min"] for r in by_name),
                # Worst relative gap between replicate medians: the honest
                # error bar on the published figure.
                "spread": (max(medians) - min(medians)) / min(medians),
            }
        merged["files"].append(entry)

    merged["peakRssKb"] = max(r["peakRssKb"] for r in runs)
    with open(out_path, "w") as fh:
        json.dump(merged, fh, indent=2)
    print(f"wrote {out_path} from {len(runs)} replicates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
