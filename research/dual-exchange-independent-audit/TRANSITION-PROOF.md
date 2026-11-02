# A paid junction for changing dual columns

This extends the same-pair cancellation theorem to two different dual columns
with one fixed row and physical chart. It supplies a concrete local scalar
saving, not a physical P104 installation, a rounding-budget improvement, an
unrestricted circuit optimum, or a new multiplication exponent. **No new κ.**

## Quantified identity and emitted program

Let X,Y be modules, A:X→Y and B,D:Y→X be linear maps with AB=AD=I_Y. All
compositions below are typed; no commutation or coordinate scalar assumption
is needed for the identity. Put E=B−D, so AE=0. With

```
S_B(x,z) = (x+B(z−Ax), Ax),
```

chronological application of S_B then S_D gives

```
R(x,z) = S_D(S_B(x,z)) = (x+E(z−Ax), z).
```

Indeed A(x+B(z−Ax))=z. The second exchange therefore subtracts D(z−Ax)
from the data and returns z to the spare. The following chronological three
shears implement R on arbitrary data and arbitrary dirty spare:

```
L_-A: z ← z−Ax
U_E:  x ← x+Ez
L_A:  z ← z+Ax.
```

The last spare value is z_original−Ax_original+A(x_original+E(z_original−Ax_original))
=z_original because AE=0. This also proves exact data restoration when B=D;
`compile_transition` emits the empty program in that case.

The standalone junction restores its spare but its data generally depend on
that arbitrary spare, exactly as the literal two exchanges do. This is an
internal representation; the dependence disappears only in the complete,
correctly paired outer macro below. It does not contradict PROOF.md's
matching-boundary theorem, which demanded a closed consumer with no dirty-spare
dependence in its data endpoint.

For a scalar row a and columns b,d of common dimension n, `transition.py`
emits the lower ADDs in increasing data-role order, the upper ADDs in increasing
role order, then the final lower ADDs. Within each lower block the data are
unchanged; within the upper block the spare is unchanged. Hence the scalar
sequence implements the three displayed block shears exactly. Every ADD uses
distinct source and target roles. No helper, initialization, erasure, copied
source, extra consumer invocation, or sign SCALE is introduced.

## Complete local macro, not just an endpoint tariff

Consider two closed consumers in one unchanged chart and ownership state:

```
S_B; G1_on_spare; S_B; S_D; G2_on_spare; S_D.
```

Replace only the consecutive middle two exchanges by R. All outer exchanges
and both consumers remain. This is valid for arbitrary functions G1,G2 on Y,
since the junction identity holds on every incoming state. In particular,
writing w0=Ax, w1=G1(w0), w2=G2(w1), the complete output is

```
(x+B(w1−w0)+D(w2−w1), z).
```

For k consumers with one fixed A and columns B_i, the same induction gives
`(x+Σ_i B_i(w_i−w_(i−1)),z)` and an allowance comprising the first and last
outer exchange, each chosen interior junction, and every paid consumer call.
This is an accounting identity, not a claim that all junctions are cheaper.

There must be no externally visible observation, modification, native call,
frame transition, ownership transition, or source-access obligation *inside*
the replaced junction. In particular, the intermediate state after the first
of its original exchanges is generally not preserved. Any permission for an
observer requires its own established invariant; this construction supplies
none. Chart preparation and all required work outside the junction remain
paid. Existing rounded/conditioned interfaces do not inherit a better error
budget merely from this exact endpoint equality.

## Source-bound scalar allowance and a concrete saving

The frozen PR6280 emitter is head
`4d6e4374d6fdda7df72ddeb19dd6756353383346`, authenticated through ORIGIN.json
and SHA256 `9d7b71ed4da90360f8a0f15b7a89599340efbb4eb1ff40054e11e621f85df5bf`.
The actual PR5602 caller tariff and coefficient admission are in canonical
`research/p104-coupled-helper-bases/local.py`, SHA256
`5f0678c768544517780d3511995faf0d7062748e7e780c0adb5c4d9c2749a925`, at base
`2485805a6d47f36ea83ddde6327d453ac82d44dc`. The earlier published
independent audit package is commit `0ff4a9f9cf763d5fa385d674fea915da53792078`;
this extension retains its source pins.

Let c(v) be the sum of the source's nonzero ADD tariffs for vector v. The
source's cheapest of its two exchange factorizations costs
`B_v=2+c(a)+c(v)+min(c(a),c(v))`. A nonzero transition costs exactly
`J=2c(a)+c(b−d)` and has `2 nnz(a)+nnz(b−d)` scalar ADDs. For zero difference
J=0 and there are no operations. The complete two-consumer comparison is

```
old: 2(B_b+B_d) + cost(G1)+cost(G2)
new: B_b+J+B_d + cost(G1)+cost(G2).
```

For `a=(3,5), b=(2,−1), d=(7,−4)`, both pairings equal one,
`E=(−5,3)`, and exact source pricing gives:

| Quantity | Value |
|---|---:|
|c(a), c(b), c(d), c(E)|26, 18, 28, 26|
|B_b, B_d, J|64, 82, 78|
|Junction allowance before → after|146 → 78|
|Complete macro allowance before → after|292 → 224|
|Complete macro scalar ADD/SCALE instructions before → after|28 → 20|
|Complete allowance after cancelling adjacent original signs → replacement|288 → 224|
|Instructions after cancelling adjacent original signs → replacement|26 → 20|

The scientifically stronger comparison first performs the obvious source
peephole: the last instruction of the inner S_B and the first instruction of
the inner S_D are both `SCALE(spare,spare,-1)`, so they cancel. The verifier
checks those exact emitted operations, removes precisely those two operations,
and compares every input basis column with both the raw and replacement
junctions. This reduced baseline costs 288 with 26 instructions. **The
replacement therefore saves 64 scalar allowance units even after the obvious
sign cancellation, reducing 288→224 and 26→20 instructions.**

The raw source-emission comparison remains 292→224, saving 68 units and
28→20 instructions. Both comparisons retain all inner work and both outer
exchanges. Neither baseline is claimed to be the globally cheapest circuit.
The instruction counts are not primitive native or Boolean gate counts.

The rewrite is not uniformly cheaper. For `a=(1,0), b=(1,1), d=(1,2^-32)`,
the difference `1−2^-32` has a dense numerator: the literal two-exchange tariff
is 132 but the three-shear tariff is 212. The verifier reproduces both valid
endpoints and this unfavorable comparison. Callers must compare complete
admissible local budgets rather than selecting the three-shear form blindly.
No search over arbitrary circuits was conducted.

## Admission and scalar-prefix control

Inputs satisfy the source compiler's exact dyadic interface: dimension at most
16, numerator magnitude at most 64 bits, denominator a power of two with at
most 33 bits, and both exact dual pairings. The difference is checked against
these bounds separately; subtraction can increase numerator size. A separate
control uses `a=(1,0), b=(1,2^64−1), d=(1,−(2^64−1))`: both old pairs
pass the compiler interface, but E has a 65-bit numerator and is rejected
before the physical-growth check. This example concerns compiler admission,
not admission by the stricter physical caller.

The actual physical caller additionally requires `|q|+1<2^16` for every scalar
coefficient. The new compiler checks that condition for every emitted a and E
coefficient. This does not assert that arbitrary input b and d satisfy that
physical caller: the verifier separately checks every actual baseline
coefficient for the compared fixtures. For example, `a=(1,0), b=(1,65534),
d=(1,−65534)` consists of individually caller-admitted pairs, yet its difference
131068 fails the caller's growth admission. The replacement is rejected;
the source's admission is not widened. When E=0 no scalar coefficient is emitted.

Write α=1+Σ|a_i| and ε=1+Σ|E_i|. Every partial scalar lower block has infinity
operator norm at most α, and every partial upper block at most ε. Therefore
every scalar prefix of the replacement has amplification at most `α² ε`.
This bound includes the partial restoration block, which cannot be ignored.
For the named fixture α=ε=9, so the bound is 729; exact coefficient-row replay
finds actual maximum 129, the same as the original cheapest two-exchange
junction. In the final lower block a partial spare row is `(45,70,−14)`, whose
absolute row sum is 129, before the final spare returns to its input value.
The separate scalar-section bounds compose with whatever amplification
contracts the unchanged G_i actually provide. No uniform bound is asserted
for arbitrary nonlinear functions, and no unchanged rounded budget is claimed.

## Reproduction, review, and limits

```sh
python3 -I -W error -B research/dual-exchange-independent-audit/verify_transition.py
python3 -I -W error -B -O research/dual-exchange-independent-audit/verify_transition.py
```

Expected receipt: `PASS_SOURCE_BOUND_CHANGING_DUAL_TRANSITION`, complete
allowance `288→224` after adjacent-sign cancellation (`292→224` raw),
instructions `26→20` (`28→20` raw), and eight rejection/discrimination
controls. The checker authenticates source bytes before execution, extracts
the actual tariff expression, checks six exact fixtures through all nine
pairs of source emitter modes (54 comparisons), checks 125 arbitrary-spare
states, and compares 375 complete nonlinear macros with direct substitution.
Fixture dimensions include 1, 2, 3 and the maximum 16; dyadic coefficients,
zero differences and an unfavorable tariff are included. The fixed fixture
suite is corroboration of the all-module proof, not a universal finite search.
Track seed 28 selects the task; no random seed is used. The stopping rule is
one valid completely priced source-bound improvement, not circuit optimization.

Negative controls cover false duality, coefficient-cap and difference-numerator
overflow, nondyadic and
inexact input, missing restoration, reversed transition direction, and an
observation at an eliminated boundary. No P104 caller interval is installed;
source and chart admission, observational compatibility, native costs, recursive
interfaces and any rounded implementation still require actual-caller proof.
The selected κ and all five inherited framework assumptions are unchanged.

Credit Nick Petalas for the PR6280 exchange compiler and Ali Romman for the
retained PR5602 tariff caller, with the earlier audit's full construction lineage
unchanged. Jerry Chen, @CubeJerry; substantial OpenAI Codex assistance from
worker D (construction and source-bound verifier), the lead (junction proposal
and independent coefficient-prefix check), and worker A (independent universal
identity and complete-cost review). Independent human/formal-kernel acceptance
is not claimed.
