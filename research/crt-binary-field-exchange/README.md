# Direct bit swaps do not move the #4174 front field inside the interchange bill

**Scoped obstruction, with an exact in-record schedule. No new κ.** The
selected conditional exponent stays `605457647/200000000000`.

## Result

`research/crt-reservoir-interchange-bill` shows that six ordinary width-`H`
calls meet `O(V H^{1-a2} + V)`, and that the literal call multiplies the
volume by `(q^E/2^H)^2`, between `2^{33}` and `2^{34}` at the minimal
layout. It leaves the direct exchange of `H` single-bit swaps unproved.

Two readings are not the same operation.

* **In-record rewrite.** One fixed pass, with a two-cell buffer, swaps
  stored bits `i < j` in `2j+16` actions and restores both heads. An
  `H`-bit field exchange is `H` such passes, total `H(2β+H+15)` per
  record. Six exchanges cost at most `18 · 2^{1/20} V H^{1-a2}` when
  `V` is a full scan of the address bits, `1 ≤ H < 2^{25}` and `L ≥ 15`.
  The volume factor is 1. Rewriting two-bit labels `[0,1,2,3]` leaves the
  payloads in their slots.
* **Payload transport.** BIT.md moves the record at address `x` to the
  address with the two bits swapped. On a linear tape, with one payload
  crossing one record boundary per action, the #4174 front field
  `[0,H)` forces more than `2^{L-4}` scans. At the minimal layout that is
  more than `2^{1310716}` scans, against an in-record allowance under
  `193536`. The same gap holds at the production layout. No
  layout-uniform constant absorbs it. The transport lower bound is also
  larger than the `2^{33}` padding, so this schedule does not remove that
  factor.

The argument is in [PROOF.md](PROOF.md).

## Task and overlap

Base `32890bc5de034ab8fc93ac88ead7279a6a416d04`, priority revision 7.
Task `uniform-transfer-audit`, scope **refined**.

This is item 11 of the eligible list below. It is the unblocked remainder
of the repair-key bill after `research/crt-transported-key-tape` and
`research/crt-paid-key-service` executed literal keys, and after
`research/crt-reservoir-interchange-bill` priced the six ordinary calls.
`research/crt-mask-repair-bridge` still asks for a Beneš-table evaluator;
that blocker is not this question. The direct single-bit schedule is what
that interchange bill left open, and it is not those executed keys.

Ordered eligible list for session r43. Open handoffs from the 19 October
index come first, with a closed smallest task removed and a distinct
remainder kept. Priority-table rows whose next decision is still open come
next. Inside `uniform-transfer-audit`, still-open successors of the
shortest unaudited list follow the order in
`research/pr4100-ledger-boundary-exponent`, then the CRT reservoir chain.
Dropped before the cut: work this account already delivered, results on
current main, questions covered by an open pull request, and topics already
on a fork `cursor/*` branch.

1. A caller that accepts `(w, q, v_N)` without restoring the original
   source slots (discussion comment 19030045).
2. The cost of placing L561 on the four scratch windows before
   `L546 -= L561` (remainder of comment 19030049).
3. Whether the PR2809 continuation serializer parks the ancestor chain or
   writes one root-sized stream per cut.
4. Whether marker, template and erased-backing cells fit the `26041 V`
   budget.
5. Whether the stored narrow band has at most `2p` off-diagonal entries
   and the rounding meets `2^{-5p}`.
6. Whether a byte-identical `outer/check_ledger.py` regenerates the
   printed `tau_eff` point.
7. Whether the word-level scalar inventory fits constant one at the two
   excluded `p = 2` CRT corners.
8. Whether that full-batch allowance composes with reservoir placement and
   the paid repair-key service.
9. The separator corners of the translated chirp origin.
10. Explicit `C` and `k` for `mu ≤ C (W/B) (log p)^k`.
11. **This package.**

Excluded before this cut: the fresh T385 wrapper, the retiming handoff,
the four-provider rebind, the matched park/restore bill (open #4167 and
#4172), the #4091 ceiling transfer, the compact-switch contract, the
rank-8/u2 entrance obstruction, and the literal one-target tape evaluator
as its own row. The last is blocked on a Beneš evaluator and is already
preceded by executed key tapes; the unblocked bill question that replaced
it is item 11.

## Reproduce

Python 3.12, standard library only, from the repository root:

```sh
python3 -B research/crt-binary-field-exchange/verify.py
python3 -B scripts/research_package.py --package research/crt-binary-field-exchange
```

`verify.py` prints

```text
PASS_CRT_BINARY_FIELD_EXCHANGE swap=2j+16 in_record_C=18*2^(1/20) minimal_L=1310720 minimal_H=10752 production_L=1540096 production_H=15360 transport=GT no_padding=1 no_new_kappa
```

The #4174 allocator is imported from its pinned path and executed on the
first plan of each layout. The big-integer scan bounds are comparisons of
exponents and one subtraction of powers of two. Not run: Lean, Docker, the
selected cold replay, and BIT.md's elementary q-digit algorithm.

## Open next questions

1. Can one adjacent address-bit transposition be charged as a block move,
   with a buffer of `2^k` payloads counted as one action, and still stay
   inside `O(V H^{1-a2})`? The one-payload cut bound does not apply to
   that model. The first step is the transposition of place values `2^{k+1}`
   and `2^k` on a tape that may shift an aligned block in one step. CRT.md
   charges one-cell moves, so this is a different model.
2. What is the stage-0 constant of BIT.md's elementary q-digit swap? It is
   still the whole callee constant on these layouts, and BIT.md does not
   state that algorithm. This package does not reconstruct it.

## Credit

Cinna Davis's #4100 supplies BIT.md and CRT.md. Hiroki KUMAZAKI's #4174
allocator supplies the field geometry. JoyboyBrian's
`research/crt-reservoir-interchange-bill` states the padding and leaves
the direct schedule open; James Reed's interchange-threshold values are
used there and are not recomputed here. The executed key tapes in
`research/crt-transported-key-tape` and `research/crt-paid-key-service`
are a different geometry and are not this bill.

Prepared by unpaidmoon with substantial Cursor Grok assistance.
Apache-2.0. No independent human review and no formal-kernel acceptance
are claimed.
