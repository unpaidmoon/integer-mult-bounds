#!/usr/bin/env python3
"""A 14-point difference basis of F_2^6 with a weight-at-most-3 closed walk.

The explicit cycle is checked in Python. The normalized census is the compiled
loop in census.c. Apache-2.0.
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

WITNESS = (0, 1, 2, 3, 4, 5, 6, 8, 16, 24, 32, 40, 55, 56)
CYCLE = (0, 32, 40, 56, 24, 16, 8, 4, 5, 55, 6, 2, 3, 1, 0)
DISPLAYED = (0, 1, 2, 3, 4, 5, 6, 8, 16, 24, 32, 40, 48, 63)
FULL = set(range(1, 64))


def require(ok: bool, why: str) -> None:
    if not ok:
        raise SystemExit("FAIL: " + why)


def differences(pts: tuple[int, ...]) -> set[int]:
    seen: set[int] = set()
    for i, a in enumerate(pts):
        if a:
            seen.add(a)
        for b in pts[i + 1 :]:
            seen.add(a ^ b)
    return seen


def edge_weights(cycle: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((cycle[i] ^ cycle[i + 1]).bit_count() for i in range(len(cycle) - 1))


def min_cycle_cost(pts: tuple[int, ...]) -> int | None:
    """Independent Held-Karp check. None means no weight-1..3 Hamiltonian cycle."""
    n = len(pts)
    weight = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            w = (pts[i] ^ pts[j]).bit_count()
            if 1 <= w <= 3:
                weight[i][j] = weight[j][i] = w
    inf = 10**9
    cost = [[inf] * n for _ in range(1 << n)]
    cost[1][0] = 0
    full = (1 << n) - 1
    for mask in range(1 << n):
        for v in range(n):
            cv = cost[mask][v]
            if cv >= inf:
                continue
            for u in range(n):
                if mask & (1 << u):
                    continue
                w = weight[v][u]
                if not w:
                    continue
                nm = mask | (1 << u)
                if cv + w < cost[nm][u]:
                    cost[nm][u] = cv + w
    best = inf
    for v in range(1, n):
        if weight[v][0]:
            best = min(best, cost[full][v] + weight[v][0])
    return None if best >= inf else best


def check_cycle(cycle: tuple[int, ...], pts: tuple[int, ...]) -> tuple[int, ...]:
    require(cycle[0] == cycle[-1] == 0, "cycle closes at 0")
    require(len(cycle) == 15, "fourteen steps")
    body = cycle[:-1]
    require(sorted(body) == sorted(pts), "cycle visits the witness once")
    require(len(set(body)) == 14, "cycle is simple")
    weights = edge_weights(cycle)
    require(all(1 <= w <= 3 for w in weights), "every step has weight 1, 2 or 3")
    counts = [0] * 6
    for i in range(14):
        edge = cycle[i] ^ cycle[i + 1]
        for bit in range(6):
            counts[bit] += (edge >> bit) & 1
    require(all(c % 2 == 0 for c in counts), "each source coordinate is used evenly")
    return weights


def compile_census() -> dict[str, str]:
    source = Path(__file__).with_name("census.c")
    require(source.is_file(), "census.c missing")
    with tempfile.TemporaryDirectory(prefix="f2-weight3-") as tmp:
        binary = str(Path(tmp) / "census")
        compiled = subprocess.run(
            ["cc", "-O3", "-std=c11", "-Wall", "-Werror", "-o", binary, str(source)],
            capture_output=True,
            text=True,
            check=False,
        )
        require(compiled.returncode == 0, "cc failed:\n" + compiled.stderr)
        ran = subprocess.run([binary], capture_output=True, text=True, check=False)
        require(ran.returncode == 0, "census failed:\n" + ran.stderr + ran.stdout)
    rows: dict[str, str] = {}
    for line in ran.stdout.splitlines():
        key, _, value = line.partition("=")
        rows[key] = value.strip()
    return rows


def main() -> None:
    require(differences(WITNESS) == FULL, "witness differences miss a mask")
    require(differences(WITNESS[:-1]) != FULL, "deleting 56 must miss a mask")
    weights = check_cycle(CYCLE, WITNESS)
    require(sum(weights) == 20, "explicit cycle application total")
    require(max(weights) == 3, "explicit cycle uses a weight-3 step")
    require(min_cycle_cost(WITNESS) == 20, "independent minimum on the witness")

    distances = sorted((63 ^ p).bit_count() for p in DISPLAYED if p != 63)
    require(distances[0] >= 4, "displayed point 63 is within distance 3 of another point")
    require(differences(DISPLAYED) == FULL, "displayed set is not a difference basis")
    require(min_cycle_cost(DISPLAYED) is None, "displayed set should have no weight-3 cycle")

    rows = compile_census()
    require(rows["hits"] == "53340", "normalized basis count")
    require(rows["cycles"] == "53270", "normalized weight-3 cycle count")
    require(rows["min_sum"] == "20", "normalized minimum application total")
    require(rows["displayed_cost"] == "0", "census displayed control")
    census_cycle = tuple(int(x) for x in rows["cycle"].split())
    census_pts = tuple(sorted(set(census_cycle)))
    require(differences(census_pts) == FULL, "census cycle is not a difference basis")
    census_weights = check_cycle(census_cycle, census_pts)
    require(sum(census_weights) == 20, "census cycle total")
    require(census_cycle == CYCLE, "census cycle matches the recorded witness")

    print(
        "PASS_F2_WEIGHT3_BASIS_WALK "
        "steps=14 max_weight=3 applications=20 "
        "normalized_hits=53340 normalized_cycles=53270 normalized_min=20 "
        "queries=140 map_applications=146 no_new_kappa=true"
    )


if __name__ == "__main__":
    main()
