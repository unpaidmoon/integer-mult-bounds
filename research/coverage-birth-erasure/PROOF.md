# Surviving birth cannot exceed the initial frame

This note answers the non-nested erasure question left by
`research/three-bank-restored-unpaid`. The selected width is `m = 73`. No new κ.

## Ledger

Let `A_0, ..., A_t` be subspaces of a space of dimension `m`. Write

```text
rank(A, B) = dim(A + B) - dim(A ∩ B).
```

When `A ⊆ B`, this is `dim(B) - dim(A)`. That is the nested Fourier-rank rule in
`research/split-centres-global/proofs/INHERITED-COMPLEX-GEOMETRY.txt`: a nested
transition has Fourier rank equal to the dimension difference. The same formula
is used below for frames that are not nested. It is a dimension count, not a
claim that the compiler realizes it off the nested hypothesis.

The surviving birth space is `U_t = A_0 ∩ ... ∩ A_t`. Its dimension is the
unpaid count. The naive endpoint count is only `dim(A_0 ∩ A_t)`.

## Step lemma

If `U ⊆ A`, then

```text
dim(U) - dim(U ∩ B) ≤ dim(A) - dim(A ∩ B).
```

The left side is `dim(U / (U ∩ B))` and the right side is `dim(A / (A ∩ B))`.
Inclusion carries `U` into `A` and `U ∩ B` into `A ∩ B`. A class that becomes
zero in `A / (A ∩ B)` is represented by a vector of `U ∩ (A ∩ B) = U ∩ B`, so
the induced map of quotients is injective.

## Paid-rank induction

For every `k`,

```text
sum_{i < k} rank(A_i, A_{i+1}) ≥ dim(A_k) - dim(U_k).
```

The case `k = 0` is `0 ≥ 0`. Assume the inequality at `k`. The next transition
splits as entering rank plus leaving rank:

```text
entering = dim(A_{k+1}) - dim(A_k ∩ A_{k+1}),
leaving  = dim(A_k) - dim(A_k ∩ A_{k+1}),
rank     = entering + leaving.
```

The identity `dim(A_{k+1}) - dim(A_k) = entering - leaving` turns the desired
increment into `entering - leaving + dim(U_k) - dim(U_{k+1})`. Subtracting that
from `rank` leaves

```text
2 · leaving - (dim(U_k) - dim(U_{k+1})).
```

Here `U_{k+1} = U_k ∩ A_{k+1}` and `U_k ⊆ A_k`, so the step lemma bounds the
dropped birth dimension by `leaving`. The difference is at least `leaving`,
hence nonnegative.

## Line birth

`U_t ⊆ A_0`, so `dim(U_t) ≤ dim(A_0)`. The same bound holds for the naive count,
because `A_0 ∩ A_t ⊆ A_0`. A one-dimensional birth therefore has unpaid count
at most 1, and naive endpoint intersection at most 1, for every finite history.
Erasing the birth line makes `U_t = 0`. No second direction can survive inside
a one-dimensional birth space, nested or not.

If the last frame is the whole space, the induction gives paid rank at least
`m - dim(U_t)`. A line birth that keeps its direction therefore still pays at
least `m - 1 = 72` to reach the full frame. That is the `72W` term of the
coverage identity. An erasure does not reduce it below 72, and it does not
produce the two-unpaid deficit.

## Explicit erasure

On `F_2^73`, take `A_0 = ⟨e_0⟩`, `A_1 = ⟨e_1⟩`, and `A_2` the whole space.
The birth line is missing from `A_1`, so the unpaid count is 0. The naive
intersection `dim(A_0 ∩ A_2)` is 1: the line was rewritten into the endpoint.
The charges are `rank(A_0, A_1) = 2` and `rank(A_1, A_2) = 72`, summing to 74,
which is at least `73 - 0`. The rewritten line is one of the 72 directions
entering at the last step. It is not a second unpaid coordinate.

A plane birth `⟨e_0, e_1⟩` contained in every later frame does have unpaid
count 2. That is a different initial frame, the plane-port contract, not an
erasure of the selected line.

## What this does not say

The nested Fourier sentence is not a theorem about non-nested compiler steps.
A physical step cheaper than `rank(A, B)` would be a different acquisition
cost. It still could not make `dim(U_t)` or `dim(A_0 ∩ A_t)` equal 2 while
`dim(A_0) = 1`. Cheaper acquisition is not the two-unpaid lever.

The plane-port copy budget, the selected ceiling, and the current selected κ
are not recomputed.
