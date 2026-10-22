#!/usr/bin/env python3
"""Failure controls for the selected BIT stock width exponent."""
import importlib.util
import os
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = importlib.util.spec_from_file_location(
    "selected_bit_stock", os.path.join(HERE, "verify.py"))
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def main():
    selected = MODULE.certificate()
    rejected = MODULE.certificate(Fraction(3, 1000))
    if rejected["adapter"] >= 0:
        raise SystemExit("3/1000 was accepted as an adapter")
    if rejected["guard"] == selected["guard"]:
        raise SystemExit("the two guards were treated as the same value")
    if MODULE.ordinary_saving(Fraction(1, 250)) != Fraction(8590884599, 2500000000000):
        raise SystemExit("ordinary saving moved")
    # A one-step larger atom still has to be checked against both slacks.
    # 1/200 = 0.005 is above the ordinary saving and still below 1 - R.
    wider = MODULE.certificate(Fraction(1, 200))
    if not (wider["adapter"] > 0 and wider["absorption"] > 0):
        raise SystemExit("control atom 1/200 lost a slack")
    if wider["guard"] == selected["guard"]:
        raise SystemExit("a different atom reproduced the selected guard")
    print("PASS_SELECTED_BIT_STOCK_WIDTH_TESTS controls=4")


if __name__ == "__main__":
    main()
