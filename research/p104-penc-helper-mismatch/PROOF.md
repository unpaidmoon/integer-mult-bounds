# Helper mismatch for the literal correction \(\Pi P_{\mathrm{enc}}\Pi\)

## Statement

Let the two data banks have the same finite dimension. Let \(H\) be a projection,
\(J_0=I-H\), and let \(T\) be invertible with \(K=T^{-1}\). Let \(D\) be invertible.
No step below requires \(HT=TH\). Define
\[
L=\begin{pmatrix}D&HT\\0&I\end{pmatrix},
\qquad
\Pi=\begin{pmatrix}J_0&H\\H&J_0\end{pmatrix},
\qquad
A=\Pi L,
\qquad
P=\begin{pmatrix}I&0\\K&I\end{pmatrix},
\]
and \(P_{\mathrm{enc}}=LPL^{-1}\), \(R=\Pi P_{\mathrm{enc}}\Pi\).

1. If \(H^2=H\), then \(\Pi^2=I\) and \(RA=AP\). On the two data banks, \(R\) is an
   intertwiner of the literal encoding \(A\). The old correction \(P\) is not.
2. Extend \(R\) by the identity on helper coordinates, as PR #3954 extends every
   compatibility map by the identity on the 72 dirty roles. The extension fixes
   every helper value.
3. The same source's completed-role chart \(F\) is not a scalar multiple of the
   identity entrance. The identity extension therefore does not carry one helper
   from that entrance to that exit.
4. For the stated shape \(H=\mathrm{diag}(0_8,I_{96})\), one factor \(\Pi\)
   exchanges 96 N-port slots and fixes the 8 J-port slots. It does not move
   helpers. Realizing \(R\) as \(\Pi\), then \(P_{\mathrm{enc}}\), then \(\Pi\)
   uses 192 N-port exchanges and still fixes helpers.
5. Under the published 208-call hypotheses, the favorable native bill exceeds
   capacity by 44,096 even when every new helper transport and both \(\Pi\)
   realizations are charged zero. The bill is not favorable. Selected \(\kappa\)
   is unchanged.

## Data-bank identity

Since \(H^2=H\) and \(J_0=I-H\), one has \(HJ_0=J_0H=0\), \(J_0^2=J_0\) and
\[
\Pi^2
=
\begin{pmatrix}J_0+H&0\\0&H+J_0\end{pmatrix}
=I.
\]
\(L\) is invertible because \(D\) is: \(L^{-1}=\begin{pmatrix}D^{-1}&-D^{-1}HT\\0&I\end{pmatrix}\).
By construction \(P_{\mathrm{enc}}L=LP\). Therefore
\[
RA=\Pi P_{\mathrm{enc}}\Pi\cdot\Pi L=\Pi P_{\mathrm{enc}}L=\Pi LP=AP.
\]
The same cancellation fails if \(H\) is not a projection, because then the
formula for \(\Pi\) need not satisfy \(\Pi^2=I\). It does not use
\(HT=TH\). The ordered commutator \(PL-LP\) can still be nonzero; that is a
different identity, already recorded for the old correction.

On a literal input, \(P\) itself fails \(PA=AP\) as soon as the first-bank
defect \(-HKa\) is nonzero. Replacing \(P\) by \(R\) removes that data-bank
defect and does not act on helpers.

## Helpers and the two pinned charts

PR #3954, §1, extends every compatibility map by the identity on the 72
arbitrary dirty roles. That extension preserves helper information. It is not
a helper-chart transport. Write a joint state as \((r,w,h)\) and
\[
R_{\mathrm{full}}(r,w,h)=(R(r,w),h).
\]
Every helper coordinate of \(R_{\mathrm{full}}\) equals the input coordinate.

§5 of that proof pins the charts used here. Every persistent entrance other
than the data-pair source is the identity. The completed all-role contract is
full \(F\) on every physical role, including each helper. §4 records
\[
C_u=\frac{(1+i)I+(1-i)X_u}{2}
\]
and the normalization identity
\[
i^{\mathrm{wt}(u)}Z_u(FC_u^{-2})Z_u=F.
\]
On one address bit let \(X=\begin{pmatrix}0&1\\1&0\end{pmatrix}\) and
\(Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix}\). Then \(C^2=X\) and \(X^2=I\), so
\(C^{-2}=X\). Also \(ZXZ=-X\), hence
\[
iZXZ=-iX\neq I.
\]
If \(F=\lambda I\), the normalization identity would require \(iZXZ=I\).
It does not. So \(F\) is not a scalar multiple of the entrance chart \(I\).
\(R_{\mathrm{full}}\) therefore does not carry a helper from the identity
entrance to the completed exit.

If two calls already present the same helper state, \(R_{\mathrm{full}}\)
preserves that equality. The operator does not create equality between \(I\)
and \(F\).

## What one \(\Pi\) moves

\(\Pi(r,w)=(J_0r+Hw,\; Hr+J_0w)\). On a coordinate with \(H_{pp}=0\) the two
banks stay in place. On a coordinate with \(H_{pp}=1\) the two banks are
exchanged. For \(H=\mathrm{diag}(0_8,I_{96})\) that is 96 exchanges. The 72
helpers are not coordinates of \(\Pi\).

The factorization \(R=\Pi P_{\mathrm{enc}}\Pi\) therefore has two N-port
exchange layers, 192 exchanges in total, whenever both factors are realized
as slot exchanges and \(P_{\mathrm{enc}}\) is applied between them. Helpers
remain fixed. This count is not the 96-per-fiber factor-word swap count of
the \(D\)-factorization in the encoded-boundary audit. That word is a
different operator.

These exchanges are logical slot counts. They are not a native rank tariff
and they are not granted as owner relabelings.

## Inherited bill

The published hypotheses are 208 local calls, rank mass 2,576 each, persistent
progress at most 2,312 each, \(104^2\) data pairs, 72 helpers per fiber in two
disjoint banks, and ambient rank 81. Recomputing those integers gives
\[
\begin{aligned}
W&=2\cdot104^2+2\cdot104\cdot72=36608,\\
\text{capacity}&=81W=2965248,\\
\text{remaining}&=81W-104^2-208\cdot2312=2473536,\\
\text{bill}&=208\cdot2576+2473536=3009344,\\
\text{excess}&=44096.
\end{aligned}
\]
This is the same gate arithmetic as PR #3954, evaluated again from the stated
integers. It is not a new root census. The hypotheses set every new interface
cost, including helper transport and both \(\Pi\) layers, to zero. The excess
remains. Charging the 192 exchanges, or a genuine \(I\to F\) helper transport,
adds a nonnegative obligation; it does not remove the excess. For
\(0\le a<1\) and child rank \(r\le 81\), \((r/81)^{1-a}\ge r/81\), so the same
strict inequality holds for that moment comparison. No new \(\kappa\) follows.

## What this does not prove

It does not exhibit a pair whose helper entrance already equals its exit, and
it does not forbid a helper map other than the identity. A changed owner
inventory, coverage law, or local profile needs its own gate. Linear slot
counts are not native-call lower bounds. The 10,816-line census is not
rerun. Lean, Docker, and a selected cold replay are not run.
