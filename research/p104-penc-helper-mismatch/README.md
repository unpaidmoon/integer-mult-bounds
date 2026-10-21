# Helper mismatch for \(\Pi P_{\mathrm{enc}}\Pi\)

**Negative interface result. No new κ.** Selected κ stays
`0.001672660197076918`.

The literal-slot defect shows that the old correction \(P\) does not intertwine
the literal encoding, and that a uniform scalar cannot cancel the resulting
N-port defect. Its first open question asks whether the changed operator
\(\Pi P_{\mathrm{enc}}\Pi\) matches every helper role as well as both data
banks, and whether that bill is favorable. This package answers that question
for the helper entrance and exit pinned by PR #3954.

## Result

On the two data banks, \(R=\Pi P_{\mathrm{enc}}\Pi\) does intertwine the
literal encoding: \(RA=AP\) whenever \(H\) is a projection and \(D,T\) are
invertible. Commutation \(HT=TH\) is not used. The old correction \(P\) fails
the same identity on the witness.

PR #3954 extends every compatibility map by the identity on the 72 dirty
helper roles. That extension fixes every helper value. The completed-role
chart \(F\) is not an invertible scalar multiple of the identity entrance: on
one address bit, \(C^2=X\) and a nonzero scalar multiple would require
\(iZXZ=I\), while \(iZXZ=-iX\). The zero map is not a chart. So \(R\) matches
the data banks and does not carry a helper from the pinned entrance \(I\) to
the completed exit \(F\).

One factor \(\Pi\) exchanges the 96 N-port slots and fixes the 8 J-port slots.
Realizing both factors around \(P_{\mathrm{enc}}\) is 192 N-port exchanges.
Helpers stay fixed. These are logical slot counts, not a native rank tariff,
and they are not the 96-per-fiber swaps of the separate \(D\)-factor word.

Recomputing the published 208-call integers gives bill \(3009344\) against
capacity \(2965248\), excess \(44096\), with helper transport and both \(\Pi\)
layers charged zero. Added nonnegative exchanges cannot remove that excess.
No new κ.

The block argument is in [PROOF.md](PROOF.md). If two calls already present
the same helper state, the identity extension preserves that match. It does
not create a match between \(I\) and \(F\).

## Scope

Task `p104-side-correction`, scope **refined**. The card asks whether a
changed producer/consumer contract has a favorable full bill. The changed
contract here is the literal correction named by the predecessor, restricted
to one helper entrance/exit and the inherited gate.

Base `12fa8c5c844be21bfefb38a19503fbd867a11244`, priority revision 7.
PR #4133 recorded the scalar obstruction. PR #3954 recorded the literal
operator, the identity extension, and the 44,096 gate. PR #4140 separated
uniform completion from the physical encoding and left the adjacent pair
open. The encoded-boundary factor word's 19,968 slot swaps are a different
operator. This package does not rerun the 10,816-line census.

## Reproduce

Python 3.12, standard library, from the repository root:

```sh
python3.12 -B scripts/research_package.py --package research/p104-penc-helper-mismatch
```

Direct check:

```sh
python3 -B research/p104-penc-helper-mismatch/verify.py
```

Expected marker:

```text
PASS_P104_PENC_HELPER_MISMATCH data=intertwiner helpers=identity_not_F slots=192 excess=44096 no_new_kappa
```

The same command passes under `-O`. Not run: Lean, Docker, a selected cold
replay, the 10,816-line census, and hosted CI.

## Open next questions

1. Can a helper map other than this identity extension carry the identity
   entrance to \(F\) and still cut the inherited excess of 44,096? The first
   step is one legal native transport, its rank tariff, and a gate that names
   the changed profile or coverage hypothesis. It is blocked until that
   transport and that changed hypothesis exist. \(\Pi P_{\mathrm{enc}}\Pi\)
   does not supply them.

## Credit

The literal operator \(\Pi P_{\mathrm{enc}}\Pi\), the 72-role identity
extension, the chart formula, and the 208-call gate are Chris R /
Clear1nsight, PR #3954, from discussion #1166 comment 19034066, retaining
the PR #3882 / #3940 residual boundary and the native P104 lineage named
there. The scalar obstruction and the open question are PR #4133. The
uniform-encoding separation is PR #4140. The dimension-free intertwiner
without a commutation hypothesis, the one-bit normalization witness, the
192-exchange count, and these checks are new.

Prepared by unpaidmoon with substantial Cursor Grok assistance.
Apache-2.0. No independent human or formal-kernel review is claimed.
