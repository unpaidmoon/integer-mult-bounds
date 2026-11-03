#!/usr/bin/env python3
"""Exact successful-fiber checks for a sharp rational-frame error threshold."""
from __future__ import annotations

import hashlib
import itertools
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import NamedTuple


class Node(NamedTuple):
    incoming: tuple[tuple[int, int], ...]
    table: tuple[tuple[int, ...], ...]


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def validate(nodes: tuple[Node, ...], q: int, width: int,
             sinks: tuple[int, ...], demand: tuple[int, ...]) -> None:
    require(type(q) is int and 2 <= q <= 5, 'alphabet')
    require(type(width) is int and 1 <= width <= 3, 'width')
    require(width <= len(nodes) <= 9, 'vertices')
    require(len(sinks) == width and len(set(sinks)) == width, 'sinks')
    require(sorted(demand) == list(range(width)), 'demands')
    ports = [1] * width
    for i, node in enumerate(nodes):
        if i < width:
            require(node == Node((), ()), 'source')
            continue
        require(0 <= len(node.incoming) <= 2, 'arity')
        require(len(node.table) == q ** len(node.incoming), 'table size')
        require(1 <= len(node.table[0]) <= 2, 'output width')
        for row in node.table:
            require(len(row) == len(node.table[0]), 'ragged table')
            require(all(type(x) is int and 0 <= x < q for x in row), 'symbol')
        for source, port in node.incoming:
            require(type(source) is int and 0 <= source < i, 'acyclic edge')
            require(type(port) is int and 0 <= port < ports[source], 'port')
        ports.append(len(node.table[0]))
    for sink in sinks:
        require(type(sink) is int and width <= sink < len(nodes), 'sink index')
        require(ports[sink] == 1, 'sink width')
        require(len(nodes[sink].incoming) == 1, 'sink edge')
        require(nodes[sink].table == tuple((a,) for a in range(q)), 'sink copy')


def evaluate(nodes: tuple[Node, ...], q: int,
             inputs: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    values = [(x,) for x in inputs]
    for node in nodes[len(inputs):]:
        index = 0
        for source, port in node.incoming:
            index = index * q + values[source][port]
        values.append(node.table[index])
    return tuple(values)


def observations(nodes: tuple[Node, ...], q: int, width: int,
                 sinks: tuple[int, ...], demand: tuple[int, ...]):
    validate(nodes, q, width, sinks, demand)
    cases = []
    for inputs in itertools.product(range(q), repeat=width):
        values = evaluate(nodes, q, inputs)
        success = all(values[sink][0] == inputs[demand[j]]
                      for j, sink in enumerate(sinks))
        cases.append((inputs, values, success))
    return tuple(cases)


def check_cuts(nodes: tuple[Node, ...], q: int, width: int,
               sinks: tuple[int, ...], demand: tuple[int, ...]):
    cases = observations(nodes, q, width, sinks, demand)
    edges = tuple((u, port, v) for v, node in enumerate(nodes)
                  for u, port in node.incoming)
    success = sum(ok for _, _, ok in cases)
    counts = {'maps': 1, 'inputs': len(cases), 'cuts': 0, 'fibers': 0,
              'deficient_cuts': 0, 'tight_deficient_cuts': 0}
    for mask in range(1 << len(nodes)):
        inside = tuple(bool(mask & (1 << i)) for i in range(len(nodes)))
        missing = tuple(demand[j] for j, sink in enumerate(sinks)
                        if inside[demand[j]] and not inside[sink])
        leaving = tuple((u, port) for u, port, v in edges
                        if inside[u] and not inside[v])
        d, e = len(missing), len(leaving)
        counts['cuts'] += 1
        require(success * q ** d <= len(cases) * q ** e, 'fiber bound')
        if d > e:
            counts['deficient_cuts'] += 1
            counts['tight_deficient_cuts'] += success * q ** d == len(cases) * q ** e
            require(success * q <= len(cases), 'strict threshold')
        if not missing:
            continue
        outside = tuple(i for i in range(width) if i not in missing)
        fibers = {}
        for inputs, values, ok in cases:
            if not ok:
                continue
            key = (tuple(inputs[i] for i in outside),
                   tuple(values[u][port] for u, port in leaving))
            data = tuple(inputs[i] for i in missing)
            require(key not in fibers or fibers[key] == data, 'fiber collision')
            fibers[key] = data
            counts['fibers'] += 1
    return counts


def add_counts(total: dict[str, int], update: dict[str, int]) -> None:
    for key, value in update.items():
        total[key] = total.get(key, 0) + value


def sink(source: int, port: int, q: int) -> Node:
    return Node(((source, port),), tuple((x,) for x in range(q)))


def parallel_maps(q: int, left: tuple[int, ...], right: tuple[int, ...]):
    return (Node((), ()), Node((), ()),
            Node(((0, 0),), tuple((x,) for x in left)),
            Node(((1, 0),), tuple((x,) for x in right)),
            sink(2, 0, q), sink(3, 0, q))


def map_census() -> dict[str, int]:
    total: dict[str, int] = {}
    for q in (2, 3):
        functions = tuple(itertools.product(range(q), repeat=q))
        for left, right in itertools.product(functions, repeat=2):
            nodes = parallel_maps(q, left, right)
            for demand in ((0, 1), (1, 0)):
                add_counts(total, check_cuts(nodes, q, 2, (4, 5), demand))
    for left, right in itertools.product(range(16), repeat=2):
        table = tuple(((left >> i) & 1, (right >> i) & 1) for i in range(4))
        nodes = (Node((), ()), Node((), ()), Node(((0, 0), (1, 0)), table),
                 sink(2, 0, 2), sink(2, 1, 2))
        for demand in ((0, 1), (1, 0)):
            add_counts(total, check_cuts(nodes, 2, 2, (3, 4), demand))
    require(total['deficient_cuts'] > 0, 'deficient coverage')
    require(total['tight_deficient_cuts'] > 0, 'sharp fiber coverage')
    return total


def diagonal(entries: tuple[int, ...]):
    return tuple(tuple(Fraction(x if i == j else 0) for j in range(len(entries)))
                 for i, x in enumerate(entries))


def difference(left, right):
    return tuple(tuple(a - b for a, b in zip(x, y)) for x, y in zip(left, right))


def matrix_rank(matrix) -> int:
    rows = [list(row) for row in matrix]
    rank = 0
    for column in range(len(rows)):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [x / scale for x in rows[rank]]
        for i in range(len(rows)):
            if i != rank:
                multiple = rows[i][column]
                rows[i] = [a - multiple * b for a, b in zip(rows[i], rows[rank])]
        rank += 1
    return rank


def framed_bill(nodes, frames, width: int, sinks, demand) -> int:
    require(len(frames) == len(nodes), 'frame count')
    m = len(frames[0])
    require(1 <= m <= 3, 'address dimension')
    identity = diagonal((1,) * m)
    for frame in frames:
        require(len(frame) == m and all(len(row) == m for row in frame), 'matrix shape')
        require(all(frame[i][j] == 0 for i in range(m) for j in range(i)), 'common flag')
    for j, target in enumerate(sinks):
        require(difference(frames[target], frames[demand[j]]) == identity, 'terminal shift')
    bill = 0
    diagonal_cuts = [0] * m
    for v, node in enumerate(nodes):
        for u, _ in node.incoming:
            delta = difference(frames[v], frames[u])
            cost = matrix_rank(delta)
            crossed = tuple(delta[i][i] != 0 for i in range(m))
            require(sum(crossed) <= cost, 'edge certificate')
            for i in range(m):
                diagonal_cuts[i] += crossed[i]
            bill += cost
    require(sum(diagonal_cuts) <= bill, 'weighted certificate')
    return bill


def swap_fixture(q: int, width: int, m: int, exact: bool):
    zero = diagonal((0,) * m)
    projection = diagonal((1,) + (0,) * (m - 1))
    identity = diagonal((1,) * m)
    shifted = diagonal((2,) + (1,) * (m - 1))
    nodes = [Node((), ()) for _ in range(width)]
    frames = [zero, projection] + [zero] * (width - 2)
    last = ((0, 0), (1, 0))
    if exact:
        tables = (tuple(((a + b) % q, b) for a, b in itertools.product(range(q), repeat=2)),
                  tuple((a, (a - b) % q) for a, b in itertools.product(range(q), repeat=2)),
                  tuple(((a - b) % q, b) for a, b in itertools.product(range(q), repeat=2)))
        for table in tables:
            require(len(set(table)) == q * q, 'reversible gate')
            nodes.append(Node(last, table))
            frames.append(projection)
            last = ((len(nodes) - 1, 0), (len(nodes) - 1, 1))
    sinks = []
    for i in range(width):
        source, port = last[i] if i < 2 else (i, 0)
        sinks.append(len(nodes))
        nodes.append(sink(source, port, q))
        frames.append(shifted if i == 0 else identity)
    demand = (1, 0) + tuple(range(2, width))
    return tuple(nodes), tuple(frames), tuple(sinks), demand


def attainment_census() -> dict[str, int]:
    counts = {'framed_fixtures': 0, 'attainment_inputs': 0, 'random_inputs': 0}
    for q, width, m in itertools.product(range(2, 6), (2, 3), range(1, 4)):
        for exact in (False, True):
            nodes, frames, sinks, demand = swap_fixture(q, width, m, exact)
            cases = observations(nodes, q, width, sinks, demand)
            correct = sum(ok for _, _, ok in cases)
            require(correct == q ** (width - (not exact)), 'attaining success')
            bill = framed_bill(nodes, frames, width, sinks, demand)
            require(bill == width * m - (not exact), 'attaining rank')
            if correct * q > len(cases):
                require(bill >= width * m, 'flag threshold')
            counts['framed_fixtures'] += 1
            counts['attainment_inputs'] += len(cases)
            if m == 1:
                add_counts(counts, check_cuts(nodes, q, width, sinks, demand))
        bad = swap_fixture(q, width, m, False)
        good = swap_fixture(q, width, m, True)
        successes = 0
        for chosen in (bad, good):
            successes += sum(ok for _, _, ok in observations(chosen[0], q, width, chosen[2], chosen[3]))
        total = 2 * q ** width
        require(successes * q > total, 'expected-budget success')
        bills = tuple(framed_bill(x[0], x[1], width, x[2], x[3]) for x in (bad, good))
        require(Fraction(sum(bills), 2) < width * m, 'expected-budget cost')
        counts['random_inputs'] += total
    return counts


def rejecting_controls() -> int:
    nodes, frames, sinks, demand = swap_fixture(2, 2, 2, False)
    changes = (
        (nodes, 1, 2, sinks, demand, 'alphabet'),
        (nodes, 2, 0, sinks, demand, 'width'),
        (nodes, 2, 2, (sinks[0], sinks[0]), demand, 'sinks'),
        (nodes, 2, 2, sinks, (0, 0), 'demands'),
        (nodes[:2] + (Node(((3, 0),), ((0,), (1,))),) + nodes[3:],
         2, 2, sinks, demand, 'acyclic edge'),
        (nodes[:2] + (Node(((0, 2),), ((0,), (1,))),) + nodes[3:],
         2, 2, sinks, demand, 'port'),
        (nodes[:2] + (Node(((0, 0),), ((0,),)),) + nodes[3:],
         2, 2, sinks, demand, 'table size'),
        (nodes[:2] + (Node(((0, 0),), ((0,), (2,))),) + nodes[3:],
         2, 2, sinks, demand, 'symbol'),
    )
    for changed, q, width, out, target, reason in changes:
        try:
            validate(changed, q, width, out, target)
        except ValueError as error:
            require(str(error) == reason, 'wrong control rejection')
        else:
            raise ValueError('control accepted')
    for reason in ('common flag', 'terminal shift'):
        changed = list(frames)
        if reason == 'common flag':
            changed[0] = ((Fraction(0), Fraction(0)), (Fraction(1), Fraction(0)))
        else:
            changed[sinks[0]] = diagonal((1, 1))
        try:
            framed_bill(nodes, tuple(changed), 2, sinks, demand)
        except ValueError as error:
            require(str(error) == reason, 'wrong frame rejection')
        else:
            raise ValueError('frame control accepted')
    return len(changes) + 2


def boundary_controls() -> tuple[str, ...]:
    nodes, frames, sinks, demand = swap_fixture(2, 2, 2, False)
    cases = observations(nodes, 2, 2, sinks, demand)
    bill = framed_bill(nodes, frames, 2, sinks, demand)
    correct = sum(ok for _, _, ok in cases)
    require(correct * 2 == len(cases) and bill < 4, 'nonstrict threshold trap')
    weighted = sum((3 if a == 0 else 1) * (3 if b == 0 else 1)
                   for (a, b), _, ok in cases if ok)
    require(weighted * 2 > 16 and bill < 4, 'biased uniformity boundary')
    diagonal_cases = tuple(ok for (a, b), _, ok in cases if a == b)
    require(all(diagonal_cases) and len(diagonal_cases) == 2, 'correlation boundary')
    nonflag = ((Fraction(1), Fraction(1)), (Fraction(1), Fraction(1)))
    require(matrix_rank(nonflag) < sum(nonflag[i][i] != 0 for i in range(2)),
            'nonflag rank boundary')
    exact_nodes, exact_frames, out, target = swap_fixture(3, 2, 2, True)
    changed = list(exact_frames)
    changed[2] = ((Fraction(1), Fraction(1)), (Fraction(0), Fraction(0)))
    changed[4] = ((Fraction(1), Fraction(-1)), (Fraction(0), Fraction(0)))
    require(framed_bill(exact_nodes, tuple(changed), 2, out, target) >= 4,
            'noncommuting flag positive')
    require(all(ok for _, _, ok in observations(exact_nodes, 3, 2, out, target)),
            'noncommuting flag endpoint')
    return ('strict threshold', 'biased inputs', 'correlated inputs',
            'nonflag rank', 'noncommuting triangular positive')


def main() -> None:
    require(len(sys.argv) == 1, 'unexpected arguments')
    result = {'status': 'PASS_BOUNDED_ERROR_PARTITION_THRESHOLD',
              'map_census': map_census(), 'attainment': attainment_census(),
              'rejecting_controls': rejecting_controls(),
              'boundary_controls': boundary_controls()}
    package = Path(__file__).resolve().parent
    names = ('README.md', 'PROOF.md', 'TASK.json', 'SOURCES.json', 'VERIFY.json', 'verify.py')
    result['sha256'] = {name: hashlib.sha256((package / name).read_bytes()).hexdigest()
                        for name in names}
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
