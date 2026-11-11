"""Exact finite corroboration of the distinct-direction construction. Apache-2.0."""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path
import platform

CORE_P = ((-1, -3, 0), (1, -1, -2), (3, 3, 3))
CORE_Q = ((1, -3, 2), (3, -1, -2), (3, -1, 2))
DIAGONAL = (8, 8, 12)
V = (1, 1, -2)
MAX_BASES = 10
MAX_COPIES = 3
INPUTS = frozenset((
    "research/fstar-twelve-line-obstruction/README.md",
    "research/fstar-twelve-line-obstruction/PROOF.md",
))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def transpose(matrix):
    return tuple(zip(*matrix))


def multiply(left, right):
    require(bool(left) and bool(right), "empty matrix")
    require(all(len(row) == len(right) for row in left), "matrix dimensions")
    columns = transpose(right)
    return tuple(tuple(sum(x * y for x, y in zip(row, col))
                       for col in columns) for row in left)


def shear(parameter):
    return tuple(tuple(Fraction(int(i == j) + 4 * parameter * V[j])
                       for j in range(3)) for i in range(3))


def construct(bases, copies):
    require(type(bases) is int and 1 <= bases <= MAX_BASES, "base count")
    require(type(copies) is int and 1 <= copies <= MAX_COPIES, "copy count")
    p_rows, q_rows = [], []
    for parameter in range(bases):
        inverse = shear(-parameter)
        dual = tuple(tuple(DIAGONAL[i] * inverse[j][i] / DIAGONAL[j]
                           for j in range(3)) for i in range(3))
        p_block = multiply(shear(parameter), CORE_P)
        q_block = multiply(dual, CORE_Q)
        for p_row, q_row in zip(p_block, q_block):
            p_rows.extend((p_row,) * copies)
            q_rows.extend((q_row,) * copies)
    return tuple(p_rows), tuple(q_rows)


def valuation(number):
    require(number != 0, "zero valuation")
    numerator, denominator = abs(number.numerator), number.denominator
    return ((numerator & -numerator).bit_length()
            - (denominator & -denominator).bit_length())


def anchors(p_rows, q_rows):
    minima = tuple(min(valuation(row[j]) for row in p_rows if row[j])
                   for j in range(3))
    q_minima = tuple(min(valuation(row[j]) for row in q_rows if row[j])
                     for j in range(3))
    gamma = min(a + b for a, b in zip(minima, q_minima))
    a_masks = tuple(sum(1 << j for j, value in enumerate(row)
                        if value and valuation(value) == minima[j])
                    for row in p_rows)
    b_masks = tuple(sum(1 << j for j, value in enumerate(row)
                        if value and valuation(value) == gamma - minima[j])
                    for row in q_rows)
    return minima, gamma, a_masks, b_masks


def rank(matrix):
    rows = [list(map(Fraction, row)) for row in matrix]
    pivot = 0
    for column in range(len(rows[0])):
        selected = next((i for i in range(pivot, len(rows))
                         if rows[i][column]), None)
        if selected is None:
            continue
        rows[pivot], rows[selected] = rows[selected], rows[pivot]
        divisor = rows[pivot][column]
        rows[pivot] = [value / divisor for value in rows[pivot]]
        for i in range(pivot + 1, len(rows)):
            coefficient = rows[i][column]
            if coefficient:
                rows[i] = [x - coefficient * y
                           for x, y in zip(rows[i], rows[pivot])]
        pivot += 1
        if pivot == len(rows):
            break
    return pivot


def projective(row):
    first = next(value for value in row if value)
    return tuple(value / first for value in row)


def dot(a_mask, b_mask):
    return (a_mask & b_mask).bit_count() % 2


def witness(matrix, a_masks, b_masks, entries):
    require(len({i for i, _, _ in entries}) == len(entries), "duplicate index")
    require(all(type(i) is int and 0 <= i < len(matrix)
                for i, _, _ in entries), "witness index")
    for position, (i, a_mask, b_mask) in enumerate(entries):
        require(type(a_mask) is int and type(b_mask) is int
                and a_mask >= 0 and b_mask >= 0, "label type")
        require(a_mask & ~a_masks[i] == 0
                and b_mask & ~b_masks[i] == 0, "outside anchor")
        require(dot(a_mask, b_mask) == 1, "diagonal label")
        for j, _, other_b in entries[position + 1:]:
            require(matrix[i][j] != 0 or dot(a_mask, other_b) == 0,
                    "forward zero")


def two_block_maximum(matrix):
    n = len(matrix)
    require(1 <= n <= 12, "subset-DP size")
    size = 1 << n
    outgoing = [sum((matrix[i][j] != 0) << j for j in range(n))
                for i in range(n)]
    good, best = [False] * size, [0] * size
    good[0] = True
    for mask in range(1, size):
        for i in range(n):
            bit = 1 << i
            rest = mask ^ bit
            if mask & bit and good[rest] and rest & ~outgoing[i] == 0:
                good[mask] = True
                break
        best[mask] = mask.bit_count() if good[mask] else max(
            best[mask ^ (1 << i)] for i in range(n) if mask & (1 << i))
    full = size - 1
    return max(mask.bit_count() + best[full ^ mask]
               for mask in range(size) if good[mask])


def local_upper_bound():
    choices = [tuple((a, b) for a in range(8) for b in range(4)
                     if a & ~anchor == 0 and dot(a, b))
               for anchor in (3, 3, 7)]
    checked = 0
    for labels in product(*choices):
        for order in permutations(range(3)):
            checked += 1
            require(any(dot(labels[order[i]][0], labels[order[j]][1])
                        for i in range(3) for j in range(i + 1, 3)),
                    "three-cluster label obstruction")
    return checked


def check_family(bases, copies):
    p_rows, q_rows = construct(bases, copies)
    matrix = multiply(p_rows, transpose(q_rows))
    n = 3 * bases * copies
    require(rank(matrix) == 3, "rank three")
    minima, gamma, a_masks, b_masks = anchors(p_rows, q_rows)
    require(minima == (0, 0, 0) and gamma == 0, "normalization")
    require(a_masks == tuple(a for _ in range(bases)
                            for a in (3, 3, 7) for _ in range(copies))
            and b_masks == (3,) * n, "canonical anchors")
    for factor in (p_rows, q_rows):
        require(Counter(map(projective, factor))
                == Counter({key: copies for key in map(projective, factor)}),
                "direction multiplicity")
        require(len(set(map(projective, factor))) == 3 * bases,
                "distinct directions")
    for i in range(n):
        t, local_i = divmod(i // copies, 3)
        for j in range(n):
            s, local_j = divmod(j // copies, 3)
            expected = (int(local_i == local_j)
                        + 4 * (t - s) * V[local_j]) * DIAGONAL[local_j]
            require(matrix[i][j] == expected, "all-entry identity")
        require(sum(value == 0 for value in matrix[i]) == 2 * copies,
                "row zero degree")
        require(sum(row[i] == 0 for row in matrix) == 2 * copies,
                "column zero degree")
    entries = [(3 * t * copies + local * copies + c, 1 << local, 1 << local)
               for t in range(bases) for local in (0, 1) for c in range(copies)]
    witness(matrix, a_masks, b_masks, entries)
    require(len(entries) == 2 * bases * copies, "attaining size")
    return n * n


def rejection_controls():
    checked = 0
    for arguments in ((0, 1), (11, 1), (True, 1), (1, 0), (1, 4), (1, 1.0)):
        try:
            construct(*arguments)
        except ValueError:
            checked += 1
        else:
            raise ValueError("invalid constructor accepted")
    p_rows, q_rows = construct(2, 1)
    matrix = multiply(p_rows, transpose(q_rows))
    _, _, a_masks, b_masks = anchors(p_rows, q_rows)
    invalid = (
        [(0, 1, 1), (1, 1, 1)],
        [(0, 1, 1), (0, 1, 1)],
        [(0, 4, 4)], [(0, 1, 2)], [(-1, 1, 1)], [(0, -1, 1)],
    )
    for entries in invalid:
        try:
            witness(matrix, a_masks, b_masks, entries)
        except ValueError:
            checked += 1
        else:
            raise ValueError("invalid witness accepted")
    require(two_block_maximum(((1, 1), (0, 1))) == 2, "directed order control")
    changed_b = (7,) * 6
    witness(matrix, a_masks, changed_b,
            [(0, 1, 1), (1, 2, 2), (2, 4, 4)])
    return checked + 2


def authenticate(package, manifest=None):
    root = package.parents[1]
    if manifest is None:
        manifest = json.loads((package / "SOURCES.json").read_text())
    rows = [row for row in manifest["files"] if row["usage"] == "input"]
    require(len(rows) == len(INPUTS) and {row["path"] for row in rows} == INPUTS,
            "source input inventory")
    for row in rows:
        require(sha256((root / row["path"]).read_bytes()).hexdigest()
                == row["sha256"], "source bytes")
    return len(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path)
    arguments = parser.parse_args()
    package = Path(__file__).resolve().parent
    source_count = authenticate(package)
    entries = sum(check_family(k, s) for k in range(1, MAX_BASES + 1)
                  for s in range(1, MAX_COPIES + 1))
    dp_cases = ((1, 1), (2, 1), (3, 1), (4, 1), (1, 2), (2, 2))
    for k, s in dp_cases:
        p_rows, q_rows = construct(k, s)
        require(two_block_maximum(multiply(p_rows, transpose(q_rows))) == 2 * k * s,
                "independent two-block DP")
    controls = rejection_controls()
    forged = json.loads((package / "SOURCES.json").read_text())
    next(row for row in forged["files"] if row["usage"] == "input")["sha256"] = "0" * 64
    try:
        authenticate(package, forged)
    except ValueError:
        controls += 1
    else:
        raise ValueError("forged source pin accepted")
    result = {"status": "PASS_DISTINCT_DIRECTION_SHARPNESS",
              "family_fixtures": MAX_BASES * MAX_COPIES,
              "matrix_entries": entries, "local_label_orders": local_upper_bound(),
              "subset_dp_fixtures": len(dp_cases), "controls": controls,
              "authenticated_inputs": source_count}
    if arguments.receipt:
        receipt = {"result": result, "python": platform.python_version(),
                   "files": {path.name: sha256(path.read_bytes()).hexdigest()
                             for path in sorted(package.iterdir()) if path.is_file()}}
        arguments.receipt.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
