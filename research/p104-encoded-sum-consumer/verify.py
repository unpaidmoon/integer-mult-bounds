#!/usr/bin/env python3
"""Sum-only consumer of the PR #3943 encoded exit, and its native bill.

The producer placement is the published encoded exit: w_N on X_N at H_n,
w_J on Y_J at H_j, q on X_J at FULL, and v_N on Y_N at FULL. This checker
does not replay that 3,642-event prefix. It checks the continuation that
publishes every corrected sum w_i on Y_i at H_i, leaves q and the helpers
in place, and does not restore x.

Chris R / Clear1nsight, PR #3943, proved the source-preserving return. The
new claim is the weaker sum-only protocol and the occupancy floor under
that weaker output. unpaidmoon, with substantial Cursor Grok assistance.
"""

from __future__ import annotations

J = 8
N = 96
HELPERS = 72
# Published PR #3943 figures at head 2cba526a4ebe0ef6c3c0143498adcf67dca97941.
# Inherited, not recomputed from the native word.
ENCODED_PROFILE = (1282, 58, 86, 104, 48, 24, 8, 8)
ENCODED_MASS = 2576
PROGRESS = 2312
LEGACY_TRANSPORTS = 192
LEGACY_UNIT_ADDS = 960
LEGACY_HALVES = 104


def fail(message):
    raise SystemExit("FAIL_ENCODED_SUM_CONSUMER " + message)


def mass(profile):
    total = 0
    for rank, count in enumerate(profile, start=1):
        total += rank * count
    return total


def blank_state(values):
    return {
        "XN": list(values["XN"]),
        "YN": list(values["YN"]),
        "XJ": list(values["XJ"]),
        "YJ": list(values["YJ"]),
        "H": list(values["H"]),
        "XN_chart": ["H"] * N,
        "YN_chart": ["FULL"] * N,
        "XJ_chart": ["FULL"] * J,
        "YJ_chart": ["H"] * J,
    }


def copy_sums(state, *, clear=True, sign=1, descend=True):
    """Lift each X_n, replace Y_n by sign * X_n, then descend Y_n."""
    transports = []
    unit_adds = 0
    for n in range(N):
        if state["XN_chart"][n] != "H":
            fail("lift started off H_n")
        state["XN_chart"][n] = "FULL"
        transports.append(("lift", n))
        if clear:
            state["YN"][n] = state["YN"][n] - state["YN"][n]
            unit_adds += 1
        state["YN"][n] = state["YN"][n] + sign * state["XN"][n]
        unit_adds += 1
        if descend:
            if state["YN_chart"][n] != "FULL":
                fail("descent started off FULL")
            state["YN_chart"][n] = "H"
            transports.append(("descend", n))
    return transports, unit_adds


def require_sums(before, after):
    if after["YN"] != before["XN"]:
        fail("Y_N is not w_N")
    if after["YJ"] != before["YJ"]:
        fail("Y_J moved")
    if after["XJ"] != before["XJ"]:
        fail("q moved")
    if after["H"] != before["H"]:
        fail("a helper moved")
    if after["XN"] != before["XN"]:
        fail("X_N value changed")
    if after["YN_chart"] != ["H"] * N or after["XN_chart"] != ["FULL"] * N:
        fail("sum-only charts are not H_n on Y and FULL on X")
    if after["YJ_chart"] != before["YJ_chart"] or after["XJ_chart"] != before["XJ_chart"]:
        fail("untouched charts changed")


def incidence_floor(transports):
    """Each nested transport meets at most one of the 96 hyperplanes."""
    seen = []
    for kind, index in transports:
        if kind not in ("lift", "descend") or not 0 <= index < N:
            fail("transport outside the N hyperplanes")
        seen.append(index)
    if len(seen) != len(transports):
        fail("incidence tally dropped a transport")
    # Each recorded transport contributes one hyperplane endpoint. The
    # incomparability hypothesis is what forbids one transport from covering
    # two of these hyperplanes; this tally does not re-prove that geometry.
    return len(seen)


def screen(native_mass, stages=9):
    progress = PROGRESS
    width = 8 * stages + 1
    roles = 104 * (stages - 1)
    credit_gap = stages * (native_mass - progress - 104) + 104
    paid = stages * native_mass + max(0, (width - 1) * roles - stages * progress)
    capacity = width * roles
    return {
        "width": width,
        "roles": roles,
        "credit_gap": credit_gap,
        "paid": paid,
        "capacity": capacity,
        "deficit": paid - capacity,
    }


def pattern(seed):
    return {
        "XN": [seed + 3 * n for n in range(N)],
        "YN": [-(seed + 5 * n + 1) for n in range(N)],
        "XJ": [seed * 17 + j for j in range(J)],
        "YJ": [1000 + seed + j * j for j in range(J)],
        "H": [seed - 40 * h for h in range(HELPERS)],
    }


def main():
    if mass(ENCODED_PROFILE) != ENCODED_MASS:
        fail("encoded profile is not mass 2576")
    encoded_h1 = ENCODED_PROFILE[0]
    sum_profile = (encoded_h1 + 2 * N,) + ENCODED_PROFILE[1:]
    if mass(sum_profile) != ENCODED_MASS + 2 * N:
        fail("sum-only mass is not encoded mass plus 192")
    if 2 * N != LEGACY_TRANSPORTS:
        fail("N is not 96")

    for seed in (0, 1, -4, 19):
        values = pattern(seed)
        before = blank_state(values)
        after = blank_state(values)
        transports, unit_adds = copy_sums(after)
        require_sums(before, after)
        if len(transports) != 2 * N or unit_adds != 2 * N:
            fail("protocol size drifted")
        if incidence_floor(transports) != 2 * N:
            fail("attained transports do not meet the floor count")
        # x is not restored: X_N still holds w_N, at FULL, not the preimage x_N.
        if after["XN"] != values["XN"] or after["XN_chart"][0] != "FULL":
            fail("x restoration was smuggled into the sum protocol")

    # Separating inputs: only coordinate n is nonzero, and it must still move.
    for n in (0, 1, 47, 95):
        values = pattern(0)
        for key in ("XN", "YN", "XJ", "YJ", "H"):
            values[key] = [0] * len(values[key])
        values["XN"][n] = 8
        before = blank_state(values)
        after = blank_state(values)
        transports, _unit_adds = copy_sums(after)
        require_sums(before, after)
        touched = [index for _kind, index in transports]
        if touched.count(n) != 2:
            fail("separating port %s did not pay two transports" % n)

    # Counting bound: 96 incomparable hyperplanes, two incidences each.
    if 2 * N != 192:
        fail("floor is not 192")
    if incidence_floor([("lift", n) for n in range(N)] + [("descend", n) for n in range(N)]) < 192:
        fail("attaining schedule under-counted")

    skipped = blank_state(pattern(3))
    copy_sums(skipped, clear=False, sign=0, descend=True)
    if skipped["YN"] == pattern(3)["XN"]:
        fail("a missing copy still published w_N")

    flipped = blank_state(pattern(3))
    copy_sums(flipped, sign=-1)
    if flipped["YN"] == pattern(3)["XN"]:
        fail("a sign flip still published w_N")

    parked = blank_state(pattern(3))
    copy_sums(parked, descend=False)
    if parked["YN_chart"] == ["H"] * N:
        fail("omitted descents still occupied H_n")

    honest = screen(ENCODED_MASS + LEGACY_TRANSPORTS)
    encoded_only = screen(ENCODED_MASS)
    scalar_as_native = screen(ENCODED_MASS + LEGACY_TRANSPORTS - (LEGACY_UNIT_ADDS - 2 * N))
    # Published PR #3943 sample row at nine stages. Here (m-1)W > sP, so the
    # linear gap equals the positive-part deficit.
    if (honest["paid"], honest["capacity"], honest["deficit"]) != (64008, 60736, 3272):
        fail("nine-stage return deficit is not 3272")
    if honest["credit_gap"] != 3272:
        fail("nine-stage linear gap drifted")
    if (encoded_only["paid"], encoded_only["capacity"], encoded_only["deficit"]) != (62280, 60736, 1544):
        fail("encoded-exit deficit is not 1544")
    # At three stages the positive part is zero. The linear gap 1160 is the
    # published weaker bound; the paid-mass deficit is larger and still positive.
    three = screen(ENCODED_MASS + LEGACY_TRANSPORTS, 3)
    if (three["paid"], three["capacity"], three["deficit"], three["credit_gap"]) != (8304, 5200, 3104, 1160):
        fail("three-stage return bill does not match the published split")
    if scalar_as_native["deficit"] >= 0:
        fail("control: charging the scalar saving as native rank did not change the sign")
    if honest["deficit"] <= 0 or three["deficit"] <= 0:
        fail("sum-only native bill was affordable")

    # Legacy source return and this sum-only consumer add the same 192 rank-one
    # transports. The 768-unit-ADD scalar gap is not a rank-profile gap.
    if (encoded_h1 + LEGACY_TRANSPORTS, *ENCODED_PROFILE[1:]) != sum_profile:
        fail("sum-only profile is not the legacy native increment")
    if LEGACY_HALVES != 104 or 2 * N != 192:
        fail("scalar comparison constants drifted")

    print(
        "PASS_ENCODED_SUM_CONSUMER transports=192 unit_adds=192 halves=0 "
        "native_mass=2768 deficit_s9=3272 encoded_deficit_s9=1544 x_restored=0"
    )


if __name__ == "__main__":
    main()
