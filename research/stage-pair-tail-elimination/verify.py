#!/usr/bin/env python3
"""Conformance and work-count evidence, produced by Nick Petalas. Apache-2.0."""

import hashlib
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path
import subprocess
import sys
import time

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def inverse(value, prime):
    return pow(value, -1, prime)


def load_kernel(source=None):
    path = PACKAGE / "kernel.py"
    namespace = {}
    exec(compile(path.read_text() if source is None else source, str(path), "exec", optimize=0), namespace)
    return namespace["tail_rank"]


def minor_rank(matrix, prime):
    height, width = len(matrix), len(matrix[0])
    require(height <= 3 and width <= 3, "minor oracle capacity")
    rows = [[int(x.numerator) * pow(int(x.denominator), -1, prime) % prime
             for x in row] for row in matrix]
    for size in range(min(height, width), 0, -1):
        for selected_rows in itertools.combinations(range(height), size):
            for selected_cols in itertools.combinations(range(width), size):
                total = 0
                for permutation in itertools.permutations(range(size)):
                    odd = sum(permutation[i] > permutation[j]
                              for i in range(size) for j in range(i + 1, size)) % 2
                    term = -1 if odd else 1
                    for i, j in enumerate(permutation):
                        term *= rows[selected_rows[i]][selected_cols[j]]
                    total += term
                if total % prime:
                    return size
    return 0


def kernel_cases(function):
    checked = 0
    for height, width, prime in ((3, 3, 2), (2, 3, 3)):
        for entries in itertools.product(range(prime), repeat=height * width):
            matrix = tuple(tuple(Q(entries[i * width + j]) for j in range(width))
                           for i in range(height))
            require(function(matrix, prime, inverse) == minor_rank(matrix, prime), "minor oracle")
            checked += 1
    for height, width in ((1, 0), (1, 1), (5, 7), (17, 17), (33, 31), (64, 64)):
        for prime in (2, 3, 5, 101, 103):
            matrix = tuple(tuple(Q(((1 << 70) + i) * prime + 1, prime + 1) if i == j else Q(0)
                                 for j in range(width)) for i in range(height))
            require(function(matrix, prime, inverse) == min(height, width), "large diagonal")
            checked += 1
    require(checked == 1271, "kernel case count")
    return checked


def boundary_controls(function):
    cases = [
        ((), 101, IndexError),
        (((Q(1),), (Q(1), Q(2))), 101, ValueError),
        (((Q(1),) * 65,), 101, ValueError),
        (((Q(1),),), 1, ValueError),
        (((Q(1),),), 1.5, ValueError),
        (((Q(1, 101),),), 101, ValueError),
    ]
    for matrix, prime, expected in cases:
        try:
            function(matrix, prime, inverse)
        except expected:
            continue
        raise ValueError("accepted invalid kernel input")
    return len(cases)


def mutation_controls():
    source = (PACKAGE / "kernel.py").read_text()
    mutations = [
        ("range(width)", "range(max(0, width - 1))"),
        ("x - factor * y", "x + factor * y"),
        ("pivot == height", "pivot >= 1"),
    ]
    witnesses = [((Q(0), Q(1)),), ((Q(1), Q(1)), (Q(1), Q(1))),
                 ((Q(1), Q(0)), (Q(0), Q(1)))]
    for (old, new), matrix in zip(mutations, witnesses, strict=True):
        require(source.count(old) == 1, "mutation anchor")
        mutant = load_kernel(source.replace(old, new))
        require(mutant(matrix, 3, inverse) != minor_rank(matrix, 3), "escaped arithmetic mutation")
    return len(mutations)


def complete(engine):
    command = [sys.executable, "-I", "-W", "error", "-B", str(PACKAGE / "adapter.py"),
               "--engine", engine]
    started = time.perf_counter()
    child = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=120)
    elapsed = time.perf_counter() - started
    require(child.returncode == 0, f"{engine} failed: {child.stderr}")
    return json.loads(child.stdout), elapsed


def main():
    function = load_kernel()
    cases = kernel_cases(function)
    boundaries = boundary_controls(function)
    mutants = mutation_controls()
    reference, reference_seconds = complete("reference")
    compared, compare_seconds = complete("compare")
    require(reference["payload"] == compared["payload"], "complete payload mismatch")
    require(reference["cache"] == compared["cache"], "complete cache workload mismatch")
    counts = compared["counts"]
    require(counts == {"full_products": 607860, "tail_products": 494696,
                      "kernel_calls": 372, "observed_full_products": 607860}, "work counts")
    payload = reference["payload"]
    require(payload["rank_sum"] == 8684 and len(payload["candidates"]) == 64,
            "complete scientific caller domain")
    require(len(payload["improved_candidates"]) == 6, "retained rational fallback decisions")
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    receipt = {
        "status": "PASS_STAGE_PAIR_TAIL_ELIMINATION", "claim_type": "exact implementation work reduction",
        "kernel_cases": cases, "boundary_controls": boundaries, "arithmetic_mutants": mutants,
        "counts": counts, "products_omitted": counts["full_products"] - counts["tail_products"],
        "cache": compared["cache"], "payload_sha256": digest,
        "complete_command_seconds": {"reference": reference_seconds, "compare_instrumented": compare_seconds},
        "python": sys.version, "errors": 0,
        "package_sha256": {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                           for path in sorted(PACKAGE.iterdir()) if path.is_file()},
    }
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
