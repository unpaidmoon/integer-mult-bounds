# Sharp obstruction for independent three-contact paths

This is a scoped proof, with an exact source-specific finite certificate.
It concerns the retained 640-input centre-contact graph of Chris R's PR4867
and PR4888, built on Cinna Davis's retained-centre interface and Cao Yifan's
PR4610 word. The question is the independent three-contact remainder posed
by unpaidmoon in PR6289. No predecessor theorem is re-audited here.

## Statement

Freeze every source chart except three contacts `a,b,c` that induce a path
`a--b--c` of rank-zero edges among the 176 empty-chart variable contacts.
Replace each of their charts independently by any nontrivial one-transvection
neighbour of the empty chart. Keep every incident edge charge, every native
map, every boundary and all 408 productive helper targets unchanged. The
complete paid-moment change satisfies, for every `0<theta<1`,

    Delta(theta) >= 3 - 2^theta + 7^theta - 8^theta > 0.

This bound is sharp simultaneously for every such theta. In the graph's
zero-based node numbering, path `(11013,11014,11015)` with neighbour label
`59` at all three nodes has rank-histogram change

    delta_0 = -2, delta_1 = 3, delta_2 = -1, delta_7 = 1, delta_8 = -1,

with every other delta zero. Rank-zero edges have cost zero. The witness
therefore attains the displayed bound literally. Labels are defined below;
label 59 is normal 30, tag 1, transvection axis 1054.

The source graph has exactly 496 induced paths of this kind. The proof combines
an exact reduction over the entire independent label domain with finite integer
minimizations on those paths. It does not enumerate a sampled collection of
label triples or extrapolate a numerical theta screen.

## The paired neighbour geometry

Write the ambient symplectic space as `F_2^n x F_2^n`, with coordinates `(x,z)`,
and the empty Lagrangian as `L_0={(0,z)}`. For each nonzero normal `x`, let
`j` be its least nonzero coordinate. Apply the two transvections with axes

    (x,0), (x,e_j).

Their images are exactly the two Lagrangian neighbours with intersection

    H_x = {(0,z): x dot z=0}

with `L_0`. To see completeness, a distance-one neighbour meets `L_0` in a
hyperplane `H_x`. Every vector in the neighbour's other coset has nonzero
first coordinate `x`, since isotropy makes that coordinate annihilate `H_x`.
Modulo `H_x`, its second coordinate has exactly two possibilities, distinguished
by its dot product with `x`. Both displayed transvections realize them.
Every nontrivial transvection image has distance one, so this is also the
complete one-transvection domain. Its size is `2(2^n-1)`.

Our zero-based labels put the two images for normal `x` at `2(x-1)` and
`2(x-1)+1`, in the axis order just displayed. Thus a label's partner is `k xor 1`.
The graph has `n=9`, so there are 1,022 labels.

For two labels, the Lagrangian distance is 0 if they agree, 1 if they are
partners, and 2 otherwise. For partners their intersection is exactly `H_x`.
For distinct normals `x,y`, any common vector has first coordinate zero,
and their intersection is exactly `H_x intersect H_y`, of dimension `n-2`.
This proves the three-valued distance without a large pair census.

## Exact elimination of the independent labels

For `j=1,...,9`, set `h_j(r)=min(r,j)` and `h_j(0)=0`. Let `U_v^j(k)` be the
sum of the changes of `h_j` over every edge incident to node `v`, when only
that node changes to label `k`. These unaries are recomputed from the actual
source frame bases by binary row elimination. No single-contact or pair-screen
receipt is used to supply or bound them.

On an old rank-zero internal edge, the two unary bills each replace rank zero
by rank one. Their sum must therefore be corrected by

    C_j(i,k) = h_j(d(i,k)) - 2.

Because the selected triple induces a path, these are its only shared edges.
Its exact full prefix change is

    U_a^j(i) + U_b^j(k) + U_c^j(l) + C_j(i,k) + C_j(k,l).

This formula counts every external edge once and each internal edge once.
The change is not the sum of two independently optimized pair invoices.
All unchanged graph edges cancel from the complete bill.

For any unary vector `f` define `T_j f(k)=min_i[f(i)+C_j(i,k)]`. The paired
geometry gives the exact identity

    T_j f(k) = min(
        f(k)-2,
        f(k xor 1)-1,
        min_{i outside k's pair} f(i) + min(2,j)-2
    ).

The outside-pair minimum follows from the two smallest minima of the disjoint
label pairs. This excludes the current pair even if it contains the global
minimum. Each of the three displayed alternatives has an actual minimizing
label; the verifier retains the witnesses. Consequently the exact path minimum
is

    min_k [U_b^j(k) + T_j U_a^j(k) + T_j U_c^j(k)].

This is an equality, not a relaxation: for fixed `k`, the two endpoint choices
are independent and both minima are attained. Sorting the 511 pair minima and
then visiting 1,022 middle labels suffices in the supplied implementation.
A `1022^3` loop is unnecessary.

## Source-specific integer certificate

The pinned builder regenerates the original graph with 19,197 nodes and
34,830 positive paid constraints. All edges incident to the changed contacts
have identity maps. There are 176 empty-chart variable contacts and 256 internal
rank-zero edges. Every changed contact has four incident edges. The complete
source paid histogram is

    {1:2201, 2:412, 3:510, 4:127, 5:40, 8:8},

and productive helper targets remain `{4:28,7:7,8:47,9:326}`. No independent
centre reward is added.

`induced_paths` visits each middle node and each unordered pair of its distinct
neighbours, excluding a closing edge. It finds 496 paths. The verifier computes
nine exact minima for each, using the equality above. Across these 4,464 problems
the componentwise minima are

    (2,1,1,1,1,1,1,0,0).

A generated report lists every path-minimum class and a literal attaining
invoice for each component. The named sharp witness attains the entire vector,
so the constants and all-theta moment bound are attained on the original graph.
The report is generated outside the checkout and binds all package-file hashes.
It is not a hand-written receipt.

## From prefixes to every concave power

For a full rank-histogram change `delta`, define

    S_j = sum_{r=1}^9 delta_r min(r,j),
    q_j = j^theta - (j-1)^theta.

Summation by parts gives

    Delta(theta) = sum_{j=1}^8 S_j (q_j-q_{j+1}) + S_9 q_9.

Every coefficient on the right is positive when `0<theta<1`. Substituting the
certified componentwise bounds yields

    Delta(theta) >= 2(q_1-q_2) + sum_{j=2}^7(q_j-q_{j+1})
                 = 3 - 2^theta + 7^theta - 8^theta.

This is `(2-2^theta)+(1+7^theta-8^theta)`. The first summand is positive for
`theta<1`; the second is positive by strict subadditivity of the concave power
at `8=1+7`. The literal sharp witness proves equality in the lower bound.

## Boundary of the result

The finite certificate plus the written identities prove this fixed graph's
three-contact obstruction for the full continuum `0<theta<1`. The exact
arbitrary-dimensional neighbour and elimination identities do not prove a
source-independent cost floor. Four-contact blocks, cycles, nonempty original
charts, second-step neighbours, changed operations, routes, native maps,
helper targets and endpoints are outside this result. No new paid improvement,
native construction, physical restoration, rounded implementation, compiler
closure, supplier admission or multiplication theorem is established.
