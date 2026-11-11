"""Generate exact eigenbases for all three disjoint-frame orbit types.

Jerry Chen (@CubeJerry), with OpenAI Codex assistance. Apache-2.0.
Normal replay imports neither this generator nor its nullspace algorithm.
"""
import argparse
import json
from pathlib import Path

from generate import nullspace
from geometry import FIRST, SIZE, WEIGHTS, coordinates, energy_matrix, need, universe
from orbits import PERMUTATIONS, QUADRATIC, TYPES


def generate():
    vectors = coordinates()
    records = []
    for count, frame, spectrum in TYPES:
        ports = sorted(set(universe()) - set(FIRST) - set(frame))
        matrix, _ = energy_matrix(ports, vectors)
        blocks = []
        for value, multiplicity in spectrum:
            shifted = [[matrix[i][j] - value * WEIGHTS[i] * int(i == j)
                        for j in range(SIZE)] for i in range(SIZE)]
            basis = nullspace(shifted)
            need(len(basis) == multiplicity, "GENERATED_MULTIPLICITY")
            blocks.append({"eigenvalue_times_16": value, "basis": basis})
        record = {"size": count, "representative": list(frame), "blocks": blocks}
        if count == 336:
            need(all(matrix[i][j] % WEIGHTS[i] == 0 for i in range(SIZE)
                     for j in range(SIZE)), "INTEGER_OPERATOR")
            operator = [[matrix[i][j] // WEIGHTS[i] for j in range(SIZE)]
                        for i in range(SIZE)]
            polynomial = [[sum(operator[i][k] * operator[k][j] for k in range(SIZE))
                           + QUADRATIC[1] * operator[i][j]
                           + QUADRATIC[2] * int(i == j)
                           for j in range(SIZE)] for i in range(SIZE)]
            basis = nullspace(polynomial)
            need(len(basis) == 4, "GENERATED_QUADRATIC_DIMENSION")
            record["quadratic_block"] = {"polynomial": list(QUADRATIC), "basis": basis}
        records.append(record)
    return {"schema": "p104-disjoint-frame-orbits/1",
            "coordinate_frame": list(FIRST),
            "coordinate_permutations": [list(p) for p in PERMUTATIONS],
            "sign_flips": list(range(8)), "orbits": records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(generate(), stream, indent=2)
        stream.write("\n")


if __name__ == "__main__":
    main()
