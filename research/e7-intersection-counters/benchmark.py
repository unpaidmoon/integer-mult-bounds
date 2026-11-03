"""Measure alternating complete E7 replays; write a generated timing receipt."""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.resolve().is_relative_to(HERE.resolve()):
        raise ValueError("write benchmark output outside the package")
    rows = []
    for label in ("original", "intersection") * 5:
        command = [sys.executable, "-I", "-W", "error", "-B",
                   str(HERE / "replay.py"), "--engine", label]
        start = time.perf_counter()
        result = subprocess.run(command, capture_output=True, timeout=60)
        elapsed = time.perf_counter() - start
        if result.returncode or result.stderr:
            raise ValueError("complete replay failed: " + result.stderr.decode())
        if not result.stdout.startswith(b"PASS_E7_MINIMUM_SUPPORT_CLASSIFICATION\n"):
            raise ValueError("complete scientific work was not reported")
        rows.append(dict(engine=label, seconds=elapsed, returncode=result.returncode,
                         stdout_sha256=sha256(result.stdout).hexdigest(),
                         stderr_bytes=len(result.stderr)))
    if len({row["stdout_sha256"] for row in rows}) != 1:
        raise ValueError("complete scientific output differs")
    samples = {label: [r["seconds"] for r in rows if r["engine"] == label]
               for label in ("original", "intersection")}
    medians = {label: statistics.median(values) for label, values in samples.items()}
    files = ("engine.py", "replay.py", "benchmark.py", "SOURCES.json")
    receipt = dict(python=sys.version, executable=sys.executable,
                   platform=platform.platform(), cpu_count=os.cpu_count(),
                   load_average=os.getloadavg(), errors=0, serial=True,
                   command_flags=["-I", "-W", "error", "-B"], records=rows,
                   median_seconds=medians,
                   range_seconds={label: [min(v), max(v)] for label, v in samples.items()},
                   reduction=1 - medians["intersection"] / medians["original"],
                   implementation_sha256={name: sha256((HERE / name).read_bytes()).hexdigest()
                                          for name in files})
    args.output.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({key: receipt[key] for key in
                      ("median_seconds", "range_seconds", "reduction", "errors")}))


if __name__ == "__main__":
    main()
