"""Independent PR6280 consumer-fusion certificate and source-emitter checks.

Prepared for @CubeJerry with OpenAI Codex assistance. Apache-2.0.
Only the authenticated emitter, never the predecessor verifier, is executed.
"""
import ast
from fractions import Fraction as Q
from hashlib import sha1, sha256
from itertools import product
import json
from pathlib import Path
import runpy

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COMPILER_SHA = "9d7b71ed4da90360f8a0f15b7a89599340efbb4eb1ff40054e11e621f85df5bf"
COMPILER_BLOB = "9ead98d5735474d1fd35b101a1f4d50426b7e943"
SOURCE_HEAD = "4d6e4374d6fdda7df72ddeb19dd6756353383346"
TARIFF_PATH = "research/p104-coupled-helper-bases/local.py"
TARIFF_SHA = "5f0678c768544517780d3511995faf0d7062748e7e780c0adb5c4d9c2749a925"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "DUPLICATE_JSON_KEY")
        result[key] = value
    return result


def checked_source(raw):
    need(sha256(raw).hexdigest() == COMPILER_SHA, "COMPILER_SOURCE_BYTES")
    blob = b"blob " + str(len(raw)).encode() + b"\0" + raw
    need(sha1(blob).hexdigest() == COMPILER_BLOB, "COMPILER_GIT_BLOB")
    return raw


def load_compiler(raw):
    namespace = {"__name__": "audited_compiler"}
    exec(compile(raw, "authenticated-PR6280-compiler.py", "exec"), namespace)
    return namespace


def bindings():
    origin = json.loads((HERE / "ORIGIN.json").read_bytes(), object_pairs_hook=no_duplicates)
    need(origin["source_head"] == SOURCE_HEAD and origin["source_pr"] == 6280
         and origin["source_path"] == "research/division-free-dual-exchange/compiler.py"
         and origin["local_path"] == "source/compiler.py"
         and origin["sha256"] == COMPILER_SHA and origin["git_blob"] == COMPILER_BLOB,
         "COMPILER_ORIGIN")
    compiler = checked_source((HERE / "source/compiler.py").read_bytes())
    tariff = (ROOT / TARIFF_PATH).read_bytes()
    need(sha256(tariff).hexdigest() == TARIFF_SHA, "TARIFF_SOURCE_BYTES")
    return compiler, tariff


def price_coefficient(value):
    """Count the actual tariff by repeated division, with no bit methods."""
    q = Q(value)
    numerator, denominator = abs(q.numerator), q.denominator
    need(numerator > 0, "NONZERO_ADD_PRICE")
    digits = ones = exponent = 0
    while numerator:
        numerator, remainder = divmod(numerator, 2)
        digits += 1
        ones += remainder
    while denominator > 1:
        denominator, remainder = divmod(denominator, 2)
        need(remainder == 0, "DYADIC_ADD_PRICE")
        exponent += 1
    return 2 * (2 + digits + ones + exponent)


def price(operations):
    total = 0
    for op, target, source, q in operations:
        if op == "ADD":
            need(target != source, "DISTINCT_ADD_ROLES")
            total += price_coefficient(q)
        else:
            need((op, target == source, q) == ("SCALE", True, -1), "SIGN_SCALE_ONLY")
            total += 2
    return total


def source_tariff_expression(raw):
    matches = []
    for node in ast.walk(ast.parse(raw)):
        if isinstance(node, ast.AugAssign) and isinstance(node.target, ast.Name):
            if node.target.id == "scalar" and "bit_count" in ast.dump(node.value):
                matches.append(node.value)
    need(len(matches) == 1, "UNIQUE_SOURCE_ADD_TARIFF")
    return compile(ast.Expression(matches[0]), "source-ADD-tariff", "eval")


def literal(operations, inputs):
    values = list(map(Q, inputs))
    for op, target, source, q in operations:
        need(0 <= target < len(values) and 0 <= source < len(values), "ROLE_RANGE")
        if op == "ADD":
            need(target != source, "DISTINCT_ADD_ROLES")
            values[target] += q * values[source]
        else:
            need(op == "SCALE" and target == source and q == -1, "SIGN_SCALE_ONLY")
            values[target] = -values[target]
    return values


def check_emitter(module, a, b, tariff):
    """Secondary code regression; the universal free-block proof is separate."""
    a, b = list(map(Q, a)), list(map(Q, b))
    n = len(a)
    need(sum(x * y for x, y in zip(a, b)) == 1, "FIXTURE_DUALITY")
    costs = {}
    for repeat in ("a", "b", "cheapest"):
        ops = module["compile_exchange"](a, b, repeat)
        ca = sum(price_coefficient(q) for q in a if q)
        cb = sum(price_coefficient(q) for q in b if q)
        expected_cost = {"a": 2 + 2 * ca + cb, "b": 2 + ca + 2 * cb,
                         "cheapest": 2 + min(2 * ca + cb, ca + 2 * cb)}[repeat]
        need(price(ops) == expected_cost, "EMITTER_TARIFF")
        need(module["allowance"](ops) == expected_cost, "SOURCE_ALLOWANCE")
        for op, _, _, q in ops:
            if op == "ADD":
                source_cost = eval(tariff, {"__builtins__": {}},
                                   {"n": abs(q.numerator), "d": q.denominator})
                need(source_cost == price_coefficient(q), "ACTUAL_CALLER_TARIFF")
        permitted = set(a + b + [-q for q in a + b] + [Q(-1)])
        need(all(q in permitted for _, _, _, q in ops), "NO_NEW_COEFFICIENTS")
        alpha, beta = 1 + sum(map(abs, a)), 1 + sum(map(abs, b))
        actual_repeat = repeat if repeat != "cheapest" else ("a" if ca < cb else "b")
        envelope = alpha * alpha * beta if actual_repeat == "a" else alpha * beta * beta
        columns = [[Q(i == j) for i in range(n + 1)] for j in range(n + 1)]
        for step in ops:
            columns = [literal([step], c) for c in columns]
            need(max(sum(abs(c[i]) for c in columns) for i in range(n + 1)) <= envelope,
                 "PREFIX_ENVELOPE")
        expected = [[Q(i == j) - b[i] * a[j] for i in range(n)] + [a[j]]
                    for j in range(n)] + [b + [Q(0)]]
        need(columns == expected, "EMITTER_BOUNDARY")
        repeated, single = (a, b) if actual_repeat == "a" else (b, a)
        count = 2 * sum(q != 0 for q in repeated) + sum(q != 0 for q in single) + 1
        need(len(ops) == count, "EMITTER_GATE_COUNT")
        costs[repeat] = expected_cost
    return costs["cheapest"]


def sequence(ops, inputs, functions, fused):
    values = list(map(Q, inputs))
    if fused:
        values = literal(ops, values)
    for fn in functions:
        if not fused:
            values = literal(ops, values)
        values[-1] = fn(values[-1])
        if not fused:
            values = literal(ops, values)
    if fused:
        values = literal(ops, values)
    return values


def functional_evidence(module):
    a, b = list(map(Q, [3, 5])), list(map(Q, [2, -1]))
    ops = module["compile_exchange"](a, b)
    functions = (lambda t: t * t + 1, lambda t: abs(t) - 2, lambda t: t * t - t)
    cases = 0
    for x0, x1, z in product(range(-2, 3), range(-2, 3), (-3, 0, 2)):
        original = [Q(x0), Q(x1), Q(z)]
        for count in (1, 2, 3):
            naive = sequence(ops, original, functions[:count], False)
            fused = sequence(ops, original, functions[:count], True)
            ax = 3 * original[0] + 5 * original[1]
            used = ax
            for fn in functions[:count]:
                used = fn(used)
            target = [original[i] + b[i] * (used - ax) for i in range(2)] + [original[-1]]
            need(naive == fused == target, "NONLINEAR_FUSION")
            cases += 1
    need((len(ops), price(ops)) == (7, 64), "NAMED_SOURCE_TARIFF")
    return {"nonlinear_dirty_input_cases": cases,
            "three_call_scalar_gates": {"separate": 42, "fused": 14},
            "three_call_scalar_allowance": {"separate": 384, "fused": 128},
            "native_or_other_function_calls_retained": 3}


def observer_evidence(module):
    """Finite corroboration of the separately proved universal observer class."""
    ops = module["compile_exchange"]([3, 5], [2, -1])
    functions = (lambda t: t, lambda t: t * t + 1, lambda t: Q(0))
    linear_count = nonlinear_count = 0
    for x0, x1, z in product(range(-2, 3), repeat=3):
        for fn in functions:
            internal = literal(ops, [x0, x1, z])
            internal[-1] = fn(internal[-1])
            returned = literal(ops, internal)
            for c0, c1 in ((1, 0), (0, 1), (3, 5), (-2, 7)):
                d = 2 * c0 - c1
                left = c0 * internal[0] + c1 * internal[1] + d * internal[2]
                right = c0 * returned[0] + c1 * returned[1] + d * returned[2]
                need(left == right, "INVARIANT_LINEAR_OBSERVER")
                linear_count += 1
            left = (3 * internal[0] + 5 * internal[1]) * internal[2]
            right = (3 * returned[0] + 5 * returned[1]) * returned[2]
            need(left == right, "INVARIANT_NONLINEAR_OBSERVER")
            nonlinear_count += 1
    internal = literal(ops, [1, 0, 7])
    internal[-1] += 1
    returned = literal(ops, internal)
    # C=(1,0), D=3 differs from CB=2 and distinguishes these actual states.
    need(internal[0] + 3 * internal[2] != returned[0] + 3 * returned[2],
         "NONINVARIANT_OBSERVER_NOT_DISTINGUISHED")
    swap = module["compile_exchange"]([1], [1])
    for z in range(-2, 3):
        internal = literal(swap, [1, z])
        internal[-1] = Q(0)
        returned = literal(swap, internal)
        need(internal[0] * internal[1] ** 2 == returned[0] * returned[1] ** 2 == 0,
             "FIXED_MAP_REACHABLE_OBSERVER")
    need(1 * 2 ** 2 != 2 * 1 ** 2, "FIXED_MAP_NOT_GLOBAL_INVARIANCE")
    return {"linear_observation_comparisons": linear_count,
            "nonlinear_observation_comparisons": nonlinear_count,
            "observer_scope_discriminators": 2,
            "contract": "O composed with S equals O universally; linear D=CB",
            "all_observation_costs_retained": True}


def expect_reject(action, expected):
    try:
        action()
    except ValueError as exc:
        need(str(exc) == expected, "WRONG_CONTROL_REASON:" + str(exc))
        return 1
    raise ValueError("CONTROL_ACCEPTED:" + expected)


def controls(module, raw, tariff):
    rejected = expect_reject(lambda: checked_source(raw + b"\n"), "COMPILER_SOURCE_BYTES")
    mutations = [
        (b"return upper + negative + upper + sign", b"return upper + negative + upper", "EMITTER_TARIFF"),
        (b"return sign + lower + negative + lower", b"return lower + sign + negative + lower", "EMITTER_BOUNDARY"),
        (b'"a" if a_cost < b_cost else "b"', b'"a" if a_cost > b_cost else "b"', "EMITTER_TARIFF"),
    ]
    for before, after, reason in mutations:
        need(raw.count(before) == 1, "UNIQUE_SOURCE_MUTATION")
        changed = load_compiler(raw.replace(before, after))
        rejected += expect_reject(lambda: check_emitter(changed, [3, 5], [2, -1], tariff), reason)
    incoming = module["compile_exchange"]([1, 0], [1, 0])
    outgoing_b = module["compile_exchange"]([1, 0], [1, 1])
    leaked = literal(outgoing_b, literal(incoming, [0, 0, 1]))
    need(leaked == [0, -1, 1], "MISMATCHED_B_COUNTEREXAMPLE")
    outgoing_a = module["compile_exchange"]([1, 1], [1, 0])
    changed_spare = literal(outgoing_a, literal(incoming, [0, 1, 0]))
    need(changed_spare == [-1, 1, 1], "MISMATCHED_A_COUNTEREXAMPLE")
    ops = module["compile_exchange"]([3, 5], [2, -1])
    at_use = literal(ops, [1, 0, 7])
    at_use[-1] += 1
    logical_boundary = literal(ops, at_use)
    need(at_use == [9, -4, 4] and logical_boundary == [3, -1, 7], "OBSERVER_COUNTEREXAMPLE")
    huge = module["compile_exchange"]([2**63, 1], [0, 1])
    need(any(abs(q) + 1 >= 2**16 for _, _, _, q in huge), "CALLER_CAP_DISTINCTION")
    invalid = [([], []), ([1], [0]), ([Q(1, 3)], [3]), ([True], [1]),
               ([Q(1, 2**33)], [2**33])]
    reasons = ["Matching bounded dimensions", "Dual pairing equals one", "Bounded dyadic denominator",
               "Exact coefficients", "Bounded dyadic denominator"]
    for (a, b), reason in zip(invalid, reasons):
        rejected += expect_reject(lambda a=a, b=b: module["compile_exchange"](a, b), reason)
    return {"exact_reason_rejections": rejected, "boundary_discriminators": 4,
            "mismatched_column_output": list(map(str, leaked)),
            "mismatched_row_output": list(map(str, changed_spare)),
            "fused_after_first_use": list(map(str, at_use)),
            "separate_after_first_consumer": list(map(str, logical_boundary))}


def main():
    raw, tariff_source = bindings()
    module = load_compiler(raw)
    tariff = source_tariff_expression(tariff_source)
    nc = runpy.run_path(str(HERE / "noncommutative.py"))["check"]()
    requests = 0
    for n in range(1, 17):
        for k in range(8):
            if n == 1:
                a, b = [Q(2**k)], [Q(1, 2**k)]
            else:
                b = [Q(1)] + [Q((i + k) % 5 - 2, 2**(k % 3)) for i in range(1, n)]
                a = [Q(0)] + [Q((2 * i + k) % 7 - 3, 2**((k + 1) % 3)) for i in range(1, n)]
                a[0] = 1 - sum(a[i] * b[i] for i in range(1, n))
            check_emitter(module, a, b, tariff)
            requests += 1
    for a, b in [([3, 5], [2, -1]), ([2**63, 1], [0, 1]), ([Q(1, 2**32)], [2**32])]:
        check_emitter(module, a, b, tariff)
        requests += 1
    result = {"status": "PASS_DUAL_EXCHANGE_FUSION_AUDIT", "certificate": nc,
              "emitter_requests": requests, "emitter_factorizations": 3 * requests,
              "functional": functional_evidence(module), "controls": controls(module, raw, tariff),
              "observers": observer_evidence(module),
              "source_head": SOURCE_HEAD, "source_sha256": COMPILER_SHA,
              "tariff_sha256": TARIFF_SHA,
              "scope": "Closed macro only; no actual P104 cut, supplier, rounded analysis or new kappa."}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
