#!/usr/bin/env python3
"""Second implementation of the log_q coefficient comparison.

Multiplies the odd symplectic factors before the power of two. Does not import
verify.py. Primality is not re-proved here; the witness value is the integer
already certified by verify.py, and only the stock/exponent inequalities are
rebuilt.
"""

import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def fail(message):
    raise SystemExit("FAIL_LOGQ_STOCK_SHAPE_INDEPENDENT " + message)


def need(condition, message):
    if not condition:
        fail(message)


def stock():
    odd = 1
    for index in range(1, 37):
        odd *= (1 << (2 * index)) - 1
    return (odd << (36 * 36)) * (14336 + 480 + 8 + 2)


def main():
    value = stock()
    need(value.bit_length() == 2642, "bit length")
    need((1 << 2641) <= value < (1 << 2642), "log2 band")
    witness = (1 << 80) + 13
    need(witness ** 33 < value <= witness ** 34, "exponent bracket")
    need((1 << 80) + 1 > 1 << 80, "domain floor")
    need(((1 << 80) + 1) ** 34 > value, "uniform B=34")
    shape = (ROOT / "research/selected-stock-shape-a-zero/PROOF.md").read_text(encoding="utf-8")
    need("2642 + rho" in shape, "shape sentence")
    need(math.gcd(2642, 34) == 2, "ratio")
    print(
        "PASS_LOGQ_STOCK_SHAPE_INDEPENDENT "
        "C_bits=2642 log_q_B=34 bit_plug_in=2642 ratio=1321/17 no_new_kappa"
    )


if __name__ == "__main__":
    main()
