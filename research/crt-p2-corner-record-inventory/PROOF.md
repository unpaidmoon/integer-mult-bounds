# Record inventory at the two excluded p = 2 corners

This is a finite counting certificate for open question 1 of
`research/crt-arena-batch-threshold`. It keeps that package's full-batch
allowance and replaces only its scalar term. No new kappa is selected.

## Inherited bill

The quantities below are the explicit bill in
`research/crt-arena-root-axis/PROOF.md`, repeated on all `8q` axes as in
`research/crt-arena-batch-threshold/PROOF.md`. For integers `p >= 2` and
`1 <= h <= ell <= p`,

```text
q = p + 2,  N = 2^h,  w = 4q,
A = N^2 + 2 N h^2 + 24 N h + 3 N,
J = N (h^2 + 3 h + 1),
T_tape = A (26 w J + 25 w) + 30 w J + 3 N h + 6 (2 h - 1) N + 3,
T_rot = 9 (ell + 2)^2 N,
T_crt = 65536 q^3 + 1024 q ell^3 + 1024 q^2,
E = 2^{4 ell} q^{16}.
```

`A` is the convenient access majorant from PR #4192 equation (4), not the
smaller exact census. The inherited scalar term charges one schoolbook
product of two `w`-bit words, at most `8 w^2` bit-steps, beside every tape
action:

```text
T_scalar = 8 w^2 T_tape,
U_old = T_crt + 4 (T_rot + T_tape + T_scalar),
B_old = 8 q U_old.
```

The predecessor proof shows `B_old < E` except at exactly
`(p, ell, h) = (2, 1, 1)` and `(2, 2, 2)`. Its displayed values are

```text
(ell, h) = (1, 1):  B_old = 75548846976,       E = 68719476736
(ell, h) = (2, 1):  B_old = 75549780608,       E = 1099511627776
(ell, h) = (2, 2):  B_old = 1241895956864,     E = 1099511627776
```

An excess of `B_old` is not a machine lower bound. The middle `p = 2` triple
is already under `E` and is not an excluded corner.

## Record inventory

PR #4192 section 2, in the vendored proof
`research/crt-arena-root-axis/vendor/pr4192-crt-benes-scan-PROOF.md`, says
that every logical get or put scans all `J` records and compares all four
key words. Section 4 gives the exact pairwise-distinctness count
`N^2 - N - N h / 2` outside those scans. The key-comparison tape motion is
already inside formula (2), hence inside `T_tape`. It is not charged again.

Let

```text
V = N^2 - N - N h / 2,
T_record = 8 w^2 (4 A J + V),
U = T_crt + 4 (T_rot + T_tape + T_record),
B = 8 q U.
```

`N h` is even for every integer `h >= 1`, so `V` is an integer. Each of the
`4 A J + V` comparisons is charged at the same schoolbook cap `8 w^2` the
predecessor used for a `w`-by-`w` product. A streaming equality of two
`w`-bit words is at most `w` bit-steps, and `w < 8 w^2` for `w >= 1`, so
this cap dominates that streaming model. Tape actions stay in `T_tape` at
one bit-step each.

## Theorem

At both excluded corners, `B < E`. The exact values are

```text
(p, ell, h) = (2, 1, 1):
  q = 4, N = 2, w = 16, A = 62, J = 10, V = 1,
  4 A J + V = 2481,
  T_record = 5081088, T_tape = 287541, T_rot = 162, T_crt = 4214784,
  U = 25689948, B = 822078336, E = 68719476736,
  B / E = 6422487 / 536870912 < 1.

(p, ell, h) = (2, 2, 2):
  q = 4, N = 4, w = 16, A = 252, J = 44, V = 8,
  4 A J + V = 44360,
  T_record = 90849280, T_tape = 4734627, T_rot = 576, T_crt = 4243456,
  U = 386581388, B = 12370604416, E = 1099511627776,
  B / E = 96645347 / 8589934592 < 1.
```

The inherited majorant still exceeds `E` at these two triples, with the
values quoted above. So the section-2 replacement is what removes the
excess. Both ratios are comparisons of this explicit majorant. They are
not a lower bound on an arena machine.

## Arithmetic at the two corners

For `(2, 1, 1)`, `A = 4 + 4 + 48 + 6 = 62` and `J = 2 * 5 = 10`. Then
`V = 4 - 2 - 1 = 1` and `4 A J + V = 2480 + 1 = 2481`. The schoolbook cap
is `8 * 16^2 = 2048`, so `T_record = 2481 * 2048 = 5081088`. One access
costs `26 * 16 * 10 + 25 * 16 = 4560` tape actions, and

```text
T_tape = 62 * 4560 + 30 * 16 * 10 + 21 = 282720 + 4800 + 21 = 287541.
```

The tail `21` is `3 * 2 * 1 + 6 * 1 * 2 + 3`. Also
`T_rot = 9 * 3^2 * 2 = 162` and

```text
T_crt = 65536 * 64 + 1024 * 4 * 1 + 1024 * 16 = 4194304 + 4096 + 16384
      = 4214784.
```

Hence

```text
U = 4214784 + 4 (162 + 287541 + 5081088) = 4214784 + 21475164 = 25689948,
B = 32 * 25689948 = 822078336.
```

The allowance is `E = 2^4 * 4^{16} = 2^{36} = 68719476736`. The difference
`E - B = 67897398400` is positive.

For `(2, 2, 2)`, `A = 16 + 32 + 192 + 12 = 252` and `J = 4 * 11 = 44`. Then
`V = 16 - 4 - 4 = 8` and `4 A J + V = 44352 + 8 = 44360`, so
`T_record = 44360 * 2048 = 90849280`. One access costs
`26 * 16 * 44 + 25 * 16 = 18304 + 400 = 18704` tape actions, and

```text
T_tape = 252 * 18704 + 30 * 16 * 44 + 99 = 4713408 + 21120 + 99 = 4734627.
```

The tail `99` is `3 * 4 * 2 + 6 * 3 * 4 + 3`. Also
`T_rot = 9 * 4^2 * 4 = 576` and

```text
T_crt = 65536 * 64 + 1024 * 4 * 8 + 1024 * 16 = 4194304 + 32768 + 16384
      = 4243456.
```

Hence

```text
U = 4243456 + 4 (576 + 4734627 + 90849280) = 4243456 + 382337932
  = 386581388,
B = 32 * 386581388 = 12370604416.
```

The allowance is `E = 2^8 * 4^{16} = 2^{40} = 1099511627776`. The difference
`E - B = 1087141023360` is positive.

## The record term is strictly below the old scalar term

On the whole admissible domain, `N = 2^h >= 2` and `w = 4(p + 2) >= 16`.
The added part of `A` is positive, so `N^2 < A`. Also
`J = N(h^2 + 3 h + 1) >= 10` and `A >= N^2 + 3 N >= 4`. Since `N` is even,
`V = N(N - 1 - h/2)` is an integer. And `2^h >= h + 1`, so
`N - 1 - h/2 >= 1/2` and `V >= 1`. Combined with `N^2 < A`,

```text
V < N^2 < A <= A J,
4 A J + V < 4 A J + A J = 5 A J.
```

The tape invoice keeps its leading piece, so
`T_tape >= A (26 w J) = 26 A w J`. Then `5 < 26 w`, hence
`5 A J < 26 A w J` and

```text
4 A J + V < T_tape.
```

Multiplying by the positive cap `8 w^2` gives `T_record < T_scalar`, and
therefore `B < B_old`, at every admissible triple.

## Corollary, citing the predecessor classification

`research/crt-arena-batch-threshold/PROOF.md` proves `B_old < E` for every
admissible triple other than the two corners above. That argument is not
reproved here. Together with `B < B_old` and the two direct comparisons,
the record inventory satisfies `B < E` for every integer `p >= 2` and
`1 <= h <= ell <= p`.

The corner theorem does not use the `p >= 3` induction. The all-domain
sentence does. Both use the inherited CRT tariff, rotation tariff, tape
invoice, convenient access majorant and maximum of `8q` axes.

## A coefficient-one cell enlargement still fits

Section 4 also says that scan control has `O(B_cells)` elementary
cell iterations per access, where equation (1) sets `B_cells = 5 w J`.
That `O` does not name its constant. The following explicit enlargement
uses coefficient one, plus one extra schoolbook cap for each charged
access and each record:

```text
T_cell = 8 w^2 (4 A J + V + A + J + A * 5 w J).
```

The same comparison as above gives `A + J <= A J` for `A, J >= 2`, so

```text
4 A J + V + A + J + 5 A w J < 6 A J + 5 A w J.
```

This is strictly below `T_tape >= 26 A w J` because `6 + 5 w < 26 w`,
that is `6 < 21 w`, which holds for `w >= 16`. Thus `T_cell < T_scalar`
on the whole admissible domain, and the predecessor classification lifts
any corner fit to every admissible triple.

Direct substitution gives

```text
(2, 1, 1):  operations = 52153,  batch = 13843295104  < 68719476736,
(2, 2, 2):  operations = 931696, batch = 244980412800 < 1099511627776.
```

Coefficient one is not a bound on every constant that could be hidden in
the section-4 `O`. It is a checked enlargement of the section-2 count by
one schoolbook cap per arena cell per charged access.

## What this does not prove

The certificate does not execute the Beneš simulator, emit a scalar
transition table, or count products that the section-2 scan does not name.
Reservoir placement, the paid repair-key service, native execution and the
outer multiplication theorem stay out of scope. The selected frontier is
unchanged. A majorant below `E` does not admit a supplier.
