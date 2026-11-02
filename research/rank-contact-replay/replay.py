"""Run the entire retained contact-distance caller with either exact engine.

Produced by Nick Petalas. The retained caller and its mathematical predicates
are David Ganz / Dugongue's PR4841, with the notices pinned in SOURCES.json.
"""

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from contact_rank import ContactRank

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[1]
SOURCE = "research/native-clifford-gauge-compiler"


def authenticate(root: Path = ROOT) -> None:
    pins = json.loads((PACKAGE / "SOURCES.json").read_text(encoding="utf-8"))
    for entry in pins["files"]:
        if entry["usage"] == "input":
            data = (root / entry["path"]).read_bytes()
            if hashlib.sha256(data).hexdigest() != entry["sha256"]:
                raise ValueError("Source hash mismatch: " + entry["path"])


def load_source(root: Path = ROOT):
    authenticate(root)
    path = root / SOURCE / "decoder/testformula.py"
    spec = importlib.util.spec_from_file_location("retained_contacts", path)
    if spec is None or spec.loader is None:
        raise ValueError("Cannot load authenticated contact caller")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def complete_replay(engine: str = "rank") -> tuple[dict, ContactRank | None]:
    if engine not in ("rank", "literal"):
        raise ValueError("Unknown contact engine")
    source = load_source()
    rank_engine = ContactRank() if engine == "rank" else None
    if rank_engine is not None:
        source.actual_change = rank_engine
    # These are precisely the calls in the retained main with --graph supplied.
    out = {"status": "PASS_EXACT_TRANSVECTION_DISTANCE", "small": source.small(),
           "actual": source.actual_graph(ROOT / SOURCE / "inputs/round3-contact-graph.txt")}
    expected = json.loads((ROOT / SOURCE / "decoder/TRANSVECTION-EXPECTED.json")
                          .read_text(encoding="utf-8"))
    if out != expected:
        raise ValueError("Complete retained contact receipt changed")
    if rank_engine is not None and rank_engine.calls != out["actual"]["exact_axis_cases"]:
        raise ValueError("Rank engine did not execute every actual contact check")
    return out, rank_engine


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", choices=("rank", "literal"), default="rank")
    args = parser.parse_args()
    out, _rank_engine = complete_replay(args.engine)
    print(json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
