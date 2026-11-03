#!/usr/bin/env python3
"""Exact affine-generator certificates for the even-window equality obstruction.

Produced by Nick Petalas. Apache-2.0.
The all-k result is a written proof; this program corroborates k = 2, 3, 4.
"""

import argparse
from fractions import Fraction
import hashlib
from itertools import combinations
import json
from pathlib import Path
import platform


PACKAGE = Path(__file__).resolve().parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def pairing(x: int, y: int, k: int) -> int:
    """Standard alternating form with consecutive coordinate pairs."""
    return sum(
        ((x >> (2 * j)) & 1) * ((y >> (2 * j + 1)) & 1)
        + ((x >> (2 * j + 1)) & 1) * ((y >> (2 * j)) & 1)
        for j in range(k)
    ) % 2


def generators(k: int) -> tuple[tuple[int, ...], ...]:
    """Enumerate each maximal isotropic subspace by its unique RREF basis."""
    require(type(k) is int and 2 <= k <= 4, "k must be an integer in 2..4")
    result = []
    candidates = 0
    for pivots in combinations(range(2 * k), k):
        free = tuple(
            (i, j) for i, p in enumerate(pivots)
            for j in range(p + 1, 2 * k) if j not in pivots
        )
        require(len(free) <= k * k, "RREF free-bit bound")
        for mask in range(1 << len(free)):
            candidates += 1
            rows = [1 << p for p in pivots]
            for bit, (i, j) in enumerate(free):
                rows[i] |= ((mask >> bit) & 1) << j
            if any(pairing(x, y, k) for x, y in combinations(rows, 2)):
                continue
            span = [0]
            for row in rows:
                span += [x ^ row for x in span]
            result.append(tuple(sorted(span)))
    require(candidates <= 256 * (1 << (k * k)), "candidate bound")
    require(len(result) == len(set(result)), "duplicate RREF subspace")
    return tuple(result)


def incidence_data(k: int) -> tuple[tuple[int, ...], tuple[tuple[int, ...], ...]]:
    """Fix w=1, so the affine hyperplane b(p,w)=1 is bit 1 = 1."""
    labels = tuple(p for p in range(1 << (2 * k)) if pairing(p, 1, k))
    family = tuple(tuple(p for p in g if p in labels)
                   for g in generators(k) if 1 not in g)
    require(len(labels) == 1 << (2 * k - 1), "hyperplane size")
    for block in family:
        require(len(block) == 1 << (k - 1), "affine generator size")
        require(all(not pairing(p, q, k) for p, q in combinations(block, 2)),
                "nonorthogonal affine generator")
    return labels, family


def certificate(k: int, labels: tuple[int, ...], family: tuple[tuple[int, ...], ...],
                partner_delta: int = 1, scalar: Fraction | None = None) -> int:
    """Eliminate all other projection symbols from affine basis equations."""
    r = 1
    s = 1
    for j in range(1, k):
        r *= (1 << j) + 1
    for j in range(1, k - 1):
        s *= (1 << j) + 1
    require(len(family) == (1 << k) * r, "family count")
    total = {q: sum(q in block for block in family) for q in labels}
    require(all(value == r for value in total.values()), "point incidence")
    rhs = 2 * r * r - s * len(family)
    denominator = r * (r - s)
    expected_scalar = Fraction(1, 1 << (k - 2)) if scalar is None else scalar
    require(Fraction(rhs, denominator) == expected_scalar, "wrong scalar")
    checked = 0
    for p in labels:
        partner = p ^ partner_delta
        if p > partner:
            continue
        require(partner in total and partner != p, "invalid partner")
        selected = tuple(block for block in family if p in block or partner in block)
        require(len(selected) == 2 * r, "pair incidence")
        for q in labels:
            coefficient = r * sum(q in block for block in selected) - s * total[q]
            expected = denominator if q in (p, partner) else 0
            require(coefficient == expected, "projection elimination failed")
        checked += 1
    require(checked * 2 == len(labels), "partner partition")
    return checked


def multiply(a: tuple[tuple[Fraction, ...], ...],
             b: tuple[tuple[Fraction, ...], ...]) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(tuple(sum(a[i][j] * b[j][l] for j in range(2))
                       for l in range(2)) for i in range(2))


def algebra_controls() -> dict[str, int]:
    """Check the exact idempotent reduction and its exceptional scalars."""
    identity = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))
    p = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(0)))
    q = ((Fraction(0), Fraction(0)), (Fraction(0), Fraction(1)))
    require(multiply(p, p) == p and multiply(q, q) == q, "complement fixture")
    require(tuple(tuple(p[i][j] + q[i][j] for j in range(2))
                  for i in range(2)) == identity, "k=2 exception must survive")
    # For Q=cI-P and P^2=P, Q^2-Q=(c^2-c)I+(2-2c)P.
    # At c!=1 it forces P=(c/2)I. The latter is not idempotent for 0<c<1.
    for k in range(3, 33):
        c = Fraction(1, 1 << (k - 2))
        forced_p = -(c * c - c) / (2 - 2 * c)
        require(forced_p == c / 2, "idempotent elimination")
        require(forced_p * forced_p != forced_p, "false idempotent")
        require(c * c / 4 - c / 2 == c * (c - 2) / 4,
                "idempotency residual")
    return {"exceptional_projection_pair": 1, "scalar_instances": 30}


def rejection_controls(labels: tuple[int, ...], family: tuple[tuple[int, ...], ...]) -> int:
    rejected = 0
    cases = (
        (family[:-1], 1, None),
        (family + (family[0],), 1, None),
        (family, 4, None),
        (family, 1, Fraction(1, 4)),
    )
    for blocks, delta, scalar in cases:
        try:
            certificate(3, labels, blocks, delta, scalar)
        except ValueError:
            rejected += 1
    require(rejected == len(cases), "a false incidence certificate passed")
    for invalid in (0, 1, 5, True, Fraction(3)):
        try:
            generators(invalid)
        except ValueError:
            rejected += 1
    require(rejected == 9, "invalid dimension accepted")
    return rejected


def source_hashes() -> dict[str, str]:
    root = PACKAGE.parent.parent
    metadata = json.loads((PACKAGE / "SOURCES.json").read_text())
    hashes = {}
    for row in metadata["files"]:
        if row["usage"] == "input":
            digest = hashlib.sha256((root / row["path"]).read_bytes()).hexdigest()
            require(digest == row["sha256"], "changed predecessor input")
            hashes[row["path"]] = digest
    return hashes


def run() -> dict:
    hashes = source_hashes()
    rows = []
    for k in range(2, 5):
        labels, family = incidence_data(k)
        pairs = certificate(k, labels, family)
        rows.append({"k": k, "labels": len(labels), "affine_generators": len(family),
                     "pair_certificates": pairs, "forced_pair_scalar": str(Fraction(1, 1 << (k - 2)))})
        if k == 3:
            rejected = rejection_controls(labels, family)
    return {"status": "PASS_EVEN_WINDOW_SATURATION_GAP", "instances": rows,
            "algebra_controls": algebra_controls(), "rejections": rejected,
            "source_sha256": hashes}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path,
                        help="write a generated source-bound receipt outside the checkout")
    args = parser.parse_args()
    if args.receipt is not None:
        root = PACKAGE.parent.parent
        require(not args.receipt.resolve().is_relative_to(root), "receipt must be outside checkout")
    result = run()
    if args.receipt is not None:
        receipt = dict(result, python=platform.python_version(), package_sha256={
            p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(PACKAGE.iterdir()) if p.is_file()
        })
        args.receipt.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
