#!/usr/bin/env python3
"""Exact finite corroboration of the single-merge tariff proof.

Produced by Nick Petalas. Apache-2.0.
The source geometry is an inherited premise, not independently replayed here.
"""

import argparse
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path
import platform


PACKAGE = Path(__file__).resolve().parent
MAX_DIMENSION = 14


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(s, u, a, m, f):
    require(all(type(x) is int for x in (s, u, a, m, f)), "integer dimensions")
    require(1 <= s < u <= MAX_DIMENSION, "dimension range")
    require(0 <= a <= m <= s and a < f <= u, "contact incidence")


def formula(s, u, a, m, f):
    validate(s, u, a, m, f)
    ranks = (a, f-a, u+1-f, u+1-f, f-1, s-m, u-m, m-a)
    return tuple(sorted(r for r in ranks if r))


def flags(s, u, a, m, f):
    validate(s, u, a, m, f)
    source = (1 << s)-1
    common = (1 << u)-1
    line = 1 << s
    delivery = (1 << a)-1
    meeting = delivery | line
    for bit in range(u):
        if meeting.bit_count() < f:
            meeting |= 1 << bit
    require(meeting.bit_count() == f, "meeting dimension")
    merge = (1 << m)-1
    return source, common, line, delivery, meeting, merge


def geometric_profile(s, u, a, m, f):
    source, common, line, delivery, meeting, merge = flags(s, u, a, m, f)
    high = common | (1 << u)
    exit_frame = common | (1 << (u+1))
    require(high & exit_frame == common, "root/reader intersection")
    require(source & line == 0 and delivery & merge == delivery, "merge flag")
    moves = ((0, delivery), (delivery, meeting), (meeting, exit_frame),
             (high, meeting), (meeting, line), (source, merge),
             (common, merge), (merge, delivery))
    ranks = []
    for left, right in moves:
        require((left & right) in (left, right), "nested native move")
        rank = abs(left.bit_count()-right.bit_count())
        if rank:
            ranks.append(rank)
    return tuple(sorted(ranks))


def endpoints(s, u):
    return (tuple(sorted((1, u, u, s, u-s))),
            tuple(sorted((1, 1, s, u-s, u-s, u-1))))


def caps(profile, u):
    require(len(profile) <= 8 and all(1 <= r <= u for r in profile), "rank range")
    return tuple(sum(min(r, k) for r in profile) for k in range(1, u+1))


def certify(profile, lower, u):
    differences = tuple(x-y for x, y in zip(caps(profile, u), caps(lower, u), strict=True))
    require(min(differences) >= 0, "capped-sum floor")
    return differences


def check_dimensions():
    actual, pair_count, recipe_count = [], 0, 0
    for u in range(2, MAX_DIMENSION+1):
        for s in range(1, u):
            pair_count += 1
            low, high = endpoints(s, u)
            require(formula(s, u, 0, s, 1) == low, "low endpoint attainment")
            require(formula(s, u, s, s, u) == high, "high endpoint attainment")
            for m in range(s+1):
                for a in range(m+1):
                    for f in range(a+1, u+1):
                        profile = geometric_profile(s, u, a, m, f)
                        require(profile == formula(s, u, a, m, f), "independent geometric invoice")
                        differences = certify(profile, low if f == 1 else high, u)
                        recipe_count += 1
                        if (s, u) == (3, 6):
                            actual.append({"a": a, "m": m, "f": f,
                                           "paid_ranks": profile, "cap_gaps": differences})
    require(len(actual) == 50, "reader-497 recipe coverage")
    require(pair_count == 91 and recipe_count == 20_839, "general finite coverage")
    return pair_count, recipe_count, actual


def payload_word():
    # Rows are A,V,B,Q,C_V,C_B. Disposal is explicitly free in this relaxation.
    return (("copy", 4, 1, 1), ("copy", 5, 2, 1), ("add", 4, 5, 1),
            ("clear", 5, 0, 0), ("add", 0, 4, 1), ("clear", 4, 0, 0),
            ("add", 0, 3, -4))


def execute(word, public):
    require(len(word) <= 8 and len(public) == 4, "payload bounds")
    rows = [*public, Fraction(0), Fraction(0)]
    for operation, destination, source, coefficient in word:
        require(0 <= destination < 6 and 0 <= source < 6, "row bounds")
        if operation == "copy":
            require(rows[destination] == 0, "copy into empty owned row")
            rows[destination] = coefficient*rows[source]
        elif operation == "add":
            rows[destination] += coefficient*rows[source]
        elif operation == "clear":
            rows[destination] = Fraction(0)
        else:
            raise ValueError("unknown payload operation")
    return tuple(rows)


def expected(public):
    a, v, b, q = public
    return (a+v+b-4*q, v, b, q, Fraction(0), Fraction(0))


def check_payload():
    basis = [tuple(Fraction(i == j) for i in range(4)) for j in range(4)]
    samples = [tuple(Fraction(x, 3) for x in row) for row in product(range(-1, 2), repeat=4)]
    for public in [*basis, *samples]:
        require(execute(payload_word(), public) == expected(public), "dirty payload endpoint")
    return basis, len(basis)+len(samples)


def check_controls(basis):
    invalid = ((3, 6, 1, 0, 2), (3, 6, 1, 1, 1), (3, 6, 0, 4, 6),
               (3, 6, 0, 0, 7), (0, 6, 0, 0, 1), (3, 6, True, 1, 2))
    for arguments in invalid:
        reason = ("integer dimensions" if type(arguments[2]) is bool else
                  "dimension range" if arguments[0] == 0 else "contact incidence")
        try:
            formula(*arguments)
        except ValueError as error:
            require(str(error) == reason, "wrong recipe rejection")
        else:
            raise ValueError("invalid recipe accepted")
    # Omitting B's cache transport turns the high endpoint into the old bill.
    baseline = (1, 1, 3, 3, 5)
    try:
        certify(baseline, endpoints(3, 6)[1], 6)
    except ValueError as error:
        require(str(error) == "capped-sum floor", "wrong unpaid-MOVE rejection")
    else:
        raise ValueError("unpaid B transport accepted")
    # Removing every cache MOVE produces a false optimistic improvement in call count.
    require(caps((1, 6, 6), 6)[0] < caps(baseline, 6)[0], "unpaid-cache control")
    changes = ((0, ("copy", 4, 2, 1)), (2, ("add", 4, 5, 0)),
               (4, ("copy", 0, 4, 1)), (5, ("add", 4, 5, 0)),
               (6, ("add", 0, 3, 0)))
    for index, gate in changes:
        word = list(payload_word())
        word[index] = gate
        rejects = 0
        for public in basis:
            try:
                rejects += execute(word, public) != expected(public)
            except ValueError:
                rejects += 1
        require(rejects > 0, "payload mutation escaped")
    return len(invalid)+2+len(changes)


def package_hashes():
    files = sorted(PACKAGE.iterdir())
    names = {"README.md", "PROOF.md", "TASK.json", "SOURCES.json", "VERIFY.json",
             "VALIDATION.md", "verify.py"}
    require({path.name for path in files} == names, "package file inventory")
    hashes = {}
    for path in files:
        require(path.is_file() and not path.is_symlink(), "regular package files")
        require(path.stat().st_size <= 1_048_576, "package byte bound")
        data = path.read_bytes()
        require(len(data) <= 1_048_576, "package byte bound")
        hashes[path.name] = hashlib.sha256(data).hexdigest()
    return hashes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, help="write a generated receipt outside the checkout")
    args = parser.parse_args()
    pairs, recipes, actual = check_dimensions()
    basis, payload_cases = check_payload()
    controls = check_controls(basis)
    result = {"status": "PASS_SINGLE_MERGE_CACHE_FLOOR", "dimension_pairs": pairs,
              "dimension_recipes": recipes, "reader497_recipes": len(actual),
              "payload_cases": payload_cases, "controls": controls,
              "python": platform.python_version(), "package_sha256": package_hashes(),
              "reader497_certificate": actual}
    if args.receipt:
        target = args.receipt.resolve()
        require(not target.is_relative_to(PACKAGE.parents[1]), "receipt must be outside checkout")
        encoded = json.dumps(result, indent=2)+"\n"
        require(target.write_text(encoded, encoding="utf-8") == len(encoded), "receipt write")
    summary = {key: result[key] for key in ("status", "dimension_pairs", "dimension_recipes",
                                          "reader497_recipes", "payload_cases", "controls")}
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
