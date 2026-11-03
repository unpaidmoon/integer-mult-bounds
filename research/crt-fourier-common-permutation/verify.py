#!/usr/bin/env python3
"""Exact bounded corroboration of the common-permutation Fourier theorem."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
MAX_BYTES = 1_048_576


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def bounded_read(path: Path) -> bytes:
    with path.open("rb") as stream:
        data = stream.read(MAX_BYTES + 1)
    require(len(data) <= MAX_BYTES, "file exceeds checker capacity")
    return data


def source_hashes() -> dict[str, str]:
    manifest = json.loads(bounded_read(PACKAGE / "SOURCES.json"))
    rows = manifest["files"]
    require(isinstance(rows, list) and len(rows) <= 16, "source inventory")
    hashes = {}
    for row in rows:
        if row["usage"] != "input":
            continue
        name = row["path"]
        require(name in {
            "research/native-coprime-grid/README.md",
            "research/native-coprime-grid/PROOF.md",
        }, "unexpected source path")
        data = bounded_read(PACKAGE.parents[1] / name)
        digest = hashlib.sha256(data).hexdigest()
        require(digest == row["sha256"], "source SHA256: " + name)
        header = b"blob " + str(len(data)).encode("ascii") + b"\0"
        require(hashlib.sha1(header + data).hexdigest() == row["git_blob"],
                "source Git blob: " + name)
        hashes[name] = digest
    require(len(hashes) == 2, "missing source inputs")
    return hashes


def shape_check(axes: tuple[int, ...]) -> int:
    require(type(axes) is tuple and 1 <= len(axes) <= 4, "axis tuple")
    require(all(type(s) is int and 2 <= s <= 257 for s in axes),
            "axis bounds")
    total = math.prod(axes)
    require(total <= 65_536, "product bound")
    for i in range(len(axes)):
        for j in range(i):
            require(math.gcd(axes[i], axes[j]) == 1, "axes not coprime")
    return total


def root_coefficients(axes: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    """All f(e_i) tuples, in canonical residue order, from local square roots."""
    total = shape_check(axes)
    choices = []
    for s in axes:
        complement = total // s
        roots = tuple(v for v in range(s) if complement * v * v % s == 1)
        choices.append(tuple(complement * v for v in roots))
    return tuple(itertools.product(*choices))


def coordinates(axes: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    shape_check(axes)
    return tuple(itertools.product(*(range(s) for s in axes)))


def make_map(axes: tuple[int, ...], coefficients: tuple[int, ...]) -> tuple[int, ...]:
    total = shape_check(axes)
    require(type(coefficients) is tuple and len(coefficients) == len(axes),
            "coefficient tuple")
    require(all(type(c) is int and 0 <= c < total for c in coefficients),
            "coefficient bounds")
    return tuple(sum(c * x for c, x in zip(coefficients, point, strict=True))
                 % total for point in coordinates(axes))


def kernel_holds(axes: tuple[int, ...], mapping: tuple[int, ...]) -> bool:
    """Literal equality of every phase, with no floating complex arithmetic."""
    total = shape_check(axes)
    if (type(mapping) is not tuple or len(mapping) != total
            or any(type(x) is not int for x in mapping)
            or sorted(mapping) != list(range(total))):
        return False
    points = coordinates(axes)
    weights = tuple(total // s for s in axes)
    for ix in range(total):
        for iy in range(total):
            tensor = sum(w * x * y for w, x, y in
                         zip(weights, points[ix], points[iy], strict=True))
            if (mapping[ix] * mapping[iy] - tensor) % total:
                return False
    return True


def cyclic_oracle(axes: tuple[int, ...]) -> tuple[set[tuple[int, ...]], int]:
    """Enumerate every homomorphism by the image of (1,...,1), not local roots."""
    total = shape_check(axes)
    points = coordinates(axes)
    # Build the cyclic-coordinate table by direct simultaneous residues.
    lookup = {tuple(k % s for s in axes): k for k in range(total)}
    require(len(lookup) == total, "cyclic coordinate bijection")
    accepted = set()
    trials = 0
    for multiplier in range(total):
        mapping = tuple(multiplier * lookup[x] % total for x in points)
        trials += 1
        if kernel_holds(axes, mapping):
            accepted.add(mapping)
    return accepted, trials


def finite_shapes() -> tuple[tuple[int, ...], ...]:
    shapes = [(s,) for s in range(2, 33)]
    for count in (2, 3):
        for axes in itertools.combinations(range(2, 14), count):
            if math.prod(axes) <= 255 and all(
                    math.gcd(a, b) == 1 for a, b in itertools.combinations(axes, 2)):
                shapes.append(axes)
    return tuple(shapes)


def compare_maps() -> dict[str, int]:
    counts = {"shapes": 0, "cyclic_candidates": 0, "accepted_maps": 0,
              "literal_phase_entries": 0, "no_map_shapes": 0}
    for axes in finite_shapes():
        produced = {make_map(axes, c) for c in root_coefficients(axes)}
        expected, trials = cyclic_oracle(axes)
        require(produced == expected, "root constructor versus cyclic oracle")
        total = math.prod(axes)
        for mapping in produced:
            require(kernel_holds(axes, mapping), "constructed Fourier identity")
            counts["literal_phase_entries"] += total * total
        counts["shapes"] += 1
        counts["cyclic_candidates"] += trials
        counts["accepted_maps"] += len(produced)
        counts["no_map_shapes"] += not produced
    return counts


def arbitrary_permutations() -> dict[str, int]:
    counts = {"full_permutations": 0, "accepted_permutations": 0,
              "nonlinear_accepted": 0}
    for axes in ((2,), (3,), (4,), (5,), (6,), (2, 3)):
        total = math.prod(axes)
        expected = {make_map(axes, c) for c in root_coefficients(axes)}
        accepted = set()
        # Include every translation and every nonlinear bijection, not just f(0)=0.
        for mapping in itertools.permutations(range(total)):
            counts["full_permutations"] += 1
            if kernel_holds(axes, mapping):
                accepted.add(mapping)
                counts["accepted_permutations"] += 1
                counts["nonlinear_accepted"] += mapping not in expected
        require(accepted == expected, "arbitrary permutation classification")
    require(counts["nonlinear_accepted"] == 0, "nonlinear escape")
    return counts


def examples() -> dict[str, object]:
    positive = (13, 17)
    coefficients = root_coefficients(positive)
    require(len(coefficients) == 4, "13 by 17 count")
    for c in coefficients:
        require(kernel_holds(positive, make_map(positive, c)), "positive fixture")
    require(not root_coefficients((3, 5)), "3 by 5 obstruction")
    require(not root_coefficients((3, 7)), "3 by 7 obstruction")
    # Standard two-map CRT still works at these excluded common-map shapes.
    two_map_entries = 0
    for axes in ((3, 5), (3, 7), (4, 5)):
        total = math.prod(axes)
        points = coordinates(axes)
        left = tuple((total // s) * pow(total // s, -1, s) for s in axes)
        right = tuple(total // s for s in axes)
        for x in points:
            for y in points:
                a = sum(c * z for c, z in zip(left, x, strict=True)) % total
                b = sum(c * z for c, z in zip(right, y, strict=True)) % total
                phase = sum(w * u * v for w, u, v in zip(right, x, y, strict=True))
                require((a * b - phase) % total == 0, "two-map scope control")
                two_map_entries += 1
    return {"axes": positive, "coefficients": coefficients,
            "two_map_scope_entries": two_map_entries}


def rejection_controls() -> int:
    invalid = [(), (1,), (True,), (2.0,), (258,), (2, 2), (6, 9),
               (2, 3, 5, 7, 11), (251, 257, 3)]
    for axes in invalid:
        try:
            root_coefficients(axes)
        except ValueError:
            pass
        else:
            raise ValueError("invalid shape accepted")
    axes = (13, 17)
    good = make_map(axes, root_coefficients(axes)[0])
    shifted = tuple((x + 1) % 221 for x in good)
    nonlinear = list(good)
    nonlinear[1], nonlinear[2] = nonlinear[2], nonlinear[1]
    require(not kernel_holds(axes, shifted), "translated common map")
    require(not kernel_holds(axes, tuple(nonlinear)), "nonlinear swap")
    require(not kernel_holds(axes, good[:-1]), "truncated map")
    require(not kernel_holds(axes, (0,) * 221), "nonbijective map")
    naive = make_map((3, 5), (10, 6))
    require(not kernel_holds((3, 5), naive), "same canonical CRT map")
    return len(invalid) + 5


def main() -> None:
    inputs = source_hashes()
    report = {"status": "PASS_CRT_FOURIER_COMMON_PERMUTATION",
              "classification": compare_maps(),
              "arbitrary_bijections": arbitrary_permutations(),
              "examples": examples(), "rejection_controls": rejection_controls(),
              "source_sha256": inputs}
    names = ("README.md", "PROOF.md", "TASK.json", "SOURCES.json", "VERIFY.json", "verify.py")
    report["package_sha256"] = {
        name: hashlib.sha256(bounded_read(PACKAGE / name)).hexdigest() for name in names
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
