# Even-window saturation is impossible from window six onward

## Statement

Let `k >= 3`, `T >= 1`, and let `r_1,...,r_v` be nonzero vectors in a real or
complex inner-product space of dimension `T`. Assume there are labels
`p_i` in a `2k`-dimensional symplectic vector space `V` over `F_2` and a nonzero
`w` such that

1. `b(p_i,w)=1` for every `i`;
2. for distinct `i,j`, `b(p_i,p_j)=0` implies `<r_i,r_j>=0`.

Repeated labels are allowed. Then

```text
v <= 2^k T - 1.                                      (1)
```

In particular, for the exact nonorthogonality adjacency `A` of a real line
system, if `rank_F2 A=2k` and `1` belongs to `col A`, its even window is `h=2k`
and (1) applies. At `h=6` and `h=8`, respectively, `v=8T` and `v=16T` are
impossible. This answers PR5282's first open next question in the negative.

The label reduction and the upper bound `v <= 2^k T` are prior work of
DreamingOfClouds in PR2244. Matarener's PR5282 poses the equality question and
explains its relevance to short-window decoder screens. We use those statements
as premises. The new step is the complementary-label projection identity (5).
The proof below also derives the needed counting bound to make its equality
conditions explicit; predecessor vector systems or invoices are not replayed.

## Affine basis equations

Put `H={p in V: b(p,w)=1}`. A generator is a maximal totally isotropic
subspace of `V`, hence has dimension `k`. Let `N_j` be the number of generators
in symplectic dimension `2j`, with `N_0=1`. Counting incident nonzero points
and generators gives

```text
N_j (2^j-1) = (2^(2j)-1) N_(j-1),
N_j = product_(a=1..j) (2^a+1).
```

Here generators containing a point correspond to generators of its symplectic
quotient. Write `r=N_(k-1)` and `s=N_(k-2)`, so `r=(2^(k-1)+1)s`.

Let `G` be the family of generators not containing `w`. Its size is

```text
|G| = N_k-N_(k-1) = 2^k r.
```

Each `L` in `G` meets `H` in an affine hyperplane of `L`, of size `2^(k-1)`.
Indeed, `L=L^perp`, so `w not in L` makes `b(-,w)` a nonzero functional on `L`.
Each point of `H` belongs to `r` members of `G`. Distinct `p,q` in `H` belong
together to `s` members exactly when `b(p,q)=0`, and to none otherwise.
The former count uses the symplectic quotient of the isotropic plane
`span(p,q)`. None of these generators can contain `w`, since `b(p,w)=1`.

The vectors whose labels lie in any `L` are pairwise orthogonal, including
vectors of the same label. There are at most `T` of them. Sum this inequality
over `G`. Each vector occurs `r` times, so `rv <= 2^k r T`.

Suppose equality `v=2^k T` holds. Then every one of these finite inequalities
is an equality. The vectors with labels in `L` form an orthogonal basis of
the ambient space for every `L` in `G`.

For each `p` in `H`, let `E_p` be the orthogonal projection onto the span of
the vectors carrying label `p`. Set it to zero for an unused label. The basis
condition says

```text
sum_(p in L intersect H) E_p = I      for every L in G.       (2)
```

Summing (2) over all generators gives

```text
sum_(p in H) E_p = 2^k I.                                   (3)
```

## Complementary labels force an impossible projection sum

Fix `p` in `H` and write `p'=p+w`. These are distinct points of `H` and
`b(p,p')=1`, so no generator contains both. For any other `q` in `H`,

```text
b(p',q) = b(p,q)+1 in F_2.
```

Consequently exactly one of `p,p'` is orthogonal to `q`. Sum equations (2)
over the `2r` generators containing either `p` or `p'`. The two selected labels
occur `r` times each, and every other label occurs `s` times. Therefore

```text
(r-s)(E_p+E_p') + s sum_(q in H) E_q = 2r I.                (4)
```

Substitute (3), use `r=(2^(k-1)+1)s`, and divide by `r-s`:

```text
E_p + E_(p+w) = 2^(2-k) I.                                 (5)
```

For `k>=3` the scalar `c=2^(2-k)` lies strictly between zero and one.
Choose any occupied label `p` and a unit vector `x` in the range of `E_p`.
Since orthogonal projections are positive semidefinite, (5) gives

```text
c = <x,(E_p+E_(p+w))x> = 1 + <x,E_(p+w)x> >= 1,
```

a contradiction. There is an occupied label because `v=2^k T>0`.
Thus equality cannot hold. Since `v` is an integer, (1) follows.

The restriction `k>=3` matters. At `k=2`, (5) has scalar one and two
complementary nonzero projections satisfy it. The proof makes no assertion
that they extend to an exact line system. This is an algebraic exception,
not a claimed attaining construction.

## Checkable linear certificate

The verifier enumerates maximal isotropic subspaces by unique reduced row
echelon bases for `k=2,3,4`. For every unordered pair `{p,p+w}`, it forms an
integer linear combination of the incidence rows of (2):

```text
r * sum_(L contains p or p+w) row(L) - s * sum_(L in G) row(L).
```

Its left side has coefficient `r(r-s)` at the two selected labels and zero
elsewhere. Its right side is `2r^2-s|G|=2rs`. Division gives exactly (5).
This is a finite certificate of the elimination step at the two windows in
the question and the exceptional window four. The all-`k` result comes from
the written incidence argument, not extrapolation from those computations.

No optimal asymptotic replacement for `2^k` is established. A sequence with
`v/T` tending to `2^k` as `T` increases is not excluded by (1). This result
does not close short windows below their cap, address arbitrary pairings, or
supply a native word, restoration schedule, complete signed invoice or new κ.
