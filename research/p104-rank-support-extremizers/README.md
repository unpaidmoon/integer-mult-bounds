# Exact rank-only NEED floor 96, with all equality cases

This contribution was produced by Nick Petalas. Apache-2.0.

Claim type: scoped written proof with exact finite corroboration. For a
104-by-104 unit-diagonal owned-delivery matrix of rank at most 56,

    NEED >= 96.

This improves the inherited rank-only lower bound 90 and proves the exact
optimum of that matrix relaxation, even with the P104 orthogonality mask.
Every minimizer is, up to simultaneous permutation, exactly 48 reciprocal
rank-one two-by-two blocks and eight singleton blocks. [PROOF.md](PROOF.md)
gives the all-field argument and separates its classical ingredients from
this application. No new kappa is claimed.

## The new step

If C has n unit diagonal entries, rank r and m nonzero ordered
off-diagonal entries, its support digraph gives

    r >= sum_i 1/(d_i+1) >= n-m/2,
    m >= 2(n-r).

The second inequality uses the integral identity
`1/(d+1)-(1-d/2)=d(d-1)/(2(d+1))`. Equality forces every degree to be zero
or one; the rank bound then forces every arc into a disjoint two-cycle.
Each corresponding block must have reciprocal coefficients and rank one.

DreamingOfClouds's [PR6170](https://github.com/CrocSwap/integer-mult-bounds/pull/6170)
already supplies the owned-delivery premises, the bound 90 and an abstract
96-entry example. The contribution is exact optimality, equality rigidity
and an explicit witness inside the actual port mask. Its theory is cited;
no predecessor scientific executable or claimed count is replayed.

The general rank/support argument is an elementary specialization of
classical acyclic-set/minrank methods, including
[Gruber's random-order bound](https://arxiv.org/abs/1101.1291).
No worldwide novelty is claimed for that inequality. The exact new
repository result is the P104 rank-only optimum and its equality contract.

## Exact evidence

[WITNESS.json](WITNESS.json) gives 48 disjoint orthogonal pairs and the eight
unused indices in Ali Romman's PR5599 port order. The witness has rank 56
over Q, F2 and F3, exactly 96 nonzero off-diagonal entries, unit diagonal,
and no nonzero outside the allowed mask. A second witness assigns all 48
pairs nontrivial rational reciprocal weights and still has rank 56.

The verifier reads only the port field of the hash-pinned source word;
it does not execute its program. Its other finite checks are:

- All 4,165 unit-diagonal binary matrices in dimensions one through four,
  using modular elimination and an independent XOR-basis rank calculation.
- All 739 unit-diagonal ternary matrices in dimensions one through three,
  using modular elimination and independent Leibniz-minor enumeration.
- The degree inequality and its exact equality condition in all 5,460
  degree/dimension cases through dimension 104.
- Nine controls: seven invalid contracts/witnesses reject, and breaking a
  reciprocal pair or deleting one directed edge increases the witness rank
  to 57 and breaks its equality form.

Every finite matrix is checked for the degree-sequence bound and the full
if-and-only-if equality statement. These censuses corroborate the written
proof; they do not replace its universal quantifiers. Counts in the emitted
receipt are computed by the verifier. No receipt is handwritten.

## Reproduce

From the worktree root, using CPython 3.12 and the standard library:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -W error -B research/p104-rank-support-extremizers/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -W error -O -B research/p104-rank-support-extremizers/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/p104-rank-support-extremizers
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/p104-rank-support-extremizers --check-source-history --check-modes
```

Another CPython 3.12 executable can replace that path. The expected final
scientific marker is `PASS_P104_RANK_SUPPORT_EXTREMIZERS`. Each direct mode
emits a JSON receipt bound to the seven package files and the live port input
by SHA256. It writes nothing and needs no Git or network at replay.
The last command requires the publication commit and its full history.

## Scope and credit

The canonical base is `2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority
revision 8. TASK.json changes `complex-rank-shape-decoder` to an originally
posed matrix extremal question at the owned-delivery bottleneck. This is a
scoped obstruction, not a completed decoder or favorable signed invoice.
The selected-binding first example passed; it is metadata orientation only.

The [advance claim](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19294829)
and the local reservation name the exact minimum/equality question. This
is separate from predecessor open questions about physical relay cost or
the threshold 3597. It does not generalize the earlier confined two-clique
paid-floor result: it drops temporal realization and optimizes matrix support.

Live open PRs, active Discussions, recent account contributions, main README
formulas and merged object/formula searches were inspected. The overlap
helper searched paginated remote records, but its sparse local search
omitted 8,633 note paths; separate Git searches covered main READMEs.
Unseen diffs, older prose and unpublished work remain coverage limits.
Empty search results are not proofs of novelty.

Credit DreamingOfClouds for the P_M contract, prior bound and example;
Matarener's [PR6267](https://github.com/CrocSwap/integer-mult-bounds/pull/6267)
for separating the owned-lineage and matrix premises; Ali Romman for
PR5599's retained port data; and the retained P104/native/helper/controller/
caller lineage. The random-order, triangular-minor and graph-cycle facts
retain their classical credit. SOURCES.json pins the source theory as
provenance and the port word as a live input. Existing notices are unchanged.

## Limits and unrun obligations

The witness is a matrix, not a legal owned layer of paid cost 56. The
P_M identity and rank-to-paid implication remain cited premises; they
are not transferred to P' accounting. Rank, diagonal and the allowed
mask cannot prove NEED greater than 96. Any improvement must add genuine
geometry, source-content or implementation constraints. The physical
NEED >= 3597 objective, full signed budget, native realization, ownership,
compiler, precision/tape, analytic recovery and the five selected framework
assumptions remain open. Independent human and formal proof-kernel review
are unclaimed. No selected cold replay, historical suite, Lean or Docker
was run.

The offline verifier fixes dimensions at 104, census dimensions at four
over F2 and three over F3, seven package files and at most 8 MiB per file
or decompressed source. It has no recursion or dynamic code execution;
every function is below 60 lines. All mathematical checks use explicit
exceptions and remain active with optimization. Warnings are errors in
both registered commands. No external linter or type checker is required.

Power of Ten rule 3 deviation: CPython and Fraction allocate during the
offline calculation. The fixed 104-by-104 matrix capacity, finite census
domains, fixed reciprocal coefficients of height below 64 and file limits
bound the live computation; there is no online or concurrent service.
The registered timeout is 120 seconds per mode. Revisit fixed-capacity
storage only if this verifier becomes an online caller. Generator library
callbacks have only the explicitly named local arithmetic operations,
with these same finite domains (rule 9 deviation).

## Open next questions

Which additional owned-geometry constraint excludes all 48-pair matrix
extremizers under paid <= 56? Start by combining the equality classification
with one explicit gather/landing or source-content constraint, charging
shared ancestors and public reads. The blocker is the missing complete
physical bound. This package stops at the exact relaxed optimum.
