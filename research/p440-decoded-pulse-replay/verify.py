#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact differential controls and unchanged complete-caller execution."""

from fractions import Fraction
import hashlib
import importlib.util
from itertools import product
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def load_fast():
    path = HERE / "fast.py"
    spec = importlib.util.spec_from_file_location("p440_prepared", path)
    module = importlib.util.module_from_spec(spec)
    exec(compile(path.read_bytes(), str(path), "exec"), module.__dict__)
    return module


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def differential_controls(fast):
    source = fast.load_source()
    gates = [None]
    for target in range(2):
        for coefficient in (Fraction(-2), Fraction(-1, 2), Fraction(0), Fraction(1, 2), Fraction(2)):
            gates.append(["add", target, 1 - target, coefficient.numerator,
                          coefficient.denominator, [7]])
        for coefficient in (-1, 0, 2):
            gates.append(["scale", target, coefficient, 1, [7]])
    cases = 0
    for length in range(3):
        for word in product(gates, repeat=length):
            prepared = fast.prepare(word)
            for initial in ({}, {0: Fraction(1, 3)}, {0: Fraction(-2), 1: Fraction(3, 2)}):
                for cut in range(length + 1):
                    pulses = {cut: [(0, Fraction(1, 2)), (1, Fraction(-1, 3))]}
                    expected = source.run(word, initial, pulses)
                    require(fast.run(prepared, initial, pulses) == expected, "pulse recurrence differs")
                    cases += 1
    return cases


def rejection_controls(fast):
    controls = [lambda: fast.load_source(fast.SOURCE.read_bytes() + b"\n"),
                lambda: fast.prepare([["other", 0, 1, 1]]),
                lambda: fast.prepare([["add", 0, 1, 1, 0]]),
                lambda: fast.prepare([None] * 8193),
                lambda: fast.run([None] * 8193, {})]
    for control in controls:
        try:
            control()
        except (ValueError, ZeroDivisionError):
            continue
        raise ValueError("source or gate boundary mutation was accepted")
    return len(controls)


def complete_callers():
    outputs = []
    for baseline in (True, False):
        command = [sys.executable, "-I", "-W", "error", "-B", str(HERE / "fast.py")]
        if sys.flags.optimize:
            command.insert(1, "-O")
        if baseline:
            command.append("--baseline")
        result = subprocess.run(command, cwd=ROOT, capture_output=True, timeout=120, check=True)
        require(not result.stderr, "complete caller emitted diagnostics")
        require(result.stdout.startswith(b"PASS_INDEPENDENT_P440_"), "missing complete success")
        outputs.append(result.stdout)
    require(outputs[0] == outputs[1], "complete caller output differs")
    return hashlib.sha256(outputs[0]).hexdigest()


def check_benchmark(output):
    receipt = json.loads((HERE / "BENCHMARK.json").read_text())
    require(receipt["output_sha256"] == output, "timed caller output differs")
    require(receipt["errors"] == 0 and receipt["successful_complete_callers"] == 10,
            "timing receipt did not complete every caller")
    for name, expected in receipt["source_sha256"].items():
        require(name in ("fast.py", "benchmark.py", "SOURCES.json"), "unknown timing source")
        require(hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected,
                "timing source changed")
    require(set(receipt["source_sha256"]) == {"fast.py", "benchmark.py", "SOURCES.json"},
            "timing source coverage missing")
    for values in receipt["samples_seconds"].values():
        require(len(values) == 5 and all(0 < value < 120 for value in values),
                "invalid complete-caller timing samples")


def main():
    fast = load_fast()
    cases = differential_controls(fast)
    controls = rejection_controls(fast)
    output = complete_callers()
    check_benchmark(output)
    names = ["README.md", "TASK.json", "SOURCES.json", "VERIFY.json", "fast.py",
             "verify.py", "benchmark.py", "BENCHMARK.json"]
    hashes = {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest() for name in names}
    print(json.dumps({"status": "PASS_P440_PREPARED_REPLAY", "differential_cases": cases,
                      "rejection_controls": controls, "complete_callers": 2,
                      "output_sha256": output, "package_sha256": hashes}, sort_keys=True))


if __name__ == "__main__":
    main()
