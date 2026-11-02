"""Local paid coin delivery, extending JoyboyBrian's PR6095 marker machine.

The half subword is zxv's PR6092 kernel. Supplied layout, program and clean
allocation are premises; this interpreter does not construct those interfaces.
New wrapper and audit: AAAmirinu + OpenAI Codex. Apache-2.0.
"""
from itertools import product

PAYLOAD = 'LRABXCTNPJ'
INVERSE = str.maketrans('LRNP', 'RLPN')


def need(ok, message):
    if not ok:
        raise ValueError(message)


def transition_table():
    """Read only mode, program symbol, a,b, scanned data and scanned coin."""
    rows = {}
    for mode, symbol, a, b, bit, coin in product(
            ('F', 'FR', 'I', 'IR'), '<>' + PAYLOAD, (0, 1), (0, 1),
            (0, 1), (0, 1)):
        next_mode, da, db, out = mode, a, b, bit
        dm = pm = rm = 0
        returned = write = False
        if symbol == '>' and mode in ('F', 'I'):
            next_mode, pm = ('FR' if mode == 'F' else 'IR'), -1
        elif symbol == '<' and mode in ('FR', 'IR'):
            next_mode, pm, returned = ('F' if mode == 'FR' else 'I'), 1, True
        elif symbol in PAYLOAD:
            pm = 1 if mode in ('F', 'I') else -1
            if mode in ('F', 'IR'):
                direction = 1 if mode == 'F' else -1
                if symbol == 'L': dm = -direction
                elif symbol == 'R': dm = direction
                elif symbol == 'N': rm = direction
                elif symbol == 'P': rm = -direction
                elif symbol == 'A': da ^= bit
                elif symbol == 'B': db ^= bit
                elif symbol == 'J': da ^= coin
                elif symbol == 'X': out ^= 1; write = True
                elif symbol == 'C': out ^= a; write = True
                elif symbol == 'T': out ^= a & b; write = True
        else:
            continue
        rows[mode, symbol, a, b, bit, coin] = (
            next_mode, da, db, out, dm, pm, rm, returned, write)
    return rows


TABLE = transition_table()


def fetch_word(width, offset=11):
    need(type(width) is int and width >= 2 and type(offset) is int and offset >= 0,
         'wrapper width/offset domain')
    return 'N' * offset + 'J' + 'R' * (width + 1) + 'C' + 'L' * (width + 1) + 'J' + 'P' * offset


def wrapped_word(half, width, offset=11):
    fetch = fetch_word(width, offset)
    need(fetch[::-1].translate(INVERSE) == fetch, 'fetch literal inverse')
    return fetch + half + fetch


def run(data, program, random_tape, width, payload_length, origins=(0, 0, 0),
        inverse=False, table=TABLE):
    """Execute single local rows; dictionaries also retain unvisited spectators.

    Both read-only tapes are copied and compared. Bounds/watchdog diagnose
    invalid fixtures or mutants; they are not additional machine transitions.
    No indexed arithmetic or gate operation occurs in the execution loop.
    """
    cells = dict(data)
    saved_program, saved_random = dict(program), dict(random_tape)
    d0, p0, r0 = origins
    head, pc, random_head = d0, p0 + 1, r0
    a = b = 0
    mode = 'I' if inverse else 'F'
    steps = moves = random_moves = markers = 0
    written = set()
    data_seen, program_seen, random_seen = {head}, {pc}, {random_head}
    while True:
        need(d0 <= head < d0 + 2 * width + 2, 'data head escaped supplied interval')
        need(p0 <= pc <= p0 + payload_length + 1, 'program head escaped markers')
        need(r0 <= random_head < r0 + 12, 'coin head escaped supplied interval')
        symbol, bit, coin = program[pc], cells[head], random_tape[random_head]
        row = table.get((mode, symbol, a, b, bit, coin))
        need(row is not None, 'undefined local transition')
        mode, a, b, value, dm, pm, rm, returned, write = row
        if write:
            cells[head] = value
            written.add(head)
        head += dm
        pc += pm
        random_head += rm
        data_seen.add(head)
        program_seen.add(pc)
        random_seen.add(random_head)
        steps += 1
        moves += abs(dm)
        random_moves += abs(rm)
        markers += int(symbol in '<>')
        if returned:
            break
        need(steps <= 2 * payload_length + 2, 'watchdog: missing marker return')
    need((head, pc, random_head, a, b, mode) ==
         (d0, p0 + 1, r0, 0, 0, 'I' if inverse else 'F'),
         'heads or finite control did not return')
    need(program == saved_program and random_tape == saved_random,
         'read-only program or random tape changed')
    return cells, {
        'steps': steps, 'data_moves': moves, 'coin_moves': random_moves,
        'marker_steps': markers, 'written': sorted(x - d0 for x in written),
        'visited_data': sorted(x - d0 for x in data_seen),
        'visited_program': sorted(x - p0 for x in program_seen),
        'visited_coin': sorted(x - r0 for x in random_seen),
    }
