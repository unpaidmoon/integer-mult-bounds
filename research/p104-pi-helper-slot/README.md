# One helper under Π P_enc Π

**Negative result. No new κ.** Selected κ stays `0.001672660197076918`.

The changed premise is the literal correction \(\Pi P_{\mathrm{enc}}\Pi\), in
place of the old correction \(P\). Open question 1 of
`research/p104-literal-slot-defect` asks whether that operator matches one
helper as well as the data banks, and whether the bill is favorable. This
package prices that question. It does not build an adjacent completed-call pair.

## Result

Let \(H\) be a projection, \(J_0=I-H\), \(T\) and \(D\) invertible, and

\[
L_T=\begin{pmatrix}D&HT\\0&I\end{pmatrix},\quad
P=\begin{pmatrix}I&0\\K&I\end{pmatrix},\quad
\Pi=\begin{pmatrix}J_0&H\\H&J_0\end{pmatrix},\quad
K=T^{-1}.
\]

No commutation between \(D\), \(T\) and \(H\) is required. \(\Pi^2=I\), and
\(Q=\Pi P_{\mathrm{enc}}\Pi\) with \(P_{\mathrm{enc}}=L_TPL_T^{-1}\) satisfies
\(QA_T=A_TP\) for \(A_T=\Pi L_T\). Both \(P\) and \(P_{\mathrm{enc}}\) fail that
identity on a separating state.

The PR #3954 endpoint extends every compatibility map by the identity on the
72 dirty helper roles. On one such coordinate \(h\), \(Q(r,w,h)=(r',w',h)\)
for every dirty \(h\), including 0. Values are restored. \(Q\) fixes the helper
basis vector, so it contributes none of the chart progress.

The published entrance of that helper is the identity chart, 0 of the 81
progress units. The published completed exit is full \(F\), 81 units. Those
charts are not equal, and \(Q\) does not insert the return from \(F\) to the
next identity entrance.

On the pinned mask \(H=\mathrm{diag}(0_8,I_{96})\), \(\Pi\) is 96 disjoint
transpositions and fixes the 8 complementary ports. The scratch-free exchange
\(x\mathrel{+}=y\), \(y\mathrel{-}=x\), \(x\mathrel{-}=y\) realizes each
transposition in three additions. The program costs 288 additions and 0 helper
additions. The first addition is not yet the swap. This is a value permutation,
not a chart transport and not a native-rank lower bound.

The retained scaffold arithmetic, recomputed from the published parameters and
not from a new census, is lower mass \(3009344\) against capacity \(2965248\),
excess \(44096\). That favorable reading already sets the \(\Pi\) occupancy
term to 0. The 288 additions remove none of the counted mass. Counting them as
rank-1 children raises the excess to \(44384\). The one-helper chart gap of 81
does not clear \(44096\) either. The bill is not favorable.

The block argument is [PROOF.md](PROOF.md). `verify.py` checks a 4-port witness
where \(D\) and \(T\) commute with neither each other nor \(H\), the published
104-port mask with \(D=I\), the exchange, the non-projection control, and the
gate integers.

## Scope

Task `p104-side-correction`, scope **refined**. Revision 7 asks for one changed
premise and its literal, dirty, and fully charged boundary. The rows ahead of
this card in the priority table already have open PRs. This premise is the
first open question of the literal-slot package. It is not the scalar
obstruction in #4133, the commutation gap in #4136, the encoding gap in #4140,
the source-chart shortcut in #4153, the fiber-tag seam in #4154, or the
standard-Y consumer in #4159.

Base `12fa8c5c844be21bfefb38a19503fbd867a11244`, priority revision 7.
The published mask and the gate parameters are taken from
`research/p104-two-axis-compatibility/PROOF.md` §§1 and 5. That census is not
replayed. The 104-port machine check uses \(D=I\) and a positive diagonal
\(T\); it is not the physical pivot \(B_0\).

## Reproduce

Python 3.12, standard library, from the repository root:

```sh
python3.12 -B scripts/research_package.py --package research/p104-pi-helper-slot
```

Direct checks:

```sh
python3 -B research/p104-pi-helper-slot/verify.py
python3 -B research/p104-pi-helper-slot/test_verify.py
```

Expected marker:

```text
PASS_P104_PI_HELPER_SLOT swaps=96 additions=288 helper_fixed=1 chart_gap=81 excess=44096 favorable=0 no_new_kappa
```

`test_verify.py` then prints `PASS_P104_PI_HELPER_SLOT_TESTS groups=3`.
The same `verify.py` command passes under `-O`. Not run: Lean, Docker, the
10,816-line census, a native helper schedule, and the selected cold replay.

## Open next questions

1. Does one helper whose published entrance is already \(F\) remove the 81-unit
   chart gap without repaying it, and can that inventory beat excess 44096?
   The first step is to name that role and recompute \(W\). It is blocked by
   the retained contract: every non-data entrance is the identity chart.
2. Can the 96 transpositions be an owner relabeling of tariff 0 instead of
   288 additions? The first step is one physical owner map that identifies
   \(X_N\) with \(Y_N\) at a single port without a move. It is blocked because
   no such map is pinned, and the predecessor proof refuses to grant \(\Pi\)
   as a free relabeling. A zero tariff would still leave excess 44096.

## Credit

The slot swap \(\Pi\), the identity extension on 72 dirty helpers, the
identity-entrance / full-\(F\) contract, and the scaffold gate are Chris R /
Clear1nsight, PR #3954, retained on main as
`research/p104-two-axis-compatibility`. The question of pricing
\(\Pi P_{\mathrm{enc}}\Pi\) on one helper is open question 1 of
`research/p104-literal-slot-defect` (PR #4133). The dimension-free conjugation
used here is the same relation that package recorded and did not price.
Rohan Arun, Chafik Boukhalfa, Adam Gall, and the native P104 lineage named in
PR #3954 remain the source of the endpoint. This package does not import those
programs.

Prepared by unpaidmoon with substantial Cursor Grok assistance. Apache-2.0.
No independent human or formal-kernel review is claimed.
