#!/usr/bin/env python3
"""Exact finite premises and equality witness for PROOF.md. Apache-2.0."""
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

DIM = 8
PAIRS = tuple(combinations(range(DIM), 2))
SIZE = DIM + len(PAIRS)


def need(condition, message):
    if not condition:
        raise ValueError(message)


def roots():
    """One integer representative per E8 line, with squared norm eight."""
    result = []
    for i, j in PAIRS:
        for sign in (1, -1):
            row = [0] * DIM
            row[i], row[j] = 2, 2 * sign
            result.append(tuple(row))
    for signs in product((1, -1), repeat=DIM - 1):
        if signs.count(-1) % 2 == 0:
            result.append((1,) + signs)
    need(len(result) == len(set(result)) == 120, "120 distinct root lines")
    return tuple(result)


def dot(x, y):
    return sum(a * b for a, b in zip(x, y, strict=True))


def zero_matrix(size):
    return [[0] * size for _ in range(size)]


def row_form(x, y):
    """Coefficients of x^T A y in the 36 entries of symmetric A."""
    return tuple(x[i] * y[i] for i in range(DIM)) + tuple(
        x[i] * y[j] + x[j] * y[i] for i, j in PAIRS
    )


def add_outer(matrix, row):
    nonzero = tuple((i, value) for i, value in enumerate(row) if value)
    for i, a in nonzero:
        for j, b in nonzero:
            matrix[i][j] += a * b


def energy_matrix(edges):
    matrix = zero_matrix(SIZE)
    for x, y in edges:
        add_outer(matrix, row_form(x, y))
    return matrix


def orthogonal_edges(lines):
    return tuple((x, y) for x, y in combinations(lines, 2) if dot(x, y) == 0)


def metric_entry(i, j):
    return (1 if i < DIM else 2) if i == j else 0


def trace_entry(i, j):
    return int(i < DIM and j < DIM)


def check_full_energy(matrix):
    for i in range(SIZE):
        for j in range(SIZE):
            need(matrix[i][j] == 3456 * metric_entry(i, j)
                 - 432 * trace_entry(i, j), "Full E8 energy coefficient")


def check_stars(lines):
    for x in lines:
        star = tuple(y for y in lines if dot(x, y) == 0)
        need(len(star) == 63, "Every orthogonal star has 63 lines")
        for i in range(DIM):
            for j in range(DIM):
                actual = sum(y[i] * y[j] for y in star)
                need(actual == 72 * int(i == j) - 9 * x[i] * x[j],
                     "Every E7 star is a tight frame")


def frames(lines):
    first = tuple(x for x in lines if sum(bool(v) for v in x) == 2
                  and next(i for i, v in enumerate(x) if v) // 2
                  == max(i for i, v in enumerate(x) if v) // 2)
    second = tuple(tuple((-1) ** ((i & j).bit_count() % 2)
                         for j in range(DIM)) for i in range(DIM))
    check_frames(lines, first, second)
    return first, second


def check_frames(lines, first, second):
    for frame in (first, second):
        need(len(frame) == len(set(frame)) == DIM, "Frame cardinality")
        need(set(frame) <= set(lines), "Frame lines belong to E8")
        for i in range(DIM):
            for j in range(DIM):
                need(dot(frame[i], frame[j]) == 8 * int(i == j),
                     "Frame is orthonormal after normalization")
    need(set(first).isdisjoint(second), "Deleted frames are disjoint")


def check_deletion(all_edges, frame):
    deleted = energy_matrix(tuple((x, y) for x, y in all_edges
                                  if x in frame or y in frame))
    diagonal = energy_matrix(tuple((x, x) for x in frame))
    for i in range(SIZE):
        for j in range(SIZE):
            need(2 * deleted[i][j] == 1088 * metric_entry(i, j)
                 - 17 * diagonal[i][j], "Frame deletion energy coefficient")
    return diagonal


def witness():
    matrix = zero_matrix(DIM)
    for i, j, sign in ((0, 7, -1), (1, 6, -1), (2, 5, 1), (3, 4, 1)):
        matrix[i][j] = matrix[j][i] = sign
    return matrix


def bilinear(x, matrix, y):
    return sum(x[i] * matrix[i][j] * y[j]
               for i in range(DIM) for j in range(DIM))


def check_witness(matrix, live_edges, first, second):
    need(sum(matrix[i][i] for i in range(DIM)) == 0, "Witness trace zero")
    norm = sum(value * value for row in matrix for value in row)
    need(norm == 8, "Witness Frobenius norm squared")
    for i in range(DIM):
        for j in range(DIM):
            need(sum(matrix[i][k] * matrix[k][j] for k in range(DIM))
                 == int(i == j), "Witness squares to identity")
    for x in first + second:
        need(bilinear(x, matrix, x) == 0, "Zero frame diagonals")
    for x in first:
        for y in second:
            if dot(x, y) == 0:
                need(bilinear(x, matrix, y) == 0, "Zero cross-frame defect")
    energy64 = sum(bilinear(x, matrix, y) ** 2 for x, y in live_edges)
    need(energy64 == 64 * 37 * norm == 18944, "Sharp energy 296")
    return norm, energy64


def check_sos(live_matrix, cross_matrix, diagonal_first, diagonal_second):
    for i in range(SIZE):
        for j in range(SIZE):
            rhs = (4736 * metric_entry(i, j) - 864 * trace_entry(i, j)
                   + 17 * (diagonal_first[i][j] + diagonal_second[i][j])
                   + 2 * cross_matrix[i][j])
            need(2 * live_matrix[i][j] == rhs, "P104 sum-of-squares coefficient")


def rejects(operation, message):
    try:
        operation()
    except ValueError:
        return
    raise ValueError("Control accepted: " + message)


def controls(lines, all_edges, first, second, live_edges, full_matrix):
    rejects(lambda: check_full_energy(energy_matrix(all_edges[:-1])),
            "one missing full-energy edge")
    rejects(lambda: check_stars(lines[:-1]), "one missing root line")
    rejects(lambda: check_frames(lines, first, first), "repeated frame")
    rejects(lambda: check_frames(lines, first[:-1], second), "short frame")
    changed = [row[:] for row in full_matrix]
    changed[0][0] += 1
    rejects(lambda: check_full_energy(changed), "one changed coefficient")
    changed_witness = witness()
    changed_witness[0][0] = 1
    rejects(lambda: check_witness(changed_witness, live_edges, first, second),
            "changed equality witness")
    need(100 * 18944 < 64 * 3701 * 8, "37.01 fails on equality witness")
    return 7


def run():
    lines = roots()
    need(all(dot(x, x) == 8 for x in lines), "Root normalization")
    all_edges = orthogonal_edges(lines)
    need(len(all_edges) == 3780, "Full orthogonal pair count")
    full_matrix = energy_matrix(all_edges)
    check_full_energy(full_matrix)
    check_stars(lines)
    first, second = frames(lines)
    live = tuple(x for x in lines if x not in first + second)
    live_edges = orthogonal_edges(live)
    cross = tuple((x, y) for x in first for y in second if dot(x, y) == 0)
    need((len(live), len(live_edges), len(cross)) == (104, 2860, 32),
         "Equality example inventory")
    diagonal_first = check_deletion(all_edges, first)
    diagonal_second = check_deletion(all_edges, second)
    check_sos(energy_matrix(live_edges), energy_matrix(cross),
              diagonal_first, diagonal_second)
    norm, energy64 = check_witness(witness(), live_edges, first, second)
    control_count = controls(lines, all_edges, first, second, live_edges, full_matrix)
    return {"status": "PASS_P104_METRIC_ENERGY", "root_lines": len(lines),
            "full_orthogonal_pairs": len(all_edges), "stars_checked": len(lines),
            "quadratic_coefficients_per_identity": SIZE ** 2,
            "example_live_lines": len(live), "example_orthogonal_pairs": len(live_edges),
            "sharp_constant": 37, "witness_norm_squared": norm,
            "witness_energy": energy64 // 64, "rejecting_controls": control_count}


def main():
    result = run()
    here = Path(__file__).resolve().parent
    names = ("verify.py", "PROOF.md", "README.md", "TASK.json", "SOURCES.json", "VERIFY.json")
    result["source_sha256"] = {name: sha256((here / name).read_bytes()).hexdigest()
                               for name in names}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
