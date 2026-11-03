#!/usr/bin/env python3
"""Replay the bounded dyadic-sphere construction; no optimal-error claim.

Jerry Chen / CubeJerry with substantial OpenAI Codex assistance. Apache-2.0.
"""

import importlib.util
import json
from fractions import Fraction
from math import isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("certificate", HERE / "verify.py")
certificate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(certificate)
SEED = "0b7fc9054fc70396e2d971f95342f0a4"
Z = [x for pair in certificate.GUIDE for x in pair]
N = sum(x * x for x in Z)


def floor_coordinate(x, radius):
    square = (radius * x) ** 2
    lower = isqrt(square // N)
    return lower if x >= 0 else -lower - (lower * lower * N != square)


def closest(k):
    radius = 2 ** k
    offset = int(SEED, 16) % 16
    order = list(range(offset, 16)) + list(range(offset))
    choices = [list(range(floor_coordinate(Z[i], radius) - 1,
                          floor_coordinate(Z[i], radius) + 2)) for i in order]
    low = [sum(min(x * x for x in c) for c in choices[j:]) for j in range(17)]
    high = [sum(max(x * x for x in c) for c in choices[j:]) for j in range(17)]
    dp, counts, transitions = {0: (0, ())}, [], 0
    for j, (i, options) in enumerate(zip(order, choices, strict=True)):
        output = {}
        for total, (score, vector) in dp.items():
            for x in options:
                squared = total + x * x
                if squared + low[j + 1] <= radius ** 2 <= squared + high[j + 1]:
                    candidate = (score + x * Z[i], vector + (x,))
                    transitions += 1
                    if squared not in output or candidate > output[squared]:
                        output[squared] = candidate
        dp = output
        counts.append(len(dp))
    if radius ** 2 not in dp:
        return {"k": k, "no_norm_vector": True, "states": counts}
    score, raw = dp[radius ** 2]
    vector = [0] * 16
    for i, x in zip(order, raw, strict=True):
        vector[i] = x
    certificate.require(sum(x * x for x in vector) == radius ** 2, "search exact norm")
    return {"k": k, "vector": vector, "norm": radius ** 2,
            "states": counts, "transitions": transitions, "dot_product": score}


def replay():
    certificate.check_sources()
    signs = json.loads((certificate.ROOT / certificate.DATA).read_text())["signs"]
    roots, _ = certificate.roots_from_signs(signs)
    certificate.require(max(map(certificate.norm, certificate.responses(roots, certificate.GUIDE)))
                        == 4820, "search predecessor positive control")
    results = []
    for k in range(4, 10):
        record = closest(k)
        if "vector" in record:
            v = record["vector"]
            z = list(zip(v[::2], v[1::2], strict=True))
            maximum = max(map(certificate.norm, certificate.responses(roots, z)))
            record.update(maximum=maximum, error=str(Fraction(maximum, 8 * record["norm"])),
                          passes=maximum < 2 * record["norm"])
        results.append(record)
        if record.get("passes"):
            break
    return results


def main():
    result = replay()
    witness = json.loads((HERE / "WITNESS.json").read_text())
    certificate.require(result == witness["search"], "search receipt")
    flat = result[-1]["vector"]
    certificate.require([list(x) for x in zip(flat[::2], flat[1::2], strict=True)] == witness["z"],
                        "search final witness")
    print(json.dumps({"status": "PASS_BOUNDED_DYADIC_SEARCH", "seed": SEED,
                      "scales_completed": len(result), "stopped_at": result[-1]["k"],
                      "search": result}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
