# One helper under the literal correction Π P_enc Π

## 1. Pinned contract

This note takes the literal-slot correction named by the open question in
`research/p104-literal-slot-defect`, and the helper extension and cost gate
written in `research/p104-two-axis-compatibility/PROOF.md` §§1 and 5. It does
not rerun the 10,816-line census or import either package.

Two data banks have a common finite dimension. \(H\) is a projection,
\(J_0=I-H\), \(T\) is invertible, \(K=T^{-1}\), and \(D\) is invertible. No
hypothesis makes \(D\) commute with \(T\) or with \(H\). The ordered encoding,
the old correction, and the literal slot swap are

\[
L_T=\begin{pmatrix}D&HT\\0&I\end{pmatrix},\qquad
P=\begin{pmatrix}I&0\\K&I\end{pmatrix},\qquad
\Pi=\begin{pmatrix}J_0&H\\H&J_0\end{pmatrix}.
\]

The literal encoding is \(A_T=\Pi L_T\). Since \(H^2=H\), one has \(\Pi^2=I\).
Since \(D\) is invertible, \(L_T\) is invertible, and

\[
P_{\mathrm{enc}}=L_TPL_T^{-1}
\]

satisfies \(P_{\mathrm{enc}}L_T=L_TP\). Conjugating by the involution \(\Pi\)
preserves that relation:

\[
(\Pi P_{\mathrm{enc}}\Pi)\,A_T=A_TP.
\]

The operator that intertwines the literal slots is \(\Pi P_{\mathrm{enc}}\Pi\),
not \(P\) and not \(P_{\mathrm{enc}}\).

The published P104 shape in that proof is \(H=\mathrm{diag}(0_8,I_{96})\).
This note uses that diagonal as a pinned mask. It does not reconstruct the
104 root labels. On this mask \(\Pi\) swaps the two data slots at each of the
96 ports where \(H_{pp}=1\), and it fixes the 8 ports where \(H_{pp}=0\).

## 2. The pinned helper

Section 1 of the same proof extends every compatibility map by the identity
on the 72 arbitrary dirty helper roles. Section 5 says every persistent
entrance other than the \(N=104^2\) data lines is the identity chart, and the
completed contract is full \(F\) on every role. Identity entrances contribute
0 of the 81 chart-progress units. Full \(F\) is 81 units. The difference on
one helper is 81.

Adjoin one such helper coordinate \(h\). Extend \(L_T\), \(P\), \(\Pi\), and
therefore \(P_{\mathrm{enc}}\) and \(Q=\Pi P_{\mathrm{enc}}\Pi\), by the
identity on \(h\). Each factor fixes \(h\), so \(Q\) fixes \(h\). For every
data state and every dirty value of \(h\), including 0,

\[
Q(r,w,h)=(r',w',h)
\]

with \((r',w')\) the data image of the unextended operator. Dirty helper
values are restored. \(Q\) does not move the helper chart: the helper basis
vector is fixed, so this operator contributes none of the 81 progress units.

The published entrance chart of this helper is the identity and the published
completed exit chart is \(F\). Those charts are not equal. An adjacent call
whose entrance is that identity chart therefore does not meet this exit.
\(Q\) does not insert the missing return. The return is not one of the
within-call 81 progress units already counted for arriving at \(F\); those
units assume the call is supposed to finish at \(F\).

## 3. Slot-exchange price of Π

\(\Pi\) is not a free owner relabeling. On an abelian group, each transposed
port \((x,y)\) is realized by the scratch-free exchange

\[
x\mathrel{+}=y,\qquad y\mathrel{-}=x,\qquad x\mathrel{-}=y.
\]

The three steps are additions of an element or its negative. After the first
step the pair is not yet swapped. After the third step it is \((y,x)\), and
every other coordinate, including \(h\) and every fixed \(J_0\) port, is
unchanged. The published mask has 96 transposed ports, so the program uses
288 additions and 0 helper additions. This is a value permutation. It is not
a chart transport and it is not a native-rank lower bound. A tariff of 0 for
the same permutation would be the free relabeling the predecessor proof
refuses to grant; this note does not derive a native lower bound of 288.

## 4. The retained bill

Recompute the published gate from its stated parameters, without a new
census. With \(n=104\), \(N=n^2\), 72 helpers on each of two sides of each
of \(n\) fibers, role count \(W=2N+2n\cdot 72\), and width \(m=81\),

\[
\begin{align*}
P_{\mathrm{total}}&=mW-N,\\
\text{lower mass}&=208\cdot 2576+(P_{\mathrm{total}}-208\cdot 2312),\\
\text{capacity}&=mW.
\end{align*}
\]

The integers are \(W=36608\), \(P_{\mathrm{total}}=2954432\), lower mass
\(3009344\), capacity \(2965248\), excess \(44096\). The predecessor states
this excess under hypotheses (a)–(e) of that section, with the \(\Pi\)
occupancy term set to 0 in order to be favorable. Realizing \(\Pi\) by the
288-addition exchange is an extra nonnegative scalar invoice. It removes
none of the counted local mass or remaining progress. Adding those 288
steps as if they were rank-1 children would raise the excess to 44384, still
above 0. Either reading fails the favorable test \(M<1\) before the separate
helper-chart return.

## 5. What this does not prove

The data intertwiner is an exact linear identity. The helper statement is the
identity extension on one coordinate, not a native helper schedule and not a
proof that all 72 roles have been implemented. The 288-addition count is one
program in the addition alphabet, not a minimum over every physical model.
The excess 44096 is the published scaffold arithmetic, not a new root census
and not a universal P104 obstruction. No \(\kappa\) changes.
