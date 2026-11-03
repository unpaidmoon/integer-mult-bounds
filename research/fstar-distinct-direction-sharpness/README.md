<!-- SPDX-License-Identifier: Apache-2.0 -->

# A sharp two-thirds anchor box with distinct factor directions

This contribution is produced by Nick Petalas.

For every positive k,s, an explicit rational three-total factorization on
3ks lines has rank three, nonzero diagonal, exactly 3k projective directions
of multiplicity s in each factor, exactly 2s zeros per row and column, and
canonical tie size two everywhere. Its directed sub-anchor box and maximum
union of two disjoint ordered nonzero blocks both equal 2ks.

In particular k=4,s=1 gives twelve distinct directions in each factor, only
two zeros in each row and column, and box exactly eight. Thus the structural
restrictions in [Sagar Thakrar's PR #3445](https://github.com/CrocSwap/integer-mult-bounds/pull/3445)
can coexist with a sharp eight-line witness, even with no repeated factor
directions. That source supplies the open question. Its universal rational
twelve-line floor remains open; this is a partial sharpness result.

Claim type: scoped written proof with finite exact corroboration. The new
step is a family of rank-one nilpotent basis changes preserving the original
whole-instance canonical anchors. The sharp core already belongs to
[Aaron Wang/navinor's PR #2978](https://github.com/CrocSwap/integer-mult-bounds/pull/2978).
[PROOF.md](PROOF.md) gives the construction, distinct-direction argument,
canonical normalization, attaining witnesses and exact upper bounds.

## Reproduce

From the repository root with CPython 3.12 and the standard library:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/fstar-distinct-direction-sharpness/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -O -B research/fstar-distinct-direction-sharpness/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/fstar-distinct-direction-sharpness
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/fstar-distinct-direction-sharpness --check-source-history
```

On other machines, replace the absolute interpreter path with the local
CPython 3.12 executable. The two direct modes report
`PASS_DISTINCT_DIRECTION_SHARPNESS` with 30 family fixtures, 48,510 exact
matrix-entry comparisons, 2,592 local label/order cases, six independent
subset-DP fixtures and fifteen controls. Both source input files are
SHA256-authenticated before the mathematical checks. No predecessor
executable or scientific suite is run.

An optional `--receipt /absolute/scratch/path.json` writes generated evidence
bound to every package file's SHA256 and both input pins. The normal replay
writes no files. Keep generated receipts and exports outside the checkout.
Hosted CI evidence is recorded separately in the PR after it completes.

## Meaning and limitations

The construction rules out a strict two-thirds box improvement based only
on distinct factor directions and two scalar zeros per row/column. It does
not disprove the eight-line lower bound or the sufficient two-block route.
It does not bound the full F-star certificate from above, give a cheaper
native decoder, or supply physical delivery, dirty restoration, a complete
signed invoice or supplier admission. The selected frontier and its five
framework assumptions are unchanged. No new kappa or complete multiplication
theorem is claimed. Independent human and formal proof-kernel review are
unclaimed.

The finite implementation caps k at ten and s at three. The proof has no
such cap. Python's managed allocations are a documented Power of Ten
deviation: the finite verifier has at most ninety rows and 8,100 entries in
each dense matrix. The rank calculation holds one further matrix copy. The
independent subset DP is capped at twelve rows and 4,096 masks. Every loop has a finite bound, there is no
recursion, and all acceptance checks remain active under optimized Python.
No third-party static analyzer is required; both registered modes enable
warnings as errors. The mathematical proof and exact executions are the
validation of this isolated research code.

## Open next questions

- Does every rational twelve-line admitted three-total factorization have
  box at least eight? Start with PR #3445's all-even remainder. A failure of
  its two-block route must be distinguished from a literal box counterexample.
  This needs a new lower-bound argument or an exact counterexample.
- Can a stronger decoder certificate beat the two-thirds box floor on this
  family? Start with the explicit k=4 instance and its original anchors.
  A connection to actual decoder cost and a complete physical invoice are
  still required. Structured versions are in [TASK.json](TASK.json).

## Credit and source boundary

Credit Sagar Thakrar / thakrarsagar for the PR #3445 question and obstruction
reduction, and PR #3435/#3420/#3409 for its ordered-block lineage. Aaron Wang /
navinor retains the core, directed box and canonical-anchor/SG lineage;
DreamingOfClouds retains the F-star definitions. Classical nilpotent matrix
inversion and rank arguments retain their classical status. The new
anchor-preserving family, its distinct-direction proof and checker are
produced by Nick Petalas. Apache-2.0.

The source base is canonical main
`2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority revision eight.
[SOURCES.json](SOURCES.json) pins the source question and proof by exact Git
blob and SHA256, alongside the frozen card and selected-record provenance.
The [advance CLAIM](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19291872)
targeted the universal remainder. The delivered scope is the first partial
sharpness construction, with that universal question left open. No
predecessor result is independently audited here.
