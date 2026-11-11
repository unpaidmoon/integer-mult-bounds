"""Exact longer-contact A2 rewrites on one pinned characteristic-two word.

New longer-contact census produced by Nick Petalas. Apache-2.0.
The source word, row-sensitive emitter and A2 construction are Ali Romman's
PR5708 work, following Dugongue, ai-nanachi and the retained native lineage.
The fixed-contact-frame question is from unpaidmoon's PR6290.
"""

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import product
from pathlib import Path
import argparse
import gzip
import json


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[1]
CERTIFICATE_SHA256 = "577323306b7b7f2547ca660e6bbef1badc953959e2f7cd20de9e1f002e254889"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def scalar_rows(records, width, owned):
    rows = [1 << index for index in range(width)]
    for event in records:
        op, dest = event[:2]
        if op == "ADD":
            rows[dest] ^= rows[event[2]]
        else:
            need(op in ("ERASE", "INIT") and dest in owned, "owned opcode")
            need(op != "INIT" or rows[dest] == 0, "INIT of live row")
            rows[dest] = 0
    return rows


def correction(event, a, b):
    dest, source, frame = event[1:]
    if dest == b and source != a:
        return ("ADD", a, source, frame)
    if source == a and dest != b:
        return ("ADD", dest, b, frame)
    return None


def candidate_changes(records, left, right):
    """Return every correction, or None at a barrier or reversed contact."""
    a, b = records[left][1:3]
    need(records[left][:3] == records[right][:3], "unequal outer gates")
    changes = {}
    for index in range(left + 1, right):
        event = records[index]
        if event[0] in ("INIT", "ERASE") and event[1] in (a, b):
            return None
        if event[0] == "ADD" and (event[1] == b or event[2] == a):
            extra = correction(event, a, b)
            if extra is None:
                return None
            changes[index] = extra
    return changes


def longer_candidates(records):
    groups = defaultdict(list)
    for index, event in enumerate(records):
        if event[0] == "ADD":
            groups[event[1:3]].append(index)
    candidates = []
    for gate, positions in sorted(groups.items()):
        for offset, left in enumerate(positions):
            for right in positions[offset + 1:]:
                changes = candidate_changes(records, left, right)
                if changes is not None and len(changes) >= 4:
                    candidates.append((left, right, gate, changes))
                    need(len(candidates) <= 4096, "candidate capacity")
    return candidates


def rewrite(records, left, right, changes):
    result = []
    for index, event in enumerate(records):
        if index not in (left, right):
            result.append(event)
            if index in changes:
                result.append(changes[index])
    need(len(result) == len(records) - 2 + len(changes), "rewrite size")
    return result


def emit_histogram(records, start, final, owned, edges):
    """Mirror the source's row-sensitive route charges; return first missing edge."""
    rows = [1 << index for index in range(len(start))]
    state = list(start)
    histogram = Counter()
    for event in records:
        op, dest = event[:2]
        if op in ("ERASE", "INIT"):
            need(dest in owned and (op != "INIT" or rows[dest] == 0), "owned action")
            rows[dest], state[dest] = 0, event[2]
            continue
        need(op == "ADD", "scalar opcode")
        source, frame = event[2:]
        if rows[source] == 0:
            continue
        for wire in (dest, source):
            old = state[wire]
            if old == frame:
                continue
            if old is None:
                need(wire in owned and rows[wire] == 0, "uninitialized public row")
            elif (old, frame) not in edges:
                return None, (old, frame)
            elif rows[wire]:
                histogram[edges[old, frame]] += 1
            state[wire] = frame
        rows[dest] ^= rows[source]
    for wire, frame in enumerate(final):
        if wire in owned:
            need(rows[wire] == 0, "live owned return")
        elif state[wire] != frame:
            edge = (state[wire], frame)
            if edge not in edges:
                return None, edge
            if rows[wire]:
                histogram[edges[edge]] += 1
        state[wire] = frame
    need(state == list(final), "final frames")
    return histogram, None


def delta_histogram(histogram, base):
    return tuple((rank, histogram[rank] - base[rank])
                 for rank in sorted(histogram.keys() | base.keys())
                 if histogram[rank] != base[rank])


def census(word, paths):
    records = [tuple(event) for event in word["records"] if event[0] not in ("Q", "ZERO_Q")]
    width, owned = len(word["start"]), set(word["owned"])
    need(width == 685 and len(records) == 11930, "source dimensions")
    edges = {}
    for key, path in paths.items():
        need(len(path) == 1, "one-edge source routes")
        a, b, rank = path[0]
        need(key == f"{a}:{b}" and 1 <= rank <= 7, "source route format")
        edges[a, b] = rank
    expected = [0 if index in owned else (1 << index) ^
                ((1 << (index - 111)) if 111 <= index < 222 else 0)
                for index in range(width)]
    need(scalar_rows(records, width, owned) == expected, "source scalar endpoint")
    base, missing = emit_histogram(records, word["start"], word["final"], owned, edges)
    need(missing is None, "source emission")
    outcomes = []
    for left, right, gate, changes in longer_candidates(records):
        changed = rewrite(records, left, right, changes)
        need(scalar_rows(changed, width, owned) == expected, "changed scalar endpoint")
        histogram, missing = emit_histogram(changed, word["start"], word["final"], owned, edges)
        outcomes.append({"first": left, "last": right, "gate": gate,
                         "contacts": len(changes), "missing_edge": missing,
                         "delta": None if missing else delta_histogram(histogram, base)})
    return {"base_paid": dict(sorted(base.items())), "outcomes": outcomes}


def strict_loss(delta):
    """Exact sufficient sign certificate, justified by strict subadditivity."""
    if not delta:
        return False
    if all(coefficient > 0 for _, coefficient in delta):
        return True
    negative = [(rank, -coefficient) for rank, coefficient in delta if coefficient < 0]
    positive = [(rank, coefficient) for rank, coefficient in delta if coefficient > 0]
    return (len(negative) == 1 and negative[0][1] == 1
            and sum(coefficient for _, coefficient in positive) >= 2
            and sum(rank * coefficient for rank, coefficient in positive) == negative[0][0])


def controls():
    outer = ("ADD", 0, 1, 0)
    contacts = (("ADD", 1, 2, 1), ("ADD", 1, 3, 2),
                ("ADD", 2, 0, 3), ("ADD", 3, 0, 4))
    count = 0
    for middle in product(contacts, repeat=4):
        records = [outer, *middle, outer]
        candidates = longer_candidates(records)
        chosen = [entry for entry in candidates if entry[:2] == (0, 5)]
        need(len(chosen) == 1 and len(chosen[0][3]) == 4, "four-contact inclusion")
        changes = chosen[0][3]
        changed = rewrite(records, 0, 5, changes)
        endpoint = scalar_rows(records, 4, set())
        need(scalar_rows(changed, 4, set()) == endpoint, "A2 identity control")
        need(scalar_rows(changed[:1] + changed[2:], 4, set()) != endpoint,
             "missing correction must change the endpoint")
        count += 1
    reversed_word = [outer, ("ADD", 1, 0, 0), outer]
    erased_word = [outer, ("ERASE", 0, 0), outer]
    need(candidate_changes(reversed_word, 0, 2) is None, "reversed contact rejection")
    need(candidate_changes(erased_word, 0, 2) is None, "erased operand rejection")
    need(not longer_candidates([outer, contacts[0], outer]), "short-domain rejection")
    need(not strict_loss(((1, 1), (2, -2), (3, 1))), "profitable shape must reject")
    small = [("ADD", 0, 1, 2)]
    paid, missing = emit_histogram(small, [0, 0], [2, 2], set(), {(0, 2): 1})
    need(paid == {1: 2} and missing is None, "route charging control")
    paid, missing = emit_histogram(small, [0, 0], [2, 2], set(), {})
    need(paid is None and missing == (0, 2), "missing route control")
    zero = [("ERASE", 0, 3), ("ADD", 1, 0, 2)]
    paid, missing = emit_histogram(zero, [0, 0], [3, 0], {0}, {})
    need(paid == {} and missing is None, "zero source omits the whole ADD")
    return {"a2_words": count, "missing_correction_rejections": count,
            "reversed_rejections": 1, "erasure_rejections": 1,
            "short_domain_rejections": 1, "profitable_shape_rejections": 1,
            "route_charging": 1, "missing_route_rejections": 1, "zero_source": 1}


def load_sources():
    sources = json.loads((PACKAGE / "SOURCES.json").read_text())
    data, hashes = {}, {}
    for entry in sources["files"]:
        if entry["usage"] == "input":
            name = entry["path"]
            path = ROOT / name
            need(path.stat().st_size < 2_000_000, "input byte capacity")
            raw = path.read_bytes()
            hashes[name] = sha256(raw).hexdigest()
            need(hashes[name] == entry["sha256"], "input hash mismatch: " + name)
            data[name] = raw
    prefix = "research/g20-conjugation-admission/"
    word = json.loads(gzip.decompress(data[prefix + "WORD.json.gz"]))
    paths = json.loads(data[prefix + "PATHS.json"])
    return word, paths, hashes


def verify_result(result):
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    need(sha256(encoded).hexdigest() == CERTIFICATE_SHA256, "candidate certificate drift")
    counts, shapes = Counter(), Counter()
    contacts = []
    for outcome in result["outcomes"]:
        contacts.append(outcome["contacts"])
        if outcome["missing_edge"] is not None:
            need(outcome["delta"] is None, "unemitted delta")
            counts["missing_route"] += 1
        else:
            delta = outcome["delta"]
            need(not delta or strict_loss(delta), "unproved or profitable moment change")
            counts["strict_loss" if delta else "neutral"] += 1
            shapes[delta] += 1
    need(len(contacts) == 1503 and min(contacts) == 4 and max(contacts) == 33,
         "longer-contact domain")
    need(counts == {"missing_route": 1450, "strict_loss": 39, "neutral": 14},
         "outcome counts")
    return {"candidates": len(contacts), "minimum_contacts": min(contacts),
            "maximum_contacts": max(contacts), **counts,
            "emitted": counts["strict_loss"] + counts["neutral"],
            "shapes": [{"delta": shape, "count": number}
                       for shape, number in sorted(shapes.items())]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="write a generated receipt outside the checkout")
    args = parser.parse_args()
    if args.output is not None:
        need(not args.output.resolve().is_relative_to(ROOT), "receipt must be outside checkout")
    word, paths, input_hashes = load_sources()
    result = census(word, paths)
    summary = verify_result(result)
    control_counts = controls()
    names = ("README.md", "PROOF.md", "TASK.json", "SOURCES.json", "VERIFY.json", "verify.py")
    receipt = {"schema": "g20-long-conjugation-obstruction/v1", "summary": summary,
               "controls": control_counts, "certificate_sha256": CERTIFICATE_SHA256,
               "input_sha256": input_hashes,
               "package_sha256": {name: sha256((PACKAGE / name).read_bytes()).hexdigest()
                                  for name in names}, "certificate": result}
    if args.output is not None:
        args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"summary": summary, "controls": control_counts}, sort_keys=True))
    print("PASS_G20_LONG_CONJUGATION_OBSTRUCTION candidates=1503 missing_route=1450"
          " emitted=53 neutral=14 strict_loss=39 min_contacts=4 max_contacts=33")


if __name__ == "__main__":
    main()
