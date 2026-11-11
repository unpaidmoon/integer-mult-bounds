#!/usr/bin/env python3
"""Complete certificate conformance. Produced by Nick Petalas. Apache-2.0."""

import copy
import hashlib
import itertools
import json
from pathlib import Path
import runpy

PACKAGE = Path(__file__).resolve().parent
API = runpy.run_path(str(PACKAGE / "adapter.py"))
need = API["need"]


def problem(matrix, forcing=None):
    return {"schema": "coupled-recurrence/v1", "matrix": matrix,
            "forcing": forcing if forcing is not None else ["1"] * len(matrix)}


def fixtures():
    values = ("0", "1/2", "1", "3/2")
    for a, b, c, d in itertools.product(values, repeat=4):
        yield problem([[a, b], [c, d]])
    for size in (1, 2, 4, 8, 16, 32, 64):
        yield API["chain_problem"](size)
        yield problem([["1/" + str(2 * size)] * size for _ in range(size)])
        for failure in (0, size - 1):
            matrix = [["0"] * size for _ in range(size)]
            matrix[failure][failure] = "1"
            yield problem(matrix, ["0"] * size)
    yield problem([["0", "2"], ["1", "0"]])
    yield problem([["999999999999/1000000000000"]])


def compare_certificates(old, new):
    statuses = {"contracting": 0, "noncontracting": 0}
    for value in fixtures():
        saved = copy.deepcopy(value)
        left, right = old.certify(value), new.certify(value)
        need(left == right, "complete certificate mismatch")
        need(value == saved, "input mutated")
        need(old.verify(value, right) is True and new.verify(value, left) is True,
             "separate certificate checks")
        statuses[right["status"]] += 1
    return statuses


def failure(call, *args):
    try:
        call(*args)
    except (ValueError, TypeError, ZeroDivisionError) as error:
        return type(error).__name__, str(error)
    raise ValueError("expected rejection")


def rejection_controls(old, new):
    controls = [problem([[True]]), problem([[-1]]), problem([[0.5]]),
                problem([["0"]] * 2), problem([["0"] * 65 for _ in range(65)]),
                problem([["1000000000001"]])]
    for value in controls:
        need(failure(old.certify, value) == failure(new.certify, value), "changed rejection")
    value = problem([["0", "1/2"], ["1/2", "0"]])
    good = new.certify(value)
    for field in ("weights", "total", "ratio"):
        bad = copy.deepcopy(good)
        if field == "ratio":
            bad[field] = "0"
        else:
            bad[field][0] = "0"
        need(failure(old.verify, value, bad) == failure(new.verify, value, bad),
             "changed false-certificate rejection")
    baseline, current, helper = API["sources"]()
    need(bool(baseline), "nonempty authenticated baseline")
    failure(API["authenticate"], current + b"\n", helper)
    failure(API["authenticate"], current, helper + b"\n")
    return {"invalid_inputs": len(controls), "false_certificates": 3, "source_mutations": 2}


def package_hashes():
    names = ("README.md", "PROOF.md", "TASK.json", "SOURCES.json", "VERIFY.json",
             "adapter.py", "verify.py", "benchmark.py")
    result = {}
    for name in names:
        path = PACKAGE / name
        need(path.stat().st_size <= 262144, "bounded package file")
        result[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def main():
    old, new = API["versions"]()
    result = {"certificate_statuses": compare_certificates(old, new),
              "controls": rejection_controls(old, new),
              "baseline_sha256": API["BASELINE_SHA"], "current_sha256": API["CURRENT_SHA"],
              "package_sha256": package_hashes()}
    print(json.dumps(result, sort_keys=True))
    print("PASS_SPARSE_COUPLED_CERTIFICATE")


if __name__ == "__main__":
    main()
