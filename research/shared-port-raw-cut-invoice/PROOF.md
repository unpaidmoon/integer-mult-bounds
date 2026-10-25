# The raw shared-port cut does not pay for its own cleanup

This is a Gaussian invoice for one changed child interface. It is not a new
decoder, a kappa, or a re-proof of the recording-only image bound.

## Source

Use `research/block3-shared-port-composition/WORD.json` and the operator
definitions in `inputs/pr4813-verify_schedule.py`. Products act on a column
from right to left. `A = C0`, `K = C0 C1 C2`, and the source identities

    B = M C2 + 2 K a,    D = Z1 V C2 W A

are the ones asserted by `load_operators`. Grades are `log2` of the uniform
support size. Every pure letter in either five-port schedule has grade 0, 1
or 3. The fused schedule's paid profile is two grade-1 calls and four grade-3
calls. The raw and fused schedules have the same final group-algebra state.

The predecessor moment charges an `Hr` call as `r^t` for real `t` in `[0, 1]`
and leaves monomials, field additions and the source's exact factor `1/2`
uncharged. That is the same exponent as `1-C` in the completion note's
`3^{1-C}` comparison. A positive gap means reward minus paid is positive.
Selected `κ` is not an input to this comparison.

## The exposed state

Index gates from zero. After raw gate 11, owner 1 is exactly

    u = B x0 + D x1 = (M C2) x0 + 2 (K a) x0 + D x1,

and no other live owner depends on `x1`. The same glue, a grade-3 term on
`x0` together with a grade-2 term on `x1`, already holds after gates 9 and 10.
`D`, `K a` and `M C2` are invertible. Therefore, for every 8-by-8 matrix `L`,
the `x1` column of `L u` is `L D`, which vanishes if and only if `L = 0`. Any
left-linear image of the five live owners with zero `x1` column must put
`L = 0` on owner 1, and then that image does not contain the summand
`2 (K a) x0`.

Isolation needs a new carrier of `D x1`. Saved original inputs are the free
bypass already allowed by the completion argument. `H`, the source's monomial
multiple of `1/2`, sends `2 K a` to `K` and does not kill `D` or `M C2`.

## What it costs to continue and to clean

Raw gate 12 is one grade-1 `A`. The state after that gate equals the fused
state after `N`. Continuing with the remaining fused gates reproduces the
fused endpoint. Dropping gate 12 does not. The resulting hybrid pays

    5 H1 + 3 H3.

That is the exposure-and-continuation bill: the fused `2 H1 + 4 H3`, plus
three rank-1 calls, minus the one rank-3 call that the raw prefix replaces.

`D = Z1 V C2 W A` uses exactly two grade-1 letters. No schedule letter has
grade 2, and a monomial preserves grade, so `D` is not one source paid letter.
A fresh copy on a saved `x1` therefore costs two `H1`. `M C2` is one `H1` on
a saved `x0`, followed by the free monomial `M`. One field subtraction for
each contaminant, then `H`, leaves the pure grade-3 unit `K x0`.

The full Gaussian bill is

    8 H1 + 3 H3.

## Moment

Credit five rank-3 jobs: the four already available from the final image, plus
this new `K`. That credit is generous. It does not charge cleanup of the
off-diagonal grade-3 terms already present in the final rows.

    gap(t) = 5 * 3^t - 8 - 3 * 3^t = 2 * 3^t - 8.

The derivative `2 ln(3) 3^t` is positive, so the maximum on `[0, 1]` is
`gap(1) = -2`. The gap is strictly negative on the whole interval.

If a new grade-2 letter equal to `D` is added to the alphabet, it replaces
only the two cleanup letters inside `D`. The bill becomes `6 H1 + 1 H2 + 3 H3`
and

    f(t) = 2 * 3^t - 2^t - 6.

Now `f'(t) > 0` if and only if `(3/2)^t > ln 2 / (2 ln 3)`. The left side is
at least 1 for `t >= 0`. The right side is strictly less than 1 because
`ln 2 < ln 9`, that is `2 < 9`. Thus `f` is increasing and
`f(1) = -2 < 0`. Widening the alphabet by this one letter does not create a
positive gap.

Leaving both contaminants uncharged, and still crediting the fifth rank-3 job,
gives gap `2 * 3^t - 5`, which equals `+1` at `t = 1`. The three cleanup
rank-1 calls are what moves that endpoint from `+1` to `-2`.

## What this does not decide

Nonlinear maps, feedback into a live owner, precision, compiler reserve and
outer transfer are outside the invoice. Each of those, if charged, adds a
nonnegative cost on a gap that is already negative. A different cut, or a
consumer that accepts the glued sum `B x0 + D x1` as one legal child, is a
different contract.
