#!/usr/bin/env python3
"""Place L561 on the four half-length scratch windows, or show the word does not.

The tape object is research/qq16-gaussian-axis-tapes/tapes.py (Clear1nsight,
Apache-2.0). This file only reads the pinned forward word and schedules
reads, writes and unit moves.
"""
import gzip
import hashlib
import io
import json
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TAPE_PATH = ROOT / "research" / "qq16-gaussian-axis-tapes" / "tapes.py"
CERTIFICATE = ROOT / "research" / "joint-query" / "certificate.json.gz"
ARCHIVE = ROOT / "research" / "community-frontier1042-audit" / "selected-replay.tar.gz"
CERTIFICATE_SHA = "a5ed85fac5ebf3c091482a113ab0d351eb5a7892fe2841a35e16017ec1ff49f7"
ARCHIVE_SHA = "22c3f4dce4b897a1d423d1388801933e288b6a6b1906cb15e1b16a5eb68db754"
WORD_MEMBER = "slots/local/CANONICAL-WORD.json.gz"
WORD_SHA = "16bc0ebb04b4be6c0ade74badc6a0c0cdba4215eda86e4ff9f13abf8ecebd219"
ADD_INDEX = 9895
ADD = ["scalar", ["add", ["L", 546], ["L", 561], -1, 1], 4]
ADAPTER_INDEX = 7963
ADAPTER = ["residual_adapter", "pre", 561, 4]
LAST_CLEARS = [8185, 8259, 8337, 8412, 8484, 8557, 8628, 8702]


def load_tapes():
    import importlib.util
    spec = importlib.util.spec_from_file_location("qq16_axis_tapes", TAPE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load pinned tape module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


TAPES = load_tapes()
Tape = TAPES.Tape
need = TAPES.need


def encode(values, width):
    lo = -(1 << (width - 1))
    hi = (1 << (width - 1)) - 1
    need(all(type(v) is int and lo <= v <= hi for v in values), "signed input range")
    return [(v >> bit) & 1 for v in values for bit in range(width)]


def decode(cells, width):
    values = []
    for start in range(0, len(cells), width):
        word = sum(cells[start + bit] << bit for bit in range(width))
        values.append(word - ((word >> (width - 1)) << width))
    return values


def rewind(tape, steps):
    for _ in range(steps):
        tape.move(-1)


def counts(tapes):
    read = write = move = 0
    for tape in tapes:
        read += tape.count["read"]
        write += tape.count["write"]
        move += tape.count["move"]
        need(tape.head == tape.origin, "head did not return")
    return read, write, move


def place(real, imag, width, one_past=False, scratch_fill=1):
    """Copy one complex register onto four half-length scratch tapes.

    Home tapes hold real and imaginary parts in coordinate order. Scratch
    receives the split used by research/qq16-l546-head-move: low coordinates
    on scratch 0/1 and high coordinates on scratch 2/3. Heads start and end
    at cell 0. one_past=True is the axis kernel's move-after-every-cell habit.
    """
    n = len(real)
    need(n == len(imag) and n >= 2 and (n & (n - 1)) == 0, "N=2^n, n>=1")
    need(type(width) is int and width >= 1, "component width")
    half = n // 2
    length = n * width
    homes = [
        Tape(encode(real, width), origin=0, trace=False, discardable=False),
        Tape(encode(imag, width), origin=0, trace=False, discardable=False),
    ]
    scratch = [
        Tape([scratch_fill] * (length // 2), origin=0, trace=False, discardable=True)
        for _ in range(4)
    ]
    for comp in range(2):
        home = homes[comp]
        low = scratch[comp]
        high = scratch[2 + comp]
        for coord in range(half):
            for bit in range(width):
                low.write(home.read())
                last = coord == half - 1 and bit == width - 1
                if one_past or not last:
                    home.move(1)
                    low.move(1)
        if not one_past:
            home.move(1)
        for coord in range(half):
            for bit in range(width):
                high.write(home.read())
                last = coord == half - 1 and bit == width - 1
                if one_past or not last:
                    home.move(1)
                    high.move(1)
        if one_past:
            rewind(home, length)
            rewind(low, length // 2)
            rewind(high, length // 2)
        else:
            rewind(home, length - 1)
            rewind(low, length // 2 - 1)
            rewind(high, length // 2 - 1)
    image = [decode(scratch[comp].cells, width) + decode(scratch[2 + comp].cells, width)
             for comp in range(2)]
    need(image == [list(real), list(imag)], "scratch image")
    need(all(tape.head == tape.origin for tape in homes + scratch), "origins")
    bits = tuple(tuple(tape.cells) for tape in scratch)
    return counts(homes + scratch), bits


def subtract_placed(real_a, imag_a, real_b, imag_b, width):
    """Re-meter the already proved L546 -= L561 schedule, to add the bills.

    The sharpness argument for this subtraction is research/qq16-l546-head-move.
    """
    n = len(real_a)
    need(n == len(imag_a) == len(real_b) == len(imag_b), "equal lengths")
    half = n // 2
    length = n * width
    half_bits = half * width
    rows = [
        encode(real_a, width),
        encode(imag_a, width),
        encode(real_b[:half], width),
        encode(imag_b[:half], width),
        encode(real_b[half:], width),
        encode(imag_b[half:], width),
    ]
    tapes = [Tape(row, origin=0, trace=False, discardable=(index >= 2))
             for index, row in enumerate(rows)]
    data0, data1, scratch0, scratch1, scratch2, scratch3 = tapes
    subtract_segment(data0, scratch0, half_bits, width)
    subtract_segment(data1, scratch1, half_bits, width)
    data0.move(1)
    data1.move(1)
    subtract_segment(data0, scratch2, half_bits, width)
    subtract_segment(data1, scratch3, half_bits, width)
    rewind(data0, length - 1)
    rewind(data1, length - 1)
    for tape in (scratch0, scratch1, scratch2, scratch3):
        rewind(tape, half_bits - 1)
    got = [decode(tapes[0].cells, width), decode(tapes[1].cells, width)]
    need(got == [[signed_difference(a, b, width) for a, b in zip(left, right)]
                 for left, right in ((real_a, real_b), (imag_a, imag_b))],
         "subtraction image")
    return counts(tapes)


def signed_difference(left, right, width):
    bits = (left - right) & ((1 << width) - 1)
    if bits >= 1 << (width - 1):
        bits -= 1 << width
    return bits


def subtract_segment(dst, src, nbits, width):
    need(nbits % width == 0 and nbits >= width, "whole coordinates")
    coords = nbits // width
    for coord in range(coords):
        borrow = 0
        for bit in range(width):
            incoming = src.read()
            resident = dst.read()
            diff = resident - incoming - borrow
            dst.write(diff & 1)
            borrow = 1 if diff < 0 else 0
            if bit != width - 1 or coord != coords - 1:
                dst.move(1)
                src.move(1)


def formulas(n, width):
    cells = n * width
    sharp = (2 * cells, 2 * cells, 8 * cells - 12)
    past = (2 * cells, 2 * cells, 8 * cells)
    return sharp, past


def load_checked(path, sha, cap):
    need(path.is_file() and not path.is_symlink(), "source file")
    raw = path.read_bytes()
    need(len(raw) <= cap, "source cap")
    need(hashlib.sha256(raw).hexdigest() == sha, "source sha")
    return raw


def register_id(token):
    if isinstance(token, list) and len(token) == 2 and token[0] in ("L", "C"):
        return token
    return None


def mentions_561(event):
    kind = event[0]
    if kind == "climb":
        return event[2] == 561
    if kind == "scalar":
        gate = event[1]
        return any(register_id(piece) == ["L", 561] or register_id(piece) == ["C", 561]
                   for piece in gate)
    if kind in ("adapter", "residual_adapter"):
        return event[2] == 561
    return False


def word_gap(events):
    kinds = {event[0] for event in events}
    need(kinds == {"phase", "scalar", "adapter", "residual_adapter", "climb"},
         "forward word gained an event kind")
    for event in events:
        kind = event[0]
        if kind == "phase":
            need(len(event) == 2 and isinstance(event[1], str), "phase schema")
        elif kind == "scalar":
            need(len(event) == 3 and event[1][0] in ("add", "scale", "clear"), "scalar schema")
            need(isinstance(event[2], int), "scalar frame")
        elif kind == "adapter":
            need(len(event) == 4 and event[1] in ("old_to_new", "new_to_old"), "adapter schema")
        elif kind == "residual_adapter":
            need(len(event) in (4, 5) and event[1] in ("pre", "post"), "residual schema")
        else:
            need(len(event) == 6 and event[1] in ("A", "B", "final", "cleanup_tail"),
                 "climb schema")
    named = [index for index, event in enumerate(events) if mentions_561(event)]
    need(named[0] == ADAPTER_INDEX and events[ADAPTER_INDEX] == ADAPTER, "entrance adapter")
    need(named[1] == ADD_INDEX and events[ADD_INDEX] == ADD, "adjacent ADD")
    need(all(index > ADD_INDEX for index in named[2:]), "an earlier L561 record appeared")
    for index, event in enumerate(events[:ADD_INDEX]):
        need(not mentions_561(event) or index == ADAPTER_INDEX, "extra pre-ADD L561 record")
    for slot, last in enumerate(LAST_CLEARS):
        token = ["C", slot]
        writes = [index for index, event in enumerate(events[:ADD_INDEX])
                  if event[0] == "scalar" and event[1][1] == token]
        need(writes and writes[-1] == last and events[last] == ["scalar", ["clear", token], 0],
             "private last-write CLEAR")
        need(not any(event[0] == "scalar" and token in event[1][1:]
                     for event in events[ADD_INDEX - 1:]),
             "private field reused at the ADD")
    return len(named)


def canonical_frames():
    raw = load_checked(ARCHIVE, ARCHIVE_SHA, 64 * 1024**2)
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tar:
        info = tar.getmember(WORD_MEMBER)
        need(info.isfile(), "word member")
        word_raw = tar.extractfile(info).read()
    need(hashlib.sha256(word_raw).hexdigest() == WORD_SHA, "word sha")
    word = json.loads(gzip.decompress(word_raw))
    need(word["start"][561] == 4 and word["frames"][4] == [459], "L561 entrance frame")
    need(word["start"][546] == 0 and word["frames"][0] == [], "L546 entrance frame")


def main():
    certificate = json.loads(gzip.decompress(load_checked(CERTIFICATE, CERTIFICATE_SHA, 8 * 1024**2)))
    events = certificate["core_words"]["forward"]
    mentions = word_gap(events)
    need(mentions == 27, "L561 mention count")
    canonical_frames()
    cases = [(2, 1), (2, 2), (4, 1), (4, 3), (8, 2), (16, 4), (32, 5), (128, 1), (512, 5)]
    for n, width in cases:
        sharp, past = formulas(n, width)
        real = [(index * 3 + 1) % (1 << (width - 1)) for index in range(n)]
        imag = [-(index % (1 << (width - 1))) for index in range(n)]
        got, bits = place(real, imag, width, one_past=False, scratch_fill=1)
        need(got == sharp, "sharp bill")
        need(any(bit == 1 for row in bits for bit in row) or real == imag == [0] * n,
             "copied bits")
        got_past, _bits = place(real, imag, width, one_past=True, scratch_fill=0)
        need(got_past == past, "one-past bill")
        need(past[2] - sharp[2] == 12, "twelve extra one-past moves")
        other_real = [(-3 * index) % (1 << (width - 1)) for index in range(n)]
        other_imag = [(2 * index + 1) % (1 << (width - 1)) for index in range(n)]
        subtracted = subtract_placed(real, imag, other_real, other_imag, width)
        cells = n * width
        need(subtracted == (4 * cells, 2 * cells, 8 * cells - 12), "subtraction re-meter")
        need(tuple(left + right for left, right in zip(got, subtracted))
             == (6 * cells, 4 * cells, 16 * cells - 24), "combined bill")
    # Dirty scratch is overwritten, and each low home bit is visible.
    zero_bill, zero_bits = place([0, 0], [0, 0], 2, scratch_fill=1)
    need(zero_bill == formulas(2, 2)[0], "zero source still overwrites scratch")
    need(zero_bits == ((0, 0),) * 4, "dirty scratch did not survive")
    base_bill, base_bits = place([0, 1], [1, 0], 2, scratch_fill=1)
    need(base_bill == formulas(2, 2)[0], "base schedule")
    seen = {base_bits}
    for comp in range(2):
        for index in range(2):
            mutated = [[0, 1], [1, 0]]
            mutated[comp][index] ^= 1
            _bill, bits = place(mutated[0], mutated[1], 2, scratch_fill=1)
            need(bits != base_bits, "home bit invisible")
            seen.add(bits)
    need(len(seen) == 5, "home-bit images")
    print(
        "PASS_QQ16_L561_SCRATCH_PLACEMENT"
        " event=9895 intervals=absent prior_records=1"
        " mentions=%d scratch_clear=C0-C7"
        " move=8*N*W-12 read=2*N*W write=2*N*W sharp=yes"
        " one_past_extra=12"
        " combined_read=6*N*W combined_write=4*N*W combined_move=16*N*W-24"
        " no_new_kappa" % mentions
    )


if __name__ == "__main__":
    main()
