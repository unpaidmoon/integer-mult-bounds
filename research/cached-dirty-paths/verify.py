"""Preservation, exact cache-work controls, and the complete scientific caller.

Produced by Nick Petalas. Apache-2.0.
"""
from contextlib import redirect_stdout
from copy import deepcopy
import hashlib
import io
import json
from pathlib import Path
import statistics
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import benchmark
import replay

HELPER = '''def follow_prefixes(node, word, step):
    """Follow an already validated word; rows are immutable within one check."""
    row, children = node
    for symbol in word:
        if symbol not in children:
            children[symbol] = (step(row, symbol), {})
        row, children = children[symbol]
    return row


'''
OLD_PATH = '''    def path(output, word):
        require(type(output) is int and 0 <= output < len(roots), "output role")
        require(type(word) is list and all(a in alphabet for a in word), "path alphabet")
        v = roots[output]
        for a in word:
            v = step(v, a)
        return v
'''
NEW_PATH = '''    prefixes = {}  # Owned by this check call; no cross-certificate reuse.

    def path(output, word):
        require(type(output) is int and 0 <= output < len(roots), "output role")
        require(type(word) is list and all(a in alphabet for a in word), "path alphabet")
        node = prefixes.setdefault(output, (roots[output], {}))
        return follow_prefixes(node, word, step)
'''


def delta_check():
    source = (replay.SOURCE / "check_certificate.py").read_text()
    actual = (HERE / "check_certificate.py").read_text()
    replay.need(actual.count(HELPER) == actual.count(NEW_PATH) == 1, "one declared cache change")
    recovered = actual.replace(HELPER, "").replace(NEW_PATH, OLD_PATH)
    replay.need(recovered == source, "non-cache code or predicate changed")


def counted_check(module, problem, certificate):
    original, count = module.reconstruct, [0]

    def reconstructed(problem, shifted):
        roots, step, terminal, states, alphabet = original(problem, shifted)

        def counted(row, symbol):
            count[0] += 1
            return step(row, symbol)

        return roots, counted, terminal, states, alphabet

    module.reconstruct = reconstructed
    try:
        verdict = module.check(problem, certificate)
    finally:
        module.reconstruct = original
    return verdict, count[0]


def fixture(degree, field):
    ops = [{"op": "query", "src": role, "dst": role, "symbol": "X"}
           for role in range(2) for _ in range(degree)]
    factor, inverse = (1, "1") if field == 2 else (2, "1/2")
    start = [{"op": "scale", "dst": role, "coefficient": factor} for role in range(2)]
    finish = [{"op": "scale", "dst": role, "coefficient": inverse} for role in range(2)]
    return {"field": field, "roles": 2, "program": ops, "reference": start + ops + finish}


def prefix_work(certificate):
    paths = certificate["paths"]
    total = sum(len(path["word"]) for path in paths)
    prefixes = {(path["output"], tuple(path["word"][:j]))
                for path in paths for j in range(1, len(path["word"]) + 1)}
    return total - len(prefixes)


def cache_controls(caller, baseline, fast):
    cases = saved = 0
    for field in ("Q", "Qi", 2, 3, 5):
        for degree in range(1, 9):
            problem = fixture(degree, field)
            for shifted in (False, True):
                certificate = caller.producer.decide(problem, shifted)
                expected = counted_check(baseline, problem, certificate)
                actual = counted_check(fast, problem, certificate)
                replay.need(expected[0] == actual[0] == "universal-identity", "complete fixture endpoint")
                reduction = prefix_work(certificate)
                replay.need(expected[1] - actual[1] == reduction, "exact distinct-prefix work law")
                replay.need(counted_check(fast, problem, certificate) == actual, "cache leaked between calls")
                cases += 1
                saved += reduction
    replay.need(saved > 0, "cache must actually avoid transitions")
    return {"complete_two_root_cases": cases, "saved_transition_calls": saved}


def rejection_controls(caller, baseline, fast):
    problem = fixture(4, "Q")
    original = caller.producer.decide(problem)
    mutations = []
    bad = deepcopy(original); bad["paths"][-1]["word"].append("unknown"); mutations.append(bad)
    bad = deepcopy(original); bad["paths"][-1]["output"] = True; mutations.append(bad)
    bad = deepcopy(original); bad["paths"][-1]["output"] = 2; mutations.append(bad)
    bad = deepcopy(original); bad["closure"].clear(); mutations.append(bad)
    bad = deepcopy(original); bad["initial"][0] = {}; mutations.append(bad)
    bad = deepcopy(original); bad["problem_sha256"] = "0" * 64; mutations.append(bad)
    for bad in mutations:
        for module in (baseline, fast):
            try:
                module.check(problem, bad)
            except (ValueError, KeyError, TypeError, ZeroDivisionError):
                pass
            else:
                raise ValueError("cache-related malformed certificate accepted")
    return len(mutations) * 2


def complete(caller):
    output = io.StringIO()
    with redirect_stdout(output):
        caller.main()
    return benchmark.normalized(output.getvalue())


def receipt_check():
    receipt = json.loads((HERE / "BENCHMARK.json").read_text())
    replay.need(receipt["executable_sha256"] == benchmark.executable_hashes(), "measured executable hashes")
    replay.need(receipt["input_sha256"] == replay.authenticate(), "measured input hashes")
    samples = receipt["samples_seconds"]
    replay.need(set(samples) == {"baseline", "cached"}, "both measured sides")
    for side, values in samples.items():
        replay.need(len(values) == 5 and all(type(v) is float and v > 0 for v in values), "five successful runs")
        replay.need(statistics.median(values) == receipt["median_seconds"][side], "measured median")
    before, after = (receipt["median_seconds"][side] for side in ("baseline", "cached"))
    replay.need(receipt["reduction_percent"] == 100 * (before - after) / before, "measured reduction")
    replay.need(receipt["failures"] == 0 and receipt["successful_complete_replays"] == 10, "no failed samples")
    replay.need(max(samples["cached"]) < min(samples["baseline"]), "timing ranges must separate")
    return receipt["scientific_output"]


def main():
    delta_check()
    caller, baseline, fast = replay.setup(False)
    controls = cache_controls(caller, baseline, fast)
    controls["rejections"] = rejection_controls(caller, baseline, fast)
    expected = receipt_check()
    old = complete(caller)
    caller.checker = fast
    new = complete(caller)
    replay.need(old == new == expected, "complete caller scientific fields")
    print(json.dumps({"controls": controls, "complete_scientific_output": new}, sort_keys=True))
    print("PASS_CACHED_DIRTY_PATHS")


if __name__ == "__main__":
    main()
