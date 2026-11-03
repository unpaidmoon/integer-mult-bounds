"""Time five alternating pairs of complete, source-authenticated replays.

Produced by Nick Petalas. Apache-2.0.
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

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import replay


def normalized(output):
    suffix = "\nPASS_UNIVERSAL_DIRTY_CERTIFICATES\n"
    replay.need(output.endswith(suffix), "complete caller success marker")
    report = json.loads(output[:-len(suffix)])
    del report["seconds"]
    del report["exponential_support"]["seconds"]
    return report


def executable_hashes():
    names = ("benchmark.py", "check_certificate.py", "replay.py", "SOURCES.json")
    return {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest() for name in names}


def run_pairs():
    hashes, inputs = executable_hashes(), replay.authenticate()
    samples = {"baseline": [], "cached": []}
    expected = None
    for trial in range(5):
        for side in ("baseline", "cached"):
            command = [sys.executable, "-I", "-W", "error", "-B", str(HERE / "replay.py")]
            if side == "baseline":
                command.append("--baseline")
            start = time.perf_counter_ns()
            result = subprocess.run(command, cwd=replay.ROOT, capture_output=True,
                                    text=True, check=True, timeout=90)
            elapsed = (time.perf_counter_ns() - start) / 1e9
            replay.need(not result.stderr, "warning-free complete replay")
            report = normalized(result.stdout)
            if expected is None:
                expected = report
            replay.need(report == expected, "complete scientific output differs")
            samples[side].append(elapsed)
            print(json.dumps({"trial": trial, "side": side, "seconds": elapsed}), flush=True)
    replay.need(executable_hashes() == hashes and replay.authenticate() == inputs,
                "sources changed during measurement")
    before, after = (statistics.median(samples[side]) for side in ("baseline", "cached"))
    return {"schema": "complete-dirty-path-benchmark/v1", "python": sys.version,
            "platform": platform.platform(), "logical_cpus": os.cpu_count(),
            "load_average_at_end": os.getloadavg(), "failures": 0,
            "executable_sha256": hashes, "input_sha256": inputs,
            "samples_seconds": samples, "median_seconds": {"baseline": before, "cached": after},
            "reduction_percent": 100 * (before - after) / before,
            "scientific_output": expected, "successful_complete_replays": 10}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    output = args.receipt.resolve()
    replay.need(not output.is_relative_to(replay.ROOT), "receipt must be outside checkout")
    replay.need(not output.exists(), "receipt must be a new path")
    receipt = run_pairs()
    with output.open("x") as stream:
        stream.write(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print("PASS_COMPLETE_DIRTY_PATH_BENCHMARK", receipt["reduction_percent"])


if __name__ == "__main__":
    main()
