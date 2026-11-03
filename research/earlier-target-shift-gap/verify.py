#!/usr/bin/env python3
"""Earlier-target frame506 shifts are the reversed-field shear conjugate.

The committed helper-462 route is not modified. This checker re-derives its
ordered-shift census and compares the source reversed-field stream operation
with an axis swap around the forward shear.
"""

from collections import Counter
from fractions import Fraction
from gzip import GzipFile
from importlib import import_module
from json import load
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "research/bit-row-route-generator/PROGRAM.json.gz"
QADIC = ROOT / "research/selected-bit-stream-routes/qadic_streams.py"


class CheckFailure(Exception):
    pass


def require(condition, message):
    if not condition:
        raise CheckFailure(message)


def factors(matrix):
    """Right-looking elimination, copied as a separate implementation."""
    rows = [[Fraction(entry) for entry in row] for row in matrix]
    result = []
    size = len(rows)
    for pivot in range(size):
        swap = next((row for row in range(pivot, size) if rows[row][pivot]), None)
        require(swap is not None, "singular matcher")
        if swap != pivot:
            rows[pivot], rows[swap] = rows[swap], rows[pivot]
            result.append(("swap", pivot, swap, Fraction(1)))
        scale = rows[pivot][pivot]
        if scale != 1:
            rows[pivot] = [value / scale for value in rows[pivot]]
            result.append(("scale", pivot, pivot, scale))
        for row in range(size):
            coefficient = rows[row][pivot]
            if row != pivot and coefficient:
                rows[row] = [left - coefficient * right for left, right in zip(rows[row], rows[pivot])]
                result.append(("add", row, pivot, coefficient))
    return tuple(result)


def route_factors(elimination, direction):
    if direction == 1:
        return elimination
    reversed_steps = []
    for kind, row, column, coefficient in reversed(elimination):
        if kind == "scale":
            coefficient = 1 / coefficient
        elif kind == "add":
            coefficient = -coefficient
        reversed_steps.append((kind, row, column, coefficient))
    return tuple(reversed_steps)


def expand_shifts(elimination, width, direction):
    """Address expansion from the route generator's row/lane loops."""
    dimension = 8 * width
    shifts = []
    for kind, source_block, target_block, coefficient in route_factors(elimination, direction):
        if kind != "add":
            continue
        for row in range(dimension):
            for lane in range(width):
                source = row * dimension + source_block * width + lane
                target = row * dimension + target_block * width + lane
                shifts.append((target, source, coefficient.numerator, coefficient.denominator))
    return shifts


def program_routes(program):
    routes = []
    current = None
    for step in program["steps"]:
        if step["op"] == "route_enter":
            require(current is None, "nested route")
            current = []
        elif step["op"] == "route_return":
            require(current is not None, "route return without entry")
            routes.append(current)
            current = None
        elif step["op"] == "ordered_shift":
            require(current is not None, "shift outside a route")
            numerator, denominator = step["coefficient"]
            current.append((step["addresses"][0], step["addresses"][1], numerator, denominator))
    require(current is None, "unclosed route")
    return routes


def classify(shifts):
    earlier = later = 0
    for target, source, _numerator, _denominator in shifts:
        require(target != source, "ordered shift aliases its source")
        if target < source:
            earlier += 1
        else:
            later += 1
    return earlier, later


def pack(shape, values):
    before, high, middle, suffix = shape
    bits = []
    for prefix in range(before):
        for first in range(high):
            for gap in range(middle):
                for second in range(high):
                    for tail in range(suffix):
                        bits.append(values[prefix][first][gap][second][tail])
    return bits


def unpack(shape, bits):
    before, high, middle, suffix = shape
    cursor = iter(bits)
    return [[[[[next(cursor) for _tail in range(suffix)]
               for _second in range(high)]
              for _gap in range(middle)]
             for _first in range(high)]
            for _prefix in range(before)]


def swap_axes(shape, values):
    before, high, middle, suffix = shape
    swapped = [[[[[0 for _tail in range(suffix)]
                  for _second in range(high)]
                 for _gap in range(middle)]
                for _first in range(high)]
               for _prefix in range(before)]
    for prefix in range(before):
        for first in range(high):
            for gap in range(middle):
                for second in range(high):
                    for tail in range(suffix):
                        swapped[prefix][second][gap][first][tail] = values[prefix][first][gap][second][tail]
    return swapped


def load_qadic():
    sys.path.insert(0, str(QADIC.parent))
    return import_module("qadic_streams")


def shear(module, values, shape, coefficient, carry, reversed_fields):
    before, high, middle, suffix = shape
    meter = module.Meter()
    source = module.Tape(meter, pack(shape, values))
    output = module.add_high(
        source, high, coefficient, lambda _prefix: carry,
        before, middle, suffix, reversed_fields)
    return unpack(shape, output.bits), meter


def pattern(shape, salt):
    before, high, middle, suffix = shape
    return [[[[[(salt + 3 * prefix + 5 * first + 7 * gap + 11 * second + 13 * tail) & 1
                 for tail in range(suffix)]
                for second in range(high)]
               for gap in range(middle)]
              for first in range(high)]
             for prefix in range(before)]


def conjugation_case(module, shape, coefficient, carry, salt):
    values = pattern(shape, salt)
    reversed_values, reversed_meter = shear(
        module, values, shape, coefficient, carry, True)
    forward_values, forward_meter = shear(
        module, swap_axes(shape, values), shape, coefficient, carry, False)
    conjugated = swap_axes(shape, forward_values)
    require(reversed_values == conjugated, "reversed-field shear is not the axis conjugate")
    require(len(reversed_meter.ordinary) == 2, "reversed-field path must record two swap oracles")
    require(forward_meter.ordinary == [], "forward shear must not call the swap oracle")
    require(reversed_values != forward_values, "reversed and forward shears unexpectedly agree")


def positive(module, program, elimination):
    require(program["owners"] == [462, 461], "helper 462 with spectator 461")
    require(program["f"] == 1, "committed witness is the f=1 route")
    counts = Counter(kind for kind, _row, _column, _coefficient in elimination)
    require(counts == Counter(swap=5, scale=5, add=14), "frame506 factor census")
    early_adds = [step for step in elimination if step[0] == "add" and step[2] < step[1]]
    late_adds = [step for step in elimination if step[0] == "add" and step[2] > step[1]]
    require(len(early_adds) == 4 and len(late_adds) == 10, "four earlier block pairs")
    routes = program_routes(program)
    require(len(routes) == 2, "two route directions")
    for direction, actual in zip((1, -1), routes):
        require(expand_shifts(elimination, 1, direction) == actual,
                "independent expansion disagrees with the committed route")
    for width in (1, 2, 3):
        shifts = expand_shifts(elimination, width, 1) + expand_shifts(elimination, width, -1)
        earlier, later = classify(shifts)
        require((earlier, later) == (64 * width * width, 160 * width * width),
                "site formula failed at width " + str(width))
    conjugation_case(module, (1, 3, 2, 2), Fraction(1, 2), 0, 1)
    conjugation_case(module, (2, 3, 1, 1), Fraction(-2, 1), 1, 4)
    conjugation_case(module, (1, 4, 1, 3), Fraction(1, 1), 0, 9)
    # The high=1 branch returns before either swap. It is not an earlier-target site.
    trivial, trivial_meter = shear(module, pattern((1, 1, 1, 1), 2), (1, 1, 1, 1), Fraction(1), 0, True)
    require(trivial == pattern((1, 1, 1, 1), 2), "width-one high axis is the identity")
    require(trivial_meter.ordinary == [], "identity axis records no oracle")


def failure_controls(module, elimination):
    def wrong_direction():
        shifts = expand_shifts(elimination, 1, 1)
        # Negating coefficients is the reverse route, not the forward route.
        negated = [(target, source, -numerator, denominator)
                   for target, source, numerator, denominator in shifts]
        require(negated == shifts, "forward and negated routes were treated as equal")

    def single_swap():
        shape = (1, 3, 1, 1)
        values = pattern(shape, 8)
        reversed_values, _meter = shear(module, values, shape, Fraction(1), 0, True)
        once = shear(module, swap_axes(shape, values), shape, Fraction(1), 0, False)[0]
        require(reversed_values == once, "one axis swap was accepted as a conjugation")

    for label, check in (("negated forward route", wrong_direction),
                         ("one-sided axis swap", single_swap)):
        try:
            check()
        except CheckFailure:
            continue
        raise CheckFailure("failure control did not fire: " + label)


def main():
    with GzipFile(PROGRAM) as handle:
        program = load(handle)
    matrix = tuple(tuple(Fraction(entry) for entry in row) for row in program["matcher"])
    elimination = factors(matrix)
    module = load_qadic()
    positive(module, program, elimination)
    failure_controls(module, elimination)
    print("PASS_EARLIER_TARGET_SHIFT_GAP earlier=64*f^2 later=160*f^2 oracle_calls=2")


if __name__ == "__main__":
    try:
        main()
    except CheckFailure as exc:
        raise SystemExit("FAIL_EARLIER_TARGET_SHIFT_GAP " + str(exc)) from exc
