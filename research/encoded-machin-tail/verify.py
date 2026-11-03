"""Exact interval, encoded resource and complete twiddle checks; writes nothing."""

from contextlib import contextmanager
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import sys
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from runtime import HERE, opened, require, selected
from controls import run as control_checks


def signed(value):
    from words import RIGHT
    tape = value.magnitude.tape
    cells = getattr(tape, "physical", tape).cells
    end = cells.index(RIGHT, 1)
    number = sum(bit << i for i, bit in enumerate(cells[1:end]))
    return -number if value.negative else number


def interval(unit, terms, denominator, stop):
    total, negative, power, odd, used = [0, 0], False, denominator, 1, 0
    for _ in range(terms):
        divisor = power * odd
        if stop and divisor > unit:
            break
        lo = unit // divisor
        total[0] += -lo - 1 if negative else lo
        total[1] += -lo if negative else lo + 1
        negative = not negative
        power *= denominator**2
        odd += 2
        used += 1
    return (total[0] - 1, total[1] + 1), used


def rational_checks():
    cases, strict, equality, digest = 0, 0, 0, sha256()
    for denominator in (5, 239):
        for exponent in range(1, 257):
            unit = 1 << exponent
            terms = exponent + 8
            old, _ = interval(unit, terms, denominator, False)
            new, used = interval(unit, terms, denominator, True)
            middle = sum(((-1)**j * Fraction(1, (2*j+1)*denominator**(2*j+1))
                          for j in range(used)), Fraction())
            following = middle + (-1)**used * Fraction(1, (2*used+1)*denominator**(2*used+1))
            require(Fraction(new[0], unit) <= min(middle, following)
                    and max(middle, following) <= Fraction(new[1], unit), "alternating enclosure")
            require(old[0] <= new[0] <= new[1] <= old[1], "old interval contains new")
            require(new[1] - new[0] == used + 2, "exact stopped width")
            divisor = (2*used+1)*denominator**(2*used+1)
            require(divisor > unit and used < terms, "first omitted floor is zero")
            require(used == 0 or (2*used-1)*denominator**(2*used-1) <= unit, "minimal stop")
            cases += 1
            strict += (new != old)
            digest.update(json.dumps([denominator, exponent, new, used]).encode())
        for index in range(12):
            divisor = (2*index+1)*denominator**(2*index+1)
            for unit in (divisor-1, divisor, divisor+1):
                _, used = interval(unit, index+3, denominator, True)
                require(used == index + (unit >= divisor), "strict stopping inequality")
                equality += 1
    precision_cases = 0
    for precision in range(16, 513):
        t = precision + 64
        r = precision + (t-1).bit_length() + 12
        j = precision + 8
        counts = [interval(1 << r, j, d, True)[1] for d in (5, 239)]
        require(sum(counts) < 2*j, "strict source division reduction")
        precision_cases += 1
    return dict(interval_cases=cases, strict_containments=strict, equality_cases=equality,
                source_precision_cases=precision_cases, transcript=digest.hexdigest())


@contextmanager
def meter(module):
    from records import Tape
    total = dict(reads=0, writes=0, moves=0, divisions=0, comparisons=0)
    originals = {name: getattr(Tape, name) for name in ("read", "write", "step")}
    quotient, compare = module.quotient, module.compare

    def read(tape):
        total["reads"] += 1
        return originals["read"](tape)

    def write(tape, symbol):
        total["writes"] += 1
        return originals["write"](tape, symbol)

    def step(tape, direction):
        total["moves"] += 1
        return originals["step"](tape, direction)

    def divide(*args, **kwargs):
        total["divisions"] += 1
        return quotient(*args, **kwargs)

    def comparison(*args):
        total["comparisons"] += 1
        return compare(*args)

    with patch.object(Tape, "read", read), patch.object(Tape, "write", write), \
         patch.object(Tape, "step", step), patch.object(module, "quotient", divide), \
         patch.object(module, "compare", comparison):
        yield total


def blank_pool(pool):
    from words import BLANK
    require(not pool.live, "all scratch leases returned")
    require(all(t.head == 1 and all(x == BLANK for x in t.cells) for t in pool.tapes),
            "scratch erased with origin heads")


def pi_case(module, precision, stop):
    from cardinal_counts import Count
    from check_support import no_decode
    from scratch_pool import ScratchPool
    from session import OuterScope, erase_marker, sealed_constructors
    t = precision + 64
    r = precision + (t-1).bit_length() + 12
    unit, terms = Count.literal(1 << r), Count.literal(precision+8)
    before = tuple((bytes(x.tape.cells), x.tape.head) for x in (unit, terms))
    pool = ScratchPool(256)
    scope = OuterScope(pool)
    try:
        with selected(module, stop), meter(module) as work:
            with sealed_constructors(), scope.installed():
                with no_decode():
                    lower, upper = module.pi_interval(unit, terms)
                try:
                    result = (signed(lower), signed(upper))
                finally:
                    lower.close()
                    upper.close()
        require(before == tuple((bytes(x.tape.cells), x.tape.head) for x in (unit, terms)),
                "Machin input tapes and heads preserved")
        require(not pool.live, "Machin early stop closes encoded iterator")
        for tape in pool.tapes:
            erase_marker(tape)
        blank_pool(pool)
        counts = [interval(1 << r, precision+8, d, stop)[1] for d in (5, 239)]
        a, _ = interval(1 << r, precision+8, 5, stop)
        b, _ = interval(1 << r, precision+8, 239, stop)
        require(result == (16*a[0]-4*b[1], 16*a[1]-4*b[0]), "literal encoded Machin interval")
        require(work["divisions"] == sum(counts), "every encoded Machin division counted")
        require(work["comparisons"] == (sum(counts)+2 if stop else 0), "new stopping comparisons charged")
        return dict(Q=precision, R=r, terms=counts, interval=result, work=work, peak=pool.peak)
    finally:
        unit.close()
        terms.close()


def twiddle_case(module, precision, length, opposite, stop):
    from cardinal_counts import Count
    from check_support import bits, no_decode
    from session import erase_marker
    from words import BLANK
    unit, stage = Count.literal(precision), Count.literal(length)
    owner = module.Twiddles()
    before = tuple((bytes(x.tape.cells), x.tape.head) for x in (unit, stage))
    try:
        with selected(module, stop), no_decode():
            output = owner.run(unit, stage, opposite)
        packet = bits(output)
        require(all(bit in (0, 1) for bit in packet), "binary twiddle output")
        require(owner.closed and not owner.pool.live, "complete closed twiddle invocation")
        blank_pool(owner.pool)
        require(before == tuple((bytes(x.tape.cells), x.tape.head) for x in (unit, stage)),
                "twiddle numerical ports preserved")
        require(len(packet) == length*(precision+2), "full twiddle output extent")
        width, values = precision+2, []
        for offset in range(0, len(packet), 2*width):
            pair = []
            for start in (offset, offset+width):
                v = sum(b << i for i, b in enumerate(packet[start:start+width]))
                pair.append(v - (1 << width) if v >= (1 << (width-1)) else v)
            require(sum(x*x for x in pair) <= 1 << (2*precision), "twiddle disk")
            values.append(pair)
        output.clear()
        erase_marker(output)
        require(output.read() == BLANK, "output consumed")
        return dict(Q=precision, length=length, opposite=opposite,
                    digest=sha256(packet).hexdigest(), values=values), packet
    finally:
        unit.close()
        stage.close()


def physical_checks():
    with opened() as module:
        controls = control_checks(module, interval, signed)
        pi_rows, twiddles = [], []
        for q in (16, 21, 32, 64):
            old, new = pi_case(module, q, False), pi_case(module, q, True)
            require(old["interval"][0] <= new["interval"][0]
                    and new["interval"][1] <= old["interval"][1], "physical pi containment")
            require(all(new["work"][k] < old["work"][k] for k in ("reads", "writes", "moves", "divisions")),
                    "complete measured Machin resource reduction")
            pi_rows.append(dict(before=old, after=new))
        for q, length in ((16, 2), (16, 4), (16, 8), (17, 16), (21, 8)):
            for opposite in (False, True):
                old, before = twiddle_case(module, q, length, opposite, False)
                new, after = twiddle_case(module, q, length, opposite, True)
                require(before == after and old == new, "complete unchanged twiddle packet on finite fixture")
                twiddles.append(new)
        return dict(pi=pi_rows, complete_twiddle_packets=twiddles, controls=controls)


def main():
    result = dict(status="PASS_ENCODED_MACHIN_TAIL", rational=rational_checks(), physical=physical_checks())
    files = sorted(p for p in HERE.iterdir() if p.is_file())
    require(len(files) <= 12 and all(p.stat().st_size <= 2**20 for p in files), "bounded package hashing")
    result["package_sha256"] = {p.name: sha256(p.read_bytes()).hexdigest() for p in files}
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
