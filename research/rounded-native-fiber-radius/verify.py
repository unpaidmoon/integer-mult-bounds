"""Exact finite certificate for the minimum full-fiber input radius."""

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FILES = ("README.md", "PROOF.md", "TASK.json", "SOURCES.json", "VERIFY.json",
         "MATRIX.json", "WITNESS.json", "verify.py")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_bytes(name: str) -> bytes:
    with (ROOT / name).open("rb") as stream:
        data = stream.read(1024 * 1024 + 1)
    require(len(data) <= 1024 * 1024, "file capacity exceeded")
    return data


def load_matrix() -> tuple:
    raw = read_bytes("MATRIX.json")
    sources = json.loads(read_bytes("SOURCES.json"))
    pins = [row for row in sources["files"]
            if row["path"] == "research/precision-state-frontier/FIXTURE.json"]
    require(len(pins) == 1, "unique predecessor matrix pin required")
    require(hashlib.sha256(raw).hexdigest() == pins[0]["sha256"], "matrix source drift")
    columns = json.loads(raw)["mode_columns"]
    require(len(columns) == 8 and all(len(c) == 112 for c in columns), "matrix shape")
    require(all(type(a) is int and a in (-1, 0, 1)
                for c in columns for a in c), "signed matrix entries")
    rows = tuple(tuple((j, columns[j][i]) for j in range(8) if columns[j][i])
                 for i in range(112))
    require(all(len(row) == 4 for row in rows), "four signed entries per owner")
    for j, k in itertools.product(range(8), repeat=2):
        require(sum(columns[j][i] * columns[k][i] for i in range(112))
                == (56 if j == k else 0), "source Gram premise")
    return rows


def apply_matrix(rows: tuple, q: tuple) -> tuple:
    require(len(q) == 8, "eight quotient coordinates required")
    return tuple(sum(sign * q[j] for j, sign in row) for row in rows)


def transpose(rows: tuple, x: tuple) -> tuple:
    require(len(x) == 112, "112 owner coordinates required")
    result = [0] * 8
    for row, value in zip(rows, x, strict=True):
        for j, sign in row:
            result[j] += sign * value
    return tuple(result)


def nearest_away(numerator: int, denominator: int) -> int:
    require(type(numerator) is int and type(denominator) is int
            and denominator > 0, "integer ratio with positive denominator required")
    magnitude = (2 * abs(numerator) + denominator) // (2 * denominator)
    return magnitude if numerator >= 0 else -magnitude


def forward(rows: tuple, x: tuple, scale: int = 8) -> tuple:
    q = tuple(nearest_away(scale * a, 52) for a in transpose(rows, x))
    correction = apply_matrix(rows, q)
    return tuple(scale * a - b for a, b in zip(x, correction, strict=True))


def validate_output(rows: tuple, output: tuple) -> None:
    require(len(output) == 112 and all(type(a) is int for a in output), "output shape")
    require(all(a in (-4, 0, 4) for a in output), "output amplitude")
    require(transpose(rows, output) == (0,) * 8, "output must be perpendicular")
    offset = apply_matrix(rows, (2,) * 8)
    require(all((a + b) % 8 == 0 for a, b in zip(output, offset, strict=True)),
            "quotient residue must be two modulo four")


def enumerate_fiber(rows: tuple, output: tuple) -> tuple:
    validate_output(rows, output)
    points, cells, radii = set(), {}, Counter()
    candidates = 0
    for q in itertools.product((-6, -2, 2, 6), repeat=8):
        candidates += 1
        correction = apply_matrix(rows, q)
        fine = tuple(a + b for a, b in zip(output, correction, strict=True))
        if any(a % 8 for a in fine):
            continue
        x = tuple(a // 8 for a in fine)
        require(forward(rows, x) == output, "literal forward map disagrees")
        require(max(map(abs, x)) <= 3, "radius-three certificate failed")
        require(x not in points, "duplicate input")
        points.add(x)
        key = tuple(((a + 6) // 4) % 2 for a in q)
        cells.setdefault(key, []).append((q, x))
        radii[max(map(abs, x))] += 1
    require(len(points) == 4096 and len(cells) == 16, "full-fiber cardinality")
    return points, cells, radii, candidates


def check_cells(rows: tuple, output: tuple, cells: dict) -> int:
    centers = set()
    for members in cells.values():
        require(len(members) == 256, "full binary quotient cell required")
        choices = [sorted({q[j] for q, _ in members}) for j in range(8)]
        require(all(len(c) == 2 and c[1] - c[0] == 8 for c in choices),
                "cell side length eight required")
        center = tuple((c[0] + c[1]) // 2 for c in choices)
        centers.add(center)
        image = apply_matrix(rows, center)
        for i in range(112):
            lo = min(x[i] for _, x in members)
            hi = max(x[i] for _, x in members)
            require(hi - lo == 4, "owner interval must have width four")
            require(4 * (lo + hi) == output[i] + image[i], "cell midpoint identity")
    require(len(centers) == 16, "different parity cells have different midpoints")
    return len(centers)


def reject(call, message: str) -> None:
    try:
        call()
    except ValueError:
        return
    raise ValueError(message)


def controls(rows: tuple, output: tuple, points: set) -> int:
    count = 0
    for n, d, want in ((1, 2, 1), (-1, 2, -1), (3, 2, 2), (-3, 2, -2),
                       (25, 52, 0), (-25, 52, 0), (26, 52, 1), (-26, 52, -1)):
        require(nearest_away(n, d) == want, "rounding boundary control")
        count += 1
    changed = list(output)
    changed[0] += 4
    reject(lambda: validate_output(rows, tuple(changed)), "changed output accepted")
    count += 1
    reject(lambda: validate_output(rows, (0,) * 112), "wrong residue accepted")
    count += 1
    reject(lambda: validate_output(rows, output[:-1]), "short output accepted")
    count += 1
    reject(lambda: nearest_away(1, 0), "zero denominator accepted")
    count += 1
    reject(lambda: nearest_away(True, 2), "Boolean numerator accepted")
    count += 1
    radius_three = next(x for x in points if max(map(abs, x)) == 3)
    reject(lambda: require(max(map(abs, radius_three)) <= 2, "radius two"),
           "false radius accepted")
    count += 1
    require(any(forward(rows, x, 4) != output for x in points), "wrong scale survived")
    return count + 1


def main() -> None:
    rows = load_matrix()
    witness = json.loads(read_bytes("WITNESS.json"))
    output = tuple(witness["output"])
    points, cells, radii, candidates = enumerate_fiber(rows, output)
    cell_count = check_cells(rows, output, cells)
    control_count = controls(rows, output, points)
    ordered = sorted(points)
    receipt = {
        "status": "PASS_ROUNDED_NATIVE_FIBER_RADIUS",
        "claim_type": "scoped proof with exact finite certificate",
        "minimum_integer_radius": 3,
        "quotient_candidates": candidates,
        "distinct_preimages": len(points),
        "radius_histogram": dict(sorted(radii.items())),
        "full_parity_cells": cell_count,
        "inputs_per_cell": 256,
        "controls": control_count,
        "input_set_sha256": hashlib.sha256(json.dumps(ordered, separators=(",", ":"))
                                           .encode()).hexdigest(),
        "package_sha256": {name: hashlib.sha256(read_bytes(name)).hexdigest()
                           for name in FILES},
        "no_new_kappa": True,
    }
    print(json.dumps(receipt, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
