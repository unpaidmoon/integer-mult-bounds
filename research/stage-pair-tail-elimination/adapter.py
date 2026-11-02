"""Source-bound complete stage-pair caller, produced by Nick Petalas. Apache-2.0."""

import argparse
import dis
from functools import lru_cache
import hashlib
import importlib.abc
import importlib.util
import json
from pathlib import Path
import sys

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def authenticate():
    manifest = json.loads((PACKAGE / "SOURCES.json").read_text())
    modules = {}
    for pin in manifest["files"]:
        if pin["usage"] != "input":
            continue
        path = ROOT / pin["path"]
        data = path.read_bytes()
        require(hashlib.sha256(data).hexdigest() == pin["sha256"], "changed source: " + pin["path"])
        if path.suffix == ".py":
            modules[path.stem] = (path, data)
    require(len(modules) == 13, "source module closure")
    return modules


class SourceLoader(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    """Compile the authenticated dependency bytes with source assertions enabled."""

    def __init__(self, modules):
        self.modules = modules

    def find_spec(self, fullname, path=None, target=None):
        if fullname in self.modules:
            return importlib.util.spec_from_loader(fullname, self)
        return None

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        path, data = self.modules[module.__name__]
        module.__file__ = str(path)
        exec(compile(data, str(path), "exec", optimize=0), module.__dict__)


def reference_observer(original, counts):
    code = original.__wrapped__.__code__
    products = [instruction.offset for instruction in dis.get_instructions(code)
                if instruction.opname == "BINARY_OP" and instruction.argrepr == "*"]
    require(len(products) == 3, "reference multiplication instrumentation")
    # The first multiplication converts inputs. The other two update rows.
    offsets = frozenset(products[1:])

    def observe(frame, event, argument):
        if frame.f_code is not code:
            return None
        if event == "call":
            frame.f_trace_opcodes = True
        elif event == "opcode" and frame.f_lasti in offsets:
            counts["observed_full_products"] += 1
        return observe

    def checked(matrix, prime):
        previous = sys.gettrace()
        require(previous is None, "reference observer needs an untraced child")
        caller = sys._getframe()
        prior_opcodes = caller.f_trace_opcodes
        # CPython 3.12 enables opcode delivery only if a frame requests it
        # before settrace is installed.
        caller.f_trace_opcodes = True
        sys.settrace(observe)
        try:
            return original(matrix, prime)
        finally:
            sys.settrace(previous)
            caller.f_trace_opcodes = prior_opcodes

    return checked


def complete(engine):
    modules = authenticate()
    require(not any(name in sys.modules for name in modules), "caller must start in a fresh process")
    loader = SourceLoader(modules)
    sys.meta_path.insert(0, loader)
    counts = {"full_products": 0, "tail_products": 0, "kernel_calls": 0,
              "observed_full_products": 0}
    try:
        import audit_stage_pair as source
        from prepare_layers import serializable
        if engine != "reference":
            namespace = {}
            path = PACKAGE / "kernel.py"
            exec(compile(path.read_bytes(), str(path), "exec", optimize=0), namespace)
            original = source.modular_rank
            reference = reference_observer(original, counts) if engine == "compare" else original

            @lru_cache(maxsize=65536)
            def replacement(matrix, prime=101):
                answer = namespace["tail_rank"](
                    matrix, prime, source._mod_inv, counts if engine == "compare" else None)
                if engine == "compare":
                    require(answer == reference(matrix, prime), "live modular rank disagreement")
                return answer

            source.modular_rank = replacement
        result = serializable(source.certificate())
        cache = source.modular_rank.cache_info()
        if engine == "compare":
            require(counts["observed_full_products"] == counts["full_products"],
                    "reference arithmetic count disagreement")
        return result, counts, cache._asdict()
    finally:
        sys.meta_path.remove(loader)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", choices=("reference", "tail", "compare"), required=True)
    args = parser.parse_args()
    result, counts, cache = complete(args.engine)
    print(json.dumps({"payload": result, "counts": counts, "cache": cache},
                     sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
