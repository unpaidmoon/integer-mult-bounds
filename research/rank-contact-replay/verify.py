"""Check the replacement engine and the full retained caller. Apache-2.0.

Produced by Nick Petalas. No source geometric result is claimed as new.
"""

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import shutil
import sys
import tempfile

PACKAGE = Path(__file__).resolve().parent
sys.path.insert(0, str(PACKAGE))
from contact_rank import ContactRank
from replay import ROOT, authenticate, complete_replay, load_source


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def kernel_checks(source) -> dict:
    engine = ContactRank()
    counts = []
    for n in (1, 2, 3):
        spaces = source.all_lagrangians(n)
        count = 0
        for u in spaces:
            for v in spaces:
                for axis in range(1 << (2 * n)):
                    need(engine(u, v, axis, n) == source.actual_change(u, v, axis, n),
                         "Rank engine differs from literal moved-space intersection")
                    count += 1
        counts.append({"n": n, "spaces": len(spaces), "axis_cases": count})
    # Nonisotropic complete subspaces are legal too. Enumerate every 2-plane.
    spaces = sorted({source.span(pair) for pair in itertools.combinations(range(1, 16), 2)},
                    key=lambda x: tuple(sorted(x)))
    need(len(spaces) == 35, "Complete binary Grassmannian count")
    general_cases = 0
    for u in spaces:
        for v in spaces:
            for axis in range(16):
                need(engine(u, v, axis, 2) == source.actual_change(u, v, axis, 2),
                     "Nonisotropic intersection mismatch")
                general_cases += 1
    # A fresh equal-value object must give the same answer after cache eviction.
    u, v = spaces[0], spaces[-1]
    expected = source.actual_change(u, v, 7, 2)
    need(engine(frozenset(list(u)), frozenset(list(v)), 7, 2) == expected,
         "Equal-value cache replacement")
    return {"lagrangian_cases": counts, "general_plane_cases": general_cases,
            "calls": engine.calls, "cache_preparations": engine.preparations}


def wider_checks(source) -> dict:
    rng = random.Random(48414841)
    engine = ContactRank()
    count = 0
    for n in (4, 5, 9):
        for _case in range(24):
            u, v = source.span([1 << j for j in range(n)]), source.span([
                (1 << j) ^ (1 << (n + j)) for j in range(n)])
            # Arbitrary symplectic transvections preserve complete subspaces.
            for _step in range(12):
                axis = rng.randrange(1, 1 << (2 * n))
                u = frozenset(x ^ (axis if source.symp(x, axis, n) else 0) for x in u)
                axis = rng.randrange(1, 1 << (2 * n))
                v = frozenset(x ^ (axis if source.symp(x, axis, n) else 0) for x in v)
            for _axis in range(64):
                axis = rng.randrange(1 << (2 * n))
                need(engine(u, v, axis, n) == source.actual_change(u, v, axis, n),
                     "Wide literal intersection mismatch")
                count += 1
    return {"pairs": 72, "axis_cases": count}


def controls(source) -> dict:
    engine = ContactRank()
    u, v = frozenset((0, 1)), frozenset((0, 2))
    good = engine(u, v, 3, 1)
    bad = [(u, v, -1, 1), (u, v, 4, 1), (u, v, True, 1),
           (u, v, 0, 0), (u, v, 0, 10), (u, v, 0, True),
           (set(u), v, 0, 1), (frozenset((0,)), v, 0, 1),
           (frozenset((0, 4)), v, 0, 1), (frozenset((0, True)), v, 0, 1),
           (frozenset((0, 1, 2, 4)), frozenset((0, 1, 2, 3)), 0, 2)]
    for args in bad:
        try:
            engine(*args)
        except ValueError:
            pass
        else:
            raise ValueError("Invalid contact was accepted")
    need(engine(u, v, 3, 1) == good and engine.preparations == 1,
         "Rejected input corrupted the one-entry cache")
    need(good == -1 and source.actual_change(u, v, 3, 1) == -1,
         "Sign-reversal and constant-zero mutants must fail")
    need(engine(u, v, 1, 1) == 0, "Fixed-subspace axis control")
    return {"invalid_inputs_rejected": len(bad), "mutation_controls": 2,
            "failed_preparation_preserves_cache": True}


def source_controls() -> int:
    pins = json.loads((PACKAGE / "SOURCES.json").read_text(encoding="utf-8"))
    entries = [e for e in pins["files"] if e["usage"] == "input"]
    with tempfile.TemporaryDirectory(prefix="contact-source-control-") as directory:
        root = Path(directory)
        for entry in entries:
            target = root / entry["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / entry["path"], target)
        authenticate(root)
        for entry in entries:
            target = root / entry["path"]
            original = target.read_bytes()
            target.write_bytes(original + b"\n# changed source bytes\n")
            try:
                load_source(root)
            except ValueError as error:
                need(str(error).startswith("Source hash mismatch:"),
                     "Mutated source was executed before authentication")
            else:
                raise ValueError("Changed source accepted")
            target.write_bytes(original)
    return len(entries)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    authenticate()
    source = load_source()
    out = {"status": "PASS_RANK_CONTACT_REPLAY", "kernel": kernel_checks(source),
           "wider": wider_checks(source), "controls": controls(source),
           "source_mutations_rejected": source_controls()}
    full, engine = complete_replay()
    need(engine is not None and engine.preparations == 1240,
         "Every consecutive actual contact must be prepared exactly once")
    out["complete_retained_caller"] = full
    out["rank_calls"] = engine.calls
    out["rank_preparations"] = engine.preparations
    out["package_sha256"] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in sorted(PACKAGE.iterdir()) if p.is_file()}
    if args.output:
        need(PACKAGE not in args.output.resolve().parents, "Write receipts outside package")
        args.output.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n",
                               encoding="utf-8")
    print(json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
