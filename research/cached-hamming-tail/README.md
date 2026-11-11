# Cached Hamming envelopes in the complete prefix-completion caller

This contribution was produced by Nick Petalas. Apache-2.0.

**Implementation-equivalence proof with exact finite conformance and a measured
local runtime improvement.** A fixed bitset cache replaces the repeated
future-vertex and old/new difference loops in SHIN09-git's PR6046 shared-tail
predicate. The complete five-label, length-twelve no-cap caller retains exactly
the same rejection decisions, traversal and returned word tuples.

Across all thirty alternating fresh-process pairs, the candidate has a **10.96%
lower median paired wall time**, with 28/30 paired wins and zero errors. This is
a local performance observation, not a portable timing guarantee. The cache is
built inside each timed caller. The complete process includes interpreter
startup, imports, source authentication, cache setup, traversal and JSON output.

| Complete process | Median | Minimum | Maximum |
| --- | ---: | ---: | ---: |
| Unchanged source caller | 63.815 ms | 62.508 ms | 72.149 ms |
| Same caller with cached tail predicate | 56.849 ms | 55.466 ms | 167.177 ms |

The slow candidate outlier is retained. An initial nine-pair experiment had
overlapping ranges and inconclusive rank-sum evidence. Before any further
measurement, the decision was to run one additional twenty-one-pair experiment
without changing the timed code and retain all thirty pairs. Both complete raw
receipts are committed. Their combined descriptive two-sided rank-sum
probability is `11226165959/59132290782430712`, about `1.90e-7`. Host contention
and sequential sampling limit its interpretation; it is not a portable speed
certificate. No samples from those two fixed experiments were removed and no
timing threshold runs in CI. An earlier in-process development probe and the
untimed profile were used to choose the implementation, not as published
performance samples.

## The new step

For visited vertices P, endpoint q and remaining budget r, let
`H={x: weight(q XOR x)+weight(x)<=r}`. The predecessor uses `U=H minus P` and
the support `D(P) union (P XOR U)`. The exact identity

```
D(P) union (P XOR U) = (D(P) union (P XOR H)) minus {0}
```

lets the implementation cache H and its XOR translations independently of the
prefix. Differences involving an already visited x are already in D(P), except
zero. The future cardinality still excludes every visited point. This is an
exact implementation of the same predicate, not a new pruning theorem.
[PROOF.md](PROOF.md) gives the equivalence, adapter and resource arguments.

An untimed profile of the original complete caller attributes 0.035 of 0.079
instrumented seconds to `tail_envelope`, including 4,434 calls. Its vertex scan
and nested difference loop are the replaced work. The unchanged parity-union
checks consume 0.029 instrumented seconds and constrain the attainable gain.
[PROFILE.txt](PROFILE.txt) retains the full profile; profiler times are not the
reported wall-time measurement. The measured wall-time reduction is smaller
than the replaced stage's profile share.

The cache has 416 reach entries and 13,312 logical translated entries, with
identical masks sharing tuples. It has a fixed bound and is discarded after
the caller. The three source files are authenticated before loading. The
adapter changes one function on its private source module and restores it on
both success and failure. No predecessor file or maintained engine is edited.

## Evidence and reproduction

Run from the repository root with the recorded CPython 3.12.15 interpreter:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/cached-hamming-tail/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -O -W error -B research/cached-hamming-tail/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/cached-hamming-tail/timing_check.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/cached-hamming-tail
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/cached-hamming-tail --check-source-history
```

An installed CPython 3.12 can replace that interpreter path. Only the standard
library is needed. Direct checks print generated receipts bound to package and
input SHA-256 hashes. They write no package files. Temporary source-corruption
fixtures use the operating system temporary directory and are removed.

The verifier compares all 13,312 translations against literal set translation,
all 21,640 canonical simple prefixes against the source's complete future set,
support mask and rejection decision, and both full returned word tuples. Each
complete caller enters 7,350 nodes, prunes 4,381 and returns 828 closed words,
all universal. Both tuple hashes are
`2e64b75bdd56124eb0993e0dcb2b79f849435465c32bdc9329ea2c171b506727`.
Six controls cover an overpermissive cache, omitted visited set, omitted XOR
translation, unsupported mode, caller-failure restoration and an actual changed
source file. These are checks of the new implementation's equivalence, not a
new scientific audit of the predecessor census or its completion theorem.

`timing_check.py` authenticates every timed source and recomputes all retained
measurement arithmetic. It does not rerun benchmarks or certify host speed.
To collect new measurements, choose an external output path that does not exist:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/cached-hamming-tail/benchmark.py --pairs 9 --output /absolute/external/path.json
```

Each child has a thirty-second timeout. All samples check the counts and both
complete tuple hashes before accepting an output. The recorded machine has
eighteen logical CPUs; load averages at orientation were 1.72, 2.73 and 2.63.
Another Python process was active. Measurements are sequential and alternate
which side runs first. OS caches were not flushed and other host work was not
controlled. The receipts retain the exact platform, interpreter and load data.

## Scope and credit

Scientific base is canonical main `2485805a6d47f36ea83ddde6327d453ac82d44dc`,
priority revision 8. The selected conditional result remains PR6030. The
[advance claim](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19292017)
takes PR6046's explicit cached-envelope runtime question. The `replay-runtime`
card is refined to this standalone caller. This does not alter the selected
frontier, supply a new kappa, or make a complete multiplication theorem claim.

Credit SHIN09-git for PR6046's shared-tail theorem, simplified predicate,
comparison traversal and open implementation question. Credit Ali Romman for
the distinct matching-capacity predicate and incremental matching engine;
Mihir Srivastava for the five-label handoff; Ross Richardson for the prefix-walk
model; Nicholas Stone for the parity correction; unpaidmoon, James Reed and
the retained word-census contributors for their cited work. The earlier
matching-balance, union-support and position-block work retains its attribution.
Classical bitsets, Hamming distance and XOR permutations are not claimed as new.

Live open PRs, active Discussions and recent account work were checked. The
overlap helper covered 316 open PRs with complete pagination at
2026-10-30T11:25:39Z, but only 95 of 8,722 local note records; its broader
Discussion refresh timed out. Separate live GraphQL reads covered start-here,
twelve active Discussions and the latest thirty handoff comments. Main README
and merged-PR searches included cached Hamming envelopes, prefix completion,
incremental pair support and tail bitsets. This bounded coverage is not a
novelty certificate; historical diffs and unpublished work remain limits.

No larger census, maintained-engine integration/default change, full historical
replay, selected cold replay, Lean or Docker run, native/dirty-restoration
construction, supplier admission or all-size theorem is supplied. All five
framework assumptions remain. Independent human and formal proof-kernel review
are unclaimed.

## Open next questions

Does this cache improve a named maintained-engine caller after its complete
setup and other predicates are paid? First select one exact small caller and
budget a full enabled-versus-disabled comparison with identical complete
outputs. A separate integration and resource budget are required; these local
results do not justify a larger census or a default change. No follow-up is
reserved. [TASK.json](TASK.json) records the same question and blockers.
