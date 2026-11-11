# Three dyadic cubic queries for every power-of-two arity

Let R=Z[1/2] and r=2^s with integer s>=2. In the fixed cubic-reader
interface of Nick Petalas's PR6200, exactly three appended dyadic cube
queries suffice to repair the retained deferred children. The attaining
schedule uses two integer source shears, restores both arbitrary dirty
sources and gives exactly the eager output. Its query count is minimal by
apoursh's existing PR6212 lower bound, restated below with credit.

This proof adds a uniform attainment formula, not a new lower bound or a
runtime gain. The source inputs are the unchanged proofs at
[PR6212 head9c159482](https://github.com/CrocSwap/integer-mult-bounds/blob/9c159482e0495b6a97e17e629debe66a0ceb9466/research/dyadic-cubic-repair/PROOF.md)
and
[PR6215 head0013c2b4](https://github.com/CrocSwap/integer-mult-bounds/blob/0013c2b40c522ccd19670a8fbd4b1531f13fed2b/research/cubic-pure-b-boundary/PROOF.md),
with complete byte pins in `SOURCES.json`.

## Contract and the chronological defect

The distinct streams y,a,b enter with arbitrary values Y,A,B. Retain
exactly r original children, each with its original order and interior:

```text
y += a^3
a += b.
```

The eager comparator appends `a -= b` after each such child, so it ends
at (Y+r*A^3,A,B). Deferring those restoring shears retains the original
children and ends at

```text
(Y + sum_(i=0)^(r-1) (A+iB)^3, A+rB, B).
```

There is no observation between children, output feedback into sources,
nonlinear source change, output recoding, or child fusion. Coefficients
are fixed by r independently of the data. Source changes are invertible
R-linear maps; a signed weighted cube accumulation is one query.
Source transformations and coefficient work are paid separately. Exact
arithmetic in this interface is a premise, not a rounded or native backend.

Using the sums of first, second and third integer powers, the output
excess over the eager comparator is the credited PR6200 defect

```text
f_r(A,B) = 3S1*A^2*B + 3S2*A*B^2 + S1^2*B^3,
S1 = r(r-1)/2,
S2 = r(r-1)(2r-1)/6.
```

A restoring repair must subtract this polynomial from y and return the
actual sources (A+rB,B) to (A,B). A formal cube identity alone would not
establish that chronological source restoration.

## Uniform coefficient identity

Define

```text
c1 = (r-1)(r-2)/(6r),
c2 = 2(r^2-1)/(3r),
c0 = -(r-1)(5r+2)/(6r).
```

Then the polynomial identity is

```text
f_r(A,B) = c1*(A+rB)^3 + c2*(A+(r/2)B)^3 + c0*A^3.       (1)
```

For an independent coefficient derivation, the four relevant combinations
of weights are

```text
c1+c2+c0 = 0,
c1+c2/2 = (r-1)/2,
c1+c2/4 = (r-1)(2r-1)/(6r),
c1+c2/8 = (r-1)^2/(4r).
```

For example, the first equality has numerator
(r-1)(r-2)+4(r^2-1)-(r-1)(5r+2)=0 over denominator6r.
The other three follow by collecting over denominators6r,6r,12r.
Expanding the right side of (1) therefore gives, in the order
A^3,A^2B,AB^2,B^3,

```text
0,
3r(r-1)/2,
r(r-1)(2r-1)/2,
r^2(r-1)^2/4,
```

which are exactly the coefficients of f_r. This is a polynomial identity
over Q for every nonzero r. The power-of-two restriction below establishes
the required coefficient ring and integer shears, not the formal expansion.

For r=2^s, r is congruent to1 or2 modulo3. Thus3 divides each of

```text
(r-1)(r-2),   r^2-1,   (r-1)(5r+2).
```

For the last expression, if r=1 mod3 use r-1; if r=2 mod3 use
5r+2=0 mod3. Cancellation removes the only odd prime in the displayed
denominators: after cancelling3, c1 and c0 have denominator dividing2r,
and c2 has denominator dividing r. These are powers of two, so all three
weights belong to R. Also r/2 is an integer. For r>=4, c1,c2 are positive
and c0 is negative, hence every displayed cube query is nonzero.

This argument does not assert dyadic admissibility of the same formula
for every other integer r. For example, r=3 gives c1=1/9 in this formula,
even though PR6212 supplies a different dyadic three-query formula at r=3.

## Actual five-event restoring schedule

Start from the actual deferred endpoint, with a=A+rB and b=B. Append
exactly these five events:

```text
1. y -= c1*a^3
2. a -= (r/2)*b
3. y -= c2*a^3
4. a -= (r/2)*b
5. y -= c0*a^3.
```

The first query reads A+rB without a preliminary shift. After event2,
the source is A+(r/2)B, which event3 reads. Event4 returns it to A,
which event5 reads. Register b stays exactly B throughout. By (1), the
three signed query contributions sum to -f_r; the final state is therefore

```text
(Y+r*A^3,A,B).
```

This holds for every incoming Y,A,B. No clean register, entry snapshot,
discarded dirty value or alteration of an original child is used.
The two shears have matrices [[1,-r/2],[0,1]] and determinant1.
A query is invertible because its source is independent of its target y.
The literal inverse repair, starting at the eager endpoint, is

```text
y += c0*a^3
a += (r/2)*b
y += c2*a^3
a += (r/2)*b
y += c1*a^3.
```

It restores the deferred endpoint, not yet the original entry state.
Reversing the retained children after this inverse repair applies, for
each child in reverse order, `a -= b` followed by `y -= a^3`; that restores
(Y,A,B) exactly. No query or original child is fused in either direction.

The schedule thus attains three appended cube queries and two integer
shears. All three queried forms have entry-A coefficient1. In particular
none is a nonzero multiple of the original entry B.

## Query optimality from PR6212

We reuse the unrestricted dyadic lower bound in apoursh's PR6212; the
following is its credited argument, included to specify the exact scope.
It allows arbitrary nonmonic dyadic forms and arbitrary GL_2(R) source
frames, so it applies to the smaller shear-only construction above.

Every queried source form has R coefficients in A,B. A single weighted
cube cannot have zero A^3 coefficient and nonzero A^2B coefficient, as
f_r does. In a hypothetical two-cube representation, both A coefficients
and both weights must be nonzero. Normalize the A coefficients over Q.
The zero A^3 coefficient forces opposite normalized weights, so

```text
f_r = lambda*((A+tB)^3-(A+uB)^3),
lambda*(t-u)=S1,
t+u=S2/S1=(2r-1)/3,
t^2+tu+u^2=S1.
```

Reorder the directions so k=t-u>0. These equations imply

```text
(2r-1)^2-6k^2=3,      lambda=S1/k,      4S1=3k^2+1.
```

Writing rational k in lowest terms shows its denominator squared divides6,
so k is an integer. Reduction of the Pell equation modulo4 makes k odd.
The last identity gives gcd(S1,k)=1, hence the reduced denominator of
lambda is exactly k. Normalization cannot hide an odd prime denominator:
for an admissible nonmonic term gamma*(alpha*A+beta*B)^3, its normalized
weight gamma*alpha^3 still belongs to R. Thus lambda must be dyadic.
Since its denominator k is both odd and a power of two, k=1. The Pell
equation then gives 2r-1=3 and r=2.

For r>2, therefore, no zero-, one- or two-query dyadic repair is possible.
Together with the five-event schedule, this proves the exact appended
query minimum is three for every r=2^s>=4. It does not prove the two-shear
count optimal, compare physical tariffs, or introduce a new lower-bound
method.

## Known cases and the original-B boundary

At r=4, (1) is literally the predecessor's known identity

```text
f_4 = (1/4)*(A+4B)^3 + (5/2)*(A+2B)^3 - (11/4)*A^3.
```

That is a credited reproduction/control, not a new r=4 result. For odd
s>=3, r=2 mod3, and PR6212 already attains the exact three-query minimum
with an integer formula including an original-B cube. For s divisible by6,
r=1 mod9, and PR6215 also supplies three-query attainment. Relative to
these two pinned proofs, the remaining power-of-two residues addressed by
the uniform formula are s=2 or4 mod6, excluding the already known s=2.
This statement concerns the scope of those sources, not literature priority.

The first previously uncovered power of two in that comparison is r=16:

```text
c1=35/16,   c2=85/8,   c0=-205/16,
f_16 = (35/16)*(A+16B)^3 + (85/8)*(A+8B)^3 - (205/16)*A^3
     = 360*A^2*B + 3720*A*B^2 + 14400*B^3.
```

Its chronological repair is query -35/16, shear -8, query -85/8,
shear -8, query +205/16, all queries on current a. Since16=7 mod9,
PR6215 proves a four-query minimum in the restricted family that must
contain a nonzero cube of a nonzero scalar multiple of original B.
Our three queried forms all contain original A, so this schedule is outside
that restricted family. It does not contradict or weaken its four-query
theorem. Calling a current register b would not make a form pure-original-B;
the restriction concerns its expression in the entry coordinates.

## Complete event bill and remaining obligations

Use the source's complete-event prices Q_c^a(N) for `y += c*a^3` and
L_c(N) for `a += c*b`. A complete query price includes its coefficient use,
source access, private restoration and return. The eager bill is

```text
r*Q_1^a(N) + r*L_1(N) + r*L_-1(N).
```

The deferred schedule retains r*Q_1^a(N)+r*L_1(N) without cancellation
or child fusion, and adds the exact five-event bill

```text
Q_-c1^a(N) + L_(-r/2)(N) + Q_-c2^a(N)
             + L_(-r/2)(N) + Q_-c0^a(N).
```

Thus it replaces r restoring shears by two shears and three additional
queries; different coefficients have different tariff symbols. An event
count comparison alone gives no inequality between the two total costs.
In particular r copies of an original child are not silently replaced by
one weighted query.

For a variable arity, preparing r and the three coefficients, cancelling
the factor3, and preparing the controller/program are additional work.
Dyadic membership is not a zero-cost coefficient generator. Physical
routing, source access, precision, native query realization, private
cleanup, storage and dispatch must be covered by a genuine complete tariff
or separately charged allowance. No such backend or matched favorable
total bill is supplied here. The proof concerns exact arithmetic and does
not imply rounded execution, a finite-field implementation, supplier
admission, a global multiplication-runtime gain or a selected-frontier
change.

The unrestricted three-versus-four classification for all other integer
arities remains open beyond the cases already resolved by the sources.
Another independent question is the minimum source-transformation cost
under a specified physical tariff. Neither follows from optimality of the
number of appended cube queries.

## Attribution

Nick Petalas's [PR6200](https://github.com/CrocSwap/integer-mult-bounds/pull/6200)
supplies the cubic-reader interface, chronological defect, rational two-cube
criterion and restoring-schedule question. Apoursh's
[PR6212](https://github.com/CrocSwap/integer-mult-bounds/pull/6212) supplies
the dyadic localization obstruction, the all-r>2 three-query lower bound,
and the earlier integer/r=3/r=4 constructions. Apoursh's
[PR6215](https://github.com/CrocSwap/integer-mult-bounds/pull/6215) supplies
the pure-original-B boundary and its additional integer attainments.
Sricharan Vagvala / theon199's PR1532 retains the quadratic fixed-reader
paid-repair interface, and Adam Gall's PR1205 and Hanson Sun's PR1246 retain
the linear deferral lineage. Polynomial coefficient comparison and
binary-form decomposition are classical. No historical-priority,
independent human review or proof-kernel acceptance is claimed.
Prepared with substantial OpenAI Codex assistance. Apache-2.0.
