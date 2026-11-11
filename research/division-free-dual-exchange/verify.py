"""Exact finite corroboration, produced by Nick Petalas; Apache-2.0."""

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path

import compiler as C

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LIMIT = 128 * 1024


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    need(path.stat().st_size <= LIMIT, "Bounded file size")
    return sha256(path.read_bytes()).hexdigest()


def bindings():
    manifest = json.loads((HERE / "SOURCES.json").read_text())
    inputs = [r for r in manifest["files"] if r["usage"] == "input"]
    need(len(inputs) == 3, "Three declared source inputs")
    for row in inputs:
        need(digest(ROOT / row["path"]) == row["sha256"], "Source hash " + row["path"])
    return {row["path"]: row["sha256"] for row in inputs}


def identity(n):
    return [[Q(i == j) for j in range(n)] for i in range(n)]


def multiply(a, b):
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n))
             for j in range(n)] for i in range(n)]


def expected(a, b):
    n = len(a)
    return [[Q(i == j) - b[i] * a[j] for j in range(n)] + [b[i]]
            for i in range(n)] + [list(a) + [Q(0)]]


def interpret(operations, n, growth=None):
    rows = identity(n)
    for op, r, s, q in operations:
        need(0 <= r < n and 0 <= s < n and q != 0, "Instruction indices")
        if op == "ADD":
            need(r != s, "Distinct row update")
            rows[r] = [x + q * y for x, y in zip(rows[r], rows[s])]
        else:
            need(op == "SCALE" and r == s and q == -1, "Sign instruction")
            rows[r] = [q * x for x in rows[r]]
        if growth is not None:
            need(max(sum(map(abs, row)) for row in rows) <= growth,
                 "Every scalar prefix respects the height envelope")
    return rows


def independent_cost(operations):
    cost = 0
    for op, _, _, q in operations:
        if op == "SCALE":
            need(q == -1, "Priced sign")
            cost += 2
        else:
            numerator = bin(abs(q.numerator))[2:]
            exponent = q.denominator.bit_length() - 1
            cost += 2 * (len(numerator) + numerator.count("1") + exponent + 2)
    return cost


def check_pair(a, b):
    a, b = tuple(map(Q, a)), tuple(map(Q, b))
    n, s = len(a), expected(a, b)
    prices = []
    for repeat in ("a", "b"):
        ops = C.compile_exchange(a, b, repeat)
        alpha, beta = 1 + sum(map(abs, a)), 1 + sum(map(abs, b))
        bound = alpha * alpha * beta if repeat == "a" else alpha * beta * beta
        matrix = interpret(ops, n + 1, bound)
        need(matrix == s and multiply(matrix, matrix) == identity(n + 1),
             "Complete exchange and arbitrary-input involution")
        repeated, single = (a, b) if repeat == "a" else (b, a)
        count = 2 * sum(q != 0 for q in repeated) + sum(q != 0 for q in single) + 1
        need(len(ops) == count, "Exact scalar gate count")
        permitted = {Q(-1)} | set(a) | set(b) | {-q for q in (*a, *b)}
        need(all(q in permitted for _, _, _, q in ops), "No new coefficients")
        prices.append(independent_cost(ops))
        need(C.allowance(ops) == prices[-1], "Independent scalar tariff")
    chosen = C.compile_exchange(a, b)
    need(independent_cost(chosen) == min(prices), "Cheaper displayed factorization")
    return len(chosen)


def consumer(a, b):
    """Check every dirty-input column with a non-scalar two-coordinate G."""
    n = len(a)
    scalar = interpret(C.compile_exchange(a, b), n + 1)
    whole = [[scalar[i // 2][j // 2] * Q(i % 2 == j % 2)
              for j in range(2 * n + 2)] for i in range(2 * n + 2)]
    g = [[Q(2), Q(1)], [Q(1), Q(1)]]
    use = identity(2 * n + 2)
    for i in range(2):
        for j in range(2):
            use[2 * n + i][2 * n + j] = g[i][j]
    actual = multiply(whole, multiply(use, whole))
    target = identity(2 * n + 2)
    for i in range(n):
        for j in range(n):
            for r in range(2):
                for s in range(2):
                    target[2 * i + r][2 * j + s] += b[i] * a[j] * (g[r][s] - Q(r == s))
    need(actual == target, "Full field consumer, arbitrary spare return and no leakage")


def legacy_fixture():
    path = ROOT / "research/dyadic-helper-basis-completion/basis.py"
    spec = importlib.util.spec_from_file_location("pinned_legacy_basis", path)
    need(spec is not None and spec.loader is not None, "Pinned comparison loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    old = module.compile_basis([3, 5, 0], [2, -1, 0], 2)
    new = C.compile_exchange([3, 5], [2, -1])
    old_cost = 0
    for op, _, _, q in old:
        if op == "ADD":
            old_cost += independent_cost([(op, 0, 1, q)])
        else:
            n, d = abs(q.numerator), q.denominator
            old_cost += 2 * (abs(n.bit_length() - d.bit_length()) + int(q < 0))
    need((len(old), old_cost, len(new), independent_cost(new)) == (20, 134, 7, 64),
         "Named emitted-program improvement")
    return {"a": [3, 5], "b": [2, -1], "roles": 3,
            "legacy_gates": len(old), "legacy_allowance": old_cost,
            "new_gates": len(new), "new_allowance": independent_cost(new),
            "new_program": [[op, r, s, str(q)] for op, r, s, q in new]}


def rejects(action):
    try:
        action()
    except ValueError:
        return 1
    raise ValueError("Expected rejection did not occur")


def controls():
    invalid = [([], []), ([1], [1, 0]), ([1], [0]), ([Q(1, 3)], [3]),
               ([1.0], [1]), ([True], [1]), ([2**65], [Q(1, 2**65)]),
               ([Q(1, 2**33)], [2**33]), ([1] * 17, [1] + [0] * 16)]
    count = sum(rejects(lambda a=a, b=b: C.compile_exchange(a, b)) for a, b in invalid)
    count += rejects(lambda: C.compile_exchange([1], [1], "unknown"))
    good = C.compile_exchange([3, 5], [2, -1], "b")
    target = expected([Q(3), Q(5)], [Q(2), Q(-1)])
    for index in range(len(good)):
        altered = good[:index] + good[index + 1:]
        count += rejects(lambda altered=altered: need(interpret(altered, 3) == target,
                                                     "Omitted operation detected"))
    bad = good[:]
    op, r, s, q = bad[2]
    bad[2] = (op, r, s, -q)
    count += rejects(lambda: need(interpret(bad, 3) == target, "Wrong sign detected"))
    count += rejects(lambda: need(interpret(list(reversed(good)), 3) == target,
                                 "Wrong chronological order detected"))
    return count


def evidence():
    counts = {"integer_pairs": 0, "dyadic_pairs": 0, "field_consumers": 0,
              "boundary_pairs": 0}
    for x, y, u, v in product(range(-3, 4), repeat=4):
        if x * u + y * v == 1:
            check_pair([x, y], [u, v])
            counts["integer_pairs"] += 1
    for n in range(1, 9):
        for k in range(8):
            b = [Q(1)] + [Q((i + k) % 5 - 2, 2**(k % 4)) for i in range(1, n)]
            a = [Q(0)] + [Q((2 * i + k) % 7 - 3, 2**((k + 1) % 4)) for i in range(1, n)]
            a[0] = 1 - sum(a[i] * b[i] for i in range(1, n))
            check_pair(a, b)
            counts["dyadic_pairs"] += 1
            if k == 0:
                consumer(a, b)
                counts["field_consumers"] += 1
    check_pair([3, 5], [2, -1])
    for a, b in [([1] + [0] * 15, [1] + [0] * 15),
                 ([2**63, 1], [0, 1]), ([Q(1, 2**32)], [2**32])]:
        check_pair(a, b)
        counts["boundary_pairs"] += 1
    consumer(list(map(Q, [3, 5])), list(map(Q, [2, -1])))
    counts["field_consumers"] += 1
    counts["controls_rejected"] = controls()
    return {"schema": "division-free-dual-exchange/1", "counts": counts,
            "fixture": legacy_fixture(), "source_sha256": bindings()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Regenerate the retained result")
    args = parser.parse_args()
    bindings()
    result = evidence()
    files = ["compiler.py", "verify.py", "PROOF.md", "README.md", "TASK.json", "SOURCES.json", "VERIFY.json"]
    result["package_sha256"] = {name: digest(HERE / name) for name in files}
    target = HERE / "RESULT.json"
    if args.write:
        target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    else:
        need(result == json.loads(target.read_text()), "Generated result and source bindings")
    print("PASS_DIVISION_FREE_DUAL_EXCHANGE " + json.dumps(result["counts"], sort_keys=True))


if __name__ == "__main__":
    main()
