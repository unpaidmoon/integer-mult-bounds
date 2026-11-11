"""Finite corroboration of the written all-width annihilator proof."""

import argparse
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from group import (action, compose, cross_phase, diagonal, generator, image,
                   inverse, monomials, parity, require, symmetric, validate)

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[1]
INPUT = ("research/centre-polynomial-cache-limits/frozen/work/"
         "centre-encoding-campaign-20261014/lanes/circuit-interface/INTERFACE.json")
PIN = "5c6c51fbffc07a683e922f17532fd90262ae9e23cc3560a696002073dd234ef3"


def read_bounded(path):
    require(path.stat().st_size <= 1 << 20, "File size at most one MiB")
    return path.read_bytes()


def source(raw):
    require(sha256(raw).hexdigest() == PIN, "Historical query source pin")
    value = json.loads(raw)
    require(len(value["R"]) == 8 and len(value["ports"]) == 112, "Query shape")
    ports = value["ports"]
    require(len(set(ports)) == 112, "Distinct source labels")
    require(all(type(q) is int and 0 < q < 512 and q.bit_count() % 2 == 1
                for q in ports), "Nine-bit odd source labels")
    return ports


def expanded_cross(s, t, n):
    """Independent coefficient expansion, with c_i squared reduced to c_i."""
    positions = {term: k for k, term in enumerate(monomials(n))}
    answer = 0
    for i in range(n):
        for j in range(n):
            if s[i] >> i & 1 and t[j] >> i & 1:
                answer ^= 1 << positions[1 << j]
            for k in range(n):
                if s[j] >> i & 1 and t[k] >> i & 1:
                    answer ^= 1 << positions[(1 << j) | (1 << k)]
    return answer


def permutation(element, n):
    return tuple(action(element, c, a, n)
                 for c in range(1 << n) for a in range(1 << n))


def small_envelopes():
    counts = []
    pair_count = 0
    for n in range(1, 4):
        size = 1 << len(monomials(n))
        elements = [(symmetric(s, n), h) for s in range(size) for h in range(size)]
        maps = []
        identity = ((0,) * n, 0)
        for element in elements:
            validate(element, n)
            maps.append(permutation(element, n))
            require(compose(element, inverse(element, n), n) == identity, "Inverse")
            require(compose(inverse(element, n), element, n) == identity, "Left inverse")
        require(len(set(maps)) == len(elements), "Injective normal form")
        counts.append({"n": n, "elements": len(elements), "states": 1 << (2 * n)})
        if n <= 2:
            for i, left in enumerate(elements):
                for j, right in enumerate(elements):
                    product = permutation(compose(left, right, n), n)
                    literal = tuple((sign ^ maps[i][target][0], maps[i][target][1])
                                    for sign, target in maps[j])
                    require(product == literal, "Literal signed composition")
                    pair_count += 1
    return counts, pair_count


def source_products(ports):
    count = 0
    for q in ports:
        left = generator(q, 9)
        validate(left, 9)
        require(compose(left, left, 9) == ((0,) * 9, 0), "Port involution")
        require(action(left, 0, 0, 9) == (0, 0), "Common fixed vector")
        for r in ports:
            right = generator(r, 9)
            require(cross_phase(left[0], right[0], 9) ==
                    expanded_cross(left[0], right[0], 9), "Quadratic coefficient routes")
            product = compose(left, right, 9)
            for c, a in ((0, 1), (511, 511), (q, r), (r, q), (q ^ r, 1)):
                s, target = action(right, c, a, 9)
                t, end = action(left, c, target & 511, 9)
                require(action(product, c, a, 9) == (s ^ t, end), "Port product action")
            count += 1
    return count


def mm(a, b):
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n))
             for j in range(n)] for i in range(n)]


def characteristic(a):
    """Faddeev-LeVerrier with checked exact integer divisions, dimension eight."""
    n = len(a)
    require(n == 8, "Fixed characteristic-polynomial fixture")
    b = [[int(i == j) for j in range(n)] for i in range(n)]
    coefficients = [1]
    for k in range(1, n + 1):
        b = mm(a, b)
        trace = sum(b[i][i] for i in range(n))
        require(trace % k == 0, "Exact characteristic coefficient")
        coefficient = -trace // k
        coefficients.append(coefficient)
        for i in range(n):
            b[i][i] += coefficient
    require(not any(x for row in b for x in row), "Regular annihilation")
    return coefficients


def determinant(a):
    values = [[Fraction(x) for x in row] for row in a]
    answer = Fraction(1)
    for k in range(len(a)):
        row = next((i for i in range(k, len(a)) if values[i][k]), None)
        if row is None:
            return Fraction(0)
        if row != k:
            values[k], values[row] = values[row], values[k]
            answer = -answer
        pivot = values[k][k]
        answer *= pivot
        for i in range(k + 1, len(a)):
            ratio = values[i][k] / pivot
            for j in range(k + 1, len(a)):
                values[i][j] -= ratio * values[k][j]
            values[i][k] = 0
    return answer


def lifted_target(element, address, width):
    sign, target = 0, 0
    for k in range(width):
        state = address >> (2 * k) & 3
        phase, moved = action(element, state >> 1, state & 1, 1)
        sign ^= phase
        target |= moved << (2 * k)
    return (-1 if sign else 1), target


def example_matrix(elements, weights, width):
    size = len(elements) if width == 0 else 4 ** width
    result = [[0] * (2 * size) for _ in range(2 * size)]
    for k, element in enumerate(elements):
        for j in range(size):
            if width == 0:
                sign, target = 1, elements.index(compose(element, elements[j], 1))
            else:
                sign, target = lifted_target(element, j, width)
            for a in range(2):
                for b in range(2):
                    result[a * size + target][b * size + j] += sign * weights[k][a][b]
    return result


def polynomial_zero(a, coefficients):
    n = len(a)
    edges = [(i, j, value) for i, row in enumerate(a)
             for j, value in enumerate(row) if value]
    for column in range(n):
        value = [int(i == column) for i in range(n)]
        for coefficient in coefficients[1:]:
            moved = [0] * n
            for i, j, scale in edges:
                moved[i] += scale * value[j]
            moved[column] += coefficient
            value = moved
        if any(value):
            return False
    return True


def algebra_example():
    elements = [(symmetric(s, 1), h) for s in range(2) for h in range(2)]
    weights = (((1, 0), (0, 0)), ((0, 0), (0, 1)),
               ((1, 1), (1, 1)), ((1, -1), (-1, 1)))
    regular = example_matrix(elements, weights, 0)
    coefficients = characteristic(regular)
    for x in range(9):
        value = 0
        for coefficient in coefficients:
            value = x * value + coefficient
        shifted = [[x * int(i == j) - regular[i][j] for j in range(8)] for i in range(8)]
        require(value == determinant(shifted), "Independent determinant evaluation")
    dimensions = []
    for width in range(1, 4):
        matrix = example_matrix(elements, weights, width)
        require(polynomial_zero(matrix, coefficients), "Tensor representation annihilation")
        dimensions.append(len(matrix))
    bad = coefficients[:]
    bad[-1] += 1
    require(not polynomial_zero(regular, bad), "Wrong polynomial rejected")
    return {"polynomial_descending": coefficients, "lift_dimensions": dimensions,
            "determinant_evaluations": 9}


def rejects(call, reason):
    try:
        call()
    except ValueError:
        return
    raise ValueError(reason)


def controls(raw):
    rejects(lambda: source(raw + b" "), "Source-byte mutation rejected")
    rejects(lambda: monomials(10), "Dimension overflow rejected")
    rejects(lambda: generator(512, 9), "Label overflow rejected")
    rejects(lambda: validate(((2, 0), 0), 2), "Asymmetry rejected")
    rejects(lambda: validate(((0, 0), 8), 2), "Phase overflow rejected")
    s, t = ((1, 0), 0), ((2, 1), 0)
    require(cross_phase(s[0], t[0], 2) & 4, "Quadratic cross term needed")
    require(compose(s, t, 2) != compose(t, s, 2), "Product order matters")
    require(compose(t, t, 2) != ((0, 0), 0), "General envelope map need not be involutive")
    require(action(generator(1, 1), 0, 1, 1)[0] == 1, "Diagonal sign needed")
    require(action(((0,), 1), 1, 0, 1)[0] == 1, "Central sign retained")
    central = ((0,), 1)
    one_slot = [(-1 if action(central, c, a, 1)[0] else 1)
                for c in range(2) for a in range(2)]
    correct = [1 + 2 * a * b for a in one_slot for b in one_slot]
    wrong = [(1 + 2 * a) * (1 + 2 * b) for a in one_slot for b in one_slot]
    require(correct != wrong and correct[0] == 3 and wrong[0] == 9,
            "Tensoring the whole sum gives the wrong operator")
    return 11


def receipt():
    raw = read_bounded(ROOT / INPUT)
    ports = source(raw)
    envelopes, pairs = small_envelopes()
    products = source_products(ports)
    example = algebra_example()
    report = {"status": "PASS_UNIFORM_CENTRE_GRAM_ANNIHILATOR",
              "source_sha256": sha256(raw).hexdigest(), "small_envelopes": envelopes,
              "exhaustive_composition_pairs": pairs, "source_generator_pairs": products,
              "source_product_states": 5 * products, "algebra_example": example,
              "controls": controls(raw) + 1,
              "enclosing_group_size_bound": 2 ** 90,
              "uniform_annihilator_degree_bound": 2 ** 93}
    names = ("README.md", "PROOF.md", "TASK.json", "SOURCES.json", "VERIFY.json",
             "group.py", "verify.py")
    report["package_sha256"] = {name: sha256(read_bounded(PACKAGE / name)).hexdigest()
                                for name in names}
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-receipt", type=Path)
    args = parser.parse_args()
    report = receipt()
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.write_receipt:
        with args.write_receipt.open("x", encoding="utf-8") as handle:
            require(handle.write(encoded) == len(encoded), "Complete receipt write")
    else:
        require(read_bounded(PACKAGE / "RESULT.json").decode("utf-8") == encoded,
                "Exact receipt bytes and types")
    print(encoded, end="")


if __name__ == "__main__":
    main()
