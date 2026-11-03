"""Exact mode-preserving rounding obstruction, produced by Nick Petalas."""

from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = "research/coded-native-caller/NORMALIZERS.json"
SUPPORT = (0, 7, 20, 111)
ROWS = (
    (1, 1, 1, 1, 0, 0, 0, 0),
    (-1, -1, 1, 1, 0, 0, 0, 0),
    (0, 0, 0, 0, 1, -1, 1, 1),
    (0, 0, 0, 0, 1, -1, -1, -1),
)
TARGET = (0, 0, 1, 1, 1, -1, 0, 0)


def need(condition, message):
    if not condition:
        raise ValueError(message)


def bounded_read(path):
    need(path.is_file() and not path.is_symlink(), "regular input required")
    need(path.stat().st_size <= 1_048_576, "input size limit")
    return path.read_bytes()


def parse_modes(raw, digest):
    need(hashlib.sha256(raw).hexdigest() == digest, "source hash")
    modes = json.loads(raw)["mode_columns"]
    validate_modes(modes)
    return tuple(tuple(column) for column in modes)


def validate_modes(modes):
    need(type(modes) is list and len(modes) == 8, "eight modes required")
    need(all(type(c) is list and len(c) == 112 for c in modes), "owner shape")
    need(all(type(v) is int and v in (-1, 0, 1) for c in modes for v in c),
         "signed mode entries")


def vector(support, value):
    need(len(support) <= 112 and len(set(support)) == len(support), "unique owners")
    need(all(type(i) is int and 0 <= i < 112 for i in support), "owner range")
    out = [Q(0)] * 112
    for i in support:
        out[i] = value
    return tuple(out)


def observe(modes, values):
    need(len(values) == 112, "observation shape")
    return tuple(sum(c * x for c, x in zip(column, values)) for column in modes)


def distance(left, right):
    need(len(left) == len(right) == 112, "distance shape")
    return max(abs(x - y) for x, y in zip(left, right))


def same_modes(modes, left, right):
    need(observe(modes, left) == observe(modes, right), "mode preservation")


def reject(label, function, *args):
    try:
        function(*args)
    except ValueError:
        return label
    raise ValueError("accepted rejection control: " + label)


def corner_census(modes, x):
    records = []
    for bits in itertools.product((0, 1), repeat=4):
        corner = [0] * 112
        for i, bit in zip(SUPPORT, bits):
            corner[i] = bit
        observed = observe(modes, corner)
        need(distance(corner, x) == Q(1, 2), "literal corner distance")
        # Independently sum rows to check every returned mode tuple.
        by_rows = tuple(sum(bit * row[k] for bit, row in zip(bits, ROWS))
                        for k in range(8))
        need(observed == by_rows and observed != TARGET, "corner exclusion")
        need(not (corner[0] - corner[7] == 0 and corner[0] + corner[7] == 1),
             "integer contradiction")
        records.append({"bits": bits, "modes": observed})
    need(len(records) == 16, "complete corner domain")
    return records


def scaled_fixtures(modes, x, lift):
    count = 0
    for exponent in range(-6, 7):
        h = Q(2) ** exponent
        for shift in range(-3, 4):
            translation = tuple(shift * ((i % 5) - 2) for i in range(112))
            current = tuple(h * (a + b) for a, b in zip(translation, x))
            output = tuple(h * (a + b) for a, b in zip(translation, lift))
            same_modes(modes, current, output)
            need(distance(current, output) == h, "translated scaled upper witness")
            need(all((v / h).denominator == 1 for v in output), "output grid")
            count += 1
    return count


def controls(modes, raw, digest, x, lift):
    malformed = [list(column) for column in modes]
    malformed[0][0] = 2
    wrong_lift = vector((0,), Q(1))
    omitted = vector(SUPPORT[:-1], Q(1, 2))
    checks = [
        reject("changed source", parse_modes, raw + b" ", digest),
        reject("missing mode", validate_modes, [list(c) for c in modes[:-1]]),
        reject("invalid coefficient", validate_modes, malformed),
        reject("duplicate owner", vector, (0, 0), Q(1, 2)),
        reject("out-of-range owner", vector, (112,), Q(1, 2)),
        reject("wrong integer lift", same_modes, modes, x, wrong_lift),
        reject("omitted fractional owner", same_modes, modes, omitted, lift),
        reject("zero corner", same_modes, modes, x, vector((), Q(0))),
    ]
    # Sum preservation alone admits a half-unit corner, but the modes do not.
    sum_only = vector((0, 20), Q(1))
    need(sum(sum_only) == sum(x) and distance(sum_only, x) == Q(1, 2),
         "sum-only positive control")
    checks.append(reject("sum-only corner", same_modes, modes, x, sum_only))
    return checks


def verify():
    sources = json.loads(bounded_read(HERE / "SOURCES.json"))
    source = next(row for row in sources["files"] if row["path"] == SOURCE)
    need(source["usage"] == "input", "declared source input")
    raw = bounded_read(HERE.parents[1] / SOURCE)
    modes = parse_modes(raw, source["sha256"])
    for i, expected in zip(SUPPORT, ROWS):
        need(tuple(column[i] for column in modes) == expected, "literal source row")
    need(tuple(column[48] for column in modes) == TARGET, "integer lift source row")
    x, lift = vector(SUPPORT, Q(1, 2)), vector((48,), Q(1))
    same_modes(modes, x, lift)
    need(observe(modes, x) == TARGET and distance(x, lift) == 1, "attainment")
    records = corner_census(modes, x)
    count = scaled_fixtures(modes, x, lift)
    rejected = controls(modes, raw, source["sha256"], x, lift)
    paths = sorted(HERE.iterdir())
    need(len(paths) <= 32 and all(p.is_file() and not p.is_symlink() for p in paths),
         "bounded regular package inventory")
    hashes = {p.name: hashlib.sha256(bounded_read(p)).hexdigest() for p in paths}
    receipt = {"minimum_radius": "1", "support": SUPPORT, "integer_lift": 48,
               "target_modes": TARGET, "corners": records, "feasible_corners": 0,
               "scaled_translated_fixtures": count, "controls": rejected,
               "source_sha256": source["sha256"], "package_sha256": hashes}
    print(json.dumps(receipt, sort_keys=True))
    print("PASS_MODE_PRESERVING_ROUNDING radius=1 corners=16 fixtures="
          + str(count) + " controls=" + str(len(rejected)) + " no_new_kappa")


if __name__ == "__main__":
    verify()
