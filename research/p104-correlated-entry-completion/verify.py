#!/usr/bin/env python3
"""Full-column entry, exact cleanup information and scoped frame geometry.

Prepared for @CubeJerry with OpenAI Codex assistance. Apache-2.0.
"""
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path
from runpy import run_path

M = run_path(str(Path(__file__).with_name("model.py")))
require = M["require"]


def mod_rank(rows, p):
    work = [[int(x) % p for x in row] for row in rows]
    i = 0
    for j in range(len(work[0])):
        k = next((k for k in range(i, len(work)) if work[k][j]), None)
        if k is None:
            continue
        work[i], work[k] = work[k], work[i]
        inv = pow(work[i][j], -1, p)
        work[i] = [v * inv % p for v in work[i]]
        for k in range(i + 1, len(work)):
            a = work[k][j]
            work[k] = [(x - a * y) % p for x, y in zip(work[k], work[i])]
        i += 1
        if i == len(work):
            break
    return i


def entry_census(p):
    """All sparse A0 and aggregate S, not a census of physical programs."""
    pool = list(itertools.product(range(p), repeat=4))
    sparse = [row for row in pool if sum(bool(x) for x in row) < 3]
    P = (1, 1, 1, 1, 1, 0)
    W = (p - 1, 1, 1, 1, 0, 0)
    checked = feasible = 0
    for A0 in sparse:
        for S in pool:
            rows = [A0 + (1, 0), (0, 0, 0, 0, 0, p - 1), S + (0, 1)]
            r = mod_rank(rows, p)
            actual = mod_rank(rows + [P, W], p) == r
            expected = A0 == (2 % p, 0, 0, 0) and any(
                S == ((-t) % p, t, t, t) for t in range(1, p))
            require(actual == expected, "independent entry classification")
            checked += 1
            feasible += actual
    require(feasible == p - 1, "entry equality count")
    return {"field": p, "quotient_entry_cases": checked, "feasible": feasible}


def correlated_Y_census():
    """Check the stronger necessary ratio with Y on the two dirty arrivals."""
    p = 3
    pool = list(itertools.product(range(p), repeat=4))
    sparse = [row for row in pool if sum(bool(x) for x in row) < 3]
    P, W = (1, 1, 1, 1, 1, 0), (2, 1, 1, 1, 0, 0)
    checked = feasible = 0
    for k, sY in itertools.product(range(p), repeat=2):
        for A0 in sparse:
            for S in pool:
                rows = [A0 + (k, 0), (0, 0, 0, 0, 0, 2), S + (sY, 1)]
                actual = mod_rank(rows + [P, W], p) == mod_rank(rows, p)
                expected = k != 0 and A0 == (2 * k % p, 0, 0, 0) and any(
                    S == ((2 * sY - t) % p, t, t, t) for t in range(1, p))
                require(actual == expected, "correlated-Y entry classification")
                checked += 1
                feasible += actual
    require(feasible == 12, "correlated-Y equality count")
    return {"field": p, "quotient_entry_cases": checked, "feasible": feasible}


def run():
    f = M["fixture"]()
    result = M["replay"](f["incoming"], M["MEETING"])
    M["endpoint"](result, f["expected"])
    require(M["replay"](result, M["INVERSE"]) == f["incoming"], "inverse endpoint")
    require(all(f["incoming"][i] != result[i] for i in (0, 1)), "two-write lower bound")
    require(not M["in_span"](f["h"], result), "no-query restoration obstruction")
    require(M["rank"](result) == 3 and M["rank"](result + [f["h"]]) == 4,
            "restoration rank gap")
    iu = next(i for i, value in enumerate(f["a"]) if value)
    iv = next(i for i, value in enumerate(f["d"]) if value)
    collision = [Q(0)] * 209
    collision[iu], collision[iv], collision[-1] = 1 / f["a"][iu], -1 / f["d"][iv], Q(1)
    require(all(sum(x * y for x, y in zip(row, collision)) == 0 for row in result),
            "same-observation collision")
    require(sum(x * y for x, y in zip(f["h"], collision)) == 1,
            "collision separates original helper")

    # Explicit original dirty-column discriminator, not a claim that PR6261
    # promised a complete endpoint. Its response projection remains correct.
    old = [M["add"](f["Y"], f["e"]), M["add"](f["a"], f["h"], -1),
           M["add"](f["d"], f["h"])]
    old_output = M["replay"](old, M["OLD_MEETING"])
    require(old_output[0] == f["expected"][0], "old partner control")
    require(old_output[1] == M["add"](f["minus"], f["Y"], -1), "old Y leak")
    require(old_output[2] == f["expected"][2], "old helper column")
    require(all(old_output[i][:104] == f["expected"][i][:104] for i in range(3)),
            "old projected positive control")

    frame_receipt = {}
    for name, ps, n in [("first", f["first"], 6), ("second", f["second"], 6),
                        ("common", f["common"], 7)]:
        require(M["binary_rank"](ps) == n and len(M["xor_span"](ps)) == 2 ** n,
                "independent frame span")
        frame_receipt[name] = {"support": len(ps), "rank": n}

    queries = []
    for lam in map(Q, (-2, -1, 0, 1, 2)):
        for rho in (Q(-2), Q(1, 2), Q(1)):
            query = M["scale"](M["add"](f["d"], f["minus"], lam), rho)
            M["cleanup_allowed"](query, f)
            require(M["dyadic_cleanup_coefficients"](query, f) == (-1 / rho, lam),
                    "dyadic cleanup coefficients")
            events = [("ADD", 2, 3, -1 / rho)]
            if lam:
                events.append(("ADD", 2, 1, lam))
            final = M["replay"]([*result, query], events)
            M["endpoint"](final, [result[0], result[1], f["h"], query])
            active = [p for p, value in zip(f["ports"], query[:104]) if value]
            size, dim = (8, 6) if lam == 0 else ((16, 6) if lam == -1 else (24, 7))
            require(len(active) == size and M["binary_rank"](active) == dim,
                    "cleanup support classification")
            queries.append({"lambda": str(lam), "rho": str(rho),
                            "support": size, "frame_dimension": dim})

    # The source singleton is a legal same-frame row operation before growth:
    # span{487} lies in G, and 2e is exactly the live X487 coordinate.
    zi = f["ports"].index(487)
    source = tuple(Q(i == zi) for i in range(209))
    require(source == M["scale"](f["e"], 2), "singleton source coefficient")
    require(M["in_frame"](487, (11, 19)), "singleton nested frame")
    prepared = M["replay"]([f["Y"], source], (("ADD", 0, 1, 1),))
    require(prepared == [f["incoming"][0], source], "singleton preparation")

    # One additional clean-query completion is exact, and counts all four
    # visible scalar writes: singleton preparation, two meeting writes, cleanup.
    completed = M["replay"]([*f["incoming"], f["d"]],
                             (*M["MEETING"], ("ADD", 2, 3, -1)))
    M["endpoint"](completed, [result[0], result[1], f["h"], f["d"]])

    return {"status": "PASS_P104_CORRELATED_ENTRY_COMPLETION", "input_columns": 209,
            "meeting_ADDs": 2, "inverse_ADDs": 2,
            "source_loaded_completion_visible_ADDs": 4,
            "no_query_rank": 3, "rank_with_original_h": 4,
            "same_observation_collision": {
                "live_port_shifts": {str(f["ports"][iu]): str(collision[iu]),
                                     str(f["ports"][iv]): str(collision[iv])},
                "original_h_shift": "1", "all_three_observed_shifts": ["0", "0", "0"]},
            "old_projection_passes_but_Y_leaks": True,
            "frames": frame_receipt, "cleanup_queries": queries,
            "finite_entry_census": [entry_census(3), entry_census(5)],
            "correlated_Y_census": correlated_Y_census(),
            "conditional_incoming_paid_ranks": {"1": 4, "6": 1},
            "complete_supplier_invoice": False, "new_kappa": False,
            "source_hashes": M["source_hashes"]()}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
