#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Five alternating fresh-process certificate and saved-check bundles.

Write every output under --scratch. Produced by Nick Petalas.
"""
import argparse
import cProfile
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import pstats
import statistics
import subprocess
import sys
import time
from fixtures import PACKAGE, ROOT, dense_fixture, load


def command_run(script, problem_path, certificate_path, environment):
    base = [sys.executable, "-X", "pycache_prefix=" + str(problem_path.parent / "bytecode"),
            "-W", "error", "-B", str(script), str(problem_path)]
    start = time.perf_counter_ns()
    result = subprocess.run(base, capture_output=True, env=environment, timeout=120)
    if result.returncode or result.stderr:
        raise ValueError("Certificate producer failed: " + result.stderr.decode())
    certificate_path.write_bytes(result.stdout)
    check = subprocess.run(base + ["--check", str(certificate_path)],
                           capture_output=True, env=environment, timeout=120)
    elapsed = time.perf_counter_ns() - start
    if check.returncode or check.stderr or check.stdout != b"PASS_RATIONAL_RANK_CERTIFICATE\n":
        raise ValueError("Saved certificate check failed: " + check.stderr.decode())
    return elapsed, sha256(result.stdout).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scratch", required=True, type=Path)
    args = parser.parse_args()
    if not args.scratch.is_dir():
        parser.error("--scratch must name an existing directory")
    fixture = dense_fixture()
    problem_path = args.scratch / "rank-problem.json"
    problem_path.write_text(json.dumps(fixture, sort_keys=True))
    old = load("profile_rank", PACKAGE / "baseline.py")
    profile = cProfile.Profile()
    profile.runcall(old.certify, fixture)
    with (args.scratch / "profile.txt").open("w") as stream:
        pstats.Stats(profile, stream=stream).sort_stats("cumtime").print_stats(20)
    environment = dict(os.environ, PYTHONPATH=str(ROOT / "scripts"), PYTHONDONTWRITEBYTECODE="1")
    environment.pop("PYTHONOPTIMIZE", None)
    environment.pop("PYTHONPYCACHEPREFIX", None)
    scripts = {"before": PACKAGE / "baseline.py", "after": ROOT / "scripts/certify_rational_rank.py"}
    samples = {side: [] for side in scripts}
    hashes = set()
    for pair in range(5):
        # Reverse each pair so neither implementation owns the first position.
        for side in (("before", "after") if pair % 2 == 0 else ("after", "before")):
            ns, digest = command_run(scripts[side], problem_path,
                                     args.scratch / (side + "-certificate.json"), environment)
            samples[side].append(ns)
            hashes.add(digest)
    if len(hashes) != 1:
        raise ValueError("Serialized certificate bytes changed")
    medians = {side: statistics.median(values) for side, values in samples.items()}
    paths = [PACKAGE / "baseline.py", PACKAGE / "fixtures.py", PACKAGE / "benchmark.py",
             ROOT / "scripts/certify_rational_rank.py", ROOT / "scripts/compare_recursive_invoices.py"]
    result = {"schema": "integer-rank-product-benchmark/v1", "errors": 0,
              "bundles": 10, "successful_cli_commands": 20,
              "fixture": {"rows": 48, "columns": 64, "rank": 8},
              "python": sys.version, "platform": platform.platform(),
              "load_average": os.getloadavg(), "cpu_count": os.cpu_count(),
              "samples_ns": samples, "medians_ns": medians,
              "wall_time_reduction": 1 - medians["after"] / medians["before"],
              "certificate_sha256": next(iter(hashes)),
              "problem_sha256": sha256(problem_path.read_bytes()).hexdigest(),
              "source_sha256": {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths}}
    output = args.scratch / "benchmark.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
