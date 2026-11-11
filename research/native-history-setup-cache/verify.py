#!/usr/bin/env python3
"""Check cache semantics and both complete unchanged caller executions."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

from run import CAPACITY, HERE, SOURCE, authenticate, cached_native, need
from benchmark import summarize


def source_module(root):
    spec = importlib.util.spec_from_file_location("oracle_monomial", root / SOURCE / "monomial.py")
    need(spec is not None and spec.loader is not None, "oracle loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def unitriangular(mask):
    columns = [1 << j for j in range(9)]
    bit = 0
    for j in range(9):
        for i in range(j):
            if mask >> bit & 1:
                columns[j] ^= 1 << i
            bit += 1
    return columns


def conformance(module):
    wrapped, cache = cached_native(module.native)
    for mask in range(300):
        columns = unitriangular(mask)
        need(wrapped(columns) == module.native(columns), "literal monomial bytes")
        need(wrapped(list(columns)) == wrapped(tuple(columns)), "content-key reuse")
    info = cache.cache_info()
    need(info.misses == 300 and info.hits == 600 and info.currsize == CAPACITY,
         "bounded capacity and complete-key hits")
    before = info.misses
    need(wrapped(unitriangular(0)) == module.native(unitriangular(0)), "evicted value")
    need(cache.cache_info().misses == before + 1, "oldest value was evicted")
    cache.cache_clear()
    columns = unitriangular(0)
    first = wrapped(columns)
    columns[1] ^= 1
    changed = wrapped(columns)
    need(first != changed, "mutated columns cannot reuse the old key")
    columns[1] ^= 1
    need(wrapped(columns) == first and cache.cache_info().hits == 1,
         "restored contents reuse their own immutable result")
    other, other_cache = cached_native(module.native)
    need(other_cache.cache_info().currsize == 0, "new invocation owns an empty cache")
    need(other(unitriangular(0)) == first and other_cache.cache_info().misses == 1,
         "no state leaks between cache owners")
    cache.cache_clear()
    other_cache.cache_clear()
    return 300


def rejection_controls(module):
    wrapped, cache = cached_native(module.native)
    invalid = [[], [0] * 8, [0] * 10, [-1] + [0] * 8,
               [512] + [0] * 8, [False] + [0] * 8]
    for columns in invalid:
        try:
            wrapped(columns)
        except ValueError:
            pass
        else:
            raise ValueError("invalid native-map boundary accepted")
    for _ in range(2):
        try:
            wrapped([0] * 9)
        except ValueError as error:
            need(str(error) == "singular native map", "same singular-map failure")
        else:
            raise ValueError("singular map accepted")
    need(cache.cache_info().misses == 2 and cache.cache_info().currsize == 0,
         "failed constructions are never cached")
    return len(invalid) + 2


def complete_callers(root):
    outputs, reports = [], []
    for mode in ("baseline", "cached"):
        command = [sys.executable, "-W", "error", "-B"]
        if sys.flags.optimize:
            command.append("-O")
        command += [str(HERE / "run.py"), "--mode", mode, "--root", str(root)]
        result = subprocess.run(command, capture_output=True, timeout=120, check=False)
        need(result.returncode == 0, result.stderr.decode())
        outputs.append(result.stdout)
        reports.append(json.loads(result.stderr))
    need(outputs[0] == outputs[1], "all complete scientific output bytes agree")
    actual = json.loads(outputs[1])
    expected = json.loads((root / SOURCE / "KERNEL-RESULT.json").read_bytes())
    need(actual == expected, "every source scientific result field is retained")
    need(reports[1]["cache"] == {"currsize": 58, "hits": 158,
                                 "maxsize": CAPACITY, "misses": 58},
         "all 216 construction requests consumed on the actual complete path")
    return sha256(outputs[0]).hexdigest(), reports[1]["cache"]


def benchmark_binding(digest):
    receipt = json.loads((HERE / "BENCHMARK.json").read_text())
    for name, source_digest in receipt["source_sha256"].items():
        need(sha256((HERE / name).read_bytes()).hexdigest() == source_digest,
             "generated measurement source binding " + name)
    need(receipt["errors"] == 0 and len(receipt["samples"]) == 10,
         "five alternating successful complete pairs")
    for trial in range(5):
        pair = receipt["samples"][2 * trial:2 * trial + 2]
        need([row["mode"] for row in pair] == ["baseline", "cached"], "alternating order")
        need(all(row["trial"] == trial and row["returncode"] == 0 for row in pair),
             "successful trial ownership")
    need({row["output_sha256"] for row in receipt["samples"]} == {digest},
         "all measured complete scientific outputs agree")
    need(receipt["summary"] == summarize(receipt["samples"]), "measurement summary")


def main():
    root = HERE.parents[1]
    authenticate(root)
    module = source_module(root)
    matrices = conformance(module)
    rejections = rejection_controls(module)
    digest, stats = complete_callers(root)
    benchmark_binding(digest)
    print(json.dumps({"status": "PASS_NATIVE_HISTORY_SETUP_CACHE", "maps": matrices,
                      "rejection_executions": rejections, "complete_callers": 2,
                      "complete_output_sha256": digest, "cache": stats}, sort_keys=True))


if __name__ == "__main__":
    main()
