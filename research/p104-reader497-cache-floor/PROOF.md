# Reader 497: the exact cost of retaining both operands

Jerry Chen (@CubeJerry), with substantial OpenAI Codex assistance. Apache-2.0.
This is a scoped written proof supported by an exhaustive integer certificate,
not proof-assistant verification. Source construction credit is retained below
and in README.md.

## 1. Source-bound interface

Use Ali Romman's PR6167, head
`564a076b113621a93edc4e39968ee4e4a8c9caf0`, as retained on canonical main
`2485805a6d47f36ea83ddde6327d453ac82d44dc`. Its word is an input, not imported
code. Event numbers below are zero-based in that exact word.

Let `S`, `U`, `H`, `L`, `R` denote its frames 519, 520, 529, 595, 914.
Direct binary span calculations give

    dim(S,U,H,L,R) = (3,6,7,1,7),
    S <= U, L <= U, H intersect R = U, S intersect L = {0}.

These are statements about the actual subspaces, not just their dimensions.
The source has the following receiver/root operations. Other source operations
and all productive endpoints are fixed.

| Event | Operation |
|---|---|
| 12888 | reader 497: frame 3 (zero space) to S |
| 12933 | reader adds the current value V of register 48 at S |
| 12934 | reader: S to U |
| 12935 | reader adds the current value B of register 228 at U |
| 13485 | owned root 772: H to U |
| 13486 | reader adds -4 times the current root value Q at U |
| 13487 | root: U to L |
| 15462 | reader: U to R |
| 15572 | consumer 161 reads reader 497 at R |

There is no other use of reader 497 between events 12888 and 15572. A complete
scan checks this, including outgoing reads. If its incoming value is A, the
required outgoing value is `A+V+B-4Q`. Treating these four values as independent
is a valid local identity test; the actual source can substitute any correlated
values into that identity. Exploiting correlations to replace one of the three
required deliveries is outside the model below.

The five original MOVE ranks are **3,3,1,5,1**, with total rank 13. Root Q must
still reach L for its other readers; reader 497 must still reach R for the
unchanged consumer. These costs cannot disappear at the selected cut.

## 2. The quantified model and the favorable relaxation

We test the following extension of the successful reader-451 retention idea:

1. Reader 497 starts in the zero frame, ends in R and only ascends by subspace
   inclusion. Root 772 starts loaded at H, ends loaded at L and only descends.
   Arbitrarily many intermediate frames are permitted, including frames not
   present in the original word's list.
2. The reader receives V, B and -4Q once each, by the same scalar additions.
   The root supplies Q directly at one common frame F. It is not cloned,
   encoded, split, mixed with the operands, or replaced by another carrier.
3. Each of V and B is supplied at its original source cut/frame, S and U
   respectively. It may be kept in one owned copy and transported downwards
   along any finite chain before delivery. The two caches do not mix with
   each other or other fields. Their source fields are not changed. A direct
   original read is the zero-distance special case.
4. No productive target is added, split or debited. No other original work is
   removed. Frames outside these paths, source computation and the consumer
   remain fixed.

For a lower bound, grant enough clean owned storage, arbitrary waiting, free
INIT/COPY/CLEAR and free ordinary control/routing. **Every native cache MOVE
is charged.** These are favorable assumptions, not free physical resources
claimed for an implementation. Actual allocation, source access, copying,
erasure, routing, precision and storage have nonnegative additional charges.
The original schedule uses no new caches. Therefore failure even in this
relaxation rules out a gain in this model before those charges are added.

The executable templates explicitly contain two INITs, two source COPYs, two
CLEARs and all three additions; they record these operations rather than
silently deleting them. They demonstrate local normalized-chart identities,
not a new native implementation or globally scheduled supplier.

## 3. Reduction from arbitrary frames and lengths to 126 recipes

Let A_V, A_B be the reader frames at which the retained V and B are delivered,
with dimensions a and b, and let f=dim(F). Owned descent gives A_V <= S and
A_B <= U. Root descent gives L <= F <= H; reader ascent and its fixed exit give
F <= R. Consequently `L <= F <= U=H intersect R`.

The reader's contact frames are comparable. F cannot precede A_V, nor equal it:
that would imply `L <= F <= A_V <= S`, contradicting `S intersect L = {0}`.
Thus A_V is strictly below F. The necessary dimension domain is exactly

    0 <= a <= 3,  0 <= b <= 6,  1 <= f <= 6,  a < f.

There are `7*(1+2+3+4+4+4) = 126` triples. All are geometrically feasible in
the relaxed model: choose any a-space in S, extend it with the independent line
L to an f-space in U, and place the b-space below, between, or above these
spaces along an extended flag in U. Thus no restriction to the source's
finite frame list is being used. A separate closure enumeration of all 2,825
subspaces of U verifies 52,964 actual comparable contact triples and recovers
exactly the same 126 dimension recipes.

Let phi(0)=0 and let phi be nonnegative, increasing and concave on the required
integer ranks. Subadditivity, `phi(x)+phi(y) >= phi(x+y)`, follows from concavity
and phi(0)=0. Compressing any unused intermediate stops can therefore only
decrease cost. After compression, sort `[0,a,b,f,7]` and take successive
positive gaps. The complete optimistic paid multiset is

    reader: consecutive positive gaps in sorted [0,a,b,f,7]
    V cache: 3-a, if nonzero
    B cache: 6-b, if nonzero
    root: 7-f and f-1, omitting zero.

The total transported rank is `22-a-b`; forgetting cache transport would
instead (incorrectly) make it 13 independently of the retained input frames.
Every rank is at most six. Longer monotone paths cannot undercut this compressed
bill. The actual input capture times may impose additional restrictions; ignoring
them enlarges the feasible class and is valid for the lower bound.

## 4. A general proof of the minimum

The minimum does not depend on enumerating binary subspaces. More generally,
let dim(S)=s, dim(U)=u, dim(H)=dim(R)=u+1, dim(L)=1, with
`1 <= s <= u-1`, `H intersect R=U`, `S,L <= U`, and `L` not contained in S.
The same two-cache model, over any field of frame coordinates, has minimum

    phi(s) + phi(u-s) + 2 phi(1) + phi(u-1).

Here phi is increasing and concave with phi(0)=0; the assertion is about
rank tariffs, not a physical realization over every field. The source case is
`(s,u)=(3,6)`. Its compressed domain is `0<=a<=s`, `0<=b<=u`, `1<=f<=u`, `a<f`.

**First move B's delivery to U without increasing the bill.** If b<=f,
remove the b-contact from the reader path. Merging the adjacent reader moves
cannot increase cost. Adding the new contact at U splits the final reader
move of size u+1-f into u-f and 1. This increases reader cost by at most

    phi(u-f)+phi(1)-phi(u+1-f) <= phi(u-f) <= phi(u-b).

The last quantity is precisely the B-cache transport removed. The inequalities
include b=f and f=u, where one of the contacts or moves is redundant. If b>=f,
the old reader tail plus B-cache cost is

    phi(b-f) + phi(u+1-b) + phi(u-b)
      >= phi(u-f) + phi(1),

by subadditivity on the first and third terms, then monotonicity on the second.
The right side is the tail after moving delivery to U. These transformations
are legal in the favorable model: remove the B-contact and retain its source
value at U until the reader reaches U; the other contacts stay unchanged.

Thus assume b=u. The remaining exact compressed cost is

    phi(a)+phi(f-a)+phi(u-f)+phi(1)
       +phi(s-a)+phi(u+1-f)+phi(f-1).

For f>=2, both root segments u+1-f and f-1 are between 1 and u-1. Concavity
minimizes their fixed-sum cost at the extremes 1,u-1. Also

    phi(a)+phi(s-a) >= phi(s),
    phi(f-a)+phi(u-f) >= phi(u-a) >= phi(u-s).

Adding these inequalities proves the stated minimum. For f=1, a=0, and the
cost is `phi(s)+phi(u-1)+2 phi(1)+phi(u)`, which is at least the bound because
`phi(u)>=phi(u-s)`. This completes the all-length, all-dimension proof.

For phi(r)=r^t, 0<t<1, the optimum is unique at the dimension level. At f=1
the last inequality is strict since s>0. At 2<=f<u, both f-a and u-f are
positive, so their subadditivity inequality is strict. At f=u, a<s gives a
strict monotonicity inequality. Finally, when f=u and a=s, any b<u retains
a positive B-cache cost and can only split the original reader path further.
Therefore equality requires `(a,b,f)=(s,u,u)`. The original schedule attains it.

This is the geometric distinction from reader 451: its earlier operand is at
frame 737, which **does** contain L=frame 595. The forced inequality a<f no
longer follows there. The theorem therefore does not contradict PR6167's
successful retained-operand rewrite.

The incidence condition is essential even at the same dimension tuple.
Replace S by the span of L and two independent vectors from the original S,
keeping its dimension three and leaving U,H,L,R fixed. Take A_V=S, A_B=U,
F=L; the root is now read before V. The emitted normalized-chart template
still returns `A+V+B-4Q`, with paid ranks `(1,1,2,3,6)`. Its gain over the
original bill is `3^t+5^t-2^t-6^t>0`, because the increments of x^t strictly
decrease. This is a **changed-geometry positive control**, not a way to replace
the actual source frame for free. It shows why a dimension-only argument
omitting the incidence hypothesis would be false.

## 5. Exact concave-order certificate and quantitative gap

For a paid multiset P define `M_k(P)=sum_{r in P} min(r,k)`, k=1,...,6. The
original multiset P0=(1,1,3,3,5) has

    (M_1,...,M_6)(P0) = (5,8,11,12,13,13).

CERTIFICATE.json lists the paid ranks and all six integer differences
`M_k(P)-M_k(P0)` for every one of the 126 triples. Each difference is
nonnegative. The following table gives the coordinatewise minimum of those
differences at each f (the minima need not be attained by the same triple).

| f | Number of recipes | k=1 | k=2 | k=3 | k=4 | k=5 | k=6 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 7 | 0 | 0 | 0 | 1 | 2 | 3 |
| 2 | 14 | 1 | 2 | 1 | 2 | 2 | 2 |
| 3 | 21 | 1 | 3 | 2 | 2 | 1 | 1 |
| 4 | 28 | 1 | 2 | 2 | 1 | 0 | 0 |
| 5 | 28 | 1 | 2 | 1 | 1 | 0 | 0 |
| 6 | 28 | 0 | 0 | 0 | 0 | 0 | 0 |

This is a complete finite integer certificate, not a failed heuristic search.
Its formula above and six checks per row provide a small standalone replay:

    for f = 1,...,6:
      for a = 0,...,min(3,f-1):
        for b = 0,...,6:
          construct the paid multiset in section 3
          check its six capped sums against (5,8,11,12,13,13)

To see why these finitely many integer inequalities imply a continuum of
tariff inequalities, put `d_k=phi(k)-phi(k-1)`,
`lambda_k=d_k-d_(k+1)` for k<6 and `lambda_6=d_6`. Increasing concavity makes
each lambda nonnegative, and direct telescoping gives, for 0<=r<=6,

    phi(r) = sum_{k=1}^6 lambda_k min(r,k).

Multiplying the six capped-sum differences by these coefficients proves

    sum_{r in P} phi(r) >= 2 phi(1) + 2 phi(3) + phi(5).

Only `(a,b,f)=(3,6,6)` has all six differences zero. For `phi(r)=r^t`,
0<t<1, all six coefficients are positive. Every other recipe is strictly
more expensive. The equality recipe forces A_V=S and A_B=F=U, exactly the
original delivery frames. The original source schedule attains the bound
without adding the optional stationary caches.

Moreover every f<6 row has its k=4 difference at least one. Deleting the
root's U meeting therefore has the uniform strict penalty

    new bill - original bill >= 2*4^t - 3^t - 5^t > 0,  0<t<1.

The last strict inequality is strict concavity. This is a bound for all powers
in that interval, not an inference from a sampled exponent or decimal root.

## 6. Consequence and boundary of the result

For the unchanged PR6167 caller, every local paid increase is repeated in its
18 local invocations; productive targets and the remaining caller work stay
fixed. Hence these changes cannot improve the complete signed target-minus-paid
moment. Adding the omitted nonnegative ordinary/storage costs cannot repair
that obstruction. No compiler threshold, new supplier, or new kappa is claimed.

This is not a proof that root 772's frame-520 stage is unavoidable in every
construction. Mixed/correlated source representations, a changed earlier prefix,
public ascending carriers, new productive helpers, root cloning, a different
consumer cut, or coordinated removal of other paid work are not covered.
Nick Petalas's PR6163 excludes a different receiver-only repair after an operand
is dropped. Here both operands are preserved through explicit charged caches;
the conclusion is an exact cost floor, not an endpoint impossibility.

Ali Romman retains PR6167/PR5827 credit; DreamingOfClouds retains
PR6144/PR6030/PR5907 and toolkit PR6170 credit; Nick Petalas retains PR6163
credit. Matarener's PR6214 corroborates the source word and repeats this open
question. Earlier native, caller, compiler and BIT contributors retain their
source attribution. No predecessor implementation has been copied into the
checker, and no independent human or proof-kernel review is asserted.
