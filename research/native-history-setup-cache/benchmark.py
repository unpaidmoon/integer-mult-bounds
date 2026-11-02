#!/usr/bin/env python3
"""Time five alternating fresh-process pairs of the complete caller."""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import platform
import statistics
import subprocess
import sys
from time import perf_counter

HERE = Path(__file__).resolve().parent


def need(condition, message):
    if not condition:
        raise ValueError(message)


def measure(root, optimized):
    samples, expected = [], None
    flags = ["-W", "error", "-B"] + (["-O"] if optimized else [])
    for trial in range(5):
        for mode in ("baseline", "cached"):
            command = [sys.executable, *flags, str(HERE / "run.py"),
                       "--root", str(root), "--mode", mode]
            start = perf_counter()
            result = subprocess.run(command, capture_output=True, timeout=120, check=False)
            elapsed = perf_counter() - start
            need(result.returncode == 0, result.stderr.decode())
            output = json.loads(result.stdout)
            need(output["status"] == "PASS_EXACT_ALL_WIDTH_FULL_HISTORY_Y_BLINDNESS",
                 "complete caller status")
            digest = sha256(result.stdout).hexdigest()
            if expected is None:
                expected = digest
            need(digest == expected, "complete scientific output bytes differ")
            samples.append({"trial": trial, "mode": mode, "seconds": elapsed,
                            "output_sha256": digest, "returncode": result.returncode,
                            "statistics": json.loads(result.stderr)})
    return samples


def summarize(samples):
    result = {}
    for mode in ("baseline", "cached"):
        values = [row["seconds"] for row in samples if row["mode"] == mode]
        result[mode] = {"median_seconds": statistics.median(values),
                        "minimum_seconds": min(values), "maximum_seconds": max(values)}
    result["fraction_less_time"] = (1 - result["cached"]["median_seconds"]
                                    / result["baseline"]["median_seconds"])
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--root", type=Path, default=HERE.parents[1])
    parser.add_argument("--optimized", action="store_true")
    args = parser.parse_args()
    samples = measure(args.root.resolve(), args.optimized)
    bound = {name: sha256((HERE / name).read_bytes()).hexdigest()
             for name in ("run.py", "benchmark.py", "SOURCES.json")}
    report = {"schema": "native-history-setup-benchmark/v1", "samples": samples,
              "summary": summarize(samples), "errors": 0, "source_sha256": bound,
              "python": sys.version, "executable": sys.executable,
              "platform": platform.platform(), "optimized": args.optimized,
              "timed_region": "fresh interpreter, authentication and complete direct caller"}
    with args.output.open("x") as handle:
        handle.write(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report["summary"], sort_keys=True))


if __name__ == "__main__":
    main()
