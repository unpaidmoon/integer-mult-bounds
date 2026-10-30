#!/usr/bin/env python3
"""Absolute phase of selected MOVE chart changes scales as i^{p f}.

The all-width statement is Lemma 2 in PROOF.md. This program binds it to the
selected #6030 word and checks the phase gates on that word's own operators.
"""

from collections import Counter
from hashlib import sha256
import gzip
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WORD = ROOT / "research/p104-helper470-twin-rung-removal/WORD.json.gz"
PREVIOUS = ROOT / "research/p104-helper-subspace-splits/WORD.json.gz"
CLIFFORD = ROOT / "research/p104-native-channel/vendor/clifford_exact.py"
NATIVE = ROOT / "research/p104-native-channel/vendor/native_verify.py"
WORD_SHA256 = "7834725d9e34ee846a9ccc615221ea81e0201613938afa185d2eda0c9a6c232f"
PREVIOUS_SHA256 = "bbb072bced5824a8d9094c49be2fc51fbfdd05fb2b7dab8106e1275053075099"
PAIR_PHASE = {0: 1077, 1: 994, 2: 239, 3: 576}
EVENT_PHASE = {0: 1336, 1: 1255, 2: 246, 3: 616}
ONLY_NEW_PAIRS = {0: 23, 1: 17, 2: 20, 3: 18}
ONLY_NEW_EVENTS = {0: 42, 1: 18, 2: 24, 3: 19}


def need(ok, why):
    if not ok:
        raise ValueError(why)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def span(basis):
    out = {0}
    for value in basis:
        need(type(value) is int and 0 < value < 512 and value not in out, "Independent frame vector")
        out |= {point ^ value for point in tuple(out)}
    return frozenset(out)


def walk(word):
    """Chart transport of the selected word. Returns MOVE endpoint pairs."""
    public = word["public"]
    owned = word["owned_fields"]
    need(word.get("schema") == "p104-accumulated-block-composition/2", "Selected word schema")
    need(public == 770 and owned == 29, "Selected inventory")
    need(len(word["initial"]) == len(word["final"]) == public, "Public boundary")
    frames = [span(row) for row in word["frames"]]
    current = list(word["initial"]) + [None] * owned
    live = set()
    moves = []
    counts = Counter()
    for event in word["program"]:
        need(isinstance(event, list) and event, "Event shape")
        op, role = event[0], event[1]
        need(op in ("MOVE", "INIT", "CLEAR", "ADD", "SCALE", "COPY"), "Opcode")
        need(isinstance(role, int) and 0 <= role < public + owned, "Role")
        counts[op] += 1
        if op == "MOVE":
            need(len(event) == 5 and type(event[4]) is bool, "MOVE shape")
            source, destination, private = event[2], event[3], event[4]
            need(current[role] == source, "MOVE leaves the recorded chart")
            need((role in live) is private, "MOVE ownership flag")
            need(0 <= source < len(frames) and 0 <= destination < len(frames), "Frame index")
            if private:
                need(frames[destination] < frames[source], "Private transport shrinks the chart")
            else:
                need(frames[source] < frames[destination], "Public transport enlarges the chart")
            current[role] = destination
            moves.append((source, destination, abs(len(word["frames"][destination]) - len(word["frames"][source]))))
        elif op == "INIT":
            need(len(event) == 3 and role >= public and role not in live, "INIT")
            live.add(role)
            current[role] = event[2]
        elif op == "CLEAR":
            need(len(event) == 3 and role in live and current[role] == event[2], "CLEAR")
            live.remove(role)
            current[role] = None
        else:
            frame = event[-1]
            need(current[role] == frame, "Scalar destination chart")
            if op != "SCALE":
                source = event[2]
                need(isinstance(source, int) and source != role, "Scalar source")
                need(current[source] == frame, "Common scalar chart")
    need(not live and current[:public] == word["final"], "Public exit charts")
    need(counts["MOVE"] == 3453 and counts["ADD"] == 18404, "Selected opcode counts")
    return moves


def reject(word, mutate):
    trial = json.loads(json.dumps(word))
    mutate(trial)
    try:
        walk(trial)
    except ValueError:
        return
    raise ValueError("Mutated word was accepted")


def rotate_state(native, state, power):
    value, denominator = state
    return {addr: native.rotate(pair, power) for addr, pair in value.items()}, denominator


def move_pairs(word):
    pairs = []
    for event in word["program"]:
        if event[0] != "MOVE":
            continue
        need(len(event) == 5, "MOVE shape")
        pairs.append((event[2], event[3]))
    return pairs


def main():
    raw = WORD.read_bytes()
    need(sha256(raw).hexdigest() == WORD_SHA256, "Selected word bytes")
    previous_raw = PREVIOUS.read_bytes()
    need(sha256(previous_raw).hexdigest() == PREVIOUS_SHA256, "PR5599 word bytes")
    word = json.loads(gzip.decompress(raw))
    previous = json.loads(gzip.decompress(previous_raw))
    need(previous.get("schema") == "p104-productive-source/1", "PR5599 schema")
    moves = walk(word)
    previous_pairs = move_pairs(previous)
    need(len(previous_pairs) == 3447, "PR5599 MOVE count")
    first_move = next(i for i, event in enumerate(word["program"]) if event[0] == "MOVE")

    def bad_source(trial):
        trial["program"][first_move][2] = (trial["program"][first_move][2] + 1) % len(trial["frames"])

    def bad_nesting(trial):
        # Keep the recorded source chart and destroy strict span nesting.
        trial["program"][first_move][3] = trial["program"][first_move][2]

    reject(word, bad_source)
    reject(word, bad_nesting)

    clifford = load(CLIFFORD, "move_phase_clifford")
    native = load(NATIVE, "move_phase_native")
    used = {frame for source, destination, _rank in moves for frame in (source, destination)}
    charts = {i: clifford.canonical_frame(9, tuple(word["frames"][i])) for i in used}
    pair_phase = {}
    samples = {}
    for source, destination, rank in moves:
        key = (source, destination)
        if key in pair_phase:
            need(pair_phase[key][0] == rank, "Repeated MOVE rank")
            continue
        record, _compiled = clifford.lower_child(charts[source].adjoint().then(charts[destination]))
        recipe = native.recipe(record)
        gates = [gate[1] for gate in recipe if gate[0] == "phase"]
        right = 0 if record["right"] is None else record["right"]["phase"]
        phase = sum(gates) % 4
        need(record["left"]["phase"] == 0 and right == phase and record["rank"] == rank, "Phase and rank")
        need(phase in PAIR_PHASE, "Phase residue")
        pair_phase[key] = (rank, phase, recipe)
        samples.setdefault(phase, (source, destination, recipe))
    need(len(pair_phase) == 2886, "Distinct MOVE operators")
    pairs = Counter(phase for _rank, phase, _recipe in pair_phase.values())
    events = Counter(pair_phase[(source, destination)][1] for source, destination, _rank in moves)
    need(dict(pairs) == PAIR_PHASE and dict(events) == EVENT_PHASE, "Phase census")
    selected_pairs = set(pair_phase)
    earlier_pairs = set(previous_pairs)
    only_new = selected_pairs - earlier_pairs
    need(len(earlier_pairs) == 2887 and len(only_new) == 78, "Certificate pair gap")
    need(len(earlier_pairs - selected_pairs) == 79 and len(earlier_pairs & selected_pairs) == 2808, "Shared charts")
    only_new_pairs = Counter(pair_phase[key][1] for key in only_new)
    only_new_events = Counter(
        pair_phase[(source, destination)][1]
        for source, destination, _rank in moves
        if (source, destination) in only_new
    )
    need(dict(only_new_pairs) == ONLY_NEW_PAIRS and dict(only_new_events) == ONLY_NEW_EVENTS, "New-pair phases")
    for phase, (source, destination, recipe) in samples.items():
        stripped = tuple(gate for gate in recipe if gate[0] != "phase")
        full = native.state(recipe)
        free = native.state(stripped)
        need(rotate_state(native, free, phase) == full, "Global phase gate")
        need(rotate_state(native, free, (phase + 1) % 4) != full, "Off-by-one phase")
        need(((2 * phase) % 4 == phase) is (phase == 0), "Width-2 phase witness")
        need(source != destination, "Sample endpoints")
    nontrivial_pairs = sum(count for phase, count in PAIR_PHASE.items() if phase)
    nontrivial_events = sum(count for phase, count in EVENT_PHASE.items() if phase)
    print(
        "PASS_MOVE_CHART_PHASE_POWER"
        f" pairs={len(pair_phase)} events={len(moves)}"
        f" phase0_pairs={PAIR_PHASE[0]} phase0_events={EVENT_PHASE[0]}"
        f" nontrivial_pairs={nontrivial_pairs} nontrivial_events={nontrivial_events}"
        f" only_new_pairs=78 only_new_events=103"
    )


if __name__ == "__main__":
    main()
