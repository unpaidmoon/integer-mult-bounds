<!-- SPDX-License-Identifier: Apache-2.0 -->

# Sharp anchor boxes with distinct directions and sparse zeros

This scoped algebraic construction is produced by Nick Petalas. It builds on
Aaron Wang/navinor's rational three-total core and directed-box definition,
and Sagar Thakrar's PR #3445 twelve-line obstruction question. The new result
is the explicit family of distinct bases with preserved canonical anchors.
The core, canonical normalization, SG implication and F-star definitions
retain their predecessor credit. No predecessor theorem is re-proved here.

## Statement

For every pair of positive integers k,s there are rational matrices P,Q with
3ks rows and three columns such that M=P Q^T has the following properties:

1. M has rank three and nonzero diagonal.
2. Each factor has exactly 3k distinct projective row directions, each with
   multiplicity s.
3. Every matrix row and column has exactly 2s zero entries.
4. Every canonical tied set has size two, and the directed sub-anchor box is
   exactly 2ks. The maximum total size of two disjoint ordered nonzero blocks
   is also exactly 2ks.

An ordered nonzero block requires every forward scalar entry in its induced
order to be nonzero. A directed sub-anchor witness assigns binary labels
(a_i,b_i) within the supplied canonical anchors (A_i,B_i), has a_i dot b_i=1,
and has a_i dot b_j=0 whenever i precedes j and M_ij=0. All binary dots are
in F_2. We retain the original whole-instance canonical anchors.

The case k=4,s=1 has twelve distinct directions in each factor, two zeros in
each row and column, and box exactly eight. Thus the two-thirds box ratio can
be sharp without repeated directions and with only two scalar zeros per row.
These properties satisfy the necessary restrictions in PR #3445. They do not
contradict that theorem or give a counterexample to its eight-row target.

## Construction

Use the credited core as displayed in PR #3445:

    P0 = [[-1,-3, 0], [ 1,-1,-2], [3, 3,3]],
    Q0 = [[ 1,-3, 2], [ 3,-1,-2], [3,-1,2]],
    D  = P0 Q0^T = diag(8,8,12).

Let u=(1,1,1)^T, v=(1,1,-2)^T and N=u v^T. Since v^T u=0, N^2=0.
For t=0,...,k-1 put

    A_t = I + 4t N,
    C_t = D A_t^(-T) D^(-1),
    P_t = A_t P0,
    Q_t = C_t Q0.

Stack the k triples (P_t,Q_t), then repeat each paired row s times. These
repetitions preserve all matrix entries between corresponding row types.
The parameter 4 is chosen to preserve the canonical anchors under the
unequal diagonal valuations of D. No normalization on a row subset is used.

## Scalar matrix and zero pattern

Nilpotence gives A_t^(-1)=I-4tN and A_t A_r^(-1)=I+4(t-r)N. Hence

    P_t Q_r^T = (I+4(t-r)N)D.

For row i and column j in these triples the entry is

    (delta_ij + 4(t-r)v_j)D_j.

When t=r, it is D on that triple. When t differs from r, every entry is
nonzero: off-diagonal entries have nonzero factors, while each diagonal
coefficient 1+4(t-r)v_i is an odd integer and cannot vanish. Consequently the
only zeros join distinct local row types inside the same triple. After
repetition, each row and column has exactly 2s zeros. Rank is at most three
by the factorization and at least three because one principal triple is D.

## Distinct projective directions

Since P0 is invertible, compare the coefficient rows e_i^T+4t v^T of A_t.
If rows with indices i,j are proportional by a nonzero scalar lambda,
inspect a coordinate outside {i,j}. All coordinates of v are nonzero,
so the inspection equates their v coefficients. Subtraction then gives

    e_i^T = lambda e_j^T.

This forces i=j and lambda=1, and the coefficient equality forces the two
parameters t to agree. The argument also covers parameter zero. Thus the
3k rows of P before repetition are projectively distinct.

For Q use

    C_t = I - 4t z w^T,
    z = Dv,                 w^T = u^T D^(-1).

Every coordinate of z and w is nonzero. The same outside-coordinate argument
for rows e_i^T-4t z_i w^T gives the identical conclusion. Q0 is invertible,
so Q also has 3k distinct projective directions. Repetition gives precisely
multiplicity s in each factor.

## Canonical anchors

For rational factors, let m_j be the minimum nonzero 2-adic valuation in
column j of P, let n_j be the corresponding minimum for Q, and put
gamma=min_j(m_j+n_j). The canonical anchors are

    A_i,j = [nu_2(P_i,j)=m_j],
    B_i,j = [nu_2(Q_i,j)=gamma-m_j].

Zero entries have infinite valuation. This is the retained rational
normalization convention; it is not a finite valuation sentinel.

All P_t are integral and A_t is congruent to I modulo two. Since t=0 is
included and every column of P0 has an odd entry, m=(0,0,0). The valuations
of the entries of D are (3,3,2). Therefore every coefficient 4D_i/D_j has
valuation at least one. Each C_t has odd denominators after cancellation
and is congruent to I modulo two. Its multiplication preserves Q0's parity
rows. In particular n=(0,0,1) and gamma=0.

Using bit masks with coordinate zero as the low bit, every triple thus has

    A = (3,3,7),            B = (3,3,3).

Each tie A_i intersect B_i is {0,1}, of cardinality two. This computation
uses the complete stacked factors and survives all s-fold repetitions.

## Exact directed box

Retain the first two local row types in every triple, including all their
copies. Give type zero the label pair (e_0,e_0) and type one the pair
(e_1,e_1). These are sub-anchors with diagonal dot one. Scalar zero entries
between retained rows only occur between these two types in the same
triple, where the binary dots are zero. This is a witness of size 2ks.

For the upper bound, apply PR #2978's triangular-rank argument separately
to each triple. Suppose a witness meets all three local row types in one
triple. Select one representative of each and keep their induced order.
Every scalar off-diagonal entry between them is zero. Their three-by-three
binary label-dot matrix has diagonal ones and zeros above the diagonal,
so it has rank three. But every b label lies in span(e_0,e_1), which makes
that matrix's rank at most two, a contradiction. A witness therefore meets
at most two local types per triple, retaining at most 2s rows there and
at most 2ks overall. The preceding witness attains equality.

This is an upper bound on the supplied directed sub-anchor box. It is not
an upper bound on a stronger decoder certificate or on actual COPY cost.

## Exact two-block quantity

An ordered nonzero block cannot meet two different local types in the same
triple, since both directed scalar entries between such types are zero.
It retains at most s rows per triple. Two disjoint ordered blocks therefore
retain at most 2ks. One block containing all copies of type zero in every
triple and another containing all copies of type one attain 2ks: between
triples all scalar entries are nonzero. This proves the second exact value.

## Scope and evidence

The theorem is a written rational construction for all positive k,s.
The implementation checks 30 bounded family members, including the explicit
twelve-line instance, with exact Fraction arithmetic. It independently
recomputes six small ordered-block optima by subset dynamic programming and
checks all 2,592 local label/order possibilities that enforce the box upper
bound. These finite checks corroborate the proof; they do not exhaust all
rational factorizations or formally check the universal argument.

The universal rational twelve-line floor eight remains open. The family
shows why distinct directions and sparse zeros alone cannot yield a strict
improvement of that box ratio. It has no physical supplier, complete paid
invoice, new kappa or selected-frontier implication. Independent human and
formal proof-kernel review are unclaimed.
