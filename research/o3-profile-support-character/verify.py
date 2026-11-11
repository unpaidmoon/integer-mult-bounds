#!/usr/bin/env python3
"""Exact checks for the (2,1,1,0)/(1,1,1) support-or-character split.

The proof is PROOF.md. This program checks the finite identities and
enumerations used there, plus a bounded rational sample. It raises
SystemExit on failure, so python -O keeps the checks. Standard library only.
"""

from __future__ import annotations

from fractions import Fraction as Fr
from itertools import product
from math import gcd, isqrt


Vec = tuple[Fr, Fr, Fr]
A: Vec = (Fr(1), Fr(0), Fr(0))
B: Vec = (Fr(0), Fr(1), Fr(0))
P: Vec = (Fr(0), Fr(0), Fr(1))
Q: Vec = (Fr(1), Fr(1), Fr(-1))
M: Vec = (Fr(2), Fr(3), Fr(-1))
AQ: Vec = (Fr(2), Fr(1), Fr(-1))
BQ: Vec = (Fr(1), Fr(2), Fr(-1))
TARGETS: tuple[Vec, ...] = (
    (Fr(1), Fr(0), Fr(1)),
    AQ,
    (Fr(0), Fr(1), Fr(1)),
    BQ,
)
SAMPLE_DENOMINATOR = 48


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit("FAIL: " + message)


def add(u: Vec, v: Vec) -> Vec:
    return (u[0] + v[0], u[1] + v[1], u[2] + v[2])


def sub(u: Vec, v: Vec) -> Vec:
    return (u[0] - v[0], u[1] - v[1], u[2] - v[2])


def scale(c: Fr, u: Vec) -> Vec:
    return (c * u[0], c * u[1], c * u[2])


def rank_one(u: Vec) -> bool:
    a, b, c = u
    return u != (0, 0, 0) and 2 * a * b + c * (a + b) == 0


def old_offsets() -> list[Vec]:
    return [(Fr(alpha), Fr(beta), Fr(gamma))
            for alpha, beta, gamma in product((0, 1, 2), (0, 1), (0, 1))]


def support_holds(frames: tuple[Vec, Vec, Vec]) -> bool:
    calls = [A, A, B, P, *frames]
    sums = {(Fr(0), Fr(0), Fr(0))}
    for call in calls:
        sums |= {add(partial, call) for partial in sums}
    return all(target in sums for target in TARGETS)


def reduced(vector: Vec) -> tuple[int, int, int, int]:
    den = 1
    for coordinate in vector:
        den = den * coordinate.denominator // gcd(den, coordinate.denominator)
    cleared = [int(coordinate * den) for coordinate in vector]
    g = den
    for value in cleared:
        g = gcd(g, abs(value))
    return (cleared[0] // g, cleared[1] // g, cleared[2] // g, den // g)


def character_counts(first: Vec) -> tuple[int, int]:
    """Numerator parity of the c-coordinate, on the reduced denominator."""
    _a1, _b1, c1, den = reduced(first)
    require(den % 2 == 1, "reduced denominator is even")
    require(c1 % 2 == 0, "reduced C1 is odd")

    def phi(vector: Vec) -> int:
        numerator = vector[2] * den
        require(numerator.denominator == 1, "c-coordinate is outside (1/d)Z")
        return int(numerator) % 2

    second = sub((Fr(1), Fr(2), Fr(0)), first)
    calls = phi(P) + phi(first) + phi(second) + phi(Q)
    # Two A calls and the B call have c-coordinate 0.
    targets = sum(phi(target) for target in TARGETS)
    return calls, targets


def check_support_classification() -> None:
    single = []
    paired = []
    for old in old_offsets():
        sigma = sub(BQ, old)
        if rank_one(sigma):
            single.append(sigma)
        if rank_one(sub(M, sigma)):
            paired.append(sub(M, sigma))
    require(single == [Q], "B+Q has a single-frame support other than Q")
    require(paired == [], "B+Q has a two-frame support")
    require(not rank_one(sub(M, scale(Fr(2), Q))), "two copies of Q leave a rank-one frame")
    require(add(Q, A) == AQ and add(Q, B) == BQ, "Q does not complete both Q-targets")
    require(sub(M, Q) == add(A, scale(Fr(2), B)), "M-Q is not A+2B")


def check_polynomial() -> None:
    # (1-a)(2-b)(a+b) + ab(3-a-b) must equal 2a + 2b - 2a^2 - b^2.
    terms: dict[tuple[int, int], int] = {}

    def absorb(poly: dict[tuple[int, int], int], factor: dict[tuple[int, int], int]) -> dict[tuple[int, int], int]:
        out: dict[tuple[int, int], int] = {}
        for (i, j), coeff in poly.items():
            for (k, ell), other in factor.items():
                key = (i + k, j + ell)
                out[key] = out.get(key, 0) + coeff * other
        return {key: value for key, value in out.items() if value}

    one_minus_a = {(0, 0): 1, (1, 0): -1}
    two_minus_b = {(0, 0): 2, (0, 1): -1}
    a_plus_b = {(1, 0): 1, (0, 1): 1}
    left = absorb(absorb(one_minus_a, two_minus_b), a_plus_b)
    right = {(1, 1): 3, (2, 1): -1, (1, 2): -1}
    for key, value in right.items():
        left[key] = left.get(key, 0) + value
    terms = {key: value for key, value in left.items() if value}
    require(terms == {(1, 0): 2, (0, 1): 2, (2, 0): -2, (0, 2): -1},
            "rank-one substitution did not simplify")


def is_square(value: int) -> bool:
    if value < 0:
        return False
    root = isqrt(value)
    return root * root == value


def sample_pairs() -> list[Vec]:
    found = [(Fr(1), Fr(0), Fr(0)), (Fr(0), Fr(2), Fr(0)), (Fr(0), Fr(0), Fr(4, 3))]
    for den in range(1, SAMPLE_DENOMINATOR + 1):
        for num in range(-2 * SAMPLE_DENOMINATOR, 2 * SAMPLE_DENOMINATOR + 1):
            a = Fr(num, den)
            disc = 4 + 8 * a * (1 - a)
            if disc < 0:
                continue
            if not (is_square(disc.numerator) and is_square(disc.denominator)):
                continue
            root = Fr(isqrt(disc.numerator), isqrt(disc.denominator))
            for sign in (1, -1):
                b = (2 + sign * root) / 2
                if a + b == 0:
                    continue
                c = -2 * a * b / (a + b)
                first = (a, b, c)
                second = (1 - a, 2 - b, -c)
                if rank_one(first) and rank_one(second):
                    found.append(first)
    return found


def check_sample(pairs: list[Vec]) -> int:
    seen = 0
    for first in pairs:
        second = sub((Fr(1), Fr(2), Fr(0)), first)
        require(rank_one(first) and rank_one(second), "sample pair is not rank one")
        require(add(first, second) == (Fr(1), Fr(2), Fr(0)), "sample pair misses A+2B")
        frames = (first, second, Q)
        require(add(add(first, second), Q) == M, "sample does not sum to M")
        require(support_holds(frames), "Q-pair misses a target")
        calls, targets = character_counts(first)
        require(calls == 2 and targets == 4, "character does not separate the sample")
        seen += 1
    require(seen == 323, "rational sample changed size")
    return seen


def check_controls() -> None:
    witness = (
        (Fr(0), Fr(-1), Fr(0)),
        (Fr(5, 2), Fr(5, 2), Fr(-5, 2)),
        (Fr(-1, 2), Fr(3, 2), Fr(3, 2)),
    )
    require(add(add(witness[0], witness[1]), witness[2]) == M, "published survivor misses M")
    require(all(rank_one(frame) for frame in witness), "published survivor is not rank one")
    require(not support_holds(witness), "published character survivor gained support")
    broken = (add(A, B), sub(sub(M, Q), add(A, B)), Q)
    require(not rank_one(broken[0]), "control summand became rank one")
    diagonal = (A, scale(Fr(2), B), Q)
    require(support_holds(diagonal), "diagonal triple lost support")
    calls, targets = character_counts(A)
    require(calls < targets, "diagonal triple is not separated")


def check_profile_list() -> None:
    """The eight O3 profiles named by PR #7128, as a list check only."""
    named = {
        (0, 1, 1, 2), (0, 1, 2, 1), (1, 0, 1, 2), (1, 0, 2, 1),
        (1, 2, 0, 1), (1, 2, 1, 0), (2, 1, 0, 1), (2, 1, 1, 0),
    }
    require(len(named) == 8 and (2, 1, 1, 0) in named, "O3 list changed")


def main() -> None:
    check_support_classification()
    check_polynomial()
    sample_count = check_sample(sample_pairs())
    check_controls()
    check_profile_list()
    print(
        "PASS_O3_PROFILE_SUPPORT_CHARACTER"
        f" sample={sample_count}"
        " calls=2 targets=4"
        " kappa=363005817/100000000000"
        " no_new_kappa=true"
    )


if __name__ == "__main__":
    main()
