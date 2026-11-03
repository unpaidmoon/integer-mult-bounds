"""Selected P104 energy, derived from its source port labels. Apache-2.0.

Jerry Chen (@CubeJerry), with OpenAI Codex assistance.
The A8 root convention and selected ports retain Matarener/DreamingOfClouds/
Ali Romman and the P104 lineage's credit. No predecessor executable is imported.
"""
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import gzip
import json

DIM = 8
PAIRS = tuple(combinations(range(DIM), 2))
SIZE = DIM + len(PAIRS)
WEIGHTS = (1,) * DIM + (2,) * len(PAIRS)
FIRST = (7, 25, 42, 52, 76, 82, 97, 127)
SECOND = (67, 104, 137, 162, 266, 289, 448, 491)
SOURCE = "research/p104-helper470-twin-rung-removal/WORD.json.gz"
SPECTRUM = ((0, 1), (600, 6), (604, 8), (608, 7),
            (660, 4), (728, 6), (796, 4))  # sixteen times each eigenvalue


def need(condition, message):
    if not condition:
        raise ValueError(message)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b, strict=True))


def universe():
    triples = [sum(1 << i for i in indices)
               for indices in combinations(range(9), 3)]
    differences = [511 ^ (1 << i) ^ (1 << j)
                   for i, j in combinations(range(9), 2)]
    return tuple(sorted(triples + differences))


def root_times_three(label):
    """Nine coordinates: 3*(indicator(T)-ones/3), or 3*(e_i-e_j)."""
    need(type(label) is int and label in universe(), "ROOT_LABEL")
    if label.bit_count() == 3:
        return tuple(2 if (label >> i) & 1 else -1 for i in range(9))
    i, j = (i for i in range(9) if not (label >> i) & 1)
    return tuple(3 * (int(k == i) - int(k == j)) for k in range(9))


def checked_ports(ports):
    need(isinstance(ports, list) and len(ports) == 104, "PORT_COUNT")
    need(all(type(q) is int and q in universe() for q in ports), "PORT_LABEL")
    need(len(set(ports)) == 104, "PORT_DUPLICATE")
    need(set(universe()) - set(ports) == set(FIRST + SECOND), "SELECTED_PUNCTURE")
    return tuple(ports)


def authenticate(raw, expected):
    need(sha256(raw).hexdigest() == expected, "SOURCE_SHA256")


def load_ports(package):
    manifest = json.loads((package / "SOURCES.json").read_bytes())
    pins = [row for row in manifest["files"] if row["path"] == SOURCE]
    need(len(pins) == 1 and pins[0]["usage"] == "input", "SOURCE_PIN")
    raw = (package.parents[1] / SOURCE).read_bytes()
    authenticate(raw, pins[0]["sha256"])
    word = json.loads(gzip.decompress(raw))
    return checked_ports(word["ports"])


def coordinates():
    """Return 2u in the orthonormal FIRST-frame basis, entirely over Z."""
    roots = {q: root_times_three(q) for q in universe()}
    for frame in (FIRST, SECOND):
        need(len(frame) == len(set(frame)) == DIM, "FRAME_SIZE")
        need(all(dot(roots[a], roots[b]) == 18 * int(a == b)
                 for a in frame for b in frame), "FRAME_ORTHOGONAL")
    result = {}
    for q, row in roots.items():
        products = tuple(dot(roots[a], row) for a in FIRST)
        need(all(value % 9 == 0 for value in products), "INTEGRAL_CHART")
        result[q] = tuple(value // 9 for value in products)
    for q in universe():
        need(sum(roots[q]) == 0 and dot(roots[q], roots[q]) == 18,
             "A8_ROOT_NORM")
        need(dot(result[q], result[q]) == 4, "UNIT_ROOT_NORM")
        for r in universe():
            need(9 * dot(result[q], result[r]) == 2 * dot(roots[q], roots[r]),
                 "GRAM_ISOMETRY")
    return result


def linear_form(left, right):
    return tuple(left[i] * right[i] for i in range(DIM)) + tuple(
        left[i] * right[j] + left[j] * right[i] for i, j in PAIRS)


def energy_matrix(ports, vectors):
    """H with E(A)=a^T H a/16; a lists diagonal then upper entries."""
    matrix = [[0] * SIZE for _ in range(SIZE)]
    edges = []
    for q, r in combinations(ports, 2):
        if dot(vectors[q], vectors[r]) != 0:
            continue
        edges.append((q, r))
        row = linear_form(vectors[q], vectors[r])
        sparse = [(i, value) for i, value in enumerate(row) if value]
        for i, left in sparse:
            for j, right in sparse:
                matrix[i][j] += left * right
    need(len(edges) == 2860, "SELECTED_EDGE_COUNT")
    return matrix, tuple(edges)


def matrix_from_entries(entries):
    need(len(entries) == SIZE, "ENTRY_COUNT")
    matrix = [[0] * DIM for _ in range(DIM)]
    for i in range(DIM):
        matrix[i][i] = entries[i]
    for (i, j), value in zip(PAIRS, entries[DIM:], strict=True):
        matrix[i][j] = matrix[j][i] = value
    return matrix


def bilinear(left, matrix, right):
    return sum(left[i] * matrix[i][j] * right[j]
               for i in range(DIM) for j in range(DIM))


def package_path():
    return Path(__file__).resolve().parent
