#!/usr/bin/env python3
"""Independent scalar audit of the four PR6349 helper-input lifts.

This file does not import research/p104-native-input-lifting. It replays the
pinned source word and the pinned lifted word with its own linear and frame
models. Prepared by unpaidmoon with substantial Cursor Grok assistance.
Apache-2.0. The words retain their predecessor authors.
"""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import gzip
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
STATUS = "PASS_P104_INPUT_LIFT_DIRECTION_AUDIT"
SOURCE_WORD = "research/p104-frontier-compression-2/WORD.json.gz"
LIFT_WORD = "research/p104-native-input-lifting/WORD.json.gz"

# Claimed in PR #6349 PROOF.md and discussion #1166 comment 19341394.
# h is the input direction. a is the departure response.
LIFTS = (
    (496, 595, {496: 1, 639: -1, 643: Fraction(-1, 2)},
     {496: 1, 639: -1, 643: Fraction(-1, 2)}),
    (649, 597, {649: 1, 648: -1},
     {649: 1, 648: -1, 198: 1}),
    (663, 105, {663: 1, 665: -1},
     {663: 1, 665: -1, 179: Fraction(1, 2)}),
    (508, 1093, {508: 1, 631: -1, 635: Fraction(-1, 2)},
     {508: 1, 631: -1, 635: Fraction(-1, 2)}),
)
CARRIERS = (
    (639, 643, 496, Fraction(-2), Fraction(-1, 2), Fraction(2), 595, 1027),
    (631, 635, 508, Fraction(-2), Fraction(-1, 2), Fraction(2), 1093, 118),
)
TARGET_DEBIT = {6: 1, 8: 3, 9: -4}


def fail(message):
    raise SystemExit("FAIL: " + message)


def need(ok, message):
    if not ok:
        fail(message)


def load_json(path):
    raw = Path(path).read_bytes()
    payload = gzip.decompress(raw) if str(path).endswith(".gz") else raw
    return raw, json.loads(payload)


def pins():
    manifest = json.loads((HERE / "SOURCES.json").read_text(encoding="utf-8"))
    return {row["path"]: row for row in manifest["files"] if row["usage"] == "input"}


def span(basis):
    """GF(2) span of integer bit masks. The zero vector is included."""
    found = {0}
    for vector in basis:
        found |= {item ^ vector for item in found}
    return found


def dimension(basis):
    size = len(span(basis))
    need(size and (size & (size - 1)) == 0, "frame span is not a vector space")
    return size.bit_length() - 1


def authenticate(path, raw):
    row = pins()[path]
    need(sha256(raw).hexdigest() == row["sha256"], "SHA-256 pin: " + path)


def endpoints(program, width, public):
    """Linear image of every register, with one symbol per public input."""
    value = [{} for _ in range(width)]
    for role in range(public):
        value[role][role] = Fraction(1)
    for event in program:
        op = event[0]
        if op == "ADD":
            dst, src, coeff = event[1], event[2], Fraction(event[3])
            incoming = value[src]
            if not incoming:
                continue
            row = value[dst]
            for key, weight in incoming.items():
                updated = row.get(key, 0) + coeff * weight
                if updated:
                    row[key] = updated
                elif key in row:
                    del row[key]
        elif op == "SCALE":
            role, coeff = event[1], Fraction(event[2])
            value[role] = {key: coeff * weight for key, weight in value[role].items()
                           if coeff * weight}
        elif op == "COPY":
            dst, src, coeff = event[1], event[2], Fraction(event[3])
            value[dst] = {key: coeff * weight for key, weight in value[src].items()
                          if coeff * weight}
        elif op in ("INIT", "CLEAR"):
            value[event[1]] = {}
        elif op != "MOVE":
            fail("unknown opcode " + op)
    return value


def schedule_ok(word):
    """Public inputs start at their declared frames. Owned lifetimes start at INIT and end at CLEAR."""
    width = word["public"] + word["owned_fields"]
    frame = [None] * width
    for role, start in enumerate(word["initial"]):
        frame[role] = start
    for index, event in enumerate(word["program"]):
        op = event[0]
        if op == "INIT":
            role, here = event[1], event[2]
            if frame[role] is not None:
                return "INIT while occupied at event " + str(index)
            frame[role] = here
        elif op == "CLEAR":
            role, here = event[1], event[2]
            if frame[role] != here:
                return "CLEAR off-frame at event " + str(index)
            frame[role] = None
        elif op == "MOVE":
            role, src, dst = event[1], event[2], event[3]
            if frame[role] != src:
                return "MOVE off-frame at event " + str(index)
            frame[role] = dst
        elif op in ("ADD", "COPY"):
            if frame[event[1]] != event[4] or frame[event[2]] != event[4]:
                return "operand off-frame at event " + str(index)
        elif op == "SCALE":
            if frame[event[1]] != event[3]:
                return "SCALE off-frame at event " + str(index)
        else:
            return "unknown opcode at event " + str(index)
    mismatches = [role for role in range(word["public"]) if frame[role] != word["final"][role]]
    if mismatches:
        return "public final frames differ: " + str(len(mismatches))
    occupied = [role for role in range(word["public"], width) if frame[role] is not None]
    if occupied:
        return "owned lifetime left open"
    return None


def departures(source, direction):
    width = source["public"] + source["owned_fields"]
    value = [Fraction(0)] * width
    for role, coeff in direction.items():
        value[role] = Fraction(coeff)
    first = {}
    departed = {}
    for event in source["program"]:
        op = event[0]
        if op == "MOVE" and event[2] == 3 and event[4] is False:
            role = event[1]
            need(role not in first, "two departures from frame 3 for role " + str(role))
            first[role] = event[3]
            if value[role]:
                departed[role] = value[role]
        elif op in ("INIT", "CLEAR"):
            value[event[1]] = Fraction(0)
        elif op == "SCALE":
            value[event[1]] *= Fraction(event[2])
        elif op == "COPY":
            value[event[1]] = Fraction(event[3]) * value[event[2]]
        elif op == "ADD":
            value[event[1]] += Fraction(event[3]) * value[event[2]]
        elif op != "MOVE":
            fail("unknown opcode in source preparation")
    return departed, first


def carrier_images(subtract):
    """Track (v, z, x) through one dirty-carrier block. x is the lifted input."""
    v = (Fraction(1), Fraction(0), Fraction(0))
    z = (Fraction(0), Fraction(1), Fraction(0))
    x = (Fraction(0), Fraction(0), Fraction(1))

    def mix(left, right, coeff):
        return tuple(left[i] + coeff * right[i] for i in range(3))

    primary_carrier = mix(v, z, Fraction(-2)) if subtract else v
    delayed = mix(z, x, Fraction(-1, 2))
    primary_carrier = mix(primary_carrier, delayed, 2)
    return primary_carrier, delayed


def without(program, event):
    indexes = [index for index, item in enumerate(program) if item == event]
    need(len(indexes) == 1, "control event is not unique: " + str(event))
    index = indexes[0]
    return program[:index] + program[index + 1:]


def forms_differ(left, right):
    return any(left[role] != right[role] for role in range(len(left)))


def target_debit(source, lifted):
    changed = [role for role, (before, after) in enumerate(zip(source["initial"], lifted["initial"]))
               if before != after or source["final"][role] != lifted["final"][role]]
    need(changed == [496, 508, 649, 663], "exactly the four lifted inputs change frame")
    before, after = Counter(), Counter()
    for role in changed:
        before[dimension(source["frames"][source["final"][role]])
               - dimension(source["frames"][source["initial"][role]])] += 1
        after[dimension(lifted["frames"][lifted["final"][role]])
              - dimension(lifted["frames"][lifted["initial"][role]])] += 1
    delta = Counter(after)
    delta.subtract(before)
    return {rank: count for rank, count in delta.items() if count}


def main():
    source_raw, source = load_json(ROOT / SOURCE_WORD)
    lift_raw, lifted = load_json(ROOT / LIFT_WORD)
    authenticate(SOURCE_WORD, source_raw)
    authenticate(LIFT_WORD, lift_raw)
    need(source["public"] == lifted["public"] == 770, "public input count")
    need(source["owned_fields"] == lifted["owned_fields"] == 29, "owned field count")
    need(len(source["program"]) == 17445 and len(lifted["program"]) == 17452, "event counts")
    need(len(source["frames"]) == 1093 and len(lifted["frames"]) == 1094, "frame counts")
    width = 799

    intersection = span(lifted["frames"][118]) & span(lifted["frames"][733])
    need(span(lifted["frames"][1093]) == intersection, "frame 1093 is not the 118/733 intersection")
    need(dimension(lifted["frames"][1093]) == 3, "frame 1093 dimension")
    for _primary, frame, _direction, _response in LIFTS:
        if frame != 1093:
            need(dimension(lifted["frames"][frame]) == 1, "one-dimensional entry frame " + str(frame))

    seen = set()
    for primary, frame, direction, response in LIFTS:
        need(lifted["initial"][primary] == frame and lifted["final"][primary] == 127,
             "lifted entry of " + str(primary))
        need(source["initial"][primary] == 3 and source["final"][primary] == 127,
             "source helper " + str(primary))
        need(direction[primary] == response[primary] == 1, "unit primary coefficient")
        overlap = seen.intersection(direction)
        need(not overlap, "input directions overlap")
        seen.update(direction)
        departed, first = departures(source, direction)
        need(departed == {role: Fraction(coeff) for role, coeff in response.items()},
             "departure response of " + str(primary))
        common = span(lifted["frames"][frame])
        for role in response:
            need(role in first, "response role never leaves frame 3: " + str(role))
            need(common <= span(source["frames"][first[role]]),
                 "entry frame is not inside a departure frame for role " + str(role))

    expected_restore = []
    for primary, _frame, direction, _response in LIFTS:
        for role, coeff in direction.items():
            if role == primary:
                continue
            expected_restore.append(["ADD", role, primary, str(-Fraction(coeff)), 127])
    # The published word emits one fixed order, matching PROOF.md.
    published_restore = [
        ["ADD", 639, 496, "1", 127],
        ["ADD", 643, 496, "1/2", 127],
        ["ADD", 648, 649, "1", 127],
        ["ADD", 665, 663, "1", 127],
        ["ADD", 631, 508, "1", 127],
        ["ADD", 635, 508, "1/2", 127],
    ]
    need(lifted["program"][-6:] == published_restore, "final six events are the inverse basis")
    need(sorted(published_restore) == sorted(expected_restore),
         "inverse basis is not B^{-1} for the four directions")
    for event in published_restore:
        need(lifted["program"].count(event) == 1, "inverse addition is not unique")

    for carrier, delayed, primary, first, injection, repair, mid, dest in CARRIERS:
        subtraction = ["ADD", carrier, delayed, str(first), 3]
        compensation = ["ADD", carrier, delayed, str(repair), dest]
        inject = ["ADD", delayed, primary, str(injection), mid]
        for event in (subtraction, compensation, inject):
            need(lifted["program"].count(event) == 1, "carrier event is not unique: " + str(event))
        order = [lifted["program"].index(event) for event in (subtraction, inject, compensation)]
        need(order == sorted(order), "carrier corrections are out of order for " + str(primary))
        cleaned, delayed_image = carrier_images(True)
        need(cleaned == (1, 0, -1) and delayed_image == (0, 1, Fraction(-1, 2)),
             "dirty carrier does not leave v-x and z-x/2")
        dirty, _delayed_image = carrier_images(False)
        need(dirty != (1, 0, -1), "omitting the carrier subtraction still cancels z")
        restored_carrier = tuple(cleaned[i] + (0, 0, 1)[i] for i in range(3))
        restored_delayed = tuple(
            delayed_image[i] + Fraction(1, 2) * (0, 0, 1)[i] for i in range(3))
        need(restored_carrier == (1, 0, 0) and restored_delayed == (0, 1, 0),
             "output basis does not restore the dirty carrier")

    need(schedule_ok(source) is None, "source schedule: " + str(schedule_ok(source)))
    need(schedule_ok(lifted) is None, "lifted schedule: " + str(schedule_ok(lifted)))
    source_forms = endpoints(source["program"], width, source["public"])
    lifted_forms = endpoints(lifted["program"], width, lifted["public"])
    need(not forms_differ(source_forms, lifted_forms),
         "scalar endpoints differ on some public input")

    damaged = without(lifted["program"], ["ADD", 639, 643, "-2", 3])
    need(forms_differ(source_forms, endpoints(damaged, width, lifted["public"])),
         "deleting the 639 carrier subtraction was accepted")
    damaged = without(lifted["program"], ["ADD", 631, 635, "-2", 3])
    need(forms_differ(source_forms, endpoints(damaged, width, lifted["public"])),
         "deleting the 631 carrier subtraction was accepted")
    damaged = [list(event) for event in lifted["program"]]
    damaged[-5] = ["ADD", 643, 496, "1", 127]
    need(forms_differ(source_forms, endpoints(damaged, width, lifted["public"])),
         "a wrong inverse coefficient was accepted")

    need(target_debit(source, lifted) == TARGET_DEBIT, "productive target debit")
    print(STATUS)
    print("endpoint_registers=799 public_inputs=770 mismatches=0")
    print("target_debit=" + json.dumps(TARGET_DEBIT, sort_keys=True))
    print("carrier_cancellation=v-x,z-x/2 restored_by_output_basis=true")
    print("native_caller_price_compiler_outer=not_run")


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    main()
