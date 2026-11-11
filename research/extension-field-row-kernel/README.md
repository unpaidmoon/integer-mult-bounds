# Faster complete extension-field tensor replay

This contribution was produced by Nick Petalas. Apache-2.0.
A prepared finite-field row-update table reduces
the runtime of Ali Romman's complete PR5637 caller. The new contribution is
the bounded arithmetic implementation, exact-output preservation proof and
complete-caller performance experiment. The predecessor's classification,
transporter construction and scientific decisions are credited premises.

```
original rref:  x -> add[x][mul[c][y]] at every row entry
prepared rref:  x -> updates[c][x][y], prepared once per field
```

The private adapter prepares each field and replaces only its module's row
elimination. Every tensor, orbit traversal, witness equation and control
remains in the unchanged source caller. [PROOF.md](PROOF.md) proves equality
of every full output row and ordered pivot column, including augmented
columns. This is stronger than preserving rank alone. No new kappa,
classification, supplier admission or selected-frontier change is claimed.

## Evidence

Five alternating fresh-process pairs reduce median complete wall time from
13.202941292 to 11.016213791 seconds, a 16.56% reduction.
The original range is 12.879240000 to 14.055809667 seconds;
the prepared range is 10.861282875 to 11.409663292 seconds.
All ten processes succeed with zero errors and the same deterministic output
SHA256 `bd7250bb19b92c00baa028d417fed1890aeb0f4865acd8c9f4a782583325f70a`.
CPython 3.12.15, macOS 27.0.1 arm64, 18 logical CPUs. These are local
measurements, including contention from other work.

| Pair | Original seconds | Prepared seconds |
|---|---:|---:|
| 1 | 13.202941292 | 10.861282875 |
| 2 | 12.879240000 | 10.997038458 |
| 3 | 12.914124041 | 11.016213791 |
| 4 | 14.055809667 | 11.148343375 |
| 5 | 13.253169500 | 11.409663292 |

The standalone verifier passes 19,753 complete row-result comparisons,
21,061 fused arithmetic entries and 65 capacity, malformed-input and
arithmetic-mutation controls. It also runs both complete source callers and
compares their deterministic reports. Both retain all 256 F2 and 65,536 F4
tensors, 90 larger changed-basis presentations, 90 special-linear
transporters, 2,322 transported basis products and 125 source controls.

The timing experiment uses five alternating fresh-process pairs, with all
field preparation, authentication, imports, orbit construction and complete
recognition/checking inside the timed interval. No performance threshold is
asserted in CI. The process report includes every sample, errors, platform,
load averages and file hashes. Generated reports and logs are written outside
the checkout. The nondeterministic elapsed-time line alone is excluded from
the complete output comparison.

The separate instrumented profile identifies `rref` as the main cost,
9.655 seconds of an 18.299-second instrumented complete caller. Profiler
timings are not used as the before/after measurement. This is a CPU-bound
Python constant-factor improvement; it changes neither the number of tensor
cases nor the asymptotic elimination cost. Other work may share the machine.

## Reproduce

From the repository root, CPython 3.12 and the standard library:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -X dev -B research/extension-field-row-kernel/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -O -W error -X dev -B research/extension-field-row-kernel/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/extension-field-row-kernel
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/extension-field-row-kernel --check-source-history
```

Expected markers are `PASS_EXTENSION_FIELD_ROW_KERNEL`,
`PASS_REGISTERED_RESEARCH_PACKAGE` and `PASS_RESEARCH_COMMIT_BYTES`.
The package commands emit hash-bound receipts to stdout and write no result
files into the checkout. Another CPython 3.12 path may replace the displayed
interpreter. The benchmark is opt-in and prints its generated JSON report:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/extension-field-row-kernel/benchmark.py --pairs 5
```

`replay.py original` and `replay.py prepared` run a single complete source
caller. Every live source is authenticated before import. The declared
inputs retain their original repository-relative paths in an official
package export; no Git or network is needed for a direct exported replay.

## Scope and limits

Canonical base is `2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority
revision 8. The `replay-runtime` card is refined to this exact caller and
kernel. [TASK.json](TASK.json) records the bounded question and stopping
rule; [SOURCES.json](SOURCES.json) pins the exact scientific source bytes.
The selected record and catalogue are provenance-only inputs.

The engine supports canonical field tables of order at most 25, at most
729 rows and at most 162 columns. These include every call in the retained
complete caller. Larger fields/dimensions and mutation of field arithmetic
after preparation are outside its contract. The source's broader API is
unchanged. A new field owns its own tables, with at most 15,625 fused
entries; no cross-presentation or cross-process cache is reused.

The written proof covers implementation equivalence on this bounded
contract; finite comparisons corroborate it. Local timing is host-specific.
Independent human and formal proof-kernel review are unclaimed. No native
producer/consumer, complete paid invoice, selected cold replay, Lean or
Docker execution is supplied. All five selected framework assumptions remain.

## Open next questions

Can this engine enter a source-owned recognition API with explicit field
and augmented-row capacities? First specify that public contract and retain
full row and pivot-order equality. The current package deliberately uses a
private adapter and keeps the predecessor bytes frozen. This question and
its blocker are also recorded in [TASK.json](TASK.json). No further
optimization is reserved by this result.

## Related open work

The live open-PR check found no other PR targeting this extension-field
recognition caller or its row-elimination runtime. Other numerical and
rank-verifier improvements concern different source callers. Later
split-product and nonsplit recognition packages #5661/#5664 and the
character/transport packages #5656/#5663/#5668 are merged mathematical
extensions; this package makes no automatic transfer of its bounded adapter
or measurement to them. No extra computations compare their results.

## Credit

Ali Romman, PR5637 at `86389e525d3efafe236e929f6ae401c68be1d115`, supplies
the finite-field arithmetic, complete caller, recognition and special-linear
transport, building on PR5540/5525 and Nick Petalas's PR5252 nucleus lineage.
apoursh's PR5502 supplies the height criterion; Ali Romman's PR5459 supplies
the character formula. David Ganz and all retained tensor/atlas predecessors
keep their credit. Finite-field elimination and table-driven arithmetic are
classical. Only the new implementation, equivalence argument and experiment
are claimed here, without a general literature-priority claim.

The advance [claim](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19299672)
records the scope. Live Discussion and open-PR searches, merged object/formula
searches and all tracked main package notes were checked. Unpublished work
and arbitrary historical diffs remain coverage limits; absent matches do not
prove novelty.
