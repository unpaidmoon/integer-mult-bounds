"""Check a complete exact spectral certificate for selected P104 geometry.

Jerry Chen (@CubeJerry), with OpenAI Codex assistance. Apache-2.0.
This checker imports neither the generator nor any predecessor executable.
"""
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
import json

from geometry import (DIM, FIRST, SECOND, SIZE, SOURCE, SPECTRUM, WEIGHTS,
                      authenticate, bilinear, checked_ports, coordinates, dot,
                      energy_matrix, linear_form, load_ports, matrix_from_entries, need,
                      package_path)


def modular_rank(columns, prime=1009):
    """An invertible reduction proves rational independence; no converse used."""
    rows = [[column[i] % prime for column in columns] for i in range(SIZE)]
    rank = 0
    for j in range(len(columns)):
        pivot = next((i for i in range(rank, SIZE) if rows[i][j]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][j], -1, prime)
        rows[rank] = [x * inverse % prime for x in rows[rank]]
        for i in range(rank + 1, SIZE):
            factor = rows[i][j]
            rows[i] = [(x - factor * y) % prime
                       for x, y in zip(rows[i], rows[rank], strict=True)]
        rank += 1
        if rank == SIZE:
            break
    return rank


def check_certificate(certificate, matrix, weights=WEIGHTS):
    need(certificate.get("schema") == "p104-selected-metric-spectrum/1", "SCHEMA")
    need(certificate.get("coordinate_frame") == list(FIRST), "COORDINATE_FRAME")
    need(certificate.get("second_deleted_frame") == list(SECOND), "SECOND_FRAME")
    need(certificate.get("energy_convention") ==
         "unordered orthogonal unit-root pairs", "ENERGY_CONVENTION")
    blocks = certificate.get("blocks")
    need(isinstance(blocks, list) and len(blocks) == len(SPECTRUM), "BLOCK_COUNT")
    columns, equality = [], []
    for block, (mu, count) in zip(blocks, SPECTRUM, strict=True):
        need(type(block.get("eigenvalue_times_16")) is int and
             block["eigenvalue_times_16"] == mu, "EIGENVALUE")
        basis = block.get("basis")
        need(isinstance(basis, list) and len(basis) == count, "MULTIPLICITY")
        for vector in basis:
            need(isinstance(vector, list) and len(vector) == SIZE and
                 all(type(x) is int and abs(x) <= 1000 for x in vector), "VECTOR")
            for i in range(SIZE):
                need(dot(matrix[i], vector) == mu * weights[i] * vector[i],
                     "EIGENVECTOR_EQUATION")
            need(mu == 0 or sum(vector[:DIM]) == 0, "POSITIVE_TRACE_ZERO")
            need(mu != 0 or vector == [1] * DIM + [0] * (SIZE - DIM),
                 "SCALAR_KERNEL")
            columns.append(vector)
        if mu == 600:
            equality = basis
    need(len(columns) == SIZE and modular_rank(columns) == SIZE, "BASIS_COMPLETE")
    return equality


def check_attainers(equality, vectors, edges):
    for vector in equality:
        matrix = matrix_from_entries(vector)
        need(sum(matrix[i][i] for i in range(DIM)) == 0, "ATTAINER_TRACE")
        need(sum(x * x for row in matrix for x in row) == 8, "ATTAINER_NORM")
        for i in range(DIM):
            for j in range(DIM):
                need(sum(matrix[i][k] * matrix[k][j] for k in range(DIM))
                     == int(i == j), "ATTAINER_INVOLUTION")
        direct = sum(bilinear(vectors[q], matrix, vectors[r]) ** 2
                     for q, r in edges)
        need(direct == 4800, "ATTAINER_ENERGY")
    need(all(dot([w * x for w, x in zip(WEIGHTS, a, strict=True)], b) == 0
             for i, a in enumerate(equality) for b in equality[i + 1:]),
         "EQUALITY_ORTHOGONAL_BASIS")


def rejected(call, expected):
    try:
        call()
    except ValueError as error:
        need(str(error) == expected, "WRONG_CONTROL_FAILURE")
        return
    raise ValueError("CONTROL_ACCEPTED:" + expected)


def controls(certificate, matrix, ports, vectors, edges, equality):
    altered = deepcopy(certificate)
    altered["blocks"][1]["eigenvalue_times_16"] += 1
    rejected(lambda: check_certificate(altered, matrix), "EIGENVALUE")
    altered = deepcopy(certificate)
    altered["blocks"][1]["basis"][0][0] += 1
    rejected(lambda: check_certificate(altered, matrix), "EIGENVECTOR_EQUATION")
    altered = deepcopy(certificate)
    altered["blocks"][1]["basis"].pop()
    rejected(lambda: check_certificate(altered, matrix), "MULTIPLICITY")
    altered = deepcopy(certificate)
    altered["blocks"][1]["basis"][1] = altered["blocks"][1]["basis"][0]
    rejected(lambda: check_certificate(altered, matrix), "BASIS_COMPLETE")
    damaged = [row[:] for row in matrix]
    damaged[0][0] += 1
    rejected(lambda: check_certificate(certificate, damaged), "EIGENVECTOR_EQUATION")
    form = linear_form(vectors[edges[0][0]], vectors[edges[0][1]])
    omitted = [[matrix[i][j] - form[i] * form[j]
                for j in range(SIZE)] for i in range(SIZE)]
    rejected(lambda: check_certificate(certificate, omitted), "EIGENVECTOR_EQUATION")
    doubled = [[2 * value for value in row] for row in matrix]
    rejected(lambda: check_certificate(certificate, doubled), "EIGENVECTOR_EQUATION")
    rejected(lambda: check_certificate(certificate, matrix, (1,) * SIZE),
             "EIGENVECTOR_EQUATION")
    repeated = list(ports)
    repeated[1] = repeated[0]
    rejected(lambda: checked_ports(repeated), "PORT_DUPLICATE")
    wrong = list(ports)
    wrong[0] = FIRST[0]
    rejected(lambda: checked_ports(wrong), "SELECTED_PUNCTURE")
    wrong_equality = deepcopy(equality)
    wrong_equality[0][0] = 1
    rejected(lambda: check_attainers(wrong_equality, vectors, edges), "ATTAINER_TRACE")
    rejected(lambda: authenticate(b"corrupt", sha256(b"source").hexdigest()),
             "SOURCE_SHA256")
    need(Fraction(300, 8) < Fraction(3751, 100), "STRONGER_CONSTANT_FAILS")
    return 13


def main():
    package = package_path()
    ports = load_ports(package)
    vectors = coordinates()
    matrix, edges = energy_matrix(ports, vectors)
    certificate = json.loads((package / "CERTIFICATE.json").read_bytes())
    equality = check_certificate(certificate, matrix)
    check_attainers(equality, vectors, edges)
    count = controls(certificate, matrix, ports, vectors, edges, equality)
    files = ("README.md", "PROOF.md", "TASK.json", "SOURCES.json", "VERIFY.json",
             "geometry.py", "generate.py", "verify.py", "CERTIFICATE.json")
    result = {"status": "PASS_P104_SELECTED_METRIC_ORBIT", "ports": len(ports),
              "unordered_orthogonal_pairs": len(edges), "sharp_constant": "75/2",
              "equality_dimension_trace_free": len(equality),
              "spectrum": {str(Fraction(mu, 16)): count for mu, count in SPECTRUM},
              "eigenvectors_checked": SIZE, "eigenvector_equations": SIZE * SIZE,
              "independence_modulus": 1009, "witness_norm_squared": 8,
              "witness_energy": 300, "negative_controls": count,
              "source_input": SOURCE,
              "file_sha256": {name: sha256((package / name).read_bytes()).hexdigest()
                              for name in files}}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
