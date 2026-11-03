"""Measure complete fresh-process callers; timing is local evidence only.

Produced by Nick Petalas. Apache-2.0.
"""
import argparse
from hashlib import sha256
from itertools import permutations
import json
import os
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def measure(command, expected, counts):
    started = time.perf_counter()
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, timeout=30)
    elapsed = time.perf_counter() - started
    if completed.returncode:
        raise ValueError("Caller failed: " + completed.stderr.decode())
    if expected is not None and completed.stdout != expected:
        raise ValueError("Complete caller output differs")
    if counts and json.loads(completed.stderr) != {"products": 277, "compared_entries": 0}:
        raise ValueError("Caller work count differs")
    return elapsed, completed.stdout


def run(rounds):
    prefix = [sys.executable, "-I", "-W", "error", "-B"]
    commands = {
        "original": prefix + ["research/nonlinear-monomial-control-ceiling/verify.py"],
        "reference": prefix + ["research/nonlinear-support-integer-products/runner.py", "--mode", "reference"],
        "integer": prefix + ["research/nonlinear-support-integer-products/runner.py"],
    }
    orders = tuple(permutations(commands))
    rows = []
    expected = None
    for number in range(rounds):
        for mode in orders[number % len(orders)]:
            elapsed, output = measure(commands[mode], expected, mode != "original")
            if expected is None:
                expected = output
            rows.append({"round": number, "mode": mode, "seconds": elapsed})
    summary = {}
    for mode in commands:
        values = [row["seconds"] for row in rows if row["mode"] == mode]
        summary[mode] = {"median_seconds": statistics.median(values),
                         "minimum_seconds": min(values), "maximum_seconds": max(values)}
    hashes = {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
              for p in sorted(HERE.glob("*.py"))}
    return {"schema": 1, "rows": rows, "summary": summary, "commands": commands,
            "errors": 0, "rounds_per_mode": rounds, "products_per_adapted_caller": 277,
            "complete_stdout_sha256": sha256(expected).hexdigest(), "implementation_sha256": hashes,
            "python": platform.python_version(), "platform": platform.platform(),
            "cpu_count": os.cpu_count(), "load_average_at_end": os.getloadavg(),
            "scope": "Fresh complete processes include interpreter startup, all source authentication, all finite checks, output comparison and private scratch cleanup. Shared-host load is uncontrolled. No portable speed guarantee."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rounds", type=int, default=18)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not 6 <= args.rounds <= 60:
        raise ValueError("rounds must be between six and sixty")
    if args.output.exists():
        raise ValueError("output must be new")
    result = run(args.rounds)
    with args.output.open("x") as output:
        output.write(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result["summary"], sort_keys=True))


if __name__ == "__main__":
    main()
