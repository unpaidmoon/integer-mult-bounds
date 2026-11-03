"""Complete unchanged PR5235 caller with an opt-in prefix-cached checker.

The adapter and cache were produced by Nick Petalas. Apache-2.0.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SOURCE = ROOT / "research/universal-dirty-certificates"


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def authenticate():
    manifest = json.loads((HERE / "SOURCES.json").read_text())
    rows = [row for row in manifest["files"] if row["usage"] == "input"]
    need(len(rows) == 13, "complete source inventory")
    for row in rows:
        data = (ROOT / row["path"]).read_bytes()
        need(hashlib.sha256(data).hexdigest() == row["sha256"], "source SHA256: " + row["path"])
        header = b"blob " + str(len(data)).encode() + b"\0"
        need(hashlib.sha1(header + data).hexdigest() == row["git_blob"], "source blob: " + row["path"])
    return {row["path"]: row["sha256"] for row in rows}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    need(spec is not None and spec.loader is not None, "source module loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def setup(cached):
    authenticate()
    caller = load("retained_dirty_caller", SOURCE / "verify.py")
    baseline = caller.checker
    fast = load("cached_dirty_checker", HERE / "check_certificate.py")
    if cached:
        caller.checker = fast
    return caller, baseline, fast


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", action="store_true")
    args = parser.parse_args()
    caller, _, _ = setup(not args.baseline)
    caller.main()


if __name__ == "__main__":
    main()
