# Persistence of one section-6 threshold comparison

**Proof, with an exact integer census. Selected κ stays `363005817/100000000000`.**

For every integer `C ≥ 1`, every integer `d0 ≥ 0` and every positive rational
`δ = a/b`, the comparison `C (j+1)^{d0} ≤ 2^{δ j}` has an explicit witness
`j*`, and it stays true for every larger integer. The same persistence holds
for any success with `j > 4 d0/δ`. The argument is [PROOF.md](PROOF.md).

## Scope and evidence

Original card: `uniform-transfer-audit`. Scope status: **refined**. The card
asks whether one of the five selected assumptions can be proved at its actual
caller, and its first experiment says to stop at one quantified implication.
This package takes assumption `precision_tape` and the threshold comparison
in section 6 of the #7000 application review. It does not prove the
assumption. The caller is that review sentence, not a native word.

This is session r285, item 8 of the ordered eligible list read on
2026-11-11. Open handoffs whose later post completes them, whose canonical
artifact is an open pull request, or which say that no target was taken, are
dropped, as are the delivered 19 October index, the H25 chain, and the 2
November review artifacts. Updated notes are one request. Three open
handoffs remain, then the revision-8 next-decision rows, then unnamed
catalogue cards:

1. Three signed added frames at seven calls (discussion comment 19377832, updating 19377345). PR #6942 closes only the all-old-once profile.
2. Eight-source singleton existence (comment 19537798, updating 19377982). The bound `28 ≤ f(8) ≤ 32` is unchanged.
3. Six-source depth-two block at `c = 7` (comment 19537594, updating 19384981).
4. Complex helpers (`p104-side-correction`, `coverage-law-change`).
5. BIT (`bit-helper-contract`).
6. New decoders and interfaces.
7. Supplier audit (`supplier-boundary-audit`).
8. **This package.** All-size audit (`uniform-transfer-audit`): the threshold comparison.
9. Verification tooling (`replay-runtime`).
10. `bit-new-register-model`.

Open PR #7286 is the same all-size row under a list that omitted the three
handoffs, so its item number there was 5. It proves the sharp monomial
record count. This package does not use that count and does not evaluate a
selected cutoff. Later conditional-κ requests on #1166 ask maintainers to
select a new exponent. Their canonical artifacts are open pull requests, so
they are outside this list.

Evidence classes:

1. **Proof.** The theorem in [PROOF.md](PROOF.md), for every integer
   `C ≥ 1`, every integer `d0 ≥ 0` and every positive integers `a, b`.
2. **Exact integer census**, only on the rectangles named in `verify.py`.
   The census checks the proof's integer inequalities, the one-step
   comparison, the review factor, and the single sharpness triple
   `(d0, a, b) = (1, 2, 5)`. It is not a substitute for the theorem.

Pins are in [SOURCES.json](SOURCES.json). Base commit
`e54523517d0f03e58352e647c403a5af3e525a57`, priority revision 8.

## Reproduce

Python 3.12 and the standard library, from the repository root:

```sh
python3 -B research/threshold-ratio-persistence/verify.py
python3 -O -B research/threshold-ratio-persistence/verify.py
python3 -I -B research/threshold-ratio-persistence/verify.py
python3 -B scripts/research_package.py --package research/threshold-ratio-persistence --check-only
python3 -B scripts/research_package.py --package research/threshold-ratio-persistence
```

Expected direct marker:

```text
PASS_THRESHOLD_RATIO_PERSISTENCE proof_rows=2100 direct_rows=592 ratio_rows=960 sharpness=1,2,5,4 kappa=363005817/100000000000 no_new_kappa=true
```

The registered replay is
`python3 -B scripts/research_package.py --package research/threshold-ratio-persistence`.
`python3 -B
scripts/research_selected_baseline.py` returned
`PASS_RESEARCH_BASELINE_BINDINGS_ONLY` and is not a scientific replay.
`make frontier7000-verify`, Lean and Docker were not run.

## Open next questions

1. For the finite list of `(C, d0, δ)` pairs that section 6 actually feeds
   into the outer cutoff, what is the least `j`? The existence proof does
   not name that cutoff. The first step is to read the outer-predicate table
   and evaluate the integer comparison. Section 6 does not isolate one pair,
   and open PR #7286 already asks whether its record count lowers one
   cutoff. This package does not answer that.
2. Can an elementary proof replace `8/5` by a smaller rational constant?
   The present constant is `2^8 > 3^5` together with `(1+1/m)^m < 3`. The
   first step is a sharper integer pair and the same binomial bound, tested
   against `(d0, a, b) = (1, 2, 5)`, where one less than the present ceiling
   already fails. Nothing external blocks that rewrite.

## Credit

The comparison and the factor `4` are the #7000 application review, section
6, by the authors credited there. The five assumption ids are the selected
record. The monomial record count is open PR #7286 and is not an input.
Prepared by unpaidmoon with substantial Cursor Grok assistance. No
formal-kernel review and no independent human review are claimed. New work
is Apache-2.0.
