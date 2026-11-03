"""Check the new kernel, complete CLI, and source-invalidation boundaries.

Produced by Nick Petalas. Apache-2.0.
"""
from fractions import Fraction as Q
from hashlib import sha256
import io
from itertools import product
import json
import os
from pathlib import Path
import random
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest

from run import PACKAGE, ROOT, authenticate
from solver import solve
from workload import problem


def require(condition, message):
    if not condition:
        raise ValueError(message)


def kernel_checks(original):
    count = singular = 0
    for entries in product(range(-2, 3), repeat=4):
        matrix = [[Q(x) for x in entries[:2]], [Q(x) for x in entries[2:]]]
        determinant = entries[0] * entries[3] - entries[1] * entries[2]
        for values in product(range(-1, 2), repeat=2):
            rhs = list(map(Q, values))
            before = [row[:] for row in matrix], rhs[:]
            actual = solve(matrix, rhs)
            require(actual == original(matrix, rhs), "Kernel result differs")
            require((actual is None) == (determinant == 0), "Singular classification")
            require(before == (matrix, rhs), "Kernel mutated its input")
            if actual is not None:
                require(all(sum(x*y for x, y in zip(row, actual)) == b
                            for row, b in zip(matrix, rhs)), "Residual is nonzero")
            else:
                singular += 1
            count += 1
    rng = random.Random(103002)
    for size in range(1, 7):
        for trial in range(60):
            matrix = [[Q(rng.randrange(-7, 8), rng.randrange(1, 8))
                       for _ in range(size)] for _ in range(size)]
            if size > 1 and trial % 3 == 0:
                matrix[-1] = matrix[0][:]
            rhs = [Q(rng.randrange(-9, 10), rng.randrange(1, 8)) for _ in range(size)]
            actual = solve(matrix, rhs)
            require(actual == original(matrix, rhs), "Rational kernel result differs")
            if actual is not None:
                require(all(sum(x*y for x, y in zip(row, actual)) == b
                            for row, b in zip(matrix, rhs)), "Rational residual")
            count += 1
    return {"systems": count, "exhaustive_singular_systems": singular}


def contract_controls():
    invalid = [([], []), ([[Q(1)]], []), ([[Q(1), Q(0)]], [Q(1)]),
               ([[1]], [Q(1)]), ([[Q(10**9 + 1)]], [Q(0)]),
               ([[Q(1, 10**9 + 1)]], [Q(0)]),
               ([[Q(0)] * 7 for _ in range(7)], [Q(0)] * 7)]
    for matrix, rhs in invalid:
        try:
            solve(matrix, rhs)
        except ValueError:
            continue
        raise ValueError("Invalid kernel contract accepted")
    matrix = [[Q(0), Q(1, 10**9)], [Q(-10**9), Q(0)]]
    require(solve(matrix, [Q(1), Q(1)]) == [Q(-1, 10**9), Q(10**9)],
            "Boundary pivot/size control")
    return len(invalid) + 1


def complete_checks(engine):
    original = engine.solve
    baseline = engine.optimize(problem())
    engine.solve = solve
    try:
        candidate = engine.optimize(problem())
        require(candidate == baseline, "Complete certificate differs")
        require(candidate["objective"] == "24" and candidate["bases_examined"] == 757,
                "Complete fixture changed")
        namespace = runpy.run_path(str(ROOT / "tests/test_research_rational_box.py"))
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(namespace["BoxTests"])
        result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)
        require(result.wasSuccessful() and result.testsRun == 6, "Inherited regression failure")
    finally:
        engine.solve = original
    require(engine.solve is original, "Original binding was not restored")
    return {"objective": "24", "bases_examined": 757, "inherited_test_groups": 6}


def invoke(command, cwd):
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=30)
    require(len(result.stdout) + len(result.stderr) < 1024 * 1024, "Excessive output")
    return result


def cli_and_invalidation(scratch):
    exported = scratch / "export"
    package = exported / "research" / PACKAGE.name
    package.mkdir(parents=True)
    for path in PACKAGE.iterdir():
        if path.is_file() and path.suffix in (".py", ".json", ".md"):
            shutil.copyfile(path, package / path.name)
    records = json.loads((PACKAGE / "SOURCES.json").read_text())["files"]
    inputs = [row["path"] for row in records if row["usage"] == "input"]
    for name in inputs:
        target = exported / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    value = scratch / "problem.json"
    value.write_text(json.dumps(problem()))
    flags = ["-O"] if sys.flags.optimize else []
    command = [sys.executable, *flags, "-B", str(package / "run.py"), str(value)]
    result = invoke(command, scratch)
    require(result.returncode == 0, "Git-free CLI failed: " + result.stderr)
    baseline = invoke([sys.executable, *flags, "-B", str(ROOT / "scripts/optimize_rational_box.py"),
                       str(value)], scratch)
    require(baseline.returncode == 0 and result.stdout == baseline.stdout,
            "Complete CLI bytes differ")
    certificate = scratch / "certificate.json"
    certificate.write_text(result.stdout)
    checked = invoke(command + ["--check", str(certificate)], scratch)
    require(checked.returncode == 0 and checked.stdout.strip() == "PASS_RATIONAL_BOX_OPTIMUM",
            "Complete certificate check failed")
    for name in inputs:
        target = exported / name
        data = target.read_bytes()
        target.write_bytes(data + b"\n")
        failed = invoke(command, scratch)
        require(failed.returncode == 2 and "Source bytes changed: " + name in failed.stderr,
                "Changed source was accepted")
        target.write_bytes(data)
    return {"complete_cli_byte_equality": True, "changed_input_rejections": len(inputs)}


def main():
    authenticate()
    sys.path.insert(0, str(ROOT / "scripts"))
    import optimize_rational_box as engine
    result = {"marker": "PASS_RATIONAL_BOX_FRACTION_FREE"}
    result.update(kernel_checks(engine.solve))
    result["contract_controls"] = contract_controls()
    with tempfile.TemporaryDirectory(dir=os.environ.get("IMB_RUN_DIR")) as directory:
        previous = tempfile.tempdir
        tempfile.tempdir = directory
        try:
            result.update(complete_checks(engine))
            result.update(cli_and_invalidation(Path(directory)))
        finally:
            tempfile.tempdir = previous
    result["sha256"] = {str(path.relative_to(ROOT)): sha256(path.read_bytes()).hexdigest()
                        for path in sorted(PACKAGE.iterdir()) if path.is_file()}
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
