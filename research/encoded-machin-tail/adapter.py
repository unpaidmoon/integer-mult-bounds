"""Stop PR3709 before its first zero floor term.

Adapted from Jose Manuel / jmbarrancoml's encoded arctangent. Apache-2.0.
The stopping comparison and explicit iterator closure are new here.
"""

from contextlib import closing


def arctangent(unit, terms, denominator):
    from cardinal_counts import Count
    from ring_words import Signed
    from router_metadata import indices, owned
    from twiddle_setup import compare, interval_sum, padded, quotient
    from words import need

    need(denominator in (5, 239), "fixed Machin denominator")
    square = 25 if denominator == 5 else 57121
    lower, upper = Signed(Count.literal(0)), Signed(Count.literal(0))
    power, odd = Count.literal(denominator), Count.literal(1)
    negative = False
    try:
        # Closing is explicit: a stop must release the encoded loop counters.
        with closing(indices(terms)) as positions:
            for _ in positions:
                with owned(Count.product(power, odd)) as (divisor,):
                    if compare(divisor, unit) > 0:
                        break
                    with owned(quotient(unit, divisor)) as (lo,):
                        with owned(Count(lo)) as (hi,):
                            hi.increment()
                            following = interval_sum(lower, upper, lo, hi, negative)
                lower.close()
                upper.close()
                lower, upper = following
                negative = not negative
                power.multiply_small(square)
                odd.increment()
                odd.increment()
        with owned(Count.literal(1)) as (tail,):
            return padded(lower, upper, tail)
    finally:
        lower.close()
        upper.close()
        power.close()
        odd.close()
