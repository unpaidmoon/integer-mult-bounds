"""Opt-in arithmetic replacement; all predecessor check predicates stay intact."""

import hashlib
import json
from pathlib import Path
import sys
from types import ModuleType

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
from packed import multiply


def authenticate(root=ROOT):
    manifest = json.loads((HERE / "SOURCES.json").read_text(encoding="utf-8"))
    inputs = {}
    for row in manifest["files"]:
        if row["usage"] != "input":
            continue
        raw = (root / row["path"]).read_bytes()
        if hashlib.sha256(raw).hexdigest() != row["sha256"]:
            raise ValueError("changed source: " + row["path"])
        inputs[row["path"]] = raw
    return inputs


def load_primary():
    inputs = authenticate()
    relative = "research/order-seventeen-clifford/verify.py"
    path = ROOT / relative
    module = ModuleType("order17_primary")
    module.__file__ = str(path)
    # Compile the authenticated source bytes, bypassing any preexisting .pyc.
    exec(compile(inputs[relative], str(path), "exec"), module.__dict__)
    return module


def main():
    if sys.argv[1:]:
        raise ValueError("unexpected arguments")
    source = load_primary()
    source.multiply = multiply
    source.main()


if __name__ == "__main__":
    main()
