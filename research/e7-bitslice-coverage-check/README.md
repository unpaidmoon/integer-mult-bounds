# The E7 bit-lane iterator keeps every weight-at-most-12 kernel word

**Coverage check of a published replay optimization. No new κ.** The selected
conditional exponent stays `781451/250000000`. PR #5729's bit-lane engine
returns the same weight-at-most-12 words as an independent census of the
27-dimensional E7 kernel. That census sees all `2^27` codewords. Zero and
exactly 1638 weight-12 words occur, and no nonzero word is lighter.

## Result

The kernel basis is the one constructed by the pinned PR #5238 geometry:
135 frame-parity rows, binary rank 36, and 27 free coordinates on which the
basis is the identity. The census splits that ordered basis in two ways,
after 13 generators and after 16. Each half is listed by doubling. A pair
`(high, low)` contributes `high XOR low`, scored by integer popcount. The
two splits return one set:

| Quantity | Value |
|---|---:|
| Distinct codewords | 134217728 |
| Nonzero codewords | 134217727 |
| Least positive weight | 12 |
| Words of weight at most 12 | 1639 |
| Words of weight 12 | 1638 |

`low_weight_words` from `research/e7-bitsliced-exhaustion/binary.py`, at batch
sizes 16 and 8, returns that set with no repeated yield. These counts are
the `minimum_support`, `minimum_supports` and `nonzero_codewords` fields of
the predecessor receipt `source/RESULT.json`.

The half-split does not call `low_weight_words`, `full_weight_census`, or the
Gray-code loop in the predecessor verifier. Batch size changes the engine's
lane width, not the returned set. A copy of the set with one support removed
compares unequal. Clearing the top bit of a support produces a weight-11 word
that is absent from the code, and the weight predicate rejects a set that
contains it. On generators `(1, 2, 4)`, the same census, a literal doubling
and the engine agree at weight bound 1, and weight bound 0 returns only zero.

## Scope

Task card `replay-runtime`, priority revision 8, base
`2485805a6d47f36ea83ddde6327d453ac82d44dc`. Scope status is **refined**.

The card asks for a new measured speedup that keeps coverage. The revision-8
verification row instead asks that the already published #5729 speedup be
checked before faster output is treated as the same coverage. Intake records
#5729 as `merged_for_archive_only`: the author evidence was not independently
replayed. This package is that replay's coverage comparison on the full E7
kernel. It does not time the engine, replace a consumer, or rerun the
reflection, frame, quadratic-rank or ambient-slice checks.

Ordered eligible list for session r63, rebuilt on 2026-10-30 against
`2485805a6d47f36ea83ddde6327d453ac82d44dc`. Open handoffs from the 19 October
index (discussion comments 19030045, 19030047, 19030049 and 19030053) come
first and are dropped: the `(w, q, v_N)` consumer, the fresh T385 wrapper,
the L546 six-tape bill and the single-ADD retiming class are already
delivered by this account or closed on main. No newer finite handoff index
replaced that list. The priority table is the revision-8 "Next bounded
decisions" table. A row stays while that table still states the decision.
Catalogue cards not named by the table follow. Dropped before the cut: work
this account already delivered, results closed on current main, questions
covered by an open pull request, and topics already on a fork `cursor/*`
branch.

1. Complex helpers (`p104-side-correction`, `coverage-law-change`).
2. BIT (`bit-helper-contract`).
3. New decoders and interfaces.
4. Supplier audit (`supplier-boundary-audit`).
5. All-size audit (`uniform-transfer-audit`).
6. **This package.** Verification tooling (`replay-runtime`): the #5729
   coverage comparison.
7. `bit-new-register-model`.
8. `r437-carrier-integration`.
9. `complex-rank-shape-decoder`.
10. `complex-new-helper-inventory`.

Rows 1 through 5 stay because the priority text still states those
decisions. Later packages from this account refine pieces inside the rows
and do not delete them. The six rows already name
`p104-side-correction`, `coverage-law-change`, `bit-helper-contract`,
`supplier-boundary-audit`, `uniform-transfer-audit` and `replay-runtime`.
Items 7 through 10 are the next catalogue cards in file order after those
six names. `portable-replay` is not one of those six names; it is later in
the catalogue than item 10.

## Reproduce

Python 3.12 and the standard library, from the repository root. The half-split
scans `2^27` words twice and finishes in well under a minute here.

```sh
python3 -B scripts/research_package.py --package research/e7-bitslice-coverage-check --check-only
python3 -I -B research/e7-bitslice-coverage-check/verify.py
python3 -B scripts/research_package.py --package research/e7-bitslice-coverage-check
```

The direct verifier prints

```text
PASS_E7_BITSLICE_COVERAGE_CHECK minimum=12 supports=1638 codewords=134217728 batches=16,8 splits=13,16 orbits_replayed=false no_new_kappa=true
```

Not run: the #5729 timing harness, reflection orbits, quadratic ranks, the
120 ambient slices, Lean, Docker, and `make frontier6030-verify`.

## Open next questions

1. Do the two predecessor orbit hashes still partition this support set?
   The iterator check does not rerun the 63 reflection maps, so a matching
   word set is not a new classification proof. First apply the frozen
   permutations in `source/verify.py` to this set and compare both hashes
   with `source/RESULT.json`.
2. Does the same equality hold for one other deletion or decoder code?
   The bit-lane proof leaves that consumer unbound. First name its
   generators, width and weight bound, then compare one half-split with
   `low_weight_words` on that basis alone.

## Credit

The geometry, frame code and minimum-weight statement are Nick Petalas's
PR #5238, retained in `research/e7-bitsliced-exhaustion/source/vendor/PR5238.py`.
The equality classification and receipt are Ali Romman's PR #5669. The
bit-lane engine and its small-code oracle are Ali Romman's PR #5729,
`research/e7-bitsliced-exhaustion`. This package does not modify those files.

Prepared by unpaidmoon with substantial Cursor Grok assistance. Apache-2.0.
No independent human review and no formal-kernel acceptance are claimed.
