# Bit length 2642 is a loose log_q shape coefficient

**Card `selected-stock-envelope`, method 2, scope refined.** No new κ.
Selected κ stays `0.001672660197076918`.

`research/selected-stock-shape-a-zero` proves `log2(C) <= 2642` for the
selected m=73 finite stock and then substitutes that bit length into the
log_q composition from `research/selected-coarse-depth-stock/PROOF.md`. On
every integer base `q > 2^80`, the same integer `C` satisfies

```text
log_q C < 34.
```

The prime `q = 2^80 + 13` has `C > q^33`, so `33` is not a uniform
coefficient on that domain. The ratio of the two C-part plugs, before the
unbound leaf constant `rho`, is exactly `2642/34 = 1321/17`.

```sh
python3.12 -B scripts/research_package.py --package research/logq-stock-shape-gap
```

Expected first lines include `PASS_LOGQ_STOCK_SHAPE_GAP` and
`PASS_LOGQ_STOCK_SHAPE_INDEPENDENT`. Direct checks:

```sh
python3.12 -I -B research/logq-stock-shape-gap/verify.py
python3.12 -I -B research/logq-stock-shape-gap/independent.py
```

## Result

| Object | Value |
|---|---|
| Stock | `\|Sp(72,2)\| * 14826` |
| Bit length | `2642`, and `2^2641 <= C < 2^2642` |
| Sufficient log_q coefficient for every integer `q > 2^80` | `34` |
| Failure | `B = 33` at the prime `2^80 + 13` |
| Shape-note plug-in | `2642`, still a valid upper bound, not necessary |
| Leaf constant | unbound |

The proof is in [PROOF.md](PROOF.md). Primality of `2^80 + 13` is a
Pocklington certificate whose small factors are trial-proved. The exponent
comparisons are integer powers.

## Limits

This does not bind `rho`, name a stage width `w = ceil(e^s)`, or close the
envelope `sigma`. Shrinking only the `B` term does not by itself shrink
`sigma` once `rho` is present. No cutoff headroom is recomputed. No supplier,
caller or selected frontier changes. The ordinary BIT reserves `8194`,
`6748` and `6741` are not this complex finite stock.

## Open next questions

1. Bind `rho` for this same finite stock, or prove it is zero under a
   completed-leaf interface. Until then the `1321/17` gap is only the C-part.
2. Repeat the coefficient at one selected stage with the actual atom width
   `w = ceil(e^s)`, which can only make a `w`-free bound looser.

## Credit

The symplectic formula, the family split `14826` and the bit length `2642`
are from `research/selected-stock-envelope-m73`. The log_q slot
`log_q C(w) <= A*w + B` is from `research/selected-coarse-depth-stock`. The
substitution of `2642` is the composition sentence in
`research/selected-stock-shape-a-zero`. Those packages retain their own
predecessor credit, including the coarse-depth and m=73 authors. The
base-change certificate and the prime `2^80 + 13` are new.

Prepared by unpaidmoon with substantial Cursor Grok assistance. Apache-2.0.
No independent human or formal-kernel review is claimed.
