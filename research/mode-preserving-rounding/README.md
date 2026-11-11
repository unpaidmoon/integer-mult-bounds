# Exact mode preservation can double the coordinate rounding radius

This scoped mathematical proof with an exact finite certificate was produced by Nick Petalas.

For the actual eight-mode matrix M of Dillon Amburgey's
[PR4933](https://github.com/CrocSwap/integer-mult-bounds/pull/4933), put

    x = (e_0 + e_7 + e_20 + e_111)/2.

Among integer outputs z preserving all eight mode sums M^T z=M^T x,
the minimum infinity-norm rounding error is exactly **one**. The output
e_48 attains it. Every integer output at distance less than one is excluded
by z_0-z_7=0 and z_0+z_7=1. Thus arbitrary joint rounding and correlated
randomness cannot retain the usual half-unit error on all feasible mode fibers.
Mode equality is required for every returned output, rather than only in expectation.
Translation and scaling give the same factor-two obstruction on every grid.

[PROOF.md](PROOF.md) states the boundary, literal five-row identity and
universal argument. This is a new rounding contract, not a replay of a
predecessor theorem. It does not assert that every mode fiber has radius one
or that an actual caller must preserve these modes. Complete kappa is unchanged.

## Reproduce

From the repository root, CPython 3.12 and the standard library suffice:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/mode-preserving-rounding/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -O -W error -B research/mode-preserving-rounding/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/mode-preserving-rounding
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/mode-preserving-rounding --check-source-history
```

Other systems may substitute their CPython 3.12 executable. Direct checks
print `PASS_MODE_PRESERVING_ROUNDING`, including sixteen excluded corners,
91 translated/scaled attaining fixtures and nine rejection controls.
The preceding JSON is a fresh receipt binding the source and package files
by SHA256. No receipt is handwritten or stored. Verification writes nothing.
Normal and optimized modes run the same explicit checks. The complete export
with its declared source input also supports Git-free direct replay.

## Scope and credit

The matrix is the coded inverse's source, not a claim that this proposed
mode-preserving rounder is installed in the selected construction. The
uniform-transfer-audit card is changed to this precision side result.
The selected binding control passes at conditional kappa .003125804;
it is not an operator replay. [TASK.json](TASK.json) records the original
card, changed scope and next questions. [SOURCES.json](SOURCES.json) pins
the exact live mode table and historical provenance.

Credit Dillon Amburgey / PR4933 for M and A^-1=I-MM^T/52,
JoyboyBrian / PR5069 for the fixed-grid inverse context, Dugongue for the
coded producer, and their retained native/controller/compiler lineage.
Ali Romman / PR5838 distinguishes possible rounding correlations from its
adverse-defect model; that calculation is not rerun. Classical lattice and
finite-box arguments retain their credit. New work is Apache-2.0.
Independent human and formal proof-kernel review are unclaimed.

The result supplies no global rounding-radius optimum, physical correlated
rounder, complete error ledger, restoration, precision/storage/tape bill,
supplier admission or complete multiplication theorem. The five framework
assumptions and selected frontier retain their status.

## Open next questions

1. What is the least uniform radius on all nonempty integer fibers of this
   exact mode map? Start with a fundamental domain of its kernel lattice;
   the lower bound here gives no global upper construction.
2. Can a concrete physical caller exploit approximate mode preservation
   rather than exact preservation? Start with one reached state and its
   permitted mode-defect budget; reachability, full propagation and tape
   costs are still missing.

## Verifier bounds

The verifier reads at most one MiB per file and at most 32 package files.
There are eight modes, 112 owners, sixteen corners and 91 scaled fixtures.
No recursion, dynamic code execution, subprocess or output-file write is
used. Functions stay below 60 lines, and errors remain enabled under -O.
Python allocates managed integers, Fractions and containers. This is a
Power of Ten rule 3 deviation bounded by those fixed domains and a registered
30-second timeout. A future arbitrary-dimension implementation must reassess
storage before changing those limits. Warning-strict normal/optimized replay
provides the available diagnostics; no new static-analyzer configuration or
physical-memory bound is claimed.
Rule 9 has a bounded test-control deviation: `reject` calls only the four
locally named functions `parse_modes`, `validate_modes`, `vector` and
`same_modes`, with nine fixed fixtures. Unexpected exceptions propagate.
