# Independent integer audit of the PR6167 compiler application

**Result: every numerical hypothesis of the published PR6167 compiler recipe
passes an independent integer/rational check. No new κ.** The earlier PR6030
complement-capacity power 1012 does **not** carry over: for PR6167 the least
integer power satisfying that inequality at θ̄ = 63/64 is **1013**. The published
recipe uses 1024 and remains valid. The sufficient rank is still
`N = 2^65807000000000`, with first passing grid index `j = 47005`.

This is a numerical application audit, not a new compiler theorem or supplier
admission. It answers the compiler-reconstruction part of PR6214's open question,
complementing PR6245's outer-arithmetic check. The selected PR6030 record,
κ = 0.003125804, is unchanged.

## Sources and the new coverage

Base: canonical main `2485805a6d47f36ea83ddde6327d453ac82d44dc`, priority revision 8.
Every live input has its full Git blob and SHA256 in [SOURCES.json](SOURCES.json).
The first three source heads below are ancestors of this base, and the consumed
files were compared byte for byte with their original heads.

| Source | Exact head | Coverage retained / added here |
|---|---|---|
| Ali Romman, [PR6167](https://github.com/CrocSwap/integer-mult-bounds/pull/6167) | `564a076b113621a93edc4e39968ee4e4a8c9caf0` | Construction, complete invoice and compiler recipe are the audited inputs. Their correctness is not regenerated here. |
| Matarener, [PR6214](https://github.com/CrocSwap/integer-mult-bounds/pull/6214) | `ee8b66c91510b1ff4e5d28be8c6567810b4b3d01` | Word/native/caller audit, decimal funding and threshold endpoint tests. This package closes the independently reconstructed numerical compiler conditions, including complement capacity and initial range. |
| JosieElliston, [PR6109](https://github.com/CrocSwap/integer-mult-bounds/pull/6109) | `729842c7a3ea54d5f8a17bfb20dd528fd8d736a5` | Complete numerical compiler binding for the older PR6030 invoice, using directed Decimal intervals. Its theorem map and first-grid argument retain credit; its source-specific headroom is not transferred. |
| AAAmirinu, concurrent [PR6245](https://github.com/CrocSwap/integer-mult-bounds/pull/6245) | `8cb302579050454a05ebd77ac7c981e84a9dcb8e` | All 54 strict and four functional outer checks; explicitly excludes the compiler threshold. Read for overlap and credit, not used as a replay input or assumed merged. |

The [higher-moment theorem](../higher-moment-strictification/README.md), sections
2 and 4, and its [finite-precompilation contract](../higher-moment-strictification/vendor/FINITE-PRECOMPILATION.md)
are pinned verbatim. Their native, allocation and compiler hypotheses remain
assumptions. `pricing.py` is hash-bound as the exact audited recipe but is never
imported, compiled or executed. The independent receipt is compared for its six
invoice totals; that is reuse of its recorded evidence, not a fresh word replay.

## Exact result and theorem binding

Let `T_s = Σ T_r r^s`, `P_s = Σ P_r r^s`, and `B = Σ T_r`.
The input has 13,444 productive fields, 66,762 paid calls, paid rank mass 240,152
and productive rank mass 240,912. The raw largest target rank is `m = 145`.
Take

```
C = 62573/20000000 = 0.003128650,  t = 1-C,
u = 1/7, v = 1024, c = 16, b = 17,
reserve = 10^-12, decay = 125/128, block = 128,
κ = 625729/200000000, d = (C-κ)/7 = 1/1400000000.
```

Here `b` is the completion-floor base, not the outer ledger's similarly named
parameter. After chronological product, paid completion and splitting, the
ambient rank is `M = 145^1024`, maximum paid rank is at most `R = 16^1024`,
and minimum target rank is at least `K = 17^1024`. The estimates use these
conservative bounds even if an actual extreme is smaller.

| Written numerical premise | Independently checked result |
|---|---|
| §2 parameter range | `0 < C < 1`, `u ≥ C`, `t+u ≥ 1`, `1 < c < b < m`, positive integer `v` |
| `α = P_t / T_t < 1-reserve` | `α < 0.999999997959146219726397364395` |
| `γ = P_(t+u)/(c^u T_t) < decay` | `γ < 0.975668301934073053974603857756` |
| `δ = B b/(c^C T_t) < decay` | `δ < 0.950630412060446606438487179897` |
| Complete paid charge after splitting | `α^v + 2γ^v + 2δ^v < 1048576000976562501/1048576001073741824 < 1` |
| §4 exit exponent below `θ̄ = 63/64` | `16^64 < 17^63` |
| Shifted logarithm condition | `2 (16^1024)^64 ≤ (145^1024)^63` |
| Complement capacity | `(63/64)^1024 < η = t M^(t-1)` |
| Initial range | `M^(1-t) < 2^1024` (its value is between `8403417.41150323478` and `8403417.41150323479`) |
| Uniform exponent gap | `uniform = κ+6d = 4380109/1400000000`; for `z = 1-uniform`, `z-t = d > 0` |
| Sufficient threshold | `(1+H)^1024 < 2^47005`, `H = 1400000000 × 47005`; the preceding grid point fails |
| Rank above the base range | `H > 8v` and `145 < 2^8`, so `2^H > M` |

All four new exact enclosures for α, γ, δ and η fit strictly inside or on the
source's printed 30-place rational intervals. Full rational endpoints, positive
slack certificates and control results are in [RESULT.json](RESULT.json).
Neither rounded display decimals nor agreement with a second receipt decides
acceptance: all acceptance comparisons use exact rational endpoints.

For the complete split bound, `(125/128)^128 < 1/16` and `v/128 = 8` bound each
tail by `2^-32`. Bernoulli's inequality gives
`(1-reserve)^v ≤ 1/(1+v reserve)`. Hence the displayed bound includes both the
original paid tail and every permitted per-owner completion tail. Its exact
slack is `97179323/1048576001073741824`. The theorem's completion and physical
implementation contracts are inherited; this inequality does not create them.

### The changed complement-power boundary

The new exact capacity satisfies

```
0.0000001186268991750197874499859942379249
  < η <
0.0000001186268991750197874499859942379250.
```

Exact integer-power comparisons establish

```
(63/64)^1013 < η < (63/64)^1012.
```

Since `0 < 63/64 < 1`, **1013 is the least integer power for this complement
inequality**. PR6109's old 1012 passes for its PR6030 inputs but fails here.
This is a changed numerical premise, not a flaw in either published recipe.
The uniform rank and logarithmic power have not been optimized or replaced.

For the fixed published power 1024 and grid step 1,400,000,000, put
`g(j) = j ln 2 - 1024 ln(1+1400000000 j)`. Then `g(0)=0`, `g'(0)<0`,
`g''(j)>0`, and `g(j)` tends to infinity. Thus it has exactly one positive
zero and its positive integer values form a final ray. The two exact integer
signs at 47004 and 47005 prove first-grid status. This argument and the same
unchanged grid value already occur in PR6109; they are corroborated, not claimed
as a new discovery or a minimum native program.

## Why the new arithmetic enclosures are rigorous

The implementation uses Python integers, `Fraction`, and `isqrt`. It imports
no repository executable and calls no floating-point, Decimal, logarithm or
exponential routine. This deliberately differs from the two author moment
engines and the prior Decimal audit.

For integer `r ≥ 1` and rational nonnegative exponent `e`, split `e = q+f`,
`q` integer and `0 ≤ f < 1`. Truncate the binary expansion of `f` after
`L = 160` places, writing

```
f = Σ_(j=1)^L bit_j 2^-j + h,    0 ≤ h < 2^-L.
```

Use scale `S = 2^256`. If `a/S ≤ x ≤ b/S`, monotonicity and the exact integer
square-root definitions give

```
floor(sqrt(a S))/S ≤ sqrt(x) ≤ ceil(sqrt(b S))/S.
```

Starting with `[rS,rS]`, successive applications therefore enclose every
`r^(2^-j)`. Multiply the factors selected by the exponent bits, rounding each
positive fixed-point product down on the lower side and up on the upper side.
An induction on processed bits proves an enclosure of the truncated power.
The omitted exponent is **not** discarded: convexity of `r^h` on `[0,1]` gives

```
1 ≤ r^h ≤ 1+(r-1)h.
```

Multiplication by this exact tail interval and by the exact integer `r^q`
proves the final enclosure. Negative exponents use reciprocal endpoints in
reverse order. Positive interval sums, products and quotients are rational
operations with no rounding. These arguments prove the enclosing algorithm;
the finite oracle below checks its implementation rather than substituting
for the argument.

Repeated-square-root enclosure is classical and already present in arkfx's
[PR706 package](../pr626-root-moment/README.md) and Ross Richardson's
[mixed-overhead package](../centre-sharing-mixed-overhead/README.md). Those
methods retain credit. No code from them is copied or executed here. The new
contribution is this fixed-source compiler audit and its exact certificate,
not the invention of integer-root arithmetic.

## Reproduce and falsify

CPython 3.12, standard library only, from the repository root:

```sh
python3.12 -B scripts/research_package.py --package research/p104-6167-compiler-audit
```

Expected final line: `PASS_REGISTERED_RESEARCH_PACKAGE` for this package.
The normal and optimized scientific runs each report
`PASS_P104_6167_COMPILER_AUDIT`, 4,100 arithmetic oracle cases, 18 semantic
controls, minimum complement power 1013 and grid index 47005.

The direct scientific command is `python3 -I -B research/p104-6167-compiler-audit/verify.py`.
It recomputes and compares the entire committed receipt; `--write` is an explicit
regeneration mode. It never regenerates source inputs. The registered boundary
commands additionally execute a temporary Git-free copy with empty `PATH`.

- **Independent arithmetic oracle:** 3,780 instances with bases 1 through 20,
  denominator 1 through 9 and numerator -2d through 2d. Raise both rational
  endpoints to the reduced integer denominator and compare with the exact
  corresponding integer power. This oracle uses neither roots nor logarithms.
- **Coarse arithmetic:** 320 cases deliberately use only 8 fixed-point bits and
  3 exponent bits, including non-dyadic and negative exponents. Seed 78 rotates
  their order; all cases run. Two explicit examples show why a floor-only upper
  root and an omitted exponent tail are invalid.
- **Semantic failures:** 18 pinned-reason controls cover insufficient tail
  offset/reserve, weak decay, nonseparated ranks, bad exit exponent, false gap,
  false rank encoding, incomplete decay blocks, preceding/later threshold
  claims, omitted rank-145 targets, confusing ambient rank with dimension 512,
  power 1012 and four forged intervals. One mutation replaces one paid rank-1
  and rank-3 pair by two rank-2 jobs: count and rank mass stay unchanged, but the
  exact moment reserve fails. Its lower bound proves failure, rather than merely
  failing to certify success.
- **Parser and file boundaries:** four arithmetic/parser rejections, seven
  separately corrupted actual input files, and one corrupted committed receipt.
  Each direct CLI failure must have the expected reason and print no success.

The fixed oracle domain is completely enumerated; there is no candidate search,
solver exclusion, performance claim or numerical root optimization. Source
corruption tests use only temporary copies. Actual commands and remaining
verification limits are recorded in [VALIDATION.md](VALIDATION.md).

## Scope and remaining assumptions

The audited proposition is: **the pinned PR6167 invoice and recipe satisfy the
numerical hypotheses of the two pinned written theorems**. Conditional on those
theorems and their physical premises, the recorded uniform rank has the stated
leaf-count saving. We do not re-prove either compiler theorem, generate its
integer batches, construct the enormous uniform word, recount the scalar word,
replay native maps, execute the physical caller or recompute outer rows.

All five selected framework assumptions remain: `native_all_columns`,
`owned_erasure`, `compiler`, `precision_tape`, and `analytic_recovery`.
The direct invoice totals match the independent receipt, but totals alone
cannot establish word validity. No human peer review, proof-kernel acceptance,
complete rounded multiplier, supplier admission or selected-frontier change is
claimed. **No new κ.**

## Open next questions

1. Bind actual controller batches to the §4 source-size, exit and complement
   premises, with owners, integer multiplicities and suspended-parent chronology
   explicit. A small separated unit and its finite scheduler are a feasible
   starting point; extending it to the actual all-size P104 contract remains
   blocked by the inherited compiler/native interface.
2. A maintainer can reconcile this exact-source numerical coverage with PR6214's
   construction audit and PR6245's outer check. Compare the pinned heads and
   uncovered physical assumptions before any admission. These packages do not
   themselves authorize a new selected result.

## Attribution

Prepared for **@CubeJerry** with substantial **OpenAI Codex assistance** in
proof analysis, implementation, checking and writing. No subagents or human
reviewers were used. Apache-2.0.

Credit Ali Romman (#6167/#5827 and the pricing lineage), DreamingOfClouds
(#6144/#6030/#5907), Matarener (#6214/#5960), JosieElliston (#6109), AAAmirinu
(#6245), zxv and Cao Yifan (moment/compiler bounds), Jacob Alan Sussman
(productive recursion and finite precompilation), Cinna Davis (controller),
pinterbanget (#4425 majorant review), arkfx and Ross Richardson (earlier
integer-root methods), and all native, BIT, outer and analytic contributors
retained in the pinned source packages. The formulas and predecessor theorem
map are credited; the arithmetic implementation here is separately written.
