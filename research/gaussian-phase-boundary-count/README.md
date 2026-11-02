# Exact boundary counts for Gaussian phase windows

This contribution was produced by Nick Petalas. Apache-2.0.

Scoped counting proof with exact finite corroboration. For the unchanged
physical-period/phase-cell carve in Jose Manuel / jmbarrancoml's
[PR3851](https://github.com/CrocSwap/integer-mult-bounds/pull/3851), the
boundary-row and long-piece counts have a formula requiring only the two
endpoint cells and a fixed number of integer operations. It handles clipped
pieces, negative lifted starts and windows crossing any number of periods.

For one-period windows in the source production domain, the published
allowance improves from

    n_B <= 4mw/d+12w

to

    n_B <= min(m, 2w ceil((t-s)(m-1)/s)+8w).

In the explicit s=480,t=485,w=3,d=48,m=384 window, the old allowance is
132, the new allowance is 48, and the exact count is 30. The execution and
actual number of rows are unchanged. This is a tighter accounting bound,
with no new kappa or selected-frontier change.

[PROOF.md](PROOF.md) gives the all-size formula and its source-domain
implication. It also substitutes the exact row and long-piece counts in
the complete source word-API tariff. This avoids silently charging saved
boundary rows while forgetting their interior charge. The coefficient of
n_B in that tariff is positive only for w>=3.

## Evidence and reproduction

From the repository root, using the CPython 3.12 standard library:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/gaussian-phase-boundary-count/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -O -W error -B research/gaussian-phase-boundary-count/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/gaussian-phase-boundary-count
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/gaussian-phase-boundary-count --check-source-history
```

Another CPython 3.12 path may replace the local path. The scientific marker
is `PASS_GAUSSIAN_PHASE_BOUNDARY_COUNT`. Registered replay runs both modes.
All acceptance checks use explicit exceptions and remain active under -O.
Default replay writes nothing. Optional `--receipt PATH` exclusively creates
a generated source-hash receipt outside the checkout; no receipt is handwritten.

The independent literal checker computes nearest indices from t*j/s and
groups the actual (physical period, nearest-j) keys. It appends one row at
a time and updates the source's threshold rule without calling the closed
form. It checks every s=10..64, w=1..3 and k satisfying the long-cell
hypothesis, every starting residue and every length 1..2s+1. Alternating
residues are shifted into negative periods. All 1,459,710 windows across 319 configurations agree exactly, including
722,570 one-period upper-bound checks. Six semantic and eleven domain controls
pass. Additional fixtures cover
larger periods, translated starts, 4w/4w+1 thresholds and the strict example.
The universal claim comes from the written proof, not these finite cases.

The verifier authenticates the three source inputs before counting. It
imports and executes no predecessor implementation or scientific suite.
Source-byte hashes bind the scope; they do not certify the numerical or
physical correctness inherited from the source.

## Scope, credit and overlap

Source head: `7ab67b4a84d28cd562b9711aa315ca5b47822b37` from PR3851.
Publication base: canonical main `2485805a6d47f36ea83ddde6327d453ac82d44dc`,
priority revision 8. [SOURCES.json](SOURCES.json) pins the retained source
bytes, original card and selected record. [TASK.json](TASK.json) explicitly
changes `uniform-transfer-audit` to this accounting side result for the
analytic/physical caller. No selected assumption is discharged.

Credit Jose Manuel for the complete physical producer/consumer and its
carve, threshold and word-API tariff. Credit Dugongue's
[PR5566](https://github.com/CrocSwap/integer-mult-bounds/pull/5566) for the
related complete Beatty-run inverse and classical floor/run viewpoint;
Vlado Vojdanovski and the phase-cell contributors, RaD/hipotures,
Chafik Boukhalfa's PR481/486/489, the physical word implementation and the
retained Harvey-van der Hoeven/source lineage. Those results are premises
and context, not audit deliverables. Frozen sources and their credit remain
unchanged. Elementary floor arithmetic is classical; no literature-priority
claim is made for it.

The [advance CLAIM](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19292015)
preceded the experiment. Live PRs, recent account work, active Discussions,
local reservations, merged searches and main-tree README formula/object
searches were checked. The card helper had no usable remote cache and
searched only 105 of 8722 local notes; separate live queries and Git-tree
searches supplemented it. Sparse notes, arbitrary diffs and unpublished
work remain outside coverage. These checks are not proof of novelty.

No changed physical planner, numerical Gaussian replay, native supplier,
retained-backing reduction, full tensor/setup bill, improved multiplication
exponent or complete multiplication theorem is supplied. The fixture does
not satisfy every production locality requirement. The full numerical,
compiler, ownership, precision/tape and analytic assumptions remain.
Independent human and formal proof-kernel review are unclaimed. Lean,
Docker and the selected supplier cold replay were not run.

## Open next questions

Can the encoded preparation planner use the exact counts before allocating
boundary banks? Start with one actual Window preparation, charge its encoded
divisions and descriptor access, and compare retained backing and the whole
setup/online bill. A changed physical allocation implementation is missing.
The arithmetic formula alone establishes no storage or runtime reduction.

## Implementation bounds

The verifier is nonrecursive. Functions remain below 60 physical lines.
The exhaustive domain fixes s<=64,w<=3 and at most 129 literal rows per
scan; extra literal scans are capped at 1024. Formula inputs are capped at
4096 bits, including a maximum-capacity fixture. The mathematical theorem
has no such bit cap. Source/package reads are capped at 256 KiB per file.
State is local, there is no dynamic code or scientific subprocess, and
failures propagate. Python's integer, dictionary and temporary allocation
are a managed-runtime deviation from fixed steady-state storage; finite
loop, bit and file bounds constrain this command. Warning-strict normal
and optimized execution are registered. An external static analyzer and
fixed-allocation native implementation are not claimed.
