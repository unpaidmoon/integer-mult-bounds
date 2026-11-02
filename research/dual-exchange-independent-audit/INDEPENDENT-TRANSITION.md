# Independent review: changing dual columns with a fixed row

Research worker A, for @CubeJerry, with substantial OpenAI Codex assistance.
No author junction implementation was imported or read. The fixed original
PR6280 compiler is the only predecessor executable used. The module argument
below is independent of the finite scalar tests.

## Universal module proof

Let A:X→Z, B,D:Z→X be module homomorphisms with AB=AD=I_Z. Let K=B−D,
so AK=0. For S_B(x,z)=((I−BA)x+Bz,Ax), direct composition in chronological
order gives

    S_B ; S_D : (x,z) ↦ (x+K(z−Ax),z).

No maps commute in this derivation. Apply L_(-A), then U_K, then L_A:

    (x,z) → (x,z−Ax) → (x+K(z−Ax),z−Ax)
          → (x+K(z−Ax),z−Ax+A[x+K(z−Ax)])
          = (x+K(z−Ax),z).

Thus the three-block junction is exact over arbitrary modules, including
nonfaithful or torsion modules. A norm or scalar tariff is an additional
source-specialization statement, not part of this module-general identity.

For arbitrary total functions G,H:Z→Z, the fully closed sequence

    S_B;G;S_B;S_D;H;S_D

can replace its middle two exchanges by the junction, retaining **both outer
exchanges and both inner functions**. Its data endpoint is exactly

    x + B(G(Ax)−Ax) + D(H(G(Ax))−G(Ax)),

and the arbitrary original spare z is restored. This is generally not
F_(H∘G) for a single fixed dual column. Omitting the junction leaves the
mismatched single-exchange boundary defect and leaks the arbitrary spare.
The outer columns may differ because the junction explicitly compensates
their difference; this does not contradict the one-use matching-boundary
theorem, whose intervening operation acts only on the spare.

Fixed A, common physical roles/chart and unchanged module meanings are
necessary hypotheses of this stated construction. Different rows require a
different formula. Observing the old returned-consumer boundary between the
removed exchanges is not licensed: the new junction returns the next encoded
state, and the old intermediate returned state is not preserved as an
observation boundary. No mutating intervention or observer/control-flow
contract is supplied. Every native, delivery, chart, ownership, precision and
recursive cost remains outside the scalar saving unless separately proved.

## Complete named invoice and finite independent evidence

For a=(3,5), b=(2,−1), d=(7,−4), the difference is k=(−5,3).
Under the authenticated PR5602 tariff, the coefficient totals are
A_a=26, A_b=18, A_d=28, A_k=26. The source's cheapest exchanges cost
64 and 82. The literal junction costs 2A_a+A_k=78, so the complete two-use
raw scalar allowance decreases from 2·64+2·82=292 to 64+78+82=224.
A fairer comparison first removes the obvious adjacent sign pair: the entering
exchange's last instruction and the leaving exchange's first instruction are
both SCALE(spare,−1). Their composition is identity. Deleting these two
instructions costs no assumptions and gives the sign-peepholed baseline
**288**, versus **224** for the junction, a further allowance saving of **64**.
The corresponding **emitted scalar ADD/SCALE instruction** counts are 26
versus 20 (raw source count28). The junction count includes seven entering,
six junction and seven exiting instructions. These are not primitive
native/Boolean gate counts or an optimal-circuit claim.

The separate checker authenticates source SHA256 and Git blob, plus the
actual caller tariff SHA256. It implements its own exact interpreter,
three-block emission and binary tariff count; it imports no author junction
code or polynomial verifier. All three input basis columns agree with both
literal source exchanges, their sign-peepholed version, and the direct endpoint. For all 125 inputs in
{-2,-1,0,1,2}³ and all 16 ordered pairs from four functions (identity,
square-plus-one, constant-minus-two, absolute-value-minus-two), all 2,000
raw separate, sign-peepholed, junction and direct-formula endpoints agree. This finite scalar
corroboration does not replace the universal module/set-map proof above.

Six discriminators detect reversed difference sign, omitted exit lower
block, omitted junction with dirty spare, a changed common row, the new
coefficient-cap obstruction below, and an observer reading the removed
returned-state boundary. Warning-strict normal and optimized Python produce
identical receipts.

## Coefficient admission and magnitude limits

Even admitted old coefficients can produce an inadmissible difference.
For a=(1,0), b=(1,65534), d=(1,−65534), both dualities hold and every old
emitted coefficient satisfies the actual caller condition |q|+1<65536.
The new difference coefficient 131068 violates it. The new three-block
junction therefore needs its own coefficient-admission check; source
compiler acceptance of both old pairs is insufficient. This explicit case
was independently supplied by worker A and relayed to the author.

For scalar fields with the usual absolute value, a conservative prefix
bound relative to the junction entrance is

    (1+Σ|a_i|)² (1+Σ|b_i−d_i|).

Each lower block has norm at most the first factor before squaring; every
upper-block prefix has norm at most the difference factor. The named bound
is 729. The checker computes every exact scalar-prefix row-sum norm:
4,9,46,46,129,46, so the actual maximum is 129. This establishes no global
macro magnitude/error bound: arbitrary G,H can have unbounded amplification,
and differing common charts or physical field availability remain unproved.

## Reproduction and source pins

Frozen prior public package: 0ff4a9f9cf763d5fa385d674fea915da53792078,
canonical scientific base 2485805a6d47f36ea83ddde6327d453ac82d44dc.
Original compiler: PR6280 4d6e4374d6fdda7df72ddeb19dd6756353383346,
blob 9ead98d5735474d1fd35b101a1f4d50426b7e943. Its author notice remains intact.

    python3 -I -W error -B research/dual-exchange-independent-audit/independent_transition.py --package research/dual-exchange-independent-audit

Expected PASS_INDEPENDENT_CHANGING_COLUMN_JUNCTION, 2,000 nonlinear cases,
288→224 scalar allowance and26→20 emitted instructions after the trivial
SCALE-pair cancellation (raw292/28), plus six discriminators.
Add -O for identical optimized output. The checker uses only the original
source/compiler.py and the pinned external caller tariff; it neither reads
nor imports any new junction implementation.

No blocker was found for this scoped exact endpoint and local invoice result.
No actual selected P104 interval, precision admission, physical caller,
primitive optimality or new κ is established. Credit Nick Petalas for the
source exchange, Ali Romman for the dual interface and tariff, and worker D
for the proposed changing-column contribution. This review supplies a
complementary independent derivation and verifier, not a separate result/PR.
