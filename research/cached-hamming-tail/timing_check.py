"""Retained measurement arithmetic, produced by Nick Petalas. Apache-2.0."""

from fractions import Fraction
from hashlib import sha256
import json
from math import comb
from pathlib import Path
import statistics

HERE = Path(__file__).resolve().parent


def need(condition, reason):
    if not condition:
        raise ValueError(reason)


def rank_sum_probability(left, right):
    """Exact two-sided permutation probability, for the fixed 30+30 sample."""
    need(len(left) == len(right) == 30, "thirty samples per side")
    need(len(set(left + right)) == 60, "rank-sum calculation assumes no ties")
    u = sum(x > y for x in right for y in left)
    counts = {(0, 0): 1}
    for rank in range(1, 61):
        updated = dict(counts)
        for (selected, total), count in counts.items():
            if selected < 30:
                key = selected + 1, total + rank
                updated[key] = updated.get(key, 0) + count
        counts = updated
    tail = sum(count for (selected, total), count in counts.items()
               if selected == 30 and total - 465 <= min(u, 900 - u))
    return u, Fraction(2 * tail, comb(60, 30))


def measurements():
    rows = []
    for filename, pairs in (("TIMINGS-INITIAL.json", 9), ("TIMINGS-CONFIRMATION.json", 21)):
        report = json.loads((HERE / filename).read_text())
        need(report["pairs"] == pairs and report["errors"] == 0, "measurement coverage")
        need(len(report["rows"]) == pairs * 2, "complete sample rows")
        for name, expected in report["source_sha256"].items():
            need(sha256((HERE / name).read_bytes()).hexdigest() == expected, "timed source bytes")
        for pair in range(pairs):
            block = report["rows"][2 * pair:2 * pair + 2]
            expected_order = ["baseline", "candidate"] if pair % 2 == 0 else ["candidate", "baseline"]
            need([r["side"] for r in block] == expected_order, "alternating sample order")
            need(all(r["pair"] == pair for r in block), "sample pair")
        rows.extend(report["rows"])
    need(all(r["counts"] == {"entered": 7350, "pruned": 4381, "closed": 828, "universal": 828}
             for r in rows), "same complete caller work")
    expected = "2e64b75bdd56124eb0993e0dcb2b79f849435465c32bdc9329ea2c171b506727"
    need(all(r["hashes"] == [expected, expected] for r in rows), "both complete word sets")
    return rows


def main():
    rows = measurements()
    baseline = [r["wall_ns"] for r in rows if r["side"] == "baseline"]
    candidate = [r["wall_ns"] for r in rows if r["side"] == "candidate"]
    ratios = []
    for index in range(0, 60, 2):
        block = {r["side"]: r["wall_ns"] for r in rows[index:index + 2]}
        ratios.append(Fraction(block["candidate"], block["baseline"]))
    u, probability = rank_sum_probability(baseline, candidate)
    output = {"status": "PASS_RETAINED_TIMING_ARITHMETIC", "pairs": 30, "errors": 0,
              "baseline_ns": [statistics.median(baseline), min(baseline), max(baseline)],
              "candidate_ns": [statistics.median(candidate), min(candidate), max(candidate)],
              "median_paired_ratio": str(statistics.median(ratios)),
              "faster_pairs": sum(r < 1 for r in ratios), "rank_sum_U": u,
              "descriptive_two_sided_rank_sum_probability": str(probability)}
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
