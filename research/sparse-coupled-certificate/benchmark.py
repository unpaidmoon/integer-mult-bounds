#!/usr/bin/env python3
"""Alternating complete CLI timings. Produced by Nick Petalas. Apache-2.0."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import runpy
import statistics
import subprocess
import sys
import tempfile
import time

PACKAGE = Path(__file__).resolve().parent
API = runpy.run_path(str(PACKAGE / "adapter.py"))
need = API["need"]


def run_commands(root, problem):
    runs = {"baseline": [], "changed": []}
    expected = None
    sequence = ["baseline", "changed"] * 5
    for label in sequence:
        command = [sys.executable, "-B", "-W", "error",
                   str(root / label / "certify_coupled_recurrence.py"), str(problem)]
        start = time.perf_counter()
        result = subprocess.run(command, capture_output=True, timeout=30, check=False)
        elapsed = time.perf_counter() - start
        need(result.returncode == 0 and not result.stderr, "complete CLI failure")
        certificate = json.loads(result.stdout)
        need(certificate["status"] == "contracting" and len(certificate["weights"]) == 64
             and len(certificate["total"]) == 64, "complete 64-type certificate")
        if expected is None:
            expected = result.stdout
        need(result.stdout == expected, "complete stdout mismatch")
        runs[label].append(elapsed)
    return runs, hashlib.sha256(expected).hexdigest(), sequence


def measure(parent):
    baseline, current, helper = API["sources"]()
    load_before = os.getloadavg()
    with tempfile.TemporaryDirectory(prefix="coupled-benchmark-", dir=parent) as temporary:
        root = Path(temporary)
        for label, source in (("baseline", baseline), ("changed", current)):
            directory = root / label
            directory.mkdir()
            (directory / "certify_coupled_recurrence.py").write_bytes(source)
            (directory / "compare_recursive_invoices.py").write_bytes(helper)
        path = root / "chain64.json"
        path.write_text(json.dumps(API["chain_problem"]()) + "\n")
        runs, digest, sequence = run_commands(root, path)
    summary = {name: {"median_seconds": statistics.median(values),
                       "range_seconds": [min(values), max(values)]} for name, values in runs.items()}
    return {"python": sys.version, "platform": platform.platform(), "cpu_count": os.cpu_count(),
            "load_before": load_before, "load_after": os.getloadavg(), "sequence": sequence,
            "runs_seconds": runs, "summary": summary, "complete_cli_executions": 10,
            "errors": 0, "stdout_mismatches": 0, "stdout_sha256": digest,
            "baseline_source_sha256": API["BASELINE_SHA"],
            "current_source_sha256": API["CURRENT_SHA"], "helper_source_sha256": API["HELPER_SHA"],
            "fraction_wall_time_saved": 1 - summary["changed"]["median_seconds"]
            / summary["baseline"]["median_seconds"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    need(not output.is_relative_to(PACKAGE.parents[1]) and output.parent.is_dir(),
         "output must have an existing external parent")
    need(not output.exists(), "output already exists")
    receipt = measure(output.parent)
    receipt["implementation_sha256"] = {
        name: hashlib.sha256((PACKAGE / name).read_bytes()).hexdigest()
        for name in ("adapter.py", "benchmark.py", "verify.py")}
    with output.open("x") as stream:
        stream.write(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, sort_keys=True))


if __name__ == "__main__":
    main()
