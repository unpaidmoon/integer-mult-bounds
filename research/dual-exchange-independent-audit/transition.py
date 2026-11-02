"""Changing-dual junction in one physical chart, Apache-2.0.

Jerry Chen (@CubeJerry), with substantial OpenAI Codex assistance. This emits
scalar ADD operations only; it does not install a physical supplier.
"""
from fractions import Fraction as Q


def need(ok, why):
    if not ok:
        raise ValueError(why)


def exact_vector(v):
    need(type(v) in (tuple, list), 'VECTOR_CONTAINER')
    need(1 <= len(v) <= 16, 'DIMENSION_BOUND')
    need(all(type(q) in (int, Q) for q in v), 'EXACT_COEFFICIENTS')
    v = tuple(map(Q, v))
    for q in v:
        need(abs(q.numerator).bit_length() <= 64, 'NUMERATOR_BOUND')
        d = q.denominator
        need(d.bit_length() <= 33 and d & (d-1) == 0, 'DYADIC_DENOMINATOR')
    return v


def compile_transition(a, b, d):
    """Replace chronological S_(a,b);S_(a,d) by L_-a;U_(b-d);L_a.

    AB=AD=1 is required. Arbitrary spare input is restored at the endpoint.
    Every emitted coefficient obeys PR5602's |q|+1 < 2**16 growth admission.
    Inputs obey PR6280's bounded exact dyadic public interface. No claim is
    made that this program minimizes cost, or that each input exchange is
    itself admitted by the stricter PR5602 physical caller.
    """
    a, b, d = map(exact_vector, (a, b, d))
    need(len(a) == len(b) == len(d), 'MATCHING_DIMENSIONS')
    need(sum(x*y for x,y in zip(a,b)) == 1, 'FIRST_DUALITY')
    need(sum(x*y for x,y in zip(a,d)) == 1, 'SECOND_DUALITY')
    e = tuple(x-y for x,y in zip(b,d))
    if not any(e):
        return []
    # Subtraction can exceed either public bit bounds or the physical scalar
    # growth admission even though both input exchanges are individually valid.
    exact_vector(e)
    need(all(abs(q)+1 < 2**16 for q in (*a,*e)), 'EMITTED_SOURCE_GROWTH')
    spare = len(a)
    lower = [('ADD',spare,i,q) for i,q in enumerate(a) if q]
    upper = [('ADD',i,spare,q) for i,q in enumerate(e) if q]
    return [(op,r,s,-q) for op,r,s,q in lower] + upper + lower
