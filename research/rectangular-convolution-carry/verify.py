#!/usr/bin/env python3
"""Finite corroboration of PROOF.md; no predecessor executable or file writes."""

import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
FILES = ("PROOF.md", "README.md", "SOURCES.json", "TASK.json", "VERIFY.json", "verify.py")
DOMAINS = ((2, 6), (3, 4), (4, 3), (5, 3), (6, 2), (7, 2), (8, 2), (9, 2))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def envelope(base: int, left: int, right: int, index: int) -> int:
    """Carry after index output digits; this formula has no size cutoff."""
    require(all(type(value) is int for value in (base, left, right, index)), "integer geometry required")
    require(base >= 2 and left >= 1 and right >= 1, "positive radix geometry required")
    require(0 <= index <= left + right, "carry index outside output")
    if index == 0:
        return 0
    shorter, longer = min(left, right), max(left, right)
    if index <= longer:
        return min(index, shorter) * (base - 1) - 1
    return (left + right - index) * (base - 1)


def digits(value: int, base: int, length: int) -> tuple[int, ...]:
    require(2 <= base <= 9 and 1 <= length <= 6, "finite digit domain exceeded")
    require(0 <= value < base**length, "unsigned input outside digit field")
    result = []
    for _ in range(length):
        value, digit = divmod(value, base)
        result.append(digit)
    require(value == 0, "digit extraction lost a high digit")
    return tuple(result)


def convolution(left: tuple[int, ...], right: tuple[int, ...], base: int) -> tuple[int, ...]:
    require(1 <= len(left) <= 6 and 1 <= len(right) <= 6, "finite convolution domain exceeded")
    require(all(type(digit) is int and 0 <= digit < base for digit in left + right),
            "unsigned radix digits required")
    coefficients = [0] * (len(left) + len(right))
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            coefficients[i + j] += x * y
    require(coefficients[-1] == 0, "zero flush coefficient required")
    return tuple(coefficients)


def carry_sequence(coefficients: tuple[int, ...], base: int) -> tuple[tuple[int, ...], int]:
    require(2 <= base <= 32 and 2 <= len(coefficients) <= 64, "finite carry domain exceeded")
    require(all(type(value) is int and value >= 0 for value in coefficients),
            "nonnegative coefficients required")
    carries = [0]
    prefix_coefficients, prefix_digits, place = 0, 0, 1
    for coefficient in coefficients:
        carry, digit = divmod(coefficient + carries[-1], base)
        carries.append(carry)
        prefix_coefficients += coefficient * place
        prefix_digits += digit * place
        place *= base
        require(prefix_digits + carry * place == prefix_coefficients, "carry prefix identity")
    return tuple(carries), prefix_digits


def check_products() -> dict[str, int]:
    products, positions, profiles = 0, 0, 0
    for base, limit in DOMAINS:
        for left in range(1, limit + 1):
            for right in range(1, limit + 1):
                bounds = tuple(envelope(base, left, right, k) for k in range(left + right + 1))
                observed = [0] * len(bounds)
                for x in range(base**left):
                    xs = digits(x, base, left)
                    for y in range(base**right):
                        coefficients = convolution(xs, digits(y, base, right), base)
                        carries, output = carry_sequence(coefficients, base)
                        require(output == x * y and carries[-1] == 0, "complete product recovery")
                        for k, carry in enumerate(carries):
                            require(carry <= bounds[k], "position-dependent envelope exceeded")
                            observed[k] = max(observed[k], carry)
                        products += 1
                        positions += len(carries)
                require(tuple(observed) == bounds, "positionwise bound is not attained")
                profiles += 1
    require(products == 79541 and profiles == 86, "complete product-domain count")
    return {"products": products, "product_positions": positions, "product_profiles": profiles}


def check_maximal_digits() -> dict[str, int]:
    profiles, positions, literal_coefficients = 0, 0, 0
    for base in range(2, 33):
        for left in range(1, 33):
            for right in range(1, 33):
                # Count j+k=i directly by the allowed interval for j.
                coefficients = tuple(
                    max(0, min(left - 1, i) - max(0, i - right + 1) + 1) * (base - 1)**2
                    for i in range(left + right)
                )
                carries, output = carry_sequence(coefficients, base)
                expected = tuple(envelope(base, left, right, k) for k in range(left + right + 1))
                require(carries == expected, "maximal-digit recurrence differs from formula")
                require(output == (base**left - 1) * (base**right - 1), "attaining product")
                require(max(carries) == min(left, right) * (base - 1) - 1, "sharp uniform cap")
                require(expected == tuple(envelope(base, right, left, k) for k in range(len(expected))),
                        "exchanging the operands changes the envelope")
                if base <= 9 and left <= 6 and right <= 6:
                    literal = convolution((base - 1,) * left, (base - 1,) * right, base)
                    require(coefficients == literal, "pair count disagrees with literal convolution")
                    literal_coefficients += len(literal)
                profiles += 1
                positions += len(carries)
    return {"attaining_profiles": profiles, "attaining_positions": positions,
            "literal_coefficients": literal_coefficients}


def check_binary_capacity() -> dict[str, int]:
    cases, savings = 0, 0
    for base in range(2, 65):
        for shorter in range(1, 65):
            size = shorter * (base - 1)
            cap = size - 1
            sharp_bits = cap.bit_length()
            old_bits = size.bit_length()
            require(cap < 2**sharp_bits, "sharp carry does not fit binary field")
            require(sharp_bits == 0 or cap >= 2**(sharp_bits - 1), "binary field not minimal")
            saving = old_bits - sharp_bits
            power_of_two = size & (size - 1) == 0
            require(saving == int(power_of_two), "bit saving criterion")
            savings += saving
            cases += 1
    return {"binary_capacity_cases": cases, "one_bit_savings": savings}


def check_controls() -> dict[str, int]:
    malformed = ((1, 2, 2, 1), (0, 1, 1, 0), (2, 0, 2, 0), (2, 2, -1, 0),
                 (2, 2, 2, -1), (2, 2, 2, 5), (True, 1, 1, 0), (2, 1.0, 1, 0))
    controls = 0
    for values in malformed:
        try:
            envelope(*values)
        except ValueError:
            controls += 1
        else:
            raise ValueError("malformed geometry accepted")
    exact = tuple(envelope(10, 2, 4, k) for k in range(7))
    require(exact == (0, 8, 17, 17, 17, 9, 0), "rectangular decimal control")
    claims = ((max(exact), 18), (max(exact), 16), (exact[5], 17), (exact[1], 9))
    for observed, claimed in claims:
        try:
            require(observed == claimed, "false sharpness claim")
        except ValueError:
            controls += 1
        else:
            raise ValueError("false sharpness control accepted")
    require(162 // 10 > exact[1], "unstructured stream boundary control")
    require((1 + 1) // 2 > envelope(2, 1, 1, 1), "initial carry boundary control")
    require(exact[-2] > 0 and exact[-1] == 0, "last-digit flush boundary control")
    for left, right in (((-1,), (1,)), ((2,), (1,))):
        try:
            convolution(left, right, 2)
        except ValueError:
            controls += 1
        else:
            raise ValueError("invalid digit control accepted")
    return {"rejecting_controls": controls, "scope_boundary_controls": 3}


def package_hashes() -> dict[str, str]:
    result = {}
    for name in FILES:
        path = PACKAGE / name
        require(path.is_file() and not path.is_symlink(), "regular package file required")
        require(path.stat().st_size <= 1024 * 1024, "package hash input exceeds 1 MiB")
        result[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def main() -> None:
    counts = check_products()
    counts.update(check_maximal_digits())
    counts.update(check_binary_capacity())
    counts.update(check_controls())
    receipt = {"status": "PASS_RECTANGULAR_CONVOLUTION_CARRY", "counts": counts,
               "claim_type": "scoped proof with finite corroboration", "new_kappa": False,
               "package_sha256": package_hashes()}
    print(json.dumps(receipt, sort_keys=True))


if __name__ == "__main__":
    main()
