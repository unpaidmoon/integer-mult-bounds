# Four-lift direction audit

Independent scalar check of the archived four helper-input lifts. No new kappa.

## Scope and evidence

Discussion #1166 comment 19341394 asks for an independent review of
[PR #6349](https://github.com/CrocSwap/integer-mult-bounds/pull/6349), head
`af7cb6c67f8fc7d82a2e4aee2dd2f07481bf6690`, archived on main as
`research/p104-native-input-lifting`. The requested checks are the four delayed
input directions, their inverse output bases, the two dirty-carrier
subtractions, and the native target debit.

This package answers those four checks and stops. It does not import that
package's verifier, constructor, or price program. Card
`supplier-boundary-audit`, scope status **refined**: one scalar boundary of
this candidate, not native, caller, ordinary, or outer admission.

On the pinned words, with a separate linear replay:

- Each claimed input direction `h` has departure response `a` on the source word.
  The four supports of `h` are disjoint and each primary coefficient is 1.
- Frame 1093 is the GF(2) intersection of frames 118 and 733 and has dimension 3.
  The other three entry frames have dimension 1, and each entry span sits inside
  every corresponding source departure frame.
- The last six events are the output additions `B^{-1} = I - (h - e_p) e_p^T`.
- Each dirty-carrier block leaves `v - x` and `z - x/2` for arbitrary carrier
  values `v, z` and lifted input `x`. Dropping the opening subtraction leaves a
  residual `2z`. The output basis restores `v` and `z`.
- All 799 register forms in the 770 public inputs agree between the source word
  and the lifted word. Deleting either carrier subtraction, or changing one
  inverse coefficient, makes them disagree.
- Both schedules are frame-legal. Every public register ends on its declared
  frame, and every owned lifetime is opened by `INIT` and closed by `CLEAR`.
- The only initial-frame changes are roles 496, 649, 663, and 508. Their
  productive ranks move from four 9's to three 8's and one 6. The target debit
  is `{6: 1, 8: 3, 9: -4}`.

The selected conditional exponent stays `781451/250000000`. This package does
not re-derive the author claim `3129111/1000000000`.

On this machine the author's registered verifier was also rerun, separately
from the checker above, at the archived sources:

```sh
python3 -W error -B research/p104-native-input-lifting/verify.py
python3 -O -W error -B research/p104-native-input-lifting/verify.py
```

Both printed `PASS_P104_NATIVE_INPUT_LIFTING_KAPPA_003129111` on CPython 3.12.3.
That repeats Ali Romman's checker, including its native, caller, price,
compiler, and outer stages. It is not an independent implementation of those
stages.

## Reproduce

Python 3.12, standard library only, from the repository root:

```sh
python3 -B research/p104-input-lift-direction-audit/verify.py
python3 -O -B research/p104-input-lift-direction-audit/verify.py
python3 scripts/research_package.py --package research/p104-input-lift-direction-audit --check-only
python3 scripts/research_package.py --package research/p104-input-lift-direction-audit
```

The verifier prints `PASS_P104_INPUT_LIFT_DIRECTION_AUDIT`. It reads the two
pinned words and writes nothing.

## Open next questions

Do the 2,930 native chart maps, including absolute phase, agree with this
scalar endpoint under an independent lowering? The author verifier reports
that it checked them, and that command passed here, but this package does not
reimplement it. `native_all_columns` stays open. The first step is an
independent Clifford replay of one changed helper normalizer.

Does the paid change `H1+H2+H3+2H4-4H5`, with the target debit checked here,
stay positive for the full caller at `3129111/1000000000`? The handoff's kappa
is that invoice. The first step is to recompute the local paid histogram and
evaluate the unchanged p16/a7 caller. Blocked because `pricing.py` and the
caller were not run.

## Credit

The lifted word and its proof are Ali Romman, PR #6349, with substantial
OpenAI Codex assistance. The source word is DreamingOfClouds, PR #6314, with
Claude Opus 5.5 assistance, retaining Ali Romman's PR #6167. Apache-2.0.

Prepared by unpaidmoon with substantial Cursor Grok assistance. The assistant
wrote this checker. The PR #6349 author checks are not reused as evidence.
