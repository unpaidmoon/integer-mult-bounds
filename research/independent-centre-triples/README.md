# Independent centre-chart triples have a sharp positive paid cost

For every induced rank-zero three-contact path in the fixed retained 640-input
centre graph, independently changing its three contacts to nontrivial
one-transvection charts increases the complete paid moment by at least

    3 - 2^theta + 7^theta - 8^theta > 0,   0<theta<1.

The bound is attained by one literal path and chart assignment for every theta.
This is a **scoped proof with an exact finite certificate**. No new kappa,
supplier admission or selected-frontier change is claimed.

## New result and predecessors

[PR6289](https://github.com/CrocSwap/integer-mult-bounds/pull/6289), by unpaidmoon,
asks whether independent charts on a three-contact path can escape the pair
ceiling. Its exact cited head is `e41bb20dcc82f3c3d550a5221ee4af0ac940ade5`.
This answers the rank-zero induced-path part of that question. The question
source is citation-only; no unmerged source is needed for reproduction.

Chris R / Clear1nsight's [PR4867](https://github.com/CrocSwap/integer-mult-bounds/pull/4867)
and [PR4888](https://github.com/CrocSwap/integer-mult-bounds/pull/4888) establish
earlier coherent and pair ceilings on this graph. We consume their retained
source graph, without replaying their screens or claiming their results as new.
A new min-plus reduction handles all independent labels at three contacts.
The exact paired geometry makes the reduction complete; it does not sample
label triples or theta values. See [PROOF.md](PROOF.md).

The broader fixed-contact floor in
[PR5590](https://github.com/CrocSwap/integer-mult-bounds/pull/5590) fixes the
scalar-contact frames, which this experiment changes. The
[PR5324](https://github.com/CrocSwap/integer-mult-bounds/pull/5324) floor fixes
contact projection dimensions and owned-centre tariffs. These transvection
neighbours change the empty contacts' projection dimension. The bounded
three-group star in [PR5161](https://github.com/CrocSwap/integer-mult-bounds/pull/5161)
keeps owned-centre boundaries fixed and has two prescribed leaf alternatives.
It does not optimize this retained-centre path's independent label domain.

The certificate visits all 496 induced rank-zero paths and all nine capped-rank
tariffs, giving 4,464 integer optimization problems. Its exact componentwise
minima are `(2,1,1,1,1,1,1,0,0)`. Node path `(11013,11014,11015)`, with label
59 at each node, attains that vector and has paid-histogram change
`{0:-2,1:3,2:-1,7:1,8:-1}`. Every incident transition is charged. All 408 helper
targets and the zero independent centre reward stay fixed.

## Reproduce

From the repository root, with CPython 3.12 and the standard library:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -W error -B research/independent-centre-triples/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -W error -O -B research/independent-centre-triples/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/independent-centre-triples
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/independent-centre-triples --check-source-history
```

Another host may replace the absolute interpreter path with its CPython 3.12.
Expected markers are `PASS_INDEPENDENT_CENTRE_TRIPLES`,
`PASS_REGISTERED_RESEARCH_PACKAGE` and `PASS_RESEARCH_COMMIT_BYTES`.
`VERIFY.json` registers both complete normal and optimized checks with
120-second limits. Set `TMPDIR` to an existing external scratch directory to
place temporary graph and source-control files there. Optional
`--output /absolute/external/path.json` writes a generated receipt containing
package-file hashes, every minimum class and literal attaining witnesses.
Writing that receipt inside the checkout is rejected.

The direct checker also compares 1,136 small literal chart pairs with the
paired geometry, 99 transforms with full independent-label oracles and 36
six-label three-contact products with exhaustive minimization. Five invalid
transform inputs, a triangle, three changed graph contracts and four actual
source-byte mutations exercise rejection boundaries. Assertions are not used
for proof checks. The selected-binding orientation passed at the pinned base.

[SOURCES.json](SOURCES.json) pins base
`2485805a6d47f36ea83ddde6327d453ac82d44dc`, catalogue revision 8 and every
runtime source. [TASK.json](TASK.json) records the changed task premise,
environment and structured next questions. All generated evidence stays outside
the checkout. The generic metadata checker needs repository history; the direct
verifier requires only this package and its four declared inputs.

## Limits

This is a negative result for one optimistic retained-centre graph grammar.
It rules out a paid-moment gain with unchanged targets before additional
physical costs. It is not a universal obstruction to finite networks.
Blocks of four or more contacts, changed routes/operations, other original
charts and second-step neighbours remain unpriced. No native amplitudes,
physical caller, restoration schedule, rounding, precision/tape proof, compiler
closure, selected cold replay, Lean or outer theorem was run. All five selected
framework assumptions remain. Independent human and formal proof-kernel review
are unclaimed.

## Open next questions

1. Can an independent connected block of four or more contacts improve the
   fixed graph invoice? A declared four-vertex tree is a feasible next test for
   the paired-label transform. Cycles need a new joint elimination. No larger
   certificate or favourable candidate is provided here.
2. Can a changed chronological scalar operation or route give a favourable
   retained-centre invoice? First write its arbitrary-input endpoints and
   complete paid/productive bill. Physical delivery and restoration are still
   missing; another chart seed cannot answer that question.

## Implementation bounds

New loops have finite domains: widths at most nine, 18 binary coordinates,
1,022 labels, 176 empty-chart contacts, 496 paths, nine prefixes and the exact
34,830-edge source graph. No recursion is used. Per-frame ranks are reused only
within one run and only for the 31 literal incident frames. Source-byte hashes
are checked before import, and the original builder and its dependencies are
unchanged. Each transform retains a minimizing label. Direct edge walks check
the global attaining witnesses.

Power-of-Ten rule 3 deviation: CPython and its standard library allocate during
execution. Live collections are bounded by the domains above, with at most
`176*9*1022` unary and transform entries per table. Temporary outputs have one
context-managed lifetime. Fixed memory pools would require a different runtime;
if this checker becomes a service or accepts larger graphs, add enforced input
capacities and a separate measured memory budget before widening these bounds.
Rule 8/9 deviation: one authenticated graph builder is loaded through Python's
module loader. The target is a fixed pinned file and its two pinned imports;
there is no arbitrary plugin dispatch. Generic source-bound replay is the
reason for retaining this boundary. Warning-strict normal and optimized checks
and source/graph mutations cover it. Static diagnostic availability is recorded
in the PR; no repository-wide tooling change is included.

## Credit

This contribution was produced by Nick Petalas. Apache-2.0.

Credit unpaidmoon / PR6289 for the independent-triple question; Chris R /
Clear1nsight / PR4867 and PR4888 for the retained graph and coherent/pair
ceilings; Cinna Davis / PR4694, PR4698 and PR4690 for the retained-centre ABI
and contact model; Cao Yifan / PR4610 for the native word; David Ganz /
Dugongue / PR4841 for the exact chart-neighbour framework; and the retained
PR4470, scalar, E8, Clifford, helper, precision, compiler, zxv and Jacob Alan
Sussman lineage. Binary Lagrangian geometry, min-plus elimination and concave
summation by parts are classical. The new contribution is their exact
independent-path application and sharp source-specific result. All predecessor
files and notices remain unchanged.
