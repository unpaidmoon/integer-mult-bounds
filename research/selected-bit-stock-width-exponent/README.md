# Selected BIT stock width exponent

**Partial coefficient binding. No new κ.** The selected conditional result
stays `60403/20000000`. This package does not fill the historical m=73
envelope coefficient.

## Result

At the selected joint-helper producer, the rechecked ordinary BIT interface
has atom

```text
s = 1/250.
```

With cover saving `C1 = 69/20000` and retained leaf saving
`a_old = 384599/10000000000`, the ordinary saving is

```text
R = (1-s) C1 + s a_old = 8590884599/2500000000000.
```

The two stock tests at this interface are the adapter inequality `s > R` and
the absorption inequality `s < 1-R`. Both hold, with exact slacks

```text
s - R     = 1409115401/2500000000000,
1 - R - s = 2481409115401/2500000000000.
```

The source width rule is `w = ceil(e^s)` with this same `s`. For any fixed
compiled `N`, `B` and `P`, borrowed digits remain `O(w log e)`, and the
positive absorption slack is the exact room in which that `o(e)` bound sits.
The admitted BIT saving `17/5000` stays strictly below `R`.

The selected outer parameters use `d = 1/1400000000` and
`beta = 1 - 3d = 1399999997/1400000000`. The receipt's two stock guards are

```text
actual_new_BIT_stock_sublinear
    = beta (1 - 1/250)
    = 348599999253/350000000000,

new_BIT_row_stock_sublinear_in_active_group
    = beta (1 - 3/1000)
    = 1395799997009/1400000000000.
```

The second value is the guard formula retained from the PR4359 endpoint
ledger. Its exponent `3/1000` has adapter slack

```text
3/1000 - R = -1090884599/2500000000000 < 0.
```

So `3/1000` fails the adapter test that the selected atom passes. The
inherited guard is still positive, and it is strictly larger than
`beta (1 - 1/250)`. Positivity of that guard is the looser comparison.

## What this does not establish

The depth base in `D_N(n) = floor(log_N n)` is not instantiated. The BIT
compiler height `H0 = 3755884544` and the uniform rank `2^64215200000000`
remain different integers in the receipts. The m=73 composition
`(43/26)(1-s)(A+B) + rho` is a different coefficient and stays unset. Passing
either outer guard does not by itself absorb the selected p16 nonrecursive
record bound. There is no new κ and no supplier admission beyond the
selected conditional hypotheses.

## Scope

Original card: `selected-stock-envelope`. Scope status: **refined**. The
2026-10-22 selection refresh makes the #4470 joint-helper construction the
selected producer. This binds that producer's BIT width exponent. The reason
is in [TASK.json](TASK.json).

## Reproduce

From the repository root, with Python 3.12:

```sh
python3 -B research/selected-bit-stock-width-exponent/verify.py
python3 -B research/selected-bit-stock-width-exponent/test_verify.py
python3 -B scripts/research_package.py --package research/selected-bit-stock-width-exponent
```

Expected marker:

```text
PASS_SELECTED_BIT_STOCK_WIDTH exponent=1/250 ordinary=8590884599/2500000000000 adapter=1409115401/2500000000000 slack=2481409115401/2500000000000 rejected_atom=3/1000 inherited_guard=1395799997009/1400000000000 selected_guard=348599999253/350000000000 no_new_kappa
```

## Open next questions

1. **Which field dimension is `N` in `D_N(n) = floor(log_N n)` for this
   template?** The width exponent is bound here; the depth base is the other
   factor in the borrowed-digit count. First step: separate the delayed-cover
   `GL_N` dimension from `H0 = 3755884544` and from
   `2^64215200000000`. Blocked by: the pinned receipts keep those integers
   as different objects.
2. **Does the selected p16 record bound move `s = 1/250`?** A fixed stock
   coefficient that grows with the joint-helper invoice could consume
   `1 - R - s`. First step: substitute raw upper `181098496`, `v = 1024` and
   the selected productive and paid counts into the query-thinned section-5
   overestimate. Blocked by: that overestimate is stated for the query-thinned
   unit, and the joint-helper proof only records that the fixed lists are finite.

## Credit

The ordinary BIT interface and the sentence `w = ceil(e^0.004)` are the
query-thinned controller proof, prepared for Cinna Davis. The selected
receipt, the parameter family `beta = 1-3d`, and the assignment of
`actual_new_BIT_stock_sublinear` are the joint-helper lattice package. The
formula `beta*(1-3/1000)` is the PR4359 endpoint ledger. The historical m=73
shape and log_q notes are separate predecessors and are not reused as this
coefficient. Selected κ `60403/20000000` is the maintainer record for #4470.

Prepared by unpaidmoon with substantial Cursor Grok assistance. No
independent human review is claimed. Apache-2.0.
