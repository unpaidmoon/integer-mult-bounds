"""Time complete fresh-process solve plus certificate-check CLI pairs.

Produced by Nick Petalas. Apache-2.0. Timing is an opt-in local measurement.
"""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import resource
import statistics
import subprocess
import sys
import tempfile
import time

from run import ROOT, PACKAGE, authenticate
from workload import problem


def source_hashes():
    paths = (ROOT / "scripts/optimize_rational_box.py",
             ROOT / "scripts/compare_recursive_invoices.py",
             PACKAGE / "run.py", PACKAGE / "solver.py", PACKAGE / "workload.py",
             PACKAGE / "benchmark.py", PACKAGE / "SOURCES.json")
    return {str(path.relative_to(ROOT)): sha256(path.read_bytes()).hexdigest() for path in paths}


def one(script, value, certificate):
    command = [sys.executable, "-B", str(script), str(value)]
    start_cpu = resource.getrusage(resource.RUSAGE_CHILDREN)
    start = time.perf_counter()
    generated = subprocess.run(command, capture_output=True, timeout=30, check=True)
    certificate.write_bytes(generated.stdout)
    checked = subprocess.run(command + ["--check", str(certificate)],
                             capture_output=True, timeout=30, check=True)
    elapsed = time.perf_counter() - start
    end_cpu = resource.getrusage(resource.RUSAGE_CHILDREN)
    cpu = end_cpu.ru_utime + end_cpu.ru_stime - start_cpu.ru_utime - start_cpu.ru_stime
    if checked.stdout != b"PASS_RATIONAL_BOX_OPTIMUM\n":
        raise ValueError("Certificate was not checked")
    return elapsed, cpu, generated.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rounds", type=int, default=7)
    args = parser.parse_args()
    if not 5 <= args.rounds <= 15:
        parser.error("Use 5..15 rounds per arm")
    authenticate()
    sources = source_hashes()
    records = {"baseline": [], "candidate": []}
    scripts = {"baseline": ROOT / "scripts/optimize_rational_box.py",
               "candidate": PACKAGE / "run.py"}
    reference = None
    with tempfile.TemporaryDirectory(dir=os.environ.get("IMB_RUN_DIR")) as directory:
        scratch = Path(directory)
        value = scratch / "problem.json"
        value.write_text(json.dumps(problem(), sort_keys=True))
        fixture_digest = sha256(value.read_bytes()).hexdigest()
        for _ in range(args.rounds):
            for arm in ("baseline", "candidate"):
                wall, cpu, output = one(scripts[arm], value, scratch / (arm + ".json"))
                if reference is None:
                    reference = output
                if output != reference:
                    raise ValueError("Complete optimization output changed")
                parsed = json.loads(output)
                if parsed["bases_examined"] != 757 or parsed["objective"] != "24":
                    raise ValueError("Complete workload changed")
                records[arm].append({"wall_seconds": wall, "cpu_seconds": cpu})
    authenticate()
    if sources != source_hashes():
        raise ValueError("Benchmark source bytes changed during measurement")
    medians = {arm: statistics.median(row["wall_seconds"] for row in values)
               for arm, values in records.items()}
    result = {"marker": "MEASURED_RATIONAL_BOX_COMPLETE_CLI", "python": sys.version,
              "platform": platform.platform(), "rounds_per_arm": args.rounds,
              "fixture_sha256": fixture_digest, "output_sha256": sha256(reference).hexdigest(),
              "bases_per_solve": 757, "checked_cli_pairs": 2 * args.rounds,
              "errors": 0, "samples": records, "median_wall_seconds": medians,
              "fraction_wall_time_removed": 1 - medians["candidate"] / medians["baseline"],
              "sources_sha256": sources}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
