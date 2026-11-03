# Independent rational reduction of the PR6167 outer ledger

This is an arithmetic audit of the fixed parameter choice in
`research/p104-retained-operand-descent/pricing.py`. It addresses the outer
ledger part of the open question in Matarener's PR6214 audit. The definitions
are read from the pinned
`research/pr4359-p7-padding/dependencies/compiler-refill/endpoint.py`,
especially `ledger`, and from the actual PR6167 call to that function.
The derivation below does not import or execute either producer.
`SOURCES.json` identifies the exact source bytes and comparison receipt.

The result is equality and strict positivity of nine savings, 54 named
strict expressions and four functional expressions at this single rational
choice. It does not establish the source theorems whose hypotheses those
expressions are intended to support, or the separate compiler threshold.

## Parameters and the maximum branch

All decimals below denote exact rationals. Define

```text
k = 625729/200000000,
tested = 62573/20000000,
g = (tested-k)/7 = 1/1400000000,
q = k+3g,   a = k+4g,   b = k+5g,   uniform = k+6g,
epsilon = 1-g,   beta = 1-3g,
r0 = g/10,   stop = layout = d = g,
B = 17/5000,
old = 0.001730970419199163702738,
m = epsilon*q = (1-g)(k+3g).
```

Here B is `bit_saving`, uniform is `complex_uniform_saving`, d is the
source's returned gap field, and k is `kappa`. These are the thirteen
supplied parameter fields; the evaluator additionally returns `cap_xi`,
`lambda_` and `lambda_prime`, derived below. The actual BIT atom is a
separate input, rho=1/250, not B.

The source defines sigma=1-b and tau=1-a. Therefore sigma-tau=a-b=-g<0.
Its expression

```text
internal = tau+(1-stop)*max(sigma-tau,0)
```

takes the zero branch of the maximum, giving internal=tau. This branch
choice is proved from the declared parameters rather than assumed from a
receipt value. The remaining substitutions give

```text
leaf = sigma+stop*(1-sigma) = 1-(1-g)b,
lambda = 1-(q+a)/2 = 1-k-7g/2,
lambda_prime = 1-q = 1-k-3g,
c = 3/32,
xi = epsilon*(1+q)-c+layout = 29/32+m,
key = beta+1-epsilon = 1-2g.
```

In particular the layout term +g cancels the -g in epsilon when reducing
xi. Dropping that term or taking the other internal-max branch changes
the ledger being audited.

The inherited helper `family()` is not the parameter source for this
candidate: it contains historical BIT saving 0.0027. PR6167 explicitly
supplies B=17/5000. Likewise `improvement_over_user_baseline` is the
inherited row name for subtraction of the exact constant old above; it
does not refer to whatever selected record is current today.

## Nine savings and their nine named strict checks

The receipt group named `margins` contains savings, not savings minus k.
Substitution in each source formula yields the second column. The third
column is the separate strict check whose full name is printed there.

| Saving row | Saving | Named strict check and value |
|---|---|---|
| `main_transform` | m | `main_transform_above_kappa` = g(3-k-3g) |
| `global_coordinate_router` | k+4g | `global_coordinate_router_above_kappa` = 4g |
| `fused_gaussian` | g+(k+3g)(1-3g) | `fused_gaussian_above_kappa` = g(4-3k-9g) |
| `group_bit_router` | g+(k+4g)(1-3g) | `group_bit_router_above_kappa` = g(5-3k-12g) |
| `group_scans` | 1-2g | `group_scans_above_kappa` = 1-k-2g |
| `boundary_algebraic_matrix` | m+g | `boundary_algebraic_matrix_above_kappa` = g(4-k-3g) |
| `sparse_union_movement` | m+g+13/32 | `sparse_union_movement_above_kappa` = 13/32+g(4-k-3g) |
| `polynomial_products` | 1-g | `polynomial_products_above_kappa` = 1-k-g |
| `microbox_face_corrections` | 77+4g | `microbox_face_corrections_above_kappa` = 77-k+4g |

For example, the boundary row c+xi-epsilon becomes m+g, and the sparse
row xi+1/2-epsilon becomes m+g+13/32. The large microbox value follows
literally from 1-(epsilon+beta+48-128+2)=77+4g; it is not normalized or
silently capped at one. Each named strict expression is its own saving
minus k, precisely as in the source's nine-row extension of `checks`.

## The other 45 named strict expressions

The following table retains every non-row name in the source ledger.
Equal values do not identify predicates: for example, several distinct
interface requirements reduce to g and remain separate entries.

| Source check | Reduced exact expression |
|---|---|
| `actual_bit_above_effective` | B-k-4g |
| `complex_above_effective` | g |
| `q_positive` | k+3g |
| `complex_endpoint` | 2g |
| `q_below_effective` | g |
| `stop_positive` | g |
| `stop_below_one` | 1-g |
| `leaf_saving_above_effective` | g(1-k-5g) |
| `q_below_internal` | g |
| `q_below_leaf` | g(2-k-5g) |
| `lambda_above_tau` | g/2 |
| `lambda_above_sigma` | 3g/2 |
| `lambda_above_internal` | g/2 |
| `lambda_prime_above_lambda` | g/2 |
| `lambda_prime_above_leaf` | g(2-k-5g) |
| `epsilon_positive` | 1-g |
| `epsilon_below_one` | g |
| `cap_above_band` | 13/32+m |
| `cap_below_cell` | 3/32-g-m |
| `group_positive` | 1-3g |
| `group_below_dimension` | 2g |
| `support_router_span` | 3g |
| `group_gauge_power_slack` | 3/16-2m+29g/10 |
| `actual_logarithmic_group_guard` | 3/16-2m+3g |
| `global_gamma_power_slack` | 9g/10 |
| `actual_logarithmic_gamma_guard` | g |
| `alpha_logarithm_absorption` | g/10 |
| `group_key_fits_record` | 2g |
| `membership_arithmetic_fits_record` | g |
| `microbox_halo_volume` | 79+3g |
| `positive_layout_slack` | g |
| `short_record_fallback` | 1-k-5g |
| `complex_below_one_over_32` | 1/32-k-5g |
| `strassen_integer_power_gap` | 2^45-7^16 |
| `theta_positive_polynomial_power` | 2 |
| `cap_below_phase_cell_power` | 35/32-m |
| `halo_covers_generic_inverse_radius` | 5 |
| `union_tag_work_per_visit_fits_record` | 3g |
| `union_header_fits_record` | 3g |
| `source_axis_superpolynomial` | g |
| `gaussian_above_main` | g(1-2q) |
| `new_complex_uniform_saving_above_b` | g |
| `improvement_over_user_baseline` | k-old |
| `new_semantic_guard_with_C1_one` | g |
| `fine_prime_halo_umbrella` | 7/2 |

Some useful derivation checks are

```text
(1-stop)b-a = (1-g)(k+5g)-(k+4g) = g(1-k-5g),
1-leaf-q = (1-g)(k+5g)-(k+3g) = g(2-k-5g),
1-(2xi-2)-r0-beta = 3/16-2m+29g/10,
1-beta-2(1-epsilon) = g,
(1-epsilon+q*beta)-epsilon*q = g(1-2q).
```

Thus the 45 names in this table and the nine distinct `_above_kappa`
names in the preceding table form exactly the source's 54-name inventory.
Equality of inventories is part of the arithmetic claim, not just a check
that some collection has length54 or positive values.

## Positivity and the exact minima

Direct comparison of the declared rationals gives

```text
0 < g < 1/100000000,
3/1000 < k < q < a < b < uniform < tested < 1/250,
0 < m < q,
0 < old < 2/1000.
```

These inequalities establish positivity of every factor of g in the
tables. In particular 1-b>249/250, 2-b>499/250, and 1-2q>124/125.
The potentially subtractive constant-scale expressions satisfy

```text
3/32-g-m > 3/32-1/100000000-1/250 > 0,
3/16-2m > 3/16-1/125 > 0,
1/32-b > 1/32-1/250 > 0.
```

The two source-specific differences and the integer-power comparison are

```text
B-a = 379893/1400000000 > 0,
k-old = 0.001397674580800836297262 > 0,
2^45-7^16 = 1951441519231 > 0.
```

Every strict expression other than `alpha_logarithm_absorption` exceeds
g/10: the other pure-g coefficients are at least1/2; the factors just
bounded are greater than1/10; the remaining positive constant-scale
expressions are larger than g. The nine saving-minus-k values also exceed
g/10, since their smallest value, derived next, exceeds2g. Consequently
the unique minimum over the 54 named strict checks is exactly

```text
alpha_logarithm_absorption = g/10 = 1/14000000000.
```

The limiting saving is also determined algebraically. The coordinate row
exceeds m by g(1+q); the fused row exceeds m by g(1-2q)>0; the group-bit
row exceeds the fused row by g*beta>0. Boundary and sparse rows exceed m
by g and g+13/32. The polynomial row has difference epsilon*(1-q)>0;
the scan and microbox rows exceed m by the elementary bounds above.
Therefore `main_transform` is the unique smallest saving. Its exact value
and slack are

```text
min(savings) = m = 3066074197809947/980000000000000000,
m-k = g(3-q) = 2097809947/980000000000000000 > 2g > 0.
```

Subtracting the same k preserves ordering, so this is also the unique
minimum among the nine `_above_kappa` rows. It is distinct from the
minimum g/10 over all 54 strict predicates.

## Four functional expressions and the two BIT atoms

The inherited evaluator defines the first three rows below. PR6167's
pricing code appends the fourth using the actual `ordinary_BIT.atom`
from `research/query-thinned-controllers/RESULT.json`.

| Functional name | Exact expression |
|---|---|
| `new_semantic_group_guard` | 3g |
| `new_BIT_row_stock_sublinear_in_active_group` | beta*(997/1000) |
| `fixed_halo_explicit_metadata_branch` | 77+4g |
| `actual_new_BIT_stock_sublinear` | beta*(249/250) |

The historical atom in the inherited second row is rho_legacy=3/1000;
the actual atom is rho=1/250. They are both distinct from the admitted
saving B=17/5000. In particular, neither replacing rho by B nor copying
the historical second row into the actual fourth row reproduces the
source. These two stock entries are exponents beta*(1-rho), not the gaps
rho*beta and not one minus the recorded exponent.

Writing s_actual=beta*(249/250) and s_legacy=beta*(997/1000), exact
evaluation gives

```text
beta = 1399999997/1400000000,
s_actual = 348599999253/350000000000,
beta-s_actual = beta/250 = 1399999997/350000000000,
s_legacy = 1395799997009/1400000000000,
beta-s_legacy = 3*beta/1000 = 4199999991/1400000000000.
```

Since 0<beta<1 and 0<3/1000<1/250<1,

```text
0 < s_actual < s_legacy < beta < 1.
```

This records both positivity and the strict sublinear relation to the
active-group exponent beta; positivity alone would not establish that
relation. The four functional entries are positive, and their unique
minimum is `new_semantic_group_guard`=3g=3/1400000000: both stock exponents
are greater than9/10 and the metadata expression is greater than77.
These inequalities are numerical statements about the recorded exponents,
not a fresh proof that a concrete supplier meets the functional interfaces.

## Verification boundary and attribution

The companion checker reconstructs the closed forms independently with
exact fractions and compares the complete parameter and named-output
inventories against the pinned PR6167 receipt. A savings field must contain
the saving, not k or its slack. Repeated JSON names, missing rows, changed
parameters, wrong maximum branches and wrong BIT atoms are distinct ways
to fail that comparison even when some resulting values remain positive.
Byte identity, exact receipt reproduction and positivity are different
claims and should remain distinguishable in the verification record.

This audit does not recompute the mixed-moment funding proof, finite
compiler threshold, native word, caller, cover, fixed-tape realization,
precision or analytic recovery. It does not discharge the source's five
framework assumptions, prove a uniform/all-size multiplication theorem,
admit a supplier, or change the selected frontier. PR6214's broader work
and the source's own checks retain their original scope. A next independent
task is the separate compiler-threshold argument and its exact inputs;
the present rational ledger does not cover it.

Credit Ali Romman's [PR6167](https://github.com/CrocSwap/integer-mult-bounds/pull/6167)
candidate and PR5827 lineage; Matarener's
[PR6214](https://github.com/CrocSwap/integer-mult-bounds/pull/6214) independent
audit and explicit remaining-outer-arithmetic handoff; zxv's
[PR4359](https://github.com/CrocSwap/integer-mult-bounds/pull/4359) endpoint
lineage; the interval/compiler work of zxv and Cao Yifan, Jacob Alan
Sussman's productive recursion, and Cinna Davis's controller. The retained
outer-parameter source credits Vlado Vojdanovski's PR1673, Chafik Boukhalfa's
PR1758/1786, and the radix-union, Strassen, fine-prime and transfer-audit
contributors. The query-thinned BIT receipt and all upstream source notices
remain credited inputs; their supplier proofs are not recreated here.
Prepared with substantial OpenAI Codex assistance. Apache-2.0.
