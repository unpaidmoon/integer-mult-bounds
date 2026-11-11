"""Conformance, complete caller and rejection controls for quarter turns.

Produced by Nick Petalas. Apache-2.0.
"""

import hashlib
from itertools import product
import json
from pathlib import Path
import sys
import tempfile

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import replay


def kernel_checks(source):
    original, fast = replay.specialize(source)
    gaussian = source.ORACLE.Ring(4)
    comparisons = 0
    for real, imag in product(range(-8, 9), repeat=2):
        for exponent in range(-12, 13):
            value = (real, imag)
            replay.require(fast(gaussian, value, exponent)
                           == original(gaussian, value, exponent), "quarter turn mismatch")
            comparisons += 1
    fallback = 0
    for order in range(1, 25):
        if order == 4:
            continue
        ring = source.ORACLE.Ring(order)
        for exponent in range(-24, 25):
            value = tuple(2 * i - 3 for i in range(ring.degree))
            replay.require(fast(ring, value, exponent)
                           == original(ring, value, exponent), "fallback mismatch")
            fallback += 1
    return comparisons, fallback


def rejects(action, message):
    try:
        action()
    except ValueError as exc:
        replay.require(message in str(exc), "unexpected rejection reason: " + str(exc))
        return
    raise ValueError("missing rejection: " + message)


def controls(source):
    # These are actual changed kernels, rather than predicates about the source.
    source.ORACLE.Ring.root_mul = lambda ring, value, exponent: value
    rejects(lambda: source.census_group((2,)), "literal convolution failed")
    source = replay.load("verify.py")
    original, _ = replay.specialize(source)
    source.ORACLE.Ring.root_mul = lambda ring, value, exponent: original(ring, value, -exponent)
    rejects(lambda: replay.caller(source), "mismatched spectral witness should be nonzero")
    source = replay.load("verify.py")
    original, _ = replay.specialize(source)
    source.ORACLE.Ring.root_mul = lambda ring, value, exponent: original(ring, value, exponent + 1)
    rejects(lambda: source.census_group((2,)), "literal convolution failed")
    return 3


def source_controls():
    manifest = json.loads((HERE / "SOURCES.json").read_text())
    rows = [row for row in manifest["files"] if row["usage"] == "input"]
    replay.require(len(rows) == 7, "source inventory changed")
    with tempfile.TemporaryDirectory(prefix="fourier source controls ") as directory:
        root = Path(directory)
        for row in rows:
            path = root / row["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes((replay.ROOT / row["path"]).read_bytes())
        replay.require(replay.authenticate(root) == replay.authenticate(), "relocation mismatch")
        for row in rows:
            path = root / row["path"]
            original = path.read_bytes()
            path.write_bytes(original + b"\ncorruption\n")
            rejects(lambda: replay.authenticate(root), "source drift: " + row["path"])
            path.write_bytes(original)
    rejects(lambda: replay.load("unknown.py"), "unknown source entry")
    return len(rows) + 1


def main():
    pins = replay.authenticate()
    source = replay.load("verify.py")
    gaussian, fallback = kernel_checks(source)
    # The retained main constructs and compares its entire canonical receipt.
    replay.caller(source)
    test_count = replay.tests()
    mutant_count = controls(source)
    source_count = source_controls()
    own_hashes = {}
    files = tuple(sorted(HERE.iterdir()))
    replay.require(len(files) <= 12, "package capacity exceeded")
    for path in files:
        if path.is_file():
            own_hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    print(json.dumps({"status": "PASS_WEIGHTED_FOURIER_ROOT_SPECIALIZATION",
                      "gaussian_cases": gaussian, "fallback_cases": fallback,
                      "retained_tests": test_count, "kernel_mutants": mutant_count,
                      "source_controls": source_count,
                      "source_hashes": pins, "package_hashes": own_hashes}, sort_keys=True))


if __name__ == "__main__":
    main()
