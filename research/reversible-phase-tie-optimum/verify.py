#!/usr/bin/env python3
"""Exact residue certificate. Produced by Nick Petalas. Apache-2.0."""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path
import platform
import sys


def need(condition, message):
    if not condition:
        raise ValueError(message)


def forward(point, first=1, last=0):
    """0 means downward half ties, 1 upward half ties."""
    need(first in (0, 1) and last in (0, 1), "invalid tie rule")
    x, y = point
    u = x - (y + first) // 2
    v = y + (8 * u + 5) // 10
    return u - (v + last) // 2, v


def inverse(point, first=1, last=0):
    need(first in (0, 1) and last in (0, 1), "invalid tie rule")
    w, v = point
    u = w + (v + last) // 2
    y = v - (8 * u + 5) // 10
    return u + (y + first) // 2, y


def residual(point, image, sign=1):
    x, y = point
    w, v = image
    return 5 * w - 3 * x + 4 * sign * y, 5 * v - 4 * sign * x - 3 * y


def norm2(point):
    x, y = point
    return x * x + y * y


def reference_nearest(value, tie):
    """Separate Fraction/divmod oracle, including negative half integers."""
    low, remainder = divmod(value.numerator, value.denominator)
    twice = 2 * remainder
    if twice < value.denominator:
        return low
    if twice > value.denominator:
        return low + 1
    return low + tie


def reference(point, first, last):
    x, y = point
    x -= reference_nearest(Fraction(y, 2), first)
    y += reference_nearest(Fraction(4 * x, 5), 0)
    x -= reference_nearest(Fraction(y, 2), last)
    return x, y


def residue_certificate():
    results = []
    for first, last in product(range(2), repeat=2):
        counts = Counter()
        witness = None
        maximum = -1
        for point in product(range(5), range(10)):
            image = forward(point, first, last)
            need(image == reference(point, first, last), "rational oracle")
            error = residual(point, image)
            counts[error] += 1
            if norm2(error) > maximum:
                maximum, witness = norm2(error), [list(point), list(image)]
            for step, output_step in (((5, 0), (3, 4)), ((0, 10), (-8, 6))):
                translated = tuple(a + b for a, b in zip(point, step))
                expected = tuple(a + b for a, b in zip(image, output_step))
                need(forward(translated, first, last) == expected, "period generator")
        need(maximum == (25 if first == last else 20), "sharp fixed-tie maximum")
        need(sum(counts.values()) == 50, "complete fundamental rectangle")
        results.append({"ties": [first, last], "max_error_squared_times_25": maximum,
                        "witness": witness,
                        "residual_counts": [[list(k), v] for k, v in sorted(counts.items())]})
    return results


def check_grid():
    cases = 0
    for first, last in product(range(2), repeat=2):
        images = set()
        limit = 25 if first == last else 20
        for point in product(range(-40, 41), repeat=2):
            image = forward(point, first, last)
            preimage = inverse(point, first, last)
            need(inverse(image, first, last) == point, "left inverse")
            need(forward(preimage, first, last) == point, "right inverse")
            need(norm2(residual(point, image)) <= limit, "forward error")
            need(norm2(residual(point, preimage, -1)) <= limit, "inverse error")
            images.add(image)
            cases += 1
        need(len(images) == 81 * 81, "finite injection")
    return cases


def check_translates():
    cases = 0
    for first, last in product(range(2), repeat=2):
        for bits in (1, 4, 16, 64, 256, 1024, 4096):
            for sx, sy in product((-1, 1), repeat=2):
                a, b = sx * (1 << bits), sy * ((1 << bits) + 1)
                shift = (5 * a, 10 * b)
                out_shift = (3 * a - 8 * b, 4 * a + 6 * b)
                for point in product(range(5), range(10)):
                    translated = tuple(x + y for x, y in zip(point, shift))
                    image = forward(translated, first, last)
                    expected = tuple(x + y for x, y in
                                     zip(forward(point, first, last), out_shift))
                    need(image == expected, "large signed translation")
                    need(image == reference(translated, first, last), "large rational oracle")
                    need(inverse(image, first, last) == translated, "large exact return")
                    cases += 1
    return cases


def check_radial_family():
    cases = 0
    for n in (1, 2, 4, 8, 16, 256, 65536, 1 << 128):
        point = (-5 * n, 3 - 10 * n)
        image = forward(point)
        need(image == (5 * n - 2, 1 - 10 * n), "radial equality family")
        need(residual(point, image) == (2, -4), "constant sharp residual")
        need(norm2(point) == 125 * n * n - 60 * n + 9, "input radius polynomial")
        need(norm2(image) - norm2(point) == 20 * n - 4, "outward radius polynomial")
        cases += 1
    return cases


def check_controls():
    point = (0, 3)
    image = forward(point)
    need(image == (-2, 1), "sharp mixed-tie witness")
    controls = {
        "smaller_squared_constant_19_over_25": norm2(residual(point, image)) > 19,
        "equal_upward_ties_at_4_over_5": norm2(residual(point, forward(point, 1, 1))) > 20,
        "equal_downward_ties_at_4_over_5": norm2(residual((0, 5), forward((0, 5), 0, 0))) > 20,
        "closed_disk_return": norm2(forward((-5, -7))) > norm2((-5, -7)),
        "clipping_keeps_inverse": inverse((0, 0)) != (-5, -7),
        "rounding_ties_does_not_matter": forward(point, 1, 1) != image,
    }
    w, v = image
    u = w + (v + 1) // 2
    y = v - (8 * u + 5) // 10
    wrong_inverse = (u + (y + 1) // 2, y)
    controls["inverse_uses_other_last_tie"] = wrong_inverse != point
    point = (-3, -3)
    u = point[0] - int(Fraction(point[1], 2))
    v = point[1] + (8 * u + 5) // 10
    wrong_forward = (u - int(Fraction(v, 2)), v)
    controls["truncate_negative_halves"] = wrong_forward != forward(point)
    for name, detected in controls.items():
        need(detected, "undetected semantic mutant: " + name)
    for first, last in ((-1, 0), (0, 2), (3, 3)):
        for operation in (forward, inverse):
            try:
                operation((0, 0), first, last)
            except ValueError:
                continue
            raise ValueError("invalid tie rule accepted")
    return sorted(controls)


def run():
    table = residue_certificate()
    grid_cases = check_grid()
    translation_cases = check_translates()
    radial_cases = check_radial_family()
    controls = check_controls()
    return {"status": "PASS_REVERSIBLE_PHASE_TIE_OPTIMUM",
            "claim_type": "scoped proof with exact finite corroboration",
            "phase": ["3/5", "4/5"], "sharp_squared_error_over_grid_squared": "4/5",
            "optimal_fixed_tie_pairs": [[0, 1], [1, 0]],
            "residue_cases": 200, "residue_table": table,
            "grid_cases": grid_cases, "large_translation_cases": translation_cases,
            "radial_family_cases": radial_cases, "semantic_controls": controls,
            "invalid_tie_rejections": 6,
            "limits": "Four fixed tie pairs only; outward slack permitted; no physical caller or kappa claim."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="exclusively write a generated hash-bound receipt")
    args = parser.parse_args()
    result = run()
    here = Path(__file__).resolve().parent
    names = ("README.md", "PROOF.md", "TASK.json", "SOURCES.json", "VERIFY.json", "verify.py")
    receipt = {"result": result,
               "package_sha256": {name: hashlib.sha256((here / name).read_bytes()).hexdigest()
                                  for name in names},
               "environment": {"python": sys.version, "platform": platform.platform()}}
    serialized = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        with args.output.open("x", encoding="utf-8") as target:
            need(target.write(serialized) == len(serialized), "partial receipt write")
    print(serialized, end="")


if __name__ == "__main__":
    main()
