"""Run the complete pinned Fourier caller with exact Gaussian quarter turns.

Produced by Nick Petalas. Apache-2.0.
"""

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "research/weighted-fourier-layout"
MAX_INPUT_BYTES = 16 * 1024 * 1024


def require(condition, message):
    if not condition:
        raise ValueError(message)


def authenticate(root=ROOT):
    manifest = json.loads((HERE / "SOURCES.json").read_text())
    rows = manifest["files"]
    require(len(rows) <= 16, "too many source pins")
    checked = {}
    for row in rows:
        if row["usage"] != "input":
            continue
        path = root / row["path"]
        with path.open("rb") as handle:
            data = handle.read(MAX_INPUT_BYTES + 1)
        require(len(data) <= MAX_INPUT_BYTES, "source capacity exceeded")
        digest = hashlib.sha256(data).hexdigest()
        require(digest == row["sha256"], "source drift: " + row["path"])
        checked[row["path"]] = digest
    return checked


def load(filename):
    require(filename in ("verify.py", "test_verify.py"), "unknown source entry")
    spec = importlib.util.spec_from_file_location("retained_fourier", SOURCE / filename)
    require(spec is not None and spec.loader is not None, "missing source loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def specialize(source):
    """Install one exact arithmetic replacement in this private module only."""
    original = source.ORACLE.Ring.root_mul

    def root_mul(ring, value, exponent):
        if ring.m != 4:
            return original(ring, value, exponent)
        phase = exponent % 4
        if phase == 0:
            return value
        if phase == 1:
            return (-value[1], value[0])
        if phase == 2:
            return (-value[0], -value[1])
        return (value[1], -value[0])

    source.ORACLE.Ring.root_mul = root_mul
    return original, root_mul


def caller(source):
    previous = sys.argv
    try:
        sys.argv = [str(SOURCE / "verify.py")]
        source.main()
    finally:
        sys.argv = previous


def tests(specialized=True):
    module = load("test_verify.py")
    if specialized:
        specialize(module.V)
    suite = unittest.defaultTestLoader.loadTestsFromModule(module)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    require(result.wasSuccessful(), "retained tests failed")
    require(result.testsRun == 11, "retained test inventory changed")
    return result.testsRun


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", action="store_true")
    parser.add_argument("--with-tests", action="store_true")
    args = parser.parse_args()
    authenticate()
    source = load("verify.py")
    if not args.baseline:
        specialize(source)
    caller(source)
    if args.with_tests:
        tests(not args.baseline)


if __name__ == "__main__":
    main()
