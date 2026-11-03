"""Authenticated baseline/current modules. Produced by Nick Petalas. Apache-2.0."""

import hashlib
from pathlib import Path
import sys
import types

BASELINE_SHA = "b2e69c54f3114f201fa2deacf3370a3d8dcd0b854f6cb4497ae4f315d9a63b1e"
CURRENT_SHA = "ea77f4b29452ad71612d9ff773d10bfb003eb774232106f10b1e875497f1075a"
HELPER_SHA = "3930c22c11da7bc6042cfeb6e459ecb06e4478430037bee3469d034353855fc6"
GUARD = b"            if rows[i][k] == 0:\n                continue\n"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def authenticate(current, helper):
    need(len(current) <= 262144 and len(helper) <= 262144, "bounded source bytes")
    need(hashlib.sha256(current).hexdigest() == CURRENT_SHA, "current source changed")
    need(hashlib.sha256(helper).hexdigest() == HELPER_SHA, "helper source changed")
    need(current.count(GUARD) == 1, "one exact zero guard")
    baseline = current.replace(GUARD, b"", 1)
    need(hashlib.sha256(baseline).hexdigest() == BASELINE_SHA, "baseline reconstruction changed")
    return baseline


def sources():
    root = Path(__file__).resolve().parents[2]
    payloads = []
    for name in ("certify_coupled_recurrence.py", "compare_recursive_invoices.py"):
        path = root / "scripts" / name
        need(not path.is_symlink() and path.stat().st_size <= 262144, "bounded source file")
        payloads.append(path.read_bytes())
    current, helper = payloads
    return authenticate(current, helper), current, helper


def module_from_bytes(source, name):
    module = types.ModuleType(name)
    module.__file__ = name + ".py"
    exec(compile(source, module.__file__, "exec"), module.__dict__)
    return module


def versions():
    baseline, current, helper = sources()
    previous = sys.modules.get("compare_recursive_invoices")
    try:
        sys.modules["compare_recursive_invoices"] = module_from_bytes(helper, "compare_recursive_invoices")
        old = module_from_bytes(baseline, "coupled_baseline")
        new = module_from_bytes(current, "coupled_current")
    finally:
        if previous is None:
            sys.modules.pop("compare_recursive_invoices", None)
        else:
            sys.modules["compare_recursive_invoices"] = previous
    return old, new


def chain_problem(size=64):
    need(type(size) is int and 1 <= size <= 64, "chain size")
    return {"schema": "coupled-recurrence/v1",
            "matrix": [["1/2" if i + 1 == j else "0" for j in range(size)]
                       for i in range(size)], "forcing": ["1"] * size}
