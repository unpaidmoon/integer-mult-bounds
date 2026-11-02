"""Complete alternating measurements, produced by Nick Petalas. Apache-2.0."""

import argparse
import hashlib
import json
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import time

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[1]


def run(engine):
    command = [sys.executable, "-I", "-W", "error", "-B", str(PACKAGE / "adapter.py"),
               "--engine", engine]
    started = time.perf_counter()
    child = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=120)
    elapsed = time.perf_counter() - started
    if child.returncode != 0:
        raise RuntimeError(f"{engine} failed: {child.stderr}")
    result = json.loads(child.stdout)
    payload = json.dumps(result["payload"], sort_keys=True, separators=(",", ":")).encode()
    return {"engine": engine, "seconds": elapsed,
            "payload_sha256": hashlib.sha256(payload).hexdigest(), "cache": result["cache"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rounds", type=int, default=5)
    args = parser.parse_args()
    if not 5 <= args.rounds <= 10:
        raise ValueError("rounds must be between five and ten")
    samples = []
    for number in range(args.rounds):
        order = ("reference", "tail") if number % 2 == 0 else ("tail", "reference")
        for engine in order:
            samples.append(run(engine))
    if len({sample["payload_sha256"] for sample in samples}) != 1:
        raise ValueError("complete payload disagreement")
    if any(sample["cache"] != samples[0]["cache"] for sample in samples):
        raise ValueError("cache workload disagreement")
    summary = {}
    for engine in ("reference", "tail"):
        times = [sample["seconds"] for sample in samples if sample["engine"] == engine]
        summary[engine] = {"median": statistics.median(times), "range": [min(times), max(times)]}
    receipt = {"status": "PASS_COMPLETE_STAGE_PAIR_MEASUREMENTS", "errors": 0,
               "samples": samples, "summary": summary, "python": sys.version,
               "platform": platform.platform(), "package_sha256": {
                   path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                   for path in sorted(PACKAGE.iterdir()) if path.is_file()}}
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
