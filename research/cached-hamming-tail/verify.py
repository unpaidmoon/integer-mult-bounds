"""Finite equivalence checks, produced by Nick Petalas. Apache-2.0."""

from hashlib import sha256
import json
from pathlib import Path
import shutil
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kernel
import source


def need(condition, reason):
    if not condition:
        raise ValueError(reason)


def check_tables(reach, shifted):
    comparisons = 0
    for last in range(32):
        for remaining in range(13):
            index = last * 13 + remaining
            values = [x for x in range(32)
                      if (last ^ x).bit_count() + x.bit_count() <= remaining]
            need(reach[index] == sum(1 << x for x in values), "reach mask")
            for old in range(32):
                expected = sum(1 << (old ^ x) for x in values)
                need(shifted[index][old] == expected, "XOR translation")
                comparisons += 1
    return comparisons


def prefixes():
    stack = [((0,), -1, 1)]
    for _ in range(21641):
        if not stack:
            return
        points, highest, seen = stack.pop()
        yield points, highest, seen
        if len(points) == 12:
            continue
        for label in range(min(highest + 1, 4), -1, -1):
            value = points[-1] ^ (1 << label)
            if not seen >> value & 1:
                stack.append((points + (value,), max(highest, label), seen | (1 << value)))
        need(len(stack) <= 56, "bounded DFS stack")
    raise ValueError("prefix domain exceeded its bound")


def check_prefixes(reference, reach, shifted):
    count = 0
    decisions = 0
    fast = kernel.cached_reject(reference, reach, shifted)
    for points, highest, seen in prefixes():
        old_future, old_possible = reference.tail_envelope(points)
        future, possible = kernel.envelope(points, seen, reference.pair_support(points), reach, shifted)
        need(future == sum(1 << x for x in old_future), "future set")
        need(possible == old_possible, "complete envelope")
        need(fast(points, highest, "two_without_cap") ==
             reference.reject(points, highest, "two_without_cap"), "rejection decision")
        decisions += 1
        count += 1
    need(count == 21640, "complete canonical prefix domain")
    return {"prefixes": count, "rejection_comparisons": decisions}


def digest(words):
    return sha256("".join("".join(map(str, w)) + "\n" for w in words).encode()).hexdigest()


def check_callers(reference):
    original = reference.reject
    baseline = reference.search("two_without_cap")
    candidate = kernel.search(reference)
    need(reference.reject is original, "source adapter restoration")
    need(candidate == baseline, "complete caller output")
    counts, closed, hits = candidate
    need(counts == {"entered": 7350, "pruned": 4381, "closed": 828, "universal": 828}, "caller counts")
    return {"counts": counts, "closed_sha256": digest(closed), "universal_sha256": digest(hits)}


def check_controls(reference, reach, shifted):
    points = (0, 1, 3, 2, 6, 7, 5, 13, 9, 8)
    seen = sum(1 << p for p in points)
    support = reference.pair_support(points)
    future, possible = kernel.envelope(points, seen, support, reach, shifted)
    need((kernel.NONZERO ^ possible) == (1 << 20) | (1 << 28), "strict missing-mask witness")
    need(future.bit_count() == 5, "strict future witness")
    wrong = list(shifted)
    index = points[-1] * 13 + 3
    wrong[index] = tuple(kernel.ALL for _ in range(32))
    need(kernel.envelope(points, seen, support, reach, wrong)[1] != possible, "overpermissive table control")
    need(kernel.envelope(points, 0, support, reach, shifted)[0] != future, "visited-mask omission control")
    need(kernel.translate(1, 1) != 1, "identity-translation control")
    try:
        kernel.cached_reject(reference, reach, shifted)(points, 4, "cheap")
    except ValueError as error:
        need("fixed shared-tail" in str(error), "wrong mode error")
    else:
        raise ValueError("unsupported mode accepted")
    old_union, old_reject = reference.union_reject, reference.reject
    def fail(points):
        raise RuntimeError("deliberate caller failure")
    reference.union_reject = fail
    try:
        try:
            kernel.search(reference)
        except RuntimeError as error:
            need(str(error) == "deliberate caller failure", "wrong adapter error")
        else:
            raise ValueError("caller failure swallowed")
        need(reference.reject is old_reject, "adapter not restored after failure")
    finally:
        reference.union_reject = old_union
    with tempfile.TemporaryDirectory(prefix="hamming-source-") as name:
        root = Path(name)
        for path in source.authenticate():
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source.ROOT / path, target)
        path = root / "research/five-label-prefix-completion/bounds.py"
        path.write_bytes(path.read_bytes() + b"\n# altered source\n")
        try:
            source.authenticate(root)
        except ValueError as error:
            need("source hash mismatch" in str(error), "wrong source error")
        else:
            raise ValueError("actual source-byte corruption accepted")
    return 6


def main():
    reference = source.load()
    reach, shifted = kernel.tables()
    report = {"status": "PASS_CACHED_HAMMING_TAIL", "claim_type": "implementation equivalence and local performance",
              "table_comparisons": check_tables(reach, shifted),
              **check_prefixes(reference, reach, shifted), "caller": check_callers(reference),
              "controls": check_controls(reference, reach, shifted), "inputs": source.authenticate()}
    report["package_sha256"] = {
        p.name: sha256(p.read_bytes()).hexdigest()
        for p in sorted(source.HERE.iterdir()) if p.is_file()}
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
