# A three-edge obstruction to scalar frame rephasing

This scoped proof and its exact finite certificate were produced by Nick Petalas.

## Definitions and source

The fixed input is the selected PR6030 word, SHA256
`7834725d9e34ee846a9ccc615221ea81e0201613938afa185d2eda0c9a6c232f`,
at canonical main `2485805a6d47f36ea83ddde6327d453ac82d44dc`.
The retained `clifford_exact.py` constructs a unitary chart `C_a` for frame `a`.
Use ordinary matrix composition, with the rightmost matrix acting first.
The source expression `chart(a).adjoint().then(chart(b))` applies `C_a†`
first, then `C_b`, so its matrix is

    T_ab = C_b C_a†.

The source native normal form expresses `T_ab = i^(p_ab) S_ab`, where
`p_ab` is the sum modulo four of its literal `phase` gates and `S_ab` is
that same recipe with only those gates deleted. This definition fixes every
permutation, quadratic phase, translation and Gaussian gate in `S_ab`.
It does not identify all possible recipes for an operator.

Three used frames and three actual MOVE occurrences suffice. Indices are
zero-based, as in the JSON program.

| Frame | Binary basis |
|---|---|
| 3 | empty |
| 2 | 35 |
| 299 | 35, 75, 400 |

| Directed edge | Event index | Public role | Child rank | `p_ab` |
|---|---:|---:|---:|---:|
| 3 to 2 | 10338 | 259 | 1 | 1 |
| 2 to 299 | 10403 | 258 | 2 | 1 |
| 3 to 299 | 14360 | 465 | 3 | 1 |

The events are on different roles. The theorem concerns one chart choice shared
by every occurrence of a frame. It does not assert a chronological three-event
subroutine or an actual closed walk by one role.

## The scalar gauge theorem

For each positive integer column multiplicity `f`, permit a separate arbitrary
unit-modulus scalar `lambda_a(f)` for each frame and replace its tensor chart by

    C'_a(f) = lambda_a(f) C_a^(tensor f).

There exists such a frame gauge making every selected MOVE equal to its fixed
phase-deleted recipe `S_ab^(tensor f)` if and only if `4` divides `f`.
In particular, no width-one frame gauge removes all these literal phase tags.
This permits width-dependent gauges and arbitrary complex unit phases, not only
fourth roots of unity.

**Proof.** Under a frame gauge the MOVE becomes

    T'_ab(f) = lambda_b(f) conjugate(lambda_a(f))
                i^(f p_ab) S_ab^(tensor f).

Since `S_ab` is invertible, equality with its phase-deleted tensor recipe requires

    lambda_b(f) / lambda_a(f) = i^(-f p_ab).

For the edges `3 to 2` and `2 to 299`, the product of the required ratios is
`i^(-2f)`. The direct edge `3 to 299` requires the same ratio to be `i^(-f)`.
Consequently `i^f = 1`, which holds exactly when `4` divides `f`.
Conversely, every literal phase gate in the retained native alphabet has an
integer exponent modulo four. If `4` divides `f`, all its tensor scalar factors
are one; the trivial gauge therefore works for every selected MOVE, without
needing a census of the remaining edges. This proves both directions. ∎

The argument is the classical cycle criterion for scalar edge potentials.
The new source-specific content is the three used edges with cycle residue
`p_32 + p_2,299 - p_3,299 = 1 mod 4`, and the resulting exact width criterion.

## Operator certificate and sharpness on the triangle

Chart cancellation gives

    T_2,299 T_3,2 = T_3,299.

Substituting the three measured phases gives

    S_3,299† S_2,299 S_3,2 = -i I.

The verifier checks the full-phase loop is `I` and the phase-deleted loop is
`-i I` on every one of the 512 coordinate basis vectors, using exact Gaussian
integer numerators and powers of two as denominators. Tensoring the identity
shows that the phase-deleted loop at width `f` is `(-i)^f I`.

At width one, one residual tag among these three is necessary and sufficient.
Set `q_3=0`, `q_2=3`, `q_299=2`, with `lambda_a=i^(q_a)`. The path edges then
have zero residual phase and the direct edge has residue `3`. This attains the
one-tag minimum on this triangle only. No global minimum tag count is claimed.

As controls, enumerating the 64 fourth-root vertex assignments gives no
solution at widths 1, 2 or 3, and four solutions at width 4. Replacing the direct
edge's phase by 2 gives four width-one solutions. Deleting the direct constraint
leaves the expected four tree solutions. Wrong loop phase and reversed sign
are rejected. These finite controls corroborate the proof, including its sign;
they are not the argument for arbitrary `f` or arbitrary unit phases.

## Scope and predecessors

Unpaidmoon / PR6293 identifies the selected tensor-phase scaling question and
reports the full phase census. That census is cited, not replayed or adopted as
this result. The three-edge witness here is independently compiled to establish
a new gauge obstruction. DLamdata / PR5894 records existing absolute-phase
coverage; this proof asserts no missing source check. Mark / Matarener's
PR5974 and PR5442 supply earlier all-width lift work.

DreamingOfClouds supplied PR6030's selected word, building on PR5907, PR5827,
Ali Romman's PR5599 and their retained P104 lineage. Chafik Boukhalfa's native
channel retains the exact compiler through icekylinx's frame-sa504 package and
the independent Gaussian interpreter from Ali Romman's PR1862 and PR1931.
Rohan Arun / PR1972, Adam Gall / PR1940, Josie Elliston / PR1071, Ali Romman /
PR1125 and the retained decoder/native sources keep their original credit.
All input files remain unchanged. Apache-2.0.

The obstruction fixes the extracted native normal forms. A different
factorization can move a scalar into other gates. Role-specific or
history-dependent charts can also change the constraint graph. No lower bound
for those mechanisms follows. No physical scalar cost, changed paid profile,
new kappa, supplier failure, selected-frontier change or complete multiplication
theorem is claimed. All five selected framework assumptions remain.
Independent human and formal proof-kernel review are unclaimed.
