#!/usr/bin/env python3
"""Exact finite corroboration of rational-width all-column certificates."""

from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from math import comb
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def matrix(rows):
    return tuple(tuple(F(x) for x in row) for row in rows)


def eye(n):
    return matrix([[int(i == j) for j in range(n)] for i in range(n)])


def mul(a, b):
    require(len(a[0]) == len(b), "matrix product shape")
    return tuple(tuple(sum(x * y for x, y in zip(row, col))
                       for col in zip(*b)) for row in a)


def kron(a, b):
    return tuple(tuple(x * y for x in ar for y in br) for ar in a for br in b)


def diagonal(blocks):
    n = sum(len(b) for b in blocks)
    out = [[F(0) for _ in range(n)] for _ in range(n)]
    offset = 0
    for block in blocks:
        for i, row in enumerate(block):
            out[offset + i][offset:offset + len(row)] = row
        offset += len(block)
    return matrix(out)


def trim(p):
    out = list(map(F, p))
    for _ in range(len(out)):
        if len(out) <= 1 or out[-1]:
            break
        out.pop()
    return tuple(out)


def peval(p, n):
    value = F(0)
    for c in reversed(p):
        value = value * n + c
    return value


def pmul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return trim(out)


def divide(a, b):
    a, b = list(trim(a)), trim(b)
    require(b != (0,) and len(a) >= len(b), "not a common denominator")
    out = [F(0)] * (len(a) - len(b) + 1)
    for k in range(len(out) - 1, -1, -1):
        out[k] = a[k + len(b) - 1] / b[-1]
        for j, c in enumerate(b):
            a[k + j] -= out[k] * c
    require(not any(a), "not a common denominator")
    return trim(out)


def counter(p):
    """Return J,e_0,a with e_0 J^f a = p(f), using forward differences."""
    p = trim(p)
    differences = [peval(p, n) for n in range(len(p))]
    coefficients = []
    for _ in range(len(p)):
        coefficients.append(differences[0])
        differences = [y - x for x, y in zip(differences, differences[1:])]
    j = matrix([[int(c == r or c == r + 1) for c in range(len(p))]
                for r in range(len(p))])
    return j, matrix([[1] + [0] * (len(p) - 1)]), matrix([[a] for a in coefficients])


def validate(terms, common):
    require(1 <= len(terms) <= 4, "term capacity")
    require(1 <= len(common) <= 17, "denominator degree capacity")
    # This sufficient executable guard is stricter than the theorem hypothesis.
    require(all(c >= 0 for c in common) and any(common), "positive-width pole guard")
    outputs, inputs, symbols = len(terms[0][0]), len(terms[0][2][0]), len(terms[0][1])
    require(1 <= outputs <= 3 and 1 <= inputs <= 3 and 1 <= symbols <= 4, "boundary capacity")
    for left, transitions, right, p, q in terms:
        d = len(right)
        require(1 <= d <= 4 and 1 <= len(p) <= 17 and 1 <= len(q) <= 17, "term size")
        require(len(left) == outputs and all(len(row) == d for row in left), "left shape")
        require(all(len(row) == inputs for row in right), "right shape")
        require(len(transitions) == symbols, "symbol coverage")
        require(all(len(t) == d and all(len(row) == d for row in t)
                    for t in transitions), "transition shape")
        require(all(c >= 0 for c in q) and any(q), "positive-width pole guard")


def lift(terms, common):
    validate(terms, common)
    pieces = []
    for left, transitions, right, p, q in terms:
        c = pmul(p, divide(common, q))
        if c != (0,):
            j, u, v = counter(c)
            pieces.append((kron(left, u), tuple(kron(t, j) for t in transitions), kron(right, v)))
    require(pieces, "identically zero coefficient list")
    require(sum(len(piece[2]) for piece in pieces) <= 64, "lifted state capacity")
    left = tuple(tuple(x for piece in pieces for x in piece[0][r])
                 for r in range(len(pieces[0][0])))
    transitions = tuple(diagonal([piece[1][s] for piece in pieces])
                        for s in range(len(pieces[0][1])))
    right = tuple(row for piece in pieces for row in piece[2])
    return left, transitions, right


def endpoint(table, word):
    left, transitions, right = table
    value = left
    for s in word:
        value = mul(value, transitions[s])
    return mul(value, right)


def literal(terms, word):
    """Scalar path oracle, without matrix multiplication or polynomial counters."""
    require(1 <= len(word) <= 6, "literal width capacity")
    out = [[F(0) for _ in terms[0][2][0]] for _ in terms[0][0]]
    for left, transitions, right, p, q in terms:
        coefficient = peval(p, len(word)) / peval(q, len(word))
        for path in product(range(len(right)), repeat=len(word) + 1):
            weight = coefficient
            for k, s in enumerate(word):
                weight *= transitions[s][path[k]][path[k + 1]]
            for r in range(len(out)):
                for c in range(len(out[0])):
                    out[r][c] += left[r][path[0]] * weight * right[path[-1]][c]
    return matrix(out)


def add_basis(row, basis):
    reduced = list(row)
    for pivot, old in basis:
        coefficient = reduced[pivot]
        reduced = [x - coefficient * y for x, y in zip(reduced, old)]
    pivot = next((i for i, x in enumerate(reduced) if x), None)
    if pivot is None:
        return False
    divisor = reduced[pivot]
    basis.append((pivot, tuple(x / divisor for x in reduced)))
    return True


def certify(table):
    left, transitions, right = table
    n = len(right)
    echelon, reached = [], []
    for generation in range(n + 1):
        if generation and generation > len(reached):
            break
        candidates = ([(row, (), r) for r, row in enumerate(left)] if generation == 0
                      else [reached[generation - 1]])
        for row, word, role in candidates:
            for s, transition in enumerate(transitions):
                new = mul((row,), transition)[0]
                extended = word + (s,)
                values = mul((new,), right)[0]
                if any(values):
                    c = next(i for i, value in enumerate(values) if value)
                    require(len(extended) <= n, "witness cutoff")
                    return {"zero": False, "word": extended, "output": role,
                            "input": c, "value": values[c]}
                if add_basis(new, echelon):
                    reached.append((new, extended, role))
        require(len(reached) <= n, "reachable dimension")
    return {"zero": True, "rows": tuple(row for row, _, _ in reached)}


def rank(rows, width):
    """Column-oriented elimination for the separately transcribed checker."""
    a = [list(row) for row in rows]
    pivot = 0
    for col in range(width):
        candidate = next((r for r in range(pivot, len(a)) if a[r][col]), None)
        if candidate is None:
            continue
        a[pivot], a[candidate] = a[candidate], a[pivot]
        divisor = a[pivot][col]
        a[pivot] = [x / divisor for x in a[pivot]]
        for r in range(pivot + 1, len(a)):
            coefficient = a[r][col]
            a[r] = [x - coefficient * y for x, y in zip(a[r], a[pivot])]
        pivot += 1
    return pivot


def check_certificate(table, certificate):
    left, transitions, right = table
    n = len(right)
    if not certificate["zero"]:
        word = certificate["word"]
        require(1 <= len(word) <= n, "witness length")
        value = endpoint(table, word)[certificate["output"]][certificate["input"]]
        require(value == certificate["value"] and value != 0, "false witness")
        return
    rows = certificate["rows"]
    require(len(rows) <= n and all(len(row) == n for row in rows), "certificate size")
    require(not rows or not any(x for row in mul(rows, right) for x in row), "return annihilation")
    dimension = rank(rows, n)
    for row in left + rows:
        for transition in transitions:
            new = mul((row,), transition)[0]
            require(rank(rows + (new,), n) == dimension, "missing closure")


def sharp_tests():
    records = []
    for states in range(1, 5):
        for degree in range(4):
            n = states * (degree + 1)
            p = (F(1),)
            for k in range(1, degree + 1):
                p = pmul(p, (F(-k * states), F(1)))
            transition = matrix([[int(j == (i + 1) % states) for j in range(states)]
                                 for i in range(states)])
            left = matrix([[1] + [0] * (states - 1)])
            right = matrix([[int(i == 0)] for i in range(states)])
            terms = ((left, (transition,), right, p, (0, 1)),)
            require(len(p) == degree + 1 and p[-1] == 1, "sharp degree")
            table = lift(terms, (0, 1))
            certificate = certify(table)
            check_certificate(table, certificate)
            require(not certificate["zero"] and len(certificate["word"]) == n, "sharp first failure")
            for width in range(1, n + 4):
                direct = (peval(p, width) / width if width % states == 0 else 0)
                require(endpoint(table, (0,) * width)[0][0] == width * direct, "sharp clearing")
                if width <= n:
                    require((direct != 0) == (width == n), "sharp cycle suppression")
            records.append({"states": states, "degree": degree, "cutoff": n})
    return records


def physical_tests():
    transitions = tuple(matrix(t) for t in [[[1, 1], [0, 1]], [[0, 1], [1, 0]],
                                           [[-1, 0], [1, 1]], [[1, 0], [0, -1]]])
    left, right = eye(2), matrix([[1, 0, 2], [0, 1, -1]])
    s, inverse = matrix([[1, 1], [0, 1]]), matrix([[1, -1], [0, 1]])
    changed = tuple(mul(mul(inverse, t), s) for t in transitions)
    first = (left, transitions, right, (1,), (0, 1))
    second = (mul(left, s), changed, mul(inverse, right), (-1, -1), (0, 1, 1))
    terms = (first, second)
    table = lift(terms, (0, 1, 1))
    certificate = certify(table)
    require(certificate["zero"], "rational gauge cancellation")
    check_certificate(table, certificate)
    checked = 0
    for width in range(1, 5):
        for word in product(range(4), repeat=width):
            require(endpoint(table, word) == literal(terms, word), "literal zero endpoint")
            raw = literal((first,), word)
            require(endpoint(lift((first,), (0, 1)), word)
                    == matrix([[width * x for x in row] for row in raw]), "nonzero clearing")
            checked += 2
    witness = certify(lift((first,), (0, 1)))
    check_certificate(lift((first,), (0, 1)), witness)
    require(not witness["zero"], "complete dirty residual")
    return checked, table, certificate


def counter_tests():
    count = 0
    for degree in range(9):
        p = tuple(F((-1) ** k * (k + 1), k + 2) for k in range(degree + 1))
        j, left, right = counter(p)
        for width in range(25):
            value = endpoint((left, (j,), right), (0,) * width)[0][0]
            require(value == peval(p, width), "polynomial counter")
            require(value == sum(comb(width, k) * right[k][0]
                                 for k in range(min(degree, width) + 1)), "binomial expansion")
            count += 1
    residues = 0
    for order in range(13):
        polynomials = []
        for k in range(order + 1):
            p = (F(1),)
            for h in range(order + 1):
                if h != k:
                    p = pmul(p, (F(h), F(1)))
            polynomials.append(p)
        for j in range(order + 1):
            for k, p in enumerate(polynomials):
                require((peval(p, -j) != 0) == (j == k), "reciprocal pole independence")
                residues += 1
    return count, residues


def controls(table, certificate):
    count = 0
    simple = (matrix([[1]]), (matrix([[1]]),), matrix([[1]]), (1,), (0, 1))
    invalid = [((simple,), (-1, 1)), ((simple,), (1,)), ((simple,), (0,)),
               ((), (0, 1)), ((simple,) * 5, (0, 1))]
    malformed = (matrix([[1, 0]]), simple[1], simple[2], (1,), (0, 1))
    invalid.append(((malformed,), (0, 1)))
    for terms, common in invalid:
        try:
            lift(terms, common)
        except ValueError:
            count += 1
        else:
            raise ValueError("invalid input accepted")
    bad_certificates = [dict(certificate, rows=()),
                        {"zero": False, "word": (), "output": 0, "input": 0, "value": 1},
                        {"zero": False, "word": (0,), "output": 0, "input": 0, "value": 1}]
    for bad in bad_certificates:
        try:
            check_certificate(table, bad)
        except ValueError:
            count += 1
        else:
            raise ValueError("false certificate accepted")
    require(endpoint(lift((simple,), (0, 1)), (0, 0))[0][0] == 1, "cleared reciprocal")
    require(literal((simple,), (0, 0))[0][0] == F(1, 2), "exterior coefficient")
    return count + 1


def main():
    sharp = sharp_tests()
    physical, table, certificate = physical_tests()
    counters, residues = counter_tests()
    rejected = controls(table, certificate)
    root = Path(__file__).resolve().parent
    files = sorted(p for p in root.iterdir() if p.is_file())
    require(len(files) <= 10 and all(p.stat().st_size <= 1_048_576 for p in files), "receipt capacity")
    receipt = {"sharp_cases": sharp, "physical_words": physical, "counter_values": counters,
               "reciprocal_residue_entries": residues, "controls": rejected,
               "sha256": {p.name: sha256(p.read_bytes()).hexdigest() for p in files}}
    print("PASS_RATIONAL_WIDTH_CERTIFICATES " + json.dumps(receipt, sort_keys=True))


if __name__ == "__main__":
    main()
