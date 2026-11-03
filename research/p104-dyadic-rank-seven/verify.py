#!/usr/bin/env python3
"""Exact dyadic P104 certificate. Jerry Chen / CubeJerry, Codex-assisted.

Apache-2.0. No predecessor executable, floating arithmetic or external library.
Complex numbers are pairs; the matrix audit uses integral common denominators.
"""

import hashlib
import itertools
import json
from fractions import Fraction as F
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DATA = "research/p104-contractive-gram-deflation/MISSING.json"
GUIDE = [(14, -10), (6, 23), (14, -10), (17, 3),
         (14, -10), (-3, -10), (-17, -3), (-17, -3)]
ZERO = (0, 0)


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def mul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def conj(a):
    return (a[0], -a[1])


def norm(a):
    return a[0] ** 2 + a[1] ** 2


def dot(a, b):
    return sum(x * y for x, y in zip(a, b, strict=True))


def gdot(a, b):
    result = ZERO
    for x, y in zip(a, b, strict=True):
        result = add(result, mul(x, y))
    return result


def mm(a, b):
    columns = list(zip(*b, strict=True))
    return [[gdot(row, col) for col in columns] for row in a]


def rank(matrix):
    """Separate Gaussian-rational elimination; no projector rank shortcut."""
    a = [[(F(x), F(y)) for x, y in row] for row in matrix]
    height, width, pivot_row = len(a), len(a[0]), 0
    for col in range(width):
        pivot = next((i for i in range(pivot_row, height) if a[i][col] != ZERO), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        value = a[pivot_row][col]
        inverse = (value[0] / norm(value), -value[1] / norm(value))
        a[pivot_row] = [mul(x, inverse) for x in a[pivot_row]]
        for row in range(pivot_row + 1, height):
            if a[row][col] != ZERO:
                scale = a[row][col]
                a[row] = [sub(x, mul(scale, y))
                          for x, y in zip(a[row], a[pivot_row], strict=True)]
        pivot_row += 1
        if pivot_row == height:
            break
    return pivot_row


def authenticate(payload, expected):
    require(hashlib.sha256(payload).hexdigest() == expected, "source digest")


def check_sources():
    sources = json.loads((HERE / "SOURCES.json").read_text())
    rows = [r for r in sources["files"] if r["usage"] == "input"]
    for row in rows:
        path = ROOT / row["path"]
        require(path.is_file() and not path.is_symlink(), "source regular file")
        authenticate(path.read_bytes(), row["sha256"])
    return rows


def roots_from_signs(signs):
    require(isinstance(signs, list) and len(signs) == 16, "sixteen omitted lines")
    omitted = set()
    for text in signs:
        require(isinstance(text, str) and len(text) == 8 and set(text) <= {"+", "-"},
                "sign alphabet")
        require(text.count("-") % 2 == 1, "odd spin parity")
        row = tuple(1 if x == "+" else -1 for x in text)
        omitted.add(tuple(row[0] * x for x in row))
    require(len(omitted) == 16, "distinct omitted lines")
    roots = []
    for i, j in itertools.combinations(range(8), 2):
        for sign in (-1, 1):
            row = [0] * 8
            row[i], row[j] = 2, 2 * sign
            roots.append(tuple(row))
    roots += [(1, *tail) for tail in itertools.product((-1, 1), repeat=7)
              if tail.count(-1) % 2 == 1 and (1, *tail) not in omitted]
    require(len(roots) == len(set(roots)) == 104, "104 distinct roots")
    require(all(dot(r, r) == 8 for r in roots), "doubled root norm")
    return roots, sorted(omitted)


def responses(roots, z):
    return [(dot(r, [x[0] for x in z]), dot(r, [x[1] for x in z])) for r in roots]


def projector(z, denominator=None, conjugate=True):
    require(len(z) == 8 and all(len(x) == 2 for x in z), "eight Gaussian coordinates")
    require(all(type(c) is int for x in z for c in x), "integer witness")
    n = sum(map(norm, z)) if denominator is None else denominator
    require(type(n) is int and n > 0, "positive denominator")
    d = [[sub((n * (i == j), 0), mul(z[i], conj(z[j]) if conjugate else z[j]))
          for j in range(8)] for i in range(8)]
    return d, n


def dyadic(n):
    return n > 0 and n & (n - 1) == 0


def audit_projector(d, n):
    require(all(d[i][j] == conj(d[j][i]) for i in range(8) for j in range(8)),
            "Hermitian projector")
    square = mm(d, d)
    require(square == [[(n * x, n * y) for x, y in row] for row in d],
            "projector idempotence")
    require(sum(d[i][i][0] for i in range(8)) == 7 * n, "projector trace seven")
    require(all(dyadic(n // gcd(n, c)) for row in d for entry in row for c in entry),
            "Gaussian-dyadic coefficients")
    require(rank(d) == 7, "complex projector rank seven")


def audit(z, roots, expected_error=None):
    d, n = projector(z)
    audit_projector(d, n)
    require(dyadic(n), "power-of-two squared norm")
    require(all(gdot(row, z) == ZERO for row in d), "projector kernel")
    s = [[(x, 0) for x in row] for row in roots]
    c = mm(mm(s, d), list(zip(*s, strict=True)))  # common denominator 8n
    values = responses(roots, z)
    maximum = max(map(norm, values))
    max_residual_squared, max_denominator = 0, 1
    for i, row in enumerate(roots):
        for j, other in enumerate(roots):
            residual = sub((n * dot(row, other), 0), c[i][j])
            require(residual == mul(values[i], conj(values[j])), "literal residual identity")
            max_residual_squared = max(max_residual_squared, norm(residual))
            for component in c[i][j]:
                reduced_denominator = 8 * n // gcd(8 * n, component)
                require(dyadic(reduced_denominator), "dyadic Gram coefficient")
                max_denominator = max(max_denominator, reduced_denominator)
    require(max_residual_squared == maximum ** 2, "maximum complex modulus")
    error = F(maximum, 8 * n)
    require(error < F(1, 4), "strict quarter error")
    if expected_error is not None:
        require(error == expected_error, "claimed error")
    basis = [roots.index(tuple(2 * (int(k == i) + sign * int(k == i + 1))
                                for k in range(8)))
             for i in range(0, 8, 2) for sign in (-1, 1)]
    minor = [[c[i][j] for j in basis] for i in basis]
    require(rank(minor) == 7, "Gram minor rank seven")
    real_minor = [[(x, 0) for x, y in row] for row in minor]
    require(rank(real_minor) == 8, "real-part rank eight")
    require(all(sum(r[i] * r[j] for r in roots) == 104 * (i == j)
                for i in range(8) for j in range(8)), "tight root frame")
    require(sum(c[i][i][0] for i in range(104)) == 91 * 8 * n, "Gram trace 91")
    u, v = [x for x, _ in z], [y for _, y in z]
    real_gram = [dot(u, u), dot(u, v), dot(v, v)]
    require(real_gram[0] * real_gram[2] > real_gram[1] ** 2, "independent real directions")
    return {"squared_norm": n, "maximum_squared_response": maximum,
            "max_entry_error": str(error), "gap_below_quarter": str(F(1, 4) - error),
            "attaining_indices": [i for i, x in enumerate(values) if norm(x) == maximum],
            "matrix_entries_checked": len(roots) ** 2, "projector_rank": 7,
            "Gram_rank": 7, "real_part_rank": 8, "real_direction_Gram": real_gram,
            "Gram_trace": 91, "residual_operator_norm": 13,
            "largest_Gram_coefficient_denominator": max_denominator}


def rejects(callback, reason):
    try:
        callback()
    except ValueError as exc:
        require(str(exc) == reason, "wrong rejection: " + str(exc))
        return
    raise ValueError("control accepted: " + reason)


def controls(z, roots, signs, sources):
    d, n = projector(z)
    rejects(lambda: audit_projector(*projector(z, n // 2)), "projector idempotence")
    rejects(lambda: audit_projector(*projector(z, conjugate=False)), "Hermitian projector")
    rejects(lambda: audit_projector(*projector(GUIDE)), "Gaussian-dyadic coefficients")
    bad = [tuple(x) for x in z]
    bad[0] = (bad[0][0] + 1, bad[0][1])
    rejects(lambda: audit_projector(*projector(bad)), "Gaussian-dyadic coefficients")
    rejects(lambda: audit(z, roots, F(1, 4)), "claimed error")
    # Entrywise nearest dyadic rounding of the old matrix destroys exact rank.
    old, old_n = projector(GUIDE)
    rounded = [[tuple((2 * c * n + old_n) // (2 * old_n) for c in entry)
                for entry in row] for row in old]
    rejects(lambda: audit_projector(rounded, n), "projector idempotence")
    rejects(lambda: roots_from_signs(signs[:-1]), "sixteen omitted lines")
    rejects(lambda: roots_from_signs(signs[:-1] + [signs[0]]), "distinct omitted lines")
    wrong_parity = list(signs)
    wrong_parity[0] = ("-" if signs[0][0] == "+" else "+") + signs[0][1:]
    rejects(lambda: roots_from_signs(wrong_parity), "odd spin parity")
    for row in sources:
        payload = (ROOT / row["path"]).read_bytes()
        rejects(lambda: authenticate(payload + b" ", row["sha256"]), "source digest")
    real_z = [(x, 0) for x, y in z]
    real_error = F(max(map(norm, responses(roots, real_z))),
                   8 * sum(map(norm, real_z)))
    require(real_error >= F(1, 4), "real-part witness boundary")
    return {"semantic_rejections": 9, "source_byte_rejections": len(sources),
            "rounded_predecessor_rank": rank(rounded), "real_only_error": str(real_error)}


def main():
    sources = check_sources()
    signs = json.loads((ROOT / DATA).read_text())["signs"]
    roots, omitted = roots_from_signs(signs)
    require(max(map(norm, responses(roots, GUIDE))) == 4820, "predecessor positive control")
    witness = json.loads((HERE / "WITNESS.json").read_text())
    z = [tuple(x) for x in witness["z"]]
    result = audit(z, roots, F(witness["expected"]["max_entry_error"]))
    require(result == witness["expected"], "complete witness receipt")
    # Changing root representatives and global conjugation must preserve the result.
    reversed_signs = ["".join("-" if c == "+" else "+" for c in s) for s in signs]
    require(roots_from_signs(reversed_signs)[0] == roots, "root representative invariance")
    require(audit([conj(x) for x in z], roots)["max_entry_error"] == result["max_entry_error"],
            "global conjugation invariance")
    real_controls = 0
    for q in omitted:
        require(F(max(dot(r, q) ** 2 for r in roots), 8 * dot(q, q)) == F(1, 4),
                "predecessor real quarter-error fixture")
        real_controls += 1
    result["controls"] = controls(z, roots, signs, sources)
    result["real_attaining_controls"] = real_controls
    result["status"] = "PASS_P104_DYADIC_RANK_SEVEN"
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
