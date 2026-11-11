"""Check the bounded evaluator, unchanged complete caller and source invalidation."""

import hashlib
import json
import os
import shutil
import statistics
import subprocess
import sys
import tempfile
from fractions import Fraction
from itertools import product
from math import factorial, prod
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import adapter
import kernel


def need(condition, message):
    if not condition:
        raise ValueError(message)


def check_schedules():
    count = 0
    for n in range(6):
        schedule = kernel.SCHEDULES[n]
        need(len(schedule) == factorial(n), "schedule size")
        need(len({p for p, _ in schedule}) == factorial(n), "duplicate permutation")
        for permutation, sign in schedule:
            need(sorted(permutation) == list(range(n)), "invalid permutation")
            visited = [False] * n
            cycles = 0
            for start in range(n):
                if visited[start]:
                    continue
                cycles += 1
                index = start
                for _ in range(n):
                    if visited[index]:
                        break
                    visited[index] = True
                    index = permutation[index]
                need(visited[index], "cycle did not close")
            need(sign == (-1) ** (n - cycles), "independent cycle parity")
            count += 1
    return count


def check_values(reference):
    count = 0
    for n, alphabet in ((1, range(-3, 4)), (2, range(-2, 3)), (3, range(2))):
        for entries in product(alphabet, repeat=n * n):
            matrix = [entries[i * n:(i + 1) * n] for i in range(n)]
            need(kernel.determinant(matrix) == reference(matrix), "finite determinant conformance")
            count += 1
    for n in range(6):
        for case in range(16):
            matrix = [[Fraction((case + 3 * i - 5 * j) ** 2 - 7, 2 ** ((case + i + j) % 3))
                       for j in range(n)] for i in range(n)]
            need(kernel.determinant(matrix) == reference(matrix), "rational determinant conformance")
            count += 1
        triangular = [[2 ** (65 + i) if i == j else int(i < j) for j in range(n)] for i in range(n)]
        need(kernel.determinant(triangular) == prod(2 ** (65 + i) for i in range(n)), "large integer determinant")
        count += 1
    matrix = [[2, 3], [5, 7]]
    need(kernel.determinant(matrix) == -1, "initial mutable matrix")
    matrix[0][0] = 4
    need(kernel.determinant(matrix) == 13, "stale matrix result reused")
    return count + 2


def check_rejections():
    rejected = 0
    for matrix in ([[1, 2]], [[1, 2, 3], [4, 5, 6]], [[0] * 6 for _ in range(6)]):
        try:
            kernel.determinant(matrix)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("invalid determinant domain accepted")
    original = kernel.SCHEDULES
    matrix = [[1, 2, 4], [3, 7, 5], [11, 13, 17]]
    expected = kernel.determinant(matrix)
    try:
        for broken in (original[3][:-1], tuple((p, -s) for p, s in original[3])):
            kernel.SCHEDULES = original[:3] + (broken,) + original[4:]
            need(kernel.determinant(matrix) != expected, "schedule corruption undetected")
            rejected += 1
    finally:
        kernel.SCHEDULES = original
    original_det = adapter.determinant
    try:
        adapter.determinant = lambda matrix: -original_det(matrix)
        try:
            adapter.run("compare")
        except ValueError as error:
            need(str(error) == "determinant disagreement", "wrong comparison rejection")
            rejected += 1
        else:
            raise ValueError("corrupt determinant accepted by complete comparison")
    finally:
        adapter.determinant = original_det
    return rejected


def exported_source_controls(expected_output):
    manifest = json.loads((HERE / "SOURCES.json").read_text())
    inputs = [pin["path"] for pin in manifest["files"] if pin["usage"] == "input"]
    need(len(inputs) == 5, "source-control capacity")
    with tempfile.TemporaryDirectory(prefix="leibniz-controls-") as temporary:
        root = Path(temporary)
        paths = inputs + [str((HERE / name).relative_to(ROOT)) for name in ("adapter.py", "kernel.py", "SOURCES.json")]
        for relative in paths:
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)
        argv = [sys.executable, "-I", "-W", "error", "-B"]
        if sys.flags.optimize:
            argv.append("-O")
        argv.append(str(root / HERE.relative_to(ROOT) / "adapter.py"))
        environment = dict(os.environ, PATH="")
        result = subprocess.run(argv, cwd=root, env=environment, capture_output=True, timeout=30, check=False)
        need(result.returncode == 0 and not result.stderr and result.stdout.decode() == expected_output,
             "Git-free complete export replay")
        for relative in inputs:
            target = root / relative
            original = target.read_bytes()
            target.write_bytes(original + b"\n")
            result = subprocess.run(argv, cwd=root, env=environment, capture_output=True, timeout=30, check=False)
            need(result.returncode != 0 and b"source hash mismatch" in result.stderr and not result.stdout,
                 "actual corrupted-source execution accepted")
            target.write_bytes(original)
    return len(inputs)


def check_measurement(output):
    receipt = json.loads((HERE / "MEASUREMENT.json").read_text())
    samples = receipt["samples"]
    need(len(samples) == 10 and receipt["errors"] == 0, "benchmark completion")
    need([row["engine"] for row in samples] == ["reference", "scheduled"] * 5, "benchmark order")
    need({row["stdout_sha256"] for row in samples} == {hashlib.sha256(output.encode()).hexdigest()},
         "benchmark scientific output")
    need(len(receipt["source_hashes"]) == 9, "benchmark input capacity")
    for path, digest in receipt["source_hashes"].items():
        need(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, "benchmark source changed")
    for engine in ("reference", "scheduled"):
        values = [row["elapsed_ns"] for row in samples if row["engine"] == engine]
        need(all(type(value) is int and 0 < value < 30_000_000_000 for value in values), "timing domain")
        need(receipt["summary"][engine] == {"median_ns": statistics.median(values), "min_ns": min(values), "max_ns": max(values)},
             "benchmark summary")
    a = receipt["summary"]["reference"]["median_ns"]
    b = receipt["summary"]["scheduled"]["median_ns"]
    need(receipt["reduction"] == 1 - b / a, "benchmark arithmetic")


def main():
    reference = adapter.load_caller().det
    schedules = check_schedules()
    values = check_values(reference)
    controls = check_rejections()
    original, _ = adapter.run("reference")
    scheduled, _ = adapter.run("scheduled")
    compared, trace = adapter.run("compare")
    need(original == scheduled == compared, "complete scientific output differs")
    need(trace == {"dimensions": [0, 10331, 8447, 705, 138, 33],
                   "sha256": "868f3a5d2c37364d7a93986027182bc08b620f98d2ddb6daf7ec945875edea39"},
         "complete determinant transcript differs")
    corruptions = exported_source_controls(original)
    check_measurement(original)
    hashes = {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
              for path in sorted(HERE.iterdir()) if path.is_file()}
    receipt = {"pass": "PASS_SIGNED_LEIBNIZ_REPLAY", "schedules": schedules, "conformance_values": values,
               "complete_determinants": sum(trace["dimensions"]), "trace": trace,
               "rejecting_controls": controls, "actual_source_corruptions": corruptions, "package_sha256": hashes}
    print(json.dumps(receipt, sort_keys=True))


if __name__ == "__main__":
    main()
