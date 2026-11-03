"""Run the complete pinned caller with one optional kernel. Apache-2.0."""

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load source module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def authenticate():
    sources = json.loads((HERE / "SOURCES.json").read_text())
    for item in sources["files"]:
        if item["usage"] == "input":
            data = (ROOT / item["path"]).read_bytes()
            if hashlib.sha256(data).hexdigest() != item["sha256"]:
                raise RuntimeError("source bytes changed: " + item["path"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("original", "prepared"))
    args = parser.parse_args()
    authenticate()
    source = ROOT / "research/extension-field-tensor-recognition/verify.py"
    caller = load("complete_extension_caller", source)
    if args.mode == "prepared":
        kernel = load("prepared_row_kernel", HERE / "kernel.py")
        kernel.install(caller.r)
    caller.main()


if __name__ == "__main__":
    main()
