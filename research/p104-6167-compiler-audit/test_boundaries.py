#!/usr/bin/env python3
"""Actual CLI rejection tests on a temporary Git-free source export.

Prepared for @CubeJerry with substantial OpenAI Codex assistance. Apache-2.0.
"""
from hashlib import sha256
from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PACKAGE = HERE.relative_to(ROOT)


def require(ok, reason):
    if not ok:
        raise SystemExit("FAIL_BOUNDARY_CONTROL: " + reason)


def main():
    manifest = json.loads((HERE / "VERIFY.json").read_text(encoding="utf-8"))
    inputs = manifest["inputs"]
    original = {p: (ROOT / p).read_bytes() for p in inputs}
    with tempfile.TemporaryDirectory(prefix="p104-compiler-controls-") as temp:
        root = Path(temp)
        package = root / PACKAGE
        package.mkdir(parents=True)
        for name in ("verify.py", "VERIFY.json", "SOURCES.json", "RESULT.json"):
            shutil.copyfile(HERE / name, package / name)
        for name, data in original.items():
            dest = root / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
        env = dict(os.environ, PATH="")
        env.pop("PYTHONOPTIMIZE", None)
        argv = [sys.executable, "-I", "-B"]
        if sys.flags.optimize:
            argv.append("-O")
        argv.append(str(package / "verify.py"))

        def invoke(reason=None):
            result = subprocess.run(argv, cwd=root, env=env, capture_output=True,
                                    text=True, timeout=60, check=False)
            if reason is None:
                require(result.returncode == 0 and "PASS_P104_6167_COMPILER_AUDIT" in result.stdout,
                        "positive export: " + result.stderr[-500:])
            else:
                require(result.returncode != 0 and reason in result.stderr,
                        "expected " + reason + "; got " + result.stderr[-500:])
                require("PASS_P104_6167_COMPILER_AUDIT" not in result.stdout,
                        "failure printed success")

        invoke()
        for name, data in original.items():
            path = root / name
            path.write_bytes(data + b"\n")
            invoke("source_hash:" + name)
            path.write_bytes(data)
        receipt = package / "RESULT.json"
        saved = receipt.read_bytes()
        mutated = json.loads(saved)
        mutated["parameters"]["H"] += 1
        receipt.write_text(json.dumps(mutated), encoding="utf-8")
        invoke("receipt_matches_recomputation")
        receipt.write_bytes(saved)
        require(all(sha256((root / p).read_bytes()).digest() == sha256(data).digest()
                    for p, data in original.items()), "controls restored their temporary inputs")
    print(json.dumps({"status": "PASS_P104_COMPILER_BOUNDARIES",
                      "git_free_positive": 1, "source_byte_rejections": len(inputs),
                      "receipt_rejections": 1, "optimized": bool(sys.flags.optimize)}, sort_keys=True))


if __name__ == "__main__":
    main()
