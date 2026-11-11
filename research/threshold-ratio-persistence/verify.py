#!/usr/bin/env python3
"""Integer checks for the section-6 threshold comparison.

The proof is in PROOF.md. These checks do not search for a cutoff and do
not discharge precision_tape. Raises are used so python -O still fails closed.
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SELECTED = ROOT / "certificates/selected-result.json"
REVIEW = ROOT / "docs/research/pr-intake-evidence/pr7000-application/PROOF-REVIEW.md"
SENTENCE = (
    "choose an integer j beyond `4d0/\u03b4` with\n"
    "`C(j+1)^d0 <= 2^(\u03b4j)` and freeze the input threshold at least 2^j. "
    "Subsequent\nratios decrease, so the inequality holds thereafter."
)


def die(message):
    raise SystemExit(message)


def holds(c_value, degree, numerator, denominator, index):
    if index < 0:
        return False
    left = pow(c_value, denominator) * pow(index + 1, degree * denominator)
    return left <= (1 << (numerator * index))


def witness(c_value, degree, numerator, denominator):
    """Return (j, T, L) for the explicit index in PROOF.md."""
    if c_value < 1 or degree < 0 or numerator < 1 or denominator < 1:
        die("witness domain")
    length = c_value.bit_length() * denominator + numerator + degree * denominator
    if length < 2:
        die("bit-length parameter")
    log_term = (length - 1).bit_length()
    power = 2 * log_term + 2
    return (1 << power) - 1, power, length, log_term


def step_holds(degree, numerator, denominator, modulus):
    """(m+1)^{d0 b} <= m^{d0 b} * 2^a, the one-step persistence comparison."""
    if modulus < 1:
        return False
    exponent = degree * denominator
    return pow(modulus + 1, exponent) <= pow(modulus, exponent) * (1 << numerator)


def main():
    selected = json.loads(SELECTED.read_text(encoding="utf-8"))
    if selected.get("kappa") != "363005817/100000000000":
        die("selected kappa changed")
    if selected.get("decimal") != "0.00363005817":
        die("selected decimal changed")
    names = [row.get("id") for row in selected.get("assumptions", [])]
    if names != [
        "native_all_columns",
        "owned_erasure",
        "compiler",
        "precision_tape",
        "analytic_recovery",
    ]:
        die("assumption ids changed")
    review = REVIEW.read_text(encoding="utf-8")
    if review.count(SENTENCE) != 1:
        die("section-6 sentence missing or duplicated")

    proof_rows = 0
    direct_rows = 0
    for c_value in range(1, 13):
        for degree in range(0, 7):
            for numerator in range(1, 6):
                for denominator in range(1, 6):
                    index, power, length, log_term = witness(
                        c_value, degree, numerator, denominator)
                    two_log = 1 << log_term
                    if two_log < length:
                        die("ceil log short")
                    if (1 << power) != 4 * two_log * two_log:
                        die("power split")
                    if 4 * length < 2 * log_term + 2:
                        die("linear room")
                    right = length + (power - 1) * degree * denominator
                    if right > power * length:
                        die("linear majorant")
                    if numerator * (1 << power) < c_value.bit_length() * denominator + numerator + power * degree * denominator:
                        die("exponent budget")
                    if degree:
                        threshold = math.ceil(8 * degree * denominator / (5 * numerator))
                        if (1 << power) < threshold:
                            die("witness below persistence threshold")
                        if not step_holds(degree, numerator, denominator, 1 << power):
                            die("witness step")
                    if numerator * index <= 4000:
                        if not holds(c_value, degree, numerator, denominator, index):
                            die("direct predicate")
                        if degree and not holds(c_value, degree, numerator, denominator, index + 1):
                            die("next predicate")
                        direct_rows += 1
                    proof_rows += 1

    ratio_rows = 0
    for degree in range(1, 16):
        for numerator in range(1, 9):
            for denominator in range(1, 9):
                threshold = math.ceil(8 * degree * denominator / (5 * numerator))
                if not step_holds(degree, numerator, denominator, threshold):
                    die("threshold step")
                span = 4 * degree * denominator / numerator
                floor_span = math.floor(span)
                ceil_small = math.ceil(2 * span / 5)
                if floor_span + 2 < ceil_small:
                    die("review factor")
                ratio_rows += 1

    # (1+1/m)^m < 3 as an integer comparison, m = 1..48.
    for modulus in range(1, 49):
        if pow(modulus + 1, modulus) >= 3 * pow(modulus, modulus):
            die("binomial bound")

    # The stated ceiling is sharp by one step at this single triple.
    if math.ceil(8 * 1 * 5 / (5 * 2)) != 4:
        die("sharpness ceiling")
    if step_holds(1, 2, 5, 3):
        die("m=3 should fail")
    if not step_holds(1, 2, 5, 4):
        die("m=4 should hold")

    # j > 4 d0/delta alone does not force the predicate.
    if holds(1000, 1, 1, 1, 5):
        die("bare review index should fail")
    if not holds(1000, 1, 1, 1, witness(1000, 1, 1, 1)[0]):
        die("large witness")

    # Degree zero persists by growth of the pure power of two.
    if not holds(5, 0, 1, 3, 8):
        die("degree zero base")
    if not holds(5, 0, 1, 3, 9):
        die("degree zero next")

    print(
        "PASS_THRESHOLD_RATIO_PERSISTENCE"
        f" proof_rows={proof_rows}"
        f" direct_rows={direct_rows}"
        f" ratio_rows={ratio_rows}"
        " sharpness=1,2,5,4"
        " kappa=363005817/100000000000"
        " no_new_kappa=true"
    )


if __name__ == "__main__":
    main()
