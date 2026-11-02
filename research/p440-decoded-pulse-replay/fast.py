#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Decode each fixed gate once before PR1431's complete forward-pulse replay.

Produced by Nick Petalas. The pulse interpreter adapts Hanson Sun's PR1431
independent.py; that source and its complete caller remain unchanged.
"""

import argparse
from fractions import Fraction
import hashlib
from pathlib import Path
import sys
from types import ModuleType

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "complex-p440-window-shocks" / "independent.py"
SOURCE_SHA256 = "f9013193a4e46aa045071f768c2815780b5a8051ff1158cd0ec917415ed1f941"


def load_source(raw=None):
    """Execute authenticated source bytes, without reading a bytecode cache."""
    data = SOURCE.read_bytes() if raw is None else raw
    if hashlib.sha256(data).hexdigest() != SOURCE_SHA256:
        raise ValueError("retained interpreter source hash mismatch")
    module = ModuleType("p440_retained_independent")
    module.__file__ = str(SOURCE)
    exec(compile(data, str(SOURCE), "exec"), module.__dict__)
    return module


def prepare(gates):
    """Retain original fields and append the immutable exact coefficient."""
    if len(gates) > 8192:
        raise ValueError("gate count exceeds the prepared replay contract")
    out = []
    for gate in gates:
        if gate is None:
            out.append(None)
        elif gate[0] == "add" and len(gate) in (5, 6):
            out.append((*gate, Fraction(gate[3], gate[4])))
        elif gate[0] == "scale" and len(gate) in (4, 5):
            out.append((*gate, Fraction(gate[2], gate[3])))
        else:
            raise ValueError("invalid gate")
    return tuple(out)


def run(gates, initial, pulses=None):
    """The source's state recurrence with a coefficient read, not a decode."""
    if len(gates) > 8192:
        raise ValueError("gate count exceeds the prepared replay contract")
    state = dict(initial)
    pulses = pulses or {}
    for index in range(len(gates) + 1):
        for donor, change in pulses.get(index, []):
            state[donor] = state.get(donor, 0) + change
            if not state[donor]:
                del state[donor]
        if index == len(gates) or gates[index] is None:
            continue
        gate = gates[index]
        value = state.get(gate[1], 0)
        coefficient = gate[-1]
        value = (value + coefficient * state.get(gate[2], 0)
                 if gate[0] == "add" else coefficient * value)
        if value:
            state[gate[1]] = value
        else:
            state.pop(gate[1], None)
    return state


def install(module):
    """Bind a private caller instance; no source file or shared module changes."""
    original = module.direct_windows

    def direct_windows(word):
        prepared = dict(word)
        prepared["B"] = list(prepare(word["B"]))
        prepared["cleanup"] = list(prepare(word["cleanup"]))
        return original(prepared)

    module.run = run
    module.direct_windows = direct_windows
    return module


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", action="store_true")
    args = parser.parse_args()
    module = load_source()
    if not args.baseline:
        install(module)
    sys.argv = [str(SOURCE)]
    module.main()


if __name__ == "__main__":
    main()
