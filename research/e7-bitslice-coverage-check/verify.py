#!/usr/bin/env python3
"""Independent coverage check for the E7 bit-lane iterator.

The half-split census does not call low_weight_words, full_weight_census, or
the Gray-code support loop. It lists each half of an independent basis by
doubling, then scores hw XOR lw by integer popcount.
"""

import json
from hashlib import sha256
from pathlib import Path
from runpy import run_path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
WIDTH = 63
DIMENSION = 27
WEIGHT_BOUND = 12


def need(condition, message):
    if not condition:
        raise ValueError(message)


def authenticate():
    sources = json.loads((HERE / "SOURCES.json").read_text(encoding="utf-8"))
    checked = 0
    for row in sources["files"]:
        if row["usage"] != "input":
            continue
        path = ROOT / row["path"]
        digest = sha256(path.read_bytes()).hexdigest()
        need(digest == row["sha256"], "input hash mismatch: " + row["path"])
        checked += 1
    need(checked == 4, "four live inputs")
    return checked


def span(generators):
    words = [0]
    for generator in generators:
        words.extend([word ^ generator for word in words])
    need(len(set(words)) == len(words), "half span repeats a word")
    return words


def half_split(basis, maximum, low_dimension):
    """Return words of weight <= maximum, the least positive weight, and span size."""
    need(0 < low_dimension < len(basis), "split must use both halves")
    lows = span(basis[:low_dimension])
    highs = span(basis[low_dimension:])
    distinct = len(lows) * len(highs)
    need(distinct == 1 << len(basis), "halves do not cover the basis span")
    found = set()
    minimum = maximum + 1
    for high in highs:
        for low in lows:
            word = high ^ low
            weight = word.bit_count()
            if word and weight < minimum:
                minimum = weight
            if weight <= maximum:
                found.add(word)
    return found, minimum, distinct


def free_coordinate_identity(basis, free):
    need(len(basis) == len(free) == DIMENSION, "E7 kernel dimension")
    need(len(set(free)) == DIMENSION, "repeated free coordinate")
    for index, vector in enumerate(basis):
        need(0 < vector < 1 << WIDTH, "kernel vector outside F_2^63")
        pattern = tuple((vector >> coordinate) & 1 for coordinate in free)
        identity = tuple(int(place == index) for place in range(DIMENSION))
        need(pattern == identity, "free coordinates are not a basis identity")


def e7_kernel():
    geometry = run_path(
        str(ROOT / "research/e7-bitsliced-exhaustion/source/vendor/PR5238.py"),
        run_name="e7_coverage_geometry",
    )
    roots = geometry["intrinsic_e7"]()
    frames = geometry["orthogonal_frames"](roots)
    rows = tuple(sum(1 << index for index in frame) for frame in frames)
    basis, free = geometry["binary_kernel"](rows)
    free_coordinate_identity(basis, free)
    need(len(frames) == 135 and len(rows) == 135, "frame count")
    return basis, free, len(frames)


def engine_words(engine, basis, width, maximum, batch_bits):
    listed = list(engine(basis, width, maximum, batch_bits))
    need(len(listed) == len(set(listed)), "engine repeated a word")
    return set(listed)


def toy_controls(engine):
    basis = (1, 2, 4)
    literal = span(basis)
    expected = {word for word in literal if word.bit_count() <= 1}
    found, minimum, distinct = half_split(basis, 1, 2)
    need(found == expected == {0, 1, 2, 4}, "toy weight-1 set")
    need(minimum == 1 and distinct == 8, "toy minimum or span")
    need(engine_words(engine, basis, 3, 1, 3) == found, "toy engine mismatch")
    zero_only = engine_words(engine, basis, 3, 0, 3)
    need(zero_only == {0} and zero_only != found, "toy bound change was ignored")
    other, other_minimum, _ = half_split(basis, 1, 1)
    need(other == found and other_minimum == 1, "toy split point changed the set")
    return 5


def receipt_counts():
    receipt = json.loads(
        (ROOT / "research/e7-bitsliced-exhaustion/source/RESULT.json").read_text(
            encoding="utf-8"
        )
    )
    need(receipt["binary_dimension"] == DIMENSION, "receipt dimension")
    need(receipt["binary_rank"] == 36, "receipt rank")
    need(receipt["frames"] == 135, "receipt frames")
    need(receipt["minimum_support"] == WEIGHT_BOUND, "receipt minimum")
    need(receipt["minimum_supports"] == 1638, "receipt support count")
    need(receipt["nonzero_codewords"] == (1 << DIMENSION) - 1, "receipt nonzero count")
    return receipt


def positive_words_have_weight(words, weight):
    return all(word.bit_count() == weight for word in words if word)


def check():
    authenticate()
    receipt = receipt_counts()
    engine = run_path(
        str(ROOT / "research/e7-bitsliced-exhaustion/binary.py"),
        run_name="e7_coverage_engine",
    )["low_weight_words"]
    toy = toy_controls(engine)
    basis, free, frames = e7_kernel()
    splits = {}
    for low_dimension in (13, 16):
        found, minimum, distinct = half_split(basis, WEIGHT_BOUND, low_dimension)
        splits[low_dimension] = (found, minimum, distinct)
    left, right = splits[13], splits[16]
    need(left[0] == right[0], "two basis splits disagree")
    need(left[1] == right[1] == WEIGHT_BOUND, "minimum left twelve")
    need(left[2] == right[2] == 1 << DIMENSION, "span missed a codeword")
    found = left[0]
    supports = found - {0}
    need(0 in found, "zero word missing")
    need(len(supports) == receipt["minimum_supports"] == 1638, "support count")
    need(positive_words_have_weight(found, WEIGHT_BOUND), "a lighter nonzero word")
    for batch_bits in (16, 8):
        produced = engine_words(engine, basis, WIDTH, WEIGHT_BOUND, batch_bits)
        need(produced == found, "engine batch " + str(batch_bits) + " dropped or added a word")
    witness = next(iter(supports))
    need(engine_words(engine, basis, WIDTH, WEIGHT_BOUND, 16) - {witness} != found,
         "dropping one support still compared equal")
    lighter = witness ^ (1 << (witness.bit_length() - 1))
    need(lighter.bit_count() == WEIGHT_BOUND - 1, "clearing the top bit did not reduce weight")
    need(lighter not in found, "a weight-eleven word was already in the code")
    forged = set(found)
    forged.add(lighter)
    need(not positive_words_have_weight(forged, WEIGHT_BOUND),
         "weight-eleven injection was accepted")
    digest = sha256(json.dumps(sorted(supports)).encode()).hexdigest()
    return {
        "status": "PASS_E7_BITSLICE_COVERAGE_CHECK",
        "minimum_positive_weight": WEIGHT_BOUND,
        "weight_at_most_12": len(found),
        "minimum_supports": len(supports),
        "distinct_codewords": 1 << DIMENSION,
        "nonzero_codewords": (1 << DIMENSION) - 1,
        "splits": [13, 16],
        "engine_batches": [16, 8],
        "supports_sha256": digest,
        "free_coordinates": list(free),
        "frames": frames,
        "toy_controls": toy,
        "orbits_replayed": False,
        "timing_remeasured": False,
        "no_new_kappa": True,
    }


if __name__ == "__main__":
    result = check()
    print(
        "PASS_E7_BITSLICE_COVERAGE_CHECK"
        " minimum={minimum_positive_weight}"
        " supports={minimum_supports}"
        " codewords={distinct_codewords}"
        " batches=16,8"
        " splits=13,16"
        " orbits_replayed=false"
        " no_new_kappa=true".format(**result)
    )
    print(json.dumps(result, indent=2, sort_keys=True))
