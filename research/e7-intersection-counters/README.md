# Faster complete E7 replay using intersection counters

This contribution was produced by Nick Petalas. Apache-2.0.

Claim type: measured verifier improvement with a scoped equivalence proof
and exact finite conformance. No new kappa is claimed.

The complete current E7 classification replay has median time 0.290648 s
with intersection counters, versus 0.370508 s with Ali Romman's PR5729
bit-lane engine. That is a 21.55% reduction on this host. Five alternating
fresh processes per engine have ranges 0.287772..0.293084 s and
0.366887..0.372666 s, respectively. All ten outputs are byte-identical,
with zero failures. [BENCHMARK.json](BENCHMARK.json) is the generated receipt
with raw samples, interpreter/environment and implementation hashes.

The new step uses

```text
wt(u xor v) = wt(u) + wt(v) - 2 wt(u and v).
```

It computes fixed lane weights once, then counts only columns selected by
the changing offset. Exact bit-plane addition and subtraction recover every
translated weight. [PROOF.md](PROOF.md) covers modular wraparound, every
coefficient assignment and iterator order. All complete classification
checks still run in the unchanged consumer.

## Reproduce

From the repository root, use CPython 3.12 and its standard library:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/e7-intersection-counters/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -O -B research/e7-intersection-counters/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/e7-intersection-counters
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/e7-intersection-counters --check-source-history
```

Another CPython 3.12 path can replace this host's path. Expected markers are
`PASS_E7_INTERSECTION_COUNTERS` and `PASS_REGISTERED_RESEARCH_PACKAGE`.
Default replay writes no files and prints a generated receipt bound to all
ten package files. The registered commands exercise normal and optimized
Python, including two complete fresh scientific callers in each mode.

For the opt-in accelerated complete replay:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/e7-intersection-counters/replay.py
```

Add `--engine original` for the current PR5729 comparator. To generate new
local timings, run `benchmark.py --output /absolute/path/outside/package.json`
with the same interpreter and flags. Timing includes process startup,
source authentication, imports, complete code enumeration, all downstream
classification checks, receipt comparison and output. The additional generic
conformance suite is outside that performance comparison.

The verifier enumerates 34,525 complete small-code comparisons on 1,381
independent generator sets, 108 wide-code cases and 87,381 scalar word pairs
for the new arithmetic. It rejects sixteen malformed or over-capacity inputs
and checks three changed-input histories. Outputs retain the original
iterator order. The complete E7 consumer compares its entire internal result
with the retained receipt, then emits identical output with both engines.

## Measurement and scope

The unreported baseline profile puts 0.236 of 0.623 instrumented seconds in
population-plane counting. Reflection transport and rational elimination
remain substantial unchanged costs, limiting the complete speedup. This
profile is diagnostic and is not one of the ten timing samples. Both timed
engines use the current default batch size sixteen. No stale original Gray
iterator is used as the comparator.

Measurements used CPython 3.12.15, macOS arm64 and eighteen logical CPUs.
The entry load averages were 1.46, 2.83 and 2.48; other work can share the
host. Alternating serial processes give both engines the same exposure to
that noise. This is a local observation, not a hardware-independent speed
promise, a multiplication runtime benchmark or a CI timing certificate.

The adapter accepts widths 0..127, at most 27 independent generators,
batch sizes 1..20 and at most 65,536 high-offset batches. These explicit
capacities include the complete E7 caller. They restrict the generic helper
interface, not the scientific replay's coefficient coverage. A generator
outside those capacities is rejected, rather than partially enumerated.
This is an opt-in standalone consumer substitution; production adoption,
concurrent shared-process use and other codes are outside the claim.

## Provenance and credit

Base main is `2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority revision 8.
SOURCES.json pins all six live inputs. The selected-binding first example
passes at conditional kappa .003125804; no selected cold replay is run.
The `replay-runtime` card is refined to this originally posed counter
implementation question. It changes no scientific support theorem.

Credit Ali Romman's [PR5729](https://github.com/CrocSwap/integer-mult-bounds/pull/5729)
for the bit-lane representation, Boolean population/threshold routines and
complete consumer, and his [PR5669](https://github.com/CrocSwap/integer-mult-bounds/pull/5669)
for the classification and retained checks. Nick Petalas's PR5238 supplies
the inherited geometry. Their source files and credit lines stay unchanged.
The weight identity and binary arithmetic are classical; the new contribution
is their intersection-count implementation and complete-command evidence.
No general literature-priority claim is made.

Live claims, open PRs, recent account work, main READMEs and merged formula
searches were checked. Sparse local coverage is incomplete. The canonical
[claim](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19294736)
records the corrected target. No predecessor audit is the deliverable.
Independent human and formal proof-kernel review are unclaimed. There is no
new native/physical caller, compiler, precision/tape, BIT or outer admission;
Lean, Docker and the selected scientific replay were not run.

## Open next questions

Can this opt-in engine replace the production iterator at a named caller
boundary, with regenerated dependent source pins? Begin with one explicit
installation and source-bound compatibility check. This package preserves
frozen sources and supplies the complete opt-in comparison; production
integration is separate. TASK.json records relevance, first step and blockers.
No further optimization or mathematical search is reserved.

## Verifier constraints

New functions are below sixty physical lines. There is no recursion. Explicit
capacities bound rows, bit lanes, widths, batches, subprocesses and timeouts.
The largest bit-lane table has 127 columns of at most 2^20 bits. The fixed
verification fixtures use smaller tables and at most 1,024 literal words.
Every complete child process has a sixty-second timeout and its exit status,
stderr and exact output are checked.

Power of Ten rules 3 and 9 require managed-runtime deviations. Python allocates
bounded integers, tuples and lists during checking. `run_path` dispatches
only to named local source/adapter files, after authenticating external
inputs. The partial iterator has exactly the retained population/threshold
helpers as injected call targets. Each standalone process owns its temporary
consumer binding. Warnings are errors in both registered modes; no shared
source, diagnostics configuration or repository-wide suite changes.
