#!/usr/bin/env python3
"""Exact corroboration of the sharp shared translated Fourier error floor."""

import hashlib
import json
import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from exact import (FLOOR_SQUARED, I, ONE, SQRT2, SQRT3, ZERO, Q, add,
                   basis, basis_errors, coefficient_error, group, moment_error,
                   nonnegative, optimal_weights, rational, root, validate)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def reject(operation, message):
    try:
        operation()
    except ValueError:
        return
    raise ValueError("control accepted: " + message)


def sources():
    package = Path(__file__).resolve().parent
    root_path = package.parents[1]
    manifest = json.loads((package / "SOURCES.json").read_text())
    require(len(manifest["files"]) == 4, "source manifest length")
    hashes = {}
    for entry in manifest["files"]:
        if entry["usage"] != "input":
            continue
        path = root_path / entry["path"]
        require(path.is_file() and path.stat().st_size <= 1_000_000, "source size")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        require(digest == entry["sha256"], "source mismatch: " + entry["path"])
        hashes[entry["path"]] = digest
    require(len(hashes) == 2, "two live source inputs")
    return hashes


def field_checks():
    require(SQRT2 * SQRT2 == rational(2), "sqrt(2) relation")
    require(SQRT3 * SQRT3 == rational(3), "sqrt(3) relation")
    require(I * I == -ONE, "imaginary relation")
    require(nonnegative(FLOOR_SQUARED), "positive floor")
    require(not nonnegative(-FLOOR_SQUARED), "negative floor")
    triples = 0
    for a, b, c in product(range(8), repeat=3):
        x, y, z = basis(a), basis(b), basis(c)
        require((x * y) * z == x * (y * z), "basis associativity")
        require((x * y).conjugate() == x.conjugate() * y.conjugate(), "conjugation")
        triples += 1
    for order in (2, 4, 8):
        require(sum((root(order, j) for j in range(order)), ZERO) == ZERO,
                "root sum")
        for j in range(order):
            require(root(order, j).squared_modulus() == ONE, "root modulus")
    return triples


def scalar_checks():
    # 16/27 - 4*x^2*(1-x) = (4/27)*(3*x-2)^2*(3*x+1).
    left = (Fraction(16, 27), Fraction(0), Fraction(-4), Fraction(4))
    right = [Fraction(0)] * 4
    for j, a in enumerate((4, -12, 9)):
        for k, b in enumerate((1, 3)):
            right[j + k] += Fraction(4, 27) * a * b
    require(tuple(right) == left, "global cubic majorant identity")
    require(Fraction(1, 2) < Fraction(16, 27), "small-mean branch")
    require(Fraction(2, 3) ** 2 * Fraction(1, 3) * 4 == Fraction(16, 27),
            "attaining scalar moment")
    checked = 0
    for denominator in range(1, 33):
        for numerator in range(denominator + 1):
            x = Fraction(numerator, denominator)
            gap = sum(left[j] * x**j for j in range(4))
            require(gap >= 0, "finite majorant corroboration")
            checked += 1
    return checked


def minimizers(digest):
    fixtures = pairs = 0
    for shape in ((2,), (4,), (2, 2), (8,), (2, 4), (2, 2, 2)):
        for offset in group(shape):
            if not any(offset) or any(add(shape, offset, offset)):
                continue
            weights = optimal_weights(shape, offset)
            errors = basis_errors(shape, offset, weights)
            require(all(x == FLOOR_SQUARED for x in errors), "uniform equality")
            require(coefficient_error(shape, offset, weights) == FLOOR_SQUARED,
                    "coefficient equality")
            require(moment_error(shape, offset, weights) == FLOOR_SQUARED,
                    "moment equality")
            digest.update(json.dumps([shape, offset, [x.serial() for x in errors]],
                                     separators=(",", ":")).encode())
            fixtures += 1
            pairs += len(errors)
    return {"group_offset_fixtures": fixtures, "literal_basis_pairs": pairs}


def phase_catalogue(digest):
    phases = (ONE, -ONE, I, -I, (rational(3) + I * 4) / 5,
              (rational(3) - I * 4) / 5)
    cases = literal_pairs = 0
    for shape, offset in (((2,), (1,)), ((4,), (2,))):
        size = len(group(shape))
        for serial, weights in enumerate(product(phases, repeat=size)):
            error = coefficient_error(shape, offset, weights)
            require(error == moment_error(shape, offset, weights), "moment reduction")
            require(nonnegative(error - FLOOR_SQUARED), "catalogue lower bound")
            if serial < 6:
                literal = basis_errors(shape, offset, weights)
                require(sum(literal, ZERO) / size**2 == error, "Parseval normalization")
                literal_pairs += len(literal)
            digest.update(json.dumps(error.serial(), separators=(",", ":")).encode())
            cases += 1
    return {"rational_phase_assignments": cases,
            "additional_literal_basis_pairs": literal_pairs}


def controls():
    shape, offset = (4,), (2,)
    weights = optimal_weights(shape, offset)
    reject(lambda: validate(shape, (0,), weights), "zero translation")
    reject(lambda: validate(shape, (1,), weights), "order-four translation")
    reject(lambda: validate(shape, offset, weights[:-1]), "wrong dimension")
    reject(lambda: validate(shape, offset, (rational(2),) + weights[1:]), "nonunit")
    reject(lambda: group((8, 8)), "capacity")
    reject(lambda: group((3,)), "unsupported exact field")
    reject(lambda: Q((Fraction(0),)), "field dimension")
    reject(lambda: nonnegative(I), "unordered field value")
    require(any(x != FLOOR_SQUARED for x in basis_errors(
        shape, offset, tuple(-w for w in weights))), "wrong global phase")
    require(any(x != FLOOR_SQUARED for x in basis_errors(
        shape, offset, weights, omega=weights)), "missing final conjugation")
    require(any(x != FLOOR_SQUARED for x in basis_errors(
        shape, offset, weights, inverse_sign=-1)), "wrong final Fourier sign")
    chars = tuple(root(4, 2 * j) for j in range(4))
    require(all(x == ZERO for x in basis_errors(
        shape, offset, (ONE,) * 4, beta=chars, omega=chars)),
        "independent phases escape the shared restriction")
    require(coefficient_error(shape, offset, (ONE,) * 4) == rational(2),
            "unweighted translated control")
    require(nonnegative(FLOOR_SQUARED - rational(Fraction(46, 100))),
            "floor exceeds 0.46")
    return {"malformed_domain_rejections": 8, "semantic_controls": 6}


def main():
    input_hashes = sources()
    digest = hashlib.sha256()
    result = {"claim_type": "scoped written proof with exact finite corroboration",
              "field_basis_triples": field_checks(),
              "scalar_grid_points": scalar_checks(),
              "minimizers": minimizers(digest),
              "phase_catalogue": phase_catalogue(digest),
              "controls": controls(),
              "ordered_scientific_digest": digest.hexdigest(),
              "squared_error_floor": "2 - 8/(3*sqrt(3))",
              "source_hashes": input_hashes}
    package = Path(__file__).resolve().parent
    names = ("README.md", "PROOF.md", "TASK.json", "SOURCES.json", "VERIFY.json",
             "exact.py", "verify.py")
    result["package_hashes"] = {
        name: hashlib.sha256((package / name).read_bytes()).hexdigest() for name in names}
    print(json.dumps(result, indent=2, sort_keys=True))
    print("PASS_SHARED_FOURIER_TRANSLATION_FLOOR")


if __name__ == "__main__":
    main()
