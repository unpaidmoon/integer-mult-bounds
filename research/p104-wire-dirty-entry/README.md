# A dirty-entry obstruction for a one-helper P104 wire meeting

This contribution was produced by Nick Petalas. Apache-2.0.

A dirty helper cannot supply PR6217's missing third effective source when
its dirt is confined to that helper at the meeting entrance. At least two
of the three incoming registers must carry the same independent dirt. If
exactly two carry it, the remaining clean live row must already isolate the
exceptional third root. The two dirty live supports must cover the other
23 ports, so each contains at least seven of them under the 16-port cap.

Claim type: **scoped response-space proof with a finite local construction**.
The result refines Matarener's explicit one-helper wire question. It does
not decide the cost or existence of a complete one-helper program.

The new kernel argument permits arbitrary finite local rational processing,
even arbitrary linear readouts. PR6217's sign, capacity and content-in-frame
facts are cited premises. They are not audited or replayed here.
[PROOF.md](PROOF.md) states every hypothesis and the proof over every field
of characteristic different from two.

## Local escape and its limit

At the common seven-frame for labels 11 and 19, the third root is 487.
Two complementary six-frame sections split the live coefficients into
parts a,d of support 15 and 8. Let e isolate the third root and c=a+d.
The normalized Gram response rows are c+e,c-e. With prepared inputs

```text
(R0,R1,R2) = (eX, aX-h, dX+h),   h arbitrary,
R1 += R2; R1 -= R0; R0 *= 2; R0 += R1
(R0,R1,R2) = ((c+e)X, (c-e)X, dX+h).
```

The exact scalar map has determinant 2 and a four-event literal inverse.
The helper retains its entrance value dX+h. Its original h is not restored
by this meeting. Preparing the correlated pair and singleton, preserving
all omitted public/dirty columns, legal native access and later removal
of dX remain open. No complete signed invoice, physical saving, supplier,
new kappa or full multiplication theorem is claimed.

This is the first local result, so construction stops here. The complete
preparation, movement, restoration, precision, compiler and caller charges
are unknown. Their omission grants no productive credit or free operation.
The selected record and its five framework assumptions are unchanged.

## Evidence and reproduction

From the repository root with CPython 3.12, standard library only:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -X dev -B research/p104-wire-dirty-entry/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -X dev -B -O research/p104-wire-dirty-entry/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/p104-wire-dirty-entry
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/p104-wire-dirty-entry --check-source-history
```

Another CPython 3.12 interpreter can replace the absolute path. Expected
markers are `PASS_P104_WIRE_DIRTY_ENTRY`,
`PASS_REGISTERED_RESEARCH_PACKAGE` and `PASS_RESEARCH_COMMIT_BYTES`.
The final command requires committed bytes and full source history.

The checker reconstructs this one new witness from the hash-bound port
fixture, checks both complete 25-column projected endpoints and the
literal inverse, and executes 625 scalar cases with arbitrary tested dirt.
It checks all 251,559 normalized F3 cases with four live coordinates,
three incoming rows of support at most two and nonzero dirt. Nonzero dirt
entries are normalized to one by row scaling. A separately implemented
augmented-matrix elimination checks every case against the kernel test.
The feasible counts by dirt-support size 1,2,3 are 0,288,108. These are
counts in this small normalized domain, not a census of P104 programs.

Eleven rejecting controls cover each omitted event, lost doubling, isolated
or wrong-sign dirt, changed singleton, aliasing, zero scaling and invalid
operations. Two positive controls outside the hypotheses show why the
support cap and nonzero dirt premise cannot be dropped. The JSON receipt
is generated at execution and binds all six package files and the exact
external port input by SHA256. No receipt is handwritten.

No predecessor scientific executable is imported. Local normal/optimized
and registered replay results are recorded in the submission. Hosted CI
is a separate check, and no hosted pass is asserted before it completes.
No Lean, Docker, native, full supplier or selected cold replay was run.
Independent human and formal proof-kernel review are unclaimed.

## Provenance and overlap

Base `2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority revision 8,
selected conditional kappa .003125804. The baseline command authenticated
source bindings only. [SOURCES.json](SOURCES.json) pins the original card,
selected record, PR6217 proof context and runtime port fixture.
[TASK.json](TASK.json) records the narrowed local obligation.

The [advance claim](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19292022)
reserves the local dirty-entry question. Live open PRs, recent account
contributions, handoffs, active Discussions, main README terms, merged PR
searches and local reservations were checked. Those searches omit arbitrary
historical diffs and unpublished work; empty results are not novelty proofs.
PR6219's A2 packing and PR6218's decoder floor address different obligations.
No predecessor mathematical number is reverified as this deliverable.

## Open next questions

Can a legal pre-cut contact prepare the correlated pair and the exceptional
singleton? Start with actual public/helper trajectories and track every
original input column. The required dirt preload and full public endpoint
are still missing.

Can that prepared helper be cleaned while beating the matched two-helper
route? First name its later access to dX and price all paid and productive
histograms together. Native delivery, cleanup and a complete caller are
blockers. These questions are also structured in TASK.json.

## Credit

Credit Matarener / PR6217 for the question, sign/capacity/two-source premises
and E8 port interpretation, DreamingOfClouds / PR6170 for frame-contract
context, and the retained P104 carrier-code, native, helper, controller and
caller lineage. Kernel dimension, support arguments and reversible row
operations are classical. The new material is the correlated-dirt necessity,
its singleton consequence and the explicit local response construction.
All predecessor files and credit lines remain unchanged.

## Verifier bounds

The direct call graph is acyclic. The verifier has no subprocess, network,
write path or dynamically loaded predecessor code. There are 251,559 census
iterations; each elimination has at most five rows and five columns. The
P104 pass uses three rows of 25 coordinates. Scalar fixtures use four events
in each direction, and every collection has a finite fixed bound. Functions
are below 60 physical lines. Explicit exceptions keep checks active under
optimized Python. Warning-strict development-mode runs and source compilation
provide the available Python diagnostics; no external static analyzer was
available in the selected environment.

Power of Ten rule 3 requires a managed-runtime deviation. CPython allocates
objects during execution. The fixed domains above bound live collections;
no census results are accumulated. Each file is limited to 256 KiB,
with one guard byte read, and file handles close on all exits. Dynamic integer
and Fraction allocation is bounded by the fixed fixtures and operation
counts. This is not a fixed-allocation runtime claim. A future compiled
verifier could use fixed-capacity arrays if that becomes necessary.
