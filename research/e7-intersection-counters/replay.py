"""Run the complete retained E7 consumer with one chosen counter engine."""
import argparse
from functools import partial
from hashlib import sha256
import json
from pathlib import Path
from runpy import run_path
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
SOURCE = REPO / "research/e7-bitsliced-exhaustion"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def read_bytes(path):
    need(path.stat().st_size <= 1_048_576, "input exceeds one MiB")
    return path.read_bytes()


def authenticate():
    sources = json.loads(read_bytes(HERE / "SOURCES.json"))
    rows = [row for row in sources["files"] if row["usage"] == "input"]
    need(len(rows) == 6, "expected six live inputs")
    for row in rows:
        data = read_bytes(REPO / row["path"])
        need(sha256(data).hexdigest() == row["sha256"],
             "source digest mismatch: " + row["path"])


def engines():
    original = run_path(str(SOURCE / "binary.py"))
    current = run_path(str(HERE / "engine.py"))
    fast = partial(current["low_weight_words"],
                   population_planes=original["population_planes"],
                   at_most=original["at_most"])
    return original["low_weight_words"], fast


def execute(engine_name):
    authenticate()
    old, new = engines()
    selected = old if engine_name == "original" else new
    binary = SOURCE / "binary.py"

    def dispatch(path, *args, **kwargs):
        if Path(path) == binary:
            need(not args and not kwargs, "unexpected binary loader contract")
            return {"low_weight_words": selected}
        return run_path(path, *args, **kwargs)

    consumer = run_path(str(SOURCE / "classify.py"))
    consumer["main"].__globals__["run_path"] = dispatch
    consumer["main"]()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", choices=("original", "intersection"),
                        default="intersection")
    args = parser.parse_args()
    sys.dont_write_bytecode = True
    sys.pycache_prefix = str(HERE / "unused-bytecode-namespace")
    execute(args.engine)


if __name__ == "__main__":
    main()
