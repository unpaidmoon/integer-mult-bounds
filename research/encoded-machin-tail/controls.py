"""Controls for the new stop, tail padding and its interrupted ownership path."""

from contextlib import nullcontext
from unittest.mock import patch

from adapter import arctangent
from runtime import require


def invoke(module, unit_value, terms_value, denominator, signed, alteration=None):
    from cardinal_counts import Count
    from check_support import no_decode
    from scratch_pool import ScratchPool
    from session import OuterScope, sealed_constructors
    unit, terms = Count.literal(unit_value), Count.literal(terms_value)
    pool = ScratchPool(64)
    scope = OuterScope(pool)
    before = tuple((bytes(x.tape.cells), x.tape.head) for x in (unit, terms))
    quotient, count = module.quotient, [0]

    def observed(*args, **kwargs):
        count[0] += 1
        if alteration == "failure" and count[0] == 2:
            raise ValueError("injected division failure")
        return quotient(*args, **kwargs)

    manager = nullcontext()
    if alteration == "no_stop":
        manager = patch.object(module, "compare", lambda _a, _b: 0)
    elif alteration == "equality_stop":
        compare = module.compare
        manager = patch.object(module, "compare", lambda a, b: 1 if compare(a, b) >= 0 else -1)
    elif alteration == "no_padding":
        padded = module.padded

        def without_padding(lower, upper, _tail):
            zero = Count.literal(0)
            try:
                return padded(lower, upper, zero)
            finally:
                zero.close()

        manager = patch.object(module, "padded", without_padding)
    try:
        with manager, patch.object(module, "quotient", observed):
            with sealed_constructors(), scope.installed():
                with no_decode():
                    lower, upper = arctangent(unit, terms, denominator)
                try:
                    return (signed(lower), signed(upper)), count[0]
                finally:
                    lower.close()
                    upper.close()
    finally:
        require(not pool.live, "control returns all leases, including early-stop counters")
        pool.empty()
        require(before == tuple((bytes(x.tape.cells), x.tape.head) for x in (unit, terms)),
                "control preserves borrowed inputs")
        unit.close()
        terms.close()


def run(module, interval, signed):
    from fractions import Fraction
    controls = []
    for alteration in (None, "no_stop", "equality_stop", "no_padding"):
        actual, count = invoke(module, 5, 4, 5, signed, alteration)
        expected, used = interval(5, 4, 5, True)
        if alteration is None:
            require((actual, count) == (expected, used), "strict equality boundary positive control")
        elif alteration == "no_padding":
            # arctan(1/5) < 1/5, while this mutant returns lower endpoint 1/5.
            require(Fraction(actual[0], 5) >= Fraction(1, 5), "omitted-tail mutant exposed")
            controls.append(alteration)
        else:
            require((actual, count) != (expected, used), "stop/resource mutant rejected")
            controls.append(alteration)
    for unit, terms, denominator, alteration, message in (
        (1, 8, 7, None, "fixed Machin denominator"),
        (1 << 35, 24, 5, "failure", "injected division failure"),
    ):
        try:
            invoke(module, unit, terms, denominator, signed, alteration)
        except ValueError as error:
            require(message in str(error), "intended failure diagnostic")
            controls.append(message)
        else:
            raise ValueError("missing control rejection")
    return controls
