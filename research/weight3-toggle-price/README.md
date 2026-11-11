# A weight-3 connector step costs `72o + 76p`

**Scoped proof with one exhaustive finite census and an attaining schedule.
No new κ.** Selected κ stays `363005817/100000000000`.

On the five-source, 31-row dirty connector, every nonempty source subset is
allowed as one toggle. Dispatch price is `o >= 0` and each source or readout
addition costs `p > 0`. The DUO schedule costs `72o + 74p`. This package
answers the weight-3 half of the open price question in
[PR #6695](https://github.com/CrocSwap/integer-mult-bounds/pull/6695): every
correct schedule that uses at least one weight-3 toggle costs at least
`72o + 76p`, and a schedule attains that price. The weight-3 extension is
therefore exactly `2p` more expensive than the DUO point for every `o >= 0`
and `p > 0`. It is not a favorable alphabet extension.

## Interface

The batch is the one in `research/universal-connector-boundary`: five
read-only sources, one arbitrarily dirty connector `z`, and all 31 nonzero
output rows. A call `T_S` adds `sum_{j in S} B_j x_j` into `z` and costs one
dispatch plus `|S|` additions. A readout `A_m` costs one dispatch and one
addition. Maps are arbitrary `F_2`-linear maps. They need not commute or be
invertible. Private scratch and tape heads are restored by each call. Outputs
are unobserved until the batch completes. There is no joint readout, second
connector, frame change, or source mutation.

The lower bound uses the identity-map, one-bit specialization, which is
necessary for a schedule that is correct for every admissible map and every
dirty input. The attaining schedule is replayed on formal symbols, so it is
correct for every map, and on explicit dirty vectors.

## Result

Let `T` be the number of toggles and `W` their total source additions. Prefix
differences are translation invariant, so the initial prefix may be taken to
be `0`. Let `u` be the number of nonzero rows that are not a difference of
two prefixes.
Each of the 31 rows needs an even positive number of readouts, because the
initial dirt in `z` is arbitrary, and a row that is not a prefix difference
needs at least four. Thus the readout count is at least `62 + 2u`, the query
count is `Q >= T + 62 + 2u`, and the addition count is `A >= W + 62 + 2u`.

**Theorem.** Every correct schedule with at least one weight-3 toggle has
`Q >= 72` and `A >= 76`. Both bounds are attained by the same schedule, so
the minimum price is `72o + 76p`. The recomputed DUO schedule, which uses no
weight-3 step, costs `72o + 74p`.

A positive per-call surcharge on weight-3 toggles, beyond the three source
additions already counted, would make this schedule strictly worse. The
operation is not treated as free.

## Proof

Closed walks in `F_2^5` have even `W`, because every source incidence is
even. A walk of length `T` with at least one weight-3 step therefore has
`W >= T + 2`, and `W >= T + 3` when `T` is odd: `T + 2` is then odd, so it
is not a legal addition count. Let `s` be the number of distinct prefixes.
Then `T >= s`, and `u` is at least `max(0, 31 - C(s, 2))`. For `s <= 8` this
counting bound is already at least 3. For `s = 9` counting allows a cover,
but none exists:

Differences are translation invariant, so one prefix may be moved to `0`.
A covering set spans `F_2^5` and therefore contains a basis. Every linear
automorphism preserves the property of being a difference basis, and `GL(5,2)`
can send any ordered basis to the standard basis. The other three points then
lie among the remaining 26 vectors. All `C(26, 3) = 2,600` such sets were
checked. None covers. The same enumerator finds 80 covers with four extra
points, which is the ten-point normal-form count recomputed by PR #6695, so
the empty nine-point result is not an empty search. Consequently `u >= 1`
whenever `s <= 9`.

Under those floors, the only pair `(T, s)` whose addition lower bound
`W_min(T) + 2u` is strictly less than 14 is `T = 10`, `s = 10`, `u = 0`,
where `W_min = 12`. Lengths 1 through 40 are the whole region in which that
bound can sit below 14: at length 40 or more, `W` is at least 42. The same
scan gives `T + 2u >= 10` in every legal pair, so `Q >= 72`. The exceptional addition corner is a closed ten-step walk with
`W = 12` and one weight-3 step, hence exactly nine singletons. Rotating that
step to the end translates the prefix set and preserves differences. The
closing triple is the XOR of the nine singleton labels. All `5^9 = 1,953,125`
label words were scanned. Exactly 1,208,400 have XOR weight 3; a separate
length-9 dynamic program counts the same 1,208,400. Among the words with ten
distinct prefixes, none has all 31 nonzero differences. The best has 29, so
at least two rows are missing. A word with fewer than ten prefixes cannot
cover, by the nine-point exclusion and the `s <= 8` count. The corner is
empty. Every remaining schedule has `W + 2u >= 14`, hence `A >= 76`.

This census is the equality case of the price proof. It agrees with the
30-of-32 mask maximum in `research/one-triple-ten-step-obstruction` (29
nonzero differences plus the automatic zero difference). That package prices
the source-leaf bill under exactly two readouts per row. It does not price
four-readout repairs or a mixed DUO word, and it does not exhibit a
`(72, 76)` schedule.

## Attaining schedule

Step masks, with `14 = {1,2,3}`, `24 = {3,4}` and `12 = {2,3}`:

```text
8, 1, 16, 14, 16, 1, 16, 2, 24, 12
```

The walk is closed, the ten prefixes are distinct, and their differences are
all of `F_2^5`. It uses one triple, two DUOs and seven singletons, so
`T = 10` and `W = 14`. Placing two readouts on the first boundary pair of
each nonzero row produces 72 calls and 76 additions. The formal-symbol replay
accepts that schedule for every linear map and every dirty input. A fixed
width-3 trial uses identity maps, source vectors `(1, 2, 3, 4, 5)`, connector
dirt `7` and row dirt `(3m + 1) mod 8`. Forty further trials use independent
pseudorandom maps and dirt. Dropping the readout of row 1 is rejected. The
word was found by a random search; the verifier checks this word only and
does not rerun the search.

The published DUO word `1, 2, 8, 18, 12, 16, 1, 2, 4, 2` is rebuilt by the
same scheduler. It costs `(72, 74)`, passes the formal replay, and contains
no weight-3 step. The published near-cover `1, 8, 1, 2, 1, 16, 4, 8, 16, 7`
misses exactly two rows, so its repaired addition floor is 78. It is not a
counterexample to 76.

## What this does not show

The theorem is only for schedules that contain a weight-3 toggle, on this
five-source batch, in the dispatch-plus-addition ledger above. It is not a
bound for weight 4, for six or more sources, for joint readouts, or for a
physical frame, routing, or tape surcharge. PR #3909 prices one arity-four
family in a different unit sum and is not this result. No supplier, native
word, or selected-frontier change follows. The nine-point exclusion and the
ten-step census are exhaustive finite checks, not a proof-assistant
derivation. The random search that proposed the witness is not a census of
attaining words.

## Reproduce

From the repository root, CPython 3.12, standard library only. The census
finishes in a few seconds.

```sh
python3 -B research/weight3-toggle-price/verify.py
python3 -I -O -W error -B research/weight3-toggle-price/verify.py
python3 -B scripts/research_package.py --package research/weight3-toggle-price
```

Expected marker:

```text
PASS_WEIGHT3_TOGGLE_PRICE queries=72 additions=76 duo=(72,74) nine_point_covers=0 weight3_full_covers=0 best_nonzero=29 weight3_sequences=1208400 no_new_kappa
```

The orientation command `python3 -B research/universal-connector-boundary/verify.py`
was run once and printed
`PASS_UNIVERSAL_CONNECTOR_BOUNDARY pairings=945 max_coverage=31 queries=74 leaves=182`.
That is the card's positive control, not evidence for this theorem. Selected
cold replay, Lean, Docker and a proof-kernel check were not run.

## Open next questions

1. What is the exact `oQ + pA` price of a schedule that contains a weight-4
   toggle and no assumption that a weight-3 toggle is present? The same case
   split applies, but the equality corner is a different census: a weight-4
   step changes the parity and the minimum addition count. PR #6695 leaves
   this half open. Open PR #3909 uses another unit ledger and does not answer
   it. Nothing structural blocks the census.
2. Does the same one-point collapse give `Q` and `A` floors at six sources
   for every toggle alphabet? PR #6695 already asks this. A six-source
   difference-basis count is larger than the five-source normal form used
   here, and the five-source floors do not transfer.

## Credit

Ross Richardson, PR #943, supplied the dirty-connector interface and the
prefix-difference readout criterion. The DUO word and the `72o + 74p` point
are from `research/duo-toggle-connector`. Nick Petalas, PR #6695
(`research/five-source-toggle-frontier`), proved the all-alphabet floor
`72o + 74p`, the weight-5 floor `72o + 78p`, and left the weight-3 and
weight-4 prices open; the ten-point normal-form count 80 is the control
recomputed there. Nick Petalas, `research/one-triple-ten-step-obstruction`,
proved the two-readout incidence-12 non-cover and the source-leaf bill 122;
this package recomputes the non-cover as its equality case and does not
restate that leaf theorem. Riquelme Soares, `research/atomic-trio-connector`,
priced the triple in the older frame-plus-application ledger. Those results
are cited and, where a number is reused as a control, recomputed. They were
not audited.

Prepared by unpaidmoon with substantial Cursor Grok assistance. New work is
Apache-2.0. No independent human or formal-kernel review is claimed.
