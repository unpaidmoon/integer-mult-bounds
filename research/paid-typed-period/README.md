# An exact search-depth obstruction for paid typed switching

Scoped written proof with exact finite corroboration. Two synchronized
recursive modes can require an arbitrarily long first profitable period,
even with two computational types, two modes and a charged recursive
adapter at every cyclic mode change. No new kappa is claimed.

For integers N>=2 and h>=0, take

    A = diag(2, 1/2), B = diag(2^(-N), 2^(N-1)),
    adapter at every cyclic mode change = 2^h I.

The exact minimum number of supplier layers in a strict-contraction word is

    (2h+1)(2N+1).

The word A^((2h+1)(2N-1)) B^(4h+2) attains it. Its two adapters include the
last-to-first boundary, and its complete product is I/2. Neither fixed mode
contracts both types. [PROOF.md](PROOF.md) proves the minimum for every N,h,
constructs rational phase reserves with unit forcing at every stage, and
realizes every stage as an integer child-rank moment at any rational
exponent between zero and one.

For N=2,h=1 at exponent 1/2, a common parent width 16 gives child counts
A=(8,2), B=(1,8), and adapter=(8,8), with every child of rank one. The first
profitable word has 15 supplier layers and two adapters. Its complete
macro has 2^33 descendants of size ratio 2^(-68), giving exponent 33/68
on period-aligned sizes. This is an abstract branching recurrence, not an
operation computing multiplication or a native supplier.

## What this changes

A finite composition search cannot use the number of computational types
and available modes alone to justify its maximum depth. This family supplies
an exact obstruction with all of its declared recursive conversion costs
included. Matrix entries and their bit lengths grow with N. A bound that
also depends on the input coefficients is outside the result.

The synchronized-mode restriction matters. Choosing a different mode for
each computational type allows type one to select B and type two to select
A immediately. The phase-expanded dimension also grows with the period.
The result does not refute a search bound for a fixed fully expanded matrix.

This is an explicit analytical side result from the `coverage-law-change`
card, recorded in [TASK.json](TASK.json). The source-binding first example
passed at base `2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority revision 8.
The selected result remains #6030, conditional kappa 781451/250000000.
The [advance claim](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19294704)
records the same scope. Main formula/object searches, merged PR searches,
live open PRs, active Discussions, recent account work and local reservations
were checked. These searches do not establish global novelty.

## Evidence

The replay writes a generated JSON receipt with hashes of all seven package
files. It writes no files into the package. Its finite domains are distinct
from the all-parameter written proof.

- All 49,140 cyclic words of lengths 1 through 12 at N=2,3,4 and h=0,1
  have the same invoice under literal 2 by 2 Fraction matrix multiplication
  and the new stage builder. Every rotation boundary is charged.
- All 550,298 realizable count triples through the predicted first passing
  length, for N=2 through 8 and h=0 through 3, are checked by multiplying
  positive integer child multiplicities and comparing with the exact
  denominator. This oracle does not use the proof's exponent inequalities.
  A mixed binary cycle has 2r changes exactly when 1<=r<=min(x,y), since its
  x A's and y B's can be divided into r nonempty alternating runs. Pure words
  have zero changes. This accounts for the whole enumerated domain.
- The constructor attains I/2 on 155 parameter pairs, N=2 through 32 and
  h=0 through 4. Eight phase-expanded examples give 288 exact positive
  reserve equations, including a unit charge at each adapter.
- There are 672 exact integer stage-moment realizations across four rational
  exponents, plus the complete 15-layer example invoice. Eighteen boundary
  and mathematical controls cover invalid inputs, nonstrict cycles, missing
  conversion charges, a short unpaid witness and both pure modes.

The checker imports no predecessor implementation and runs no predecessor
scientific suite. Normal and optimized modes keep every acceptance and
rejection check active.

## Reproduce

From the repository root, with CPython 3.12 and its standard library:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -W error -B research/paid-typed-period/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -W error -O -B research/paid-typed-period/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/paid-typed-period
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/paid-typed-period --check-source-history
```

Another CPython 3.12 path may replace the displayed local interpreter path.
Expected markers are `PASS_PAID_TYPED_PERIOD`,
`PASS_REGISTERED_RESEARCH_PACKAGE`, and `PASS_RESEARCH_COMMIT_BYTES`.
The two registered scientific commands each have a 180-second limit.

## Limits and engineering notes

The reference constructor accepts N in 2..64, h in 0..8 and words of at most
4,096 supplier layers. Reserve construction is limited to 128 full phases.
The proof has no such finite parameter cutoff. It requires the exact
diagonal modes, synchronized choice, cyclic return and recursive adapters
specified above. More general adapters and unknown physical fees are outside
the invoice. Integer child moments alone do not establish that any useful
linear or multiplication target can be supplied.

The verifier has fixed enumeration bounds, streams its censuses, reads exactly
seven named package files of at most one MiB each, and uses exact integers and
Fractions. There is no recursion, dynamic evaluation, generated code or
external process in the scientific replay. Functions are below 60 lines.
Assertions document construction invariants; explicit checks decide acceptance
under optimization too. The rejection fixture has eleven explicitly bounded
local callback targets.

Python requires dynamic allocation, a deviation from Power of Ten rule 3.
Its scope is the fixed domains above. The model has at most 8,192 stage
entries, each stage exponent has absolute value at most 72, and the reserve
has at most 128 phase pairs. These bounds also bound rational bit growth and
live memory; enumeration does not retain earlier words or triples. Warning
strict normal and optimized replay, in-memory compilation, and source review
provide diagnostics. No ruff, mypy or pyright executable was found on PATH;
a separate static analyzer was not run. A larger domain would require revisiting
these bounds before changing the constants.

No physical caller, native implementation, dirty restoration, ownership,
stock, precision/tape or outer recovery is supplied. Selected cold replay,
native replay, Lean and Docker are unrun. Independent human and formal
proof-kernel review are unclaimed.

## Open next questions

Does an actual source-compatible caller require synchronized recursive modes
with a favorable paid period? Extract both mode contracts and every
type-specific child list, including conversions at both boundaries. This
could turn the search-depth obstruction into a supplier improvement. No
physical producer/consumer or complete native/restoration/precision/storage
invoice is supplied here, which blocks that transfer. This result does not
justify a wider search over abstract modes without such a caller.

## Credit

This contribution was produced by Nick Petalas. The exact paid period family,
its minimum and its integer child-rank realization are the new scoped result.
Positive-vector and cyclic recurrence certificates are classical, and are
already retained in A051, A054, A055 and A057 of
[the analytic theory](../kappa-action-theory/volumes/04-analytic.md).
Ross Richardson's [PR2881](https://github.com/CrocSwap/integer-mult-bounds/pull/2881)
settles a different single-type seed-switching question. Gonzalo Mier's
[PR4034](https://github.com/CrocSwap/integer-mult-bounds/pull/4034)
records the existing fixed typed-matrix method and the need for actual caller
contracts. Those contributions are cited, not re-audited.
Periodic stabilizing products are established switched-system theory; see
Ettore Fornasini and Maria Elena Valcher,
[Stability and stabilizability criteria for discrete-time positive switched systems](https://www.research.unipd.it/handle/11577/2488007),
2012, DOI 10.1109/TAC.2011.2173416. No priority is claimed for that general
theory. Exact repository source pins are in [SOURCES.json](SOURCES.json).
Apache-2.0.
