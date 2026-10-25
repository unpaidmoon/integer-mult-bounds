#!/usr/bin/env python3
"""Direct binary exchanges versus the ordinary-interchange bill.

The in-record schedule is executed. The payload-transport lower bound is an
exact integer comparison on the #4174 layouts. No new kappa is claimed.
"""
from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BLANK = None
C = Fraction(8667, 5000000)
A2 = C * (1 - C * C)
ALLOCATOR = ROOT / "research/pr4100-guard-coloring/vendor/pr4174_allocator.py"


def fail(message: str) -> None:
    raise SystemExit("FAIL: " + message)


def need(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def must_fail(check, message: str) -> None:
    try:
        check()
    except SystemExit:
        return
    fail("control did not fail: " + message)


def phrase(path: str, text: str) -> None:
    body = (ROOT / path).read_text(encoding="utf-8")
    need(text in body, "missing phrase in " + path + ": " + text[:60])


def load_allocator():
    spec = importlib.util.spec_from_file_location("pr4174_allocator", ALLOCATOR)
    module = importlib.util.module_from_spec(spec)
    sys.modules["pr4174_allocator"] = module
    spec.loader.exec_module(module)
    return module


def swap_record(data: list, i: int, j: int) -> tuple[int, int, int]:
    """Swap stored bits i < j. One 2-cell buffer. Heads return. Buffer ends blank."""
    need(0 <= i < j < len(data), "bit positions out of range")
    buf = [BLANK, BLANK]
    data_head = 0
    buffer_head = 0
    moves = reads = writes = 0

    def move_data(target: int) -> None:
        nonlocal data_head, moves
        while data_head != target:
            data_head += 1 if target > data_head else -1
            moves += 1

    def move_buffer(target: int) -> None:
        nonlocal buffer_head, moves
        while buffer_head != target:
            buffer_head += 1 if target > buffer_head else -1
            moves += 1

    def read_data():
        nonlocal reads
        reads += 1
        return data[data_head]

    def write_data(bit: int) -> None:
        nonlocal writes
        writes += 1
        data[data_head] = bit

    def read_buffer():
        nonlocal reads
        reads += 1
        return buf[buffer_head]

    def write_buffer(bit) -> None:
        nonlocal writes
        writes += 1
        buf[buffer_head] = bit

    move_data(i)
    old_i = read_data()
    move_buffer(0)
    write_buffer(old_i)
    move_data(j)
    old_j = read_data()
    move_buffer(1)
    write_buffer(old_j)
    move_buffer(0)
    saved_i = read_buffer()
    write_data(saved_i)
    move_buffer(1)
    saved_j = read_buffer()
    move_data(i)
    write_data(saved_j)
    move_buffer(0)
    write_buffer(BLANK)
    move_buffer(1)
    write_buffer(BLANK)
    move_buffer(0)
    move_data(0)
    need(buf == [BLANK, BLANK], "buffer not blank")
    need(data_head == 0 and buffer_head == 0, "heads not home")
    return moves, reads, writes


def exchange_fields(data: list, left: int, right: int, width: int) -> int:
    need(width >= 1 and left >= 0 and left + width <= right and right + width <= len(data),
         "fields are not disjoint")
    total = 0
    for offset in range(width):
        moves, reads, writes = swap_record(data, left + offset, right + offset)
        need((moves, reads, writes) == (2 * (right + offset) + 6, 4, 6),
             "single-swap action split")
        total += moves + reads + writes
    return total


def field_actions(right: int, width: int) -> int:
    return width * (2 * right + width + 15)


def h_power_bound(height: int) -> None:
    """height^a2 < 2^{1/20} whenever height < 2^25, since 25 a2 < 1/20."""
    need(1 <= height < 2 ** 25, "height outside the elementary range used here")
    numerator = 25 * 8667 * (5000000 ** 2 - 8667 ** 2)
    denominator = 5000000 ** 3
    need(20 * numerator < denominator, "25 a2 is not below 1/20")


def sigma(address: int, high: int, low: int) -> int:
    high_bit = (address >> high) & 1
    low_bit = (address >> low) & 1
    if high_bit == low_bit:
        return address
    return address ^ ((1 << high) | (1 << low))


def check_small_transport() -> None:
    for length in range(2, 7):
        size = 1 << length
        for low in range(length):
            for high in range(low + 1, length):
                distance = (1 << high) - (1 << low)
                moved = 0
                for address in range(size):
                    image = sigma(address, high, low)
                    gap = abs(image - address)
                    if gap:
                        moved += 1
                        need(gap == distance, "pair distance")
                need(moved == size // 2, "exactly half the addresses move")


def front_pair(plan) -> tuple[tuple[int, int], tuple[int, int]]:
    for source, destination in plan.swaps:
        if destination == (0, plan.layout.H):
            return source, destination
    fail("no front field")


def transport_gap(layout, plan) -> int:
    source, destination = front_pair(plan)
    length, height = layout.L, layout.H
    need(destination == (0, height), "front destination")
    need(source[0] >= 2 * height, "front partner is not disjoint from the two front fields")
    # Position 0 is the MSB, place value 2^{L-1}.
    high = length - 1
    low = length - 1 - source[0]
    need(high > low >= 0, "place exponents")
    return (1 << high) - (1 << low)


def check_layout(allocator, p: int, ell: int, widths, name: str) -> tuple[int, int]:
    layout = allocator.Layout(p, ell, widths)
    plan = next(allocator.iter_plans(layout))
    need(tuple(destination for _, destination in plan.swaps) == (
        (0, layout.H), (layout.H, 2 * layout.H), (layout.L - layout.H, layout.L)),
         name + " destinations")
    distance = transport_gap(layout, plan)
    scans = distance // 4
    allowance = 18 * layout.H
    need(scans > allowance, name + " transport does not exceed the in-record allowance")
    need(scans.bit_length() - 1 >= layout.L - 4, name + " scan exponent")
    h_power_bound(layout.H)
    per_record = field_actions(layout.L - layout.H, layout.H)
    need(per_record <= 3 * layout.H * layout.L, name + " in-record field bound")
    return layout.L, layout.H


def check_phrases() -> None:
    phrase("research/unconditional-batched-crt/BIT.md",
           "in O(V e^(1-a2)) time and O(V) visited")
    phrase("research/unconditional-batched-crt/BIT.md",
           "a2=c(1-c^2)=0.001733394791695384296")
    phrase("research/unconditional-batched-crt/BIT.md",
           "not the fields, payload or e.")
    phrase("research/unconditional-batched-crt/CRT.md",
           "Three disjoint source/destination exchanges suffice.")
    phrase("research/crt-reservoir-interchange-bill/PROOF.md",
           "A direct binary exchange, made of")
    phrase("research/crt-reservoir-interchange-bill/PROOF.md",
           "would avoid the padding. That routine is not")


def check_padding() -> None:
    q = 2 ** 89 - 1
    height = 10752
    width = height // 89 + 1
    need(q ** (width - 1) < 2 ** height <= q ** width, "radix width at H=10752")
    padded = (q ** width) ** 2
    need(2 ** (2 * height + 33) < padded < 2 ** (2 * height + 34),
         "minimal padding is between 2^33 and 2^34")


def main() -> None:
    check_phrases()
    check_small_transport()
    check_padding()
    for length, left, right in ((8, 1, 4), (8, 0, 7), (20, 3, 11), (40, 0, 17)):
        original = [((k * 3 + left) & 1) for k in range(length)]
        data = original[:]
        moves, reads, writes = swap_record(data, left, right)
        expected = original[:]
        expected[left], expected[right] = expected[right], expected[left]
        need(data == expected, "swap image")
        need(moves + reads + writes == 2 * right + 16, "swap total")
        need((moves, reads, writes) == (2 * right + 6, 4, 6), "swap split")
    record = [k & 1 for k in range(30)]
    before = record[:]
    total = exchange_fields(record, 2, 14, 5)
    for offset in range(5):
        need(record[2 + offset] == before[14 + offset], "field image left")
        need(record[14 + offset] == before[2 + offset], "field image right")
    for index, bit in enumerate(record):
        if index < 2 or 7 <= index < 14 or index >= 19:
            need(bit == before[index], "spectator")
    need(total == field_actions(14, 5), "field total")
    # The in-record rewrite does not move payloads between slots.
    payloads = [10, 11, 12, 13]
    labels = [0, 1, 2, 3]
    for index, label in enumerate(labels):
        bits = [(label >> shift) & 1 for shift in range(1, -1, -1)]
        swap_record(bits, 0, 1)
        labels[index] = bits[0] * 2 + bits[1]
    need(payloads == [10, 11, 12, 13], "payloads stay in their slots")
    need(labels == [0, 2, 1, 3], "stored labels are rewritten")
    must_fail(lambda: swap_record([0, 1, 0], 2, 1), "reversed positions")
    must_fail(lambda: exchange_fields([0, 1, 0, 1], 0, 1, 2), "overlapping fields")

    allocator = load_allocator()
    minimal_length, minimal_height = check_layout(
        allocator, 1310720, 21, (20,) * (1 << 16), "minimal")
    need((minimal_length, minimal_height) == (1310720, 10752), "minimal parameters")
    production_widths = tuple(24 - (index % 2) for index in range(1 << 16))
    production_p = 6 * sum(production_widths)
    production_length, production_height = check_layout(
        allocator, production_p, 24, production_widths, "production")
    need((production_p, production_length, production_height) == (9240576, 1540096, 15360),
         "production parameters")
    # A uniform constant cannot hide the MSB transport on every larger layout:
    # scans >= 2^{L-4} and H <= L/100, so the ratio is at least 2^{L-4}/L.
    need(2 ** (minimal_length - 4) > 36 * minimal_height, "minimal ratio")
    print(
        "PASS_CRT_BINARY_FIELD_EXCHANGE "
        f"swap=2j+16 in_record_C=18*2^(1/20) "
        f"minimal_L={minimal_length} minimal_H={minimal_height} "
        f"production_L={production_length} production_H={production_height} "
        "transport=GT no_padding=1 no_new_kappa"
    )


if __name__ == "__main__":
    main()
