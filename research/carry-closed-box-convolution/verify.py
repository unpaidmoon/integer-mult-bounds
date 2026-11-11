#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact unpadded carry-graded box convolution and bounded corroboration.

Produced by Nick Petalas. The carry filter and four-product sign convention
build on Chafik Boukhalfa / PR524; changed weights and stride are proved here.
"""

from dataclasses import dataclass
from hashlib import sha256
from itertools import product
import json
from math import gcd, prod
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


@dataclass(frozen=True)
class Layout:
    shape: tuple[int, ...]
    volume: int
    modulus: int
    weights: tuple[int, ...]
    coordinates: tuple[tuple[int, ...], ...]
    grades: tuple[int, ...]
    slots: tuple[int, ...]
    product_slots: int


def coordinates(shape: tuple[int, ...], volume: int) -> tuple[tuple[int, ...], ...]:
    rows = []
    for index in range(volume):
        value, row = index, []
        for radix in shape:
            row.append(value % radix)
            value //= radix
        require(value == 0, "coordinate overflow")
        rows.append(tuple(row))
    return tuple(rows)


def raw_layout(shape: tuple[int, ...], modulus: int, weights: tuple[int, ...]) -> Layout:
    """Internal constructor, also used for invalid arithmetic controls."""
    volume = prod(shape)
    rows = coordinates(shape, volume)
    grades = tuple(sum(a * w for a, w in zip(row, weights, strict=True)) % modulus
                   for row in rows)
    slots = tuple(i + volume * grade for i, grade in enumerate(grades))
    require(len(set(slots)) == volume, "input slots collide")
    return Layout(shape, volume, modulus, weights, rows, grades, slots, 2 * max(slots) + 1)


def layout(shape: tuple[int, ...], modulus: int | None = None) -> Layout:
    require(type(shape) is tuple and 1 <= len(shape) <= 16, "use 1..16 axes")
    require(all(type(n) is int and 1 <= n <= 4096 for n in shape), "invalid radix")
    volume, dimension = prod(shape), len(shape)
    require(volume <= 4096, "volume exceeds 4096")
    if modulus is None:
        candidates = (t for t in range(dimension + 1, 65) if gcd(t, volume) == 1)
        modulus = next(candidates, None)
    require(type(modulus) is int and dimension < modulus <= 64, "invalid grade modulus")
    require(gcd(modulus, volume) == 1, "grade modulus must be coprime to volume")
    weights = [0] * dimension
    for i in range(dimension - 2, -1, -1):
        weights[i] = (weights[i + 1] + 1) * pow(shape[i], -1, modulus) % modulus
    result = raw_layout(shape, modulus, tuple(weights))
    require(result.product_slots < 2 * volume * modulus, "product slot bound failed")
    return result


def pack(values: tuple[int, ...], plan: Layout, sign: int, slot_bytes: int) -> int:
    require(sign in (-1, 1), "invalid sign split")
    encoded = bytearray((max(plan.slots) + 1) * slot_bytes)
    for value, slot in zip(values, plan.slots, strict=True):
        coefficient = max(sign * value, 0)
        start = slot * slot_bytes
        encoded[start:start + slot_bytes] = coefficient.to_bytes(slot_bytes, "little")
    return int.from_bytes(encoded, "little")


def convolve(left: tuple[int, ...], right: tuple[int, ...], plan: Layout,
             mutation: str | None = None) -> tuple[int, ...]:
    require(len(left) == len(right) == plan.volume, "wrong input length")
    require(all(type(x) is int and abs(x) <= 65536 for x in left + right), "invalid coefficient")
    left_bound, right_bound = max(map(abs, left)), max(map(abs, right))
    bound = max(left_bound, right_bound, plan.volume * left_bound * right_bound)
    slot_bytes = max(1, (bound.bit_length() + 7) // 8)
    require(bound < 1 << (8 * slot_bytes), "coefficient radix is not strict")
    fp, fm = pack(left, plan, 1, slot_bytes), pack(left, plan, -1, slot_bytes)
    gp, gm = pack(right, plan, 1, slot_bytes), pack(right, plan, -1, slot_bytes)
    products = (fp * gp, fm * gm, fp * gm, fm * gp)
    signs = (1, 1, -1, -1) if mutation != "omit_cross" else (1, 1, 0, 0)
    buffers = tuple(p.to_bytes(plan.product_slots * slot_bytes, "little") for p in products)
    output = []
    for index, grade in enumerate(plan.grades):
        slots = (index + plan.volume * grade, index + plan.volume * (grade + plan.modulus))
        if mutation == "omit_wrap":
            slots = slots[:1]
        value = 0
        for slot in slots:
            if slot < plan.product_slots:
                start = slot * slot_bytes
                value += sum(sign * int.from_bytes(buf[start:start + slot_bytes], "little")
                             for sign, buf in zip(signs, buffers, strict=True))
        output.append(value)
    return tuple(output)


def oracle(left: tuple[int, ...], right: tuple[int, ...], plan: Layout) -> tuple[int, ...]:
    """Direct coordinate convolution, independent of grade arithmetic and packing."""
    by_coordinate = {row: i for i, row in enumerate(plan.coordinates)}
    result = [0] * plan.volume
    for i, a in enumerate(plan.coordinates):
        for j, b in enumerate(plan.coordinates):
            target = tuple(x + y for x, y in zip(a, b, strict=True))
            if all(x < n for x, n in zip(target, plan.shape, strict=True)):
                result[by_coordinate[target]] += left[i] * right[j]
    return tuple(result)


def check_carries() -> dict[str, int]:
    shapes = pairs = rejected_aliases = 0
    for dimension in range(1, 6):
        for shape in product(range(1, 4), repeat=dimension):
            if prod(shape) > 100:
                continue
            plan = layout(shape)
            shapes += 1
            for i, a in enumerate(plan.coordinates):
                for j, b in enumerate(plan.coordinates):
                    target = plan.coordinates[(i + j) % plan.volume]
                    incoming = count = 0
                    for x, y, z, radix in zip(a, b, target, shape, strict=True):
                        total = x + y + incoming
                        require(total % radix == z, "digit recurrence failed")
                        incoming = total // radix
                        require(incoming in (0, 1), "nonbinary carry")
                        count += incoming
                    require(incoming == (i + j) // plan.volume, "wrong final carry")
                    residue = (plan.grades[i] + plan.grades[j] + incoming
                               - plan.grades[(i + j) % plan.volume]) % plan.modulus
                    valid = all(x + y < r for x, y, r in zip(a, b, shape, strict=True))
                    require(residue == count % plan.modulus, "all-carry congruence failed")
                    require((residue == 0) == valid, "overflow alias admitted")
                    rejected_aliases += int(not valid)
                    pairs += 1
    return {"carry_shapes": shapes, "carry_pairs": pairs, "rejected_aliases": rejected_aliases}


def check_products() -> dict[str, int]:
    exhaustive = ragged = 0
    for shape in ((1,), (2,), (1, 2), (3,), (2, 2), (2, 1, 2)):
        plan = layout(shape)
        words = tuple(product((-1, 0, 1), repeat=plan.volume))
        for left in words:
            for right in words:
                require(convolve(left, right, plan) == oracle(left, right, plan), "signed product mismatch")
                exhaustive += 1
    for shape in ((2, 3, 2), (3, 1, 2, 3), (1, 3, 1, 2, 1), (4, 3), (3, 3, 3), (2,) * 6):
        plan = layout(shape)
        for k in range(8):
            left = tuple((i * i + 3 * i + k) % 7 - 3 for i in range(plan.volume))
            right = tuple((5 * i + i * k + 2) % 7 - 3 for i in range(plan.volume))
            require(convolve(left, right, plan) == oracle(left, right, plan), "ragged product mismatch")
            ragged += 1
    return {"exhaustive_products": exhaustive, "ragged_products": ragged}


def check_large() -> dict[str, int]:
    plan = layout((2,) * 12)
    left = tuple((-1) ** sum(a) for a in plan.coordinates)
    right = tuple(2 ** (12 - sum(a)) for a in plan.coordinates)
    expected = tuple(prod(2 if x == 0 else -1 for x in a) for a in plan.coordinates)
    require(convolve(left, right, plan) == expected, "separable large product failed")
    require(plan.modulus == 13 and plan.product_slots == 106495, "changed large layout")
    # PR524's recurrence and stride, used only for the layout comparison.
    old_weights = [1]
    for radix in plan.shape[:-1]:
        old_weights.append((radix * old_weights[-1] - 1) % len(plan.shape))
    old_slots = tuple(i + (2 * plan.volume - 1)
                      * (sum(x * w for x, w in zip(a, old_weights, strict=True)) % 12)
                      for i, a in enumerate(plan.coordinates))
    old_extent = 2 * max(old_slots) + 1
    require(old_extent == 188391 and old_extent > plan.product_slots, "layout does not improve")
    return {"large_output_coefficients": plan.volume, "old_product_slots": old_extent,
            "new_product_slots": plan.product_slots, "saved_slots": old_extent - plan.product_slots}


def accepts_pair(plan: Layout, i: int, j: int, final: bool = True) -> bool:
    end = (i + j) // plan.volume if final else 0
    return (plan.grades[i] + plan.grades[j] + end
            - plan.grades[(i + j) % plan.volume]) % plan.modulus == 0


def check_boundaries() -> dict[str, int]:
    plan = layout((4096,))
    positive = (65536,) * plan.volume
    zeros = (0,) * plan.volume
    require(convolve(positive, zeros, plan) == zeros, "right zero input failed")
    require(convolve(zeros, positive, plan) == zeros, "left zero input failed")
    expected = tuple((i + 1) * 65536**2 for i in range(plan.volume))
    require(convolve(positive, positive, plan) == expected, "maximum coefficient input failed")
    tall = layout((2,) * 12 + (1,) * 4)
    left = tuple((-1) ** sum(a) for a in tall.coordinates)
    right = tuple(2 ** (12 - sum(a)) for a in tall.coordinates)
    expected = tuple(prod(2 if x == 0 else -1 for x in a[:12]) for a in tall.coordinates)
    require(convolve(left, right, tall) == expected, "maximum dimension input failed")
    return {"boundary_products": 4}


def check_controls() -> dict[str, int]:
    require(accepts_pair(layout((2,)), 1, 1, False), "missing-final-carry control lost its alias")
    require(not accepts_pair(layout((2,)), 1, 1), "final carry does not reject")
    short = raw_layout((2, 2, 2), 3, (0, 2, 0))
    require(accepts_pair(short, 7, 7), "small-modulus control lost its alias")
    wrong = raw_layout((2, 2), 3, (1, 0))
    require(accepts_pair(wrong, 3, 3), "wrong-recurrence control lost its alias")
    plan = layout((2, 2, 2))
    left, right = (1, -1, 1, -1, 1, -1, 1, -1), (-1,) * 8
    expected = oracle(left, right, plan)
    require(convolve(left, right, plan, "omit_cross") != expected, "signed-cross control failed")
    require(convolve((1,) * 8, (1,) * 8, plan, "omit_wrap")
            != oracle((1,) * 8, (1,) * 8, plan), "grade-wrap control failed")
    invalid = (((), None), ((0,), None), ((True,), None), ((4097,), None),
               ((2,) * 17, None), ((4096, 2), None), ((2, 2), 2), ((2, 2), 4))
    rejected = 0
    for shape, modulus in invalid:
        try:
            layout(shape, modulus)
        except ValueError:
            rejected += 1
    require(rejected == len(invalid), "invalid layout admitted")
    for bad in ((1,), (False,) * 8, (65537,) * 8):
        try:
            convolve(bad, right, plan)
        except ValueError:
            rejected += 1
    require(rejected == len(invalid) + 3, "invalid input admitted")
    return {"arithmetic_controls": 5, "input_rejections": rejected}


def authenticate(root: Path, package: Path) -> dict[str, str]:
    raw = (package / "SOURCES.json").read_bytes()
    require(len(raw) <= 65536, "source manifest exceeds bound")
    source = json.loads(raw)
    require(len(source["files"]) == 5, "unexpected source inventory")
    hashes = {}
    for row in source["files"]:
        if row["usage"] == "input":
            path = root / row["path"]
            require(path.is_file() and not path.is_symlink(), "input is not regular")
            data = path.read_bytes()
            require(len(data) <= 1048576, "source input exceeds bound")
            digest = sha256(data).hexdigest()
            require(digest == row["sha256"], "source bytes changed: " + row["path"])
            hashes[row["path"]] = digest
    require(len(hashes) == 3, "incomplete source authentication")
    return hashes


def main() -> None:
    package = Path(__file__).resolve().parent
    hashes = authenticate(package.parents[1], package)
    results = {}
    for part in (check_carries(), check_products(), check_large(), check_boundaries(), check_controls()):
        results.update(part)
    for name in ("README.md", "PROOF.md", "TASK.json", "SOURCES.json", "VERIFY.json", "verify.py"):
        hashes[name] = sha256((package / name).read_bytes()).hexdigest()
    print(json.dumps({"status": "PASS_CARRY_CLOSED_BOX_CONVOLUTION", "checks": results,
                      "sha256": hashes}, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
