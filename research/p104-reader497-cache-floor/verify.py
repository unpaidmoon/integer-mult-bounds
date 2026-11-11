"""Exact reader-497 retention floor. Standard library, Apache-2.0.

Jerry Chen (@CubeJerry), with substantial OpenAI Codex assistance.
Source word/reader-451 retention: Ali Romman / PR6167; root descent:
DreamingOfClouds / PR6144. See README.md. No predecessor code is executed.
"""
import argparse
from collections import Counter, deque
from copy import deepcopy
from fractions import Fraction
import gzip
from hashlib import sha1, sha256
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
WORD = "research/p104-retained-operand-descent/WORD.json.gz"
BASE_RANKS = [1, 1, 3, 3, 5]
STATUS = "PASS_P104_READER497_CACHE_FLOOR"
ANCHORS = {
    12888: ["MOVE", 497, 3, 519, False],
    12933: ["ADD", 497, 48, "1", 519],
    12934: ["MOVE", 497, 519, 520, False],
    12935: ["ADD", 497, 228, "1", 520],
    13485: ["MOVE", 772, 529, 520, True],
    13486: ["ADD", 497, 772, "-4", 520],
    13487: ["MOVE", 772, 520, 595, True],
    15462: ["MOVE", 497, 520, 914, False],
    15572: ["ADD", 161, 497, "-1/2", 914],
}


def need(condition, reason):
    if not condition:
        raise ValueError(reason)


def canonical(value):
    return (json.dumps(value, sort_keys=True, indent=2) + "\n").encode()


def authenticate():
    sources = json.loads((HERE / "SOURCES.json").read_bytes())
    hashes = {}
    for pin in sources["files"]:
        if pin["usage"] != "input":
            continue
        raw = (ROOT / pin["path"]).read_bytes()
        digest = sha256(raw).hexdigest()
        need(digest == pin["sha256"], "input SHA256: " + pin["path"])
        need(sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
             == pin["git_blob"], "input Git blob: " + pin["path"])
        hashes[pin["path"]] = digest
    return json.loads(gzip.decompress((ROOT / WORD).read_bytes())), hashes


def elements(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def extend(space, vector):
    return space | sum(1 << (x ^ vector) for x in elements(space))


def span(basis):
    space = 1  # bit zero represents the zero vector
    for vector in basis:
        need(type(vector) is int and 0 < vector < 512, "binary vector")
        need(not (space >> vector) & 1, "independent basis")
        space = extend(space, vector)
    return space


def inside(left, right):
    return left & right == left


def dimension(space):
    size = space.bit_count()
    need(size > 0 and size & (size - 1) == 0, "subspace cardinality")
    return size.bit_length() - 1


def basis(space):
    result, generated = [], 1
    for vector in elements(space):
        if not (generated >> vector) & 1:
            result.append(vector)
            generated = extend(generated, vector)
    need(generated == space, "representative basis reconstruction")
    return result


def source_contract(word):
    need(word["public"] == 770 and word["owned_fields"] == 29, "source role inventory")
    need(len(word["program"]) == 22821, "source event count")
    for index, expected in ANCHORS.items():
        need(word["program"][index] == expected, "source anchor " + str(index))
    touches = []
    for i in range(12888, 15573):
        e = word["program"][i]
        if e[1] == 497 or (e[0] in ("ADD", "COPY") and e[2] == 497):
            touches.append(i)
    need(touches == [12888, 12933, 12934, 12935, 13486, 15462, 15572],
         "complete receiver interval")
    frames = {str(i): span(word["frames"][i]) for i in (3, 519, 520, 529, 595, 737, 914)}
    zero, s, u, h, line, end = [frames[str(i)] for i in (3, 519, 520, 529, 595, 914)]
    need([dimension(x) for x in (zero, s, u, h, line, end)] == [0, 3, 6, 7, 1, 7],
         "source frame dimensions")
    need(inside(s, u) and inside(line, u) and h & end == u and s & line == zero,
         "source frame intersections")
    need(inside(line, frames["737"]), "reader451 contrasting containment")
    actual_ranks = sorted(abs(dimension(frames[str(e[2])]) - dimension(frames[str(e[3])]))
                          for e in ANCHORS.values() if e[0] == "MOVE")
    need(actual_ranks == BASE_RANKS, "baseline paid ranks from source events")
    return frames


def rank_recipe(a, b, f):
    need(type(a) is int and type(b) is int and type(f) is int, "integer dimensions")
    need(0 <= a <= 3 and 0 <= b <= 6 and 1 <= f <= 6 and a < f, "dimension domain")
    cuts = sorted([0, a, b, f, 7])
    receiver = [y - x for x, y in zip(cuts, cuts[1:]) if y != x]
    caches = [x for x in (3 - a, 6 - b) if x]
    root = [x for x in (7 - f, f - 1) if x]
    return sorted(receiver + caches + root)


def truncated_sums(ranks):
    return [sum(min(r, k) for r in ranks) for k in range(1, 7)]


def proof_row(a, b, f):
    ranks = rank_recipe(a, b, f)
    gaps = [x - y for x, y in zip(truncated_sums(ranks), truncated_sums(BASE_RANKS))]
    need(all(x >= 0 for x in gaps), "concave tariff domination")
    need(any(gaps) or (a, b, f) == (3, 6, 6), "unique equality dimensions")
    if f < 6:
        need(gaps[3] >= 1, "strict rank-four gap for deleted stop")
    need(sum(ranks) == 22 - a - b, "complete transported rank mass")
    return {"dimensions": [a, b, f], "ranks": ranks, "truncated_gaps": gaps}


def all_subspaces(universe):
    """Closure enumeration in literal source vectors, not a dimension formula."""
    points = tuple(elements(universe))
    seen, queue = {1}, deque([1])
    while queue:
        old = queue.popleft()
        for vector in points:
            if old >> vector & 1:
                continue
            new = extend(old, vector)
            if new not in seen:
                seen.add(new)
                queue.append(new)
    return sorted(seen, key=lambda s: (dimension(s), s))


def geometry(frames):
    s, u, line = (frames[k] for k in ("519", "520", "595"))
    spaces = all_subspaces(u)
    need(Counter(map(dimension, spaces)) == {0: 1, 1: 63, 2: 651, 3: 1395,
                                           4: 651, 5: 63, 6: 1},
         "complete binary six-space census")
    a_spaces = [x for x in spaces if inside(x, s)]
    f_spaces = [x for x in spaces if inside(line, x)]
    need((len(a_spaces), len(f_spaces)) == (16, 374), "source subspace intervals")
    counts, representatives = Counter(), {}
    for a_space in a_spaces:
        for f_space in f_spaces:
            if not inside(a_space, f_space):
                continue
            for b_space in spaces:
                if not ((inside(b_space, a_space)) or
                        (inside(a_space, b_space) and inside(b_space, f_space)) or
                        (inside(f_space, b_space))):
                    continue
                triple = tuple(map(dimension, (a_space, b_space, f_space)))
                counts[triple] += 1
                representatives.setdefault(triple, (a_space, b_space, f_space))
    expected = {(a, b, f) for a, b, f in product(range(4), range(7), range(1, 7)) if a < f}
    need(set(counts) == expected and len(expected) == 126, "all geometric dimension recipes")
    return counts, representatives


def emit(frames, meeting):
    """Local normalized-chart template, not a full physical supplier word.

    Dirty receiver A, preserved V/B, preloaded owned Q, and two owned caches.
    Captures precede root arrival; arbitrary retention is granted.
    """
    a_space, b_space, f_space = meeting
    s, u, h, line, end = (frames[k] for k in ("519", "520", "529", "595", "914"))
    events = [("INIT", 4, s), ("COPY", 4, 1, s), ("INIT", 5, u), ("COPY", 5, 2, u)]

    def move(role, old, new, owned):
        if old != new:
            events.append(("MOVE", role, old, new, owned))

    move(4, s, a_space, True)
    move(5, u, b_space, True)
    move(3, h, f_space, True)
    current = 1
    for at, donor, coefficient in sorted([(a_space, 4, 1), (b_space, 5, 1), (f_space, 3, -4)],
                                         key=lambda x: (dimension(x[0]), x[1])):
        move(0, current, at, False)
        events.append(("ADD", 0, donor, coefficient, at))
        current = at
    move(0, current, end, False)
    move(3, f_space, line, True)
    events.extend([("CLEAR", 4, a_space), ("CLEAR", 5, b_space)])
    return events


def execute(frames, events):
    """Independent event ledger and all-input rational linear interpretation."""
    zero_row = (Fraction(0),) * 4
    rows = {r: tuple(Fraction(int(j == r)) for j in range(4)) for r in range(4)}
    chart = {0: 1, 1: frames["519"], 2: frames["520"], 3: frames["529"]}
    owned, ranks, operations = {3}, [], Counter()
    for event in events:
        op, role = event[:2]
        operations[op] += 1
        if op == "INIT":
            need(role in (4, 5) and role not in chart, "clean cache allocation")
            chart[role], rows[role] = event[2], zero_row
            owned.add(role)
        elif op == "MOVE":
            _, _, old, new, private = event
            need(chart.get(role) == old, "move source chart")
            need(type(private) is bool and private == (role in owned), "move ownership")
            need(old != new and (inside(new, old) if private else inside(old, new)), "monotone move")
            ranks.append(abs(dimension(old) - dimension(new)))
            chart[role] = new
        elif op == "COPY":
            donor, at = event[2:]
            need(role in owned and rows[role] == zero_row, "copy into clean owned cache")
            need(chart[role] == chart[donor] == at, "copy common chart")
            rows[role] = rows[donor]
        elif op == "ADD":
            donor, coefficient, at = event[2:]
            need(chart[role] == chart[donor] == at, "addition common chart")
            rows[role] = tuple(x + coefficient * y for x, y in zip(rows[role], rows[donor]))
        elif op == "CLEAR":
            need(role in (4, 5) and role in owned and chart[role] == event[2], "cache erasure")
            rows[role] = zero_row
            del chart[role]
            owned.remove(role)
        else:
            raise ValueError("unknown local opcode")
    need(rows[0] == (1, 1, 1, -4), "arbitrary-input receiver endpoint")
    need(all(rows[r] == tuple(int(j == r) for j in range(4)) for r in (1, 2, 3)), "preserved source values")
    need(chart == {0: frames["914"], 1: frames["519"], 2: frames["520"], 3: frames["595"]},
         "complete exit charts and cache cleanup")
    need(owned == {3}, "no leaked cache lifetime")
    return sorted(ranks), dict(sorted(operations.items()))


def reject(action, reason):
    try:
        action()
    except ValueError as error:
        need(str(error) == reason, "control rejected for wrong reason: " + str(error))
        return reason
    raise ValueError("negative control accepted: " + reason)


def controls(word, frames, representatives):
    results = {}
    original = emit(frames, representatives[(0, 0, 1)])
    bad = deepcopy(original)
    i = next(i for i, e in enumerate(bad) if e[:3] == ("ADD", 0, 3))
    bad[i] = (*bad[i][:3], 4, bad[i][-1])
    results["root_sign"] = reject(lambda: execute(frames, bad), "arbitrary-input receiver endpoint")
    for cache, label in ((4, "missing_V_capture"), (5, "missing_B_capture")):
        changed = [e for e in original if not (e[0] == "COPY" and e[1] == cache)]
        results[label] = reject(lambda: execute(frames, changed), "arbitrary-input receiver endpoint")
    changed = [e for e in original if not (e[0] == "CLEAR" and e[1] == 4)]
    results["uncleared_cache"] = reject(lambda: execute(frames, changed), "complete exit charts and cache cleanup")
    changed = [e for e in original if not (e[0] == "MOVE" and e[1] == 4)]
    results["unmoved_cache"] = reject(lambda: execute(frames, changed), "addition common chart")
    changed = deepcopy(original)
    i = next(i for i, e in enumerate(changed) if e[0] == "MOVE" and e[1] == 4)
    changed[i] = (*changed[i][:4], False)
    results["wrong_cache_ownership"] = reject(lambda: execute(frames, changed), "move ownership")
    changed = deepcopy(original)
    changed[i] = (*changed[i][:3], frames["914"], True)
    results["ascending_owned_cache"] = reject(lambda: execute(frames, changed), "monotone move")
    mutant = deepcopy(word)
    mutant["program"][12933][3] = "-1"
    results["changed_source_read"] = reject(lambda: source_contract(mutant), "source anchor 12933")
    results["source_frame_cap"] = reject(lambda: rank_recipe(4, 6, 6), "dimension domain")
    paid, _ = execute(frames, original)
    free = list(paid)
    free.remove(3)
    free.remove(6)
    results["free_cache_transport"] = reject(
        lambda: need(all(x >= y for x, y in zip(truncated_sums(free), truncated_sums(BASE_RANKS))),
                     "concave tariff domination"), "concave tariff domination")
    results["read_V_after_root_at_595"] = reject(
        lambda: need(inside(frames["595"], frames["519"]), "historical V cannot follow root"),
        "historical V cannot follow root")
    results["convex_tariff_is_outside_theorem"] = reject(
        lambda: need(sum(r * r for r in rank_recipe(3, 6, 4)) >= sum(r * r for r in BASE_RANKS),
                     "concavity is necessary"), "concavity is necessary")
    mutant = deepcopy(word)
    mutant["frames"][519] = basis(frames["595"]) + basis(frames["519"])[:2]
    results["changed_source_incidence"] = reject(lambda: source_contract(mutant), "source frame intersections")
    return results


def contained_line_example(frames):
    """Changed-hypothesis positive control, explicitly NOT the source geometry."""
    altered = dict(frames)
    altered["519"] = span(basis(frames["595"]) + basis(frames["519"])[:2])
    need(dimension(altered["519"]) == 3 and inside(altered["595"], altered["519"]),
         "contrasting incidence")
    events = emit(altered, (altered["519"], altered["520"], altered["595"]))
    ranks, operations = execute(altered, events)
    need(ranks == [1, 1, 2, 3, 6], "contrasting paid bill")
    gaps = [x - y for x, y in zip(truncated_sums(ranks), truncated_sums(BASE_RANKS))]
    need(all(g <= 0 for g in gaps) and gaps[2] < 0, "contrasting concave improvement")
    return {"scope": "changed source frame, not a PR6167 implementation",
            "replacement_source_basis": basis(altered["519"]), "ranks": ranks,
            "operations": operations, "truncated_gaps": gaps,
            "strict_power_gain": "3^t+5^t-2^t-6^t > 0 for 0<t<1"}


def general_small_domain():
    """Finite corroboration of PROOF section 4; not its universal proof."""
    rows, comparisons = 0, 0
    for u in range(2, 11):
        for s in range(1, u):
            baseline = [s, u - s, 1, 1, u - 1]
            for f in range(1, u + 1):
                for a in range(min(s, f - 1) + 1):
                    at_u = [a, f - a, u - f, 1, s - a, u + 1 - f, f - 1]
                    for b in range(u + 1):
                        cuts = sorted([0, a, b, f, u + 1])
                        paid = [y - x for x, y in zip(cuts, cuts[1:])]
                        paid.extend([s - a, u - b, u + 1 - f, f - 1])
                        for cap in range(1, u + 1):
                            new, normalized, old = [sum(min(r, cap) for r in rs)
                                                    for rs in (paid, at_u, baseline)]
                            need(new >= normalized >= old, "general delivery-normalization inequalities")
                            comparisons += 2
                        rows += 1
    return {"u_range": [2, 10], "recipes": rows, "integer_inequalities": comparisons,
            "scope": "finite corroboration only; all-u result uses written subadditivity/concavity proof"}


def run():
    word, hashes = authenticate()
    frames = source_contract(word)
    counts, representatives = geometry(frames)
    certificate, total_events = [], 0
    for triple in sorted(counts):
        row = proof_row(*triple)
        events = emit(frames, representatives[triple])
        ranks, operations = execute(frames, events)
        need(ranks == row["ranks"], "emitted moves equal independently priced recipe")
        need(operations["INIT"] == operations["COPY"] == operations["CLEAR"] == 2,
             "charge two full cache lifetimes")
        row.update(geometric_realizations=counts[triple], representative_bases=[
            basis(s) for s in representatives[triple]], operations=operations)
        certificate.append(row)
        total_events += len(events)
    equality = [r["dimensions"] for r in certificate if not any(r["truncated_gaps"])]
    need(equality == [[3, 6, 6]], "unique equality recipe")
    return {
        "status": STATUS, "source_hashes": hashes,
        "scope": "Monotone reader/root paths, two direct retained operands, fixed sources and consumer; no source mixing or target changes.",
        "source_anchors": {str(k): v for k, v in ANCHORS.items()},
        "frame_dimensions": {k: dimension(v) for k, v in frames.items()},
        "baseline_ranks": BASE_RANKS, "baseline_truncated_sums": truncated_sums(BASE_RANKS),
        "dimension_recipes": len(certificate), "geometric_realizations": sum(counts.values()),
        "symbolic_template_events": total_events, "equality_recipes": equality,
        "min_gaps_by_root_dimension": {
            str(f): [min(r["truncated_gaps"][j] for r in certificate if r["dimensions"][2] == f)
                     for j in range(6)] for f in range(1, 7)},
        "strict_deleted_stop_lower_bound": "2*4^t-3^t-5^t for 0<t<1",
        "general_small_domain": general_small_domain(),
        "contained_line_positive_control": contained_line_example(frames),
        "controls": controls(word, frames, representatives), "certificate": certificate,
        "limitations": ["Not a universal reader497 obstruction.",
                        "Local normalized-chart templates are not full native/caller implementations.",
                        "Free ordinary setup/storage/erasure is an optimistic relaxation; cache MOVEs are charged.",
                        "No full selected replay, compiler/outer/precision proof, human or kernel review.",
                        "No new kappa; all five selected framework assumptions remain."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write a fresh receipt outside the package instead of comparing it")
    args = parser.parse_args()
    result = run()
    encoded = canonical(result)
    if args.output:
        need(not args.output.resolve().is_relative_to(HERE), "output must be outside frozen package")
        args.output.write_bytes(encoded)
    else:
        need(encoded == (HERE / "CERTIFICATE.json").read_bytes(), "complete certificate bytes")
    print(f"{STATUS} recipes={result['dimension_recipes']} geometric={result['geometric_realizations']} "
          f"controls={len(result['controls'])} no_new_kappa")


if __name__ == "__main__":
    main()
