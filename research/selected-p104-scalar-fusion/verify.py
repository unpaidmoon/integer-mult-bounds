#!/usr/bin/env python3
"""One exact scalar fusion on the selected P104 word. Apache-2.0."""

import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction
import gzip
import hashlib
import io
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
INPUT = "research/p104-helper470-twin-rung-removal/WORD.json.gz"
SOURCE_SHA256 = "7834725d9e34ee846a9ccc615221ea81e0201613938afa185d2eda0c9a6c232f"
FIRST, LAST = 231, 392
ORIGINAL = ["ADD", 210, 403, "1/4", 3]
FUSED = ["ADD", 210, 403, "1/2", 3]


def need(condition, message):
    if not condition:
        raise ValueError(message)


def bounded_read(path, maximum):
    with path.open("rb") as stream:
        raw = stream.read(maximum + 1)
    need(len(raw) <= maximum, "file exceeds declared bound")
    return raw


def authenticate(raw):
    need(hashlib.sha256(raw).hexdigest() == SOURCE_SHA256, "source hash")
    return raw


def load_word():
    raw = authenticate(bounded_read(ROOT / INPUT, 256 * 1024))
    with gzip.GzipFile(fileobj=io.BytesIO(raw)) as stream:
        payload = stream.read(4 * 1024 * 1024 + 1)
    need(len(payload) <= 4 * 1024 * 1024, "decompressed source bound")
    word = json.loads(payload)
    need(len(word["program"]) == 22803, "source event count")
    return word


def check_region(region):
    need(len(region) == 162, "region length")
    need(region[0] == ORIGINAL and region[-1] == ORIGINAL, "endpoint gates")
    for gate in region[1:-1]:
        need(gate[-1] == 3, "common frame")
        if gate[0] == "ADD":
            need(len(gate) == 5, "ADD arity")
            target, source = gate[1:3]
            need(target != source, "distinct ADD roles")
            need(target != 403 and source != 210, "ADD commutation")
        else:
            need(gate[0] == "SCALE" and len(gate) == 4, "scalar gate grammar")
            need(gate[1] not in (210, 403), "SCALE commutation")
            need(Fraction(gate[2]) != 0, "invertible SCALE")


def rewrite(word):
    region = word["program"][FIRST:LAST + 1]
    check_region(region)
    result = deepcopy(word)
    result["program"][FIRST] = FUSED.copy()
    del result["program"][LAST]
    need(len(result["program"]) == 22802, "new event count")
    return result


def region_roles(region):
    roles = set()
    for gate in region:
        roles.add(gate[1])
        if gate[0] == "ADD":
            roles.add(gate[2])
    need(len(roles) == 133, "complete region role inventory")
    need(all(type(role) is int and 0 <= role < 1024 for role in roles), "role domain")
    return sorted(roles)


def row_operator(region, roles):
    positions = {role: index for index, role in enumerate(roles)}
    matrix = [[Fraction(i == j) for j in range(len(roles))]
              for i in range(len(roles))]
    for gate in region:
        target = positions[gate[1]]
        coefficient = Fraction(gate[-2])
        if gate[0] == "ADD":
            source = positions[gate[2]]
            matrix[target] = [a + coefficient * b
                              for a, b in zip(matrix[target], matrix[source], strict=True)]
        else:
            matrix[target] = [coefficient * a for a in matrix[target]]
    return matrix


def execute(region, initial):
    state = initial.copy()
    for gate in region:
        if gate[0] == "ADD":
            state[gate[1]] += Fraction(gate[3]) * state[gate[2]]
        else:
            state[gate[1]] *= Fraction(gate[2])
    return state


def check_columns(before, after, roles, operator):
    for column, role in enumerate(roles):
        initial = {item: Fraction(item == role) for item in roles}
        old = execute(before, initial)
        new = execute(after, initial)
        need(old == new, "independent scalar basis execution")
        need([new[item] for item in roles] == [row[column] for row in operator],
             "row/column oracle agreement")
    for seed in range(8):
        initial = {role: Fraction(((role + 7) * (seed + 3)) % 31 - 15, seed + 1)
                   for role in roles}
        need(execute(before, initial) == execute(after, initial), "arbitrary dirty fixture")


def check_envelope(before, after):
    need(set(before) == set(after), "word fields")
    for key in before:
        if key != "program":
            need(before[key] == after[key], "unchanged word boundary")
    old, new = before["program"], after["program"]
    need(old[:FIRST] == new[:FIRST], "unchanged prefix")
    need(old[LAST + 1:] == new[LAST:], "unchanged suffix")
    need(old[FIRST + 1:LAST] == new[FIRST + 1:LAST], "unchanged intervening events")
    need([gate for gate in old if gate[0] != "ADD"] ==
         [gate for gate in new if gate[0] != "ADD"], "unchanged nonscalar structure")
    counts = Counter(gate[0] for gate in old)
    counts["ADD"] -= 1
    need(counts == Counter(gate[0] for gate in new), "exact event delta")


def check_controls(before, after, roles):
    rejected = 0
    for gate in (["ADD", 403, 0, "1", 3], ["ADD", 0, 210, "1", 3],
                 ["SCALE", 210, "2", 3], ["SCALE", 403, "2", 3],
                 ["ADD", 0, 1, "1", 4], ["MOVE", 0, 3, 4, False]):
        bad = deepcopy(before)
        bad[1] = gate
        try:
            check_region(bad)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("unsafe intervening gate accepted")
    expected = row_operator(before, roles)
    for coefficient in ("1/4", "3/4", "-1/2", "0"):
        bad = deepcopy(after)
        bad[0][3] = coefficient
        need(row_operator(bad, roles) != expected, "wrong coefficient accepted")
        rejected += 1
    raw = bounded_read(ROOT / INPUT, 256 * 1024)
    try:
        authenticate(bytes([raw[0] ^ 1]) + raw[1:])
    except ValueError:
        rejected += 1
    else:
        raise ValueError("corrupt source accepted")
    need(rejected == 11, "control inventory")
    return rejected


def verify():
    source = load_word()
    result = rewrite(source)
    check_envelope(source, result)
    before = source["program"][FIRST:LAST + 1]
    after = result["program"][FIRST:LAST]
    roles = region_roles(before)
    old_operator = row_operator(before, roles)
    need(old_operator == row_operator(after, roles), "complete rational region operator")
    check_columns(before, after, roles, old_operator)
    controls = check_controls(before, after, roles)
    files = ("README.md", "TASK.json", "SOURCES.json", "VERIFY.json", "verify.py")
    hashes = {name: hashlib.sha256(bounded_read(HERE / name, 1024 * 1024)).hexdigest()
              for name in files}
    receipt = {"status": "PASS_SELECTED_P104_SCALAR_FUSION", "claim_type": "finite certificate and scoped rewrite proof",
               "before_events": 22803, "after_events": 22802, "ADD_saved": 1,
               "commuting_intervening_gates": 160, "exact_operator_entries": 133 ** 2,
               "basis_columns": 133, "dirty_vectors": 8, "rejecting_controls": controls,
               "source_sha256": SOURCE_SHA256, "package_sha256": hashes,
               "word_json_sha256": hashlib.sha256(json.dumps(result, sort_keys=True,
                    separators=(",", ":")).encode()).hexdigest(), "new_kappa": False}
    return receipt, result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit-word", action="store_true", help="print verified full word JSON instead of receipt")
    arguments = parser.parse_args()
    receipt, word = verify()
    print(json.dumps(word if arguments.emit_word else receipt, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
