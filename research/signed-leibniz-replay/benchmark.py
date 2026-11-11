"""Five alternating complete fresh-process pairs; timing never gates CI."""

import argparse
import hashlib
import json
import os
import platform
import statistics
import subprocess
import sys
import tempfile
from pathlib import Path
from time import perf_counter_ns

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def command(engine, cache):
    argv = [sys.executable, "-X", "pycache_prefix=" + cache, "-W", "error", "-B"]
    if engine == "reference":
        return argv + [str(ROOT / "research/dyadic-helper-channel-capacity/verify.py")]
    return argv + [str(HERE / "adapter.py"), "--engine", "scheduled"]


def measure(engine):
    with tempfile.TemporaryDirectory(prefix="leibniz-bench-") as cache:
        argv = command(engine, cache)
        start = perf_counter_ns()
        result = subprocess.run(argv, cwd=ROOT, capture_output=True, timeout=30, check=False)
        elapsed = perf_counter_ns() - start
    if result.returncode != 0 or result.stderr:
        raise ValueError("complete replay failed: " + result.stderr.decode(errors="replace"))
    if not result.stdout.endswith(b"PASS_DYADIC_HELPER_CHANNEL_CAPACITY\n"):
        raise ValueError("complete caller did not reach its success predicate")
    return {"engine": engine, "elapsed_ns": elapsed, "stdout_sha256": hashlib.sha256(result.stdout).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    samples = []
    for _ in range(5):
        for engine in ("reference", "scheduled"):
            samples.append(measure(engine))
    if len({row["stdout_sha256"] for row in samples}) != 1:
        raise ValueError("complete scientific outputs differ")
    summaries = {}
    for engine in ("reference", "scheduled"):
        values = [row["elapsed_ns"] for row in samples if row["engine"] == engine]
        summaries[engine] = {"median_ns": statistics.median(values), "min_ns": min(values), "max_ns": max(values)}
    manifest = json.loads((HERE / "SOURCES.json").read_text())
    paths = [HERE / name for name in ("kernel.py", "adapter.py", "benchmark.py", "SOURCES.json")]
    paths += [ROOT / pin["path"] for pin in manifest["files"] if pin["usage"] == "input"]
    sources = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}
    receipt = {"python": sys.version, "platform": platform.platform(), "cpu_count": os.cpu_count(),
               "load_average": os.getloadavg(), "samples": samples, "summary": summaries,
               "errors": 0, "source_hashes": sources,
               "reduction": 1 - summaries["scheduled"]["median_ns"] / summaries["reference"]["median_ns"]}
    with args.output.open("x") as stream:
        json.dump(receipt, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(json.dumps({"summary": summaries, "reduction": receipt["reduction"], "errors": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
