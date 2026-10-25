#!/usr/bin/env python3
"""Rejecting controls for the serializer-cut comparison."""

import importlib.util
from pathlib import Path

PATH = Path(__file__).resolve().parent / "verify.py"
SPEC = importlib.util.spec_from_file_location("serializer_cut", PATH)
cut = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cut)


def require_failure(name, fn):
    try:
        fn()
    except SystemExit:
        return
    raise SystemExit("control accepted a bad instance: " + name)


def main():
    if cut.D(63) != 0 or cut.D(64) != 1:
        raise SystemExit("depth samples moved")
    if cut.D(1 << 26050) != 42857:
        raise SystemExit("full-copy depth is no longer 42857")
    if cut.D(1 << 26050) <= 26041:
        raise SystemExit("full root copies no longer exceed 26041")
    if 4 * (4 + 13 + 12) + (1 + 3 + 12) != 132:
        raise SystemExit("per-level invoice arithmetic moved")
    cut.assert_child_is_capsule(4 * cut.CHILD_CAPSULE, 4 * cut.ROOT_PACKET)
    require_failure(
        "child recopies the root packet",
        lambda: cut.assert_child_is_capsule(4 * cut.ROOT_PACKET, 4 * cut.ROOT_PACKET),
    )
    require_failure(
        "child length is not the adopted capsule",
        lambda: cut.assert_child_is_capsule(32, 4 * cut.ROOT_PACKET),
    )
    require_failure(
        "root length is not the root packet",
        lambda: cut.assert_child_is_capsule(4 * cut.CHILD_CAPSULE, 4 * cut.CHILD_CAPSULE),
    )
    print("PASS_PR2809_SERIALIZER_CUT_CONTROLS")


if __name__ == "__main__":
    main()
