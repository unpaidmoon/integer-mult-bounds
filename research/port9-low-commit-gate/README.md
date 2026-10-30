# Port9 new-low commit and cache-retirement gate

**Partial interface result. No new κ.** The selected conditional exponent stays
`781451/250000000` (`certificates/selected-result.json` at this base). This
package does not admit a supplier or schedule a cache retirement.

The port9 leaf in `research/port9-low-cache-carry` returns a raw 3-bit new-low
on tape 18 and preserves the supplied 64-digit cache on tape 17. Its open
question asks how that new-low is committed and how the cache survives until
its last consumer. The answers at this halt are:

- An eight-transition successor marks the three new-low bits with `RIGHT` and
  returns the head. It changes no other tape. It is a later owner step: the
  marked word fails the leaf's raw-exit contract.
- Blanking cache bits 24 through 191 (digits 8 through 63) also fails that
  contract. The published witness and the same cache with digit 8 changed from
  0 to 4 keep the same owner permutation and the same new-low, and they differ
  only in the preserved tail. The leaf reads every cache bit through the
  endpoint and writes none of them. Generic rotation and descriptor cleanup
  never name tapes 17 or 18.

So this leaf is not a legal last consumer of the cache. [PROOF.md](PROOF.md)
records the walks and the static tape sets. [RESULT.json](RESULT.json) is the
deterministic receipt.

## Scope and evidence

Task `supplier-boundary-audit`, scope **changed**. Structured handoff item 9 on
[#1166](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19137812)
asked for one literal N-dimensional stock/owner/route generator after PR #4957.
Canonical [#4945](https://github.com/CrocSwap/integer-mult-bounds/discussions/4945)
then received the route generator, carry frontend, padding controller, quarter
rotation and the port9 leaf (PR #6241). Those results left this commit and
retirement question open. This package takes that remaining piece. It does not
rebuild the generator, retune a moment, or move the selected frontier.

The predecessor leaf, frontend and rotation bytes are live inputs, not copies.
Base `2485805a6d47f36ea83ddde6327d453ac82d44dc`. Pins are in [SOURCES.json](SOURCES.json).

## Reproduce

From the repository root, CPython 3.12, standard library only:

```sh
python3.12 -B scripts/research_package.py --package research/port9-low-commit-gate --check-only
python3.12 -B scripts/research_package.py --package research/port9-low-commit-gate
```

The registered normal and optimized commands rerun `verify.py` and compare
[RESULT.json](RESULT.json). Each execution checks both leaf orientations, the
digit-8 mutant, the static component tapes, and both successor programs against
the predecessor exit test. Expect `PASS_PORT9_LOW_COMMIT_GATE`.

## Open next questions

1. Hand the marked 3-bit word to one real low-type consumer and charge that
   read. The marker alone is not a consumer, and the raw leaf contract stops
   before it.
2. Name the cache's last consumer, then retire the tail only after that read.
   Digits 8 through 63 are still returned here. The missing whole-T layout and
   ROW installer block any earlier erasure.

## Credit

Prepared by unpaidmoon with substantial Cursor Grok assistance. Apache-2.0.
AAAmirinu supplied the port9 leaf (PR #6241). JoyboyBrian supplied the low-cache
frontend (PR #5332) and the route generator. Ali Romman supplied the
complete-owner rotation (PR #5849). David Arias supplied the tape machine.
Chris R / Clear1nsight supplied the PR #4957 backend-API handoff. No
predecessor bytes or notices are changed.
