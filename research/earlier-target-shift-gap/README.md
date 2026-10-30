# Earlier-target frame506 shifts remain the reversed-field oracle

**Scoped classification and conjugation. No new κ.** The selected conditional
exponent stays `781451/250000000`.

The helper-462 / frame-506 route has `224 f²` ordered shifts. Signed-dyadic
scaling and the fixed-tape affine kernels price the later-target part and
leave `64 f²` earlier-target sites unpriced. Those sites update the smaller
address. The proved forward shear updates the later high axis only.

On Jose Manuel's stream layout, the earlier-target operation is
`add_high(..., reversed_fields=True)`. It is the forward shear conjugated by
a swap of the two high axes, and each call records two
`completed_swap_oracle` entries. The forward call records none. The oracle
body is charged as `T_old`, not as a fixed-tape transition count.

[PROOF.md](PROOF.md) gives the address formula and the conjugation. The
checker recomputes both route directions from the stored matcher and compares
them with the committed `f = 1` program.

## Scope and evidence

Task card: `supplier-boundary-audit`, refined to handoff
[#1166 comment 19137812](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19137812)
after the route schedule, unit-scale class, and later-target kernels already
on this base. The scope change is in [TASK.json](TASK.json).

Base commit `2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority revision 8.
Live inputs are the committed route program and `qadic_streams.py`. Pins are
in [SOURCES.json](SOURCES.json).

Not run: a fixed-tape transposition, a full helper-462 owner replay, P3 stock
or precision admission, Lean, Docker, or the selected cold replay. The two
oracle records are not given a numeric transition bill here.

## Reproduce

Python 3.12 and the standard library, from the repository root:

```sh
python3 -B scripts/research_package.py --package research/earlier-target-shift-gap --check-only
python3.12 -B scripts/research_package.py --package research/earlier-target-shift-gap
```

Expected token: `PASS_EARLIER_TARGET_SHIFT_GAP earlier=64*f^2 later=160*f^2 oracle_calls=2`.

## Open next questions

1. Give one fixed-tape axis transposition the same all-extent transition and
   visited-cell contract as the forward shear. That is the missing half of
   `E = τ L τ`. Start from `completed_swap_oracle`'s rectangular layout and
   charge padding, exchange, unpadding, and cleanup. The blocker is that the
   current oracle body is random access charged only as `T_old`.
2. Install that bill on the `64 f²` helper-462 sites together with low-cache
   lifetime and ROW padding. A kernel identity does not admit the route.
   The blocker is the same owner-bank and P3 contract left by the route
   generator.

## Credit

The route schedule and address expansion are Chris R / Clear1nsight's
PR #4957 / #4989. The stream lemma and the completed-swap oracle are Jose
Manuel's. JoyboyBrian's signed-dyadic scaling, ordered shear, and in-place
affine shear identified the earlier-target remainder and priced the other
classes. ai-nanachi's ordinary API handoff is the request being narrowed.
Prepared by unpaidmoon with substantial Cursor Grok assistance. Apache-2.0.
No independent human or proof-kernel review is claimed.
