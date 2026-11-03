"""Alternate fresh complete callers and retain successful output hashes.

Produced by Nick Petalas. The timing includes interpreter startup, source
authentication, all small checks, the entire graph caller and receipt checking.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import time

PACKAGE = Path(__file__).resolve().parent


def run_one(engine: str) -> dict:
    argv = [sys.executable, "-I", "-W", "error", "-B",
            str(PACKAGE / "replay.py"), "--engine", engine]
    start = time.perf_counter_ns()
    result = subprocess.run(argv, capture_output=True, timeout=120, check=True)
    elapsed = time.perf_counter_ns() - start
    if result.stderr:
        raise ValueError("Unexpected diagnostic: " + result.stderr.decode())
    receipt = json.loads(result.stdout)
    if receipt["actual"]["exact_axis_cases"] != 79360:
        raise ValueError("Complete graph work was not performed")
    return {"engine": engine, "argv": argv, "elapsed_ns": elapsed,
            "stdout_sha256": hashlib.sha256(result.stdout).hexdigest(),
            "actual_axis_cases": receipt["actual"]["exact_axis_cases"],
            "returncode": result.returncode}


def measure(pairs: int) -> dict:
    runs = []
    for _pair in range(pairs):
        for engine in ("literal", "rank"):
            runs.append(run_one(engine))
    if len({run["stdout_sha256"] for run in runs}) != 1:
        raise ValueError("Complete caller outputs disagree")
    samples = {engine: [r["elapsed_ns"] for r in runs if r["engine"] == engine]
               for engine in ("literal", "rank")}
    summaries = {engine: {"median_ns": statistics.median(values),
                          "min_ns": min(values), "max_ns": max(values)}
                 for engine, values in samples.items()}
    return {"status": "PASS_COMPLETE_CONTACT_BENCHMARK", "pairs": pairs,
            "errors": 0, "python": sys.version, "platform": platform.platform(),
            "cpu_count": os.cpu_count(), "load_average": os.getloadavg(),
            "runs": runs, "summaries": summaries,
            "median_reduction_fraction": 1 - summaries["rank"]["median_ns"]
            / summaries["literal"]["median_ns"],
            "package_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in sorted(PACKAGE.iterdir()) if p.is_file()}}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pairs", type=int, default=5, choices=range(5, 10))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if PACKAGE in args.output.resolve().parents:
        raise ValueError("Write benchmark logs outside the package")
    out = measure(args.pairs)
    args.output.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n",
                           encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("status", "pairs", "errors", "summaries",
                                        "median_reduction_fraction")}, sort_keys=True))


if __name__ == "__main__":
    main()
