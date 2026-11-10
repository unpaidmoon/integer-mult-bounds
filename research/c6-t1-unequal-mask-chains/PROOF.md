# Unequal T1 masks are joined by a monotone chain

No new κ. In the unsigned six-source characteristic-6 floor model, every
legal endpoint pair whose masks differ is realized by a floor word that
keeps the multiset `(6,6,6,7,7,7)` at every diagonal index `s = 4,...,18`.
There are 2280 such pairs. The selected conditional κ stays
`781451/250000000`.

This is an exhaustive finite census of those pairs, with an explicit word
for each pair. It is not a search that failed, and it is not a statement
about weight-3 shapes outside this multiset. The equal-mask pairs are the
120 words already constructed in PR #7042. They are not recounted here.

## 1. Hypotheses carried from the endpoint lemmas

A floor word has length 36 and calls each of six sources exactly six times.
`q_t` is the count of the first `t` letters, and

```text
S(s) = q_s + q_{39-s}.
```

The one-step identity, for `s = 4,...,17`, is

```text
S(s+1) = S(s) + e_{w_s} - e_{w_{38-s}}.
```

PR #7042 proves two facts that this note uses and that `verify.py` rechecks
on their finite domains.

**Lemma 1.** If `S(18)` is a permutation of `(6,6,6,7,7,7)`, then
`q_18 = (3,3,3,3,3,3)` and the three coordinates equal to 7 are exactly the
three bridge letters in positions 18, 19 and 20. There are 20 such splits.

**Lemma 2.** If `S(4)` is a permutation of `(6,6,6,7,7,7)`, write
`M_4` for its mask and `D` for the final letter. Either `D` is outside
`M_4` and `q_4` is 1 on `M_4 ∪ {D}`, or `D` is in `M_4` and `q_4` is 2 at
`D` and 1 on the rest of `M_4`. There are 60 pairs of each type, and every
pair `(M_4, D)` occurs once.

The recheck visits every row assignment in the four-row table of Lemma 1
and every vector of sum 4 in `{0,...,6}^6` against every final letter. The
counts are 20 and 120, with no extra shape.

## 2. Budgets

Fix masks `M_4` and `M_18` and a final letter `D`. Let `p = q_4` be the
vector in Lemma 2, let `b` be the indicator of `M_18`, and let `d` be the
indicator of `D`. The letters still to place are 14 early letters, in
positions 4 through 17, and 14 late letters, in positions 21 through 34.
Their per-source budgets are

```text
e = (3,3,3,3,3,3) - p,
l = (3,3,3,3,3,3) - d - b.
```

Every coordinate of `p` is 0, 1 or 2, so `e` is positive. Every coordinate
of `d` and of `b` is 0 or 1, so `l` is positive: the smallest entry is 1,
when `D` lies in `M_18`. The sums are `∑ p = 4`, `∑ b = 3` and `∑ d = 1`,
hence `∑ e = ∑ l = 14`. These formulas are checked on every orbit
representative.

A chain step consumes one early letter `a` and one late letter `b`.

- If `a = b`, the mask is unchanged.
- If `a ≠ b`, the step is legal only when `a` is currently a 6 and `b` is
  currently a 7. The mask then loses `b` and gains `a`.

Either step preserves the multiset `(6,6,6,7,7,7)`. After 14 steps the
budgets are exhausted.

## 3. From a path to a word

Given such a path `(a_t, b_t)` for `t = 0,...,13`, build

```text
prefix + (a_0,...,a_13) + sorted(M_18) + (b_13,...,b_0) + (D).
```

The prefix is the increasing list `M_4 ∪ {D}` when `D` is outside `M_4`,
and `(D, D, u, v)` with `u < v` the other two mask sources when `D` is in
`M_4`. Position `4+t` holds `a_t` and position `34-t` holds `b_t`. The
bridge is positions 18, 19 and 20. It lies in every late prefix used by
`s = 4,...,17`, so it cancels in the one-step difference. It contributes
to `S(18)` exactly once.

The call count of source `j` is `p_j + e_j + b_j + l_j + d_j = 6`. The
length is `4 + 14 + 3 + 14 + 1 = 36`. Starting from the Lemma-2 vector
`S(4)`, the path rule keeps the multiset through `s = 18`, and the final
mask is `M_18` because the bridge indicator is `b` and `q_18 = p + e` is
identically 3. The program checks `q_18`, both endpoint masks, and the
multiset at every `s = 4,...,18`, rather than trusting this paragraph alone.

## 4. The ten orbits

Two unequal triples `(M_4, D, M_18)` and `(M_4', D', M_18')` lie in one
orbit of the symmetric group on the six sources when they have the same
intersection size and `D` lies in the same combination of the two masks.
The sources then split into four regions whose sizes depend only on that
intersection size `k`:

| region | size |
|---|---:|
| `M_4 ∩ M_18` | `k` |
| `M_4 \ M_18` | `3-k` |
| `M_18 \ M_4` | `3-k` |
| neither | `k` |

For `k = 0` the regions `both` and `neither` are empty, so `D` lies in
exactly one mask. The other two intersection sizes admit all four
membership patterns. That is ten nonempty classes. Their sizes, from
listing every pair, are

| intersection | `D` in `M_4` | `D` in `M_18` | pairs |
|---:|---|---|---:|
| 0 | no | yes | 60 |
| 0 | yes | no | 60 |
| 1 | no | no | 180 |
| 1 | no | yes | 360 |
| 1 | yes | no | 360 |
| 1 | yes | yes | 180 |
| 2 | no | no | 360 |
| 2 | no | yes | 180 |
| 2 | yes | no | 180 |
| 2 | yes | yes | 360 |

The total is 2280. Equal masks are excluded: there are `20 · 6 = 120` of
them, already realized by pure slides.

A permutation that matches the four regions, and sends `D` to `D'`, sends
a realizing word to a realizing word. Masks and the final letter move with
the sources, and the multiset of values of `S(s)` does not change. The
program builds one such permutation for every pair in an orbit and checks
the image word.

## 5. The census

For each of the ten orbits the program searches the budget graph from the
Lemma-2 mask, with the budgets of Section 2. The state is the remaining
early budget, the remaining late budget, and the current mask. Each
coordinate is at most 3, and the mask has three members. Breadth-first
search returns a path of length 14 in every orbit. The assembled
representative keeps the multiset, has `q_18` identically 3, and has the
requested endpoint masks. Transporting that word along the region
bijection succeeds for all 2280 pairs.

The recorded moving word of PR #7042,

```text
012340011223344555014555443322110023
```

is one pair in the intersection-2 class with `D` in neither mask. It is
checked directly. Swapping its first two early letters leaves the
multiset. That is a failure control, not a second census.

No orbit is reported empty. An empty search is not used as a nonexistence
proof, because none occurred. The statement is existence for every pair in
a finite, fully listed domain.

## 6. What this does not say

The alphabet is unchanged. No signed bill is computed, and the selected
frontier is not changed. Lemma 1 still forces `q_18` to be identically 3,
so these words remain outside the `(0, 9)` shape that PR #7029 called
(H1). The other five separation-3 families are not searched. A word that
keeps this multiset is not a classification of every weight-3 diagonal.
