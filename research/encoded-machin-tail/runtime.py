"""Authenticate the live inputs before opening the retained tape runtime."""

from contextlib import contextmanager
from hashlib import sha256
import importlib
import json
from pathlib import Path
import sys
from unittest.mock import patch

from adapter import arctangent

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def authenticate():
    rows = json.loads((HERE / "SOURCES.json").read_text())["files"]
    require(4 <= len(rows) <= 16, "bounded source row inventory")
    require(sum(row["usage"] == "input" for row in rows) == 4, "four live inputs")
    for row in rows:
        if row["usage"] == "input":
            path = ROOT / row["path"]
            require(path.is_file() and not path.is_symlink(), "regular input: " + row["path"])
            require(path.stat().st_size <= 2**27, "bounded input size")
            require(sha256(path.read_bytes()).hexdigest() == row["sha256"],
                    "source hash: " + row["path"])


@contextmanager
def opened():
    authenticate()
    path = ROOT / "research/physical-ring-product"
    old = sys.path[:]
    sys.path.insert(0, str(path))
    try:
        source = importlib.import_module("ring_sources")
        require(Path(source.__file__).resolve() == path / "ring_sources.py", "source module identity")
        with source.opened():
            module = importlib.import_module("twiddle_setup")
            require(Path(module.__file__).resolve() == path / "twiddle_setup.py", "twiddle module identity")
            yield module
    finally:
        sys.path[:] = old


@contextmanager
def selected(module, stop):
    function = arctangent if stop else module.arctangent
    with patch.object(module, "arctangent", function):
        yield
