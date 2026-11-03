# Selected MOVE phases cannot all be removed by frame rephasing

A scoped proof with an exact finite certificate, produced by Nick Petalas.

On the selected PR6030 word, the native recipes for `3 to 2`, `2 to 299` and
`3 to 299` each contain total explicit phase `i`. Their cycle residue is one
modulo four. Scalar changes to the frame charts cancel around this triangle,
so they cannot remove every explicit phase. At column multiplicity `f`, even
arbitrary width-dependent unit-complex frame gauges succeed for every selected
MOVE exactly when `4` divides `f`. The phase-deleted triangle loop is `-i I` at
width one. One residual tag is necessary and sufficient on that triangle.

This answers a new changed-chart question prompted by unpaidmoon / PR6293,
without repeating its full phase census. It closes the particular remedy of
removing tensor-phase bookkeeping by one scalar gauge per frame. Keeping the
correct phases already works; no source correctness failure is asserted.
The [proof](PROOF.md) fixes the normal forms and gives the all-width argument.

## Evidence and reproduction

From the repository root, using CPython 3.12 and the standard library:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/move-frame-phase-obstruction/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -O -W error -B research/move-frame-phase-obstruction/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/move-frame-phase-obstruction
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/move-frame-phase-obstruction --check-source-history
```

Another CPython 3.12 interpreter may replace that local path. The direct verifier
also works from a source export without Git. Expected markers are
`PASS_MOVE_FRAME_PHASE_OBSTRUCTION`, `PASS_REGISTERED_RESEARCH_PACKAGE` and
`PASS_RESEARCH_COMMIT_BYTES`.

The verifier authenticates all three live sources, binds the named frames and
actual event indices, and compiles only the three witness edges. The separate
Gaussian interpreter checks their signed Pauli actions and absolute phases.
Both the full and phase-deleted loops are checked on all 512 basis states.
The 64 fourth-root gauge assignments are enumerated at each width 1 through 4.
Compatible-triangle, tree, restored-loop, wrong-phase, reversed-sign and changed
source-byte controls run in both normal and optimized Python. Output includes
a generated receipt binding the package and live input hashes. It writes no
files. Hosted CI status is recorded separately in the PR body.

## Limitations

The theorem fixes the recipes with literal `phase` gates removed. It does not
cover refactoring their other gates or using distinct charts by role or history.
The three edges occur on different roles; the diagnostic loop is an operator
identity, not a chronological subroutine. No whole-word native replay, selected
cold replay, physical caller, all-size implementation, Lean or Docker was run.
No new kappa or complete multiplication theorem is claimed. All five selected
framework assumptions remain. Independent human and formal proof-kernel review
are unclaimed.

The verifier uses bounded source sizes, three nine-axis charts, 512 basis
states and 64 gauge assignments per tested width. Python and the frozen exact
interpreters allocate dynamically; these finite bounds replace a fixed-memory
implementation. Dynamic module loading is restricted to two authenticated
files. Frozen source style and its internal assertions are retained, while new
acceptance checks use exceptions and remain enabled under `-O`. No external
static analyzer was available; warning-strict execution and the registered
checks are the available diagnostics.

## Open next questions

Can role-specific phase charts eliminate tags while preserving every actual
common-chart ADD and COPY relation and the endpoint normalizers? Start with
these three occurrences and add the real scalar-gate compatibility constraints.
The obstruction here requires one shared phase per frame, so that larger graph
and its physical scalar bill remain open. Do not treat missing compatibility or
restoration charges as zero.

## Credit

The witness and gauge application were produced by Nick Petalas. The cycle
criterion and tensor-product scalar identity are classical. Credit unpaidmoon /
PR6293 for the selected tensor-phase question; DLamdata / PR5894 for existing
absolute-phase coverage; Mark / Matarener's PR5974 and PR5442 for earlier lift
work; DreamingOfClouds / PR6030 and the retained PR5907/5827/5599 word lineage;
Chafik Boukhalfa's native channel; icekylinx's retained exact compiler; and Ali
Romman's independent Gaussian interpreter from PR1862/1931. Further retained
P104 credit is in [PROOF.md](PROOF.md) and the unchanged source packages.
Apache-2.0.
