# The rank-only NEED optimum and its equality cases

This contribution was produced by Nick Petalas. Apache-2.0.

## Statement

Let K be any field and C an n-by-n matrix over K with every diagonal entry
equal to one. Write r = rank_K C and let m count its nonzero off-diagonal
entries, counting ordered positions. Then

    m >= 2(n-r).                                             (1)

Equality holds if and only if, after a simultaneous permutation of rows and
columns, C is a direct sum of singleton blocks [1] and blocks

    [ 1    t ]
    [ 1/t  1 ],                  t in K, t != 0.             (2)

Consequently, if ceil(n/2) <= R <= n, the minimum m among unit-diagonal
matrices of rank at most R is exactly 2(n-R). Every minimizer has rank R,
n-R blocks of type (2), and 2R-n singletons. This is an elementary
specialization of classical acyclic-set/minrank bounds, with the equality
argument supplied below; no literature-wide priority claim is made for (1).

## Proof of the inequality

Make a loop-free digraph D with arc i -> j exactly when i != j and C_ij != 0.
Let d_i be its outdegrees, so sum_i d_i = m. Any vertex set inducing an
acyclic digraph gives a principal submatrix which is triangular in a
topological order, with unit diagonal. Its size is therefore at most r.

Choose a uniformly random ordering of the n vertices and retain i when it
precedes every out-neighbor. Every arc between retained vertices points
forward in this order, so the retained set is acyclic. Vertex i is retained
with probability 1/(d_i+1). Thus the classical random-order argument gives

    r >= sum_i 1/(d_i+1).                                   (3)

For each nonnegative integer d,

    1/(d+1) - (1-d/2) = d(d-1)/(2(d+1)) >= 0,               (4)

with equality exactly when d is zero or one. Summing (4) in (3) proves
r >= n-m/2, which is (1). The integrality of degrees is the step lost by
the continuous Jensen relaxation r >= n^2/(n+m).

## Proof of equality rigidity

Suppose m = 2(n-r). Equality holds throughout (3)-(4), so every outdegree
is zero or one. The directed cycles of such a digraph are vertex-disjoint.
Let c be their number. Deleting one vertex from each cycle leaves an
acyclic induced subgraph of size n-c, so n-c <= r. Every cycle consumes at
least two arcs, giving c <= m/2 = n-r. Hence c = n-r and every one of the
m arcs belongs to one of c disjoint directed two-cycles. There are no
other arcs, including arcs into or out of the cycles.

The matrix is therefore a direct sum of two-by-two blocks with nonzero
off-diagonal entries and isolated singleton blocks. Each two-by-two block
has rank at least one. These lower bounds already sum to n-c = r, so every
two-by-two block has rank exactly one. Its determinant vanishes, forcing
C_ij C_ji = 1, exactly (2). Conversely each displayed block has rank one,
and its two arcs give equality in (1). This proves both directions.

For a rank cap R, (1) gives m >= 2(n-R). If n <= 2R, take n-R disjoint
blocks (2) and 2R-n singletons. Equality forces r=R and the stated counts.
The proof applies in every characteristic. Nonzero diagonal entries can
also be normalized to one by row scaling, preserving rank and support.

## The 104-port application

DreamingOfClouds's PR6170, P104-LEMMAS.md section 9 G1a, supplies these
necessary premises for its P_M owned-delivery matrix:

1. C_jj=1, and C_ji=0 at every off-diagonal non-orthogonal port pair.
2. rank_Q C <= M <= owned paid.
3. NEED is precisely the number m of nonzero off-diagonal entries.

These are cited premises, not replayed results. In particular this package
does not assert them for the different P' accounting convention.
At owned paid <= 56, (1) gives

    NEED >= 2(104-56) = 96.                                 (5)

The predecessor's continuous Jensen relaxation gives ceil(104^2/56-104)
=90. It already describes an abstract 96-entry example. The new step is
that 96 is the exact optimum of this matrix relaxation, and every
optimizer consists of 48 reciprocal pairs and eight singleton ports.

WITNESS.json lists 48 disjoint pairs in the retained 104-port orthogonality
mask, plus the eight remaining indices. Put ones in each selected pair
and on the diagonal, with all other entries zero. The verifier reads only
the port field of Ali Romman's PR5599 retained WORD.json.gz, checks every
selected pair is orthogonal, and computes rank 56 over Q, F2 and F3.
It also checks 48 nontrivial rational reciprocal weights. This witness
satisfies the matrix mask, rather than just an unconstrained support count.

No claim follows that the witness is a legal owned program of paid cost 56.
Gather/landing geometry, shared ancestry, public lifetimes, source reads and
physical realization impose additional constraints. The original NEED >=
3597 objective is still open. The exact relaxed optimum says that rank,
diagonal and mask constraints alone cannot prove it. A stronger result must
use additional geometry or implementation constraints. No selected-frontier
change or new kappa is claimed.

## Attribution and classical background

The owned-delivery premises, the 90 bound, the abstract 96-entry example
and the missing physical conditions retain DreamingOfClouds's PR6170
credit. Matarener's PR6267 separates those assumptions from the owned
lineage factorization and physical floor. Ali Romman and the retained
P104/native/helper/controller/caller lineage retain the port data credit.

The random-order inequality (3) is classical; see Hermann Gruber,
[*Bounding the Feedback Vertex Number of Digraphs in Terms of Vertex
Degrees*, Theorem 4](https://arxiv.org/abs/1101.1291).
Triangular minors and functional-digraph cycle decomposition are also
classical. The contribution here is the exact P104 rank-only optimum,
its equality characterization and a mask-compatible finite certificate.
Independent human and formal proof-kernel review are unclaimed.
