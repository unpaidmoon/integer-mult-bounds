#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Largest paid child rank of the selected complex word inside F_2^9.

Child rank is the dimension of one strict nested climb, or one fixed centre
descent. Both are subspaces of the word's h=9 frame space, so no paid child
has rank above 9. The unrestricted-end event graph tightens ordinary climbs
further. This checker does not build a new decoder and does not change kappa.
"""

import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
K8 = ROOT / "research" / "selected-k8-unrestricted-ends"
sys.path.insert(0, str(K8))
sys.path.insert(0, str(ROOT / "research" / "complex-local-word-ceiling"))

import ceiling  # noqa: E402
import common  # noqa: E402
import model as unrestricted  # noqa: E402

Q = Fraction
TARGET = Q(1, 99)
M = 73
FAMILIES = 896
STAGES = 9
CENTRE = 64
SELECTED = {1: 2412, 2: 418, 3: 432, 4: 142, 5: 82, 8: 8}
LOCAL_MASS = 5586


def require(ok, why):
    if not ok:
        raise SystemExit("FAIL: " + why)


def dec(value, places=16):
    sign = "-" if value < 0 else ""
    value = abs(value)
    scaled = (value.numerator * 10**places) // value.denominator
    text = str(scaled).zfill(places + 1)
    return sign + text[:-places] + "." + text[-places:]


def centre_ranks(word, frames):
    """Recompute fixed centre descents from the word, without the event graph."""
    ranks = []
    levels = {int(t): frames.basis(U) for t, U in word.get("target_levels", {}).items()}
    v = word["report"]["v"]
    for q, raw in zip(word["centers"], word["center_frames"]):
        upper = frames.basis(raw)
        served = {levels.get(e[1] - v, ()) for e in word["cut"] if e[2] == q}
        for target in sorted(served, key=lambda frame: -len(frame)):
            require(frames.contained(target, upper), "centre target not inside its frame")
            if target != upper:
                ranks.append(len(upper) - len(target))
            upper = target
    return ranks


def bracket(local):
    low, high = ceiling.ceiling(local, M, FAMILIES, STAGES, CENTRE)
    require(high - low == Q(1, 10**15), "ceiling grid is not one 1e-15 step")
    return low, high


def main():
    frames = unrestricted.M
    require(frames.H == 9, "frame alphabet is not F_2^9")
    require(frames.basis(frames.FULL) == tuple(1 << i for i in range(8, -1, -1)),
            "FULL is not the standard basis of F_2^9")
    require(len(frames.basis(tuple(range(1, 1 << 9)))) == 9, "full space has rank other than 9")

    word = common.word()
    report = word["report"]
    require(report["h"] == 9 and report["v"] == 112 and report["R"] == 480,
            "selected word geometry")
    require({int(r): n for r, n in report["local_profile"].items()} == SELECTED,
            "selected local profile")
    require(sum(r * n for r, n in SELECTED.items()) == LOCAL_MASS, "local mass")

    direct_centres = centre_ranks(word, frames)
    graph = unrestricted.Model(word)
    require(graph.centre_children == direct_centres == [8] * 8,
            "centre descents are not eight rank-8 children")

    for node in graph.order:
        low, high = graph.lo[node], graph.hi[node]
        require(frames.contained(low, high), "empty frame interval")
        require(len(low) <= len(high) <= 9, "frame dimension leaves F_2^9")
    for node, fixed in graph.fixed_frames.items():
        require(frames.contained(graph.lo[node], fixed)
                and frames.contained(fixed, graph.hi[node]),
                "fixed frame outside its interval")

    domain_frames = 0
    for node, choices in graph.domain.items():
        for choice in choices:
            domain_frames += 1
            require(frames.contained(graph.lo[node], choice)
                    and frames.contained(choice, graph.hi[node]),
                    "enumerated frame outside its interval")
            require(len(choice) <= 9, "enumerated frame above dimension 9")

    max_gap = 0
    positive_edges = 0
    for (src, dst), copies in graph.edges.items():
        if copies <= 0:
            continue
        positive_edges += 1
        gap = len(graph.hi[dst]) - len(graph.lo[src])
        require(0 <= gap <= 9, "edge dimension gap is outside 0..9")
        max_gap = max(max_gap, gap)
        # Every legal climb on this edge has rank <= gap: the source frame
        # contains lo[src] and the destination frame is contained in hi[dst].
        given_src = graph.frame_of(src, graph.baseline())
        given_dst = graph.frame_of(dst, graph.baseline())
        require(frames.contained(given_src, given_dst), "baseline climb is not nested")
        require(len(given_dst) - len(given_src) <= gap, "baseline climb exceeds the edge cap")
    require(max_gap == 6, "positive-edge climb cap is not 6")

    cone_edges = set(graph.cone_edges)
    cone_paid = sum(1 for edge in cone_edges if graph.edges.get(edge, 0) > 0)
    cone_zero = sum(1 for edge in cone_edges if graph.edges.get(edge, 0) == 0)
    require(cone_paid == 0 and cone_zero == len(cone_edges) == 106,
            "cone restoration edges are not exactly 106 zero-charge edges")

    profile = graph.profile(graph.baseline())
    require(profile == SELECTED, "baseline paid profile")
    require(max(profile) == 8, "baseline emits a child above rank 8")
    # Centre rank 8 is above the graph-edge cap, so it is the global maximum.
    require(max(direct_centres) > max_gap, "centre rank does not strictly exceed graph climbs")

    selected_lo, selected_hi = bracket(SELECTED)
    require(selected_hi == Q(1690054109089, 10**15), "selected ceiling moved")
    rank9 = {9: Q(LOCAL_MASS, 9)}
    rank8 = {8: Q(LOCAL_MASS, 8)}
    rank8_int = {8: 698, 2: 1}
    rank9_int = {9: 620, 6: 1}
    require(sum(r * n for r, n in rank8_int.items()) == LOCAL_MASS, "rank-8 integer mass")
    require(sum(r * n for r, n in rank9_int.items()) == LOCAL_MASS, "rank-9 integer mass")
    cap8_lo, cap8_hi = bracket(rank8)
    cap8i_lo, cap8i_hi = bracket(rank8_int)
    cap9_lo, cap9_hi = bracket(rank9)
    cap9i_lo, cap9i_hi = bracket(rank9_int)
    cap43_lo, cap43_hi = bracket({43: Q(LOCAL_MASS, 43)})
    cap44 = {44: 126, 42: 1}
    require(sum(r * n for r, n in cap44.items()) == LOCAL_MASS, "rank-44 integer mass")
    cap44_lo, cap44_hi = bracket(cap44)
    for name, high in (
        ("selected", selected_hi),
        ("cap8", cap8_hi),
        ("cap8-integer", cap8i_hi),
        ("cap9", cap9_hi),
        ("cap9-integer", cap9i_hi),
        ("cap43", cap43_hi),
    ):
        require(high < TARGET, name + " reaches 1/99")
    require(cap44_lo > TARGET, "rank-44 greedy histogram does not clear 1/99")
    require(selected_hi < cap8_hi < cap9_hi < cap43_hi < TARGET < cap44_lo,
            "ceiling order")

    try:
        ceiling.model(SELECTED, M, FAMILIES, STAGES, CENTRE, R=52)
    except ValueError as exc:
        require("halving guard" in str(exc), "idle rank 52 failed for the wrong reason")
    else:
        raise SystemExit("FAIL: idle rank 52 was accepted")

    # The packing model will price a rank-10 histogram. The frame contract cannot emit it.
    rank10_lo, rank10_hi = bracket({10: Q(LOCAL_MASS, 10)})
    require(rank10_hi < TARGET, "rank 10 already clears 1/99")
    require(10 > frames.H, "rank 10 is inside the frame alphabet")

    print(
        "PASS_F2_NINE_PAID_CHILD_RANK"
        f" H=9 graph_climb_cap={max_gap} centre=8x8 paid_rank_cap=8"
        f" positive_edges={positive_edges} cone_edges={cone_zero}"
        f" domain_frames={domain_frames}"
        f" selected_hi={dec(selected_hi)}"
        f" cap8_hi={dec(cap8_hi)} cap9_hi={dec(cap9_hi)}"
        f" cap43_hi={dec(cap43_hi)} cap44_lo={dec(cap44_lo)}"
        " target=1/99 cleared_by_physical_cap=no no_new_kappa"
    )
    del cap8_lo, cap8i_lo, cap9_lo, cap9i_lo, cap43_lo, cap44_hi, rank10_lo


if __name__ == "__main__":
    main()
