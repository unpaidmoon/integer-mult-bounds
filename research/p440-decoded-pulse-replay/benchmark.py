#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Time fresh complete baseline/changed callers in alternating order."""

import hashlib
import json
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    samples = {"baseline": [], "prepared": []}
    output_hashes = set()
    for _ in range(5):
        for mode in samples:
            command = [sys.executable, "-I", "-W", "error", "-B", str(HERE / "fast.py")]
            if mode == "baseline":
                command.append("--baseline")
            start = time.perf_counter()
            result = subprocess.run(command, cwd=ROOT, capture_output=True,
                                    timeout=120, check=True)
            elapsed = time.perf_counter() - start
            if result.stderr or not result.stdout.startswith(b"PASS_INDEPENDENT_P440_"):
                raise ValueError("complete caller did not succeed cleanly")
            samples[mode].append(elapsed)
            output_hashes.add(hashlib.sha256(result.stdout).hexdigest())
    if len(output_hashes) != 1:
        raise ValueError("complete caller outputs differ")
    summary = {mode: {"median_seconds": statistics.median(values),
                      "range_seconds": [min(values), max(values)]}
               for mode, values in samples.items()}
    names = ["fast.py", "benchmark.py", "SOURCES.json"]
    hashes = {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest() for name in names}
    baseline = summary["baseline"]["median_seconds"]
    prepared = summary["prepared"]["median_seconds"]
    print(json.dumps({"status": "PASS_COMPLETE_P440_TIMING", "samples_seconds": samples,
                      "summary": summary, "seconds_saved": baseline - prepared,
                      "reduction_percent": 100 * (baseline - prepared) / baseline,
                      "successful_complete_callers": 10, "errors": 0,
                      "output_sha256": next(iter(output_hashes)), "source_sha256": hashes,
                      "python": sys.version, "platform": platform.platform(),
                      "processor": platform.processor(), "executable": sys.executable,
                      "workload": "unchanged PR1431 independent.main including all controls"},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
