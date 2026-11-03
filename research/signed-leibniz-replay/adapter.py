"""Run the complete pinned capacity caller, changing only its determinant evaluator."""

import contextlib
import hashlib
import importlib.util
from importlib.machinery import SourceFileLoader
import io
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "research/dyadic-helper-channel-capacity"
sys.path.insert(0, str(HERE))
from kernel import determinant


def authenticate():
    manifest = json.loads((HERE / "SOURCES.json").read_text())
    if len(manifest["files"]) > 16:
        raise ValueError("source manifest exceeds its fixed capacity")
    for pin in manifest["files"]:
        if pin["usage"] != "input":
            continue
        path = ROOT / pin["path"]
        if path.stat().st_size > 1_000_000:
            raise ValueError("source input exceeds its fixed capacity")
        if hashlib.sha256(path.read_bytes()).hexdigest() != pin["sha256"]:
            raise ValueError("source hash mismatch: " + pin["path"])


class SourceOnlyLoader(SourceFileLoader):
    """Authenticate source rather than executing an unrelated cached bytecode file."""

    def get_code(self, fullname):
        path = self.get_filename(fullname)
        return self.source_to_code(self.get_data(path), path)


def load_source(name, path):
    spec = importlib.util.spec_from_file_location(name, path, loader=SourceOnlyLoader(name, str(path)))
    if spec is None or spec.loader is None:
        raise ValueError("missing caller source loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_caller():
    """Read both authenticated modules directly from source, bypassing bytecode."""
    authenticate()
    old_capacity = sys.modules.pop("capacity", None)
    try:
        sys.modules["capacity"] = load_source("capacity", SOURCE / "capacity.py")
        module = load_source("capacity_caller", SOURCE / "verify.py")
    finally:
        sys.modules.pop("capacity", None)
        if old_capacity is not None:
            sys.modules["capacity"] = old_capacity
    return module


def run(engine):
    caller = load_caller()
    reference = caller.det
    digest = hashlib.sha256()
    dimensions = [0] * 6

    def compared(matrix):
        expected = reference(matrix)
        actual = determinant(matrix)
        if actual != expected:
            raise ValueError("determinant disagreement")
        n = len(matrix)
        dimensions[n] += 1
        digest.update((repr((matrix, actual)) + "\n").encode())
        return actual

    if engine == "scheduled":
        caller.det = determinant
    elif engine == "compare":
        caller.det = compared
    elif engine != "reference":
        raise ValueError("unknown determinant engine")
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        caller.main()
    return output.getvalue(), {"dimensions": dimensions, "sha256": digest.hexdigest()}


def main():
    args = sys.argv[1:]
    if args not in ([], ["--engine", "reference"], ["--engine", "scheduled"], ["--engine", "compare"]):
        raise ValueError("usage: adapter.py [--engine reference|scheduled|compare]")
    engine = args[1] if args else "scheduled"
    output, trace = run(engine)
    print(output, end="")
    if engine == "compare":
        print(json.dumps(trace, sort_keys=True))


if __name__ == "__main__":
    main()
