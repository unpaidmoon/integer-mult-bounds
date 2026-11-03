#!/usr/bin/env python3
"""Check the new response boundary, not the predecessor's scientific claims.

This contribution was produced by Nick Petalas. Apache-2.0.
"""

import hashlib
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
PORT_PATH = "research/p104-carrier-code-uniqueness/e8/ports.json"
PORT_SHA = "ba6a0b9cf76b7cccc1ce8b3d1aa78a4aa329b34d45aded694648f0cf43fc9fce"
WORD = (("add", 1, 2, 1), ("add", 1, 0, -1),
        ("scale", 0, 0, 2), ("add", 0, 1, 1))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_limited(path):
    with path.open("rb") as stream:
        data = stream.read(262145)
    require(len(data) <= 262144, "file size limit")
    return data


def load_ports():
    data = read_limited(HERE.parents[1] / PORT_PATH)
    require(hashlib.sha256(data).hexdigest() == PORT_SHA, "port source hash")
    ports = json.loads(data)
    require(isinstance(ports, list) and len(ports) == 104, "port shape")
    require(all(type(p) is int and 0 < p < 512 for p in ports), "port range")
    require(len(set(ports)) == 104, "port uniqueness")
    return ports


def binary_rank(rows):
    basis = [0] * 9
    for initial in rows:
        value = initial
        for bit in range(8, -1, -1):
            if value >> bit & 1:
                if basis[bit]:
                    value ^= basis[bit]
                else:
                    basis[bit] = value
                    break
    return sum(bool(v) for v in basis)


def scaled_root(port):
    weight = port.bit_count()
    if weight == 3:
        return tuple(2 if port >> bit & 1 else -1 for bit in range(9))
    require(weight == 7, "root weight")
    zeros = [bit for bit in range(9) if not port >> bit & 1]
    return tuple(3 if bit == zeros[0] else -3 if bit == zeros[1] else 0
                 for bit in range(9))


def gram(left, right):
    return Q(sum(a * b for a, b in zip(scaled_root(left), scaled_root(right),
                                      strict=True)), 9)


def witness(ports):
    x, y, z = 11, 19, 487
    require(all(p in ports for p in (x, y, z)), "triangle membership")
    common = [p for p in ports if not (p & x).bit_count() % 2
              and not (p & y).bit_count() % 2]
    require(len(common) == 24 and z in common, "common section")
    require(binary_rank((x, y)) == 2, "seven-frame rank")
    require(all(binary_rank((x, y, n)) == 3 for n in (455, 56)), "six-frame rank")
    first = [not (p & 455).bit_count() % 2 for p in common]
    second = [not (p & 56).bit_count() % 2 for p in common]
    require(all(a != b for a, b in zip(first, second, strict=True)), "complement")
    require(sum(first) == 16 and sum(second) == 8, "section sizes")
    plus = tuple(gram(x, p) / 2 for p in common)
    minus = tuple(gram(y, p) / 2 for p in common)
    c = tuple(Q(0) if p == z else value for p, value in zip(common, plus, strict=True))
    e = tuple(value - base for value, base in zip(plus, c, strict=True))
    require(minus == tuple(a - b for a, b in zip(c, e, strict=True)), "Gram targets")
    require(all(c[i] for i, p in enumerate(common) if p != z), "broad support")
    a = tuple(value if inside else Q(0) for value, inside in zip(c, first, strict=True))
    d = tuple(value - part for value, part in zip(c, a, strict=True))
    incoming = [list(e) + [Q(0)], list(a) + [Q(-1)], list(d) + [Q(1)]]
    expected = [list(plus) + [Q(0)], list(minus) + [Q(0)], incoming[2][:]]
    require([sum(bool(v) for v in row[:-1]) for row in incoming] == [1, 15, 8],
            "incoming live supports")
    return common, incoming, expected


def execute(rows, word):
    require(len(rows) == 3 and 1 <= len(rows[0]) <= 25, "register shape")
    require(all(len(row) == len(rows[0]) for row in rows), "register widths")
    require(len(word) <= 4, "word bound")
    result = [row[:] for row in rows]
    for operation, target, source, coefficient in word:
        require(0 <= target < 3 and 0 <= source < 3, "event index")
        if operation == "add":
            require(target != source, "ADD alias")
            result[target] = [a + coefficient * b for a, b in
                              zip(result[target], result[source], strict=True)]
        else:
            require(operation == "scale" and coefficient != 0, "SCALE contract")
            result[target] = [coefficient * a for a in result[target]]
    return result


def local_checks(incoming, expected):
    result = execute(incoming, WORD)
    require(result == expected, "response endpoint")
    inverse = tuple((op, target, source, -Q(coef) if op == "add" else 1 / Q(coef))
                    for op, target, source, coef in reversed(WORD))
    require(execute(result, inverse) == incoming, "literal inverse")
    cases = 0
    for clean, left, right, dirt in itertools.product(range(-2, 3), repeat=4):
        start = [[Q(clean)], [Q(left - dirt)], [Q(right + dirt)]]
        end = [[Q(left + right + clean)], [Q(left + right - clean)], start[2][:]]
        require(execute(start, WORD) == end, "dirty scalar endpoint")
        require(execute(end, inverse) == start, "dirty scalar inverse")
        cases += 1
    return {"symbolic_input_columns": 25, "dirty_scalar_cases": cases,
            "forward_events": len(WORD), "inverse_events": len(inverse)}


def mod_rank(rows):
    matrix = [[entry % 3 for entry in row] for row in rows]
    pivot = 0
    for column in range(len(matrix[0])):
        candidates = [i for i in range(pivot, len(matrix)) if matrix[i][column]]
        if not candidates:
            continue
        index = candidates[0]
        matrix[pivot], matrix[index] = matrix[index], matrix[pivot]
        factor = pow(matrix[pivot][column], -1, 3)
        matrix[pivot] = [(factor * v) % 3 for v in matrix[pivot]]
        for row in range(len(matrix)):
            if row != pivot:
                factor = matrix[row][column]
                matrix[row] = [(a - factor * b) % 3 for a, b in
                               zip(matrix[row], matrix[pivot], strict=True)]
        pivot += 1
        if pivot == len(matrix):
            break
    return pivot


def kernel_image(rows, dirt):
    pivot = next(i for i in range(3) if dirt[i])
    return [tuple((rows[j][k] - dirt[j] * rows[pivot][k]) % 3 for k in range(4))
            for j in range(3) if j != pivot]


def small_census():
    # F3^4, support <=2. Normalize nonzero dirt entries to one by row scaling.
    pool = [r for r in itertools.product(range(3), repeat=4) if sum(bool(x) for x in r) <= 2]
    patterns = [b for b in itertools.product(range(2), repeat=3) if any(b)]
    target = [(1, 1, 1, 1, 0), (2, 1, 1, 1, 0)]
    require(len(pool) == 33 and len(patterns) == 7, "small-domain bounds")
    totals, feasible = [0, 0, 0], [0, 0, 0]
    oracle_cases = 0
    for rows in itertools.product(pool, repeat=3):
        for dirt in patterns:
            image = kernel_image(rows, dirt)
            in_space = all(r[1] == r[2] == r[3] for r in image)
            determinant = (image[0][0] * image[1][1] - image[1][0] * image[0][1]) % 3
            succeeds = in_space and determinant != 0
            weight = sum(dirt)
            totals[weight - 1] += 1
            if succeeds:
                feasible[weight - 1] += 1
                require(weight >= 2, "isolated-dirt theorem")
                if weight == 2:
                    clean = dirt.index(0)
                    require(rows[clean][0] != 0 and rows[clean][1:] == (0, 0, 0),
                            "clean singleton theorem")
                    dirty = [i for i in range(3) if dirt[i]]
                    require(all(any(rows[i][k] for i in dirty) for k in range(1, 4)),
                            "dirty union theorem")
            # Full augmented-row elimination does not use the kernel formula.
            augmented = [tuple(row) + (b,) for row, b in zip(rows, dirt, strict=True)]
            direct = mod_rank(augmented + target) == mod_rank(augmented)
            require(direct == succeeds, "independent augmented-rank oracle")
            oracle_cases += 1
    return {"F3_cases": sum(totals), "F3_cases_by_dirty_weight": totals,
            "F3_feasible_by_dirty_weight": feasible, "independent_rank_cases": oracle_cases}


def rejection_controls(incoming, expected):
    failures = []
    for index in range(4):
        failures.append((incoming, WORD[:index] + WORD[index + 1:]))
    failures.append((incoming, WORD[:2] + (("scale", 0, 0, 1),) + WORD[3:]))
    bad_dirt = [row[:] for row in incoming]
    bad_dirt[1][-1] = Q(0)
    failures.append((bad_dirt, WORD))
    same_sign = [row[:] for row in incoming]
    same_sign[1][-1] = Q(1)
    failures.append((same_sign, WORD))
    bad_singleton = [row[:] for row in incoming]
    bad_singleton[0][0] += 1
    failures.append((bad_singleton, WORD))
    for rows, word in failures:
        require(execute(rows, word) != expected, "endpoint mutant escaped")
    invalid = ((("add", 0, 0, 1),), (("scale", 0, 0, 0),), (("other", 0, 0, 1),))
    for word in invalid:
        try:
            execute(incoming, word)
        except ValueError:
            continue
        raise ValueError("invalid event escaped")
    return len(failures) + len(invalid)


def scope_controls():
    # The isolated-dirt conclusion fails once a clean row may carry all of c.
    rows = [(0, 1, 1, 1, 0), (1, 0, 0, 0, 0), (0, 0, 0, 0, 1)]
    targets = [(1, 1, 1, 1, 0), (2, 1, 1, 1, 0)]
    require(mod_rank(rows + targets) == mod_rank(rows), "support-limit escape")
    # The full-rank argument also requires a nonzero dirt vector.
    clean = [(1, 0, 0, 0, 0), (0, 1, 1, 0, 0), (0, 0, 0, 1, 0)]
    require(mod_rank(clean + targets) == mod_rank(clean), "zero-dirt escape")
    return 2


def main():
    ports = load_ports()
    common, incoming, expected = witness(ports)
    result = {"marker": "PASS_P104_WIRE_DIRTY_ENTRY", "claim_type": "scoped-response-proof",
              "triangle": [11, 19, 487], "common_ports": common,
              "incoming_live_supports": [1, 15, 8], "source_sha256": PORT_SHA}
    result.update(local_checks(incoming, expected))
    result.update(small_census())
    result["rejecting_controls"] = rejection_controls(incoming, expected)
    result["outside_scope_positive_controls"] = scope_controls()
    names = ("README.md", "PROOF.md", "verify.py", "TASK.json", "SOURCES.json", "VERIFY.json")
    result["package_sha256"] = {name: hashlib.sha256(read_limited(HERE / name)).hexdigest()
                                for name in names}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
