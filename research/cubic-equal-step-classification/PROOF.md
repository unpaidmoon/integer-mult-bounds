# Exact classification of equal-step dyadic cubic repairs

Prepared for @CubeJerry with substantial OpenAI Codex assistance. Apache-2.0.
The fixed reader interface, chronological defect and unrestricted two-query
obstruction are due to Nick Petalas (#6200) and apoursh (#6212).
AAAmirinu's #6246 supplies the power-of-two branch. The new contribution is
the exhaustive equal-step classification, its `r = 2^s + 1` branch, and the
actual chronological repair for that branch. This is a local exact-arithmetic
result, not an admitted supplier or a runtime improvement.

## Contract and theorem

Let `R = Z[1/2]`. Three distinct streams enter with arbitrary values `(Y,A,B)`.
Retain all `r >= 3` children, in their original order and with their interiors
unchanged:

```text
y += a^3
a += b
```

The eager comparator restores `a -= b` after every child. It finishes at
`(Y + r A^3, A, B)`. Deferred restoration leaves
`(Y + sum_(j=0)^(r-1) (A+jB)^3, A+rB, B)`.
There is no intermediate observation, output feedback into sources, nonlinear
source change, child fusion or output recoding. Source transformations are
invertible linear maps over R and are charged separately. A query adds a
fixed signed R-weighted cube of a source linear form to y.

Call a three-query repair **equal-step with entry-A at an end** when its three
entry-source directions, in any order, have slopes `0,d,2d` for a nonzero
rational d: each source form is a nonzero multiple of one of
`A, A+dB, A+2dB`. Allow arbitrary nonmonic R-linear forms and arbitrary
`GL_2(R)` source frames. Every query weight is nonzero. This is a restriction
on directions in the entry coordinates, not on names of changing registers.

**Theorem.** Such a repair exists exactly when either r or r-1 is a power
of two. Necessarily `2d = r` or `2d = r-1`, respectively. After monic
normalization its three weights are unique. The construction is realizable
using only `a += c b` source shears, with b unchanged throughout.

For `r = 2^s + 1`, `s >= 1`, exactly three appended queries and three
integer source shears suffice. The unrestricted dyadic query minimum is
three by #6212; that lower bound is reused, not new. For `r = 2^s >= 4`,
the construction is exactly the five-event repair already given by #6246.
No statement excludes three unequal-step queries at any other arity.

## Coefficient elimination forces two possible spacings

The excess over the eager output, from #6200, is

```text
f_r = 3 S1 A^2 B + 3 S2 A B^2 + S1^2 B^3,
S1 = r(r-1)/2,    S2 = r(r-1)(2r-1)/6.
```

A repair subtracts f_r and restores both sources. Negating all query
weights gives a three-cube decomposition of f_r. Normalizing a physical
term `gamma (alpha A + beta B)^3`, with alpha nonzero, gives weight
`gamma alpha^3`, which lies in R. The slope `beta/alpha` may initially be
any rational: no unsupported assumption that a normalized slope is dyadic
is needed. Thus any allowed nonmonic repair implies

```text
f_r = w0 A^3 + w1 (A+dB)^3 + w2 (A+2dB)^3,   wi in R.
```

Comparing the four coefficients gives

```text
w0 + w1 + w2 = 0,
d (w1 + 2w2) = S1,
d^2 (w1 + 4w2) = S2,
d^3 (w1 + 8w2) = S1^2.
```

At each node t in `{0,d,2d}`, `t^3 = 3d t^2 - 2d^2 t`.
The last three equations therefore require
`S1^2 = 3d S2 - 2d^2 S1`. Since S1 is nonzero, substitution yields

```text
0 = 2d^2 - (2r-1)d + r(r-1)/2
  = (2d-r)(2d-r+1)/2.
```

Hence the spacing must be `r/2` or `(r-1)/2`, even if nonmonic frames
initially allowed non-dyadic slopes. Conversely, for either spacing the
first three equations determine unique weights and the node identity
implies the fourth. Uniqueness follows from the distinct nodes, or directly
from

```text
w2 = (S2 - d S1)/(2d^2),
w1 = (2d S1 - S2)/d^2,
w0 = -w1-w2.
```

Writing u=2d, the two possibilities are:

| u | w0, at slope 0 | w1, at slope u/2 | w2, at slope u |
|---|---|---|---|
| r | `-(r-1)(5r+2)/(6r)` | `2(r^2-1)/(3r)` | `(r-1)(r-2)/(6r)` |
| r-1 | `-r(5r-7)/(6(r-1))` | `2r(r-2)/(3(r-1))` | `r(r+1)/(6(r-1))` |

The first row is #6246's identity, credited in full. The second row is
the additional identity. Both are rational identities for every integer
r>=3; dyadic admissibility is a separate question.

There is also a direct quadrature interpretation of the second row.
For u=r-1, let `a=r(r+1)/(6(r-1))` and `b=2r(r-2)/(3(r-1))`.
For every polynomial p of degree at most three,

```text
sum_(j=0)^u p(j) = a [p(0)+p(u)] + b p(u/2).
```

To see this independently, center at u/2. Reflection j -> u-j kills the
odd centered moments on both sides. The constant and quadratic moments
give `2a+b=r` and `a u^2/2 = r(r^2-1)/12`, which determine a,b above.
Apply this to p(j)=(A+jB)^3 and subtract r A^3. The result is the second
row because `a-r=w0`, `b=w1`, `a=w2`. This uses classical polynomial
quadrature, not a new general quadrature theorem; the contribution is its
dyadic classification and source-restoring use at this repository interface.

## Odd primes give the exact dyadic boundary

In the first row, if an odd prime p divides r, its w2 numerator
`(r-1)(r-2)` is congruent to 2 modulo p. The denominator is divisible by
p, so that factor cannot cancel; w2 is not dyadic. In the second row,
an odd prime p dividing r-1 similarly sees numerator `r(r+1) = 2 mod p`,
again preventing cancellation. This argument includes p=3: the additional
factor 3 in the denominator does not help.

Therefore the first row requires r to be a power of two, and the second
requires r-1 to be a power of two. Rescaling the physical forms cannot hide
the obstruction: each normalized weight `gamma alpha^3` still belongs to R.
This proves necessity for all allowed nonmonic forms and source frames,
not only the displayed shear implementation.

Conversely, suppose r is a power of two. Its residue modulo 3 is 1 or 2,
so 3 divides all three displayed numerators in the first row. Cancellation
leaves denominators dividing 2r, a power of two. This is #6246's argument.
If r-1 is a power of two, r is 0 or 2 modulo 3. Thus 3 divides
`r(r+1)`, `r(r-2)` and `r(5r-7)`. The second row's denominators then divide
`2(r-1)`, also a power of two. All three weights are nonzero for r>=3.
This proves sufficiency of coefficient membership. The next section supplies
the missing chronological realization. Since consecutive positive powers
of two occur only at 1 and 2, the eligible spacing is unique for r>=3.

## Six-event restoration for r = 2^s + 1

Put `u=r-1=2^s`, `d=u/2`, and take the second row's weights. Starting from
the actual deferred endpoint `a=A+rB`, append:

```text
1. a -= b
2. y -= w2 a^3
3. a -= d b
4. y -= w1 a^3
5. a -= d b
6. y -= w0 a^3
```

The three queries see `A+uB`, `A+dB`, and A in that order. Their sum is
`-f_r`. The source returns to A, b stays B, and y becomes `Y+rA^3` for
every incoming Y,A,B. No entry snapshot, clean scratch, lost dirty value
or alteration to an original child is used. Every source shear has
determinant one and an integer coefficient. Every query is invertible
because its source does not involve y. Reversing these six events and
negating their coefficients restores the deferred endpoint; reversing each
retained child as `a -= b; y -= a^3` then restores the original entry state.

For the credited first row, u=r and the initial `a -= b` is absent;
the remaining five events are exactly #6246's schedule. Among schedules
restricted to b-preserving shears and these three query directions, the
source-shear counts are also minimal: a query cannot change a's slope.
The first row starts at one queried slope and must visit the other two,
requiring at least two changes. The second starts at the distinct slope r
and must visit all three, requiring at least three. The displayed orders
attain those bounds. This small visit-count argument is not a minimum for
arbitrary source frames or a physical movement tariff.

At the new discriminating arity r=33:

```text
f_33 = (187/32)(A+32B)^3 + (341/16)(A+16B)^3 - (869/32)A^3
     = 1584 A^2 B + 34320 A B^2 + 278784 B^3.
```

The actual repair has shears -1,-16,-16 and cube coefficients
`-187/32,-341/16,+869/32`, with the interleaving above. The first shear
is essential: applying the first cube at the deferred slope 33 corrupts
the output even if the sources are later restored.

## What is new, and what is deliberately not claimed

The existence of three queries for r=3 belongs to #6212; this formula
reproduces its identity. For `r=2^s+1`, powers of two modulo nine cycle as
`2,4,8,7,5,1`, so r cycles as `3,5,0,8,6,2`.
The #6215 pure-original-B constructions already attain three in the
classes 5,0,8,2. Its four-query floor applies to classes 3 and 6 only
when a nonzero original-B cube is required. Every direction here has a
nonzero A coefficient and so is outside that restricted family.

Relative to the three pinned predecessors, the new count cases include
`s = 5 mod 6` and `s = 1 mod 6, s>=7`: the first are r=33 and r=129.
They are not covered by #6246's power-of-two arities. The classification
also proves that this exact equal-step idea cannot extend to other r.
These are comparisons with those sources, not a literature-priority claim.

For example r=14 is excluded by the equal-step theorem but #6212 supplies
three integer queries at slopes 5,4 and the pure-B direction. The verifier
executes that credited schedule as a positive scope control. Consequently,
failure of equal-step membership is explicitly not a four-query lower bound.
The general three-versus-four dyadic classification remains open.

The location of the zero slope is also essential. At r=50 the identity

```text
f_50 = -(A-35B)^3 - 33 A^3 + 34(A+35B)^3
```

has equally spaced directions with zero in the middle. From the deferred
slope 50, visit slopes -35,35,0 with shears -85,70,-35 and subtract the
displayed cubes. This is an exact three-query repair although neither 50
nor 49 is a power of two. It is a positive control outside the stated
`0,d,2d` family, not a counterexample to the theorem or a new query minimum:
#6212 already attains three queries at r=50 because 50=2 modulo 3.

## Complete logical bill and expansion gate

Use the predecessor's complete-event prices `Q_c^a(N)` for a query
`y += c a^3` and `L_c(N)` for `a += c b`. A query price must include its
coefficient use, source access, private work/restoration and return.
Different coefficients retain different symbols. Let S_r(N) account for
all additional preparation/controller, routing, precision and storage work
not included in these complete-event prices. It is unknown, not zero.

The eager program costs

```text
E_r(N) = r Q_1^a(N) + r L_1(N) + r L_-1(N).
```

For the new branch the complete symbolic deferred bill is

```text
D_r(N) = r Q_1^a(N) + r L_1(N)
       + L_-1(N) + Q_-w2^a(N) + 2 L_-d(N)
       + Q_-w1^a(N) + Q_-w0^a(N) + S_r(N).
```

All original children remain paid. Thus a favorable replacement requires

```text
Q_-w2^a(N) + Q_-w1^a(N) + Q_-w0^a(N) + 2 L_-d(N) + S_r(N)
    < (r-1) L_-1(N).
```

If a physical backend recursively implements Q or L, its complete recurrence
must be substituted into these symbols; no recursive child may be dropped.
This package supplies no such backend, numeric inequality or admitted call.
Dyadic membership does not make coefficients free or establish rounded
correctness. Preparing r and weights, division/cancellation by 3, dispatch,
native realization, error propagation, source placement and any scratch
allocation/erasure still require the stated charges or separate proofs.
The expansion decision is to stop after this logical classification.

No new kappa. All five selected framework assumptions remain: native maps
at arbitrary column multiplicity, owned allocation/erasure, uniform compiler
closure, precision/tape implementation, and analytic recovery. This is neither
a finite-field statement nor a full multiplier proof, supplier admission,
independent human review or formal-kernel verification.

## Evidence and next questions

The written elimination and odd-prime argument prove the infinite-domain
classification. `verify.py` checks polynomial identities, exact finite
membership, literal symbolic and dirty-value schedules, their inverses and
semantic rejection controls. `crosscheck.py` derives weights by separate
exact elimination and derives the defect from concatenated reader blocks.
Neither imports predecessor executable code. These computations corroborate
the proof; their finite domains do not establish it alone. Exact executed
coverage is recorded in `RESULT.json` and `VALIDATION.md`.

Open next questions, with their first steps and blockers, are in README.md
and TASK.json. In particular, changing the direction pattern may escape this
classification; a failed equal-step search cannot close that larger problem.

## Credit

Nick Petalas (#6200) supplied the fixed cubic reader, defect, rational query
criterion and restoring-schedule question. Apoursh (#6212) supplied the
dyadic localization obstruction, the unrestricted three-query lower bound
for r>2, earlier three/four-query constructions and the known r=3 identity;
apoursh (#6215) supplied the pure-original-B boundary and its attainments.
AAAmirinu (#6246) supplied the entire power-of-two branch, the two-shear
chronology and its proof. Sricharan Vagvala/theon199 (#1532), Adam Gall
(#1205) and Hanson Sun (#1246) retain the quadratic and linear lineage.
Coefficient comparison, Vandermonde uniqueness and localization arguments
are classical. Source proofs are retained or source-pinned unchanged.
