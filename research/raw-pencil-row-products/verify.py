"""Exact product controls and unchanged complete scientific replay."""
import hashlib
import itertools
import json
from pathlib import Path
import random
import shutil
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kernel import row_product
import replay
from replay import ROOT, REPOSITORY, authenticated_bytes, require, run, source_modules


def product_controls():
    cases = 0
    with source_modules() as (decomposition, _):
        fields = [decomposition.a.Field(p, modulus) for p, modulus in
                  ((2, [0, 1]), (3, [0, 1]), (2, [1, 1, 1]), (3, [1, 0, 1]))]
        rng = random.Random(5692)
        for field in fields:
            for height, inner, width in itertools.product(range(5), repeat=3):
                for variant in range(4):
                    left = [[rng.randrange(field.q) if variant else 0
                             for _ in range(inner)] for _ in range(height)]
                    right = [[rng.randrange(field.q) if variant else 0
                              for _ in range(width)] for _ in range(inner)]
                    snapshot = ([r[:] for r in left], [r[:] for r in right])
                    actual = row_product(left, right, width, field)
                    require(actual == decomposition.mm(left, right, width, field),
                            'differential product')
                    require((left, right) == snapshot, 'input mutation')
                    if actual:
                        require(len({id(row) for row in actual}) == height,
                                'aliased output rows')
                    cases += 1
            # A nonzero last summand catches an accidentally truncated inner loop.
            left, right = [[0, 1]], [[0], [1]]
            require(row_product(left, right, 1, field) == [[1]], 'last summand')
            require(row_product([[1]], [[1]], 1, field) != [[0]], 'zero mutant')
    return cases


def receipt():
    paths = sorted(path for path in ROOT.iterdir() if path.is_file())
    return {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}


def rejection_controls():
    global row_product
    original = row_product
    mutants = (
        lambda left, right, width, field: [[0] * width for _ in left],
        lambda left, right, width, field: original(left, right[:-1], width, field),
        lambda left, right, width, field: [[0] * width] * len(left),
    )
    rejected = 0
    try:
        for mutant in mutants:
            row_product = mutant
            try:
                product_controls()
            except ValueError:
                rejected += 1
            else:
                raise ValueError('product mutant accepted')
    finally:
        row_product = original
    manifest = json.loads((ROOT / 'SOURCES.json').read_text())
    with tempfile.TemporaryDirectory(prefix='raw-pencil-source-control-') as name:
        temporary = Path(name)
        for entry in manifest['files']:
            if entry['usage'] == 'input':
                destination = temporary / entry['path']
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(REPOSITORY / entry['path'], destination)
        authenticated_bytes(temporary)
        changed = temporary / 'research/raw-pencil-decomposition/decompose.py'
        changed.write_bytes(changed.read_bytes() + b'\n# changed source\n')
        try:
            authenticated_bytes(temporary)
        except ValueError as error:
            require('source hash:' in str(error), 'wrong source rejection')
            rejected += 1
        else:
            raise ValueError('changed source accepted')
    return rejected


def complete_work_count():
    totals = {'reference_product_terms': 0, 'retained_product_terms': 0}
    original = replay.row_product

    def counted(left, right, width, field):
        require(all(len(row) == len(right) for row in left), 'inner shape')
        require(all(len(row) == width for row in right), 'column shape')
        totals['reference_product_terms'] += width * len(left) * len(right)
        totals['retained_product_terms'] += width * sum(
            coefficient != 0 for row in left for coefficient in row)
        return original(left, right, width, field)

    try:
        replay.row_product = counted
        run('audit')
    finally:
        replay.row_product = original
    totals['omitted_zero_product_terms'] = (
        totals['reference_product_terms'] - totals['retained_product_terms'])
    require(totals['omitted_zero_product_terms'] > 0, 'no arithmetic improvement')
    return totals


def main():
    cases = product_controls()
    controls = rejection_controls()
    work = complete_work_count()
    print(json.dumps({'status': 'PASS_RAW_PENCIL_ROW_PRODUCTS',
                      'differential_products': cases, 'rejected_controls': controls,
                      'work': work,
                      'package_sha256': receipt()},
                     sort_keys=True))


if __name__ == '__main__':
    main()
