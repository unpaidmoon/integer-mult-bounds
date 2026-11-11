#!/usr/bin/env python3
"""Exact finite corroboration of the variance-sensitive compiler tail screen."""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from math import lcm
from pathlib import Path


FILES = ("README.md", "PROOF.md", "TASK.json", "SOURCES.json", "VERIFY.json", "verify.py")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rational(value):
    require(type(value) is F, "exact Fraction required")
    require(max(value.numerator.bit_length(), value.denominator.bit_length()) <= 128,
            "rational input exceeds 128 bits")


def extremal(p, variance):
    rational(p)
    rational(variance)
    require(0 < p < 1 and 0 < variance <= p * (1 - p), "invalid moments")
    b = p + variance / p
    theta = p / b
    return ((F(0), 1 - theta), (b, theta))


def statistics(law):
    require(1 <= len(law) <= 5, "law size outside 1..5")
    for z, mass in law:
        rational(z)
        rational(mass)
        require(0 <= z <= 1 and mass > 0, "invalid law entry")
    require(sum(mass for _, mass in law) == 1, "mass is not one")
    p = sum(z * mass for z, mass in law)
    second = sum(z * z * mass for z, mass in law)
    return p, second - p * p


def exp_minus(value, cache):
    """Enclose exp(-value) using 64 positive Taylor terms and a geometric tail."""
    rational(value)
    require(0 <= value <= 8, "exponential domain outside 0..8")
    if value in cache:
        return cache[value]
    require(len(cache) < 4096, "exponential cache capacity exhausted")
    term = total = F(1)
    for index in range(1, 65):
        term *= value / index
        total += term
    first_omitted = term * value / 65
    tail = first_omitted / (1 - value / 66)
    bounds = (1 / (total + tail), 1 / total)
    require(0 < bounds[0] <= bounds[1] <= 1, "invalid exponential enclosure")
    cache[value] = bounds
    return bounds


def scale(interval, factor):
    lo, hi = interval
    return (lo * factor, hi * factor) if factor >= 0 else (hi * factor, lo * factor)


def transform(law, h, cache):
    terms = [scale(exp_minus(h * z, cache), mass) for z, mass in law]
    return sum(lo for lo, _ in terms), sum(hi for _, hi in terms)


def quadratic(z, b, h, cache):
    base = 1 - 2 * z / b + z * z / (b * b)
    coefficient = (2 + h * b) * z / b - (1 + h * b) * z * z / (b * b)
    lo, hi = scale(exp_minus(h * b, cache), coefficient)
    return base + lo, base + hi


def moment_census(cache):
    counts = dict(laws=0, nondegenerate=0, comparisons=0, equalities=0,
                  strict=0, pointwise=0, beyond_b=0)
    points = tuple(F(i, 4) for i in range(5))
    for weights in product(range(3), repeat=5):
        total = sum(weights)
        if total == 0:
            continue
        law = tuple((z, F(w, total)) for z, w in zip(points, weights) if w)
        p, variance = statistics(law)
        counts["laws"] += 1
        if variance == 0:
            continue
        counts["nondegenerate"] += 1
        comparison = extremal(p, variance)
        require(statistics(comparison) == (p, variance), "extremal moments differ")
        b = comparison[1][0]
        is_extremal = all(z in (0, b) for z, _ in law)
        for h in (F(1, 4), F(1), F(2), F(4)):
            actual = transform(law, h, cache)
            envelope = transform(comparison, h, cache)
            if is_extremal:
                require(dict(law) == dict(comparison), "wrong extremal weights")
                require(actual == envelope, "extremal transform differs")
                counts["equalities"] += 1
            else:
                require(actual[1] < envelope[0], "strict transform bound failed")
                counts["strict"] += 1
            counts["comparisons"] += 1
            for z in points + (F(3, 2), F(2)):
                poly = quadratic(z, b, h, cache)
                exponential = exp_minus(h * z, cache)
                if z in (0, b):
                    require(poly == exponential, "Hermite interpolation failed")
                else:
                    require(poly[0] > exponential[1], "quadratic majorant failed")
                counts["pointwise"] += 1
                counts["beyond_b"] += int(z > b)
    return counts


def optimum(theta, alpha, q):
    for value in (theta, alpha, q):
        rational(value)
    require(0 < alpha < theta < 1 and q >= 1, "invalid gate parameters")
    exponent = alpha.denominator
    a = alpha.numerator
    y = theta * (1 - alpha) / (alpha * (1 - theta))
    entropy = (theta / alpha) ** a * ((1 - theta) / (1 - alpha)) ** (exponent - a)
    value = q ** exponent * entropy
    return y, value


def objective_power(theta, alpha, q, y):
    require(y > 1, "tail parameter must be positive")
    return (q * (1 - theta + theta / y)) ** alpha.denominator * y ** alpha.numerator


def stationary_census():
    counts = dict(parameters=0, tariff_cases=0, passing=0, failing=0, off_minimum=0)
    for denominator in range(3, 11):
        for high in range(2, denominator):
            theta = F(high, denominator)
            for low in range(1, high):
                alpha = F(low, denominator)
                counts["parameters"] += 1
                for numerator in range(8, 17):
                    q = F(numerator, 8)
                    y, expected = optimum(theta, alpha, q)
                    actual = objective_power(theta, alpha, q, y)
                    require(actual == expected, "entropy and critical value differ")
                    require(alpha * (1 - theta) * y == theta * (1 - alpha),
                            "stationary derivative not zero")
                    for trial in ((1 + y) / 2, (2 + y) / 3, 2 * y, 3 * y):
                        require(objective_power(theta, alpha, q, trial) > actual,
                                "off-minimum objective failed")
                        counts["off_minimum"] += 1
                    counts["tariff_cases"] += 1
                    counts["passing" if actual < 1 else "failing"] += 1
    return counts


def screen_comparison():
    counts = dict(strict=0, coincident=0)
    for p in (F(1, 3), F(1, 2), F(2, 3)):
        for step in range(1, 5):
            variance = F(step, 4) * p * (1 - p)
            b = p + variance / p
            for offset in range(1, 4):
                x = p * F(offset, 4)
                _, old = optimum(p, x, F(1))
                _, new = optimum(p / b, x / b, F(1))
                common = lcm(x.denominator, (x / b).denominator)
                old_power = old ** (common // x.denominator)
                new_power = new ** (common // (x / b).denominator)
                if step == 4:
                    require(new_power == old_power, "maximal variance screens differ")
                    counts["coincident"] += 1
                else:
                    require(new_power < old_power, "variance screen is not stronger")
                    counts["strict"] += 1
    return counts


def cube_bounds(value):
    require(0 <= value <= 64, "cube-root domain outside 0..64")
    low, high = F(0), F(4)
    for _ in range(48):
        middle = (low + high) / 2
        if middle ** 3 == value:
            return middle, middle
        if middle ** 3 < value:
            low = middle
        else:
            high = middle
    require(low ** 3 <= value <= high ** 3, "cube-root bracket failed")
    return low, high


def histogram_fixture():
    target = ((2, 32), (6, 16), (10, 2))
    tilted = tuple((F(e - 2, 8), F(w * 2 ** (e // 2), 256)) for e, w in target)
    require(statistics(tilted) == (F(1, 2), F(1, 8)), "wrong tilted moments")
    require(sum(w * 2 ** (e // 2) for e, w in target) == 256, "wrong target mass")
    q_squared = F(32 ** 2 * 2, 43 ** 2)
    require(q_squared > 1, "fixture must have q greater than one")
    _, new_squared = optimum(F(2, 3), F(1, 2), F(1))
    require(q_squared * new_squared == F(128, 129) ** 2, "wrong new optimum")
    require(F(128, 129) < 1, "variance screen does not pass")
    _, old_eighth = optimum(F(1, 2), F(3, 8), F(1))
    require(q_squared ** 4 * old_eighth == F(2 ** 60, 3 ** 3 * 5 ** 5 * 43 ** 8),
            "wrong older optimum")
    require(2 ** 60 > 3 ** 3 * 5 ** 5 * 43 ** 8, "older screen unexpectedly passes")
    root_lo, root_hi = F(5, 4), F(63, 50)
    require(root_lo ** 3 < 2 < root_hi ** 3, "cube root is not enclosed")
    direct_upper = (16 + 16 * root_hi + 4 * root_hi ** 2) / 43
    require(direct_upper < F(128, 129), "literal tail point does not pass the bound")
    brackets = [(w, cube_bounds(F(2) ** (e - 5))) for e, w in target]
    literal_upper = sum(w * bounds[1] for w, bounds in brackets) / 43
    require(literal_upper < direct_upper, "independent rank-ratio calculation differs")
    # Same moments, distinct support: the equality threshold is strict here.
    perturbed = ((F(0), F(1, 10)), (F(1, 2), F(3, 5)), (F(1), F(3, 10)))
    require(statistics(perturbed) == (F(3, 5), F(9, 100)), "perturbed moments differ")
    _, equal_value = optimum(F(4, 5), F(1, 2), F(5, 4))
    require(equal_value == 1, "two-point equality fixture is not on the boundary")
    perturbed_upper = F(1, 4) + F(3, 4) / root_lo + F(3, 16) / root_lo ** 2
    require(perturbed_upper < 1, "nonextremal equality fixture fails")
    return {"target": {"4": 32, "64": 16, "1024": 2}, "paid": {"32": 43},
            "guaranteed_bound": "128/129", "literal_upper": str(direct_upper),
            "lambda": "1/6", "equality_laws": 2}


def rejected(function, arguments):
    try:
        function(*arguments)
    except ValueError:
        return
    raise ValueError("invalid input was accepted")


def controls(cache):
    cases = ((extremal, (F(0), F(1, 8))), (extremal, (F(1), F(1, 8))),
             (extremal, (F(1, 2), F(0))), (extremal, (F(1, 2), F(-1, 8))),
             (extremal, (F(1, 2), F(1, 3))), (extremal, (0.5, F(1, 8))),
             (optimum, (F(1, 2), F(1, 2), F(1))),
             (optimum, (F(1, 2), F(1, 4), F(1, 2))),
             (statistics, (((F(0), F(1, 3)), (F(1), F(1, 3))),)),
             (exp_minus, (F(-1), cache)), (exp_minus, (F(9), cache)),
             (exp_minus, (F(1), {F(i): (F(1), F(1)) for i in range(4096, 8192)})))
    for function, arguments in cases:
        rejected(function, arguments)
    # A reversed critical ratio cannot satisfy the derivative equation.
    theta, alpha = F(2, 3), F(1, 2)
    y, _ = optimum(theta, alpha, F(1))
    require(alpha * (1 - theta) / y != theta * (1 - alpha), "inverse-ratio mutant survives")
    # Omitting the variance makes b=p, which is inconsistent with the second moment.
    p, variance = F(1, 2), F(1, 8)
    require(p * p != p * p + variance, "variance omission survives")
    # Uniform multiplicities are not the tilted probability measure.
    raw = tuple((F(e - 2, 8), F(w, 50)) for e, w in ((2, 32), (6, 16), (10, 2)))
    require(statistics(raw) != (p, variance), "untilted-weights mutant survives")
    require(F(128, 3 * 42) > 1, "insufficient paid-mass statistical control survives")
    return {"invalid_inputs": len(cases), "semantic_mutants": 4}


def main():
    cache = {}
    result = {"claim_type": "scoped written proof with exact finite corroboration",
              "moments": moment_census(cache), "stationary": stationary_census(),
              "screen_comparison": screen_comparison(),
              "fixture": histogram_fixture(), "controls": controls(cache)}
    result["exponential_cache_entries"] = len(cache)
    root = Path(__file__).resolve().parent
    hashes = {}
    for name in FILES:
        data = (root / name).read_bytes()
        require(len(data) <= 128 * 1024, "receipt source exceeds 128 KiB")
        hashes[name] = sha256(data).hexdigest()
    print(json.dumps({"result": result, "sources_sha256": hashes}, sort_keys=True))
    print("PASS_VARIANCE_TAIL_GATE no_new_kappa")


if __name__ == "__main__":
    main()
