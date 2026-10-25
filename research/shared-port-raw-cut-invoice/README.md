# The first raw shared-port cut loses its Gaussian moment

**Negative result. No new κ.** The selected conditional exponent stays
`605457647/200000000000`.

The recording-only theorem for the fused five-bank producer leaves one escape:
the raw state after gate 11, whose grade-3 channel has image dimension `5d`.
This package prices that state as a child that must be exposed, continued and
cleaned. On the predecessor moment, for every exponent `t` in `[0, 1]`,

```text
gap(t) = 2 * 3^t - 8 <= -2.
```

Replacing the two cleanup letters inside `D` by one new grade-2 letter still
gives `2 * 3^t - 2^t - 6 <= -2`.

## Scope and evidence

Original card: `complex-rank-shape-decoder`. Scope status: **refined**. The
card asks for a larger-rank decoder profile. The open request actually taken
is the changed-resource invoice after the fixed-producer completion ceiling
([discussion comment 19133451](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19133451)).
Open PR [#5491](https://github.com/CrocSwap/integer-mult-bounds/pull/5491)
already shows that this raw cut raises the grade-3 image dimension from `4d`
to `5d`, and it leaves the cleanup bill open. This package does not replay
that image proof. It prices the bill.

The exposed owner is `B x0 + D x1`, with `B = M C2 + 2 K a`. No left-linear
image of the live owners can drop `D x1` and keep `2 K a x0`. A fresh `D`
costs two source rank-1 calls, and `M C2` costs one more. Keeping the later
fused banks costs the hybrid profile `5 H1 + 3 H3` before that cleanup. The
proof, the derivative comparison, and the controls are in [PROOF.md](PROOF.md).

The moment does not charge monomials, field additions, the factor `1/2`, or a
field copy of the exposed owner. Charging any of them widens the deficit.
Precision, compiler reserve, outer transfer and feedback into a live owner are
not decided here. They are further nonnegative charges on a gap that is already
negative.

Source pins are in [SOURCES.json](SOURCES.json). The two live inputs are the
predecessor gate list and operator file, used at their bytes on this base.
They are not copied.

## Reproduce

From the repository root, Python 3.12, standard library only:

```sh
python3 -B scripts/research_package.py --package research/shared-port-raw-cut-invoice --check-only
python3 -B scripts/research_package.py --package research/shared-port-raw-cut-invoice
```

Direct checks, each under two seconds here:

```sh
python3 -B research/shared-port-raw-cut-invoice/verify.py
python3 -O -B research/shared-port-raw-cut-invoice/verify.py
```

Both print `PASS_SHARED_PORT_RAW_CUT_INVOICE` with `gap_t1=-2`. The verifier
rejects a missing aligning rank-1 call, an add-sign fault, a wrong pivot
operator, and a grade-2 letter hiding in the source schedule. No native suite,
Lean build, selected cold replay or full compiler/outer replay was run.

## Open next questions

1. Can a feedback write into the live owner, outside the recording-only
   interface, separate `D x1` from `K a x0` with fewer than two extra rank-1
   letters? This matters because that is the only Gaussian saving large enough
   to flip `gap(1)`. The first step is one explicit feedback word and its paid
   profile. The blocker is that every pure source letter is invertible, so a
   left multiply cannot delete `D`.

2. Do the off-diagonal grade-3 terms in the final rows need their own cleanup
   before those four jobs are legal children? This matters because the reward
   used here already credits all four. The first step is to price one
   off-diagonal class on row 3. The blocker is a consumer contract that says
   whether an image-dimension credit is a legal child.

## Credit

The gate list and operators are the PR4813 / block3 schedule retained in
`research/block3-shared-port-composition`, including the hexapode, Dugongue,
Yiyang / Lyy-iiis, lee-phys, Jacob Alan Sussman and Cinna Davis / 1337isnot1337
lineage recorded there. The recording-only `4d` bound and the raw-cut `5d`
witness are Chris R / Clear1nsight and JoyboyBrian's open
[#5491](https://github.com/CrocSwap/integer-mult-bounds/pull/5491). This
package only prices the cleanup those results leave open.

Prepared by unpaidmoon with substantial Cursor Grok assistance. Apache-2.0.
