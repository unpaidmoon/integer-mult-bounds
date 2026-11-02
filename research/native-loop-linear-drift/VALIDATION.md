# Validation boundary and implementation constraints

This contribution is produced by Nick Petalas.

The direct normal and optimized checks passed on the required CPython 3.12
interpreter. Both produced identical generated receipts. No hosted pass is
currently claimed.

## Exact coverage

`verify.py` authenticates PR5492's unchanged recipe JSON before decoding it.
It derives the four-coordinate circuit from all eight 512-coordinate signed
wrappers, checks the new 96-edge orbit against a second full-bank decoder,
and tests all eight shift-pair parity premises. The written proof turns
these finite facts into the universal iterate and correction-state results.
No predecessor verifier or receipt is imported or executed.

The receipt includes each package file's SHA256, the exact source hash,
all 25 cycle-boundary vectors, the shift cuts and the hash of all 96 edge
cuts. It is generated on demand, and is never handwritten. Its normal and
optimized bytes must agree. Finite checks do not establish mathematical
literature priority, human acceptance or proof-assistant acceptance.

## Engineering inspection

Playbook: investigation. The original assignment also authorizes adding a
new scoped package. Build the Lever led to the standalone, deterministic
certificate checker; Prove It Works led to full-bank comparison at every
new orbit edge and direct Git-free replay. Unslop applies to the prose.

The checker has no recursion, network, subprocess, dynamic code loading or
third-party dependency. All science loops have explicit fixed bounds:
512 addresses, nine bits, 24 traversals, four stages, 256 pairs per ambient
edge, 128 covariance fixtures, 2,401 pair inputs, 769 consecutive iterates,
and 33 collision paths of at most 768 traversals each. Source files are
limited to 64 KiB, package hashing to 16 files of at most 1 MiB each, and
receipt reads to 1 MiB. Each function is below 60 physical lines. Schema
and range checks occur before source-controlled loops. Explicit exceptions
keep acceptance active under `-O`. The source is read-only; the only optional
write creates a new receipt outside the checkout and checks the byte count.

Power of Ten rule 3 deviation: CPython allocates integers, tuples, lists and
JSON data during the bounded check. The fixed dimensions and iteration
limits bound live mathematical storage. The largest primary state is the
512-coordinate bank; only 96 four-coordinate cuts and 25 orbit boundaries
are retained. The loaded JSON and eight 512-entry plans are fixed-size
setup data. Python allocator internals are not a byte-exact heap bound.
Replacing managed allocation would require a separate runtime and becomes
a follow-up only if this checker becomes a reusable unbounded service.

Power of Ten rule 10 boundary: warning-strict normal and optimized Python
runs are registered. No separate static analyzer is configured for this
isolated standard-library package. AST inspection checks function lengths
and syntax without generating bytecode. No repository-wide tooling change
is part of the scientific result.

The exact proof, code and diff received local self-review. Independent human
and formal proof-kernel review remain unclaimed.

## Local and hosted checks

Both exact registered commands were also timed individually on local
CPython 3.12. Normal execution completed in 0.741 seconds and optimized
execution in 0.747 seconds, each with return code zero and identical output.
These single observations check the replay deadline; no speedup or portable
timing guarantee is claimed. The enclosing registered replay reported
`PASS_REGISTERED_RESEARCH_PACKAGE` with outcome `negative-result`.

AST inspection passed for all 21 functions, with a maximum of 31 physical
lines, and whitespace checks passed. Publication-byte/source-history and
official export checks run against the publication commit and are reported
in the PR body. The direct exported verifier needs only this package and its
one declared recipe input; no Git executable is required.

The selected baseline orientation reported
`PASS_RESEARCH_BASELINE_BINDINGS_ONLY` for selected PR6030 at canonical main
`2485805a6d47f36ea83ddde6327d453ac82d44dc`. This authenticates bindings and
metadata; it is not a selected science replay. The final upstream refresh
retained that main commit and unchanged relevant guidance, selected record
and recipe inputs.

Full selected supplier replay, other tensor widths, chronological caller
embedding, physical tape realization, dynamic-grid error analysis, Lean,
Docker, all-size multiplication and hosted CI are unrun here.
