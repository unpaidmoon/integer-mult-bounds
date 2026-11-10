#!/usr/bin/env python3
"""Shared-chart terminal for one heterogeneous centre offer. No new kappa.

The strip-all policy in research/center-chain-terminal-feasibility moves every
touched rank-8 and rank-9 field to the empty chart and back. This checker
builds a different suffix: form each selected observation at the single
rank-9 chart that already holds its X block and pivot, bring each selected
centre there, then bring each affected Y row to that same chart for the
correction and return it. The predecessor evaluator is the legality and
endpoint oracle. The optimistic incremental moment stays strictly negative.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
NORMAL = ROOT / "research/center-helper-normal-form"
CHAIN = ROOT / "research/center-chain-terminal-feasibility"
CHART1 = 1


def need(ok, message):
    if not ok:
        raise ValueError(message)


def load_module(path, name):
    spec = spec_from_file_location(name, path)
    module = module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def pins():
    manifest = json.loads((HERE / "SOURCES.json").read_text())
    for row in manifest["files"]:
        if row["usage"] != "input":
            continue
        digest = sha256((ROOT / row["path"]).read_bytes()).hexdigest()
        need(digest == row["sha256"], "changed source " + row["path"])
    return manifest["base_commit"]


def span(basis):
    out = {0}
    for vector in basis:
        out |= {item ^ vector for item in tuple(out)}
    return out


def y_rows(abi, centres):
    selected = set(centres)
    rows = {}
    for index, row in enumerate(abi["B_rows"]):
        coefficients = {key - 632: Fraction(value) for key, value in row if key - 632 in selected}
        if coefficients:
            rows[index] = coefficients
    return rows


def observation(rows, pivot):
    return {index: value for index, value in rows.items() if index < 224} | {pivot: 1}


def schedule(centres, abi, observations, final, pivots):
    """Y rows travel to chart 1; centres travel between chart 0 and chart 1."""
    tail = []
    for centre in centres:
        pivot = pivots[centre]
        for index, value in sorted(observations[centre].items()):
            if index != pivot:
                tail.append(("add", pivot, index, value, CHART1))
        tail.append(("transport", 632 + centre, 0, CHART1, 9))
        tail.append(("add", 632 + centre, pivot, -1, CHART1))
        for index, value in sorted(observations[centre].items()):
            if index != pivot:
                tail.append(("add", pivot, index, -value, CHART1))
    rows = y_rows(abi, centres)
    for index, coefficients in sorted(rows.items()):
        chart = final[index]
        tail.append(("transport", index, chart, CHART1, 1))
        for centre, value in sorted(coefficients.items()):
            tail.append(("add", index, 632 + centre, -value, CHART1))
        tail.append(("transport", index, CHART1, chart, 1))
    for centre in centres:
        tail.append(("transport", 632 + centre, CHART1, 0, 9))
    return tail, rows


def moment_floor(width_counts):
    """Lower bound of sum c_w w^t on t in [0,1], using w^t >= 1."""
    return sum(width_counts.values())


def moment_cap(width_counts):
    """Upper bound of sum c_w w^t on t in [0,1], using w^t <= w."""
    return sum(count * width for width, count in width_counts.items())


def prepare():
    base = pins()
    normal = load_module(NORMAL / "verify.py", "centre_normalizer")
    engine = load_module(NORMAL / "inputs/retained_verify.py", "centre_emitter")
    engine.HERE = NORMAL
    chain = load_module(CHAIN / "verify.py", "centre_chain_terminal")
    payload = engine.load()
    frames = payload["canonical"]["frames"]
    abi = json.loads((NORMAL / "inputs/ABI.json").read_text())
    rational_rows = [{index: Fraction(value) for index, value in row} for row in abi["R_rows"]]
    cold = {
        index for index in range(224, 632)
        if payload["canonical"]["start"][index] == 0 and payload["canonical"]["final"][index] == 1
    }
    header, determinant, _ = normal.make_header(rational_rows, cold)
    footer = normal.inverse_header(header, 1)
    need(len(header) == len(footer) == 379 and determinant == 64, "joint normalization not charged whole")
    starts, _, source = engine.emit(payload)
    final = payload["canonical"]["final"] + [0] * 8
    observations = [observation(rational_rows[centre], normal.J[centre]) for centre in range(8)]
    word = header + source + footer
    original, old_paid = chain.evaluate(word, starts, final, frames)
    need(original == chain.target(abi, observations, set()), "source ABI drifted")
    need(old_paid == Counter(engine.PAID), "source paid profile drifted")
    chart_span = span(frames[CHART1])
    need(len(frames[CHART1]) == 9 and len(chart_span) == 512, "chart 1 is not the full rank-9 frame")
    geometry = []
    for centre in range(8):
        pivot = normal.J[centre]
        data = [index for index in observations[centre] if index != pivot]
        need(len(data) == 56, "X block is not 56 registers")
        need(all(final[index] == CHART1 for index in data), "X block leaves chart 1")
        need(final[pivot] == CHART1, "pivot leaves chart 1")
        rows = y_rows(abi, (centre,))
        charts = [final[index] for index in rows]
        need(len(charts) == len(set(charts)) == 56, "Y charts are not 56 distinct registers")
        subspaces = []
        for chart in charts:
            basis = frames[chart]
            image = span(basis)
            need(len(basis) == 8 and image < chart_span, "Y chart is not codimension 1 in chart 1")
            subspaces.append(image)
        incomparable = 0
        for left in range(len(subspaces)):
            for right in range(left + 1, len(subspaces)):
                if subspaces[left] < subspaces[right] or subspaces[right] < subspaces[left]:
                    incomparable += 1
        need(incomparable == 0, "two Y charts are nested")
        geometry.append(dict(centre=centre, x=56, y=56, y_pairs_nested=0))
    return dict(base=base, chain=chain, normal=normal, abi=abi, observations=observations,
                final=final, frames=frames, starts=starts, word=word, old_paid=old_paid,
                header=header, footer=footer, engine=engine, geometry=geometry)


def screen(state, centres, dual):
    chain = state["chain"]
    centres = tuple(centres)
    tail, rows = schedule(centres, state["abi"], state["observations"], state["final"], state["normal"].J)
    actual, paid = chain.evaluate(state["word"] + tail, state["starts"], state["final"], state["frames"])
    wanted = chain.target(state["abi"], state["observations"], set(centres))
    need(actual == wanted, "shared-chart endpoint missed " + str(centres))
    extra = paid - state["old_paid"]
    predicted = Counter({1: 2 * len(rows), 9: 2 * len(centres)})
    need(extra == predicted, "paid profile " + str(dict(extra)) + " != " + str(dict(predicted)))
    reward = Counter({8: len(centres)})
    # w^t <= w and 1^t = 1 give reward <= 8s and cost >= 2u + 2s.
    deficit_floor = moment_floor(extra) - moment_cap(reward)
    need(deficit_floor == 2 * len(rows) - 6 * len(centres) > 0, "moment floor is not positive")
    # Exact endpoint deficits: t=0 uses 9^0=1 and 8^0=1; t=1 uses 9 and 8.
    endpoint_deficit = {
        "0": 2 * len(rows) + len(centres),
        "1": 2 * len(rows) + 10 * len(centres),
    }
    strip, info = chain.terminal(centres, state["abi"], state["observations"], state["final"],
                                 state["frames"], state["normal"].J)
    strip_paid = Counter(event[4] for event in strip if event[0] == "transport")
    need(strip_paid == Counter(info["extra_paid"]), "strip receipt does not match its word")
    need(set(strip_paid) <= {8, 9} and strip_paid[9] >= extra[9] and strip_paid[8] >= 0,
         "strip profile left the compared alphabet")
    strip_advantage_at_zero = strip_paid[8] + (strip_paid[9] - extra[9]) - extra[1]
    need(strip_advantage_at_zero >= 1, "shared chart does not beat the strip policy at t=0")
    if dual:
        inverse = chain.inverse(wanted)
        _, _, dual_source = state["engine"].emit(state["engine"].load(), dual=True)
        normal = state["normal"]
        dual_word = (normal.dual_header(state["header"]) + dual_source
                     + normal.dual_header(state["footer"]) + chain.raw_dual(tail))
        dual_rows, dual_paid = chain.evaluate(dual_word, state["starts"], state["final"], state["frames"])
        need(dual_rows == chain.transpose(inverse) and dual_paid == paid, "raw dual mismatch " + str(centres))
    return dict(centres=list(centres), y_registers=len(rows), extra_paid=dict(sorted(extra.items())),
                reward={"8": len(centres)}, deficit_floor=deficit_floor,
                endpoint_deficits=endpoint_deficit,
                strip_paid=dict(sorted(strip_paid.items())),
                strip_advantage_at_zero=strip_advantage_at_zero,
                scalar_adds=sum(event[0] == "add" for event in tail),
                dual_checked=dual)


def controls(state):
    chain = state["chain"]
    centres = (0,)
    tail, _ = schedule(centres, state["abi"], state["observations"], state["final"], state["normal"].J)
    wanted = chain.target(state["abi"], state["observations"], {0})
    y_add = next(index for index, event in enumerate(tail)
                 if event[0] == "add" and event[1] < 224 and event[2] == 632)
    omitted = tail[:y_add] + tail[y_add + 1:]
    got, _ = chain.evaluate(state["word"] + omitted, state["starts"], state["final"], state["frames"])
    need(got != wanted, "omitted Y correction was accepted")
    pivot = state["normal"].J[0]
    restored = [event for event in tail if not (event[0] == "add" and event[1] == pivot and event[3] < 0)]
    got, _ = chain.evaluate(state["word"] + restored, state["starts"], state["final"], state["frames"])
    need(got != wanted, "unrestored pivot was accepted")
    climb = next(index for index, event in enumerate(tail) if event[0] == "transport" and event[1] == 632)
    bad = list(tail)
    event = bad[climb]
    bad[climb] = (event[0], event[1], event[2], event[3], event[4] - 1)
    rejected = False
    try:
        chain.evaluate(state["word"] + bad, state["starts"], state["final"], state["frames"])
    except ValueError:
        rejected = True
    need(rejected, "undercharged width was accepted")
    rows = sorted(y_rows(state["abi"], centres))
    left, right = state["final"][rows[0]], state["final"][rows[1]]
    direct = [("transport", rows[0], left, right, 0)]
    rejected = False
    try:
        chain.evaluate(state["word"] + direct, state["starts"], state["final"], state["frames"])
    except ValueError:
        rejected = True
    need(rejected, "direct Y-to-Y transport was accepted")
    return ["omitted Y correction", "unrestored pivot", "undercharged width", "direct Y-to-Y transport"]


def main():
    state = prepare()
    screens = []
    for centre in range(8):
        screens.append(screen(state, (centre,), dual=True))
    for pair in combinations(range(8), 2):
        screens.append(screen(state, pair, dual=True))
    screens.append(screen(state, tuple(range(8)), dual=True))
    failures = controls(state)
    need(len(screens) == 8 + 28 + 1, "case census is incomplete")
    need(all(row["deficit_floor"] > 0 for row in screens), "some case does not lose")
    report = dict(status="PASS_SHARED_CHART_TERMINAL_LOSES", new_kappa=None,
                  base_commit=state["base"], geometry=state["geometry"],
                  source_paid=dict(sorted(state["old_paid"].items())),
                  cases=len(screens), singleton=screens[0], pair=screens[8],
                  all_eight=screens[-1], deficit_floors=sorted({row["deficit_floor"] for row in screens}),
                  controls=failures,
                  normalization_gates=758,
                  claim="optimistic incremental moment stays negative; not an unrestricted producer obstruction")
    text = json.dumps(report, sort_keys=True)
    need("PASS_SHARED_CHART_TERMINAL_LOSES" in text and report["new_kappa"] is None, "receipt marker")
    print("PASS_SHARED_CHART_TERMINAL_LOSES cases={0} deficit_floors={1} no_new_kappa".format(
        report["cases"], ",".join(str(item) for item in report["deficit_floors"])))


if __name__ == "__main__":
    main()
