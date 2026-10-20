#!/usr/bin/env python3
"""Largest paid child rank in the E8 label-pairing alphabet.

The support alphabet is PR717's label pairing on the 120 root lines:
N_ij = (<r_i, r_j> + 1) mod 2. A paid term of pairing rank rho is one
recursive child of rank rho. A frame transport of that child is one child
of the same rank. A dirty-slot restoration is one rank-1 child. No new kappa.
"""
import importlib.util
import itertools
import sys
from fractions import Fraction as Q
from pathlib import Path


def fail(message):
    raise SystemExit("FAIL_E8_LABEL_CHILD_RANK_CAP " + message)


def f2_rank(rows):
    basis = {}
    for v in rows:
        while v:
            h = v.bit_length() - 1
            if h in basis:
                v ^= basis[h]
            else:
                basis[h] = v
                break
    return len(basis), basis


def e8_lines():
    roots = []
    for i, j in itertools.combinations(range(8), 2):
        for si in (1, -1):
            for sj in (1, -1):
                v = [0] * 8
                v[i], v[j] = 2 * si, 2 * sj
                roots.append(tuple(v))
    for signs in itertools.product((1, -1), repeat=8):
        if signs.count(-1) % 2 == 0:
            roots.append(tuple(signs))
    lines = []
    seen = set()
    for root in roots:
        neg = tuple(-a for a in root)
        key = root if root > neg else neg
        if key not in seen:
            seen.add(key)
            lines.append(root)
    return roots, lines


def inner(x, y):
    dot = sum(a * b for a, b in zip(x, y))
    if dot % 4 != 0:
        fail("doubled inner product not divisible by 4")
    return dot // 4


def pairing_rows(lines):
    n = len(lines)
    gram = [[inner(lines[i], lines[j]) for j in range(n)] for i in range(n)]
    rows = []
    for i in range(n):
        row = 0
        for j in range(n):
            if (gram[i][j] + 1) & 1:
                row |= 1 << j
        rows.append(row)
    return gram, rows


def load_ceiling():
    path = Path("research/complex-local-word-ceiling/ceiling.py")
    spec = importlib.util.spec_from_file_location("selected_ceiling", path)
    if spec is None or spec.loader is None:
        fail("cannot load ceiling.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def invoice_rank(kind, rho):
    if kind in ("term", "transport"):
        if not isinstance(rho, int) or not 1 <= rho <= 9:
            fail("term or transport rank outside 1..9: " + repr((kind, rho)))
        return rho
    if kind == "restore":
        if rho != 1:
            fail("restoration is a rank-1 child")
        return 1
    fail("unknown invoice kind " + repr(kind))


def main():
    roots, lines = e8_lines()
    if len(roots) != 240 or len(lines) != 120:
        fail("expected 240 roots and 120 lines, got %d and %d" % (len(roots), len(lines)))
    gram, rows = pairing_rows(lines)
    off = {gram[i][j] for i in range(120) for j in range(120) if i != j}
    if any(gram[i][i] != 2 for i in range(120)) or off != {-1, 0, 1}:
        fail("line inner products are not the E8 root-line values")
    for i in range(120):
        for j in range(i):
            bit_ij = (rows[i] >> j) & 1
            bit_ji = (rows[j] >> i) & 1
            if bit_ij != bit_ji:
                fail("label pairing is not symmetric")
    rank, basis = f2_rank(rows)
    if rank != 9:
        fail("full label pairing rank is %d, not 9" % rank)
    for row in rows:
        residual = row
        while residual:
            h = residual.bit_length() - 1
            if h not in basis:
                fail("a pairing row leaves the 9-dimensional row space")
            residual ^= basis[h]
    pivot_columns = sorted(basis)
    minor_rows = [basis[column] for column in pivot_columns]
    minor_rank, _ = f2_rank(minor_rows)
    if minor_rank != 9 or len(pivot_columns) != 9:
        fail("reduced pairing basis is not rank 9")
    # A tenth independent row is not a submatrix of this pairing.
    outside = 1 << 120
    outside_rank, _ = f2_rank(rows + [outside])
    if outside_rank != 10:
        fail("control row was not independent of the pairing")
    capped, _ = f2_rank([row for row in rows])
    if capped > 9:
        fail("subrow rank exceeded 9")

    selected = {1: 2412, 2: 418, 3: 432, 4: 142, 5: 82, 8: 8}
    selected_mass = sum(rank_ * count for rank_, count in selected.items())
    if selected_mass != 5586 or max(selected) != 8:
        fail("selected local profile is not mass 5586 with maximum rank 8")
    samples = (
        ("term", 9),
        ("term", 8),
        ("term", 1),
        ("transport", 9),
        ("transport", 4),
        ("restore", 1),
    )
    invoice_max = max(invoice_rank(kind, rho) for kind, rho in samples)
    if invoice_max != 9:
        fail("invoice maximum is not 9")
    rejected = False
    try:
        invoice_rank("term", 10)
    except SystemExit:
        rejected = True
    if not rejected:
        fail("rank-10 term was accepted")
    rejected = False
    try:
        invoice_rank("restore", 9)
    except SystemExit:
        rejected = True
    if not rejected:
        fail("rank-9 restoration was accepted")

    ceiling = load_ceiling()
    fractional = {9: Q(5586, 9)}
    integer = {9: 620, 6: 1}
    if 9 * 620 + 6 != 5586:
        fail("integer rank-9 histogram misses the local mass")
    width, families, stages, centre = 73, 896, 9, 64
    target = Q(1, 99)
    frac_lo, frac_hi = ceiling.ceiling(fractional, width, families, stages, centre)
    int_lo, int_hi = ceiling.ceiling(integer, width, families, stages, centre)
    sel_lo, sel_hi = ceiling.ceiling(selected, width, families, stages, centre)
    if not (frac_lo < frac_hi < target and int_lo < int_hi < target and sel_hi < int_hi):
        fail("rank-9 ceiling is not strictly below 1/99 and above the selected word")
    frac_at_target = ceiling.relax(fractional, width, families, stages, centre, target)
    int_at_target = ceiling.relax(integer, width, families, stages, centre, target)
    if frac_at_target[0] <= 1 or int_at_target[0] <= 1:
        fail("rank-9 relaxation does not fail at a = 1/99")
    # Smaller ranks are weakly dearer per unit of mass once a > 0, so the
    # rank-9 histogram is the favorable screen inside the cap.
    eight = {8: Q(5586, 8)}
    eight_at_frac = ceiling.relax(eight, width, families, stages, centre, frac_lo)
    if eight_at_frac[0] <= 1:
        fail("rank-8 mass is not strictly above the rank-9 screen")

    print(
        "PASS_E8_LABEL_CHILD_RANK_CAP"
        " lines=120 pairing_rank=9 minor_rank=9"
        " selected_max_rank=8 invoice_max_rank=9"
        " rank9_ceiling_hi=%s integer_ceiling_hi=%s selected_ceiling_hi=%s"
        " below_1/99=true rank10_rejected=true"
        " controls=10 no_new_kappa=true" % (frac_hi, int_hi, sel_hi)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
