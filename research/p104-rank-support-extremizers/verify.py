#!/usr/bin/env python3
"""Exact finite corroboration of the written support/equality theorem."""

from fractions import Fraction
from hashlib import sha256
from io import BytesIO
from itertools import combinations, permutations, product
import gzip
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
SOURCE = "research/p104-helper-subspace-splits/WORD.json.gz"
MAX_N = 104
MAX_FILE = 8 * 1024 * 1024


def require(condition, message):
    if not condition:
        raise ValueError(message)


def bounded_bytes(path):
    with path.open("rb") as stream:
        data = stream.read(MAX_FILE + 1)
    require(len(data) <= MAX_FILE, "file size limit")
    return data


def validate(matrix):
    n = len(matrix)
    require(1 <= n <= MAX_N, "matrix dimension")
    require(all(len(row) == n for row in matrix), "square matrix")
    require(all(matrix[i][i] == 1 for i in range(n)), "unit diagonal")
    require(all(type(x) in (int, Fraction) for row in matrix for x in row),
            "exact entries")
    return n


def rank_mod(matrix, prime):
    n = validate(matrix)
    require(prime in (2, 3), "supported prime")
    require(all(type(x) is int for row in matrix for x in row), "integer entries")
    work = [[x % prime for x in row] for row in matrix]
    rank = 0
    for col in range(n):
        pivot = next((i for i in range(rank, n) if work[i][col]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][col], -1, prime)
        work[rank] = [x * inverse % prime for x in work[rank]]
        for i in range(rank + 1, n):
            coefficient = work[i][col]
            work[i] = [(x - coefficient * y) % prime
                       for x, y in zip(work[i], work[rank])]
        rank += 1
    return rank


def rank_rational(matrix):
    n = validate(matrix)
    work = [[Fraction(x) for x in row] for row in matrix]
    rank = 0
    for col in range(n):
        pivot = next((i for i in range(rank, n) if work[i][col]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        for i in range(rank + 1, n):
            if not work[i][col]:
                continue
            coefficient = work[i][col] / work[rank][col]
            work[i] = [x - coefficient * y
                       for x, y in zip(work[i], work[rank])]
        rank += 1
    return rank


def rank_binary(matrix):
    n = len(matrix)
    basis = [0] * n
    rank = 0
    for row in matrix:
        bits = sum((x & 1) << j for j, x in enumerate(row))
        for j in range(n - 1, -1, -1):
            if not bits & (1 << j):
                continue
            if basis[j]:
                bits ^= basis[j]
            else:
                basis[j] = bits
                rank += 1
                break
    return rank


def determinant_mod(matrix, prime):
    n = len(matrix)
    require(n <= 3, "minor oracle dimension")
    value = 0
    for order in permutations(range(n)):
        inversions = sum(order[i] > order[j]
                         for i in range(n) for j in range(i + 1, n))
        term = -1 if inversions % 2 else 1
        for i in range(n):
            term *= matrix[i][order[i]]
        value += term
    return value % prime


def rank_minors(matrix, prime):
    n = len(matrix)
    require(n <= 3, "minor oracle dimension")
    for size in range(n, 0, -1):
        for rows in combinations(range(n), size):
            for cols in combinations(range(n), size):
                minor = [[matrix[i][j] for j in cols] for i in rows]
                if determinant_mod(minor, prime):
                    return size
    return 0


def support(matrix):
    n = len(matrix)
    return [[j for j in range(n) if i != j and matrix[i][j]]
            for i in range(n)]


def equality_form(matrix, prime=None):
    neighbors = support(matrix)
    for i, row in enumerate(neighbors):
        if len(row) > 1:
            return False
        if not row:
            continue
        j = row[0]
        if neighbors[j] != [i]:
            return False
        coefficient = matrix[i][j] * matrix[j][i]
        if (coefficient % prime if prime else coefficient) != 1:
            return False
    return True


def finite_census(prime, max_n):
    require((prime, max_n) in ((2, 4), (3, 3)), "census domain")
    rows = []
    for n in range(1, max_n + 1):
        positions = [(i, j) for i in range(n) for j in range(n) if i != j]
        count, equality = 0, 0
        minima = {}
        for entries in product(range(prime), repeat=len(positions)):
            matrix = [[int(i == j) for j in range(n)] for i in range(n)]
            for (i, j), value in zip(positions, entries):
                matrix[i][j] = value
            rank = rank_mod(matrix, prime)
            oracle = rank_binary(matrix) if prime == 2 else rank_minors(matrix, prime)
            require(rank == oracle, "independent rank disagreement")
            degrees = [len(row) for row in support(matrix)]
            edges = sum(degrees)
            expectation = sum((Fraction(1, d + 1) for d in degrees), Fraction())
            require(rank >= expectation >= Fraction(2 * n - edges, 2), "rank bound")
            extremal = edges == 2 * (n - rank)
            require(extremal == equality_form(matrix, prime), "equality classification")
            equality += extremal
            minima[rank] = min(minima.get(rank, n * n), edges)
            count += 1
        for rank, edges in minima.items():
            if 2 * rank >= n:
                require(edges == 2 * (n - rank), "attained minimum")
        rows.append({"n": n, "matrices": count, "extremizers": equality,
                     "minimum_by_rank": minima})
    return rows


def load_ports():
    manifest = json.loads(bounded_bytes(PACKAGE / "SOURCES.json"))
    pins = [row for row in manifest["files"] if row["path"] == SOURCE]
    require(len(pins) == 1 and pins[0]["usage"] == "input", "source declaration")
    raw = bounded_bytes(PACKAGE.parents[1] / SOURCE)
    require(sha256(raw).hexdigest() == pins[0]["sha256"], "source SHA256")
    with gzip.GzipFile(fileobj=BytesIO(raw)) as stream:
        payload = stream.read(MAX_FILE + 1)
    require(len(payload) <= MAX_FILE, "decompressed size limit")
    ports = json.loads(payload)["ports"]
    require(len(ports) == 104 and len(set(ports)) == 104, "port count")
    require(all(type(x) is int and 0 < x < 512 and x.bit_count() % 2
                for x in ports), "odd nine-bit ports")
    return ports, sha256(raw).hexdigest()


def p104_matrix(ports, witness):
    pairs, singletons = witness["pairs"], witness["singletons"]
    require(len(pairs) == 48 and len(singletons) == 8, "block counts")
    require(all(type(pair) is list and len(pair) == 2 for pair in pairs), "pair shape")
    indices = [x for pair in pairs for x in pair] + singletons
    require(all(type(x) is int for x in indices), "integer indices")
    require(sorted(indices) == list(range(104)), "partition")
    matrix = [[int(i == j) for j in range(104)] for i in range(104)]
    for i, j in pairs:
        require(not (ports[i] & ports[j]).bit_count() % 2, "orthogonal pair")
        matrix[i][j] = matrix[j][i] = 1
    return matrix


def witness_checks(ports):
    witness = json.loads(bounded_bytes(PACKAGE / "WITNESS.json"))
    matrix = p104_matrix(ports, witness)
    require(rank_rational(matrix) == rank_mod(matrix, 2) == rank_mod(matrix, 3) == 56,
            "P104 witness rank")
    require(sum(map(len, support(matrix))) == 96 and equality_form(matrix),
            "P104 support/equality")
    require(all(i == j or not matrix[i][j] or not (ports[i] & ports[j]).bit_count() % 2
                for i in range(104) for j in range(104)), "P104 mask")
    weighted = [row[:] for row in matrix]
    for k, (i, j) in enumerate(witness["pairs"]):
        coefficient = Fraction((-1) ** k * (k + 2), k + 3)
        weighted[i][j], weighted[j][i] = coefficient, 1 / coefficient
    require(rank_rational(weighted) == 56 and equality_form(weighted), "weighted family")
    return matrix, witness


def rejection_controls(matrix, witness, ports):
    failures = 0
    for mode in range(7):
        try:
            if mode == 0:
                validate([[0]])
            elif mode == 1:
                validate([[1, 0]])
            elif mode == 2:
                validate([[1.0]])
            elif mode == 3:
                rank_mod([[1]], 5)
            elif mode == 4:
                bad = {"pairs": witness["pairs"][:-1], "singletons": witness["singletons"]}
                p104_matrix(ports, bad)
            elif mode == 5:
                bad = json.loads(json.dumps(witness))
                bad["pairs"][0][1] = bad["pairs"][0][0]
                p104_matrix(ports, bad)
            else:
                bad_ports = ports[:]
                i, j = witness["pairs"][0]
                bad_ports[j] = bad_ports[i]
                p104_matrix(bad_ports, witness)
        except ValueError:
            failures += 1
        else:
            raise ValueError("rejection control accepted")
    i, j = witness["pairs"][0]
    broken = [row[:] for row in matrix]
    broken[i][j] = 2
    require(rank_rational(broken) == 57 and not equality_form(broken), "wrong reciprocal")
    broken[i][j] = 0
    require(rank_rational(broken) == 57 and not equality_form(broken), "one-way edge")
    return failures + 2


def main():
    ports, source_hash = load_ports()
    matrix, witness = witness_checks(ports)
    census = {str(p): finite_census(p, n) for p, n in ((2, 4), (3, 3))}
    degree_cases = 0
    for n in range(1, MAX_N + 1):
        for degree in range(n):
            gap = Fraction(1, degree + 1) - 1 + Fraction(degree, 2)
            require(gap == Fraction(degree * (degree - 1), 2 * (degree + 1)), "degree identity")
            require(gap >= 0 and ((gap == 0) == (degree in (0, 1))), "degree equality")
            degree_cases += 1
    controls = rejection_controls(matrix, witness, ports)
    files = ("README.md", "PROOF.md", "TASK.json", "SOURCES.json", "VERIFY.json",
             "verify.py", "WITNESS.json")
    hashes = {name: sha256(bounded_bytes(PACKAGE / name)).hexdigest() for name in files}
    print(json.dumps({"claim_type": "scoped proof with exact finite corroboration",
                      "n": 104, "rank": 56, "NEED": 96, "pairs": 48, "singletons": 8,
                      "census": census, "degree_cases": degree_cases, "controls": controls,
                      "source_sha256": source_hash, "package_sha256": hashes}, sort_keys=True))
    print("PASS_P104_RANK_SUPPORT_EXTREMIZERS")


if __name__ == "__main__":
    main()
