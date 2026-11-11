#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact conformance and corruption controls for integer product checking.

Produced by Nick Petalas. The frozen baseline retains Ali Romman's credit.
"""
from copy import deepcopy
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
import random
from fixtures import PACKAGE, ROOT, dense_fixture, load, problem


def require(condition, message):
    if not condition:
        raise ValueError(message)


def bindings():
    source = json.loads((PACKAGE / "SOURCES.json").read_text())
    pins = {row["path"]: row for row in source["files"]}
    require(sha256((PACKAGE / "baseline.py").read_bytes()).hexdigest() ==
            pins["scripts/certify_rational_rank.py"]["sha256"], "Baseline bytes changed")
    path = "scripts/compare_recursive_invoices.py"
    require(sha256((ROOT / path).read_bytes()).hexdigest() == pins[path]["sha256"],
            "Parser dependency bytes changed")
    return load("frozen_rank", PACKAGE / "baseline.py"), load(
        "integer_rank", ROOT / "scripts/certify_rational_rank.py")


def rejects(tool, value, certificate):
    try:
        tool.verify(value, certificate)
    except (ValueError, TypeError, KeyError, ZeroDivisionError):
        return True
    return False


def certificate_cases(old, new):
    count = 0
    for entries in product(range(2), repeat=9):
        value = problem([list(entries[i:i+3]) for i in (0, 3, 6)])
        require(old.certify(value) == new.certify(value), "Binary certificate changed")
        count += 1
    rng = random.Random(103011)
    for m, n in product(range(1, 6), repeat=2):
        for _ in range(3):
            value = problem([[str(Q(rng.randrange(-5, 6), rng.randrange(1, 12)))
                              for _ in range(n)] for _ in range(m)])
            require(old.certify(value) == new.certify(value), "Rational certificate changed")
            count += 1
    for value in (problem([[0]*64 for _ in range(64)]),
                  problem([[int(i == j) for j in range(64)] for i in range(64)]),
                  problem([[0, 0, 0, 0], [0, 0, 2, 1], [0, 3, 0, 2], [0, 6, 4, 6]]),
                  dense_fixture()):
        require(old.certify(value) == new.certify(value), "Boundary certificate changed")
        count += 1
    return count


def product_cases(new):
    rng = random.Random(911)
    count = 0
    for m, k, n in product(range(4), repeat=3):
        for _ in range(8):
            a = [[Q(rng.randrange(-9, 10), rng.randrange(1, 17)) for _ in range(k)]
                 for _ in range(m)]
            b = [[Q(rng.randrange(-9, 10), rng.randrange(1, 17)) for _ in range(n)]
                 for _ in range(k)]
            c = [[sum((a[i][t]*b[t][j] for t in range(k)), Q(0))
                  for j in range(n)] for i in range(m)]
            require(new._product_equal(a, b, c, m, k, n), "True rational product rejected")
            count += 1
            if m and n:
                c[-1][-1] += Q(1, 19)
                require(not new._product_equal(a, b, c, m, k, n), "False product accepted")
                count += 1
    # Each denominator fits a certificate's 4096-character rational budget,
    # but their coprime product exceeds the fast path's memory guard.
    a = [[Q(1), Q(1)]]
    b = [[Q(1, 2**9000)], [Q(1, 3**6000)]]
    c = [[b[0][0] + b[1][0]]]
    require(new._scaled_rows([[b[0][0], b[1][0]]]) is None, "Scale guard did not fire")
    require(new._product_equal(a, b, c, 1, 2, 1), "Fallback rejected a true product")
    c[0][0] += Q(1, 11)
    require(not new._product_equal(a, b, c, 1, 2, 1), "Fallback accepted a false product")
    count += 2
    return count


def rejection_cases(old, new):
    value = problem([[1, 0, 1], [0, 1, 1], [1, 1, 2]])
    good = old.certify(value)
    count = 0
    for key in ("minor_inverse", "coefficients", "right_kernel", "left_kernel"):
        for i, row in enumerate(good[key]):
            for j in range(len(row)):
                bad = deepcopy(good)
                bad[key][i][j] = str(Q(bad[key][i][j]) + Q(1, 13))
                require(rejects(old, value, bad) and rejects(new, value, bad),
                        "A corrupted witness component was accepted")
                count += 1
    for key, data in (("rank", True), ("rank", -1), ("rows", [0, 0]),
                      ("columns", [0, 3]), ("minor_inverse", [[1]]),
                      ("coefficients", []), ("right_kernel", []), ("left_kernel", [])):
        bad = deepcopy(good)
        bad[key] = data
        require(rejects(old, value, bad) and rejects(new, value, bad),
                "A malformed witness was accepted")
        count += 1
    return count


def main():
    old, new = bindings()
    counts = {"complete_certificates": certificate_cases(old, new),
              "rational_products_and_mutants": product_cases(new),
              "certificate_rejections": rejection_cases(old, new)}
    paths = sorted(p for p in PACKAGE.iterdir() if p.is_file())
    paths += [ROOT / "scripts/certify_rational_rank.py", ROOT / "scripts/compare_recursive_invoices.py"]
    require(len(paths) <= 16 and all(p.stat().st_size <= 1024**2 for p in paths),
            "Receipt file bound exceeded")
    hashes = {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths}
    print(json.dumps({"status": "PASS_INTEGER_RANK_PRODUCTS", "counts": counts,
                      "source_sha256": hashes}, sort_keys=True))


if __name__ == "__main__":
    main()
