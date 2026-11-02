"""Time complete fresh callers and emit hash-bound evidence. Apache-2.0."""

import argparse
import datetime
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


def canonical_output(stdout):
    lines = stdout.splitlines()
    if (len(lines) != 3 or lines[1] != "PASS_EXTENSION_FIELD_TENSOR_RECOGNITION"
            or not lines[2].startswith("elapsed_seconds=")):
        raise RuntimeError("complete caller did not finish successfully")
    report = json.loads(lines[0])
    if ([row["domain"] for row in report["exhaustive"]] != [256, 65536]
            or report["controls"] != 125 or report["SL_transporters"] != 90):
        raise RuntimeError("complete caller coverage changed")
    return (lines[0] + "\n" + lines[1] + "\n").encode()


def run_once(mode, optimized=False):
    command = [sys.executable, "-I", "-W", "error", "-B"]
    if optimized:
        command.append("-O")
    command += [str(HERE / "replay.py"), mode]
    environment = dict(os.environ)
    environment.pop("PYTHONOPTIMIZE", None)
    started = time.perf_counter()
    process = subprocess.run(command, capture_output=True, text=True,
                             timeout=150, check=False, env=environment)
    elapsed = time.perf_counter() - started
    if process.returncode != 0 or process.stderr:
        raise RuntimeError("complete caller failed: " + process.stderr[:2000])
    output = canonical_output(process.stdout)
    return {"mode": mode, "wall_seconds": elapsed,
            "load_average": os.getloadavg() if hasattr(os, "getloadavg") else None,
            "output_sha256": hashlib.sha256(output).hexdigest(),
            "report": json.loads(process.stdout.splitlines()[0])}


def file_hashes():
    names = ("kernel.py", "replay.py", "benchmark.py", "SOURCES.json")
    return {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
            for name in names}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pairs", type=int, default=5, choices=range(5, 11))
    args = parser.parse_args()
    runs = []
    for pair in range(args.pairs):
        for mode in ("original", "prepared"):
            run = run_once(mode)
            run["pair"] = pair + 1
            runs.append(run)
            print(json.dumps({"completed_pair": pair + 1, "mode": mode}), file=sys.stderr)
    if len({row["output_sha256"] for row in runs}) != 1:
        raise RuntimeError("complete reports disagree")
    summary = {}
    for mode in ("original", "prepared"):
        samples = [row["wall_seconds"] for row in runs if row["mode"] == mode]
        summary[mode] = {"median": statistics.median(samples),
                         "minimum": min(samples), "maximum": max(samples)}
    summary["fraction_removed"] = 1 - summary["prepared"]["median"] / summary["original"]["median"]
    receipt = {"claim_type": "local complete-caller performance measurement",
               "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "python": sys.version, "executable": sys.executable,
               "platform": platform.platform(), "cpu_count": os.cpu_count(),
               "errors": 0, "hashes": file_hashes(), "summary": summary, "runs": runs}
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
