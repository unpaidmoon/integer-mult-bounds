"""Ten alternating fresh-process pairs of the complete scientific caller.

Produced by Nick Petalas. Apache-2.0. Timing is evidence, never a CI gate.
"""

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


def main():
    pins = replay.authenticate()
    runs = []
    load_before = os.getloadavg() if hasattr(os, "getloadavg") else None
    for pair in range(10):
        for mode in ("baseline", "specialized"):
            command = [sys.executable, "-I", "-W", "error", "-B", str(HERE / "replay.py")]
            if mode == "baseline":
                command.append("--baseline")
            start = time.perf_counter()
            result = subprocess.run(command, capture_output=True, timeout=120)
            elapsed = time.perf_counter() - start
            if result.returncode:
                raise RuntimeError(result.stderr.decode(errors="replace"))
            if not result.stdout.startswith(b"PASS_WEIGHTED_FOURIER_LAYOUT "):
                raise RuntimeError("complete caller did not finish")
            runs.append({"pair": pair, "mode": mode, "seconds": elapsed,
                         "stdout_sha256": hashlib.sha256(result.stdout).hexdigest(),
                         "returncode": result.returncode})
    if len({row["stdout_sha256"] for row in runs}) != 1:
        raise RuntimeError("complete caller output changed")
    summaries = {}
    for mode in ("baseline", "specialized"):
        values = [row["seconds"] for row in runs if row["mode"] == mode]
        summaries[mode] = {"median_seconds": statistics.median(values),
                           "range_seconds": [min(values), max(values)]}
    print(json.dumps({"runs": runs, "summaries": summaries, "failures": 0,
                      "paired_savings_seconds": [runs[2*i]["seconds"] - runs[2*i+1]["seconds"]
                                                 for i in range(10)],
                      "work_counts": json.loads(result.stdout.split(b" ", 1)[1]),
                      "source_hashes": pins,
                      "program_hashes": {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
                                         for name in ("benchmark.py", "replay.py", "SOURCES.json")},
                      "python": sys.version, "executable": sys.executable,
                      "platform": platform.platform(), "cores": os.cpu_count(),
                      "load_before": load_before,
                      "scope": "complete retained scientific main; tests run separately"}, indent=2))


if __name__ == "__main__":
    main()
