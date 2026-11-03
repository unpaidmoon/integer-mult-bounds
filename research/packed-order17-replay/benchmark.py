"""Alternate five complete four-command replay bundles per implementation."""

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

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_replay import authenticate

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def bundle(fast):
    source = ROOT / "research/order-seventeen-clifford"
    primary = HERE / "run_replay.py" if fast else source / "verify.py"
    commands = []
    for path in (primary, source / "independent.py"):
        for mode in ([], ["-O"]):
            commands.append([sys.executable, "-I", "-B", "-W", "error", *mode, str(path)])
    digests = []
    started = time.perf_counter()
    for command in commands:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, check=True, timeout=60)
        if result.stderr:
            raise ValueError("unexpected replay stderr")
        if b"PASS_" not in result.stdout:
            raise ValueError("missing completion marker")
        digests.append(hashlib.sha256(result.stdout).hexdigest())
    return time.perf_counter() - started, digests


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    authenticate()
    implementation_sha256 = {
        name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
        for name in ("packed.py", "run_replay.py", "benchmark.py")}
    source_sha256 = hashlib.sha256((HERE / "SOURCES.json").read_bytes()).hexdigest()
    runs = {"baseline": [], "packed": []}
    expected = None
    sequence = []
    load_before = os.getloadavg() if hasattr(os, "getloadavg") else None
    for pair in range(5):
        for name in (("baseline", "packed") if pair % 2 == 0 else ("packed", "baseline")):
            elapsed, digests = bundle(name == "packed")
            if expected is None:
                expected = digests
            if digests != expected:
                raise ValueError("complete replay output mismatch")
            runs[name].append(elapsed)
            sequence.append(name)
    summary = {name: {"median_seconds": statistics.median(values),
                      "range_seconds": [min(values), max(values)]}
               for name, values in runs.items()}
    receipt = {"schema_version": 1, "python": sys.version, "executable": sys.executable,
               "platform": platform.platform(), "cpu_count": os.cpu_count(),
               "load_before": load_before,
               "load_after": os.getloadavg() if hasattr(os, "getloadavg") else None,
               "scope": "complete original four-command suite; packed primary and unchanged independent",
               "sequence": sequence, "runs_seconds": runs, "summary": summary,
               "completed_commands": 40, "failures": 0, "output_mismatches": 0,
               "stdout_sha256_by_command": expected,
               "implementation_sha256": implementation_sha256,
               "source_manifest_sha256": source_sha256,
               "fraction_wall_time_saved": 1 - summary["packed"]["median_seconds"] /
                                                 summary["baseline"]["median_seconds"]}
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(receipt, stream, indent=2)
        stream.write("\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
