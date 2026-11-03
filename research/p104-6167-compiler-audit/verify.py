#!/usr/bin/env python3
"""Independent integer/rational compiler application check for PR6167.

No predecessor code, floats, Decimal, logarithm or exponential is executed.
Prepared for @CubeJerry with substantial OpenAI Codex assistance. Apache-2.0.
See README.md for the arithmetic proof, predecessor credit and precise scope.
"""
from copy import deepcopy
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from math import isqrt
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = "research/p104-retained-operand-descent/RESULT.json"
AUDIT = "research/p104-retained-operand-independent-audit/RESULT.json"
THEOREM = "research/higher-moment-strictification/README.md"
PRECOMPILE = "research/higher-moment-strictification/vendor/FINITE-PRECOMPILATION.md"
MARKER = "PASS_P104_6167_COMPILER_AUDIT"
SCALE_BITS, EXPONENT_BITS = 256, 160


class Rejection(ValueError):
    pass


def require(ok, code):
    if not ok:
        raise Rejection(code)


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "duplicate_json_key")
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=pairs)


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def mul(a, b):
    require(a[0] >= 0 and b[0] >= 0, "nonnegative_intervals")
    return a[0] * b[0], a[1] * b[1]


def div(a, b):
    require(a[0] >= 0 and b[0] > 0, "positive_interval_divisor")
    return a[0] / b[1], a[1] / b[0]


def exact(x):
    return F(x), F(x)


def ceil_div(a, b):
    return -(-a // b)


def ceil_sqrt(n):
    q = isqrt(n)
    return q + (q * q != n)


@lru_cache(maxsize=None)
def power(base, exponent, scale_bits=SCALE_BITS, exponent_bits=EXPONENT_BITS):
    """Outward fixed-point roots plus a convex bound on the exponent tail."""
    require(type(base) is int and base >= 1, "positive_integer_base")
    require(type(scale_bits) is int and scale_bits >= 2, "scale_bits")
    require(type(exponent_bits) is int and exponent_bits >= 1, "exponent_bits")
    exponent = F(exponent)
    if exponent < 0:
        lo, hi = power(base, -exponent, scale_bits, exponent_bits)
        return 1 / hi, 1 / lo
    whole = exponent.numerator // exponent.denominator
    fraction = exponent - whole
    if base == 1 or not fraction:
        return exact(base ** whole)
    scale = 1 << scale_bits
    bits = (fraction.numerator << exponent_bits) // fraction.denominator
    tail = fraction - F(bits, 1 << exponent_bits)
    require(0 <= tail < F(1, 1 << exponent_bits), "exponent_tail")
    root_lo = root_hi = base * scale
    product_lo = product_hi = scale
    for index in range(exponent_bits):
        root_lo = isqrt(root_lo * scale)
        root_hi = ceil_sqrt(root_hi * scale)
        if bits & (1 << (exponent_bits - 1 - index)):
            product_lo = product_lo * root_lo // scale
            product_hi = ceil_div(product_hi * root_hi, scale)
    factor = base ** whole
    return (F(factor * product_lo, scale),
            F(factor * product_hi, scale) * (1 + (base - 1) * tail))


def histogram(raw):
    require(type(raw) is dict and raw, "histogram_object")
    result = {}
    for rank, count in raw.items():
        require(type(rank) is str and rank.isdecimal() and str(int(rank)) == rank,
                "canonical_rank")
        require(int(rank) > 0 and type(count) is int and count > 0,
                "positive_histogram_entry")
        result[int(rank)] = count
    return result


def moment(hist, exponent):
    result = exact(0)
    for rank, count in sorted(hist.items()):
        result = add(result, mul(exact(count), power(rank, exponent)))
    return result


def decimal_bound(q, digits, upper=False):
    """Outward decimal printing using integers only."""
    unit = 10 ** digits
    n = ceil_div(q.numerator * unit, q.denominator) if upper else q.numerator * unit // q.denominator
    sign = "-" if n < 0 else ""
    n = abs(n)
    return f"{sign}{n // unit}.{n % unit:0{digits}d}"


def enclosure(value):
    return {"lower": str(value[0]), "upper": str(value[1]),
            "decimal_lower": decimal_bound(value[0], 40),
            "decimal_upper": decimal_bound(value[1], 40, True)}


def parameters(cost):
    st, co = cost["strictification"], cost["compiler"]
    return {"C": F(st["tested"]), "kappa": F(cost["kappa"]),
            "u": F(st["tail_offset"]), "v": st["power"],
            "c": st["cutoff"], "b": st["floor"],
            "reserve": F(st["reserve"]), "decay": F(st["tail_decay"]),
            "block": st["tail_block"], "theta": F(co["theta"]),
            "p": co["logarithm_power"], "gap": F(co["gap"]),
            "uniform": F(co["uniform_saving"]), "H": co["H"],
            "j": co["integer_test_exponent"], "N": co["N"]}


def hypotheses(T, P, par, ambient=None):
    """Instantiate sections 2 and 4 of the written theorem, not pricing.py."""
    C, u, v, c, b = (par[k] for k in ("C", "u", "v", "c", "b"))
    t, m = 1 - C, max(T) if ambient is None else ambient
    require(0 < C < 1, "saving_range")
    require(u >= C and t + u >= 1, "higher_moment_sigma")
    require(all(type(x) is int and x >= 1 for x in (v, c, b, m)), "integer_ranks")
    require(1 < c < b < m, "separated_rank_bases")
    reserve, decay, block = (par[k] for k in ("reserve", "decay", "block"))
    require(0 < reserve < 1 and 0 < decay < 1, "tail_constants")
    require(type(block) is int and block > 0 and v % block == 0, "whole_decay_blocks")
    target = moment(T, t)
    alpha = div(moment(P, t), target)
    gamma = div(moment(P, t + u), mul(power(c, u), target))
    delta = div(exact(sum(T.values()) * b), mul(power(c, C), target))
    require(alpha[1] < 1 - reserve, "paid_moment_reserve")
    require(gamma[1] < decay, "original_paid_tail")
    require(delta[1] < decay, "completion_tail")
    require(decay ** block < F(1, 16), "tail_decay_block")
    normalized = 1 / (1 + v * reserve) + 4 * F(1, 16) ** (v // block)
    require(normalized < 1, "complete_split_budget")
    theta, p = par["theta"], par["p"]
    require(0 < theta < 1 and type(p) is int and p > 0, "majorant_parameters")
    a, d = theta.numerator, theta.denominator
    require(c ** d < b ** a, "exit_exponent")
    require(2 ** (d - a) * c ** (v * d) <= m ** (v * a), "shifted_exit")
    eta = mul(exact(t), power(m, -v * C))
    require(theta ** p < eta[0], "complement_capacity")
    initial = power(m, v * C)
    require(initial[1] < 2 ** p, "initial_range")
    gap, kappa, uniform = (par[k] for k in ("gap", "kappa", "uniform"))
    require(0 < kappa < uniform < C < 1, "saving_order")
    require(gap == C - uniform == (C - kappa) / 7, "compiler_gap")
    require(gap.numerator == 1, "unit_fraction_grid")
    step = gap.denominator
    H, j = par["H"], par["j"]
    require(type(H) is int and type(j) is int and j > 1 and H == step * j, "threshold_grid")
    require(par["N"] == f"2^{H}", "rank_encoding")
    require((H + 1) ** p < 2 ** j, "threshold_pass")
    require((step * (j - 1) + 1) ** p >= 2 ** (j - 1), "threshold_predecessor")
    # g(j)=j ln2-p ln(1+step*j): g(0)=0, g'(0)<0, g''>0.
    # These hypotheses plus the two exact signs prove first-grid status.
    require(p * step > 1, "threshold_convexity")
    require(H > 8 * v and m < 2 ** 8, "threshold_above_ambient")
    return {"alpha": alpha, "gamma": gamma, "delta": delta, "eta": eta,
            "initial": initial, "normalized": normalized,
            "complete_split_slack": 1 - normalized,
            "alpha_reserve_slack": 1 - reserve - alpha[1],
            "gamma_slack": decay - gamma[1], "delta_slack": decay - delta[1],
            "complement_slack": eta[0] - theta ** p}


def bind(cost, other):
    T, P, par = histogram(cost["targets"]), histogram(cost["paid"]), parameters(cost)
    require(par["C"] == F(62573, 20000000) and par["kappa"] == F(625729, 200000000),
            "pr6167_parameter_identity")
    required = {"u": F(1, 7), "v": 1024, "c": 16, "b": 17,
                "reserve": F(1, 10**12), "decay": F(125, 128), "block": 128,
                "theta": F(63, 64), "p": 1024}
    require(all(par[key] == value for key, value in required.items()), "pr6167_compiler_recipe")
    totals = {"productive_fields": sum(T.values()), "paid_calls": sum(P.values()),
              "paid_rank_mass": sum(r * n for r, n in P.items()),
              "rank_mass_surplus": sum(r * n for r, n in T.items()) - sum(r * n for r, n in P.items()),
              "max_paid_rank": max(P), "max_target_rank": max(T)}
    require(totals == other["layer2_invoice"]["6167"], "independent_invoice_receipt")
    require((totals["productive_fields"], totals["paid_calls"], totals["rank_mass_surplus"])
            == (13444, 66762, 760), "pr6167_invoice_totals")
    for key in ("productive_fields", "paid_calls", "rank_mass_surplus"):
        require(totals[key] == cost[key], "author_invoice_totals")
    found = hypotheses(T, P, par)
    for key in ("alpha", "gamma", "delta", "eta"):
        shown = (cost["compiler"] if key == "eta" else cost["strictification"])[key]
        require(F(shown["lower"]) <= found[key][0] <= found[key][1] <= F(shown["upper"]),
                "published_interval_" + key)
    require(found["normalized"] == F(cost["strictification"]["normalized_paid_upper"]),
            "published_complete_budget")
    return T, P, par, totals, found


def source_pins(root=ROOT):
    manifest = strict_json((HERE / "SOURCES.json").read_text(encoding="utf-8"))
    inputs = [row for row in manifest["files"] if row.get("usage") == "input"]
    expected = strict_json((HERE / "VERIFY.json").read_text(encoding="utf-8"))["inputs"]
    require({r["path"] for r in inputs} == set(expected), "input_manifest_coverage")
    pins = {}
    for row in inputs:
        digest = sha256((root / row["path"]).read_bytes()).hexdigest()
        require(digest == row["sha256"], "source_hash:" + row["path"])
        pins[row["path"]] = digest
    return pins


def rejection(name, expected, call, controls):
    try:
        call()
    except Rejection as exc:
        require(str(exc) == expected, "wrong_control_reason:" + name + ":" + str(exc))
        controls[name] = expected
    else:
        raise Rejection("accepted_control:" + name)


def arithmetic_controls(seed=78):
    # A distinct oracle: integer raising of interval endpoints, not roots/logs.
    count = 0
    for base in range(1, 21):
        for denominator in range(1, 10):
            for numerator in range(-2 * denominator, 2 * denominator + 1):
                e = F(numerator, denominator)
                lo, hi = power(base, e)
                exact_power = F(base) ** e.numerator
                require(0 < lo <= hi and lo ** e.denominator <= exact_power <= hi ** e.denominator,
                        "integer_power_oracle")
                count += 1
    # Low precision deliberately exercises rounding and non-dyadic tails.
    # The seed changes order, not the coverage or novelty claim.
    low_count = 0
    bases = list(range(2, 18))
    bases = bases[seed % len(bases):] + bases[:seed % len(bases)]
    for base in bases:
        for denominator in (3, 5, 7, 11):
            for numerator in (-2, -1, 1, 2, 4):
                e = F(numerator, denominator)
                lo, hi = power(base, e, 8, 3)
                require(lo ** e.denominator <= F(base) ** e.numerator <= hi ** e.denominator,
                        "coarse_integer_power_oracle")
                low_count += 1
    sqrt_lo, sqrt_hi = power(2, F(1, 2), 4, 1)
    require(sqrt_lo**2 < 2 < sqrt_hi**2, "floor_root_is_not_upper")
    tail_lo, tail_hi = power(2, F(1, 3), 8, 1)
    require(tail_lo == 1 and tail_lo**3 < 2 < tail_hi**3,
            "discarded_exponent_tail_is_unsound")
    controls = {}
    rejection("base_zero", "positive_integer_base", lambda: power(0, F(1, 2)), controls)
    rejection("bool_histogram_count", "positive_histogram_entry", lambda: histogram({"1": True}), controls)
    rejection("noncanonical_rank", "canonical_rank", lambda: histogram({"01": 2}), controls)
    rejection("duplicate_json", "duplicate_json_key", lambda: strict_json('{"x":1,"x":2}'), controls)
    return {"integer_power_oracle_cases": count, "coarse_rounding_oracle_cases": low_count,
            "unsound_rounding_demonstrations": 2, "rejections": controls}


def semantic_controls(cost, other, T, P, par, found):
    controls = {}
    def altered_parameter(key, value, code):
        altered = dict(par, **{key: value})
        rejection(key + "_changed", code, lambda: hypotheses(T, P, altered), controls)
    altered_parameter("u", F(1, 10000), "higher_moment_sigma")
    altered_parameter("reserve", F(1, 10**8), "paid_moment_reserve")
    altered_parameter("decay", F(127, 128), "tail_decay_block")
    altered_parameter("theta", F(45, 46), "exit_exponent")
    altered_parameter("gap", 2 * par["gap"], "compiler_gap")
    altered_parameter("b", par["c"], "separated_rank_bases")
    altered_parameter("N", "2^65807000000001", "rank_encoding")
    altered_parameter("v", 1023, "whole_decay_blocks")
    altered = dict(par, j=par["j"] - 1, H=par["H"] - par["gap"].denominator,
                   N=f'2^{par["H"] - par["gap"].denominator}')
    rejection("previous_grid_point", "threshold_pass", lambda: hypotheses(T, P, altered), controls)
    altered = dict(par, j=par["j"] + 1, H=par["H"] + par["gap"].denominator,
                   N=f'2^{par["H"] + par["gap"].denominator}')
    rejection("later_grid_not_first", "threshold_predecessor", lambda: hypotheses(T, P, altered), controls)
    without_main = {r: n for r, n in T.items() if r != 145}
    rejection("missing_main_targets", "paid_moment_reserve",
              lambda: hypotheses(without_main, P, par), controls)
    rejection("qubit_dimension_as_ambient", "complement_capacity",
              lambda: hypotheses(T, P, par, ambient=512), controls)
    p_min = 1
    while par["theta"] ** p_min >= found["eta"][0]:
        p_min += 1
    require(par["theta"] ** (p_min - 1) > found["eta"][1], "least_power_certified")
    altered_parameter("p", p_min - 1, "complement_capacity")
    for key in ("alpha", "gamma", "delta", "eta"):
        changed = deepcopy(cost)
        section = "compiler" if key == "eta" else "strictification"
        changed[section][key] = {"lower": "0", "upper": "1/1000000000000000000000000000000000000000000000000"}
        rejection("forged_" + key, "published_interval_" + key,
                  lambda changed=changed: bind(changed, other), controls)
    changed = deepcopy(cost)
    # Same count and rank mass: a mere aggregate-receipt check cannot catch it.
    changed["paid"]["1"] -= 1
    changed["paid"]["2"] += 2
    changed["paid"]["3"] -= 1
    changed_alpha = div(moment(histogram(changed["paid"]), 1 - par["C"]),
                        moment(T, 1 - par["C"]))
    require(changed_alpha[0] > 1 - par["reserve"], "mutant_really_exhausts_reserve")
    rejection("same_mass_paid_redistribution", "paid_moment_reserve",
              lambda: bind(changed, other), controls)
    return controls, p_min


def theorem_binding():
    text = (ROOT / THEOREM).read_text(encoding="utf-8")
    for fragment in ("u >= C,  sigma = t+u >= 1,", "alpha   = P_t / T_t,",
                     "gamma_u = P_(t+u) / (c^u T_t),", "delta   = B b / (c^C T_t).",
                     "alpha^v + 2 gamma_u^v + 2 delta^v,", "2^(b−a) r_max^b <= m^a,",
                     "theta_bar^p < eta = t m^(t−1),", "m^(1−t) < 2^p.",
                     "(1+H)^p < 2^((z−t)H)"):
        require(fragment in text, "theorem_statement_fragment")
    text = (ROOT / PRECOMPILE).read_text(encoding="utf-8")
    require('Put `m=max{k:W_k>0}`, `k_min=min{k:W_k>0}`, and' in text
            and '`r_max=max{r_j}`. Require `r_max<k_min`.' in text, "compiler_rank_definitions")


def run():
    pins = source_pins()
    theorem_binding()
    cost = strict_json((ROOT / SOURCE).read_text(encoding="utf-8"))["complete_cost"]
    other = strict_json((ROOT / AUDIT).read_text(encoding="utf-8"))
    T, P, par, totals, found = bind(cost, other)
    arithmetic = arithmetic_controls()
    controls, p_min = semantic_controls(cost, other, T, P, par, found)
    return {"status": MARKER, "source_sha256": pins, "invoice": totals,
            "method": {"fixed_point_bits": SCALE_BITS, "exponent_bits": EXPONENT_BITS,
                       "arithmetic": "integers, Fraction and isqrt only; no predecessor code execution"},
            "parameters": {k: str(v) if isinstance(v, F) else v for k, v in par.items()},
            "certified_intervals": {k: enclosure(found[k]) for k in ("alpha", "gamma", "delta", "eta", "initial")},
            "strict_lower_slacks": {k: str(found[k]) for k in ("complete_split_slack", "alpha_reserve_slack",
                                    "gamma_slack", "delta_slack", "complement_slack")},
            "normalized_paid_upper": str(found["normalized"]), "least_complement_power": p_min,
            "arithmetic_controls": arithmetic, "semantic_controls": controls,
            "scope": "PR6167 numerical compiler application only. Source theorems, word-to-invoice, native/caller/outer and all five framework assumptions are inherited. No new kappa."}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write the deterministic exact receipt")
    args = parser.parse_args()
    receipt = run()
    path = HERE / "RESULT.json"
    if args.write:
        path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    else:
        require(strict_json(path.read_text(encoding="utf-8")) == receipt, "receipt_matches_recomputation")
    print(json.dumps({"status": MARKER, "semantic_controls": len(receipt["semantic_controls"]),
                      "arithmetic_oracle_cases": receipt["arithmetic_controls"]["integer_power_oracle_cases"]
                      + receipt["arithmetic_controls"]["coarse_rounding_oracle_cases"],
                      "least_complement_power": receipt["least_complement_power"],
                      "j": receipt["parameters"]["j"], "H": receipt["parameters"]["H"]}, sort_keys=True))


if __name__ == "__main__":
    main()
