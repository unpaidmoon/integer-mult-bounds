"""Generate the exact eigenbasis certificate; normal replay does not call this.

Jerry Chen (@CubeJerry), with OpenAI Codex assistance. Apache-2.0.
"""
from fractions import Fraction
from functools import reduce
from math import gcd, lcm
import argparse
import json
from pathlib import Path

from geometry import (FIRST, SECOND, SIZE, SPECTRUM, WEIGHTS, coordinates,
                      energy_matrix, load_ports, need, package_path)


def nullspace(matrix):
    rows = [list(map(Fraction, row)) for row in matrix]
    pivots = []
    for column in range(SIZE):
        rank = len(pivots)
        pivot = next((i for i in range(rank, SIZE) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        divisor = rows[rank][column]
        rows[rank] = [value / divisor for value in rows[rank]]
        for i in range(SIZE):
            if i != rank and rows[i][column]:
                multiplier = rows[i][column]
                rows[i] = [x - multiplier * y
                           for x, y in zip(rows[i], rows[rank], strict=True)]
        pivots.append(column)
    result = []
    for free in (i for i in range(SIZE) if i not in pivots):
        vector = [Fraction(0)] * SIZE
        vector[free] = Fraction(1)
        for i, pivot in enumerate(pivots):
            vector[pivot] = -rows[i][free]
        denominator = lcm(*(value.denominator for value in vector))
        integers = [int(value * denominator) for value in vector]
        content = reduce(gcd, integers)
        first = next(value for value in integers if value)
        result.append([value // content * (1 if first > 0 else -1)
                       for value in integers])
    return result


def generate():
    package = package_path()
    ports = load_ports(package)
    matrix, _ = energy_matrix(ports, coordinates())
    blocks = []
    for value, multiplicity in SPECTRUM:
        shifted = [[matrix[i][j] - value * WEIGHTS[i] * int(i == j)
                    for j in range(SIZE)] for i in range(SIZE)]
        basis = nullspace(shifted)
        need(len(basis) == multiplicity, "GENERATED_MULTIPLICITY")
        blocks.append({"eigenvalue_times_16": value, "basis": basis})
    return {"schema": "p104-selected-metric-spectrum/1",
            "coordinate_frame": list(FIRST), "second_deleted_frame": list(SECOND),
            "energy_convention": "unordered orthogonal unit-root pairs",
            "blocks": blocks}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(generate(), stream, indent=2)
        stream.write("\n")


if __name__ == "__main__":
    main()
