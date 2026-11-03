"""Read the exact declared predecessor bytes; produced by Nick Petalas."""

from hashlib import sha256
import json
from pathlib import Path
from types import ModuleType

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def authenticate(root=ROOT):
    manifest = json.loads((HERE / "SOURCES.json").read_text())
    pins = {}
    for row in manifest["files"]:
        if row["usage"] == "input":
            path = root / row["path"]
            raw = path.read_bytes()
            actual = sha256(raw).hexdigest()
            if actual != row["sha256"]:
                raise ValueError("source hash mismatch: " + row["path"])
            pins[row["path"]] = actual
    return pins


def load():
    authenticate()
    path = ROOT / "research/five-label-prefix-completion/bounds.py"
    module = ModuleType("retained_prefix_completion")
    exec(compile(path.read_bytes(), str(path), "exec"), module.__dict__)
    return module
