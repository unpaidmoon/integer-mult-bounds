#!/usr/bin/env python3
"""Second arithmetic path: realification over Fraction, no primary imports.

Jerry Chen (@CubeJerry), substantial OpenAI Codex assistance. Apache-2.0.
This is same-author cross-checking, not independent human review.
"""

import hashlib
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def check(condition, message):
    if not condition:
        raise ValueError(message)


def rank(a):
    a = [list(map(Q, row)) for row in a]
    pivot = 0
    for column in range(len(a[0])):
        choices = [i for i in range(pivot, len(a)) if a[i][column]]
        if not choices:
            continue
        i = choices[0]
        a[pivot], a[i] = a[i], a[pivot]
        scale = a[pivot][column]
        a[pivot] = [x / scale for x in a[pivot]]
        for i in range(len(a)):
            if i != pivot:
                factor = a[i][column]
                a[i] = [x - factor * y for x, y in zip(a[i], a[pivot], strict=True)]
        pivot += 1
        if pivot == len(a):
            break
    return pivot


def main():
    sources = json.loads((HERE / "SOURCES.json").read_text())
    for source in sources["files"]:
        if source["usage"] == "input":
            data = (ROOT / source["path"]).read_bytes()
            check(hashlib.sha256(data).hexdigest() == source["sha256"], "source hash")
    data = json.loads((ROOT / "research/p104-contractive-gram-deflation/MISSING.json").read_text())
    absent = {tuple(Q(1 if c == "+" else -1) / 2 for c in s) for s in data["signs"]}
    absent |= {tuple(-x for x in row) for row in absent}
    roots = set()
    for positions in itertools.combinations(range(8), 2):
        for signs in itertools.product((-1, 1), repeat=2):
            row = [Q(0)] * 8
            for i, sign in zip(positions, signs, strict=True):
                row[i] = Q(sign)
            if next(x for x in row if x) > 0:
                roots.add(tuple(row))
    for signs in itertools.product((-1, 1), repeat=8):
        row = tuple(Q(x, 2) for x in signs)
        if signs.count(-1) % 2 and signs[0] > 0 and row not in absent:
            roots.add(row)
    roots = sorted(roots)
    check(len(roots) == 104, "root count")
    witness = json.loads((HERE / "WITNESS.json").read_text())
    u, v = zip(*witness["z"], strict=True)
    n = sum(x * x + y * y for x, y in zip(u, v, strict=True))
    a = [[Q(int(i == j)) - Q(u[i] * u[j] + v[i] * v[j], n)
          for j in range(8)] for i in range(8)]
    b = [[Q(u[i] * v[j] - v[i] * u[j], n) for j in range(8)] for i in range(8)]
    realified = [a[i] + [-x for x in b[i]] for i in range(8)]
    realified += [b[i] + a[i] for i in range(8)]
    for i, j in itertools.product(range(16), repeat=2):
        check(realified[i][j] == realified[j][i], "realification symmetric")
        check(sum(realified[i][k] * realified[k][j] for k in range(16))
              == realified[i][j], "realification projector")
    check(rank(realified) == 14, "realification rank fourteen")
    check(rank(a) == 8, "real part rank eight")
    x = [sum(ri * ui for ri, ui in zip(r, u, strict=True)) for r in roots]
    y = [sum(ri * vi for ri, vi in zip(r, v, strict=True)) for r in roots]
    squared_errors = []
    for i, j in itertools.product(range(104), repeat=2):
        er = (x[i] * x[j] + y[i] * y[j]) / (2 * n)
        ei = (y[i] * x[j] - x[i] * y[j]) / (2 * n)
        squared_errors.append(er * er + ei * ei)
        check(er.denominator & (er.denominator - 1) == 0, "real dyadic residual")
        check(ei.denominator & (ei.denominator - 1) == 0, "imaginary dyadic residual")
    error = Q(witness["expected"]["max_entry_error"])
    check(max(squared_errors) == error * error and error < Q(1, 4), "full residual maximum")
    print(json.dumps({"status": "PASS_FRACTION_REALIFICATION", "roots": len(roots),
                      "realification_rank": 14, "real_part_rank": 8,
                      "matrix_entries": len(squared_errors),
                      "max_squared_error": str(max(squared_errors))}, sort_keys=True))


if __name__ == "__main__":
    main()
