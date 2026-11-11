"""Complete fixed-caller timings, produced by Nick Petalas. Apache-2.0."""

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kernel
import source


def worker(side):
    reference = source.load()
    started = time.perf_counter_ns()
    output = reference.search("two_without_cap") if side == "baseline" else kernel.search(reference)
    counts, closed, hits = output
    hashes = [sha256("".join("".join(map(str, w)) + "\n" for w in words).encode()).hexdigest()
              for words in (closed, hits)]
    return {"side": side, "counts": counts, "hashes": hashes,
            "caller_ns": time.perf_counter_ns() - started}


def sample(side):
    env = dict(os.environ)
    env.pop("PYTHONOPTIMIZE", None)
    started = time.perf_counter_ns()
    result = subprocess.run([sys.executable, "-I", "-W", "error", "-B", __file__, "--worker", side],
                            env=env, capture_output=True, check=True, timeout=30)
    wall = time.perf_counter_ns() - started
    row = json.loads(result.stdout)
    if result.stderr:
        raise ValueError("unexpected stderr: " + result.stderr.decode())
    return {"wall_ns": wall, **row}


def benchmark(pairs):
    started = datetime.now(timezone.utc).isoformat()
    files = ("kernel.py", "source.py", "benchmark.py", "SOURCES.json")
    hashes = {p: sha256((source.HERE / p).read_bytes()).hexdigest() for p in files}
    rows = []
    expected = None
    for pair in range(pairs):
        order = ("baseline", "candidate") if pair % 2 == 0 else ("candidate", "baseline")
        for side in order:
            row = sample(side)
            observed = (row["counts"], row["hashes"])
            if expected is None:
                expected = observed
            if observed != expected or row["counts"]["universal"] != 828:
                raise ValueError("complete caller output mismatch")
            rows.append({"pair": pair, **row})
    if hashes != {p: sha256((source.HERE / p).read_bytes()).hexdigest() for p in files}:
        raise ValueError("timed source changed")
    summary = {}
    for side in ("baseline", "candidate"):
        values = [r["wall_ns"] for r in rows if r["side"] == side]
        summary[side] = {"median_ns": statistics.median(values), "min_ns": min(values), "max_ns": max(values)}
    ratios = []
    for pair in range(pairs):
        block = {r["side"]: r["wall_ns"] for r in rows if r["pair"] == pair}
        ratios.append(block["candidate"] / block["baseline"])
    return {"started_at": started, "finished_at": datetime.now(timezone.utc).isoformat(),
            "python": sys.version, "platform": platform.platform(), "cpu_count": os.cpu_count(),
            "load_average": os.getloadavg(), "pairs": pairs, "errors": 0, "rows": rows,
            "source_sha256": hashes, "input_sha256": source.authenticate(), "summary": summary,
            "median_paired_ratio": statistics.median(ratios), "faster_pairs": sum(r < 1 for r in ratios),
            "scope": "Sequential fresh processes; complete caller, source reading, cache setup, startup and output included. OS caches not flushed; other host work uncontrolled. No performance threshold in CI."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker", choices=("baseline", "candidate"))
    parser.add_argument("--pairs", type=int, default=9)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.worker:
        print(json.dumps(worker(args.worker), sort_keys=True))
        return
    if not 5 <= args.pairs <= 30 or args.output is None:
        parser.error("provide --output and 5 <= --pairs <= 30")
    if args.output.exists():
        parser.error("output already exists")
    report = benchmark(args.pairs)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(json.dumps({k: report[k] for k in ("summary", "median_paired_ratio", "faster_pairs", "errors")}))


if __name__ == "__main__":
    main()
