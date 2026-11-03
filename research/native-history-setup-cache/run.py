#!/usr/bin/env python3
"""Run the unchanged direct-history caller with bounded native setup reuse."""

import argparse
from functools import lru_cache
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import runpy
import sys

HERE = Path(__file__).resolve().parent
SOURCE = Path("research/physical-zqy-scalar-span")
CAPACITY = 256


def need(condition, message):
    if not condition:
        raise ValueError(message)


def authenticate(root):
    manifest = json.loads((HERE / "SOURCES.json").read_text())
    for item in manifest["files"]:
        if item["usage"] == "input":
            raw = (root / item["path"]).read_bytes()
            need(sha256(raw).hexdigest() == item["sha256"],
                 "source bytes " + item["path"])


def cached_native(original):
    """Snapshot all nine columns; retain at most 256 immutable results."""
    @lru_cache(maxsize=CAPACITY)
    def compile_columns(columns):
        result = original(columns)
        need(type(result) is bytes and len(result) == 1024,
             "one immutable 512-column monomial")
        return result

    def native(columns):
        key = tuple(columns)
        need(len(key) == 9 and all(type(v) is int and 0 <= v < 512 for v in key),
             "nine binary native-map columns")
        return compile_columns(key)

    return native, compile_columns


def execute(root, mode):
    authenticate(root)
    need("native" not in sys.modules and "monomial" not in sys.modules,
         "a fresh caller process")
    runtime = root / SOURCE
    spec = importlib.util.spec_from_file_location("monomial", runtime / "monomial.py")
    need(spec is not None and spec.loader is not None, "monomial module loader")
    module = importlib.util.module_from_spec(spec)
    sys.modules["monomial"] = module
    spec.loader.exec_module(module)
    original = module.native
    wrapped, cache = cached_native(original)
    if mode == "cached":
        module.native = wrapped
    saved_argv, saved_path = sys.argv, list(sys.path)
    try:
        sys.path.insert(0, str(runtime))
        sys.argv = [str(runtime / "verify_kernel.py")]
        runpy.run_path(str(runtime / "verify_kernel.py"), run_name="__main__")
        info = cache.cache_info()
        print(json.dumps({"mode": mode, "cache": info._asdict()}, sort_keys=True),
              file=sys.stderr)
    finally:
        module.native = original
        cache.cache_clear()
        sys.argv, sys.path = saved_argv, saved_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("baseline", "cached"), default="cached")
    parser.add_argument("--root", type=Path, default=HERE.parents[1])
    args = parser.parse_args()
    execute(args.root.resolve(), args.mode)


if __name__ == "__main__":
    main()
