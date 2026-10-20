# T488 owner-invoice identity

Partial invoice certificate. No new κ. The selected conditional κ stays
`836330098538459/500000000000000000` (`0.001672660197076918`).

## Result

On the vendored PR #3653 numerics inputs at head
`607a09ff441c79b215a8127a81f4cc70021d0d9b`, the published admission histogram
is exactly the literal-owner histogram plus the retiming bill on all 4,392 calls.

Both providers carry the same local bills. The old bill is
`{1:2439, 2:726, 3:224, 4:102, 5:20, 8:8}` and the retimed bill is
`{1:2437, 2:724, 3:226, 4:102, 5:20, 8:8}`. The per-call move is
`-2 H_1 - 2 H_2 + 2 H_3`. Its rank mass is 0, and it removes two children.
Sections `A`, `cut`, `restore`, `warps`, `center_frames`, `helper_final`,
`removed` and `start_extra` are unchanged, as is the width inventory. Sections
`B` and `cleanup` change on both providers.

The four recorded old histograms agree: `OWNER-PROFILE.json`,
`OWNER-EXPECTED.json`, the portable-replay primal profile, and
`OLD-ARITHMETIC.json`. `OWNER-PROFILE.json` has SHA256
`1e37bb17fa4ca6fd84d62c6f540e09be96724ea3af4ea50e3e27c6ecb796b35c`, the digest
named for `PROFILE.json` in the owner expectation. The literal payload digest
`20662cc64df34cab409fdf31ed0f0222462530922a01308a46964d661d2374cf` agrees
between the owner expectation and the portable replay. The rows themselves are
not in this package.

Applying the move to the literal histogram
`{1:10826280, 2:3188592, 3:1015650, 4:447984, 5:94794, 8:35136, 48:186782}`
yields the recorded admission profile
`{1:10817496, 2:3179808, 3:1024434, 4:447984, 5:94794, 8:35136, 48:186782}`.
Rank mass stays `31,762,944 = 65,088 * 488`. The idle part, common to both
bills, is `{1:114192, 3:31842, 5:6954, 48:186782}`.

With `live = 488 * 896 = 437,248`,

```text
73 * live - 31762944 = live - 64 * 4392 = 156160.
```

Role count `1,791,936 = 4,392 * 408`, and the physical family count `437,757`
agrees across the three old receipts. This certificate does not derive `437,757`.

## What this does not establish

The 1,791,936 literal owner rows are not regenerated. Equality of payload
digests is not a replay of those rows. The local bills are the `report.local_profile`
fields of the four canonical words, not a recount of every event. Moment
brackets, the conditional κ of PR #3653, native admission, and the fresh
bootstrap wrapper are not rerun. Rank mass is invariant under this move, so
the histogram change is not, by itself, an exponent claim.

## Reproduction

```sh
python3.12 -B scripts/research_package.py --package research/t488-owner-invoice-identity
```

Direct check:

```sh
python3.12 -I -B research/t488-owner-invoice-identity/verify.py
```

Expected marker: `PASS_T488_OWNER_INVOICE_IDENTITY`.

## Credit

The composition and the recorded admission profile are Rohan Arun's PR #3653.
The retimed words are from roger-sato's PR #3642. The literal-owner expectation
is the PR #3633 package as vendored by #3653 (hexapode). Nick Petalas's PR #3740
reproduced the root arithmetic and left this invoice comparison open. The
identity is recomputed here from the vendored bytes. No predecessor checker is
imported.

Prepared by unpaidmoon with substantial Cursor Grok assistance. No independent
human or formal-kernel review is claimed. New work is Apache-2.0.

## Open next questions

1. Recompute the old histogram from the literal rows, not from
   `OWNER-EXPECTED.json`. Why it matters: this certificate binds the payload
   digest and does not read the rows. First step: materialize `FILL.json.gz`
   at SHA256 `20662cc64df34cab409fdf31ed0f0222462530922a01308a46964d661d2374cf`
   and sum its rank column. Blocker: that payload is not vendored here.
2. Recount `report.local_profile` from the `B` and `cleanup` events under the
   word's child-rank convention. Why it matters: the bill is taken from the
   report field. First step: one rank rule that reproduces `{1:2439, 2:726, 3:224}`
   on the old base word and `{1:2437, 2:724, 3:226}` on the new base word.
   Blocker: the event rank field is not the child histogram.
