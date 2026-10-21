#!/usr/bin/env python3
"""Failure controls for the Pi helper-slot certificate. Loads verify.py by path."""

import importlib.util
from pathlib import Path

_PATH = Path(__file__).resolve().parent / "verify.py"
_SPEC = importlib.util.spec_from_file_location("p104_pi_helper_slot_verify", _PATH)
verify = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(verify)


def require(condition, message):
    if not condition:
        raise SystemExit("FAIL_P104_PI_HELPER_SLOT_TESTS " + message)


def test_dropped_third_addition():
    x, y = verify.F(4), verify.F(9)
    x = x + y
    y = x - y
    require((x, y) != (verify.F(9), verify.F(4)), "two-step exchange must fail")


def test_helper_mutation_rejected():
    mask = verify.published_mask()
    r = [verify.F(1)] * 104
    w = [verify.F(2)] * 104
    image = verify.apply_pi(r, w, verify.F(5), mask)
    require(image[2] == verify.F(5), "Pi keeps the helper")
    require((image[0], image[1], image[2] + 1) != image, "a mutated helper is not Pi")


def test_gate_is_not_cleared_by_the_invoice():
    gate = verify.scaffold_gate()
    require(gate["excess"] == 44096, "pinned excess")
    require(gate["lower"] + 288 > gate["capacity"], "exchange does not make the bill favorable")
    require(gate["excess"] > 81, "one chart gap is smaller than the excess and does not erase it")


def main():
    test_dropped_third_addition()
    test_helper_mutation_rejected()
    test_gate_is_not_cleared_by_the_invoice()
    verify.main()
    print("PASS_P104_PI_HELPER_SLOT_TESTS groups=3")


if __name__ == "__main__":
    main()
