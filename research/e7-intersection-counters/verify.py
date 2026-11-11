"""Exact conformance and complete-caller replay for intersection counters."""
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
from runpy import run_path
import statistics
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def need(condition, message):
    if not condition:
        raise ValueError(message)


def literal_words(rows):
    words = [0]
    for row in rows:
        words.extend([word ^ row for word in words[:]])
    return words


def small_codes(original, current):
    codes = comparisons = 0
    for dimension in range(5):
        for rows in combinations(range(1, 16), dimension):
            literal = literal_words(rows)
            if len(set(literal)) != len(literal):
                continue
            codes += 1
            for maximum in range(5):
                expected = sorted(word for word in literal if word.bit_count() <= maximum)
                for batch in range(1, 6):
                    old = list(original(rows, 4, maximum, batch))
                    new = list(current(rows, 4, maximum, batch))
                    need(new == old and sorted(new) == expected,
                         "small-code content or iterator order changed")
                    comparisons += 1
    need((codes, comparisons) == (1381, 34525), "small-code coverage changed")
    return codes, comparisons


def wide_codes(original, current):
    comparisons = 0
    for width in (0, 1, 7, 31, 63, 64, 65, 127):
        dimension = min(10, width)
        rows = []
        for i in range(dimension):
            extra = sum((((i + 1) * (j + 3) + (i ^ j)).bit_count() & 1) << j
                        for j in range(width - dimension))
            rows.append((extra << dimension) | (1 << i))
        literal = literal_words(rows)
        for maximum in sorted({0, width // 3, width // 2, width}):
            expected = sorted(word for word in literal if word.bit_count() <= maximum)
            for batch in (1, 3, 7, 16):
                new = list(current(rows, width, maximum, batch))
                need(new == list(original(rows, width, maximum, batch)),
                     "wide-code iterator order changed")
                need(sorted(new) == expected, "wide-code content changed")
                comparisons += 1
    return comparisons


def arithmetic_cases(translated, population):
    pairs = 0
    for width in range(9):
        lanes = 1 << width
        mask = (1 << lanes) - 1
        columns = [sum(1 << lane for lane in range(lanes) if lane >> bit & 1)
                   for bit in range(width)]
        base = population(columns)
        for offset in range(1 << width):
            intersection = population([columns[j] for j in range(width)
                                       if offset >> j & 1])
            planes = translated(base, intersection, offset.bit_count(),
                                mask, width.bit_length())
            for lane in range(lanes):
                actual = sum((plane >> lane & 1) << bit
                             for bit, plane in enumerate(planes))
                need(actual == (lane ^ offset).bit_count(),
                     "translated population arithmetic differs")
                pairs += 1
    return pairs


def reject(action):
    try:
        action()
    except ValueError:
        return
    raise ValueError("invalid input was accepted")


def controls(engine):
    cases = [([1], -1, 0, 1), ([1], True, 0, 1), ([1], 128, 0, 1),
             ([1], 1, -1, 1), ([1], 1, True, 1), ([1], 1, 2, 1),
             ([True], 1, 1, 1), ([-1], 1, 1, 1), ([2], 1, 1, 1),
             ([0], 1, 1, 1), ([1, 2, 3], 2, 1, 1),
             ([1], 1, 1, 0), ([1], 1, 1, 21), ([1], 1, 1, True),
             ([1 << i for i in range(28)], 28, 1, 16),
             ([1 << i for i in range(18)], 18, 1, 1)]
    for args in cases:
        reject(lambda args=args: list(engine(*args)))
    # Successive changed inputs must not reuse an old result table.
    need(list(engine([1, 2], 3, 1)) == [0, 1, 2], "initial input control")
    need(list(engine([3, 4], 3, 1)) == [0, 4], "changed generator control")
    need(list(engine([1, 2], 3, 0)) == [0], "changed bound control")
    return len(cases), 3


def benchmark_receipt():
    receipt = json.loads((HERE / "BENCHMARK.json").read_text())
    rows = receipt["records"]
    need(len(rows) == 10 and receipt["errors"] == 0, "benchmark coverage")
    need([r["engine"] for r in rows] == ["original", "intersection"] * 5,
         "benchmark was not alternating")
    need(all(r["returncode"] == 0 and r["stderr_bytes"] == 0 for r in rows),
         "benchmark includes a failed replay")
    need(len({r["stdout_sha256"] for r in rows}) == 1, "benchmark outputs differ")
    medians = {label: statistics.median(r["seconds"] for r in rows if r["engine"] == label)
               for label in ("original", "intersection")}
    need(receipt["median_seconds"] == medians, "benchmark median changed")
    need(receipt["reduction"] == 1 - medians["intersection"] / medians["original"],
         "benchmark reduction changed")
    need(medians["intersection"] < medians["original"], "no measured improvement")
    for name, expected in receipt["implementation_sha256"].items():
        need(sha256((HERE / name).read_bytes()).hexdigest() == expected,
             "benchmark implementation changed: " + name)
    return receipt["reduction"]


def complete_callers():
    outputs = []
    for label in ("original", "intersection"):
        command = [sys.executable, "-I", "-W", "error", "-B",
                   str(HERE / "replay.py"), "--engine", label]
        result = subprocess.run(command, capture_output=True, timeout=60)
        need(result.returncode == 0 and not result.stderr,
             "complete replay failed: " + result.stderr.decode())
        need(result.stdout.startswith(b"PASS_E7_MINIMUM_SUPPORT_CLASSIFICATION\n"),
             "complete scientific work was not reported")
        outputs.append(result.stdout)
    need(outputs[0] == outputs[1], "complete classification output differs")
    return sha256(outputs[0]).hexdigest()


def main():
    sys.dont_write_bytecode = True
    replay = run_path(str(HERE / "replay.py"))
    replay["authenticate"]()
    original, current = replay["engines"]()
    code = run_path(str(HERE / "engine.py"))
    helpers = run_path(str(replay["SOURCE"] / "binary.py"))
    codes, comparisons = small_codes(original, current)
    wide = wide_codes(original, current)
    pairs = arithmetic_cases(code["translated_planes"], helpers["population_planes"])
    rejected, invalidations = controls(current)
    reduction = benchmark_receipt()
    complete_hash = complete_callers()
    names = ("README.md", "PROOF.md", "TASK.json", "SOURCES.json", "VERIFY.json",
             "engine.py", "replay.py", "verify.py", "benchmark.py", "BENCHMARK.json")
    hashes = {name: sha256((HERE / name).read_bytes()).hexdigest() for name in names}
    print(json.dumps(dict(status="PASS_E7_INTERSECTION_COUNTERS", codes=codes,
                         small_comparisons=comparisons, wide_comparisons=wide,
                         arithmetic_pairs=pairs, rejected_inputs=rejected,
                         invalidation_controls=invalidations,
                         complete_output_sha256=complete_hash,
                         recorded_local_reduction=reduction,
                         python=sys.version.split()[0], package_sha256=hashes),
                     sort_keys=True))


if __name__ == "__main__":
    main()
