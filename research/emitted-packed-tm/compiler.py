"""Complete packed finite-TM emitter. Produced by Nick Petalas. Apache-2.0."""

from dataclasses import dataclass
from itertools import product


OPS = frozenset(("set", "load", "store", "add", "sub", "and", "or",
                 "not", "shiftl", "shiftr", "jlt", "jzero", "jump",
                 "read", "write", "halt"))
ZERO, ONE, TWO = 31, 1, 2
M, COUNT, POS, TEMP = 32, 33, 34, 35


def require(condition, message):
    if not condition:
        raise ValueError(message)


@dataclass(frozen=True)
class Machine:
    tapes: int
    alphabet: int
    states: int
    delta: dict
    output: int = 0

    def validate(self):
        shape = (self.tapes, self.alphabet, self.states, self.output)
        require(all(type(x) is int for x in shape), "integer machine shape")
        require(1 <= self.tapes <= 4 and 1 <= self.alphabet <= 4,
                "machine tape/alphabet limit")
        require(1 <= self.states <= 16 and 0 <= self.output < self.tapes,
                "machine state/output limit")
        require(type(self.delta) is dict, "transition dictionary")
        require(len(self.delta) <= self.states * self.alphabet ** self.tapes,
                "transition count limit")
        for key, value in self.delta.items():
            require(type(key) is tuple and len(key) == 2, "transition key")
            require(type(value) is tuple and len(value) == 3, "transition value")
            q, reads = key
            nq, writes, moves = value
            require(type(q) is int and type(nq) is int and
                    0 <= q < self.states and 0 <= nq < self.states,
                    "transition state")
            for row in (reads, writes, moves):
                require(type(row) is tuple and len(row) == self.tapes and
                        all(type(x) is int for x in row), "transition row")
            require(all(0 <= s < self.alphabet for s in reads + writes),
                    "transition symbol")
            require(all(d in (-1, 0, 1) for d in moves), "transition move")


class Assembler:
    def __init__(self):
        self.code = []
        self.labels = {}

    def mark(self, label):
        require(label not in self.labels, "duplicate label")
        self.labels[label] = len(self.code)

    def emit(self, op, *args):
        require(op in OPS and len(self.code) < 1000000, "emitter capacity/opcode")
        self.code.append((op, *args))

    def finish(self):
        code = []
        for op, *args in self.code:
            if op in ("jump", "jzero", "jlt"):
                require(args[-1] in self.labels, "unresolved branch")
                args[-1] = self.labels[args[-1]]
            code.append((op, *args))
        return tuple(code)


def packing_init(a, field_log):
    a.emit("add", 3, 0, TWO)
    a.emit("set", 6, 0)
    a.mark("log")
    a.emit("jlt", 3, TWO, "log_end")
    a.emit("shiftr", 3, 3, ONE)
    a.emit("add", 6, 6, ONE)
    a.emit("jump", "log")
    a.mark("log_end")
    a.emit("set", 7, 3 + field_log)
    a.emit("shiftr", 6, 6, 7)
    a.emit("set", 8, 1)
    a.emit("set", 4, 0)
    a.mark("block")
    a.emit("add", 9, 8, 8)
    a.emit("jlt", 6, 9, "block_end")
    a.emit("add", 8, 8, 8)
    a.emit("add", 4, 4, ONE)
    a.emit("jump", "block")
    a.mark("block_end")
    a.emit("sub", 5, 8, ONE)


def prepare(a, head, tape):
    a.emit("shiftr", 10, head, ONE)
    a.emit("and", 11, head, ONE)
    a.emit("set", TEMP, 2 * tape)
    a.emit("add", 11, 11, TEMP)


def access(a, stride_log, field_log, base, write=False):
    # Same ordinary packed field representation as PR4538; no hidden RAM call.
    a.emit("shiftr", 14, 10, 4)
    a.emit("and", 15, 10, 5)
    a.emit("set", 16, field_log)
    a.emit("shiftl", 17, 15, 16)
    a.emit("set", 18, stride_log)
    a.emit("shiftl", 19, 14, 18)
    a.emit("add", 19, 19, 11)
    a.emit("set", 20, base)
    a.emit("add", 19, 19, 20)
    a.emit("load", 21, 19)
    a.emit("set", 23, (1 << (1 << field_log)) - 1)
    if write:
        a.emit("shiftl", 24, 23, 17)
        a.emit("not", 25, 24)
        a.emit("and", 26, 21, 25)
        a.emit("shiftl", 27, 12, 17)
        a.emit("or", 28, 26, 27)
        a.emit("store", 19, 28)
    else:
        a.emit("shiftr", 22, 21, 17)
        a.emit("and", 13, 22, 23)


def move(a, head, direction, label):
    if direction == 0:
        return
    a.emit("and", TEMP, head, ONE)
    a.emit("jzero", TEMP, (label, "positive"))
    if direction == 1:
        a.emit("jlt", head, TWO, (label, "cross_right"))
        a.emit("sub", head, head, TWO)
        a.emit("jump", (label, "end"))
        a.mark((label, "cross_right"))
        a.emit("set", head, 0)
    else:
        a.emit("add", head, head, TWO)
    a.emit("jump", (label, "end"))
    a.mark((label, "positive"))
    if direction == 1:
        a.emit("add", head, head, TWO)
    else:
        a.emit("jzero", head, (label, "cross_left"))
        a.emit("sub", head, head, TWO)
        a.emit("jump", (label, "end"))
        a.mark((label, "cross_left"))
        a.emit("set", head, 1)
    a.mark((label, "end"))


def emit_input(a, machine, heads, stride_log, field_log, base):
    for tape, head in enumerate(heads):
        a.emit("set", head, 0)
        a.emit("read", COUNT)
        a.emit("set", POS, 0)
        a.mark(("input", tape))
        a.emit("jzero", COUNT, ("input_end", tape))
        a.emit("read", 12)
        prepare(a, POS, tape)
        access(a, stride_log, field_log, base, write=True)
        a.emit("add", POS, POS, TWO)
        a.emit("sub", COUNT, COUNT, ONE)
        a.emit("jump", ("input", tape))
        a.mark(("input_end", tape))
    a.emit("jump", ("state", 0))


def emit_states(a, machine, heads, symbols, layout):
    stride_log, field_log, base = layout
    for q in range(machine.states):
        a.mark(("state", q))
        for tape, head in enumerate(heads):
            prepare(a, head, tape)
            access(a, *layout)
            a.emit("add", symbols[tape], 13, ZERO)
        for serial, reads in enumerate(product(range(machine.alphabet),
                                              repeat=machine.tapes)):
            skip = ("skip", q, serial)
            for symbol, expected in zip(symbols, reads):
                a.emit("set", TEMP, expected)
                a.emit("jlt", symbol, TEMP, skip)
                a.emit("jlt", TEMP, symbol, skip)
            transition = machine.delta.get((q, reads))
            if transition is None:
                a.emit("jump", "output")
            else:
                nq, writes, moves = transition
                for tape, value in enumerate(writes):
                    prepare(a, heads[tape], tape)
                    a.emit("set", 12, value)
                    access(a, stride_log, field_log, base, write=True)
                for tape, direction in enumerate(moves):
                    move(a, heads[tape], direction, (q, serial, tape))
                a.emit("jump", ("state", nq))
            a.mark(skip)
        a.emit("jump", "output")  # Unreachable for a well-formed input.


def emit_output(a, machine, layout):
    a.mark("output")
    a.emit("set", POS, 0)
    a.mark("output_loop")
    a.emit("jzero", M, "halt")
    prepare(a, POS, machine.output)
    access(a, *layout)
    a.emit("write", 13)
    a.emit("add", POS, POS, TWO)
    a.emit("sub", M, M, ONE)
    a.emit("jump", "output_loop")
    a.mark("halt")
    a.emit("halt")


def compile_machine(machine):
    machine.validate()
    k = machine.tapes
    field_log = 0 if machine.alphabet <= 2 else 1
    stride_log = (2 * k - 1).bit_length()
    base = 128
    heads = tuple(range(40, 40 + k))
    symbols = tuple(range(40 + k, 40 + 2 * k))
    a = Assembler()
    a.emit("set", ZERO, 0)
    a.emit("set", ONE, 1)
    a.emit("set", TWO, 2)
    a.emit("read", TEMP)  # House-standard outer list length.
    a.emit("read", 0)  # Scale n; not a runtime fuel bound.
    a.emit("read", M)
    packing_init(a, field_log)
    layout = (stride_log, field_log, base)
    emit_input(a, machine, heads, *layout)
    emit_states(a, machine, heads, symbols, layout)
    emit_output(a, machine, layout)
    code = a.finish()
    metadata = {"base": base, "stride": 1 << stride_log,
                "field_bits": 1 << field_log, "heads": heads,
                "boundaries": {a.labels[("state", q)]: q
                               for q in range(machine.states)},
                "output": a.labels["output"], "halt": a.labels["halt"]}
    return code, metadata


def width_bound(machine, code_length, scale, lengths, steps, output_length):
    require(type(scale) is int and 0 <= scale < 1 << 256, "scale limit")
    require(type(steps) is int and 0 <= steps <= 1000000, "step limit")
    require(type(output_length) is int and 0 <= output_length <= 1000000,
            "output limit")
    require(len(lengths) == machine.tapes and
            all(type(x) is int and 0 <= x <= 1000000 for x in lengths),
            "length limit")
    machine.validate()
    require(type(code_length) is int and 1 <= code_length <= 1000000,
            "code length limit")
    span = scale + sum(lengths) + steps + output_length + machine.tapes + 3
    stride = 1 << (2 * machine.tapes - 1).bit_length()
    return max(10, (256 + stride * (span + 1)).bit_length(),
               code_length.bit_length())
