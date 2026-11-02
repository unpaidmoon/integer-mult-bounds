# A drift orbit and its correction-state consequence

This contribution is produced by Nick Petalas. New work is Apache-2.0.

## Fixed maps and inherited facts

Use precisely PR5492's four signed rank-one recipes. In their stored order,
the edges are `0→29`, `0→2`, `2→341`, `29→341`. One cycle applies the first
backwards, the second and third forwards, and the fourth backwards. Denote
this rounded map by C. PR5492 already identifies the cycle as an ideal
Gaussian-rational identity and proves that its independently rounded edges
need not be flat. Those facts and its original witness are inherited.

For Gaussian integers a,b, define L_epsilon by

```text
D = a-b
S = b + floor(D/2)
E = epsilon*i*D
B = S - floor(E/2)
A = B+E
L_epsilon(a,b) = (A,B),     epsilon in {+1,-1}.
```

Floors act separately on the real and imaginary components. This is the
retained pair convention, with epsilon=-1 for an inverse edge. Signed affine
wrappers are exact coordinate permutations and powers of i. The verifier
imports no predecessor executable.

## A four-coordinate invariant circuit

Let V be the Gaussian-integer sublattice supported on coordinates
`(1,10,39,44)`. Write its entries as `(a,b,c,d)`. The source recipes restrict
to the following four stages. In each row both pair operations read the
same incoming vector, and their output assignments occur simultaneously.

| Stage | First pair and assignments | Second pair and assignments |
|---|---|---|
| 0 | `(A,B)=L_-(a,-c)`; `c'=iA, a'=-iB` | `(P,Q)=L_-(b,-d)`; `b'=P, d'=-Q` |
| 1 | `(A,B)=L_+(a,-b)`; `a'=A, b'=-B` | `(P,Q)=L_+(-id,ic)`; `c'=P, d'=-Q` |
| 2 | `(A,B)=L_+(-ic,ia)`; `a'=A, c'=-B` | `(P,Q)=L_+(b,-d)`; `b'=P, d'=-Q` |
| 3 | `(A,B)=L_-(a,-b)`; `a'=A, b'=-B` | `(P,Q)=L_-(c,-d)`; `d'=iP, c'=-iQ` |

The complete wrapper plans verify this restriction exactly. Every active
kernel input is paired with another active input, every output returns to
V, and the complementary zero pairs stay zero. Consequently C maps V to V.
The circuit is also recorded as eight pairs of integer/phase tuples in
`verify.py:CIRCUIT`. `derive_circuit` reconstructs every tuple from the
byte-authenticated source recipes; it does not infer support from probes.

## Integral-shift lemma

Suppose a pair is shifted by `(u,v)` with both components of `u-v` even.
Then for every Gaussian-integer a,b,

```text
L_epsilon(a+u,b+v) = L_epsilon(a,b) + U_epsilon(u,v),
```

where U_epsilon is the ideal linear pair obtained by replacing each floor
with exact division by two. Indeed
`floor((z+2m)/2)=floor(z/2)+m` componentwise, and multiplication by
`epsilon*i` preserves evenness. Substitute this equality into D,S,E,B,A.
The shift term is independent of a,b. The same proof works for every
integer multiple of `(u,v)`, including negative multiples. Exact monomial
wrappers transport the shift linearly.

Define

```text
x = (3+2i, 1, 3i, 3+i)
delta = (-4+4i, 4+4i, 4+4i, 4-4i).
```

Transporting delta through the four ideal stages gives this exact certificate.

| Cut | Shift on `(a,b,c,d)` |
|---|---|
| Entry | `(-4+4i, 4+4i, 4+4i, 4-4i)` |
| After 0 | `(8i, 0, 0, -8i)` |
| After 1 | `(-4+4i, -4-4i, -4-4i, 4-4i)` |
| After 2 | `(-8, 0, 0, 8)` |
| After 3 | `(-4+4i, 4+4i, 4+4i, 4-4i)` |

Every incoming shifted pair difference is even. The verifier checks all
eight differences before division, using the displayed circuit. Hence the
lemma proves, for every v in V and every integer k,

```text
C(v+k*delta) = C(v)+k*delta.                         (1)
```

This universal statement follows from parity and the floor identity. The
128 random fixtures only corroborate it.

## Finite orbit certificate

Executing the fixed circuit 24 times on x gives

```text
C^24(x) = (-1+6i, 5+4i, 4+7i, 7-3i) = x+delta.      (2)
```

The verifier enumerates all 25 cycle boundaries and all 96 internal edge
boundaries. Every internal boundary agrees with a second interpreter on
all 512 coordinates. That interpreter separately decodes each signed affine
wrapper using explicit bit sums and uses these component formulas for L_+.
For `D=(r,s)` and `b=(p,q)`,

```text
A = (p+floor(r/2)-floor(s/2), q+floor(s/2)+ceil(r/2))
B = (p+floor(r/2)+ceil(s/2), q+floor(s/2)-floor(r/2)).
```

L_- exchanges A and B. These follow directly from the pair definition,
using `ceil(t/2)=t-floor(t/2)`. The finite domain `[-3,3]^4` corroborates the
formula and exact pair inverse on all 2,401 Gaussian input pairs. The full
orbit and the hash of its 96 cuts are printed in the generated receipt.
Equation (2) is a finite exact computation, not a universal theorem inferred
from samples.

Combining (1) and (2) by induction proves

```text
C^(24k)(x) = x+k*delta,       k >= 0.                (3)
```

More generally, if `0<=r<24`, then
`C^(24k+r)(x)=C^r(x)+k*delta`. The bounded replay checks 769 consecutive
instances of this formula. Since delta is nonzero, (3) proves infinite
order and unbounded defect relative to the ideal identity. Its squared
Euclidean norm is `8*4^2=128`, so the defect is `8 sqrt(2) k` after `24k`
traversals. No minimal drift period is asserted.

For every integer g>=0, execute the same integer-coordinate convention on
`h Z[i]^512`, h=2^-g. Scaling (3) gives exactly
`C_h^(24k)(h x)=h x+k h delta`. Therefore no finite absolute defect envelope
independent of path length exists at any fixed grid. This does not preclude
a path-length-dependent error budget or a changing grid.

## Exact correction requires growing side information

Fix K>=0. Suppose a correction service receives only an unchanged rounded
payload y and a tag s in a finite set S. Its deterministic decoder D must
recover every original v in V after each permitted length `0,24,...,24K`.
Tag generation may depend arbitrarily on v and the path. The decoder has no
separate path length, saved original or other path-dependent input.

For each k in `0,...,K`, choose `v_k=x-k*delta` and use path length 24k.
Equations (1) and (3) give

```text
C^(24k)(v_k) = C^(24k)(x-k*delta) = x.
```

All final payloads are identical. The originals v_k are pairwise distinct
because delta is nonzero and Gaussian-integer addition is torsion-free.
Their tags must therefore be pairwise distinct: otherwise the same decoder
input `(x,s)` would have two different required outputs. Thus `|S|>=K+1`.
A b-bit fixed-width tag has at most `2^b` states, giving
`b>=ceil(log2(K+1))`. There is no fixed finite tag alphabet that works for
all K under this contract. The checker executes the collision family for
K=32, with 33 distinct original vectors and one common final payload.

The all-input premise matters. The collision originals have increasing
magnitude, so this argument does not give a uniform-in-K lower bound on a
fixed bounded source box. Giving the decoder a path counter, the original
input or a modified payload changes the information contract. Reversing a
known complete path remains exactly possible and is not contradicted.

## Diagnostic bill and remaining obligations

One traversal consists of exactly four rank-one native edges. The finite
24-traversal certificate therefore uses 96 native edges and 192 signed
wrappers. Its reduced circuit uses 192 active Gaussian pairs; the independent
full-bank interpreter executes 24,576 pairs and decodes all 98,304 wrapper
entries. These are diagnostic verification operations, not recursive costs
claimed for a production supplier. The 24,576 pairs exclude the separate
covariance, oracle and control computations. They are not a whole-verifier
operation count.

The scalar reference uses ordinary unbounded integers, floor division,
monomial preparation and array accesses. Physical tape movement, ownership,
precision overflow, setup/cleanup and recursive child costs are not supplied
by this checker and are not assigned zero. Receipt hashes authenticate
finite inputs and outputs; they are not human or proof-kernel review.

PR5492's cycle joins occurrences on different fields, so no repeated
chronological supplier segment is constructed. The result is an obstruction
to path-independent exact rounded frame service and to a path-length-free
absolute error envelope for the specified edges. It does not refute the
conditional selected supplier, arbitrary rounding policies or integer
multiplication. All five selected framework assumptions remain explicit.
