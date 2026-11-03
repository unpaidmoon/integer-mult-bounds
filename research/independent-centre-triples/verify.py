#!/usr/bin/env python3
"""Source-bound independent-centre triple certificate. Apache-2.0."""

from collections import Counter
from hashlib import sha256
from itertools import product
from pathlib import Path
import argparse
import importlib.util
import json
import tempfile

from geometry import (binary_rank, induced_paths, label_distance, need,
                      neighbours, path_minimum, transform)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
EXPECTED_MINIMA = (2, 1, 1, 1, 1, 1, 1, 0, 0)


def authenticate(root):
    sources = json.loads((HERE / "SOURCES.json").read_text())
    for row in sources["files"]:
        if row["usage"] == "input":
            actual = sha256((root / row["path"]).read_bytes()).hexdigest()
            need(actual == row["sha256"], "source bytes: " + row["path"])


def source_controls(directory):
    sources = json.loads((HERE / "SOURCES.json").read_text())
    inputs = [row["path"] for row in sources["files"] if row["usage"] == "input"]
    need(len(inputs) == 4, "complete source-control domain")
    root = directory / "source-controls"
    for name in inputs:
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / name).read_bytes())
    authenticate(root)
    rejected = 0
    for name in inputs:
        target = root / name
        original = target.read_bytes()
        need(bool(original), "nonempty source input")
        target.write_bytes(original[:-1] + bytes((original[-1] ^ 1,)))
        try:
            authenticate(root)
        except ValueError:
            rejected += 1
        target.write_bytes(original)
    need(rejected == len(inputs), "each altered source rejects")
    return rejected


def load_graph(directory):
    path = ROOT / "research/sol1337-contact-frontier/build_graph.py"
    spec = importlib.util.spec_from_file_location("retained_centre_builder", path)
    need(spec is not None and spec.loader is not None, "source builder loader")
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    metadata = builder.build(directory)
    lines = (directory / "center-contact-graph.txt").read_text().splitlines()
    n, f, m, e = map(int, lines[0].split())
    need((n, f, m, e) == (19197, 4429, 145, 34830), "exact graph dimensions")
    need(len(lines) == 1 + n + f + m + e, "complete graph payload")
    nodes = tuple(tuple(map(int, line.split())) for line in lines[1:1 + n])
    lags = tuple(tuple(map(int, line.split())) for line in lines[1 + n:1 + n + f])
    edges = tuple(tuple(map(int, line.split())) for line in lines[1 + n + f + m:])
    validate_graph(nodes, lags, edges)
    need(metadata["inputs"] == 640 and metadata["independent_center_reward"] == 0,
         "retained arbitrary inputs and no independent centre credit")
    need(metadata["helpers"] == {4: 28, 7: 7, 8: 47, 9: 326}, "unchanged helper credits")
    return nodes, lags, edges


def validate_graph(nodes, lags, edges):
    need(len(nodes) == 19197 and len(lags) == 4429 and len(edges) == 34830,
         "bounded original graph")
    need(all(len(row) == 2 and 0 <= row[0] < len(lags) and row[1] in (0, 1)
             for row in nodes), "node domain")
    need(all(len(row) == 9 and all(0 <= x < 1 << 18 for x in row)
             for row in lags), "nine-dimensional frame bases")
    need(lags[0] == tuple(1 << (9 + i) for i in range(9)), "literal empty chart")
    for row in edges:
        need(len(row) == 5, "edge shape")
        a, b, rank, sign, map_id = row
        need(0 <= a < len(nodes) and 0 <= b < len(nodes), "edge endpoints")
        need(0 <= rank <= 9 and sign == 1 and 0 <= map_id < 145, "paid edge domain")
        if nodes[a][1] == 0 or nodes[b][1] == 0:
            need(map_id == 0 and a != b, "identity-map contact edge")
    paid = Counter(r for _, _, r, _, _ in edges if r)
    need(paid == {1: 2201, 2: 412, 3: 510, 4: 127, 5: 40, 8: 8}, "baseline bill")


def prepare(nodes, lags, edges):
    selected = {i for i, (_, fixed) in enumerate(nodes) if fixed == 0}
    empty = {i for i in selected if nodes[i][0] == 0}
    need(len(selected) == 184 and len(empty) == 176, "contact domains")
    incident = {i: [] for i in empty}
    internal = []
    for a, b, rank, _, _ in edges:
        if a in empty:
            incident[a].append((b, rank))
        if b in empty:
            incident[b].append((a, rank))
        if a in empty and b in empty:
            need(rank == 0, "old internal rank zero")
            internal.append((a, b))
    need(len(internal) == 256 and all(len(es) == 4 for es in incident.values()),
         "complete empty-chart incident edges")
    paths = induced_paths(empty, internal)
    need(len(paths) == 496, "all induced rank-zero paths")
    images = neighbours(9)
    fids = {nodes[o][0] for es in incident.values() for o, _ in es}
    need(len(fids) == 31, "external frame cache domain")
    ranks = {f: tuple(binary_rank(image + lags[f], 9) - 9 for image in images)
             for f in sorted(fids)}
    unary = {}
    for node in sorted(empty):
        unary[node] = tuple(tuple(sum(min(ranks[nodes[o][0]][k], j) - min(r, j)
                                     for o, r in incident[node]) for k in range(1022))
                            for j in range(1, 10))
    return paths, unary, images


def direct_delta(path, labels, nodes, lags, edges, images):
    changed = {v: images[k] for v, k in zip(path, labels)}
    delta = [0] * 10
    for a, b, old, _, map_id in edges:
        if a in changed or b in changed:
            need(map_id == 0, "literal joint uses identity-map edges")
            left = changed[a] if a in changed else lags[nodes[a][0]]
            right = changed[b] if b in changed else lags[nodes[b][0]]
            new = binary_rank(left + right, 9) - 9
            delta[new] += 1
            delta[old] -= 1
    return tuple(delta)


def prefix_values(delta):
    return tuple(sum(delta[r] * min(r, j) for r in range(10)) for j in range(1, 10))


def prove_paths(paths, unary, nodes, lags, edges, images):
    transformed = {(v, j): transform(unary[v][j - 1], j)
                   for v in unary for j in range(1, 10)}
    minima = [10**9] * 9
    witnesses = [None] * 9
    classes = Counter()
    for path in paths:
        a, b, c = path
        values = []
        for j in range(1, 10):
            left, right = transformed[a, j], transformed[c, j]
            value, labels = min((unary[b][j - 1][k] + left[k][0] + right[k][0],
                                 (left[k][1], k, right[k][1])) for k in range(1022))
            need(value >= EXPECTED_MINIMA[j - 1], "exact independent-triple prefix floor")
            values.append(value)
            if value < minima[j - 1]:
                minima[j - 1] = value
                witnesses[j - 1] = (path, labels)
        classes[tuple(values)] += 1
    need(tuple(minima) == EXPECTED_MINIMA, "attained componentwise global minima")
    literal = []
    for j, witness in enumerate(witnesses, 1):
        path, labels = witness
        delta = direct_delta(path, labels, nodes, lags, edges, images)
        need(prefix_values(delta)[j - 1] == minima[j - 1], "literal attaining invoice")
        literal.append({"prefix": j, "path": path, "labels": labels, "delta": delta})
    sharp_path, sharp_labels = (11013, 11014, 11015), (59, 59, 59)
    need(sharp_path in paths, "sharp witness is an induced source path")
    sharp_delta = direct_delta(sharp_path, sharp_labels, nodes, lags, edges, images)
    need(prefix_values(sharp_delta) == EXPECTED_MINIMA, "one witness attains every prefix")
    return {"prefix_minima": minima, "attaining_witnesses": literal,
            "sharp_witness": {"path": sharp_path, "labels": sharp_labels, "delta": sharp_delta},
            "path_prefix_classes": [{"minima": v, "paths": count}
                                    for v, count in sorted(classes.items())]}


def controls():
    geometry_cases = 0
    for width in range(1, 5):
        images = neighbours(width)
        for i, left in enumerate(images):
            for k, right in enumerate(images):
                need(binary_rank(left + right, width) - width == label_distance(i, k),
                     "literal paired-neighbour geometry")
                geometry_cases += 1
    transform_cases = 0
    for count in (4, 6, 14):
        for seed in range(11):
            values = tuple(((i + 1) * (seed + 3) + i * i) % 17 - 8 for i in range(count))
            for j in (1, 2, 9):
                actual = transform(values, j)
                brute = tuple(min((values[i] + min(label_distance(i, k), j) - 2, i)
                                  for i in range(count)) for k in range(count))
                need(actual == brute, "transform agrees with exhaustive independent labels")
                transform_cases += 1
    path_cases = 0
    for seed in range(9):
        costs = [tuple((seed * (i + 1) + 3 * i * i + offset) % 11 - 5
                       for i in range(6)) for offset in (0, 2, 5)]
        for j in (1, 2, 7, 9):
            brute = min((sum(costs[t][labels[t]] for t in range(3))
                         + min(label_distance(labels[0], labels[1]), j)
                         + min(label_distance(labels[1], labels[2]), j) - 4, labels)
                        for labels in product(range(6), repeat=3))
            need(path_minimum(*costs, j) == brute, "literal full-product path oracle")
            path_cases += 1
    rejected = 0
    for values, j in (((0, 1), 1), ((0, 1, 2), 1), ((0, 0, 0, 0), 0),
                      ((0, 0, 0, 0), 10), ((0, 0, 0, 0.5), 1)):
        try:
            transform(values, j)
        except ValueError:
            rejected += 1
    need(rejected == 5, "invalid min-plus inputs reject")
    need(induced_paths({0, 1, 2}, ((0, 1), (1, 2))) == ((0, 1, 2),), "path fixture")
    need(not induced_paths({0, 1, 2}, ((0, 1), (1, 2), (0, 2))), "triangle excluded")
    need(prefix_values((0, 1, 0, 0, 0, 0, 0, 1, -1, 0))[0] < EXPECTED_MINIMA[0],
         "the inherited single/pair threshold does not prove the new first-prefix bound")
    return {"geometry_cases": geometry_cases, "transform_oracles": transform_cases,
            "full_product_path_oracles": path_cases, "invalid_input_controls": rejected}


def graph_controls(nodes, lags, edges):
    index = next(i for i, (a, b, _, _, _) in enumerate(edges)
                 if nodes[a][1] == 0 or nodes[b][1] == 0)
    rejected = 0
    for field, value in ((3, -1), (4, 1), (2, 10)):
        bad = list(edges)
        row = list(bad[index])
        row[field] = value
        bad[index] = tuple(row)
        try:
            validate_graph(nodes, lags, bad)
        except ValueError:
            rejected += 1
    need(rejected == 3, "negative charge, changed map and invalid rank reject")
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output is not None:
        need(not args.output.resolve().is_relative_to(ROOT), "receipt must stay outside checkout")
    authenticate(ROOT)
    checked = controls()
    with tempfile.TemporaryDirectory(prefix="independent-centre-triples-") as raw:
        nodes, lags, edges = load_graph(Path(raw))
        paths, unary, images = prepare(nodes, lags, edges)
        result = prove_paths(paths, unary, nodes, lags, edges, images)
        checked["graph_rejection_controls"] = graph_controls(nodes, lags, edges)
        checked["source_rejection_controls"] = source_controls(Path(raw))
    result.update(status="PASS_INDEPENDENT_CENTRE_TRIPLES", paths=len(paths), labels=1022,
                  prefix_problems=len(paths) * 9, controls=checked,
                  claim_type="scoped proof with exact finite certificate",
                  moment_lower_bound="3-2^theta+7^theta-8^theta", theta_domain="0<theta<1")
    result["package_sha256"] = {p.name: sha256(p.read_bytes()).hexdigest()
                                for p in sorted(HERE.iterdir()) if p.is_file()}
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.write_text(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
