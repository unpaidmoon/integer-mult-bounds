"""Exact iterated native-loop drift certificate, produced by Nick Petalas.

Apache-2.0. The signed recipes are JoyboyBrian / PR5492's unchanged input.
No predecessor executable is imported or run.
"""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import random

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[1]
SOURCE = "research/native-rounded-loop-defect/RECIPES.json"
SOURCE_HASH = "97f769fe20aada89d065f538af137f6385d4fbcdb21e0832dd850429f679b8b2"
SUPPORT = (1, 10, 39, 44)
START = ((3, 2), (1, 0), (0, 3), (3, 1))
DRIFT = ((-4, 4), (4, 4), (4, 4), (4, -4))
STEPS = ((0, True), (1, False), (2, False), (3, True))
# Each pair lists (input index, input phase, output index, output phase).
# Indices here refer to SUPPORT, not the 512-coordinate ambient bank.
CIRCUIT = (
    (((0, 0, 2, 1), (2, 2, 0, 3)), ((1, 0, 1, 0), (3, 2, 3, 2))),
    (((0, 0, 0, 0), (1, 2, 1, 2)), ((3, 3, 2, 0), (2, 1, 3, 2))),
    (((2, 3, 0, 0), (0, 1, 2, 2)), ((1, 0, 1, 0), (3, 2, 3, 2))),
    (((0, 0, 0, 0), (1, 2, 1, 2)), ((2, 0, 3, 1), (3, 2, 2, 3))),
)


def need(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def rotate(value, phase):
    real, imag = value
    return ((real, imag), (-imag, real), (-real, -imag), (imag, -real))[phase % 4]


def lifting_pair(a, b, inverse=False, require_even=False):
    difference = (a[0] - b[0], a[1] - b[1])
    if require_even:
        need(all(x % 2 == 0 for x in difference), "shift difference must be even")
    middle = (b[0] + difference[0] // 2, b[1] + difference[1] // 2)
    turned = rotate(difference, -1 if inverse else 1)
    second = (middle[0] - turned[0] // 2, middle[1] - turned[1] // 2)
    return (second[0] + turned[0], second[1] + turned[1]), second


def compile_wrapper(record):
    expected = {"matrix_rows", "offset", "linear_Z4", "quadratic_rows", "phase"}
    need(type(record) is dict and set(record) == expected, "wrapper schema")
    rows, linear, quadratic = (record[k] for k in
                               ("matrix_rows", "linear_Z4", "quadratic_rows"))
    need(all(type(v) is list and len(v) == 9 for v in (rows, linear, quadratic)),
         "wrapper dimension")
    need(all(type(x) is int and 0 <= x < 512 for x in rows + quadratic), "binary row")
    need(all(type(x) is int and 0 <= x < 4 for x in linear), "linear phase")
    need(type(record["offset"]) is int and 0 <= record["offset"] < 512, "offset")
    need(type(record["phase"]) is int and 0 <= record["phase"] < 4, "global phase")
    result = []
    for x in range(512):
        y = record["offset"]
        for j, row in enumerate(rows):
            y ^= ((row & x).bit_count() % 2) << j
        phase = record["phase"] + sum(((x >> j) & 1) * linear[j] for j in range(9))
        phase += 2 * sum(((x >> j) & 1) * ((x >> k) & 1) * ((quadratic[j] >> k) & 1)
                         for j in range(9) for k in range(j + 1, 9))
        result.append((y, phase % 4))
    need(sorted(y for y, _ in result) == list(range(512)), "wrapper bijection")
    return tuple(result)


def inverse_wrapper(plan):
    result = [None] * 512
    for x, (y, phase) in enumerate(plan):
        result[y] = (x, -phase % 4)
    need(all(value is not None for value in result), "inverse wrapper totality")
    return tuple(result)


def load_source():
    path = ROOT / SOURCE
    need(path.stat().st_size <= 65536, "source size bound")
    raw = path.read_bytes()
    need(sha256(raw).hexdigest() == SOURCE_HASH, "source authentication")
    records = json.loads(raw)
    need(type(records) is list and len(records) == 4, "four native recipes")
    plans = []
    for record in records:
        need(type(record) is dict and set(record) == {"left", "right", "rank"},
             "native recipe schema")
        need(type(record["rank"]) is int and record["rank"] == 1, "native rank")
        plans.append((compile_wrapper(record["left"]), compile_wrapper(record["right"])))
    return records, tuple(plans)


def derive_circuit(plans):
    circuit = []
    for j, inverse in STEPS:
        left, right = plans[j]
        before, after = ((inverse_wrapper(left), inverse_wrapper(right))
                         if inverse else (right, left))
        entries = {before[x][0]: (i, before[x][1]) for i, x in enumerate(SUPPORT)}
        need(len(entries) == 4, "four distinct kernel entries")
        pairs = []
        for address in sorted(entries):
            if address % 2:
                continue
            need(address + 1 in entries, "support closed under kernel pairing")
            pair = []
            for t in (address, address + 1):
                output, phase = after[t]
                need(output in SUPPORT, "support closed under wrapper output")
                pair.append((*entries[t], SUPPORT.index(output), phase))
            pairs.append(tuple(pair))
        need(len(pairs) == 2, "exactly two active pairs")
        circuit.append(tuple(pairs))
    need(tuple(circuit) == CIRCUIT, "literal four-coordinate circuit")


def reduced_edge(values, stage, circuit=CIRCUIT, require_even=False):
    output = [None] * 4
    for first, second in circuit[stage]:
        a = rotate(values[first[0]], first[1])
        b = rotate(values[second[0]], second[1])
        c, d = lifting_pair(a, b, STEPS[stage][1], require_even)
        output[first[2]] = rotate(c, first[3])
        output[second[2]] = rotate(d, second[3])
    need(all(value is not None for value in output), "reduced edge totality")
    return tuple(output)


def reduced_loop(values, circuit=CIRCUIT):
    for stage in range(4):
        values = reduced_edge(values, stage, circuit)
    return values


def literal_wrapper(values, record, inverse):
    """Second decoder: explicit bit sums rather than compiled wrapper plans."""
    output = [None] * 512
    for x in range(512):
        bits = tuple((x >> j) & 1 for j in range(9))
        y = record["offset"]
        for j in range(9):
            parity = sum(bits[k] * ((record["matrix_rows"][j] >> k) & 1)
                         for k in range(9)) % 2
            y ^= parity << j
        phase = record["phase"] + sum(bits[j] * record["linear_Z4"][j] for j in range(9))
        phase += 2 * sum(bits[j] * bits[k] * ((record["quadratic_rows"][j] >> k) & 1)
                         for j in range(9) for k in range(j + 1, 9))
        if inverse:
            output[x] = rotate(values[y], -phase)
        else:
            output[y] = rotate(values[x], phase)
    need(all(value is not None for value in output), "literal wrapper totality")
    return output


def literal_edge(values, record, inverse):
    values = literal_wrapper(values, record["left" if inverse else "right"], inverse)
    for x in range(0, 512, 2):
        ar, ai = values[x]
        br, bi = values[x + 1]
        dr, di = ar - br, ai - bi
        # Independent component formula; ceil(t/2) = -floor(-t/2).
        first = (br + dr // 2 - di // 2, bi + di // 2 - (-dr // 2))
        second = (br + dr // 2 - (-di // 2), bi + di // 2 - dr // 2)
        values[x], values[x + 1] = (second, first) if inverse else (first, second)
    return literal_wrapper(values, record["right" if inverse else "left"], inverse)


def embed(values):
    result = [(0, 0)] * 512
    for address, value in zip(SUPPORT, values, strict=True):
        result[address] = value
    return result


def translate(values, multiplier):
    return tuple((a + multiplier * c, b + multiplier * d)
                 for (a, b), (c, d) in zip(values, DRIFT, strict=True))


def check_orbit(records):
    reduced, literal = START, embed(START)
    orbit, cuts = [reduced], []
    for _ in range(24):
        for stage, (j, inverse) in enumerate(STEPS):
            reduced = reduced_edge(reduced, stage)
            literal = literal_edge(literal, records[j], inverse)
            need(literal == embed(reduced), "independent full-bank orbit edge")
            cuts.append(reduced)
        orbit.append(reduced)
    need(reduced == translate(START, 1), "24-traversal nonzero drift identity")
    need(any(value != (0, 0) for value in DRIFT), "drift nonzero")
    need(sum(a * a + b * b for a, b in DRIFT) == 128, "squared drift norm")
    return tuple(orbit), sha256(canonical(cuts)).hexdigest()


def check_covariance():
    shifts = [DRIFT]
    shift = DRIFT
    for stage in range(4):
        shift = reduced_edge(shift, stage, require_even=True)
        shifts.append(shift)
    need(shift == DRIFT, "shift returns exactly")
    rng = random.Random(5492)
    for case in range(128):
        width = 4 if case < 64 else 80
        values = tuple((rng.getrandbits(width + 1) - (1 << width),
                        rng.getrandbits(width + 1) - (1 << width)) for _ in range(4))
        multiplier = case - 64
        need(reduced_loop(translate(values, multiplier)) ==
             translate(reduced_loop(values), multiplier), "signed covariance fixture")
    return shifts


def check_pair_oracle():
    count = 0
    for ar in range(-3, 4):
        for ai in range(-3, 4):
            for br in range(-3, 4):
                for bi in range(-3, 4):
                    a, b = (ar, ai), (br, bi)
                    c, d = lifting_pair(a, b)
                    need(lifting_pair(c, d, True) == (a, b), "pair two-sided inverse")
                    dr, di = ar - br, ai - bi
                    expected = ((br + dr // 2 - di // 2, bi + di // 2 - (-dr // 2)),
                                (br + dr // 2 - (-di // 2), bi + di // 2 - dr // 2))
                    need((c, d) == expected, "independent component formula")
                    count += 1
    return count


def check_iterates(orbit):
    values = START
    for n in range(24 * 32 + 1):
        quotient, remainder = divmod(n, 24)
        need(values == translate(orbit[remainder], quotient), "complete iterate formula")
        if n < 24 * 32:
            values = reduced_loop(values)
    collision_inputs = []
    for k in range(33):
        values = translate(START, -k)
        collision_inputs.append(values)
        for _ in range(24 * k):
            values = reduced_loop(values)
        need(values == START, "correction decoder collision family")
    need(len(set(collision_inputs)) == 33, "distinct original inputs at one payload")
    return 24 * 32 + 1, len(collision_inputs)


def check_controls():
    failures = 0
    try:
        lifting_pair((1, 0), (0, 0), require_even=True)
    except ValueError as error:
        need(str(error) == "shift difference must be even", "exact parity rejection")
        failures += 1
    need(failures == 1, "odd shift rejected")
    values = START
    for _ in range(12):
        values = reduced_loop(values)
    need(values != START and values != translate(START, 1), "false short-period control")
    failures += 1
    altered = [[list(pair) for pair in stage] for stage in CIRCUIT]
    entry = list(altered[0][0][0])
    entry[3] = (entry[3] + 1) % 4
    altered[0][0][0] = tuple(entry)
    values = START
    for _ in range(24):
        values = reduced_loop(values, altered)
    need(values != translate(START, 1), "absolute wrapper phase control")
    failures += 1
    need(translate(START, -1) != translate(START, 1), "drift sign control")
    failures += 1
    values = ((1, 0), (0, 0), (0, 0), (0, 0))
    before = values
    for _ in range(12):
        values = reduced_loop(values)
    need(values == before, "periodic positive control")
    need(reduced_loop(((0, 0),) * 4) == ((0, 0),) * 4, "zero positive control")
    return failures, 2


def run():
    records, plans = load_source()
    derive_circuit(plans)
    orbit, cut_hash = check_orbit(records)
    shifts = check_covariance()
    pair_cases = check_pair_oracle()
    iterates, collisions = check_iterates(orbit)
    rejection_controls, positive_controls = check_controls()
    files = sorted(path for path in PACKAGE.iterdir() if path.is_file())
    need(len(files) <= 16 and all(path.stat().st_size <= 1048576 for path in files),
         "package inventory bound")
    return {
        "status": "PASS_NATIVE_LOOP_LINEAR_DRIFT", "support": SUPPORT,
        "start": START, "drift": DRIFT, "drift_squared_norm": 128,
        "orbit": orbit, "shift_cuts": shifts, "orbit_edge_sha256": cut_hash,
        "independent_full_bank_edges": 96, "shift_pair_evenness_checks": 8,
        "covariance_fixtures": 128, "pair_oracle_cases": pair_cases,
        "iterate_formula_checks": iterates, "same_payload_distinct_inputs": collisions,
        "rejection_controls": rejection_controls, "positive_controls": positive_controls,
        "source_sha256": SOURCE_HASH,
        "package_sha256": {path.name: sha256(path.read_bytes()).hexdigest() for path in files},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--check-receipt", type=Path)
    args = parser.parse_args()
    need(not (args.receipt and args.check_receipt), "one receipt mode")
    result = canonical(run()) + b"\n"
    if args.receipt:
        need(args.receipt.is_absolute() and not args.receipt.is_relative_to(ROOT),
             "receipt must be outside the checkout")
        with args.receipt.open("xb") as stream:
            need(stream.write(result) == len(result), "complete receipt write")
    if args.check_receipt:
        need(args.check_receipt.stat().st_size <= 1048576, "receipt size bound")
        need(args.check_receipt.read_bytes() == result, "generated receipt equality")
    print(result.decode(), end="")


if __name__ == "__main__":
    main()
