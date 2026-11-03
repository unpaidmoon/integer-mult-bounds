"""Opt-in complete rational-box CLI with a fraction-free solve kernel.

Produced by Nick Petalas. Apache-2.0. The original optimizer is Ali Romman's.
"""
from hashlib import sha256
import json
from pathlib import Path
import sys

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[1]


def authenticate(root=ROOT, package=PACKAGE):
    raw = (package / "SOURCES.json").read_bytes()
    if len(raw) > 1024 * 1024:
        raise ValueError("Source manifest exceeds 1 MiB")
    records = json.loads(raw)["files"]
    expected = {
        "scripts/optimize_rational_box.py",
        "scripts/compare_recursive_invoices.py",
        "tests/test_research_rational_box.py",
    }
    inputs = [row for row in records if row["usage"] == "input"]
    if len(inputs) != 3 or {row["path"] for row in inputs} != expected:
        raise ValueError("Unexpected source input inventory")
    for row in inputs:
        data = (root / row["path"]).read_bytes()
        if sha256(data).hexdigest() != row["sha256"]:
            raise ValueError("Source bytes changed: " + row["path"])


def main(argv=None):
    try:
        authenticate()
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(str(error), file=sys.stderr)
        return 2
    sys.path.insert(0, str(ROOT / "scripts"))
    import optimize_rational_box as engine
    from solver import solve
    original = engine.solve
    engine.solve = solve
    try:
        return engine.main(argv)
    finally:
        engine.solve = original


if __name__ == "__main__":
    raise SystemExit(main())
