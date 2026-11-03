"""Replay exhaustive frame coverage and the three exact spectra. Apache-2.0.

Jerry Chen (@CubeJerry), with OpenAI Codex assistance.
No generator, numerical eigensolver or predecessor executable is imported.
"""
from collections import Counter
from copy import deepcopy
from hashlib import sha256
import json

from geometry import (DIM, FIRST, SECOND, SIZE, WEIGHTS, coordinates, dot,
                      energy_matrix, load_ports, need, package_path, universe)
from orbits import (PERMUTATIONS, QUADRATIC, TYPES, enumerate_frames, orbit,
                    orbit_partition, reflection_actions, stabilizer_actions)
from verify import modular_rank, rejected
from moments import check_moments

QUADRATIC_ACTION = ((796, 0, 0, -68), (0, 796, 68, 0),
                    (0, 68, 660, 0), (-68, 0, 0, 660))


def check_cover(frames, vectors, actions):
    need(len(frames) == 2025, "FRAME_COUNT")
    for frame in frames:
        need(len(frame) == len(set(frame)) == DIM and
             all(dot(vectors[q], vectors[r]) == 0 for i, q in enumerate(frame)
                 for r in frame[i + 1:]), "FRAME_DOMAIN")
    need(orbit(FIRST, reflection_actions(vectors)) == frames, "FRAME_TRANSITIVITY")
    census = Counter(len(set(FIRST) & set(frame)) for frame in frames)
    need(census == {0: 1260, 1: 512, 2: 224, 4: 28, 8: 1}, "INTERSECTION_CENSUS")
    disjoint = {frame for frame in frames if not set(frame) & set(FIRST)}
    classes = orbit_partition(disjoint, actions)
    actual = [(len(group), min(group)) for group in classes]
    need(actual == [(count, frame) for count, frame, _ in TYPES], "ORBIT_CLASSIFICATION")
    need(sum(SECOND in group and len(group) == 896 for group in classes) == 1,
         "SELECTED_ORBIT_MEMBERSHIP")
    histograms = ({0: 16, 4: 12}, {0: 8, 2: 16, 4: 4}, {0: 4, 2: 24})
    for group, expected in zip(classes, histograms, strict=True):
        for frame in group:
            supports = [{i for i, x in enumerate(vectors[q]) if x} for q in frame]
            actual = Counter(len(a & b) for i, a in enumerate(supports)
                             for b in supports[i + 1:])
            need(actual == expected, "SUPPORT_INTERSECTION_INVARIANT")
    return classes


def checked_vector(vector):
    need(isinstance(vector, list) and len(vector) == SIZE and
         all(type(x) is int and abs(x) <= 1000 for x in vector), "ORBIT_VECTOR")


def check_quadratic(block, matrix):
    need(block.get("polynomial") == list(QUADRATIC), "QUADRATIC_POLYNOMIAL")
    basis = block.get("basis")
    need(isinstance(basis, list) and len(basis) == 4, "QUADRATIC_DIMENSION")
    for column, vector in enumerate(basis):
        checked_vector(vector)
        need(sum(vector[:DIM]) == 0, "QUADRATIC_TRACE_ZERO")
        for i in range(SIZE):
            need(dot(matrix[i], vector) == WEIGHTS[i] * sum(
                basis[j][i] * QUADRATIC_ACTION[j][column] for j in range(4)),
                "QUADRATIC_ACTION")
    # The displayed 4x4 rational action has two identical quadratic factors.
    for i in range(4):
        for j in range(4):
            need(sum(QUADRATIC_ACTION[i][k] * QUADRATIC_ACTION[k][j]
                     for k in range(4)) + QUADRATIC[1] * QUADRATIC_ACTION[i][j]
                 + QUADRATIC[2] * int(i == j) == 0, "QUADRATIC_IDENTITY")
    return basis


def check_spectrum(record, matrix, specification):
    count, frame, spectrum = specification
    need(record.get("size") == count, "ORBIT_SIZE")
    need(record.get("representative") == list(frame), "ORBIT_REPRESENTATIVE")
    blocks = record.get("blocks")
    need(isinstance(blocks, list) and len(blocks) == len(spectrum), "ORBIT_BLOCKS")
    columns = []
    for block, (mu, multiplicity) in zip(blocks, spectrum, strict=True):
        need(type(block.get("eigenvalue_times_16")) is int and
             block["eigenvalue_times_16"] == mu, "ORBIT_EIGENVALUE")
        basis = block.get("basis")
        need(isinstance(basis, list) and len(basis) == multiplicity,
             "ORBIT_MULTIPLICITY")
        for vector in basis:
            checked_vector(vector)
            need(all(dot(row, vector) == mu * weight * x
                     for row, weight, x in zip(matrix, WEIGHTS, vector, strict=True)),
                 "ORBIT_EIGENVECTOR_EQUATION")
            need(mu == 0 or sum(vector[:DIM]) == 0, "ORBIT_POSITIVE_TRACE_ZERO")
            need(mu != 0 or vector == [1] * DIM + [0] * (SIZE - DIM),
                 "ORBIT_SCALAR_KERNEL")
            columns.append(vector)
    if count == 336:
        columns.extend(check_quadratic(record.get("quadratic_block", {}), matrix))
    else:
        need("quadratic_block" not in record, "UNEXPECTED_QUADRATIC")
    need(len(columns) == SIZE and modular_rank(columns) == SIZE, "ORBIT_BASIS_COMPLETE")


def check_records(certificate, vectors):
    need(certificate.get("schema") == "p104-disjoint-frame-orbits/1", "ORBIT_SCHEMA")
    need(certificate.get("coordinate_frame") == list(FIRST), "ORBIT_COORDINATE_FRAME")
    need(certificate.get("coordinate_permutations") == [list(p) for p in PERMUTATIONS]
         and certificate.get("sign_flips") == list(range(DIM)), "ORBIT_GENERATORS")
    records = certificate.get("orbits")
    need(isinstance(records, list) and len(records) == 3, "ORBIT_RECORD_COUNT")
    matrices = []
    for record, specification in zip(records, TYPES, strict=True):
        _, frame, _ = specification
        ports = sorted(set(universe()) - set(FIRST) - set(frame))
        matrix, _ = energy_matrix(ports, vectors)
        check_spectrum(record, matrix, specification)
        matrices.append(matrix)
    return matrices


def controls(certificate, matrices, vectors, frames, actions):
    shortened = set(frames)
    shortened.remove(min(frames))
    rejected(lambda: check_cover(shortened, vectors, actions), "FRAME_COUNT")
    rejected(lambda: check_cover(frames, vectors, []), "ORBIT_CLASSIFICATION")
    wrong = (1, 0, 2, 3, 4, 5, 6, 7)
    rejected(lambda: stabilizer_actions(vectors, (wrong,)), "ROOT_CLOSURE")
    altered = deepcopy(certificate["orbits"][0])
    altered["size"] += 1
    rejected(lambda: check_spectrum(altered, matrices[0], TYPES[0]), "ORBIT_SIZE")
    altered = deepcopy(certificate["orbits"][0])
    altered["representative"][0] = FIRST[0]
    rejected(lambda: check_spectrum(altered, matrices[0], TYPES[0]), "ORBIT_REPRESENTATIVE")
    altered = deepcopy(certificate["orbits"][0])
    altered["blocks"][1]["basis"][0][0] += 1
    rejected(lambda: check_spectrum(altered, matrices[0], TYPES[0]),
             "ORBIT_EIGENVECTOR_EQUATION")
    altered = deepcopy(certificate["orbits"][0])
    altered["blocks"][1]["basis"][1] = altered["blocks"][1]["basis"][0]
    rejected(lambda: check_spectrum(altered, matrices[0], TYPES[0]), "ORBIT_BASIS_COMPLETE")
    altered = deepcopy(certificate["orbits"][1])
    altered["quadratic_block"]["polynomial"][2] += 1
    rejected(lambda: check_spectrum(altered, matrices[1], TYPES[1]), "QUADRATIC_POLYNOMIAL")
    altered = deepcopy(certificate["orbits"][1])
    altered["quadratic_block"]["basis"][0][8] += 1
    rejected(lambda: check_spectrum(altered, matrices[1], TYPES[1]), "QUADRATIC_ACTION")
    altered = deepcopy(certificate["orbits"][1])
    altered["quadratic_block"]["basis"].pop()
    rejected(lambda: check_spectrum(altered, matrices[1], TYPES[1]), "QUADRATIC_DIMENSION")
    doubled = [[2 * x for x in row] for row in matrices[2]]
    rejected(lambda: check_spectrum(certificate["orbits"][2], doubled, TYPES[2]),
             "ORBIT_EIGENVECTOR_EQUATION")
    need(QUADRATIC[1] ** 2 - 4 * QUADRATIC[2] == 36992, "QUADRATIC_DISCRIMINANT")
    need(32 ** 2 > 17 ** 2 * 2, "IRRATIONAL_ROOT_ABOVE_SELECTED_MINIMUM")
    return 11


def main():
    package = package_path()
    load_ports(package)
    vectors = coordinates()
    frames = enumerate_frames(vectors)
    actions = stabilizer_actions(vectors)
    classes = check_cover(frames, vectors, actions)
    certificate = json.loads((package / "ORBITS.json").read_bytes())
    matrices = check_records(certificate, vectors)
    count = controls(certificate, matrices, vectors, frames, actions)
    moments = check_moments(vectors)
    files = ("orbits.py", "generate_orbits.py", "verify_orbits.py", "ORBITS.json",
             "ORBIT-PROOF.md", "HERMITIAN-PROOF.md", "moments.py")
    print(json.dumps({"status": "PASS_P104_ALL_DISJOINT_FRAME_ORBITS",
          "frames": len(frames), "disjoint_from_fixed_frame": sum(map(len, classes)),
          "fixed_frame_orbit_sizes": [len(group) for group in classes],
          "selected_orbit_size": 896, "sharp_constants": ["37", "37", "75/2"],
          "rational_eigenvectors_checked": 104, "quadratic_block_dimension": 4,
          "quadratic_eigenvalues": "(182 +/- 17*sqrt(2))/4, each multiplicity 2",
          "negative_controls": count + moments["negative_controls"],
          "hermitian_extension": moments,
          "file_sha256": {name: sha256((package / name).read_bytes()).hexdigest()
                          for name in files}}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
