"""Exact fixed-domain corroboration of the integer fanout tariff theorem."""

import hashlib
import itertools
import json
import platform
import sys
from fractions import Fraction
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
FILES = ("README.md", "PROOF.md", "TASK.json", "SOURCES.json", "VERIFY.json", "verify.py")
IDENTITY = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
DEMAND = ((1, 0, 5), (0, 1, 12), (0, 0, 1))
FORWARD = ((1, 0, 2), (0, 1, 2), (1, 0, 2))
INVERSE = tuple((i, j, -a) for i, j, a in reversed(FORWARD))
CONJUGATION = INVERSE + ((0, 2, 1),) + FORWARD
DIRECT = ((0, 2, 5), (1, 2, 12))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_bytes(path):
    require(path.is_file() and not path.is_symlink(), "missing regular input")
    require(path.stat().st_size <= 1024 * 1024, "input exceeds one MiB")
    return path.read_bytes()


def authenticate():
    source = json.loads(read_bytes(PACKAGE / "SOURCES.json"))
    live = [row for row in source["files"] if row["usage"] == "input"]
    require(len(live) == 1, "exactly one context input required")
    row = live[0]
    require(row["path"] == "research/noncommutative-two-row-tariff/README.md", "source path")
    payload = read_bytes(PACKAGE.parent.parent / row["path"])
    require(hashlib.sha256(payload).hexdigest() == row["sha256"], "source hash mismatch")
    return {name: hashlib.sha256(read_bytes(PACKAGE / name)).hexdigest() for name in FILES}


def operator(word):
    require(len(word) <= 8, "fixed checker word capacity")
    matrix = [list(row) for row in IDENTITY]
    for i, j, coefficient in word:
        require(type(i) is int and type(j) is int, "integer role indices")
        require(i in (0, 1) and j in (0, 1, 2) and i != j, "gate roles")
        require(type(coefficient) is int and abs(coefficient) <= 12, "checker coefficient capacity")
        matrix[i] = [x + coefficient * y for x, y in zip(matrix[i], matrix[j], strict=True)]
    return tuple(tuple(row) for row in matrix)


def multiply(left, right):
    return tuple(tuple(sum(left[i][k] * right[k][j] for k in range(3))
                       for j in range(3)) for i in range(3))


def execute(word, values):
    state = list(values)
    for i, j, coefficient in word:
        state[i] += coefficient * state[j]
    return tuple(state)


def check_attainers():
    forward, inverse = operator(FORWARD), operator(INVERSE)
    require(forward == ((5, 2, 0), (12, 5, 0), (0, 0, 1)), "attaining column")
    require(multiply(forward, inverse) == IDENTITY, "right inverse")
    require(multiply(inverse, forward) == IDENTITY, "left inverse")
    for word in (CONJUGATION, DIRECT):
        require(operator(word) == DEMAND, "full dirt/source endpoint")
    cases = 0
    for values in itertools.product(range(-4, 5), repeat=3):
        a, b, p = values
        for word in (CONJUGATION, DIRECT):
            require(execute(word, values) == (a + 5 * p, b + 12 * p, p), "literal dirty input")
            cases += 1
    return cases


def short_columns(origin):
    reached = {origin}
    frontier = {origin}
    layers = [1]
    edges = 0
    for _depth in range(2):
        following = set()
        for x, y in frontier:
            for a in range(60):
                following.add(((x + a * y) % 60, y))
                following.add((x, (y + a * x) % 60))
                edges += 2
        frontier = following - reached
        reached.update(following)
        layers.append(len(frontier))
    return reached, layers, edges


def check_short_obstruction():
    rows = []
    for axis, origin in enumerate(((1, 0), (0, 1))):
        reached, layers, edges = short_columns(origin)
        expected = set()
        for s, t in itertools.product(range(60), repeat=2):
            if axis == 0:
                expected.update(((1, t), ((1 + s * t) % 60, t)))
            else:
                expected.update(((t, 1), (t, (1 + s * t) % 60)))
        require(reached == expected, "independent two-shear normal form")
        for sign in (-1, 1):
            require((sign * 5 % 60, sign * 12 % 60) not in reached, "short integer column excluded")
        rows.append({"origin": list(origin), "new_states_by_depth": layers, "edges": edges})
    require(5 * 5 - 12 * 2 == 1, "primitive demand Bezout witness")
    return rows


def bill(word, mu, c):
    return sum((mu if j == 2 else c) for _i, j, _a in word)


def check_prices():
    prices = sorted({Fraction(n, d) for n in range(1, 11) for d in range(1, 5)})
    cases = 0
    for mu, c in itertools.product(prices, repeat=2):
        witness = min(bill(DIRECT, mu, c), bill(CONJUGATION, mu, c))
        require(witness == min(2 * mu, mu + 6 * c), "attained envelope")
        cases += 1
    require(bill(CONJUGATION, 10, 1) == 16, "integer discriminator")
    require(min(2 * 10, 10 + 4 * 1) == 14, "excluded finite-formula extension")
    require(bill(CONJUGATION, 6, 1) == bill(DIRECT, 6, 1), "tariff transition")
    return cases


def check_controls():
    controls = 0
    for k in range(len(CONJUGATION)):
        deleted = CONJUGATION[:k] + CONJUGATION[k + 1:]
        require(operator(deleted) != DEMAND, "deleted gate accepted")
        i, j, a = CONJUGATION[k]
        wrong_sign = CONJUGATION[:k] + ((i, j, -a),) + CONJUGATION[k + 1:]
        require(operator(wrong_sign) != DEMAND, "wrong sign accepted")
        controls += 2
    require(operator(((0, 2, 5),)) != DEMAND, "missing second output accepted")
    require(operator(((1, 0, 2), (0, 2, 5), (1, 0, -2))) != DEMAND, "wrong ratio accepted")
    return controls + 2


def main():
    require(len(sys.argv) == 1, "this fixed verifier takes no arguments")
    hashes = authenticate()
    receipt = {
        "status": "PASS_INTEGER_FANOUT_SHORTENING_GAP",
        "claim_type": "scoped proof with exact finite corroboration",
        "demand": [5, 12],
        "tariff": "min(2*mu,mu+6*c), mu>0,c>0",
        "literal_dirty_executions": check_attainers(),
        "modulus_60_short_column_census": check_short_obstruction(),
        "rational_price_fixtures": check_prices(),
        "semantic_rejection_controls": check_controls(),
        "package_sha256": hashes,
        "python": platform.python_version(),
    }
    print(json.dumps(receipt, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
