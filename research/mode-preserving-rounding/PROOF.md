# An exact radius-one mode fiber

This scoped proof was produced by Nick Petalas. Apache-2.0.

## Contract and source

Let M be the 112-by-8 integer mode matrix in Dillon Amburgey's
[PR4933](https://github.com/CrocSwap/integer-mult-bounds/pull/4933), head
`d969c458c24278e0fd37e5b4c0ff8a53a496b430`.
Its columns are `mode_columns` in the source-pinned NORMALIZERS.json.
The cited inverse-code identity is A^-1 = I - MM^T/52. That identity
is a predecessor premise; no new check of its factorization is claimed.

Consider rounding x in R^112 to z in Z^112 subject to

    M^T z = M^T x.

The rule may use all coordinates, arbitrary nonlinear computation and
arbitrary correlated randomness. There is no coordinatewise rounding premise.
Mode equality is required for each returned output. Equality only in
expectation is a weaker contract and is outside this obstruction.
We require the target mode tuple to have an integer lift. This avoids an
obstruction caused merely by an empty fiber.

## The witness and exact optimum

Use zero-based owner indices. Write m_i for row i of M. The source rows are

    m_0   = ( 1, 1, 1, 1, 0, 0, 0, 0),
    m_7   = (-1,-1, 1, 1, 0, 0, 0, 0),
    m_20  = ( 0, 0, 0, 0, 1,-1, 1, 1),
    m_111 = ( 0, 0, 0, 0, 1,-1,-1,-1),
    m_48  = ( 0, 0, 1, 1, 1,-1, 0, 0).

They give the exact relation

    m_0 + m_7 + m_20 + m_111 = 2 m_48.                 (1)

Put x = (e_0 + e_7 + e_20 + e_111)/2. Then M^T x = m_48,
so z = e_48 is an integer lift. Its infinity-norm distance from x is one.

Suppose an integer lift z had ||z-x||_infinity < 1. Every coordinate of x
outside S={0,7,20,111} is zero, so every corresponding integer z_i is zero.
On S, each z_i must be zero or one. Mode 0 and mode 2 now require

    z_0 - z_7 = 0,          z_0 + z_7 = 1.             (2)

The first equality follows from the zero target in mode 0. The second
follows from the unit target in mode 2. The rows m_20 and m_111 contribute
zero to both equations. Equations (2) force z_0=z_7=1/2, contradicting
integrality. Consequently

    min { ||z-x||_infinity : z in Z^112, M^T z=M^T x } = 1.    (3)

The same argument applies to each realized integer output of a randomized rule.
Thus no rule can guarantee a smaller uniform radius on all inputs with
nonempty integer mode fibers, even if it is allowed arbitrary correlations.
This does not show that radius one suffices on every such fiber.

For any h>0 and any n in Z^112, translation and scaling give

    min { ||z-h(n+x)||_infinity : z in h Z^112,
          M^T z=M^T h(n+x) } = h.                     (4)

Indeed z/h-n is an integer lift of M^T x. The attaining output is
h(n+e_48). Thus retaining exact modes can require twice the usual
half-grid coordinate radius, at every output-grid scale.

## Why this is a rounding obstruction

There are exactly sixteen integer outputs inside the open radius-one box.
They are the {0,1} choices on S, zero elsewhere. The verifier enumerates all
sixteen, compares column-oriented and row-oriented mode calculations, and
finds no lift. Equation (2), rather than extrapolation from that census,
proves the exclusion of every integer output in the box.

If the mode constraint is removed, z=0 has distance 1/2. Even preserving
the ordinary sum does not cause this example's obstruction: e_0+e_20 has
the same sum as x and distance 1/2, but different modes. Allowing radius
one admits e_48. The obstruction therefore retains both its mode and
grid hypotheses and is consistent with an explicit feasible lift.

## Scope and remaining obligations

This is a new local precision contract for the cited code. It is not a
claim about every reachable state of a native caller. A caller could avoid
the displayed input, allow mode defects, keep extra residue information,
or round to a finer grid. Those are changed contracts.

The theorem gives neither the global optimal mode-preserving radius nor
an efficient rounder. The A^-1 factorization motivates preserving M^T x;
it does not imply that a complete inverse implementation must preserve
those modes exactly. No physical correlated-rounding algorithm, native
restoration, tape/storage tariff, complete error propagation, supplier
admission, new kappa or selected-frontier update follows. All five framework
assumptions remain. Independent human and formal proof-kernel review are
unclaimed.

## Credit

Dillon Amburgey supplies the actual code and mode representation. JoyboyBrian's
[PR5069](https://github.com/CrocSwap/integer-mult-bounds/pull/5069) supplies
the source-bound fixed-grid inverse context. Dugongue's coded producer and
the retained native, controller and compiler authors retain their credit.
Ali Romman's [PR5838](https://github.com/CrocSwap/integer-mult-bounds/pull/5838)
separates independently adverse completed defects from possible physical
rounding correlations. Its word and error calculation are not inputs here.
The lattice and finite-box arguments are elementary classical methods.
The source-bound witness, exact fiber radius and new contract are proved here.
