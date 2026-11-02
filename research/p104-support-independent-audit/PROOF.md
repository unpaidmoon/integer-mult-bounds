# Sharp stability of the rank-only support bound

Jerry Chen (@CubeJerry), with substantial OpenAI Codex assistance. Apache-2.0.
The graph operations, triangular-minor argument and rank monotonicity below are
classical. The contribution is their quantitative stability consequence and its
P104-mask application; no literature-wide priority claim is made.

## Statement

Let C be an n by n matrix over any field K, with every diagonal entry one.
Let r be its rank, and let m count **ordered** nonzero off-diagonal entries.
Put s = m - 2(n-r). Then s is a nonnegative integer. There is a set B of at
most 2s indices such that the principal matrix C[V \\ B] is, after a simultaneous
row and column permutation, a direct sum of singleton [1] blocks and blocks

    [1   t  ]
    [1/t 1  ],       t in K, t != 0.                         (1)

An empty retained principal matrix is permitted. The operation deletes the same
indices from rows and columns; it does not change any retained coefficient.
The coefficient 2 is optimal, even in the actual 104-port P104 mask at rank 56
and m=97. The proof applies in every characteristic, including two.

At s=0 this independently proves PR6275's support inequality and equality
classification. PR6275 uses a random-order acyclic-set expectation. The argument
here instead constructs a deterministic cycle-deletion/minor certificate and
quantifies the distance from equality for s>0.

## 1. Deterministic decomposition

Form the loop-free support digraph: i -> j iff i != j and C_ij != 0. Degree
means indegree plus outdegree, counting both arcs of a reciprocal pair.
Repeatedly delete a vertex that belongs to a directed cycle and has current
degree at least three. Let h be the number of deletions, d_1,...,d_h their
degrees at deletion, and

    D = sum_a (d_a-2).                                      (2)

Thus D >= h. Each removed arc is charged exactly once, when its first endpoint
is deleted. The choice of eligible vertex is arbitrary; the implementation
chooses the least index deterministically.

Every surviving cyclic vertex has degree exactly two: a cycle needs at least
one incoming and one outgoing arc, and the stopping condition rules out any
additional arc. Consequently it has precisely its two cycle arcs, and **no
incoming or outgoing edge to another cycle or to the remaining vertices**.
The surviving cycles are therefore isolated weak components. All other
vertices induce an acyclic digraph.

Write c for the number of surviving directed cycles, l_1,...,l_c for their
lengths (all at least two), and E for the number of arcs in the acyclic part.
Set

    L = sum_b (l_b-2).

The complete support count is the exact identity

    m = 2h + D + 2c + L + E.                                (3)

No directed edge is discarded from this count. Arcs removed during peeling,
arcs in isolated cycles and remaining acyclic arcs form a partition.

## 2. Exact cycle ranks and the excess identity

A unit-diagonal matrix supported on one directed cycle of length l with
nonzero edge weights w_1,...,w_l has determinant

    1 + (-1)^(l-1) product_i w_i.                           (4)

This follows directly from the determinant expansion: the identity permutation
and the full cycle are the only supported permutations. Deleting any one cycle
vertex gives a triangular principal matrix with diagonal one. Thus the cycle
block has rank l-1 when (4) vanishes and rank l otherwise. This uses no ordering
or characteristic assumption on K. In particular a two-cycle is singular
exactly when its two weights multiply to one.

Let u count the nonsingular surviving cycle blocks. The acyclic block is
triangular with diagonal one in a topological order, so it has full rank.
Because the cycles are isolated, the principal matrix after the h deletions
is block diagonal and has exact rank

    n - h - c + u.

Taking a principal submatrix cannot increase rank. Therefore

    delta = r - (n-h-c) >= u >= 0.                          (5)

Subtracting 2(n-r) from (3) proves the exact nonnegative accounting identity

    s = D + L + E + 2 delta.                                (6)

This proves s>=0 independently of PR6275's inequality; the reasoning is not
circular. The certificate records all terms in (6).

## 3. Construct the exceptional set

Starting with the h already deleted indices, additionally delete:

- all but one vertex from every cycle of length l>=3, costing l-1 <= 2(l-2);
- the tail of every remaining acyclic arc, costing at most E distinct indices;
- one endpoint from each nonsingular two-cycle, costing q<=u<=delta indices.

All surviving arcs are now precisely the singular reciprocal two-cycles.
The remaining vertices are isolated, giving (1). The number deleted obeys

    |B| <= h + 2L + E + q
         <= D + 2L + E + delta
         <= 2(D + L + E + 2delta) = 2s.                     (7)

The constructor emits B and the retained pair/singleton partition. Its consumer
checks these actual coefficients, not only the scalar bound (7).

An independent inductive check of the same theorem is useful. Deleting a cyclic
vertex of degree d>=3 leaves rank r'<=r and excess

    s' = s + 2-d + 2(r'-r) <= s-1.

Induction gives at most 1+2s'<=2s-1 deletions. If no such vertex exists, the
matrix already decomposes into the isolated cycles and acyclic block above,
which satisfy the result block by block. This second argument corroborates the
accounting proof without using the predecessor expectation argument.

## 4. Sharpness, including the P104 mask

The matrix

    T = [ 1 1 0 ]
        [ 0 1 1 ]
        [-1 0 1 ]

has rank two, three off-diagonal entries, and s=1 over every field. Its
determinant is zero and each two-by-two principal determinant is one.
After deleting any single index, its remaining off-diagonal support contains a
one-way edge, which is neither a singleton nor a reciprocal block. Two deletions
are necessary and sufficient. The same facts hold in characteristic two.

The pinned PR5599 port list has 104 distinct odd nine-bit labels. Its allowed
off-diagonal mask is binary orthogonality: popcount(p_i & p_j) is even.
Indices 0,1,2 are pairwise orthogonal. Install T on them, 47 disjoint reciprocal
all-one pairs on other allowed edges, and seven singleton ones. The checker
constructs the matching deterministically and emits every pair and singleton.
It checks all 10,816 mask positions, rank 56 over Q/F2/F3/F5/F7, and m=97.
Deleting indices 1 and 2 attains the bound; all 104 one-index deletions fail
the required block form. The triangle remains if deletion is outside it.

This is a sharp example in the matrix relaxation. It is **not** a legal owned
program or an invoice of 56 paid operations.

## 5. Consequence for the owned-delivery relaxation

PR6170 section 9 G1a supplies the cited P_M premises: C has diagonal one,
zeros on the non-orthogonal mask, rank r<=owned paid<=56, and NEED=m. Those
physical/source premises are not re-proved here and do not transfer to P'.
PR6275 proves the exact minimum NEED=96 and classifies equality.

For NEED=96+e, the actual excess is

    s = e + 2(r-56) <= e.

Therefore every such matrix has a principal deletion set of size at most 2e
outside which it is exactly a reciprocal-pair/singleton block sum. The allowed
mask is preserved on the retained indices. This strengthens equality rigidity
to a quantitative constraint on every near-minimizer, without assuming r=56.

It does not establish NEED>=3597, legal frame delivery, a favorable paid bill,
or any change in the selected multiplication exponent. To exploit the result
physically, a separate argument must exclude these block sums after allowing
up to 2e exceptional indices, while retaining cancellation, branching, relays,
public source reads and ownership/lifetime costs.

## Scope, evidence and attribution

The universal statement is the written proof above; the finite checker is
corroboration and a certificate implementation. It imports no predecessor proof
checker, graph routine, rank routine, witness or result receipt. Its Tarjan
constructor is checked by a separate reachability/partition consumer; small
field ranks are additionally checked by XOR bases or determinant minors, and
small deletion distances by exhaustive principal subsets.

Nick Petalas supplied PR6275, exact head
`681c547a36e742eceebbde04cb427bcd10cd3293`, including the bound, equality
classification and P104-mask attaining example. Those results retain his credit.
DreamingOfClouds supplied PR6170's P_M model, earlier rank relaxation and physical
gap. Matarener's PR6267 distinguishes the matrix and owned-lineage obligations.
Ali Romman and the retained P104/native/helper/controller/caller lineage supplied
the canonical port data. All source-specific notices remain unchanged.

Worker C's deterministic proof/checker received a separate read-only AI proof
review using the induction above, followed by orchestrator inspection. This is
independent mathematical reasoning within coordinated OpenAI Codex assistance,
not independent human peer review or proof-kernel verification. No Lean, native
supplier, selected cold replay, complete uniform compiler, rounded multiplier
or physical admission is claimed. **No new kappa.**
