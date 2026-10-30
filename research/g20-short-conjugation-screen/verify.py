"""Certify the remaining one-to-three-contact conjugations on the #5708 word.

The census follows the A2 cases in research/g20-conjugation-admission/construct.py
and the paid-query count in its emit path. It does not import that module.
"""

from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path
import gzip
import json

ROOT = Path(__file__).resolve().parents[2]
PRIOR = ROOT / "research" / "g20-conjugation-admission"
SAVING = ((1, 1), (2, -2), (3, 1))
LOSS_A = ((1, 2), (2, -1))
LOSS_B = ((1, 1), (2, 1), (4, 1))
EXPECTED = {
    "candidates": 765,
    "missing_edge": 605,
    "endpoint_failures": 0,
    "other_route_failures": 0,
    "emitted": 160,
    "loss_a": 153,
    "loss_b": 1,
    "neutral": 6,
    "saving": 0,
    "non_a2": 324,
    "k1_missing": 184,
    "k1_emitted": 0,
    "k2_missing": 220,
    "k2_loss_a": 109,
    "k2_neutral": 2,
    "k3_missing": 201,
    "k3_loss_a": 44,
    "k3_loss_b": 1,
    "k3_neutral": 4,
    "routes": 2369,
}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def load_pinned():
    sources = json.loads((Path(__file__).resolve().parent / "SOURCES.json").read_text())
    wanted = {row["path"]: row["sha256"] for row in sources["files"] if row["usage"] == "input"}
    blobs = {}
    for name, expected in wanted.items():
        path = ROOT / name
        actual = digest(path)
        need(actual == expected, "input hash mismatch " + name)
        blobs[name] = path.read_bytes()
    readme = blobs["research/g20-conjugation-admission/README.md"].decode()
    proof = blobs["research/g20-conjugation-admission/PROOF.md"].decode()
    source = blobs["research/g20-conjugation-admission/construct.py"].decode()
    need("priced765 remaining\none-to-three-contact conjugations" in readme,
         "README no longer states the 765-conjugation discovery claim")
    need("local-only evidence, not replayed search" in readme,
         "README no longer marks that discovery as local-only")
    need("2*2^t>1+3^t" in proof, "PROOF no longer states the one-step concavity saving")
    need('extra = ["ADD", a, s, e[3]]' in source, "missing A2 correction ADD(a, s)")
    need('extra = ["ADD", d, b, e[3]]' in source, "missing A2 correction ADD(d, b)")
    word = json.loads(gzip.decompress(blobs["research/g20-conjugation-admission/WORD.json.gz"]))
    paths = json.loads(blobs["research/g20-conjugation-admission/PATHS.json"])
    local = json.loads(blobs["research/g20-conjugation-admission/LOCAL-RESULT.json"])
    return word, paths, local


def load_edges(paths):
    edges = {}
    for key, value in paths.items():
        left, right = key.split(":")
        need(len(value) == 1, "route " + key + " is not one edge")
        start, end, rank = value[0]
        need(start == int(left) and end == int(right), "route endpoints disagree with " + key)
        need(type(rank) is int and 1 <= rank <= 7, "route rank outside 1..7")
        edges[(start, end)] = rank
    need(len(edges) == EXPECTED["routes"], "route count changed")
    return edges


def expected_rows(width, owned):
    rows = []
    for index in range(width):
        if index in owned:
            rows.append(0)
            continue
        row = 1 << index
        if 111 <= index < 222:
            row ^= 1 << (index - 111)
        rows.append(row)
    return rows


def endpoint_ok(records, width, owned, expected):
    rows = [1 << index for index in range(width)]
    for event in records:
        op, dest = event[0], event[1]
        if op == "ADD":
            rows[dest] ^= rows[event[2]]
        elif op == "ERASE":
            if dest not in owned:
                return False
            rows[dest] = 0
        elif op == "INIT":
            if dest not in owned or rows[dest]:
                return False
        else:
            return False
    return rows == expected


def paid_histogram(records, width, owned, start, final, edges, used=None):
    rows = [1 << index for index in range(width)]
    state = start[:]
    paid = Counter()
    for event in records:
        op, dest = event[0], event[1]
        if op in ("ERASE", "INIT"):
            if dest not in owned or (op == "INIT" and rows[dest]):
                return "owned_op", None
            rows[dest] = 0
            state[dest] = event[2]
            continue
        if op != "ADD":
            return "opcode", None
        source, frame = event[2], event[3]
        if not rows[source]:
            continue
        for wire in (dest, source):
            origin = state[wire]
            if origin == frame:
                continue
            rank = edges.get((origin, frame))
            if rank is None:
                return "missing_edge", None
            if used is not None:
                used.add((origin, frame))
            if rows[wire]:
                paid[rank] += 1
            state[wire] = frame
        rows[dest] ^= rows[source]
    for dest, frame in enumerate(final):
        if dest in owned:
            if rows[dest]:
                return "owned_live", None
            state[dest] = frame
            continue
        origin = state[dest]
        if origin == frame:
            continue
        rank = edges.get((origin, frame))
        if rank is None:
            return "missing_edge", None
        if used is not None:
            used.add((origin, frame))
        if rows[dest]:
            paid[rank] += 1
        state[dest] = frame
    if state != final:
        return "final_state", None
    return None, paid


def correction(event, gate_dest, gate_source):
    """A2 correction for an outer ADD(gate_dest, gate_source)."""
    dest, source, frame = event[1], event[2], event[3]
    if dest == gate_source and source != gate_dest:
        return ["ADD", gate_dest, source, frame]
    if source == gate_dest and dest != gate_source:
        return ["ADD", dest, gate_source, frame]
    return None


def rewrite(scalars, left, right, gate_dest, gate_source):
    """Return the corrected skeleton, or a short rejection name."""
    changes = []
    for index in range(left + 1, right):
        event = scalars[index]
        if event[0] in ("ERASE", "INIT") and event[1] in (gate_dest, gate_source):
            return "barrier"
        if event[0] == "ADD" and (event[1] == gate_source or event[2] == gate_dest):
            extra = correction(event, gate_dest, gate_source)
            if extra is None:
                return "non_a2"
            changes.append((index, extra))
            if len(changes) > 3:
                return "too_long"
    if not changes:
        return "commuting"
    replaced = {index: extra for index, extra in changes}
    out = []
    for index, event in enumerate(scalars):
        if index in (left, right):
            continue
        if index in replaced:
            extra = replaced[index]
            frame = event[3]
            out.append(event[:3] + [frame])
            out.append(extra[:3] + [frame])
        else:
            out.append(event)
    return out


def delta_of(paid, base):
    ranks = set(paid) | set(base)
    return tuple(sorted((rank, paid[rank] - base[rank]) for rank in ranks if paid[rank] != base[rank]))


def classify(delta):
    if delta == ():
        return "neutral"
    if delta == LOSS_A:
        return "loss_a"
    if delta == LOSS_B:
        return "loss_b"
    if delta == SAVING:
        return "saving"
    raise ValueError("unclassified paid delta " + str(delta))


def screen(word, edges):
    scalars = [event[:] for event in word["records"] if event[0] not in ("Q", "ZERO_Q")]
    width = len(word["start"])
    owned = set(word["owned"])
    need(len(word["final"]) == width, "start and final widths differ")
    expected = expected_rows(width, owned)
    need(endpoint_ok(scalars, width, owned, expected), "published word misses its scalar endpoint")
    used = set()
    reason, base = paid_histogram(
        scalars, width, owned, word["start"], word["final"], edges, used)
    need(reason is None, "published word does not emit: " + str(reason))
    need(used, "published word uses no route")
    groups = defaultdict(list)
    for index, event in enumerate(scalars):
        if event[0] == "ADD":
            groups[(event[1], event[2])].append(index)
    counts = Counter()
    for (gate_dest, gate_source), positions in groups.items():
        for left_at, left in enumerate(positions):
            for right in positions[left_at + 1:]:
                rewritten = rewrite(scalars, left, right, gate_dest, gate_source)
                if isinstance(rewritten, str):
                    counts[rewritten] += 1
                    continue
                contacts = (len(rewritten) - len(scalars)) + 2
                need(contacts in (1, 2, 3), "contact count outside 1..3")
                if not endpoint_ok(rewritten, width, owned, expected):
                    counts["endpoint_failures"] += 1
                    counts["k" + str(contacts) + "_endpoint"] += 1
                    continue
                route_reason, paid = paid_histogram(
                    rewritten, width, owned, word["start"], word["final"], edges)
                if route_reason is not None:
                    need(route_reason == "missing_edge", "unexpected route failure " + route_reason)
                    counts["missing_edge"] += 1
                    counts["k" + str(contacts) + "_missing"] += 1
                    continue
                kind = classify(delta_of(paid, base))
                counts["emitted"] += 1
                counts[kind] += 1
                counts["k" + str(contacts) + "_" + kind] += 1
    counts["base"] = base
    counts["used_route"] = next(iter(used))
    return counts


def controls(word, edges, counts):
    need(classify(SAVING) == "saving", "the known one-step saving must stay visible")
    need(classify(LOSS_A) == "loss_a" and classify(()) == "neutral", "shape names drifted")
    used = counts["used_route"]
    broken = dict(edges)
    del broken[used]
    reason, _paid = paid_histogram(
        [event[:] for event in word["records"] if event[0] not in ("Q", "ZERO_Q")],
        len(word["start"]), set(word["owned"]), word["start"], word["final"], broken)
    need(reason == "missing_edge", "deleting a live route must block the base word")
    scalars = [event[:] for event in word["records"] if event[0] not in ("Q", "ZERO_Q")]
    mutated = [event[:] for event in scalars]
    mutated[0][2] = mutated[0][2] + 1
    reason, paid = paid_histogram(
        mutated, len(word["start"]), set(word["owned"]), word["start"], word["final"], edges)
    need(reason is not None or paid != counts["base"], "a changed ADD source left the base histogram")


def main():
    word, paths, local = load_pinned()
    published = {int(rank): count for rank, count in local["stats"]["paid"].items()}
    need(local["productive_conjugations"] == 2, "published productive step count changed")
    need(local["local_paid_delta"] == {"1": 2, "2": -4, "3": 2},
         "published local saving is no longer two concavity steps")
    edges = load_edges(paths)
    counts = screen(word, edges)
    need(dict(counts["base"]) == published, "recomputed base histogram disagrees with LOCAL-RESULT")
    observed = {
        "candidates": counts["missing_edge"] + counts["emitted"] + counts["endpoint_failures"],
        "missing_edge": counts["missing_edge"],
        "endpoint_failures": counts["endpoint_failures"],
        "other_route_failures": 0,
        "emitted": counts["emitted"],
        "loss_a": counts["loss_a"],
        "loss_b": counts["loss_b"],
        "neutral": counts["neutral"],
        "saving": counts["saving"],
        "non_a2": counts["non_a2"],
        "k1_missing": counts["k1_missing"],
        "k1_emitted": counts["k1_loss_a"] + counts["k1_loss_b"] + counts["k1_neutral"] + counts["k1_saving"],
        "k2_missing": counts["k2_missing"],
        "k2_loss_a": counts["k2_loss_a"],
        "k2_neutral": counts["k2_neutral"],
        "k3_missing": counts["k3_missing"],
        "k3_loss_a": counts["k3_loss_a"],
        "k3_loss_b": counts["k3_loss_b"],
        "k3_neutral": counts["k3_neutral"],
        "routes": len(edges),
    }
    need(observed == EXPECTED, "census changed: " + str(observed))
    controls(word, edges, counts)
    print(
        "PASS_G20_SHORT_CONJUGATION_SCREEN"
        " candidates=765 missing_edge=605 emitted=160"
        " loss_2h1_minus_h2=153 loss_h1_h2_h4=1 neutral=6"
        " savings=0 k1_emitted=0 endpoint_failures=0"
    )


if __name__ == "__main__":
    main()
