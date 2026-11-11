"""Check the new kernel and unchanged complete caller. Apache-2.0."""

import hashlib
import itertools
import json
from pathlib import Path

import importlib.util

HERE = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load verification module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require(value, message):
    if not value:
        raise RuntimeError(message)


def rejected(action):
    try:
        action()
    except ValueError:
        return 1
    raise RuntimeError("invalid input was accepted")


def small_checks(source, kernel):
    comparisons = arithmetic = controls = 0
    fields = [(2, (0, 1)), (3, (0, 1)), (2, (1, 1, 1)),
              (2, (1, 1, 0, 1)), (3, (1, 0, 1)),
              (2, (1, 1, 0, 0, 1)), (5, (2, 0, 1))]
    for p, modulus in fields:
        field = source.Field(p, modulus)
        engine = kernel.RowKernel(field)
        for c, x, y in itertools.product(range(field.q), repeat=3):
            require(engine.updates[c][x][y] == field.add[x][field.mul[c][y]], "fused arithmetic")
            arithmetic += 1
        shapes = [(0, 0), (1, 1), (3, 4), (7, 18), (9, 9)]
        for height, size in shapes:
            matrix = [[(3*i + 7*j + i*j) % field.q for j in range(size)]
                      for i in range(height)]
            for width in range(min(size, 9) + 1):
                before = [row[:] for row in matrix]
                result = engine.rref(matrix, width)
                require(result == source.rref(matrix, width, field), "rectangular rows differ")
                require(matrix == before, "input mutation")
                if height:
                    result[0][0].append(0)
                    require(matrix == before, "input alias")
                comparisons += 1
        if field.q <= 4:
            for flat in itertools.product(range(field.q), repeat=6):
                matrix = [list(flat[:3]), list(flat[3:])]
                for width in range(4):
                    require(engine.rref(matrix, width) == source.rref(matrix, width, field), "exhaustive rows differ")
                    comparisons += 1
        for matrix, width in [([[field.q]], 1), ([[True]], 1), ([[0], []], 1),
                              ([[0]], 2), ([], -1), ([], True), ([], 163),
                              ([[0] * 163], 1), ([[]] * 730, 0)]:
            controls += rejected(lambda: engine.rref(matrix, width))
    return comparisons, arithmetic, controls


def boundary_checks(source, kernel):
    field = source.Field(2, (0, 1))
    engine = kernel.RowKernel(field)
    matrix = [[int(j == i % 9) for j in range(162)] for i in range(729)]
    require(engine.rref(matrix, 162) == source.rref(matrix, 162, field), "capacity boundary")
    controls = rejected(lambda: kernel.RowKernel(source.Field(29, (0, 1))))
    original = engine.updates
    altered = [[list(row) for row in table] for table in original]
    altered[1][1][1] = 1
    engine.updates = tuple(tuple(tuple(row) for row in table) for table in altered)
    require(engine.rref([[1, 1], [1, 1]], 2) != source.rref([[1, 1], [1, 1]], 2, field), "arithmetic mutant survived")
    controls += 1
    return controls


def main():
    replay = load("row_replay", HERE / "replay.py")
    replay.authenticate()
    source = load("original_recognizer", replay.ROOT / "research/extension-field-tensor-recognition/recognize.py")
    kernel = load("row_kernel", HERE / "kernel.py")
    benchmark = load("row_benchmark", HERE / "benchmark.py")
    comparisons, arithmetic, controls = small_checks(source, kernel)
    controls += boundary_checks(source, kernel)
    runs = [benchmark.run_once(mode, optimized=not __debug__)
            for mode in ("original", "prepared")]
    require(runs[0]["output_sha256"] == runs[1]["output_sha256"], "complete reports differ")
    hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(HERE.iterdir()) if p.is_file()}
    print(json.dumps({"status": "PASS_EXTENSION_FIELD_ROW_KERNEL",
                      "row_comparisons": comparisons + 1, "field_operations": arithmetic,
                      "controls": controls, "complete_runs": runs, "hashes": hashes}, sort_keys=True))


if __name__ == "__main__":
    main()
