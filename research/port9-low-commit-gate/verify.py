#!/usr/bin/env python3
"""Commit successor and cache-retirement obstruction for the port9 leaf.

Prepared by unpaidmoon with substantial Cursor Grok assistance. Apache-2.0.
The leaf, frontend and rotation are unchanged predecessor programs.
"""
import importlib.util
import json
from copy import deepcopy
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PORT9 = ROOT / 'research' / 'port9-low-cache-carry'
TAIL_START = 24
TAIL_END = 191  # inclusive; digits 8..63 occupy bits 24..191
CACHE_BITS = 192


def need(condition, message):
    if not condition:
        raise ValueError(message)


def load_port9():
    sys.path.insert(0, str(PORT9))
    spec = importlib.util.spec_from_file_location('port9_low_cache_verify', PORT9 / 'verify.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def instruction_tapes(instructions):
    return {row[1] for row in instructions if row[0] in ('branch', 'write', 'move')}


def run_machine(bundle, program, bank, cap):
    machine = bundle['modules']['machine']
    result = machine.Machine(program, [machine.Tape(dict(cells), head) for cells, head in bank]).run(cap)
    state = [(dict(tape.cells), tape.head) for tape in result.tapes]
    return result, state


def relative_cells(cells, origin):
    return {index - origin: symbol for index, symbol in cells.items()}


def commit_program(machine):
    """Mark the owned 3-bit new-low and return its head. Eight fall-through steps."""
    rows = [('move', 18, 1)] * 3
    rows.append(('write', 18, machine.RIGHT))
    rows.extend([('move', 18, -1)] * 3)
    rows.append(('halt',))
    return machine.Program(tuple(rows), 19)


def retirement_program(machine):
    """Blank cache bits 24..191 and return the cache head. Straight-line."""
    rows = [('move', 17, 1)] * TAIL_START
    for index in range(TAIL_END - TAIL_START + 1):
        rows.append(('write', 17, machine.BLANK))
        if TAIL_START + index != TAIL_END:
            rows.append(('move', 17, 1))
    rows.extend([('move', 17, -1)] * TAIL_END)
    rows.append(('halt',))
    return machine.Program(tuple(rows), 19)


def fails(label, action):
    try:
        action()
    except ValueError as error:
        return str(error)
    raise ValueError('negative control accepted: ' + label)


def witness_values():
    values = [int(i == j) for i in range(8) for j in range(8)]
    values[:8] = [2, 3, 2, 1, 1, 1, 0, 0]
    return values


def payload_for(shape):
    size = shape[0] * shape[1] * shape[2]
    return [int((j * j + 3 * j + j // 7 + 2) % 11 in (0, 1, 4, 7)) for j in range(size)]


def leaf(port9, bundle, programs, values, shape, inverse):
    bank = port9.fixture(bundle, shape, values, payload_for(shape))
    cap = 393 * len(payload_for(shape)) + 600 * shape[1].bit_length() + 30001
    observation = port9.native_run(bundle, programs[inverse], bank, cap)
    port9.check_composition(bundle, observation, bank, shape, values, payload_for(shape), inverse)
    return bank, observation


def run():
    port9 = load_port9()
    bundle = port9.adapter.load()
    column = port9.source_column(bundle)
    programs, metadata = {}, {}
    untouched = {}
    for inverse in (False, True):
        programs[inverse], metadata[inverse] = port9.adapter.build(inverse, bundle)
        parts = metadata[inverse]['components']
        for name in ('generic', 'cleanup'):
            span = programs[inverse].instructions[parts[name]['start']:parts[name]['stop']]
            touched = instruction_tapes(span)
            need(touched.isdisjoint({17, 18}), name + ' touches the cache or new-low tape')
            untouched[str(inverse) + ':' + name] = sorted(touched)
        front = programs[inverse].instructions[parts['frontend']['start']:parts['frontend']['stop']]
        need(17 in instruction_tapes(front) and 18 in instruction_tapes(front),
             'frontend no longer binds the cache and new-low tapes')

    machine = bundle['modules']['machine']
    commit = commit_program(machine)
    retire = retirement_program(machine)
    need(len(commit.instructions) == 8 and instruction_tapes(commit.instructions) == {18},
         'commit successor is not the eight-step tape-18 walk')
    tail_cells = TAIL_END - TAIL_START + 1
    expected_retire = TAIL_START + tail_cells + (tail_cells - 1) + TAIL_END + 1
    need(len(retire.instructions) == expected_retire == 551, 'retirement instruction count')
    need(instruction_tapes(retire.instructions) == {17}, 'retirement touches another tape')

    shape = (1, 125, 1)
    witness = witness_values()
    mutant = witness.copy()
    mutant[8] = 4
    need(port9.arithmetic(witness, 125) == port9.arithmetic(mutant, 125) == (2, -3, 93),
         'published quarter code depends on a digit outside the weighted row')
    need(mutant[8] != witness[8] and mutant[:8] == witness[:8], 'mutant stays off the weighted row')

    banks, observations = {}, {}
    for inverse in (False, True):
        banks[inverse], observations[inverse] = leaf(port9, bundle, programs, witness, shape, inverse)
    mutant_bank, mutant_observation = leaf(port9, bundle, programs, mutant, shape, False)

    forward = observations[False][0]
    mutant_state = mutant_observation[0]
    need(forward[18] == mutant_state[18] and forward[0] == mutant_state[0],
         'digit 8 changed the new-low or the owner permutation')
    need(forward[17] != mutant_state[17], 'digit 8 was not preserved in the cache')
    for tape in range(19):
        if tape != 17:
            need(forward[tape] == mutant_state[tape], 'digit 8 changed tape ' + str(tape))

    origin = forward[17][1]
    low_origin = forward[18][1]
    need(forward[17][1] == banks[False][17][1] and forward[18][1] == banks[False][18][1],
         'leaf moved a cache or new-low head')
    need(forward[17][0] == banks[False][17][0], 'leaf rewrote the cache')
    cache = relative_cells(forward[17][0], origin)
    low = relative_cells(forward[18][0], low_origin)
    need(set(low) == {0, 1, 2}, 'new-low is not the raw three-bit word')
    need(all(cache[bit] in (machine.ZERO, machine.ONE) for bit in range(CACHE_BITS)),
         'cache data bits are not a complete 192-bit word')
    need(cache[CACHE_BITS] == machine.RIGHT, 'cache endpoint marker moved')

    # The rotation and cleanup name neither tape, so one direct run records writes.
    cap = 393 * 125 + 600 * 7 + 30001
    traced, _ = run_machine(bundle, programs[False], banks[False], cap)
    need(not traced.write_positions[17], 'leaf writes the preserved cache')
    need({index - low_origin for index in traced.write_positions[18]} == {0, 1, 2},
         'leaf writes outside the raw new-low word')
    visited = sorted(index - origin for index in traced.visits[17])
    need(visited == list(range(CACHE_BITS + 1)), 'cache scan is not every bit through the endpoint')

    commit_result, commit_state = run_machine(bundle, commit, forward, 20)
    commit_visited = sorted(index - low_origin for index in commit_result.visits[18])
    need(commit_result.steps == 8 and commit_result.halted, 'commit transition count')
    need(commit_visited == [0, 1, 2, 3], 'commit visit is not the three bits plus the marker cell')
    marked = relative_cells(commit_state[18][0], low_origin)
    need(marked[3] == machine.RIGHT and {bit: marked[bit] for bit in range(3)} == low,
         'commit failed to mark the unchanged new-low bits')
    need(commit_state[18][1] == low_origin, 'commit failed to return the new-low head')
    for tape in range(19):
        if tape != 18:
            need(commit_state[tape] == forward[tape], 'commit changed tape ' + str(tape))
    commit_error = fails('marked new-low still matches the raw leaf contract', lambda: port9.check_composition(
        bundle, (commit_state, observations[False][1], observations[False][2], observations[False][3]),
        banks[False], shape, witness, payload_for(shape), False))

    retire_result, retire_state = run_machine(bundle, retire, forward, 600)
    need(retire_result.steps == 551 and retire_result.halted, 'retirement transition count')
    retired = relative_cells(retire_state[17][0], origin)
    need(all(bit not in retired for bit in range(TAIL_START, TAIL_END + 1)), 'tail bits survived retirement')
    need({bit: retired[bit] for bit in range(TAIL_START)} == {bit: cache[bit] for bit in range(TAIL_START)},
         'retirement rewrote a weighted-row bit or an earlier marker')
    need(retired.get(CACHE_BITS) == machine.RIGHT and retire_state[17][1] == origin,
         'retirement disturbed the endpoint or the cache head')
    for tape in range(19):
        if tape != 17:
            need(retire_state[tape] == forward[tape], 'retirement changed tape ' + str(tape))
    retire_error = fails('retired tail still matches the leaf cache contract', lambda: port9.check_composition(
        bundle, (retire_state, observations[False][1], observations[False][2], observations[False][3]),
        banks[False], shape, witness, payload_for(shape), False))
    mutant_cache = relative_cells(mutant_state[17][0], origin)
    mutant_retired = relative_cells(run_machine(bundle, retire, mutant_state, 600)[1][17][0], origin)
    need(all(bit not in mutant_retired for bit in range(TAIL_START, TAIL_END + 1)),
         'mutant tail survived the same retirement')
    need([mutant_cache[bit] for bit in range(TAIL_START, TAIL_START + 3)]
         != [cache[bit] for bit in range(TAIL_START, TAIL_START + 3)],
         'digit 8 was not visible in the preserved cache')
    need(all(bit not in mutant_retired for bit in range(TAIL_START, TAIL_END + 1))
         and all(bit not in retired for bit in range(TAIL_START, TAIL_END + 1)),
         'the two retired tails still differ')

    inverse_state = observations[True][0]
    need(inverse_state[17] == banks[True][17] and inverse_state[18][1] == banks[True][18][1],
         'inverse orientation does not preserve the cache and new-low head')
    need(set(relative_cells(inverse_state[18][0], inverse_state[18][1])) == {0, 1, 2},
         'inverse new-low is not the raw three-bit word')

    return {
        'status': 'PASS_PORT9_LOW_COMMIT_GATE',
        'source': {
            'port': 9, 'direction': 'inverse', 'column': 1,
            'column_entries': [str(entry) for entry in column],
            'weighted_row': witness[:8], 'ignored_digit_index': 8,
            'ignored_digit_values': [witness[8], mutant[8]],
            'new_low': 2, 'quarter_code': -3, 'modulus': 125, 'offset': 93,
        },
        'static': {
            'generic_and_cleanup_avoid_tapes': [17, 18],
            'component_tapes': untouched,
            'frontend_names_cache_and_new_low': True,
            'leaf_cache_writes': 0,
            'leaf_new_low_write_offsets': [0, 1, 2],
            'cache_visit_min': visited[0],
            'cache_visit_max': visited[-1],
            'cache_visit_count': len(visited),
        },
        'commit': {
            'transitions': 8, 'visited_cells': 4, 'marker_offset': 3,
            'preserves_three_bits': True, 'other_tapes_unchanged': True,
            'leaf_contract_error': commit_error,
        },
        'retirement': {
            'transitions': 551, 'blanked_offsets': [TAIL_START, TAIL_END],
            'preserves_offsets_0_through_23': True, 'preserves_endpoint': True,
            'leaf_contract_error': retire_error,
            'distinct_digit8_caches_become_equal_on_the_tail': True,
        },
        'orientations_executed': ['forward', 'inverse'],
        'limits': [
            'The commit is a successor of the raw leaf exit, not a change to that exit.',
            'Tail retirement at this halt deletes cache data the leaf contract still returns.',
            'Low-type, ROW and whole-T consumers remain absent, so no legal cache retirement is scheduled.',
            'No selected-frontier or kappa change.',
        ],
    }


if __name__ == '__main__':
    need(sys.argv[1:] in ([], ['--write']), 'replay or explicit receipt generation')
    result = run()
    target = HERE / 'RESULT.json'
    encoded = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if sys.argv[1:]:
        target.write_text(encoded, encoding='utf-8')
    else:
        need(result == json.loads(target.read_text(encoding='utf-8')),
             'exact retained deterministic receipt')
    print(result['status'])
