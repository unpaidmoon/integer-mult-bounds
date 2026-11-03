#!/usr/bin/env python3
"""Check the selected three-edge scalar-phase obstruction with exact arithmetic."""

from hashlib import sha256
import gzip
import importlib.util
import itertools
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = Path(__file__).resolve().parent
WORD = "research/p104-helper470-twin-rung-removal/WORD.json.gz"
CLIFFORD = "research/p104-native-channel/vendor/clifford_exact.py"
NATIVE = "research/p104-native-channel/vendor/native_verify.py"
INPUT_SHA256 = {
    WORD: "7834725d9e34ee846a9ccc615221ea81e0201613938afa185d2eda0c9a6c232f",
    CLIFFORD: "2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962",
    NATIVE: "3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38",
}
FRAMES = {3: (), 2: (35,), 299: (35, 75, 400)}
EDGES = ((3, 2), (2, 299), (3, 299))
EVENTS = (10338, 10403, 14360)


def need(condition, label):
    if not condition:
        raise ValueError(label)


def authenticate(raw, expected, label):
    need(sha256(raw).hexdigest() == expected, label + " source bytes")


def reject(operation, label):
    try:
        operation()
    except ValueError:
        return
    raise ValueError(label + " was accepted")


def load(relative, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    need(spec is not None and spec.loader is not None, "Module loader")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def sources():
    manifest = json.loads((PACKAGE / "SOURCES.json").read_text())
    pins = {row["path"]: row["sha256"] for row in manifest["files"]
            if row["usage"] == "input"}
    need(pins == INPUT_SHA256, "Declared live source pins")
    payloads = {}
    for relative, expected in INPUT_SHA256.items():
        raw = (ROOT / relative).read_bytes()
        need(len(raw) <= 16 * 1024 * 1024, "Bounded source input")
        authenticate(raw, expected, relative)
        reject(lambda: authenticate(raw + b"\n", expected, relative), "Changed source")
        payloads[relative] = raw
    word = json.loads(gzip.decompress(payloads[WORD]))
    need(word["schema"] == "p104-accumulated-block-composition/2", "Word schema")
    need(len(word["frames"]) <= 4096 and len(word["program"]) <= 100000, "Word bounds")
    for frame, basis in FRAMES.items():
        need(tuple(word["frames"][frame]) == basis, "Named frame basis")
    for index, (a, b) in zip(EVENTS, EDGES):
        event = word["program"][index]
        need(event[0] == "MOVE" and event[2:5] == [a, b, False], "Selected MOVE occurrence")
    return word


def compile_edges(word, clifford, native):
    charts = {frame: clifford.canonical_frame(9, basis) for frame, basis in FRAMES.items()}
    recipes, stripped, phases, ranks = [], [], [], []
    for a, b in EDGES:
        operator = charts[a].adjoint().then(charts[b])
        record, _compiled = clifford.lower_child(operator)
        recipe = native.recipe(record)
        expected = native.adjoint(native.frame(tuple(word["frames"][a]), 9))
        expected += native.frame(tuple(word["frames"][b]), 9)
        # This checker reconstructs signed Pauli action and the absolute phase.
        native.equal(recipe, expected, "Triangle edge")
        phase = sum(gate[1] for gate in recipe if gate[0] == "phase") % 4
        phases.append(phase)
        ranks.append(record["rank"])
        recipes.append(recipe)
        stripped.append(tuple(gate for gate in recipe if gate[0] != "phase"))
    need(phases == [1, 1, 1] and ranks == [1, 2, 3], "Triangle phase and rank")
    return recipes, stripped, phases, ranks


def gauge_solutions(phases, width):
    need(len(phases) == 3 and 1 <= width <= 4, "Finite gauge control domain")
    solutions = []
    # Variables are q(3), q(2), q(299), each in Z/4.
    for q0, q1, q2 in itertools.product(range(4), repeat=3):
        residuals = ((width * phases[0] + q1 - q0) % 4,
                     (width * phases[1] + q2 - q1) % 4,
                     (width * phases[2] + q2 - q0) % 4)
        if residuals == (0, 0, 0):
            solutions.append((q0, q1, q2))
    return solutions


def controls(phases):
    counts = [len(gauge_solutions(phases, width)) for width in range(1, 5)]
    need(counts == [0, 0, 0, 4], "Width residue controls")
    need(len(gauge_solutions([1, 1, 2], 1)) == 4, "Compatible triangle control")
    # On the two-edge tree every root phase determines one solution.
    tree = [(q0, (q0 - 1) % 4, (q0 - 2) % 4) for q0 in range(4)]
    need(len(tree) == 4 and all((b - a + 1) % 4 == (c - b + 1) % 4 == 0
                               for a, b, c in tree), "Tree control")
    return counts


def basis_checks(native, recipes, stripped):
    full_loop = recipes[0] + recipes[1] + native.adjoint(recipes[2])
    bare_loop = stripped[0] + stripped[1] + native.adjoint(stripped[2])
    restored_loop = bare_loop + (("phase", 1),)
    for address in range(512):
        need(native.state(full_loop, address) == ({address: (1, 0)}, 0), "Exact chart loop")
        need(native.state(bare_loop, address) == ({address: (0, -1)}, 0), "Phase-free loop is -i I")
    need(native.state(restored_loop) == ({0: (1, 0)}, 0), "Restored loop control")
    reject(lambda: need(native.state(bare_loop) == ({0: (1, 0)}, 0), "Wrong loop"),
           "Deleting the needed phase")
    reject(lambda: need(native.state(bare_loop) == ({0: (0, 1)}, 0), "Wrong sign"),
           "Reversed holonomy sign")


def main():
    start = time.perf_counter()
    word = sources()
    clifford = load(CLIFFORD, "phase_obstruction_clifford")
    native = load(NATIVE, "phase_obstruction_native")
    recipes, stripped, phases, ranks = compile_edges(word, clifford, native)
    counts = controls(phases)
    basis_checks(native, recipes, stripped)
    files = sorted(path for path in PACKAGE.iterdir() if path.is_file())
    receipt = {
        "claim_type": "scoped proof with exact finite certificate",
        "input_sha256": INPUT_SHA256,
        "package_sha256": {path.name: sha256(path.read_bytes()).hexdigest() for path in files},
        "edges": EDGES, "event_indices_zero_based": EVENTS,
        "ranks": ranks, "edge_phases_mod4": phases,
        "cycle_phase_mod4": (phases[0] + phases[1] - phases[2]) % 4,
        "stripped_loop_scalar": "-i", "basis_states": 512,
        "z4_gauge_solution_counts_at_widths_1_through_4": counts,
        "python": sys.version.split()[0],
        "elapsed_seconds": round(time.perf_counter() - start, 6),
    }
    print(json.dumps(receipt, sort_keys=True))
    print("PASS_MOVE_FRAME_PHASE_OBSTRUCTION edges=3 basis_states=512 cycle_phase=1")


if __name__ == "__main__":
    main()
