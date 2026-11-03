#!/usr/bin/env python3
"""Exact finite checks of the constructive, all-field support-stability proof.

Jerry Chen (@CubeJerry), with OpenAI Codex assistance. Apache-2.0.
"""

from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from io import BytesIO
from itertools import combinations, permutations, product
import gzip
import json
from pathlib import Path
from runpy import run_path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[1]
SOURCE = "research/p104-helper-subspace-splits/WORD.json.gz"
LIMIT = 8 * 1024 * 1024
API = run_path(str(PACKAGE / "stability.py"))
construct = API["construct"]
check = API["validate_certificate"]
normalize = API["normalized"]
blocks = API["block_form"]
require = API["require"]


def identity(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def binary_rank(matrix):
    """Independent XOR basis, with no scalar-field elimination calls."""
    basis = {}
    for row in matrix:
        word = sum((x & 1) << j for j, x in enumerate(row))
        while word:
            bit = word.bit_length() - 1
            if bit in basis:
                word ^= basis[bit]
            else:
                basis[bit] = word
                break
    return len(basis)


def determinant(matrix):
    value, n = 0, len(matrix)
    for order in permutations(range(n)):
        inversions = sum(order[i] > order[j] for i in range(n) for j in range(i + 1, n))
        term = (-1) ** inversions
        for i, j in enumerate(order):
            term *= matrix[i][j]
        value += term
    return value


def minor_rank(matrix, prime):
    n = len(matrix)
    require(n <= 3, "minor oracle size")
    for size in range(n, 0, -1):
        for rows in combinations(range(n), size):
            for columns in combinations(range(n), size):
                if determinant([[matrix[i][j] for j in columns] for i in rows]) % prime:
                    return size
    return 0


def deletion_distance(matrix, prime):
    """Exhaustive principal-subset oracle, independent of the constructor."""
    n = len(matrix)
    require(n <= 4, "distance oracle size")
    matrix = normalize(matrix, prime)
    for size in range(n + 1):
        for deleted in combinations(range(n), size):
            keep = set(range(n)) - set(deleted)
            valid = True
            for i in keep:
                neighbors = [j for j in keep if i != j and (matrix[i][j] or matrix[j][i])]
                if len(neighbors) > 1:
                    valid = False
                    break
                if neighbors:
                    j = neighbors[0]
                    if matrix[i][j] * matrix[j][i] % prime != 1:
                        valid = False
                        break
            if valid:
                return size
    raise ValueError("distance oracle failed")


def check_case(matrix, prime, oracle=True):
    cert = construct(matrix, prime)
    require(check(matrix, cert, prime), "certificate rejected")
    if oracle:
        alternate = binary_rank(matrix) if prime == 2 else minor_rank(matrix, prime)
        require(alternate == cert["rank"], "independent rank")
    if len(matrix) <= 4:
        distance = deletion_distance(matrix, prime)
        require(distance <= len(cert["deleted"]) <= 2 * cert["excess"], "distance bound")
        require((distance == 0) == (cert["excess"] == 0), "equality rigidity")
    return cert


def finite_domains():
    counts, tight = {}, 0
    for prime, maximum in ((2, 4), (3, 3)):
        count = 0
        for n in range(1, maximum + 1):
            positions = [(i, j) for i in range(n) for j in range(n) if i != j]
            for values in product(range(prime), repeat=len(positions)):
                matrix = identity(n)
                for (i, j), value in zip(positions, values):
                    matrix[i][j] = value
                cert = check_case(matrix, prime)
                tight += (cert["excess"] > 0 and deletion_distance(matrix, prime)
                          == 2 * cert["excess"])
                count += 1
        counts[f"all_F{prime}_through_{maximum}"] = count
    count, n = 0, 5
    positions = [(i, j) for i in range(n) for j in range(n) if i != j]
    for support_size in range(6):
        for support in combinations(positions, support_size):
            matrix = identity(n)
            for i, j in support:
                matrix[i][j] = 1
            check_case(matrix, 2)
            count += 1
    counts["F2_dimension_5_support_at_most_5"] = count
    counts["positive_excess_tight_small_cases"] = tight
    return counts


def weighted_cycles():
    count = 0
    for n in range(2, 10):
        for prime in (None, 2, 3, 5, 7):
            modes = ("acyclic", "singular") if prime == 2 else ("acyclic", "singular", "nonsingular")
            for mode in modes:
                matrix, weight = identity(n), Fraction(1)
                for i in range(n - 1):
                    value = 1 if prime is not None else Fraction((-1) ** i * (i + 2), i + 3)
                    matrix[i][i + 1] = value
                    weight *= value
                closing = (-1) ** n / weight
                if mode == "acyclic":
                    closing = 0  # Acyclic control, including characteristic two.
                elif mode == "nonsingular":
                    closing *= 2
                matrix[n - 1][0] = closing
                cert = construct(matrix, prime)
                require(check(matrix, cert, prime), "weighted certificate")
                require(cert["rank"] == n - int(mode == "singular"), "weighted cycle rank")
                count += 1
    return count


def authenticate(raw, expected):
    require(len(raw) <= LIMIT and sha256(raw).hexdigest() == expected, "source hash")
    with gzip.GzipFile(fileobj=BytesIO(raw)) as stream:
        payload = stream.read(LIMIT + 1)
    require(len(payload) <= LIMIT, "source expansion")
    ports = json.loads(payload)["ports"]
    require(type(ports) is list and len(ports) == 104 and len(set(ports)) == 104,
            "port inventory")
    require(all(type(x) is int and 0 < x < 512 and x.bit_count() % 2 for x in ports),
            "port domain")
    return ports


def p104_fixture():
    manifest = json.loads((PACKAGE / "SOURCES.json").read_text())
    pins = [row for row in manifest["files"] if row["path"] == SOURCE and row["usage"] == "input"]
    require(len(pins) == 1, "source manifest")
    raw = (ROOT / SOURCE).read_bytes()
    ports = authenticate(raw, pins[0]["sha256"])
    orthogonal = lambda i, j: (ports[i] & ports[j]).bit_count() % 2 == 0
    triangle = [0, 1, 2]
    require(all(orthogonal(i, j) for i, j in combinations(triangle, 2)), "triangle mask")
    remaining, pairs = set(range(3, 104)), []
    while remaining and len(pairs) < 47:
        i = min(remaining)
        remaining.remove(i)
        j = next((j for j in sorted(remaining) if orthogonal(i, j)), None)
        require(j is not None, "greedy matching failed")
        remaining.remove(j)
        pairs.append([i, j])
    require(len(pairs) == 47 and len(remaining) == 7, "P104 block counts")
    matrix = identity(104)
    matrix[0][1] = matrix[1][2] = 1
    matrix[2][0] = -1
    for i, j in pairs:
        matrix[i][j] = matrix[j][i] = 1
    require(all(i == j or not matrix[i][j] or orthogonal(i, j)
                for i in range(104) for j in range(104)), "P104 allowed mask")
    certificates = []
    for prime in (None, 2, 3, 5, 7):
        cert = construct(matrix, prime)
        require(check(matrix, cert, prime), "P104 certificate")
        require((cert["rank"], cert["support"], cert["excess"]) == (56, 97, 1),
                "P104 arithmetic")
        require(cert["deleted"] == [1, 2], "P104 attaining deletion")
        certificates.append(cert)
    # No single deletion can destroy both remaining triangle arcs. Inspect all
    # 104 choices directly; no graph-generator theorem is used for this control.
    for gone in range(104):
        try:
            blocks(normalize(matrix), set(range(104)) - {gone})
        except ValueError:
            pass
        else:
            raise ValueError("P104 nonsharp witness")
    witness = {"triangle": triangle, "triangle_weights": [1, 1, -1],
               "pairs": pairs, "singletons": sorted(remaining),
               "certificates": certificates}
    return matrix, witness, raw, pins[0]["sha256"]


def negative_controls(matrix, raw, source_hash):
    base = construct(matrix, 3)
    mutations = [
        ("accounting fields", lambda c: c.update(rank=55)),
        ("accounting fields", lambda c: c.update(excess=0)),
        ("residual partition", lambda c: c["cycles"].pop()),
        ("cycle edge", lambda c: c["cycles"][0].reverse()),
        ("deleted set", lambda c: c["deleted"].append(c["deleted"][0])),
        ("residual is not a reciprocal block sum", lambda c: c.update(deleted=[1])),
        ("block certificate", lambda c: c["singletons"].pop()),
        ("field tag", lambda c: c.update(field="F2")),
    ]
    count = 0
    for message, change in mutations:
        cert = deepcopy(base)
        change(cert)
        try:
            check(matrix, cert, 3)
        except ValueError as error:
            require(str(error) == message, "wrong rejection reason: " + str(error))
            count += 1
        else:
            raise ValueError("false certificate accepted")
    dense = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    cert = construct(dense, 3)
    require(cert["peeled"], "peel control missing")
    cert["peeled"][0][1] -= 1
    try:
        check(dense, cert, 3)
    except ValueError as error:
        require(str(error) == "peel degree", "peel rejection reason")
        count += 1
    else:
        raise ValueError("wrong peel degree accepted")
    for changed in (raw[:-1], raw[:-1] + bytes([raw[-1] ^ 1])):
        try:
            authenticate(changed, source_hash)
        except ValueError as error:
            require(str(error) == "source hash", "source rejection reason")
            count += 1
        else:
            raise ValueError("changed source accepted")
    for bad, prime, message in (([[0]], None, "unit diagonal"),
                                ([[1.0]], None, "exact entries"),
                                ([[1, Fraction(1, 3)], [0, 1]], 3, "field denominator")):
        try:
            construct(bad, prime)
        except ValueError as error:
            require(str(error) == message, "input rejection reason")
            count += 1
        else:
            raise ValueError("invalid matrix accepted")
    return count


def main():
    census = finite_domains()
    weighted = weighted_cycles()
    matrix, witness, raw, source_hash = p104_fixture()
    controls = negative_controls(matrix, raw, source_hash)
    files = ("README.md", "PROOF.md", "TASK.json", "SOURCES.json", "VERIFY.json",
             "stability.py", "verify.py")
    receipt = {"claim_type": "scoped all-field proof with exact finite corroboration",
               "census": census, "weighted_cycle_cases": weighted,
               "rejection_controls": controls, "P104": witness,
               "source_sha256": source_hash,
               "package_sha256": {name: sha256((PACKAGE / name).read_bytes()).hexdigest()
                                  for name in files}}
    print(json.dumps(receipt, sort_keys=True))
    print("PASS_P104_SUPPORT_STABILITY")


if __name__ == "__main__":
    main()
