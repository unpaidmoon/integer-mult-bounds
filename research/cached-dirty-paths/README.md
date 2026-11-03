# Shared-prefix replay for complete dirty-circuit certificates

This contribution was produced by Nick Petalas. Apache-2.0.

Claim type: exact implementation-preservation argument and measured performance
improvement. The complete PR5235 scientific caller runs with a prefix cache
local to each certificate check. No new dirty-circuit theorem, supplier,
selected-frontier update or kappa is claimed. Independent human and formal
proof-kernel review are unclaimed.

## Result and evidence

The implementation replaces repeated rooted path traversal with a trie. Every
requested output role owns a separate root. All certificate predicates and every
initial,
terminal and operator-closure equation remain in place. The source producer,
field arithmetic, fixtures and complete scientific caller are unchanged.

Five alternating runs per side give a **22.57% reduction** in complete replay
wall time, with zero failures and identical scientific output.

| Complete replay | Median seconds | Range seconds |
| --- | ---: | ---: |
| baseline | 5.680195 | 5.459807 to 6.071584 |
| cached | 4.398449 | 4.318587 to 4.558831 |

The timed path includes interpreter startup, authentication of thirteen source
files, imports, the complete scientific replay and its output. Only the two
explicit elapsed-time fields are removed for scientific output comparison.
Every replay retains 210 echo identities, 120 differential circuits,
180 literal counterexamples, 15 certificate rejections, 9 input rejections,
596 finite-field operations, 51 Gaussian controls, three committed examples
and the 130-state, 65-basis-row exponential-support fixture with 2^64 words.
These are predecessor coverage counts, preserved here, not new mathematical results.

An untimed profile found rooted path evaluation used 5.906 of 20.534 instrumented
seconds. Those times identify the changed work and are excluded from performance
samples. Producer elimination and full closure checks remain paid. The machine
has 18 logical CPUs and other research processes may run concurrently. Alternating
the sides limits drift. These are local measurements, not a portable speed ratio.

## Why the checker accepts the same certificates

For ordinary JSON inputs, fix one call, its reconstructed roots and exact
transition function. Define
R(i,empty)=root_i and R(i,wa)=step(R(i,w),a). The old function evaluates this
recursion by a finite loop on each requested word.

The new trie starts with root_i. When a child labelled a is absent, it stores
step(R(i,w),a). Induction on prefix length proves that every stored row equals
the old R(i,w). An existing child therefore returns exactly the old result.
Roots remain keyed by output role, and the trie belongs to one check call.
No reuse crosses problems, fields, shifted interpretations or certificates.

Stored row dictionaries remain unchanged. The retained transition, terminal
and linear-combination functions build new dictionaries, and scalar operations
do not mutate operands. Every request still checks its output index and every
symbol before consulting the cache. A valid cached prefix cannot bypass path
validation. The rest of the checker is byte-for-byte unchanged. `verify.py`
reverses the declared cache-only edit and requires exact equality with the
authenticated predecessor source.

Let P be the sum of requested path lengths, U the number of distinct nonempty
rooted prefixes and R the number of requested roots. The old path evaluator
applies P transitions; the cache applies U. Full closure evaluation is unchanged.
For S dependency states, each sparse row has at most S entries, so extra retained
space is O(S(U+R)). This is a memory tradeoff, not a constant-memory claim.

New controls use two roots with shared symbol sequences over Q, Q(i), F2, F3
and F5, degrees one through eight, and both shifted interpretations. They compare
verdicts and check the exact P-U transition saving. Repeated calls test cache
lifetime. Both implementations reject malformed shared-prefix paths, Boolean or
out-of-range roles, missing initial/closure coverage and wrong source digests.
The complete old and new scientific outputs must agree as well.

## Reproduce

From the repository root, using standard-library CPython 3.12:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/cached-dirty-paths
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/cached-dirty-paths/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -O -B research/cached-dirty-paths/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/cached-dirty-paths --check-source-history
```

Expected result: `PASS_CACHED_DIRTY_PATHS`. Registered checks run both complete
variants and all new controls. Normal execution writes nothing. Any CPython 3.12
executable can replace the absolute interpreter path.

For a fresh ten-run measurement, choose a new path outside the checkout:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/cached-dirty-paths/benchmark.py --receipt /absolute/new/external/benchmark.json
```

`BENCHMARK.json` is the retained generated measurement artifact. Replay checks
its executable/input hashes, success count, exact scientific output and derived
medians. A fresh measurement need not reproduce the local wall times. It must
preserve the scientific output. Every live source file is pinned by SHA256 and
Git blob in SOURCES.json and declared in VERIFY.json.

## Scope and implementation constraints

Only this opt-in package changes. The retained PR5235 package stays immutable.
`replay.py --baseline` uses its checker; the default uses the cached copy. The
wrapper authenticates every source file before loading it. The copied checker
keeps its original attribution. No general adoption is made here.

New cache code has no recursion, eviction or global result cache. Traversal is
bounded by word length. The new fixtures have at most sixteen unary calls;
the retained complete caller bounds the shipped replay. The benchmark has ten
child processes with 90-second deadlines and captures bounded complete reports.

Power-of-ten deviations: Python dictionaries and exact arithmetic allocate during
execution. The cache bound above and fixed replay domains constrain live memory;
no fixed-allocation compliance is claimed. The retained independently transcribed
`reconstruct` function is 86 lines and remains byte-identical. Splitting it would
exceed this cache-only change and its exact-delta gate. New functions are below
60 lines. The fixed-module loader is needed to run the unchanged caller and
authenticates its source inventory first. Warning-strict normal and optimized
Python, exact-delta and behavioral checks provide the available diagnostics.
A future larger adapter must price its cache memory explicitly.

No selected supplier replay, native/physical admission, rounded execution,
compiler closure, storage/stock/tape pricing, analytic recovery, Lean, Docker or
independent human review is supplied. The five selected framework assumptions
remain. Faster replay does not improve the selected multiplication bound.

## Open next questions

Can a larger source-bound independent-symbol program retain the benefit within
a stated peak-memory budget? Start by measuring its rooted-prefix count and
sparse-row sizes, then compare the complete producer/checker path. A compatible
real adapter and measured memory budget are blockers. The present cache avoids
no transitions when every requested prefix is distinct.

## Credit and overlap

zxv / [PR5235](https://github.com/CrocSwap/integer-mult-bounds/pull/5235) supplies
the compiler, independent checker, scalar layer, proof, fixtures and explicit
repeated-path performance handoff. Classical weighted-automata equivalence and
noncommutative identity testing retain their Kiefer and Raz-Shpilka credit.
The echo scheduler retains androolloyd, Chafik Boukhalfa / PR628 and Ali Romman /
PR621 credit. Cinna Davis / PR4100 and PR4088, ToikY, Sagar Thakrar, roger-sato,
Charles Bethin and Ross Richardson retain the dirty-phase, tensor and register
attribution in the predecessor README. No predecessor mathematics is claimed
or audited as this contribution.

The cache, preservation argument and measurements were produced by Nick Petalas.
The target was reserved in the [advance CLAIM](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19294845).
Live PRs, active Discussions, local reservations, recent account work, main README
text and merged object/formula searches were checked. The cached search covered
333 open PRs and 6,046 Discussion records but omitted 8,623 sparse main notes.
Separate Git searches covered relevant main README text. Arbitrary diffs,
unpublished work and later publications remain outside that coverage.
These searches do not establish global novelty.
