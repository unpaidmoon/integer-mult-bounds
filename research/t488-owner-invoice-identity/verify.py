#!/usr/bin/env python3
"""Invoice bridge for the retimed T488 composition.

Independent of research/retimed-t488-composition. The vendored bytes are the
numerics inputs and the recorded admission profile at PR #3653 head
607a09ff441c79b215a8127a81f4cc70021d0d9b. This checker does not import that
package, rerun its moment engines, or regenerate the literal owner rows.
"""

import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUTS = HERE / "inputs"
HEAD = "607a09ff441c79b215a8127a81f4cc70021d0d9b"
SHA256 = {
    "OLD-base.json.gz": "735c540b1fe29d0ceeb4d2f304ec941e5f2bd3bc92bafc8cce2b4f9a67a3b653",
    "NEW-base.json.gz": "6df3356808e29909776be8bc0faf03df983401a267c2d740d1ac2dbcaa278269",
    "OLD-extra.json.gz": "886338fc32da14f3389a82c8120a1bcf9c5e2f0ec3e9b2d377fdae809e1d977f",
    "NEW-extra.json.gz": "65624efec36b35934b750c1741ba2ad4e6df3cff86e44536b0c016ebddb0fb55",
    "OWNER-EXPECTED.json": "924493b6bbeade055af4916ac7bd6d7d7ec0600719f5c39636dc3f16d7ec14ea",
    "OWNER-PROFILE.json": "1e37bb17fa4ca6fd84d62c6f540e09be96724ea3af4ea50e3e27c6ecb796b35c",
    "OWNER-PORTABLE-REPLAY.json": "bfe8ebc9d646751467745d90110b5600b7df5bf039afdeafb7ea19b0d5046dee",
    "OLD-ARITHMETIC.json": "2f0113dab9dedd5941b1fdee737e6b928539cc78034877c0082a812832f45d3e",
    "PUBLISHED-PROFILE.json": "8b21b03d25cb7bb226b91a63f2458e7b2e92df5779d9e99f0b5275c4c9e90afd",
}
PRESERVED = (
    "start_extra",
    "helper_final",
    "removed",
    "warps",
    "center_frames",
    "cut",
    "restore",
    "A",
)
DELTA = {1: -2, 2: -2, 3: 2}
REPLICAS = 488
CALLS = 4392
ROLES = 1791936
LIVE = REPLICAS * 896
RANK_MASS = 31762944
COVERAGE_DEFICIT = 156160


class Reject(Exception):
    pass


def need(ok, message):
    if not ok:
        raise Reject(message)


def load(name):
    raw = (INPUTS / name).read_bytes()
    need(hashlib.sha256(raw).hexdigest() == SHA256[name], "sha256 " + name)
    if name.endswith(".gz"):
        raw = gzip.decompress(raw)
    return json.loads(raw)


def counts(raw):
    out = {}
    need(isinstance(raw, dict) and raw, "profile must be a nonempty object")
    for key, value in raw.items():
        rank = int(key)
        number = int(value)
        need(rank > 0 and number >= 0, "bad rank count")
        need(rank not in out, "duplicate rank")
        out[rank] = number
    return out


def bill(word):
    need(isinstance(word, dict) and "report" in word, "word report missing")
    return counts(word["report"]["local_profile"])


def move(before, after):
    ranks = set(before) | set(after)
    delta = {rank: after.get(rank, 0) - before.get(rank, 0) for rank in ranks}
    return {rank: number for rank, number in delta.items() if number}


def apply_move(old, delta, calls):
    ranks = set(old) | set(delta)
    derived = {rank: old.get(rank, 0) + calls * delta.get(rank, 0) for rank in ranks}
    need(all(number >= 0 for number in derived.values()), "negative derived count")
    return derived


def mass(profile):
    return sum(rank * number for rank, number in profile.items())


def provider_delta(old_word, new_word):
    for field in PRESERVED:
        need(field in old_word and field in new_word, "missing field " + field)
        need(old_word[field] == new_word[field], "field changed: " + field)
    need(old_word["report"]["width_inventory"] == new_word["report"]["width_inventory"],
         "width inventory changed")
    need(old_word["B"] != new_word["B"], "B section identical")
    need(old_word["cleanup"] != new_word["cleanup"], "cleanup section identical")
    before, after = bill(old_word), bill(new_word)
    delta = move(before, after)
    need(mass(delta) == 0, "local rank mass changed")
    return before, after, delta


def bridge():
    owner = load("OWNER-EXPECTED.json")
    replay = load("OWNER-PORTABLE-REPLAY.json")
    arithmetic = load("OLD-ARITHMETIC.json")
    published = counts(load("PUBLISHED-PROFILE.json"))
    literal = counts(load("OWNER-PROFILE.json"))
    expected = counts(owner["profile"])
    replay_profile = counts(replay["primal"]["profile"])
    arithmetic_profile = counts(arithmetic["profile"])
    need(literal == expected == replay_profile == arithmetic_profile, "literal histograms disagree")
    need(hashlib.sha256((INPUTS / "OWNER-PROFILE.json").read_bytes()).hexdigest()
         == owner["literal_files"]["PROFILE.json"], "PROFILE.json digest")
    need(owner["payload_sha256"] == replay["materialized"]["payload_sha256"], "payload sha256")
    need(owner["replicas"] == replay["replicas"] == arithmetic["replicas"] == REPLICAS, "replicas")
    need(owner["calls"] == replay["calls"] == arithmetic["calls"] == CALLS, "calls")
    need(CALLS == 9 * REPLICAS, "nine calls per replica")
    need(owner["rows"] == replay["roles"] == arithmetic["roles"] == ROLES, "roles")
    need(ROLES == CALLS * 408, "408 helper roles per call")
    need(owner["physical"] == replay["physical"] == arithmetic["physical"] == 437757, "physical")
    bills = {}
    deltas = []
    for tag in ("base", "extra"):
        before, after, delta = provider_delta(load("OLD-" + tag + ".json.gz"),
                                               load("NEW-" + tag + ".json.gz"))
        bills[tag] = {"old": before, "new": after, "delta": delta}
        deltas.append(delta)
    need(deltas[0] == deltas[1] == DELTA, "provider delta")
    need(bills["base"]["old"] == bills["extra"]["old"], "old bills differ")
    need(bills["base"]["new"] == bills["extra"]["new"], "new bills differ")
    need(sum(bills["base"]["new"].values()) - sum(bills["base"]["old"].values()) == -2,
         "child-count drop")
    derived = apply_move(literal, DELTA, CALLS)
    need(derived == published, "published profile is not the literal histogram plus the retiming")
    need(mass(derived) == mass(literal) == RANK_MASS == 65088 * REPLICAS, "rank mass")
    idle = {rank: literal[rank] - CALLS * bills["base"]["old"].get(rank, 0) for rank in literal}
    idle_again = {rank: published[rank] - CALLS * bills["base"]["new"].get(rank, 0) for rank in published}
    need(idle == idle_again, "idle histogram depends on which bill is subtracted")
    need({rank for rank, number in idle.items() if number} == {1, 3, 5, 48}, "idle support")
    need(all(number >= 0 for number in idle.values()), "negative idle")
    need(73 * LIVE - RANK_MASS == LIVE - 64 * CALLS == COVERAGE_DEFICIT, "coverage deficit")
    need(literal != published, "retiming did not change the histogram")
    return derived


def controls():
    literal = counts(load("OWNER-PROFILE.json"))
    published = counts(load("PUBLISHED-PROFILE.json"))
    shifted = apply_move(literal, DELTA, CALLS - 1)
    need(shifted != published, "call count is not used")
    bumped = dict(literal)
    bumped[1] += 1
    need(apply_move(bumped, DELTA, CALLS) != published, "literal rank 1 is not used")
    bad = dict(DELTA)
    bad[1] -= 1
    try:
        need(mass(bad) == 0, "rank mass")
    except Reject:
        pass
    else:
        raise Reject("nonzero rank-mass delta was accepted")
    old_word = load("OLD-base.json.gz")
    new_word = load("NEW-base.json.gz")
    new_word = dict(new_word)
    new_word["A"] = []
    try:
        provider_delta(old_word, new_word)
    except Reject:
        pass
    else:
        raise Reject("changed A section was accepted")


def main():
    derived = bridge()
    controls()
    print(
        "PASS_T488_OWNER_INVOICE_IDENTITY"
        " head=" + HEAD
        + " calls=" + str(CALLS)
        + " replicas=" + str(REPLICAS)
        + " delta=-2H1-2H2+2H3"
        + " rank_mass=" + str(RANK_MASS)
        + " coverage_deficit=" + str(COVERAGE_DEFICIT)
        + " published_ranks=" + str(len(derived))
        + " literal_rows_replayed=false"
        + " no_new_kappa=true"
    )


if __name__ == "__main__":
    try:
        main()
    except Reject as exc:
        raise SystemExit("FAIL: " + str(exc)) from None
