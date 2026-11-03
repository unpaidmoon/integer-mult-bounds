#!/usr/bin/env python3
"""Meaningful rejection controls for the full-column and cleanup claims.

Prepared for @CubeJerry with OpenAI Codex assistance. Apache-2.0.
"""
from fractions import Fraction as Q
from pathlib import Path
from runpy import run_path

M = run_path(str(Path(__file__).with_name("model.py")))


def reject(name, message, operation):
    try:
        operation()
    except ValueError as error:
        M["require"](str(error) == message, "wrong rejection reason: " + name)
        return
    raise ValueError("control accepted: " + name)


def main():
    f = M["fixture"]()
    rows = f["incoming"]
    expect = f["expected"]
    controls = 0

    def endpoint_case(name, altered, events=M["MEETING"]):
        nonlocal controls
        reject(name, "full-column endpoint", lambda: M["endpoint"](M["replay"](altered, events), expect))
        controls += 1

    endpoint_case("old singleton normalization", [M["add"](f["Y"], f["e"]), *rows[1:]])
    endpoint_case("omit exceptional wire coefficient", [rows[0], M["add"](f["a"], f["h"], -1), rows[2]])
    endpoint_case("same-sign helper dirt", [rows[0], M["add"](M["add"](f["a"], f["e"], -1), f["h"]), rows[2]])
    endpoint_case("extra public Y in wire", [rows[0], M["add"](rows[1], f["Y"]), rows[2]])
    endpoint_case("omit second meeting write", rows, M["MEETING"][:1])

    reject("aliased row operation", "ADD alias", lambda: M["replay"](rows, (("ADD", 1, 1, 1),)))
    controls += 1
    reject("source corruption", "port source hash", lambda: M["authenticate"](b"[]\n"))
    controls += 1
    reject("query is just outgoing wire", "cleanup query lacks required quotient",
           lambda: M["cleanup_allowed"](f["minus"], f))
    controls += 1
    reject("query has independent dirt", "cleanup query must be pure live",
           lambda: M["cleanup_allowed"](M["add"](f["d"], f["Y"]), f))
    controls += 1
    nonunit_query = M["scale"](f["d"], 3)
    M["cleanup_allowed"](nonunit_query, f)  # A valid field-linear query.
    reject("nonunit dyadic query scaling", "cleanup scale is not a dyadic unit",
           lambda: M["dyadic_cleanup_coefficients"](nonunit_query, f))
    controls += 1

    for p in f["common"]:
        query = tuple(Q(i == f["ports"].index(p)) for i in range(209))
        reject("singleton cleanup", "cleanup query lacks required quotient",
               lambda query=query: M["cleanup_allowed"](query, f))
        controls += 1

    # Every five-dimensional subframe of the exact rank-six d-span fails.
    span = M["xor_span"](f["second"])
    hyperplanes = {tuple(sorted(v for v in span if not (v & n).bit_count() % 2))
                  for n in range(1, 512)}
    hyperplanes.discard(tuple(sorted(span)))
    M["require"](len(hyperplanes) == 63, "rank-six hyperplane census")
    for frame in hyperplanes:
        reject("five-frame query", "public query support outside frame",
               lambda frame=frame: M["public_query_frame"](f["d"], f["ports"], set(frame)))
        controls += 1

    # Positive boundaries: q=d and q=d+2W both restore h. A support restriction
    # is intentionally NOT applied to an owned-delivered query in a small frame.
    for query in (f["d"], M["add"](f["d"], f["minus"], 2)):
        M["cleanup_allowed"](query, f)
    M["public_query_frame"](f["d"], f["ports"], span)
    print("PASS_P104_CORRELATED_ENTRY_CONTROLS", controls, "exact-reason rejections")


if __name__ == "__main__":
    main()
